import tempfile
import unittest
from pathlib import Path

from src.demo_seed import DEMO_EMAIL, DEMO_PASSWORD, seed_demo
from src.live_pipeline import LiveStore


class DemoSeedTests(unittest.TestCase):
    def test_seed_is_realistic_idempotent_and_tenant_scoped(self):
        with tempfile.TemporaryDirectory() as directory:
            store = LiveStore(Path(directory) / "demo.sqlite3")
            first = seed_demo(store, "123456")
            second = seed_demo(store, "123456")
            self.assertTrue(first["synthetic"])
            self.assertEqual(first["email"], DEMO_EMAIL)
            self.assertEqual(first["password"], DEMO_PASSWORD)
            self.assertEqual(second["conversations"], 5)
            self.assertEqual(len(store.conversations(first["tenant_id"])), 5)
            self.assertEqual(len(store.tenant_contacts(first["tenant_id"])), 5)
            self.assertEqual(store.connection_tenant("123456"), first["tenant_id"])
            self.assertEqual(store.financial_summary()["records"], 6)


if __name__ == "__main__":
    unittest.main()
