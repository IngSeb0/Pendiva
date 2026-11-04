from contextlib import closing
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import MagicMock, Mock

from src.business_assistant import _words, answer_question, ask, get_history, init_assistant, snapshot
from src.live_pipeline import AnalysisError, LiveStore, parse_webhook
from tests.test_live_pipeline import payload


class AssistantTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1])
        self.store = LiveStore(Path(self.directory.name) / "test.sqlite3")
        self.store.initialize()
        init_assistant(self.store)
        self.store.save_business_profile({"sector": "Servicios de limpieza", "servicios": "Limpieza"})
        self.store.add_messages(parse_webhook(payload(), "123456"))

    def tearDown(self):
        self.directory.cleanup()

    def response(self, data):
        response = MagicMock()
        response.__enter__.return_value = response
        response.read.return_value = json.dumps({"choices": [{"message": {"content": json.dumps(data)}}]}).encode()
        return response

    def good_answer(self):
        return {"respuesta": "Hay una solicitud de cotización.", "limitaciones": "Faltan detalles.",
                "evidencia_ids": ["fuente_1"], "acciones": [{"observacion": "Solicita una cotización.",
                "accion": "Preguntar tipo y fecha del servicio.", "evidencia_ids": ["fuente_1"]}]}

    def test_selected_english_reaches_model_instructions(self):
        messages, coverage, profile, history = snapshot(self.store, "Which quotes need attention?")
        opener = Mock(return_value=self.response(self.good_answer()))
        answer_question("Which quotes need attention?", messages, coverage, profile, history,
                        "fixture-key", "nebius", opener, language="en")
        payload = json.loads(opener.call_args.args[0].data)
        self.assertIn("Responde en inglés", payload["messages"][0]["content"])
        with self.assertRaises(ValueError):
            answer_question("Question", messages, coverage, profile, history, "fixture-key", "nebius", opener, language="xx")

    def test_answer_uses_cleaning_context_and_remaps_only_verified_sources(self):
        messages, coverage, profile, history = snapshot(self.store, "¿Qué cotizaciones necesitan atención?")
        opener = Mock(return_value=self.response(self.good_answer()))
        result = answer_question("¿Qué cotizaciones necesitan atención?", messages, coverage, profile, history,
                                 "fixture-key", "nebius", opener)
        request = json.loads(opener.call_args.args[0].data)
        encoded = json.dumps(request, ensure_ascii=False)
        self.assertIn("Servicios de limpieza", encoded)
        self.assertNotIn("wamid.fixture", encoded)
        self.assertNotIn("573000000000", encoded)
        self.assertIn("fuente_1", encoded)
        self.assertIn("Nunca afirmes que no hay fotos", request["messages"][0]["content"])
        self.assertEqual(result["fuentes"]["fuente_1"]["sender"], "573000000000")
        self.assertEqual(result["acciones"][0]["evidencia_ids"], ["fuente_1"])
        self.assertEqual(coverage["stored_messages"], 1)
        self.assertFalse(coverage["history_complete"])

    def test_rejects_invented_or_missing_evidence(self):
        messages, coverage, profile, history = snapshot(self.store, "cotización")
        for ids in (["inventado"], []):
            answer = self.good_answer()
            answer["acciones"][0]["evidencia_ids"] = ids
            with self.assertRaises(AnalysisError):
                answer_question("cotización", messages, coverage, profile, history, "fixture-key", "nebius",
                                Mock(return_value=self.response(answer)))

    def test_empty_conversation_does_not_call_model(self):
        opener = Mock()
        result = answer_question("¿Qué hago?", [], {}, {}, [], "fixture-key", "nebius", opener)
        opener.assert_not_called()
        self.assertEqual(result["acciones"], [])
        self.assertEqual(result["evidencia_ids"], [])

    def test_conversation_is_persisted_and_available_after_reopening(self):
        result = ask(self.store, "¿Qué debo hacer?", "fixture-key", "nebius", Mock(return_value=self.response(self.good_answer())))
        reopened = LiveStore(self.store.path)
        turns = get_history(reopened)
        self.assertEqual(len(turns), 1)
        self.assertEqual(turns[0]["id"], result["id"])
        self.assertEqual(turns[0]["acciones"][0]["evidencia_ids"], ["fuente_1"])

    def test_retrieval_prioritizes_relevant_older_messages_and_discloses_limit(self):
        for number in range(24):
            self.store.add_messages([{"id": f"fixture-{number}", "sender": "573000000000", "name": "Prueba",
                                     "timestamp": 1793100100 + number, "text": "Consulta general"}])
        selected, coverage, _, _ = snapshot(self.store, "cotizaciones")
        self.assertTrue(any(item["id"] == "wamid.fixture" for item in selected))
        self.assertEqual(coverage["stored_messages"], 25)
        self.assertEqual(coverage["selected_messages"], 25)
        self.assertEqual(coverage["scanned_messages"], 25)

    def test_bilingual_service_synonyms_retrieve_matching_business_evidence(self):
        self.store.add_messages([{"id":"fixture-budget","sender":"573000000001","name":"Lina",
            "timestamp":1793100200,"text":"My budget is 120000 COP for a sofa cleaning quote","kind":"text"}])
        for number in range(45):
            self.store.add_messages([{"id":f"unrelated-{number}","sender":"573000000002","name":"Other",
                "timestamp":1793100300+number,"text":"General office question with no service details","kind":"text"}])
        self.assertIn('quote', _words('cotizaciones estimate quotation'))
        self.assertIn('budget', _words('presupuesto customer budget'))
        selected, coverage, _, _ = snapshot(self.store, 'Which estimates mention a customer budget?')
        self.assertEqual(selected[0]['id'], 'fixture-budget')
        self.assertLessEqual(coverage['selected_sources'], 36)
        self.assertFalse(coverage['history_complete'])

    def test_non_text_metadata_is_saved_without_claiming_media_was_transcribed(self):
        event = payload(message_id="media.fixture")
        event["entry"][0]["changes"][0]["value"]["messages"][0] = {
            "id": "media.fixture", "from": "573000000000", "timestamp": "1793101000", "type": "audio",
            "audio": {"id": "media-id-fixture", "mime_type": "audio/ogg"}}
        parsed = parse_webhook(event, "123456")
        self.assertEqual(parsed[0]["kind"], "audio")
        self.assertIn("no interpretado", parsed[0]["text"])
        self.store.add_messages(parsed)
        self.store.add_messages(parsed)
        with closing(self.store.connect()) as db:
            row = db.execute("SELECT kind,raw FROM live_messages WHERE id=?", ("media.fixture",)).fetchone()
        self.assertEqual(row["kind"], "audio")
        self.assertEqual(json.loads(row["raw"])["audio"]["id"], "media-id-fixture")
        self.assertEqual(len(self.store.messages("573000000000")), 2)
