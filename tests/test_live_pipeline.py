import hashlib
import hmac
import json
from contextlib import closing
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import MagicMock, Mock

from src.live_pipeline import AnalysisError, LiveStore, analyze_messages, parse_statuses, parse_webhook, summarize_webhook, verify_signature


def payload(message_id="wamid.fixture", phone="123456"):
    return {"object": "whatsapp_business_account", "entry": [{"changes": [{"field": "messages", "value": {
        "metadata": {"phone_number_id": phone}, "contacts": [{"wa_id": "573000000000", "profile": {"name": "Prueba"}}],
        "messages": [{"id": message_id, "from": "573000000000", "timestamp": "1793100000", "type": "text", "text": {"body": "Quiero una cotización"}}],
        "statuses": [{"id": "outbound-fixture", "status": "delivered"}]}}]}]}


class LiveWebhookTests(unittest.TestCase):
    def test_financial_import_calculates_result_and_actionable_alerts(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as directory:
            store = LiveStore(Path(directory) / "live.sqlite3")
            store.initialize()
            summary = store.import_financial_csv(
                "fecha,tipo,monto,categoria\n"
                "2026-10-01,venta,1000,Servicio\n"
                "2026-10-01,gasto,800,Publicidad\n"
                "2026-09-01,venta,1200,Servicio\n"
                "2026-09-01,gasto,100,Operación\n")
            self.assertEqual(summary["sales"], 2200)
            self.assertEqual(summary["expenses"], 900)
            self.assertEqual(summary["result"], 1300)
            self.assertTrue(any(item["type"] == "tendencia" for item in summary["recommendations"]))
    def test_message_migration_keeps_existing_text_and_accepts_new_types(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as directory:
            path = Path(directory) / "existing.sqlite3"
            with closing(sqlite3.connect(path)) as db, db:
                db.execute("CREATE TABLE live_messages (id TEXT PRIMARY KEY, sender TEXT NOT NULL, name TEXT NOT NULL, timestamp INTEGER NOT NULL, text TEXT NOT NULL)")
                db.execute("INSERT INTO live_messages VALUES ('old','123','Fixture',1,'Mensaje previo')")
            store = LiveStore(path)
            store.initialize()
            store.initialize()
            self.assertEqual(store.messages("123")[0]["text"], "Mensaje previo")
            self.assertEqual(store.messages("123")[0]["kind"], "text")
            self.assertEqual(store.ingestion_status()["stored_messages"], 1)

    def test_delivery_statuses_are_persisted_and_deduplicated_without_inventing_outgoing_messages(self):
        event = payload()
        event["entry"][0]["changes"][0]["value"]["messages"] = []
        event["entry"][0]["changes"][0]["value"]["statuses"] = [{"id": "outbound-fixture", "status": "delivered", "timestamp": "1793100000"}]
        statuses = parse_statuses(event, "123456")
        self.assertEqual(len(statuses), 1)
        self.assertEqual(parse_statuses(event, "999"), [])
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as directory:
            store = LiveStore(Path(directory) / "test.sqlite3")
            store.initialize()
            store.add_messages([], webhook_delivery=True, statuses=statuses)
            store.add_messages([], webhook_delivery=True, statuses=statuses)
            self.assertEqual(store.ingestion_status()["stored_statuses"], 1)
            self.assertEqual(store.conversations(), [])

    def test_activity_migration_preserves_existing_observations(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as directory:
            path = Path(directory) / "existing.sqlite3"
            with closing(sqlite3.connect(path)) as db, db:
                db.execute("CREATE TABLE webhook_activity (id INTEGER PRIMARY KEY, received_at TEXT NOT NULL, deliveries INTEGER NOT NULL, messages_added INTEGER NOT NULL)")
                db.execute("INSERT INTO webhook_activity VALUES (1, '2026-10-28T00:00:00+00:00', 4, 2)")
            store = LiveStore(path)
            store.initialize()
            store.initialize()
            status = store.ingestion_status()
            self.assertEqual(status["signed_deliveries"], 4)
            self.assertEqual(status["messages_added_by_webhook"], 2)
            self.assertIsNone(status["last_delivery_summary"])

    def test_safe_summary_distinguishes_events_without_text_or_identifiers(self):
        event = payload()
        summary = summarize_webhook(event, "123456")
        self.assertEqual(summary["matching_changes"], 1)
        self.assertEqual(summary["text_messages"], 1)
        self.assertEqual(summary["statuses"], 1)
        for private in ("wamid.fixture", "573000000000", "Quiero una cotización"):
            self.assertNotIn(private, json.dumps(summary))
        self.assertEqual(summarize_webhook(event, "999")["other_number_changes"], 1)
        event["entry"][0]["changes"][0]["field"] = "account_update"
        self.assertEqual(summarize_webhook(event, "123456")["other_updates"], 1)

    def test_signature_uses_raw_body_and_rejects_invalid_secret(self):
        body = json.dumps(payload()).encode()
        signature = "sha256=" + hmac.new(b"fixture-secret", body, hashlib.sha256).hexdigest()
        self.assertTrue(verify_signature(body, signature, "fixture-secret"))
        self.assertFalse(verify_signature(body + b" ", signature, "fixture-secret"))
        self.assertFalse(verify_signature(body, signature, ""))

    def test_parses_only_expected_phone_and_deduplicates(self):
        events = parse_webhook(payload(), "123456")
        self.assertEqual(len(events), 1)
        self.assertEqual(parse_webhook(payload(phone="999"), "123456"), [])
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as directory:
            store = LiveStore(Path(directory) / "live.sqlite3")
            store.initialize()
            self.assertEqual(store.conversations(), [])
            self.assertEqual(store.add_messages(events), 1)
            self.assertEqual(store.add_messages(events), 0)
            self.assertEqual(store.conversations()[0]["message_count"], 1)

    def test_rejects_analysis_if_new_message_arrives_and_marks_prior_stale(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as directory:
            store = LiveStore(Path(directory) / "live.sqlite3")
            store.initialize()
            store.add_messages(parse_webhook(payload(), "123456"))
            sender = "573000000000"
            messages = store.messages(sender)
            result = {"resumen": "Consulta", "siguiente_paso": "Revisar", "incertidumbre": "",
                      "etapa": "cotizacion", "evidencia_ids": [messages[0]["id"]], "model": "muse-spark-1.3"}
            self.assertTrue(store.save_analysis(sender, messages, result))
            store.add_messages(parse_webhook(payload(message_id="wamid.next"), "123456"))
            self.assertTrue(store.conversations()[0]["analysis"]["stale"])
            self.assertFalse(store.save_analysis(sender, messages, result))

    def test_independent_recommendations_and_business_change(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as directory:
            store = LiveStore(Path(directory) / "live.sqlite3")
            store.initialize()
            profile = store.save_business_profile({"nombre": "Negocio de prueba", "sector": "Servicios"})
            store.add_messages(parse_webhook(payload(), "123456"))
            sender = "573000000000"
            messages = store.messages(sender)
            rec = {"tipo": "cotizacion", "accion": "Revisar", "motivo": "Pidió precio", "prioridad": "alta", "evidencia_ids": [messages[0]["id"]]}
            result = {"resumen": "Consulta", "incertidumbre": "", "recomendaciones": [rec, {**rec, "accion": "Confirmar horario"}], "model": "test"}
            self.assertTrue(store.save_analysis(sender, messages, result, profile))
            analysis = store.conversations()[0]["analysis"]
            self.assertTrue(store.review_recommendation(sender, analysis["created_at"], 0, "completada", "Hecho"))
            updated = store.conversations()[0]["analysis"]
            self.assertEqual([r["estado"] for r in updated["recomendaciones"]], ["completada", "pendiente"])
            store.save_business_profile({"nombre": "Negocio cambiado"})
            self.assertTrue(store.conversations()[0]["analysis"]["stale"])
            self.assertFalse(store.review_recommendation(sender, analysis["created_at"], 1, "completada", ""))
            self.assertFalse(store.save_analysis(sender, messages, result, profile))

    def test_recommendation_revision_prevents_outdated_edit(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as directory:
            store = LiveStore(Path(directory) / "live.sqlite3")
            store.initialize()
            store.add_messages(parse_webhook(payload(), "123456"))
            sender = "573000000000"
            messages = store.messages(sender)
            result = {"resumen": "Consulta", "recomendaciones": [], "incertidumbre": "Sin evidencia", "model": "test"}
            self.assertTrue(store.save_analysis(sender, messages, result))
            self.assertFalse(store.review_recommendation(sender, "revision-antigua", 0, "completada", ""))


class LiveMuseTests(unittest.TestCase):
    def response(self, evidence_id):
        result = {"resumen": "Solicita cotización", "incertidumbre": "Faltan detalles", "recomendaciones": [
            {"tipo": "cotizacion", "accion": "Revisar solicitud", "motivo": "Pidió precio",
             "prioridad": "alta", "evidencia_ids": [evidence_id]}]}
        response = MagicMock()
        response.__enter__.return_value = response
        response.read.return_value = json.dumps({"output": [{"type": "message", "content": [
            {"type": "output_text", "text": json.dumps(result)}]}]}).encode()
        return response

    def test_request_contains_real_input_and_validated_evidence(self):
        messages = parse_webhook(payload(), "123456")
        opener = Mock(return_value=self.response("mensaje_1"))
        result = analyze_messages(messages, "fixture-key", opener=opener)
        request = json.loads(opener.call_args.args[0].data)
        self.assertIn("Quiero una cotización", request["input"])
        self.assertNotIn(messages[0]["id"], request["input"])
        self.assertNotIn(messages[0]["sender"], request["input"])
        self.assertIn("mensaje_1", request["input"])
        self.assertFalse(request["store"])
        self.assertEqual(request["reasoning"]["effort"], "minimal")
        self.assertEqual(request["max_output_tokens"], 4096)
        self.assertEqual(request["text"]["format"]["type"], "json_schema")
        self.assertEqual(result["recomendaciones"][0]["evidencia_ids"], [messages[0]["id"]])

    def test_incomplete_meta_response_is_reported_without_parsing_partial_output(self):
        messages = parse_webhook(payload(), "123456")
        response = MagicMock()
        response.__enter__.return_value = response
        response.read.return_value = json.dumps({"status": "incomplete", "output": [],
                                                 "incomplete_details": {"reason": "max_output_tokens"}}).encode()
        with self.assertRaisesRegex(AnalysisError, "no terminó"):
            analyze_messages(messages, "fixture-key", opener=Mock(return_value=response))

    def test_rejects_invented_evidence_and_absent_key(self):
        messages = parse_webhook(payload(), "123456")
        with self.assertRaises(AnalysisError):
            analyze_messages(messages, "fixture-key", opener=Mock(return_value=self.response("inventado")))
        opener = Mock()
        with self.assertRaises(AnalysisError):
            analyze_messages(messages, "", opener=opener)
        opener.assert_not_called()

    def test_aliases_map_multiple_messages_and_duplicate_ids_are_rejected(self):
        first = parse_webhook(payload(), "123456")[0]
        second = {**first, "id": "wamid.second", "text": "Otra pregunta"}
        opener = Mock(return_value=self.response("mensaje_2"))
        result = analyze_messages([first, second], "fixture-key", opener=opener)
        self.assertEqual(result["recomendaciones"][0]["evidencia_ids"], ["wamid.second"])
        request = json.loads(opener.call_args.args[0].data)["input"]
        self.assertNotIn("wamid.fixture", request)
        self.assertNotIn("wamid.second", request)
        opener = Mock()
        with self.assertRaises(AnalysisError):
            analyze_messages([first, first], "fixture-key", opener=opener)
        opener.assert_not_called()

    def test_multiple_recommendations_and_empty_evidence(self):
        messages = parse_webhook(payload(), "123456")
        response = self.response("mensaje_1")
        body = json.loads(response.read.return_value)
        raw = json.loads(body["output"][0]["content"][0]["text"])
        raw["recomendaciones"].append({**raw["recomendaciones"][0], "accion": "Confirmar horario"})
        body["output"][0]["content"][0]["text"] = json.dumps(raw)
        response.read.return_value = json.dumps(body).encode()
        result = analyze_messages(messages, "fixture-key", opener=Mock(return_value=response), business_context={"sector": "Servicios"})
        self.assertEqual(len(result["recomendaciones"]), 2)
        raw["recomendaciones"][1]["evidencia_ids"] = []
        body["output"][0]["content"][0]["text"] = json.dumps(raw)
        response.read.return_value = json.dumps(body).encode()
        with self.assertRaises(AnalysisError):
            analyze_messages(messages, "fixture-key", opener=Mock(return_value=response))


class LiveNvidiaTests(unittest.TestCase):
    def response(self, evidence_id):
        result = {"resumen": "Consulta", "incertidumbre": "Faltan detalles", "recomendaciones": [
            {"tipo": "cotizacion", "accion": "Revisar solicitud", "motivo": "Solicitó información",
             "prioridad": "alta", "evidencia_ids": [evidence_id]}]}
        response = MagicMock()
        response.__enter__.return_value = response
        response.read.return_value = json.dumps({"choices": [{"message": {"content": json.dumps(result)}}]}).encode()
        return response

    def test_nvidia_request_and_evidence_are_validated(self):
        messages = parse_webhook(payload(), "123456")
        opener = Mock(return_value=self.response("mensaje_1"))
        result = analyze_messages(messages, "fixture-key", opener=opener, provider="nvidia")
        request = opener.call_args.args[0]
        data = json.loads(request.data)
        self.assertEqual(request.full_url, "https://integrate.api.nvidia.com/v1/chat/completions")
        self.assertEqual(data["model"], "nvidia/nemotron-3-super-120b-a12b")
        self.assertEqual(result["provider"], "nvidia")
        self.assertEqual(result["recomendaciones"][0]["evidencia_ids"], [messages[0]["id"]])
        self.assertNotIn(messages[0]["id"], json.dumps(data))
        self.assertNotIn("fixture-key", json.dumps(result))

    def test_nebius_uses_its_own_endpoint_and_validates_evidence(self):
        messages = parse_webhook(payload(), "123456")
        opener = Mock(return_value=self.response("mensaje_1"))
        result = analyze_messages(messages, "fixture-key", opener=opener, provider="nebius")
        request = opener.call_args.args[0]
        self.assertEqual(request.full_url, "https://api.tokenfactory.us-central1.nebius.com/v1/chat/completions")
        self.assertEqual(json.loads(request.data)["model"], "nvidia/nemotron-3-super-120b-a12b")
        self.assertEqual(result["provider"], "nebius")
        self.assertEqual(result["recomendaciones"][0]["evidencia_ids"], [messages[0]["id"]])
        self.assertNotIn(messages[0]["id"], opener.call_args.args[0].data.decode())
        bad_opener = Mock(return_value=self.response("inventado"))
        with self.assertRaises(AnalysisError):
            analyze_messages(messages, "fixture-key", opener=bad_opener, provider="nebius")
        self.assertEqual(bad_opener.call_count, 1)

    def test_nvidia_rejects_invented_ids_and_no_fallback(self):
        messages = parse_webhook(payload(), "123456")
        opener = Mock(return_value=self.response("inventado"))
        with self.assertRaises(AnalysisError):
            analyze_messages(messages, "fixture-key", opener=opener, provider="nvidia")
        self.assertEqual(opener.call_count, 1)
        with self.assertRaises(AnalysisError):
            analyze_messages(messages, "fixture-key", opener=opener, provider="unknown")
        self.assertEqual(opener.call_count, 1)


if __name__ == "__main__":
    unittest.main()
