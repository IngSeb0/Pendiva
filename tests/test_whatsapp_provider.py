import unittest
from datetime import datetime, timezone

from src.whatsapp_provider import (
    ConnectionState,
    SimulatedWhatsAppProvider,
)


class SimulatedWhatsAppProviderTests(unittest.TestCase):
    def setUp(self):
        self.provider = SimulatedWhatsAppProvider(b"fixture-secret")

    def test_connection_lifecycle(self):
        self.assertEqual(
            self.provider.connection_status("tenant-a").state,
            ConnectionState.DISCONNECTED,
        )
        connected = self.provider.connect("tenant-a")
        self.assertEqual(connected.state, ConnectionState.CONNECTED)
        self.assertEqual(connected.external_ref, "sim:tenant-a")
        self.assertEqual(
            self.provider.disconnect("tenant-a").state,
            ConnectionState.DISCONNECTED,
        )

    def test_synthetic_webhook_signature(self):
        body = b'{"event":"fixture"}'
        signature = self.provider.sign_for_test(body)
        self.assertTrue(self.provider.verify_webhook(body, signature))
        self.assertFalse(self.provider.verify_webhook(body + b"!", signature))
        self.assertFalse(self.provider.verify_webhook(body, "sha256=invalid"))

    def test_normalize_provider_neutral_event(self):
        event = self.provider.normalize_event({
            "event_id": "evt-1",
            "event_type": "message.received",
            "occurred_at": "2026-10-15T10:30:00Z",
            "tenant_ref": "tenant-a",
            "payload": {"text": "synthetic"},
        })
        self.assertEqual(event.event_id, "evt-1")
        self.assertEqual(event.occurred_at, datetime(2026, 10, 15, 10, 30, tzinfo=timezone.utc))
        self.assertEqual(event.payload["text"], "synthetic")

    def test_normalization_rejects_missing_fields_or_invalid_payload(self):
        with self.assertRaisesRegex(ValueError, "event_id"):
            self.provider.normalize_event({"event_type": "message.received"})
        with self.assertRaisesRegex(ValueError, "payload"):
            self.provider.normalize_event({
                "event_id": "evt-1",
                "event_type": "message.received",
                "occurred_at": "2026-10-15T10:30:00Z",
                "tenant_ref": "tenant-a",
                "payload": [],
            })

    def test_capabilities_are_explicitly_marked_simulated(self):
        capabilities = self.provider.get_capabilities()
        self.assertTrue(capabilities.simulated)
        self.assertTrue(capabilities.app_message_echoes)
        self.assertTrue(capabilities.history_sync)


if __name__ == "__main__":
    unittest.main()
