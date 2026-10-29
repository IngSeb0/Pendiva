"""Small, dependency-free local MVP for Pendiva's sales signal dashboard.

All bundled records and the demo-message endpoint are synthetic. This module
does not connect to Meta or send WhatsApp messages.
"""

from __future__ import annotations

from datetime import datetime, timezone
from contextlib import closing
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import re
import sqlite3
import unicodedata
from urllib.parse import urlparse

from src.demo_cases import CASES
from src.meta_model import MetaModelError, analyze_case


ROOT = Path(__file__).resolve().parents[1]
STATIC_DIR = ROOT / "src" / "static"
DEFAULT_DB = ROOT / "data" / "pendiva.sqlite3"
MAX_MESSAGE_LENGTH = 2000


def _fold(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text.casefold())
    return "".join(char for char in normalized if not unicodedata.combining(char))


def classify_message(text: str) -> dict[str, str]:
    """Return a transparent, keyword-based signal with its exact evidence."""
    folded = _fold(text)
    rules = (
        ("pago_por_verificar", ("ya pague", "ya realice el pago", "te transferi", "te consigne"),
         "Verificar el pago manualmente."),
        ("objecion_precio", ("muy caro", "esta caro", "me parece caro", "descuento", "bajar el precio"),
         "Revisar la objeción de precio y responder con contexto."),
        ("cotizacion_pendiente", ("cotizacion", "presupuesto", "cuanto cuesta", "cuanto vale", "precio"),
         "Dar seguimiento a la cotización solicitada."),
        ("promesa_de_seguimiento", ("te confirmo", "te envio", "te llamo", "manana te", "paso manana"),
         "Revisar si se cumplió el seguimiento prometido."),
    )
    for signal, phrases, action in rules:
        for phrase in phrases:
            if phrase in folded:
                return {
                    "signal": signal,
                    "action": action,
                    "evidence": text.strip(),
                    "method": "reglas_demo",
                }
    return {
        "signal": "sin_clasificar",
        "action": "Revisar la conversación manualmente.",
        "evidence": text.strip(),
        "method": "reglas_demo",
    }


class DashboardStore:
    def __init__(self, db_path: str | Path):
        self.db_path = str(db_path)

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path, timeout=10)
        connection.row_factory = sqlite3.Row
        return connection

    def initialize(self) -> None:
        if self.db_path != ":memory:":
            Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        with closing(self._connect()) as connection:
            with connection as db:
                db.execute("""CREATE TABLE IF NOT EXISTS events (
                event_id TEXT PRIMARY KEY,
                contact_name TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TEXT NOT NULL,
                signal TEXT NOT NULL,
                action TEXT NOT NULL,
                evidence TEXT NOT NULL,
                method TEXT NOT NULL
            )""")
                db.execute("""CREATE TABLE IF NOT EXISTS demo_case_status (
                    case_id TEXT PRIMARY KEY,
                    status TEXT NOT NULL CHECK (status IN ('pendiente', 'revisado'))
                )""")
                db.executemany(
                    "INSERT OR IGNORE INTO demo_case_status (case_id, status) VALUES (?, 'pendiente')",
                    [(case["id"],) for case in CASES],
                )
                count = db.execute("SELECT COUNT(*) FROM events").fetchone()[0]
                if count == 0:
                    fixtures = [
                        ("demo-001", "Cliente demo 01", "Hola, ¿me compartes la cotización del servicio?"),
                        ("demo-002", "Cliente demo 02", "Me parece muy caro, ¿hay alguna alternativa?"),
                        ("demo-003", "Cliente demo 03", "Ya pagué la reserva, te envío el comprobante."),
                        ("demo-004", "Cliente demo 04", "Perfecto, mañana te confirmo la dirección."),
                    ]
                    for event_id, name, message in fixtures:
                        self._insert(db, event_id, name, message, "demo")

    @staticmethod
    def _insert(db: sqlite3.Connection, event_id: str, name: str, message: str, source: str) -> bool:
        analysis = classify_message(message)
        cursor = db.execute(
            "INSERT OR IGNORE INTO events "
            "(event_id, contact_name, message, created_at, signal, action, evidence, method) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (event_id, name, message.strip(), datetime.now(timezone.utc).isoformat(),
             analysis["signal"], analysis["action"], analysis["evidence"], source),
        )
        return cursor.rowcount == 1

    def add_demo_message(self, event_id: str, contact_name: str, message: str) -> bool:
        if not event_id or len(event_id) > 120:
            raise ValueError("event_id must be between 1 and 120 characters")
        if not contact_name.strip() or len(contact_name) > 80:
            raise ValueError("contact_name must be between 1 and 80 characters")
        if not message.strip() or len(message) > MAX_MESSAGE_LENGTH:
            raise ValueError(f"message must be between 1 and {MAX_MESSAGE_LENGTH} characters")
        with closing(self._connect()) as connection:
            with connection as db:
                return self._insert(db, event_id, contact_name.strip(), message.strip(), "reglas_demo")

    def list_leads(self) -> list[dict[str, str]]:
        with closing(self._connect()) as connection:
            rows = connection.execute("SELECT * FROM events ORDER BY created_at DESC, event_id DESC").fetchall()
        return [dict(row) for row in rows]

    def list_cases(self) -> list[dict]:
        with closing(self._connect()) as connection:
            rows = connection.execute("SELECT case_id, status FROM demo_case_status").fetchall()
        statuses = {row["case_id"]: row["status"] for row in rows}
        return [{**case, "status": statuses.get(case["id"], "pendiente")} for case in CASES]

    def set_case_status(self, case_id: str, status: str) -> bool:
        if status not in {"pendiente", "revisado"}:
            raise ValueError("Estado no válido")
        if case_id not in {case["id"] for case in CASES}:
            return False
        with closing(self._connect()) as connection:
            with connection:
                cursor = connection.execute(
                    "UPDATE demo_case_status SET status = ? WHERE case_id = ?", (status, case_id)
                )
                return cursor.rowcount == 1


class RequestHandler(BaseHTTPRequestHandler):
    store: DashboardStore

    def _json(self, status: int, body: dict | list) -> None:
        encoded = json.dumps(body, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path == "/api/health":
            self._json(200, {"status": "ok", "mode": "demo_synthetic"})
        elif path == "/api/leads":
            self._json(200, self.store.list_leads())
        elif path == "/api/demo/cases":
            self._json(200, self.store.list_cases())
        elif path == "/api/demo/meta-status":
            self._json(200, {"configured": bool(os.environ.get("MODEL_API_KEY", "").strip())})
        elif path == "/":
            content = (STATIC_DIR / "index.html").read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        else:
            self._json(404, {"error": "not_found"})

    def do_POST(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        case_match = re.fullmatch(r"/api/demo/cases/([a-z0-9-]+)/status", path)
        analyze_match = re.fullmatch(r"/api/demo/cases/([a-z0-9-]+)/analyze", path)
        if path != "/api/demo/messages" and not case_match and not analyze_match:
            self._json(404, {"error": "not_found"})
            return
        try:
            origin = self.headers.get("Origin")
            port = self.server.server_port
            if origin and origin not in {f"http://localhost:{port}", f"http://127.0.0.1:{port}"}:
                self._json(403, {"error": "Origen no permitido"})
                return
            if self.headers.get_content_type() != "application/json":
                self._json(415, {"error": "Se requiere JSON"})
                return
            length = int(self.headers.get("Content-Length", "0"))
            if length < 1 or length > MAX_MESSAGE_LENGTH + 512:
                raise ValueError("request body too large")
            payload = json.loads(self.rfile.read(length))
            if not isinstance(payload, dict):
                raise ValueError("request body must be an object")
            if case_match:
                updated = self.store.set_case_status(case_match.group(1), str(payload.get("status", "")))
                self._json(200 if updated else 404, {"updated": updated})
                return
            if analyze_match:
                case = next((item for item in CASES if item["id"] == analyze_match.group(1)), None)
                if case is None:
                    self._json(404, {"error": "Caso no encontrado"})
                    return
                api_key = os.environ.get("MODEL_API_KEY", "").strip()
                if not api_key:
                    self._json(503, {"error": "Falta configurar MODEL_API_KEY en el servidor local."})
                    return
                self._json(200, analyze_case(case, api_key))
                return
            event_id = str(payload.get("event_id") or "").strip()
            if not event_id:
                event_id = f"demo-{os.urandom(8).hex()}"
            added = self.store.add_demo_message(
                event_id,
                str(payload.get("contact_name") or "").strip(),
                str(payload.get("message") or ""),
            )
            self._json(201 if added else 200, {"created": added, "event_id": event_id,
                                               "analysis": classify_message(str(payload["message"]))})
        except (ValueError, TypeError, KeyError, json.JSONDecodeError) as error:
            self._json(400, {"error": str(error)})
        except MetaModelError as error:
            self._json(502, {"error": str(error)})

    def log_message(self, format: str, *args) -> None:
        # Avoid logging message bodies or request payloads.
        print(f"{self.address_string()} {format % args}")


def create_server(host: str = "127.0.0.1", port: int = 8000,
                  db_path: str | Path = DEFAULT_DB) -> ThreadingHTTPServer:
    store = DashboardStore(db_path)
    store.initialize()
    handler = type("PendivaRequestHandler", (RequestHandler,), {"store": store})
    return ThreadingHTTPServer((host, port), handler)


if __name__ == "__main__":
    host = os.environ.get("PENDIVA_HOST", "127.0.0.1")
    port = int(os.environ.get("PENDIVA_PORT", "8000"))
    server = create_server(host, port, os.environ.get("PENDIVA_DB", str(DEFAULT_DB)))
    print(f"Pendiva demo listening on http://{host}:{port} (synthetic data only)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
