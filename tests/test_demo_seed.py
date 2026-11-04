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
            self.assertEqual(second["conversations"], 9)
            self.assertEqual(len(store.conversations(first["tenant_id"])), 9)
            self.assertEqual(len(store.tenant_contacts(first["tenant_id"])), 9)
            self.assertEqual(store.connection_tenant("123456"), first["tenant_id"])
            self.assertEqual(store.financial_summary()["records"], 6)

    def test_english_seed_is_consistent_and_contains_only_synthetic_records(self):
        with tempfile.TemporaryDirectory() as directory:
            store = LiveStore(Path(directory) / "demo-en.sqlite3")
            seeded = seed_demo(store, language="en")
            self.assertEqual(len(store.conversations(seeded["tenant_id"])), 9)
            profile = store.business_profile(seeded["tenant_id"])
            self.assertEqual(profile["nombre"], "Home Services Demo")
            messages = store.messages("573000000101", seeded["tenant_id"])
            self.assertIn("three-seat sofa", " ".join(item["text"] for item in messages))
            finance = store.financial_summary(seeded["tenant_id"])
            self.assertEqual(finance["sales"], 3250)
            self.assertEqual(finance["expenses"], 1730)
            self.assertEqual(finance["result"], 1520)

    def test_english_seed_can_leave_finance_empty_for_csv_import_demo(self):
        with tempfile.TemporaryDirectory() as directory:
            store = LiveStore(Path(directory) / "demo-en-empty-finance.sqlite3")
            seeded = seed_demo(store, language="en", include_finance=False)
            self.assertEqual(len(store.conversations(seeded["tenant_id"])), 9)
            self.assertEqual(store.financial_summary(seeded["tenant_id"])["records"], 0)
            csv_path = Path(__file__).resolve().parents[1] / "fixtures" / "demo" / "cleaning-sales-demo-en.csv"
            imported = store.import_financial_csv(csv_path.read_text(encoding="utf-8"), seeded["tenant_id"])
            self.assertEqual(imported["records"], 6)
            self.assertEqual(imported["sales"], 3250)
            self.assertEqual(imported["expenses"], 1730)


if __name__ == "__main__":
    unittest.main()
