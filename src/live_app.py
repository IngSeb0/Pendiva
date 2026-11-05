"""Single-operator local dashboard and Meta webhook for a sandbox pilot.

Run behind a proxy that exposes ONLY /webhooks/meta; the dashboard is local.
Local accounts protect dashboard routes; this prototype is not production ready.
"""
from __future__ import annotations

import base64
import binascii
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import hmac
import json
import os
from pathlib import Path
import re
import secrets
import time
from urllib.parse import parse_qs, urlparse

from src.live_pipeline import AnalysisError, LiveStore, analyze_messages, parse_statuses, parse_webhook, summarize_webhook, verify_signature
from src.auth import BootstrapAlreadyComplete, LoginAttemptLimiter
from src.business_assistant import ask, ask_pendiva, get_history, init_assistant
from src.local_config import load_local_config
from src.voice import DEFAULT_VOICE, VoiceError, synthesize, transcribe
from src.multimodal import MediaError, init_media, add_media, list_media, get_media, analyze_media, save_result, delete_media, pending_whatsapp_media, fetch_whatsapp_media
from src.custom_tools import init_tools, propose, preview, activate, list_views, get_view, deactivate, quote_date_import
from src.opportunity_extraction import propose_opportunities
from src.reply_drafts import init_reply_drafts, list_drafts, save_draft, update_draft, suggested_reply, pendiva_reply_suggestion, generate_reply

ROOT = Path(__file__).resolve().parents[1]
MAX_BODY = 262144


def create_server(host="127.0.0.1", port=8000, db_path=None, environ=None, webhook_only=False):
    config = dict(os.environ if environ is None else environ)
    auth_password = config.get("PENDIVA_AUTH_PASSWORD", "")
    sessions = {}
    login_attempts = LoginAttemptLimiter()
    # Pendiva is the product-facing assistant; Meta Model API powers its answers.
    provider = "meta"
    store = LiveStore(db_path or ROOT / "data" / "live.sqlite3")
    store.initialize()
    init_assistant(store)
    init_media(store)
    init_tools(store)
    init_reply_drafts(store)

    def with_identity(method):
        def wrapped(handler):
            handler.identity = store.identity()
            try:
                return method(handler)
            finally:
                handler.identity.close()
        return wrapped

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
            if getattr(self, "path", "") == "/" and config.get("PENDIVA_DEMO_MODE") != "1":
                # Remove cookies issued by earlier versions without Path=/.
                self.send_header("Set-Cookie", "pendiva_session=; Path=/api/auth; HttpOnly; SameSite=Strict; Max-Age=0")
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; media-src 'self' blob:; object-src 'none'; base-uri 'none'; frame-ancestors 'none'")
            self.end_headers()
            self.wfile.write(body)

        def authenticated(self):
            token = self.session_token()
            if auth_password:
                return token in sessions and sessions[token] > time.time()
            return self.identity.session(token) is not None

        def require_write(self):
            if not self.require_auth():
                return False
            current = self.current_identity()
            if current:
                if self.identity.can(current["role"], "write"):
                    return True
                self.respond(403, {"error": "forbidden"})
                return False
            # The single-password compatibility mode is limited to a local demo.
            if auth_password and self.authenticated():
                return True
            self.respond(401, {"error": "authentication_required"})
            return False

        def require_read(self):
            if not self.require_auth():
                return False
            current = self.current_identity()
            if current and self.identity.can(current["role"], "read"):
                return True
            if auth_password and self.authenticated():
                return True
            self.respond(401 if not current else 403, {"error": "authentication_required" if not current else "forbidden"})
            return False

        def secure_cookie_attribute(self):
            enabled = str(config.get("PENDIVA_COOKIE_SECURE", "")).lower() in {"1", "true", "yes"}
            return "; Secure" if enabled else ""

        def login_keys(self, email):
            address = getattr(self, "client_address", ("local",))[0]
            normalized_email = hashlib.sha256(str(email).strip().lower().encode("utf-8", "replace")).hexdigest()
            return ("ip:" + str(address), "email:" + normalized_email)

        def session_token(self):
            for item in self.headers.get("Cookie", "").split(";"):
                key, _, value = item.strip().partition("=")
                if key == self.cookie_name():
                    return value
            return ""

        def cookie_name(self):
            # Browser cookies are host-scoped, not port-scoped. Keep demo logins
            # separate from the user's regular local panel and other demos.
            return f"pendiva_demo_{self.server.server_port}" if config.get("PENDIVA_DEMO_MODE") == "1" else "pendiva_session"

        def current_identity(self):
            return self.identity.session(self.session_token())

        def tenant_id(self):
            current = self.current_identity()
            return current["tenant_id"] if current else None

        def require_auth(self):
            if self.authenticated():
                return True
            self.respond(401, {"error": "authentication_required"})
            return False

        def require_csrf(self):
            current = self.current_identity()
            if not current:
                return True
            supplied = self.headers.get("X-CSRF-Token", "")
            if supplied and hmac.compare_digest(supplied, current["csrf_token"]):
                return True
            self.respond(403, {"error": "csrf_token_required"})
            return False

        @with_identity
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
            elif parsed.path == "/health":
                self.respond(200, {"ok": True})
            elif parsed.path == "/api/auth/status":
                has_users = self.identity.db.execute("SELECT COUNT(*) FROM users").fetchone()[0] > 0
                identity = self.current_identity()
                if identity:
                    identity = {key: value for key, value in identity.items() if key != "token"}
                self.respond(200, {"required": bool(auth_password) or has_users,
                                   "bootstrap_available": not auth_password and not has_users,
                                   "authenticated": self.authenticated(), "identity": identity})
            elif parsed.path == "/":
                self.respond(200, (ROOT / "src" / "static" / "live.html").read_bytes(), "text/html; charset=utf-8")
            elif parsed.path in ("/assets/pendiva.css", "/assets/pendiva.js", "/assets/studio.js", "/assets/voice-session.js"):
                filename = parsed.path.rsplit("/", 1)[-1]
                mime = "text/css" if filename.endswith(".css") else "application/javascript"
                self.respond(200, (ROOT / "src" / "static" / filename).read_bytes(), mime + "; charset=utf-8")
            elif not self.require_auth():
                return
            elif parsed.path == "/api/status":
                provider_keys = {"meta": "MODEL_API_KEY"}
                self.respond(200, {"webhook_configured": all(config.get(k) for k in
                             ("WHATSAPP_VERIFY_TOKEN", "WHATSAPP_APP_SECRET", "WHATSAPP_PHONE_NUMBER_ID")),
                             "muse_configured": provider == "meta" and bool(config.get("MODEL_API_KEY")),
                             "ai_provider": provider,
                             "ai_configured": bool(config.get("MODEL_API_KEY")),
                             "ai_providers": {name: bool(config.get(key)) for name, key in provider_keys.items()},
                             "elevenlabs_configured": bool(config.get("ELEVENLABS_API_KEY")),
                             "provider": "Meta Cloud API", "mode": "demo" if config.get("PENDIVA_DEMO_MODE") == "1" else "live",
                             "ingestion": store.ingestion_status()})
            elif parsed.path == "/api/conversations":
                self.respond(200, store.conversations(self.tenant_id()))
            elif parsed.path == "/api/priorities":
                self.respond(200, store.priority_queue(self.tenant_id()))
            elif parsed.path == "/api/followups":
                current = self.current_identity()
                if not current:
                    self.respond(401, {"error": "authentication_required"})
                else:
                    try:
                        items = store.followups(current['tenant_id'], parse_qs(parsed.query).get('today', [''])[0])
                    except ValueError as exc:
                        self.respond(400, {"error": str(exc)})
                    else:
                        self.respond(200, items)
            elif parsed.path == "/api/summary":
                days = parse_qs(parsed.query).get("days", ["7"])[0]
                try:
                    summary = store.owner_summary(int(days), self.tenant_id())
                except (TypeError, ValueError):
                    self.respond(400, {"error": "El periodo debe ser un número entre 1 y 90 días"})
                else:
                    self.respond(200, summary)
            elif parsed.path == "/api/finance":
                if self.require_auth():
                    self.respond(200, store.financial_summary(self.tenant_id()))
            elif parsed.path == "/api/business":
                self.respond(200, store.business_profile(self.tenant_id()))
            elif parsed.path == "/api/tenant/profile":
                current = self.current_identity()
                if not current:
                    self.respond(401, {"error": "authentication_required"})
                else:
                    self.respond(200, store.tenant_profile(current["tenant_id"]))
            elif parsed.path == "/api/tenant/contacts":
                current = self.current_identity()
                if not current:
                    self.respond(401, {"error": "authentication_required"})
                else:
                    self.respond(200, store.tenant_contacts(current["tenant_id"]))
            elif parsed.path == "/api/assistant/history":
                self.respond(200, get_history(store, self.tenant_id()))
            elif parsed.path == "/api/custom-views":
                self.respond(200, list_views(store, self.tenant_id() or "local"))
            elif match := re.fullmatch(r"/api/custom-views/([0-9a-f]{32})", parsed.path):
                scope = self.tenant_id() or "local"
                view = get_view(store, scope, match.group(1))
                self.respond(200, preview(store, scope, view)) if view else self.respond(404, {"error": "not_found"})
            elif match := re.fullmatch(r"/api/conversations/(\d{1,20})/media", parsed.path):
                self.respond(200, list_media(store, self.tenant_id() or "local", match.group(1)))
            elif match := re.fullmatch(r"/api/conversations/(\d{1,20})/whatsapp-media", parsed.path):
                self.respond(200, pending_whatsapp_media(store, self.tenant_id() or "local", match.group(1)))
            elif match := re.fullmatch(r"/api/media/([0-9a-f]{32})/content", parsed.path):
                asset = get_media(store, self.tenant_id() or "local", match.group(1))
                self.respond(200, asset["content"], asset["mime"]) if asset else self.respond(404, {"error": "not_found"})
            elif match := re.fullmatch(r"/api/conversations/(\d{1,20})/workflow", parsed.path):
                self.respond(200, store.conversation_workflow(match.group(1), self.tenant_id()))
            elif match := re.fullmatch(r"/api/conversations/(\d{1,20})/opportunities", parsed.path):
                if not self.tenant_id():
                    self.respond(401, {"error":"authentication_required"})
                else:
                    self.respond(200, store.conversation_opportunities(match.group(1), self.tenant_id()))
            elif match := re.fullmatch(r"/api/conversations/(\d{1,20})/reply-drafts", parsed.path):
                current = self.current_identity()
                if not current:
                    self.respond(401, {"error": "authentication_required"})
                else:
                    self.respond(200, list_drafts(store, current['tenant_id'], match.group(1)))
            elif match := re.fullmatch(r"/api/conversations/(\d{1,20})/workflow-history", parsed.path):
                self.respond(200, store.workflow_history(match.group(1), self.tenant_id()))
            elif match := re.fullmatch(r"/api/conversations/(\d{1,20})", parsed.path):
                self.respond(200, {"messages": store.messages(match.group(1), self.tenant_id())})
            else:
                self.respond(404, {"error": "not_found"})

        @with_identity
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
                limit = 6 * 1024 * 1024 if path == "/api/media/upload" else MAX_BODY
                if not (0 <= length <= limit and (length > 0 or path == "/api/auth/logout")):
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
                    tenant_id = store.connection_tenant(phone_id)
                    store.add_messages(events, webhook_delivery=True, delivery_summary=summarize_webhook(payload, phone_id),
                                       statuses=parse_statuses(payload, phone_id), tenant_id=tenant_id)
                    self.respond(200, {"received": True})
                    return
                if path == "/api/auth/login":
                        request = json.loads(body)
                        login_keys = self.login_keys(request.get("email", ""))
                        if max(login_attempts.retry_after(key) for key in login_keys):
                            self.respond(429, {"error": "too_many_attempts"})
                            return
                        if auth_password:
                            if not hmac.compare_digest(str(request.get("password", "")), auth_password):
                                for key in login_keys: login_attempts.failed(key)
                                self.respond(401, {"error": "Credenciales inválidas"})
                                return
                            token = secrets.token_urlsafe(32)
                            sessions[token] = time.time() + 8 * 3600
                            identity_data = {}
                        else:
                            identity_data = self.identity.login(str(request.get("email", "")), str(request.get("password", "")))
                            if not identity_data:
                                for key in login_keys: login_attempts.failed(key)
                                self.respond(401, {"error": "Credenciales inválidas"})
                                return
                            token = identity_data["token"]
                        for key in login_keys: login_attempts.succeeded(key)
                        public_identity = {key: value for key, value in identity_data.items() if key != "token"}
                        encoded = json.dumps(public_identity, ensure_ascii=False).encode()
                        self.send_response(200)
                        self.send_header("Content-Type", "application/json; charset=utf-8")
                        self.send_header("Set-Cookie", f"{self.cookie_name()}={token}; Path=/; HttpOnly; SameSite=Strict; Max-Age=28800{self.secure_cookie_attribute()}")
                        self.send_header("Content-Length", str(len(encoded)))
                        self.end_headers()
                        self.wfile.write(encoded)
                        return
                if path == "/api/auth/bootstrap":
                    if self.identity.db.execute("SELECT COUNT(*) FROM users").fetchone()[0]:
                        self.respond(409, {"error": "La empresa inicial ya fue creada"})
                        return
                    request = json.loads(body)
                    try:
                        result = self.identity.bootstrap(request.get("name", ""), request.get("email", ""),
                                                    request.get("password", ""), request.get("sector", "professional_services"))
                    except BootstrapAlreadyComplete:
                        self.respond(409, {"error": "La empresa inicial ya fue creada"})
                        return
                    phone_id = config.get("WHATSAPP_PHONE_NUMBER_ID", "")
                    if phone_id:
                        with self.identity.db:
                            self.identity.db.execute("INSERT OR REPLACE INTO tenant_connections(tenant_id,phone_number_id,verified,created_at) "
                                                "VALUES(?,?,1,datetime('now'))", (result["tenant_id"], phone_id))
                    self.respond(201, result)
                    return
                if path == "/api/auth/logout":
                    token = self.session_token()
                    if token:
                        self.identity.revoke(token)
                        sessions.pop(token, None)
                    self.send_response(204)
                    self.send_header("Set-Cookie", f"{self.cookie_name()}=; Path=/; HttpOnly; SameSite=Strict; Max-Age=0{self.secure_cookie_attribute()}")
                    self.end_headers()
                    return
                if not self.require_auth():
                    return
                if path != "/api/auth/logout" and not self.require_csrf():
                    return
                origin = self.headers.get("Origin")
                port = self.server.server_port
                if (origin and origin not in {f"http://localhost:{port}", f"http://127.0.0.1:{port}"}) or self.headers.get_content_type() != "application/json":
                    self.respond(403, {"error": "invalid_origin"})
                    return
                read_only_actions = {"/api/assistant/ask", "/api/assistant/voice", "/api/assistant/transcribe",
                                     "/api/custom-views/propose", "/api/custom-views/preview", "/api/reply-template"}
                permitted = self.require_read() if path in read_only_actions else self.require_write()
                if not permitted:
                    return
                if path == "/api/business":
                    self.respond(200, store.save_business_profile(json.loads(body), self.tenant_id()))
                    return
                if path in ("/api/media/upload", "/api/media/fetch", "/api/media/analyze", "/api/media/delete", "/api/custom-views/propose", "/api/custom-views/preview", "/api/custom-views/activate", "/api/custom-views/deactivate", "/api/custom-views/import"):
                    current = self.current_identity()
                    if path not in read_only_actions and current and not self.identity.can(current["role"], "write"):
                        self.respond(403, {"error": "forbidden"})
                        return
                    request = json.loads(body)
                    if not isinstance(request, dict): raise ValueError("invalid request")
                    scope = self.tenant_id() or "local"
                    if path == "/api/media/upload":
                        ident = add_media(store, scope, request.get("sender"), request.get("name"), request.get("mime"), request.get("content"))
                        self.respond(201, {"id": ident}); return
                    if path == "/api/media/fetch":
                        if request.get("consent_to_download") is not True:
                            self.respond(400, {"error":"Confirma la descarga del archivo de WhatsApp."}); return
                        ident = fetch_whatsapp_media(store, scope, request.get("sender"), request.get("message_id"),
                                                     config.get("WHATSAPP_TEST_ACCESS_TOKEN", ""), config.get("WHATSAPP_PHONE_NUMBER_ID", ""),
                                                     config.get("WHATSAPP_TEST_GRAPH_VERSION", "v25.0"))
                        self.respond(201, {"id":ident}); return
                    if path == "/api/media/analyze":
                        if request.get("consent_to_send_to_meta") is not True:
                            self.respond(400, {"error":"Confirma el envío del archivo a Meta."}); return
                        asset = get_media(store, scope, request.get("id", ""))
                        if not asset: self.respond(404, {"error":"not_found"}); return
                        ffmpeg = config.get("PENDIVA_FFMPEG_PATH", "")
                        if not ffmpeg:
                            local = list((ROOT / "data" / "demo-tools" / "imageio_ffmpeg" / "binaries").glob("ffmpeg*.exe"))
                            ffmpeg = str(local[0]) if local else None
                        result = analyze_media(asset, config.get("MODEL_API_KEY", ""), request.get("language", "es"), ffmpeg=ffmpeg)
                        save_result(store, scope, asset["id"], result)
                        self.respond(200, {"result":result}); return
                    if path == "/api/media/delete":
                        ident = request.get("id", "")
                        if not isinstance(ident, str) or not re.fullmatch(r"[0-9a-f]{32}", ident): raise ValueError("invalid id")
                        self.respond(200, {"deleted":delete_media(store, scope, ident)}); return
                    if path == "/api/custom-views/propose":
                        if request.get("consent_to_send_to_meta") is not True:
                            self.respond(400, {"error":"Confirma el envío de tu solicitud a Meta."}); return
                        self.respond(200, propose(request.get("messages"), config.get("MODEL_API_KEY", ""), request.get("language", "es"))); return
                    if path == "/api/custom-views/preview":
                        self.respond(200, preview(store, scope, request.get("config"))); return
                    if path == "/api/custom-views/activate":
                        ident = activate(store, scope, request.get("config"))
                        self.respond(201, {"id":ident}); return
                    if path == "/api/custom-views/import":
                        if request.get("commit") not in (True, False): raise ValueError("invalid commit")
                        self.respond(200, quote_date_import(store, scope, request.get("content"), request["commit"], current["user_id"] if current else None)); return
                    ident = request.get("id", "")
                    if not isinstance(ident, str) or not re.fullmatch(r"[0-9a-f]{32}", ident): raise ValueError("invalid id")
                    self.respond(200, {"deactivated":deactivate(store, scope, ident)}); return
                if path == "/api/tenant/profile":
                    current = self.current_identity()
                    if not current or not self.identity.can(current["role"], "write"):
                        self.respond(403, {"error": "forbidden"})
                        return
                    self.respond(200, store.save_tenant_profile(
                        current["tenant_id"], json.loads(body), current["user_id"]))
                    return
                if path == "/api/tenant/contacts":
                    current = self.current_identity()
                    if not current or not self.identity.can(current["role"], "write"):
                        self.respond(403, {"error": "forbidden"})
                        return
                    request = json.loads(body)
                    self.respond(201, store.add_contact(current["tenant_id"], request.get("phone", ""),
                                                        request.get("name", "")))
                    return
                if path == "/api/finance/import":
                    request = json.loads(body)
                    if not isinstance(request, dict):
                        raise ValueError("invalid request")
                    self.respond(200, store.import_financial_csv(request.get("content", ""), self.tenant_id()))
                    return
                if path == "/api/assistant/ask":
                    request = json.loads(body)
                    if not isinstance(request, dict):
                        raise ValueError("invalid request")
                    selected_provider = request.get("provider", provider)
                    consent = "consent_to_send_to_meta" if selected_provider == "meta" else ""
                    if not consent or request.get(consent) is not True:
                        self.respond(400, {"error": "Confirma el envío de la pregunta, el contexto y los fragmentos al proveedor de IA."})
                        return
                    key_name = "MODEL_API_KEY" if selected_provider == "meta" else ""
                    self.respond(200, ask(store, request.get("question"), config.get(key_name, ""), selected_provider, language=request.get("language", "es"), tenant_id=self.tenant_id()))
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
                    text = transcribe(audio, request.get("mime", ""), config.get("ELEVENLABS_API_KEY", ""), language=request.get("language", "es"))
                    self.respond(200, {"text": text})
                    return
                reply_match = re.fullmatch(r"/api/conversations/(\d{1,20})/reply-drafts", path)
                if reply_match:
                    current = self.current_identity()
                    if not current:
                        self.respond(401, {"error": "authentication_required"}); return
                    if not self.identity.can(current['role'], 'write'):
                        self.respond(403, {"error": "forbidden"}); return
                    ident = save_draft(store,current['tenant_id'],reply_match.group(1),current['user_id'],json.loads(body))
                    self.respond(201, {"id":ident}); return
                reply_update = re.fullmatch(r"/api/conversations/(\d{1,20})/reply-drafts/([0-9a-f]{32})", path)
                if reply_update:
                    current = self.current_identity()
                    if not current:
                        self.respond(401, {"error": "authentication_required"}); return
                    if not self.identity.can(current['role'], 'write'):
                        self.respond(403, {"error": "forbidden"}); return
                    updated=update_draft(store,current['tenant_id'],reply_update.group(1),current['user_id'],reply_update.group(2),json.loads(body))
                    self.respond(200 if updated else 404, {"updated":updated}); return
                if path == '/api/reply-template':
                    current = self.current_identity()
                    if not current:
                        self.respond(401, {"error": "authentication_required"}); return
                    request = json.loads(body)
                    sender = request.get('sender') if isinstance(request, dict) else None
                    if sender:
                        if not self.identity.can(current['role'], 'write'):
                            self.respond(403, {"error": "forbidden"}); return
                        messages = store.messages(str(sender), current['tenant_id'])
                        if not messages:
                            self.respond(404, {"error": "not_found"}); return
                        missing = []
                        with closing(store.connect()) as db:
                            row = db.execute("SELECT result,message_ids FROM live_analyses WHERE tenant_id=? AND sender=? ORDER BY created_at DESC LIMIT 1",
                                             (current['tenant_id'], str(sender))).fetchone()
                        if row:
                            try:
                                if json.loads(row['message_ids']) == [message['id'] for message in messages]:
                                    recommendation = json.loads(row['result']).get('recomendaciones', [{}])[0]
                                    missing = recommendation.get('missing_information', [])
                            except (TypeError, ValueError, IndexError):
                                missing = []
                        self.respond(200, {'text': pendiva_reply_suggestion(messages, missing, request.get('language', 'es')),
                                            'sources': [{'text': messages[-1]['text']} ]}); return
                    self.respond(200, {'text': suggested_reply(request.get('language','es'))}); return
                reply_suggestion = re.fullmatch(r"/api/conversations/(\d{1,20})/reply-suggestion", path)
                if reply_suggestion:
                    current=self.current_identity()
                    if not current:
                        self.respond(401,{"error":"authentication_required"});return
                    if not self.identity.can(current['role'],'write'):
                        self.respond(403,{"error":"forbidden"});return
                    request=json.loads(body)
                    if not isinstance(request,dict) or request.get('consent_to_send_to_meta') is not True:
                        self.respond(400,{"error":"Confirma el envío de los mensajes a Pendiva."});return
                    if not config.get('MODEL_API_KEY'):
                        self.respond(503,{"error":"Pendiva no está configurado."});return
                    messages=store.messages(reply_suggestion.group(1),current['tenant_id'])
                    if not messages:
                        self.respond(404,{"error":"not_found"});return
                    self.respond(200,generate_reply(messages,store.business_profile(current['tenant_id']),
                        config['MODEL_API_KEY'],request.get('language','es')));return
                opportunity_proposals = re.fullmatch(r"/api/conversations/(\d{1,20})/opportunity-proposals", path)
                if opportunity_proposals:
                    current = self.current_identity()
                    if not current:
                        self.respond(401, {"error": "authentication_required"})
                        return
                    if current['role'] not in ('owner', 'manager', 'advisor'):
                        self.respond(403, {"error": "forbidden"})
                        return
                    request = json.loads(body)
                    if not isinstance(request, dict) or request.get('consent_to_send_to_meta') is not True:
                        self.respond(400, {"error": "Confirma el envío de los mensajes a Pendiva."})
                        return
                    if not config.get('MODEL_API_KEY'):
                        self.respond(503, {"error": "Pendiva no está configurado."})
                        return
                    messages = store.messages(opportunity_proposals.group(1), current['tenant_id'])
                    if not messages:
                        self.respond(404, {"error": "not_found"})
                        return
                    include_media = request.get('include_media', False)
                    if not isinstance(include_media, bool):
                        raise ValueError('Solicitud no válida')
                    observations = list_media(store, current['tenant_id'], opportunity_proposals.group(1)) if include_media else []
                    self.respond(200, propose_opportunities(messages, config['MODEL_API_KEY'], request.get('language', 'es'), media=observations))
                    return
                opportunity_update = re.fullmatch(r"/api/conversations/(\d{1,20})/opportunities/([0-9a-f]{32})", path)
                if opportunity_update:
                    current = self.current_identity()
                    if not current:
                        self.respond(401, {"error":"authentication_required"}); return
                    if not self.identity.can(current['role'], 'write'):
                        self.respond(403, {"error":"forbidden"}); return
                    updated=store.update_conversation_opportunity(opportunity_update.group(1),current['tenant_id'],opportunity_update.group(2),json.loads(body),current['user_id'])
                    self.respond(200 if updated else 404, {"updated":updated}); return
                opportunity_match = re.fullmatch(r"/api/conversations/(\d{1,20})/opportunities", path)
                if opportunity_match:
                    current = self.current_identity()
                    if not current:
                        self.respond(401, {"error":"authentication_required"}); return
                    if not self.identity.can(current['role'], 'write'):
                        self.respond(403, {"error":"forbidden"}); return
                    ident = store.create_conversation_opportunity(opportunity_match.group(1), current['tenant_id'], json.loads(body))
                    self.respond(201, {"id":ident}); return
                workflow_match = re.fullmatch(r"/api/conversations/(\d{1,20})/workflow", path)
                if workflow_match:
                    current = self.current_identity()
                    if current and not self.identity.can(current["role"], "write"):
                        self.respond(403, {"error": "forbidden"})
                        return
                    self.respond(200, store.save_conversation_workflow(workflow_match.group(1), json.loads(body), self.tenant_id(), current["user_id"] if current else None))
                    return
                rec_match = re.fullmatch(r"/api/conversations/(\d{1,20})/recommendations/(\d{1,2})", path)
                if rec_match:
                    request = json.loads(body)
                    if not isinstance(request, dict):
                        raise ValueError("invalid request")
                    updated = store.review_recommendation(rec_match.group(1), request.get("revision"), int(rec_match.group(2)),
                                                          request.get("status"), request.get("note", ""), self.tenant_id())
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
                    updated = store.review(sender, self.tenant_id())
                    self.respond(200 if updated else 404, {"updated": updated})
                    return
                selected_provider = request.get("provider", provider)
                if selected_provider != "meta":
                    self.respond(400, {"error": "Proveedor de IA no admitido."})
                    return
                selected_key_name = "MODEL_API_KEY"
                if not config.get(selected_key_name):
                    self.respond(503, {"error": "El proveedor seleccionado no está configurado en esta sesión."})
                    return
                consent_field = "consent_to_send_to_meta"
                if request.get(consent_field) is not True:
                    destination = "Pendiva (Meta)"
                    self.respond(400, {"error": f"Se requiere confirmar el envío de esta conversación a {destination}."})
                    return
                messages = store.messages(sender, self.tenant_id())
                if not messages:
                    self.respond(404, {"error": "Conversación no encontrada"})
                    return
                profile = store.business_profile(self.tenant_id())
                language = request.get("language", "es")
                analysis = analyze_messages(messages, config[selected_key_name], provider=selected_provider, business_context=profile, language=language)
                if not store.save_analysis(sender, messages, analysis, profile=profile, tenant_id=self.tenant_id()):
                    self.respond(409, {"error": "Cambió la conversación o el negocio; vuelve a analizar."})
                    return
                self.respond(200, analysis)
            except MediaError as error:
                self.respond(400, {"error": str(error)})
            except (ValueError, KeyError, TypeError, AttributeError, json.JSONDecodeError):
                self.respond(400, {"error": "Solicitud o evento no válido"})
            except AnalysisError as error:
                self.respond(503, {"error": str(error)})
            except VoiceError as error:
                self.respond(503, {"error": str(error)})

        def log_message(self, format, *args):
            # Do not print webhook query tokens, message contents, or sender numbers.
            print(f"[pendiva] {self.command} {urlparse(self.path).path.split('/')[1]} {args[1] if len(args) > 1 else ''}", flush=True)

    server = ThreadingHTTPServer((host, port), Handler)
    return server


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
