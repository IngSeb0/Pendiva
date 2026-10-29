"""Inspect or update ONLY Pendiva's existing sandbox app callback.

Default is read-only. --apply verifies the running isolated receiver first,
preserves every subscribed WhatsApp field, and uses secrets only in memory.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import secrets
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

from src.local_config import load_local_config

ROOT = Path(__file__).resolve().parents[1]
PENDIVA_APP_ID = "889989257436890"


def graph_request(config, data=None, opener=urlopen):
    app_id = config.get("WHATSAPP_APP_ID", PENDIVA_APP_ID)
    if app_id != PENDIVA_APP_ID:
        raise ValueError("Esta herramienta sólo configura la app Pendiva autorizada.")
    secret = config.get("WHATSAPP_APP_SECRET", "")
    version = config.get("WHATSAPP_TEST_GRAPH_VERSION", "")
    if not secret or not re.fullmatch(r"v[0-9]+\.[0-9]+", version):
        raise ValueError("Faltan WHATSAPP_APP_SECRET o WHATSAPP_TEST_GRAPH_VERSION válidos.")
    request = Request(f"https://graph.facebook.com/{version}/{app_id}/subscriptions",
                      data=urlencode(data).encode() if data is not None else None,
                      headers={"Authorization": f"Bearer {app_id}|{secret}",
                               "Content-Type": "application/x-www-form-urlencoded"})
    with opener(request, timeout=20) as response:
        return json.load(response)


def subscription(config, opener=urlopen):
    rows = graph_request(config, opener=opener).get("data", [])
    matches = [row for row in rows if row.get("object") == "whatsapp_business_account"]
    if len(matches) != 1:
        raise ValueError("No se encontró una única suscripción de WhatsApp existente en Pendiva.")
    row = matches[0]
    fields = [item["name"] for item in row.get("fields", [])]
    return {"app_id": PENDIVA_APP_ID, "callback_url": row.get("callback_url"),
            "active": row.get("active"), "fields": fields}


def validate_receiver(callback, verify_token, opener=urlopen):
    parsed = urlparse(callback)
    if (parsed.scheme != "https" or not re.fullmatch(r"[a-z0-9-]+\.trycloudflare\.com", parsed.netloc)
            or parsed.path != "/webhooks/meta" or parsed.query or parsed.fragment):
        raise ValueError("Se esperaba el callback temporal HTTPS generado para /webhooks/meta.")
    if not verify_token:
        raise ValueError("Falta WHATSAPP_VERIFY_TOKEN.")

    def status(request):
        try:
            with opener(request, timeout=20) as response:
                return response.status, response.read()
        except HTTPError as error:
            return error.code, b""

    challenge = secrets.token_hex(12)
    query = urlencode({"hub.mode": "subscribe", "hub.verify_token": verify_token, "hub.challenge": challenge})
    code, body = status(callback + "?" + query)
    if code != 200 or body.decode() != challenge:
        raise ValueError("El receptor público no respondió correctamente al desafío de verificación.")
    for path in ("/", "/api/status", "/api/conversations", "/api/business"):
        if status(f"https://{parsed.netloc}{path}")[0] != 404:
            raise ValueError("El receptor público expone una ruta que debería estar bloqueada.")
    if status(Request(callback, data=b"{}", headers={"Content-Type": "application/json"}))[0] != 403:
        raise ValueError("El receptor público no rechazó el evento sin firma.")
    return {"challenge": True, "panel_blocked": True, "unsigned_rejected": True}


def configure(config, callback, opener=urlopen):
    current = subscription(config, opener)
    checks = validate_receiver(callback, config.get("WHATSAPP_VERIFY_TOKEN", ""), opener)
    fields = sorted(set(current["fields"]) | {"messages"})
    result = graph_request(config, {"object": "whatsapp_business_account", "callback_url": callback,
                           "verify_token": config["WHATSAPP_VERIFY_TOKEN"], "fields": ",".join(fields)}, opener)
    if result.get("success") is not True:
        raise ValueError("Meta no confirmó el cambio del callback.")
    updated = subscription(config, opener)
    if updated["callback_url"] != callback or not updated["active"] or set(updated["fields"]) != set(fields):
        raise ValueError("La lectura posterior no confirmó la configuración esperada.")
    return {**updated, "receiver_checks": checks}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="update callback to data/demo-runtime.json after public checks")
    args = parser.parse_args(argv)
    try:
        config = load_local_config(ROOT / ".env")
        if args.apply:
            runtime = json.loads((ROOT / "data" / "demo-runtime.json").read_text(encoding="utf-8"))
            callback = runtime.get("public_url")
            if not isinstance(callback, str):
                raise ValueError("Inicia primero python -m scripts.iniciar_demo --tunnel.")
            result = configure(config, callback)
        else:
            result = subscription(config)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except HTTPError as error:
        print(f"Meta o el receptor devolvió HTTP {error.code}; revisa acceso y configuración.", file=sys.stderr)
    except (OSError, URLError):
        print("No se pudo conectar o falta el estado local de la demo.", file=sys.stderr)
    except (ValueError, KeyError, TypeError):
        print("La configuración no se pudo validar; comprueba la app, el receptor y las variables requeridas.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
