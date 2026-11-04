"""Explicit outbound smoke test for a Meta-provisioned WhatsApp test sender.

No request is made unless --send is supplied. This cannot test Coexistence,
history sync, or messages sent from WhatsApp Business App.
"""

from __future__ import annotations

import argparse
import http.client
import json
import os
import re
import ssl
import sys
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.local_config import load_local_config


ENV_NAMES = (
    "WHATSAPP_TEST_GRAPH_VERSION",
    "WHATSAPP_TEST_PHONE_NUMBER_ID",
    "WHATSAPP_TEST_ACCESS_TOKEN",
    "WHATSAPP_TEST_RECIPIENT",
)


@dataclass(frozen=True)
class TestConfig:
    graph_version: str
    phone_number_id: str
    access_token: str
    recipient: str


def load_config(environment: dict[str, str] | None = None) -> TestConfig:
    env = os.environ if environment is None else environment
    missing = [name for name in ENV_NAMES if not env.get(name)]
    if missing:
        raise ValueError("Missing required environment variables: " + ", ".join(missing))

    version = env["WHATSAPP_TEST_GRAPH_VERSION"]
    phone_number_id = env["WHATSAPP_TEST_PHONE_NUMBER_ID"]
    recipient = env["WHATSAPP_TEST_RECIPIENT"]
    if not re.fullmatch(r"v\d+\.\d+", version):
        raise ValueError("WHATSAPP_TEST_GRAPH_VERSION must match vNN.N")
    if not phone_number_id.isdigit():
        raise ValueError("WHATSAPP_TEST_PHONE_NUMBER_ID must contain digits only")
    if not re.fullmatch(r"\+?\d{7,15}", recipient):
        raise ValueError("WHATSAPP_TEST_RECIPIENT must be an international test number")
    return TestConfig(version, phone_number_id, env["WHATSAPP_TEST_ACCESS_TOKEN"], recipient)


def send_hello_world(config: TestConfig, connection_factory=http.client.HTTPSConnection) -> str:
    path = f"/{config.graph_version}/{config.phone_number_id}/messages"
    payload = {
        "messaging_product": "whatsapp",
        "to": config.recipient,
        "type": "template",
        "template": {"name": "hello_world", "language": {"code": "en_US"}},
    }
    connection = connection_factory(
        "graph.facebook.com", timeout=15, context=ssl.create_default_context()
    )
    try:
        connection.request(
            "POST",
            path,
            body=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {config.access_token}",
                "Content-Type": "application/json",
            },
        )
        response = connection.getresponse()
        body = response.read()
        if response.status < 200 or response.status >= 300:
            # Do not print response body, credentials, or recipient identifiers.
            if response.status == 401:
                raise RuntimeError("Meta API returned HTTP 401: token inválido, vencido o sin autorización para este emisor de prueba")
            raise RuntimeError(f"Meta API returned HTTP {response.status}")
        try:
            result = json.loads(body)
            message_id = result["messages"][0]["id"]
        except (ValueError, KeyError, IndexError, TypeError) as exc:
            raise RuntimeError("Meta API response did not contain a message ID") from exc
        if not isinstance(message_id, str) or not message_id:
            raise RuntimeError("Meta API response did not contain a valid message ID")
        return message_id
    finally:
        connection.close()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Send only Meta's hello_world test template.")
    parser.add_argument(
        "--send",
        action="store_true",
        help="perform one outbound send to the configured test recipient",
    )
    args = parser.parse_args(argv)
    if not args.send:
        print("Dry run. No API request sent. Add --send to send one hello_world test message.")
        return 0
    try:
        config = load_config(load_local_config(PROJECT_ROOT / ".env"))
        message_id = send_hello_world(config)
    except (ValueError, RuntimeError, OSError, http.client.HTTPException) as exc:
        print(f"Test send failed: {exc}", file=sys.stderr)
        return 1
    print(f"Test message accepted by Meta; message_id={message_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
