from pathlib import Path
import tempfile
import unittest

from src.mvp_app import DashboardStore, classify_message


class MessageClassificationTests(unittest.TestCase):
    def test_detects_signals_with_accented_spanish_and_keeps_evidence(self):
        result = classify_message("Ya pagué la reserva")
        self.assertEqual(result["signal"], "pago_por_verificar")
        self.assertEqual(result["evidence"], "Ya pagué la reserva")
        self.assertEqual(result["method"], "reglas_demo")

    def test_unrecognized_message_stays_unclassified(self):
        self.assertEqual(classify_message("Hola, muchas gracias") ["signal"], "sin_clasificar")


class DashboardStoreTests(unittest.TestCase):
    def test_demo_cases_keep_evidence_and_review_state_after_restart(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp_dir:
            store = DashboardStore(Path(temp_dir) / "demo.sqlite3")
            store.initialize()
            cases = store.list_cases()
            self.assertEqual(len(cases), 5)
            for case in cases:
                self.assertTrue(case["messages"][case["evidence_index"]]["text"])
                self.assertEqual(case["status"], "pendiente")
            case_id = cases[0]["id"]
            self.assertTrue(store.set_case_status(case_id, "revisado"))
            store.initialize()
            self.assertEqual(store.list_cases()[0]["status"], "revisado")
            self.assertFalse(store.set_case_status("missing-case", "revisado"))
            with self.assertRaises(ValueError):
                store.set_case_status(case_id, "incorrecto")

    def test_initializes_synthetic_fixtures_and_deduplicates_events(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp_dir:
            store = DashboardStore(Path(temp_dir) / "demo.sqlite3")
            store.initialize()
            self.assertEqual(len(store.list_leads()), 4)
            self.assertTrue(store.add_demo_message("evt-1", "Contacto de prueba", "Necesito cotización"))
            self.assertFalse(store.add_demo_message("evt-1", "Contacto de prueba", "Necesito cotización"))
            self.assertEqual(len(store.list_leads()), 5)

    def test_rejects_empty_or_oversized_demo_messages(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp_dir:
            store = DashboardStore(Path(temp_dir) / "demo.sqlite3")
            store.initialize()
            with self.assertRaises(ValueError):
                store.add_demo_message("evt-2", "Contacto", " ")
            with self.assertRaises(ValueError):
                store.add_demo_message("evt-3", "Contacto", "a" * 2001)


if __name__ == "__main__":
    unittest.main()
