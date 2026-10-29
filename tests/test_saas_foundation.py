import tempfile
import unittest
from pathlib import Path

from src.domain_validation import validate_date, validate_evidence_state, validate_money, validate_stage
from src.live_pipeline import LiveStore


class SaaSFoundationTests(unittest.TestCase):
    def test_identity_sessions_and_tenant_isolation(self):
        with tempfile.TemporaryDirectory() as directory:
            store = LiveStore(Path(directory) / "saas.sqlite3")
            store.initialize()
            identity = store.identity()
            first = identity.bootstrap("Empresa Uno", "uno@example.com", "una-clave-local-segura", "home_services")
            second = identity.bootstrap("Empresa Dos", "dos@example.com", "otra-clave-local-segura", "professional_services")
            session = identity.login("uno@example.com", "una-clave-local-segura")
            self.assertEqual(session["tenant_id"], first["tenant_id"])
            store.add_contact(first["tenant_id"], "573000000001", "Cliente Uno")
            store.add_contact(second["tenant_id"], "573000000001", "Cliente Dos")
            self.assertEqual(store.tenant_contacts(first["tenant_id"])[0]["name"], "Cliente Uno")
            self.assertEqual(store.tenant_contacts(second["tenant_id"])[0]["name"], "Cliente Dos")
            self.assertTrue(identity.can(session["role"], "write"))
            identity.revoke(session["token"])
            self.assertIsNone(identity.session(session["token"]))
            identity.close()

    def test_domain_contracts_reject_ambiguous_values(self):
        self.assertEqual(validate_stage("quote_sent"), "quote_sent")
        self.assertEqual(validate_evidence_state("pending"), "pending")
        self.assertEqual(validate_date("2026-10-28"), "2026-10-28")
        self.assertEqual(validate_money("1250,50"), "1250.50")
        with self.assertRaises(ValueError):
            validate_stage("lost_by_silence")
        with self.assertRaises(ValueError):
            validate_date("28/10/2026")
        with self.assertRaises(ValueError):
            validate_money("-10")


if __name__ == "__main__":
    unittest.main()
