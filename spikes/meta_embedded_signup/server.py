"""Local-only diagnostic harness for Meta WhatsApp Embedded Signup.

This is a temporary integration spike, not the product connection store. It
binds to loopback, exchanges the OAuth code server-side, reads shared phone
metadata, and deliberately discards the access token without persisting it.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
import re
from typing import Callable, Mapping
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


GRAPH_HOST = "graph.facebook.com"
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")


@dataclass(frozen=True)
class MetaConfig:
    app_id: str
    config_id: str
    app_secret: str
    graph_version: str
    signup_extras: dict[str, object] = field(default_factory=dict)


class MetaSignupError(RuntimeError):
    """A sanitized error that is safe to return to the local browser."""


def load_config(env: Mapping[str, str] | None = None) -> MetaConfig | None:
    values = os.environ if env is None else env
    app_id = values.get("META_APP_ID", "").strip()
    config_id = values.get("META_EMBEDDED_SIGNUP_CONFIG_ID", "").strip()
    app_secret = values.get("META_APP_SECRET", "").strip()
    graph_version = values.get("META_GRAPH_VERSION", "").strip()
    extras_raw = values.get("META_EMBEDDED_SIGNUP_EXTRAS", "").strip()

    if not any((app_id, config_id, app_secret, graph_version, extras_raw)):
        return None
    if not re.fullmatch(r"\d+", app_id):
        raise ValueError("META_APP_ID must contain digits only")
    if not re.fullmatch(r"\d+", config_id):
        raise ValueError("META_EMBEDDED_SIGNUP_CONFIG_ID must contain digits only")
    if not app_secret:
        raise ValueError("META_APP_SECRET is required for server-side code exchange")
    if not re.fullmatch(r"v\d+\.\d+", graph_version):
        raise ValueError("META_GRAPH_VERSION must match vNN.N")
    try:
        signup_extras = json.loads(extras_raw) if extras_raw else {}
    except json.JSONDecodeError as exc:
        raise ValueError("META_EMBEDDED_SIGNUP_EXTRAS must be valid JSON") from exc
    if not isinstance(signup_extras, dict):
        raise ValueError("META_EMBEDDED_SIGNUP_EXTRAS must be a JSON object")
    if set(signup_extras) - {"setup", "featureType", "sessionInfoVersion"}:
        raise ValueError("META_EMBEDDED_SIGNUP_EXTRAS contains unsupported keys")
    setup = signup_extras.get("setup", {})
    if not isinstance(setup, dict) or set(setup) - {"solutionID"}:
        raise ValueError("META_EMBEDDED_SIGNUP_EXTRAS.setup supports only solutionID")
    if "featureType" in signup_extras and not isinstance(signup_extras["featureType"], str):
        raise ValueError("META_EMBEDDED_SIGNUP_EXTRAS.featureType must be a string")
    if "sessionInfoVersion" in signup_extras and not isinstance(
        signup_extras["sessionInfoVersion"], (str, int)
    ):
        raise ValueError("META_EMBEDDED_SIGNUP_EXTRAS.sessionInfoVersion must be text or a number")
    return MetaConfig(app_id, config_id, app_secret, graph_version, signup_extras)


class MetaSignupClient:
    """Performs a one-time exchange and metadata check without storing tokens."""

    def __init__(
        self,
        config: MetaConfig,
        opener: Callable[..., object] = urlopen,
    ) -> None:
        self.config = config
        self.opener = opener

    def complete(self, code: str, waba_id: str) -> dict[str, object]:
        if not code or len(code) > 8192:
            raise MetaSignupError("Meta did not return a usable authorization code")
        if not re.fullmatch(r"\d+", waba_id):
            raise MetaSignupError("Meta did not return a valid WhatsApp account ID")

        query = urlencode({
            "client_id": self.config.app_id,
            "client_secret": self.config.app_secret,
            "code": code,
        })
        token_url = (
            f"https://{GRAPH_HOST}/{self.config.graph_version}/oauth/access_token?{query}"
        )
        token_data = self._get_json(Request(token_url, method="GET"))
        access_token = token_data.get("access_token")
        if not isinstance(access_token, str) or not access_token:
            raise MetaSignupError("Meta did not return an access token")

        phones_url = (
            f"https://{GRAPH_HOST}/{self.config.graph_version}/{waba_id}/phone_numbers?"
            "fields=id,display_phone_number,verified_name"
        )
        phone_data = self._get_json(Request(
            phones_url,
            headers={"Authorization": f"Bearer {access_token}"},
            method="GET",
        ))
        data = phone_data.get("data")
        if not isinstance(data, list):
            raise MetaSignupError("Meta returned an unexpected phone-number response")

        phones: list[dict[str, str]] = []
        for item in data:
            if not isinstance(item, dict):
                continue
            phone_id = item.get("id")
            display_number = item.get("display_phone_number")
            if isinstance(phone_id, str) and phone_id.isdigit():
                phone: dict[str, str] = {"id": phone_id}
                if isinstance(display_number, str):
                    phone["display_phone_number"] = display_number
                verified_name = item.get("verified_name")
                if isinstance(verified_name, str):
                    phone["verified_name"] = verified_name
                phones.append(phone)

        # The token remains a local variable and is neither returned nor stored.
        return {"waba_id": waba_id, "phone_numbers": phones}

    def _get_json(self, request: Request) -> dict[str, object]:
        try:
            with self.opener(request, timeout=15) as response:
                payload = json.loads(response.read())
        except (HTTPError, URLError, TimeoutError, OSError, ValueError) as exc:
            # Do not include Meta's body or the URL: either can contain secrets.
            raise MetaSignupError("Meta could not complete the signup check") from exc
        if not isinstance(payload, dict):
            raise MetaSignupError("Meta returned an unexpected response")
        if "error" in payload:
            raise MetaSignupError("Meta could not complete the signup check")
        return payload


def render_page(config: MetaConfig | None) -> bytes:
    app_config = {
        "appId": config.app_id if config else "",
        "configId": config.config_id if config else "",
        "graphVersion": config.graph_version if config else "",
        "extras": config.signup_extras if config else {},
    }
    safe_json = json.dumps(app_config).replace("</", "<\\/")
    with open(os.path.join(STATIC_DIR, "index.html"), "rb") as page_file:
        html = page_file.read().decode("utf-8")
    html = html.replace("__META_CONFIG__", safe_json)
    return html.encode("utf-8")


def make_handler(config: MetaConfig | None) -> type[BaseHTTPRequestHandler]:
    class Handler(BaseHTTPRequestHandler):
        server_version = "EmbeddedSignupSpike/0.1"
        sys_version = ""

        def log_message(self, format: str, *args: object) -> None:
            # Avoid logging query strings, authorization data, or personal data.
            print(f"[local-spike] {self.command} {self.path.split('?')[0]}")

        def _respond(self, status: int, body: bytes, content_type: str) -> None:
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            self.end_headers()
            self.wfile.write(body)

        def _json(self, status: int, payload: dict[str, object]) -> None:
            self._respond(status, json.dumps(payload).encode(), "application/json; charset=utf-8")

        def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
            if self.path == "/":
                self._respond(200, render_page(config), "text/html; charset=utf-8")
                return
            if self.path == "/health":
                self._json(200, {"status": "ok", "configured": config is not None})
                return
            self._json(404, {"error": "Not found"})

        def do_POST(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
            if self.path != "/api/complete":
                self._json(404, {"error": "Not found"})
                return
            if config is None:
                self._json(503, {"error": "Set the Meta app configuration first"})
                return

            origin = self.headers.get("Origin")
            host = self.headers.get("Host", "")
            allowed_origins = {f"http://{host}"} if host in {
                "localhost:8765", "127.0.0.1:8765"
            } else set()
            if origin is not None and origin not in allowed_origins:
                self._json(403, {"error": "Requests must come from this local page"})
                return

            try:
                content_length = int(self.headers.get("Content-Length", "0"))
            except ValueError:
                content_length = 0
            if content_length < 1 or content_length > 16_384:
                self._json(400, {"error": "Invalid request size"})
                return
            try:
                payload = json.loads(self.rfile.read(content_length))
            except (UnicodeDecodeError, json.JSONDecodeError):
                self._json(400, {"error": "Invalid JSON"})
                return
            if not isinstance(payload, dict):
                self._json(400, {"error": "Invalid signup response"})
                return

            try:
                result = MetaSignupClient(config).complete(
                    str(payload.get("code", "")),
                    str(payload.get("waba_id", "")),
                )
            except MetaSignupError as exc:
                self._json(502, {"error": str(exc)})
                return
            self._json(200, result)

    return Handler


def main() -> None:
    config = load_config()
    server = ThreadingHTTPServer(("127.0.0.1", 8765), make_handler(config))
    print("Local-only Meta Embedded Signup spike: http://127.0.0.1:8765")
    print("Bound to 127.0.0.1; no access token is persisted.")
    if config is None:
        print("Meta settings are empty. Add the required environment variables and restart.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Stopping local spike.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
