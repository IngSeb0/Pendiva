"""Single-operator local dashboard and Meta webhook for a sandbox pilot.

Run behind a proxy that exposes ONLY /webhooks/meta; the dashboard is local.
This development server has no user authentication and is not production ready.
"""
from __future__ import annotations

import base64
import binascii
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import hmac
import json
import os
from pathlib import Path
import re
from urllib.parse import parse_qs, urlparse

from src.live_pipeline import AnalysisError, LiveStore, analyze_messages, parse_statuses, parse_webhook, summarize_webhook, verify_signature
from src.business_assistant import ask, get_history, init_assistant
from src.local_config import load_local_config
from src.voice import DEFAULT_VOICE, VoiceError, synthesize, transcribe

ROOT = Path(__file__).resolve().parents[1]
MAX_BODY = 262144


def create_server(host="127.0.0.1", port=8000, db_path=None, environ=None, webhook_only=False):
    config = dict(os.environ if environ is None else environ)
    provider = config.get("PENDIVA_AI_PROVIDER", "meta").strip().lower()
    store = LiveStore(db_path or ROOT / "data" / "live.sqlite3")
    store.initialize()
    init_assistant(store)

    class Handler(BaseHTTPRequestHandler):
        def setup(self):
            super().setup()
            self.connection.settimeout(10)

        def local_host_allowed(self):
            # Only the isolated receiver accepts an arbitrary public tunnel host.
            host_header = self.headers.get("Host")
            return webhook_only or not host_header or host_header in {
                f"localhost:{self.server.server_port}", f"127.0.0.1:{self.server.server_port}"}

        def respond(self, code, data, content_type="application/json; charset=utf-8"):
            body = data if isinstance(data, bytes) else json.dumps(data, ensure_ascii=False).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'")
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            if not self.local_host_allowed():
                self.respond(403, {"error": "invalid_host"})
                return
            parsed = urlparse(self.path)
            if webhook_only and parsed.path != "/webhooks/meta":
                self.respond(404, {"error": "not_found"})
                return
            if parsed.path == "/webhooks/meta":
                params = parse_qs(parsed.query)
                token = params.get("hub.verify_token", [""])[0]
                expected = config.get("WHATSAPP_VERIFY_TOKEN", "")
                if (expected and params.get("hub.mode", [""])[0] == "subscribe"
                        and hmac.compare_digest(token, expected) and params.get("hub.challenge")):
                    self.respond(200, params["hub.challenge"][0].encode(), "text/plain; charset=utf-8")
                else:
                    self.respond(403, {"error": "verification_failed"})
            elif parsed.path == "/":
                self.respond(200, (ROOT / "src" / "static" / "live.html").read_bytes(), "text/html; charset=utf-8")
            elif parsed.path == "/api/status":
                provider_keys = {"meta": "MODEL_API_KEY", "nvidia": "NVIDIA_API_KEY", "nebius": "NEBIUS_API_KEY"}
                self.respond(200, {"webhook_configured": all(config.get(k) for k in
                             ("WHATSAPP_VERIFY_TOKEN", "WHATSAPP_APP_SECRET", "WHATSAPP_PHONE_NUMBER_ID")),
                             "muse_configured": provider == "meta" and bool(config.get("MODEL_API_KEY")),
                             "ai_provider": provider,
                             "ai_configured": bool(config.get({"meta": "MODEL_API_KEY", "nvidia": "NVIDIA_API_KEY", "nebius": "NEBIUS_API_KEY"}.get(provider, ""))),
                             "ai_providers": {name: bool(config.get(key)) for name, key in provider_keys.items()},
                             "elevenlabs_configured": bool(config.get("ELEVENLABS_API_KEY")),
                             "provider": "Meta Cloud API", "mode": "live",
                             "ingestion": store.ingestion_status()})
            elif parsed.path == "/api/conversations":
                self.respond(200, store.conversations())
            elif parsed.path == "/api/business":
                self.respond(200, store.business_profile())
            elif parsed.path == "/api/assistant/history":
                self.respond(200, get_history(store))
            elif match := re.fullmatch(r"/api/conversations/(\d{1,20})", parsed.path):
                self.respond(200, {"messages": store.messages(match.group(1))})
            else:
                self.respond(404, {"error": "not_found"})

        def do_POST(self):
            if not self.local_host_allowed():
                self.respond(403, {"error": "invalid_host"})
                return
            path = urlparse(self.path).path
            if webhook_only and path != "/webhooks/meta":
                self.respond(404, {"error": "not_found"})
                return
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if not 0 < length <= MAX_BODY:
                    self.respond(413, {"error": "invalid_size"})
                    return
                body = self.rfile.read(length)
                if path == "/webhooks/meta":
                    if not verify_signature(body, self.headers.get("X-Hub-Signature-256", ""), config.get("WHATSAPP_APP_SECRET", "")):
                        self.respond(403, {"error": "invalid_signature"})
                        return
                    payload = json.loads(body)
                    phone_id = config.get("WHATSAPP_PHONE_NUMBER_ID", "")
                    events = parse_webhook(payload, phone_id)
                    store.add_messages(events, webhook_delivery=True, delivery_summary=summarize_webhook(payload, phone_id),
                                       statuses=parse_statuses(payload, phone_id))
                    self.respond(200, {"received": True})
                    return
                origin = self.headers.get("Origin")
                port = self.server.server_port
                if (origin and origin not in {f"http://localhost:{port}", f"http://127.0.0.1:{port}"}) or self.headers.get_content_type() != "application/json":
                    self.respond(403, {"error": "invalid_origin"})
                    return
                if path == "/api/business":
                    self.respond(200, store.save_business_profile(json.loads(body)))
                    return
                if path == "/api/assistant/ask":
                    request = json.loads(body)
                    if not isinstance(request, dict):
                        raise ValueError("invalid request")
                    consent = {"meta": "consent_to_send_to_meta", "nvidia": "consent_to_send_to_nvidia", "nebius": "consent_to_send_to_nebius"}.get(provider, "")
                    if not consent or request.get(consent) is not True:
                        self.respond(400, {"error": "Confirma el envío de la pregunta, el contexto y los fragmentos al proveedor de IA."})
                        return
                    key_name = {"meta": "MODEL_API_KEY", "nvidia": "NVIDIA_API_KEY", "nebius": "NEBIUS_API_KEY"}.get(provider, "")
                    self.respond(200, ask(store, request.get("question"), config.get(key_name, ""), provider))
                    return
                if path == "/api/assistant/voice":
                    request = json.loads(body)
                    if not isinstance(request, dict):
                        raise ValueError("invalid request")
                    if request.get("consent_to_send_to_elevenlabs") is not True:
                        self.respond(400, {"error": "Confirma el envío de esta respuesta a ElevenLabs."})
                        return
                    audio = synthesize(request.get("text"), config.get("ELEVENLABS_API_KEY", ""),
                                       config.get("ELEVENLABS_VOICE_ID") or DEFAULT_VOICE)
                    self.respond(200, audio, "audio/mpeg")
                    return
                if path == "/api/assistant/transcribe":
                    request = json.loads(body)
                    if not isinstance(request, dict):
                        raise ValueError("invalid request")
                    if request.get("consent_to_send_audio_to_elevenlabs") is not True:
                        self.respond(400, {"error": "Confirma el envío del audio a ElevenLabs."})
                        return
                    try:
                        audio = base64.b64decode(request.get("audio", ""), validate=True)
                    except (ValueError, TypeError, binascii.Error):
                        raise ValueError("invalid audio") from None
                    text = transcribe(audio, request.get("mime", ""), config.get("ELEVENLABS_API_KEY", ""))
                    self.respond(200, {"text": text})
                    return
                rec_match = re.fullmatch(r"/api/conversations/(\d{1,20})/recommendations/(\d{1,2})", path)
                if rec_match:
                    request = json.loads(body)
                    if not isinstance(request, dict):
                        raise ValueError("invalid request")
                    updated = store.review_recommendation(rec_match.group(1), request.get("revision"), int(rec_match.group(2)),
                                                          request.get("status"), request.get("note", ""))
                    self.respond(200 if updated else 409, {"updated": updated})
                    return
                match = re.fullmatch(r"/api/conversations/(\d{1,20})/(analyze|review)", path)
                if not match:
                    self.respond(404, {"error": "not_found"})
                    return
                request = json.loads(body)
                if not isinstance(request, dict):
                    raise ValueError("invalid request")
                sender, action = match.groups()
                if action == "review":
                    updated = store.review(sender)
                    self.respond(200 if updated else 404, {"updated": updated})
                    return
                selected_provider = request.get("provider", provider)
                if selected_provider not in {"meta", "nvidia", "nebius"}:
                    self.respond(400, {"error": "Proveedor de IA no admitido."})
                    return
                selected_key_name = {"meta": "MODEL_API_KEY", "nvidia": "NVIDIA_API_KEY", "nebius": "NEBIUS_API_KEY"}[selected_provider]
                if not config.get(selected_key_name):
                    self.respond(503, {"error": "El proveedor seleccionado no está configurado en esta sesión."})
                    return
                consent_field = {"meta": "consent_to_send_to_meta", "nvidia": "consent_to_send_to_nvidia", "nebius": "consent_to_send_to_nebius"}[selected_provider]
                if request.get(consent_field) is not True:
                    destination = {"meta": "Muse (Meta)", "nvidia": "NVIDIA", "nebius": "Nebius"}[selected_provider]
                    self.respond(400, {"error": f"Se requiere confirmar el envío de esta conversación a {destination}."})
                    return
                messages = store.messages(sender)
                if not messages:
                    self.respond(404, {"error": "Conversación no encontrada"})
                    return
                profile = store.business_profile()
                analysis = analyze_messages(messages, config[selected_key_name], provider=selected_provider, business_context=profile)
                if not store.save_analysis(sender, messages, analysis, profile=profile):
                    self.respond(409, {"error": "Cambió la conversación o el negocio; vuelve a analizar."})
                    return
                self.respond(200, analysis)
            except (ValueError, KeyError, TypeError, AttributeError, json.JSONDecodeError):
                self.respond(400, {"error": "Solicitud o evento no válido"})
            except AnalysisError as error:
                self.respond(503, {"error": str(error)})
            except VoiceError as error:
                self.respond(503, {"error": str(error)})

        def log_message(self, format, *args):
            # Do not print webhook query tokens, message contents, or sender numbers.
            print(f"[pendiva] {self.command} {urlparse(self.path).path.split('/')[1]} {args[1] if len(args) > 1 else ''}", flush=True)

    return ThreadingHTTPServer((host, port), Handler)


if __name__ == "__main__":
    config = load_local_config(ROOT / ".env")
    server = create_server(host=config.get("PENDIVA_HOST", "127.0.0.1"),
                           port=int(config.get("PENDIVA_PORT", "8000")),
                           db_path=config.get("PENDIVA_LIVE_DB") or None,
                           environ=config)
    print(f"Pendiva local: http://127.0.0.1:{server.server_port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
