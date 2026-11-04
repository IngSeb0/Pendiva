"""Run Pendiva's local panel and isolated sandbox receiver with one command.

No WhatsApp message is sent. --check-model makes one synthetic AI request.
--tunnel exposes only the webhook receiver through the existing cloudflared.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import threading
import time

from src.live_app import create_server
from src.live_pipeline import AnalysisError, LiveStore, analyze_messages
from src.demo_seed import seed_demo
from src.local_config import load_local_config

ROOT = Path(__file__).resolve().parents[1]
KEYS = {"meta": "MODEL_API_KEY"}


def check_config(config: dict) -> dict:
    # Muse is the only supported provider in the product; ignore stale local selections.
    provider = "meta"
    required = ("WHATSAPP_PHONE_NUMBER_ID", "WHATSAPP_VERIFY_TOKEN", "WHATSAPP_APP_SECRET")
    missing = [key for key in (*required, KEYS.get(provider, "PENDIVA_AI_PROVIDER")) if not config.get(key, "").strip()]
    problems = []
    if provider not in KEYS:
        problems.append("Proveedor de IA no admitido.")
    phone = config.get("WHATSAPP_PHONE_NUMBER_ID", "")
    if phone and not re.fullmatch(r"[0-9]+", phone):
        problems.append("WHATSAPP_PHONE_NUMBER_ID debe ser numérico.")
    test_phone = config.get("WHATSAPP_TEST_PHONE_NUMBER_ID", "")
    if phone and test_phone and phone != test_phone:
        problems.append("El emisor del smoke test y el receptor del webhook son distintos.")
    ports = []
    for name, default in (("PENDIVA_PORT", "8000"), ("PENDIVA_WEBHOOK_PORT", "8772")):
        try:
            value = int(config.get(name, default))
            if not 1024 <= value <= 65535:
                raise ValueError
            ports.append(value)
        except ValueError:
            problems.append(f"{name} debe ser un puerto entre 1024 y 65535.")
    if len(ports) == 2 and ports[0] == ports[1]:
        problems.append("Panel y webhook necesitan puertos distintos.")
    return {"configured": not missing and not problems, "provider": provider,
            "missing": missing, "problems": problems, "scope": "sandbox_local"}


def check_model(config: dict, analyzer=analyze_messages) -> dict:
    provider = "meta"
    # Only this fictional text is sent. Never read live conversations here.
    messages = [{"id": "synthetic.demo.quote", "timestamp": 1793188800,
                 "text": "Necesito una cotización de mantenimiento para dos equipos la próxima semana."}]
    result = analyzer(messages, config.get(KEYS.get(provider, ""), ""), provider=provider,
                      business_context={"nombre": "Negocio ficticio de evaluación", "sector": "Servicios"})
    return {"valid": True, "provider": provider, "model": result["model"],
            "recommendations": len(result["recomendaciones"]), "data": "synthetic",
            "checked_at": datetime.now(timezone.utc).isoformat()}


def cloudflared_path(root: Path = ROOT) -> str:
    installed = shutil.which("cloudflared")
    if installed:
        return installed
    candidates = sorted((root / "data").glob("cloudflared-*.exe"), reverse=True)
    if candidates:
        return str(candidates[0])
    raise ValueError("Falta cloudflared. Instálalo desde Cloudflare antes de usar --tunnel.")


def remove_owned_runtime(path: Path, started_at: str) -> None:
    """Do not erase the runtime file of a newer, separately running demo."""
    try:
        runtime = json.loads(path.read_text(encoding="utf-8"))
        if runtime.get("started_at") == started_at:
            path.unlink(missing_ok=True)
    except (OSError, ValueError, AttributeError):
        return


def start_demo(config: dict, tunnel=False, demo_data=False, demo_language="es", demo_no_finance=False):
    panel_port = int(config.get("PENDIVA_PORT", "8000"))
    webhook_port = int(config.get("PENDIVA_WEBHOOK_PORT", "8772"))
    db_path = config.get("PENDIVA_LIVE_DB") or ROOT / "data" / "live.sqlite3"
    servers, threads = [], []
    process = log = None
    runtime_written = False
    runtime_path = ROOT / "data" / "demo-runtime.json"
    executable = cloudflared_path() if tunnel else None
    try:
        if demo_data:
            seeded = seed_demo(LiveStore(db_path), config.get("WHATSAPP_PHONE_NUMBER_ID", "") if tunnel else "",
                               language=demo_language, include_finance=not demo_no_finance)
            print(f"Datos sintéticos cargados: {seeded['conversations']} conversaciones.", flush=True)
            print(f"Usuario demo: {seeded['email']} / {seeded['password']}", flush=True)
        # Both listeners use exactly the same database and startup configuration.
        servers.append(create_server("127.0.0.1", panel_port, db_path, config))
        servers.append(create_server("127.0.0.1", webhook_port, db_path, config, webhook_only=True))
        for server in servers:
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            threads.append(thread)
        runtime = {"panel_url": f"http://127.0.0.1:{panel_port}",
                   "webhook_local": f"http://127.0.0.1:{webhook_port}/webhooks/meta",
                   "started_at": datetime.now(timezone.utc).isoformat(), "public_url": None}
        print(f"Panel: {runtime['panel_url']}", flush=True)
        print(f"Receptor aislado: {runtime['webhook_local']}", flush=True)
        if tunnel:
            log_path = ROOT / "data" / "cloudflared.log"
            log = log_path.open("w", encoding="utf-8")
            kwargs = {"creationflags": subprocess.CREATE_NO_WINDOW} if sys.platform == "win32" else {}
            process = subprocess.Popen([executable, "tunnel", "--url", f"http://127.0.0.1:{webhook_port}",
                                        "--no-autoupdate", "--protocol", "http2"],
                                       stdout=log, stderr=subprocess.STDOUT, **kwargs)
            deadline = time.monotonic() + 40
            while time.monotonic() < deadline:
                if process.poll() is not None:
                    raise RuntimeError("Cloudflared terminó; revisa data/cloudflared.log.")
                found = re.search(r"https://[a-z0-9-]+\.trycloudflare\.com", log_path.read_text(encoding="utf-8", errors="replace"))
                if found:
                    runtime["public_url"] = found.group(0) + "/webhooks/meta"
                    print(f"Callback temporal: {runtime['public_url']}", flush=True)
                    break
                time.sleep(0.25)
            if not runtime["public_url"]:
                raise RuntimeError("Cloudflare no entregó una URL temporal a tiempo.")
        runtime_path.write_text(json.dumps(runtime, indent=2), encoding="utf-8")
        runtime_written = True
        print("Ctrl+C detiene los servicios. No se envían mensajes ni se llama al modelo automáticamente.", flush=True)
        while True:
            if process and process.poll() is not None:
                raise RuntimeError("El túnel terminó. Reinicia la demo y actualiza el callback en Meta.")
            time.sleep(0.5)
    finally:
        if process and process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)
        if log:
            log.close()
        for server, thread in zip(servers, threads):
            server.shutdown()
            thread.join(timeout=3)
        for server in servers:
            server.server_close()
        if runtime_written:
            remove_owned_runtime(runtime_path, runtime["started_at"])


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate configuration without connecting")
    parser.add_argument("--check-model", action="store_true", help="one real AI request with fictional data; may consume credits")
    parser.add_argument("--provider", choices=sorted(KEYS), help="provider for --check-model only; does not change .env")
    parser.add_argument("--tunnel", action="store_true", help="expose the isolated receiver through Cloudflare")
    parser.add_argument("--demo", action="store_true", help="load reproducible fictional customers and conversations")
    parser.add_argument("--demo-db", help="separate SQLite path for fictional demo data")
    parser.add_argument("--demo-language", choices=("es", "en"), default="es", help="language of seeded fictional demo content")
    parser.add_argument("--demo-no-finance", action="store_true", help="leave demo finance empty so an English CSV can be imported")
    args = parser.parse_args(argv)
    if args.provider and not args.check_model:
        parser.error("--provider requiere --check-model")
    try:
        config = dict(load_local_config(ROOT / ".env"))
        if args.demo:
            config["PENDIVA_LIVE_DB"] = args.demo_db or str(ROOT / "data" / "demo.sqlite3")
            config.pop("PENDIVA_AUTH_PASSWORD", None)
            config["PENDIVA_DEMO_MODE"] = "1"
        elif args.demo_db:
            parser.error("--demo-db requiere --demo")
        if args.demo_language != "es" and not args.demo:
            parser.error("--demo-language requiere --demo")
        if args.demo_no_finance and not args.demo:
            parser.error("--demo-no-finance requiere --demo")
        if args.provider:
            config["PENDIVA_AI_PROVIDER"] = args.provider
        report = check_config(config)
        if args.check or (not report["configured"] and (not args.demo or args.tunnel)):
            print(json.dumps(report, ensure_ascii=False, indent=2))
            if not report["configured"]:
                return 1
            if not args.check_model:
                return 0
        if args.check_model:
            result = check_model(config)
            (ROOT / "data").mkdir(exist_ok=True)
            (ROOT / "data" / f"model-check-{result['provider']}.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0
        start_demo(config, args.tunnel, args.demo, args.demo_language, args.demo_no_finance)
    except KeyboardInterrupt:
        print("Demo detenida.")
    except (ValueError, OSError, RuntimeError, AnalysisError) as error:
        if isinstance(error, AnalysisError):
            message = str(error)
        elif isinstance(error, ValueError):
            message = str(error)
        else:
            message = "No se pudo iniciar la demo; comprueba puertos, red y cloudflared."
        print(message, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
