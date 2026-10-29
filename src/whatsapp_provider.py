"""Provider-neutral simulated WhatsApp connection contract.

This module has no network client and does not model a live provider payload.
The HMAC format below is deliberately synthetic and is not Meta's signature
verification implementation.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
import hashlib
import hmac
from typing import Any, Mapping


class ConnectionState(StrEnum):
    DISCONNECTED = "disconnected"
    PENDING = "pending"
    CONNECTED = "connected"
    ERROR = "error"


@dataclass(frozen=True)
class ConnectionResult:
    state: ConnectionState
    external_ref: str | None = None
    detail: str | None = None


@dataclass(frozen=True)
class ProviderCapabilities:
    history_sync: bool
    app_message_echoes: bool
    contact_sync: bool
    outbound_messages: bool
    simulated: bool = True


@dataclass(frozen=True)
class NormalizedEvent:
    event_id: str
    event_type: str
    occurred_at: datetime
    tenant_ref: str
    payload: Mapping[str, Any]


class SimulatedWhatsAppProvider:
    """In-memory adapter for contract and orchestration tests only."""

    def __init__(self, signing_secret: bytes = b"test-only-secret") -> None:
        self._signing_secret = signing_secret
        self._connections: dict[str, ConnectionResult] = {}

    def connect(self, tenant_ref: str) -> ConnectionResult:
        result = ConnectionResult(ConnectionState.CONNECTED, f"sim:{tenant_ref}")
        self._connections[tenant_ref] = result
        return result

    def connection_status(self, tenant_ref: str) -> ConnectionResult:
        return self._connections.get(
            tenant_ref, ConnectionResult(ConnectionState.DISCONNECTED)
        )

    def sign_for_test(self, raw_body: bytes) -> str:
        """Create the synthetic test signature; never use for a live webhook."""
        digest = hmac.new(self._signing_secret, raw_body, hashlib.sha256).hexdigest()
        return f"sha256={digest}"

    def verify_webhook(self, raw_body: bytes, signature: str) -> bool:
        expected = self.sign_for_test(raw_body)
        return hmac.compare_digest(expected, signature)

    def normalize_event(self, envelope: Mapping[str, Any]) -> NormalizedEvent:
        required = ("event_id", "event_type", "occurred_at", "tenant_ref", "payload")
        missing = [key for key in required if key not in envelope]
        if missing:
            raise ValueError(f"Missing required event fields: {', '.join(missing)}")
        if not isinstance(envelope["payload"], Mapping):
            raise ValueError("payload must be a mapping")
        timestamp = envelope["occurred_at"]
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        if not isinstance(timestamp, datetime):
            raise ValueError("occurred_at must be an ISO-8601 string or datetime")
        return NormalizedEvent(
            event_id=str(envelope["event_id"]),
            event_type=str(envelope["event_type"]),
            occurred_at=timestamp,
            tenant_ref=str(envelope["tenant_ref"]),
            payload=dict(envelope["payload"]),
        )

    def disconnect(self, tenant_ref: str) -> ConnectionResult:
        result = ConnectionResult(ConnectionState.DISCONNECTED)
        self._connections[tenant_ref] = result
        return result

    def get_capabilities(self) -> ProviderCapabilities:
        # Values are illustrative fixtures, not verified capabilities of a BSP.
        return ProviderCapabilities(
            history_sync=True,
            app_message_echoes=True,
            contact_sync=True,
            outbound_messages=True,
        )
