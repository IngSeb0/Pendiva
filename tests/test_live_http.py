"""Exercise request handlers without opening outbound network connections."""
from email.message import Message
import hashlib
import hmac
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

from src.live_app import create_server
from tests.test_live_pipeline import payload


class LiveHandlerTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1])
        self.server = create_server(port=0, db_path=Path(self.directory.name) / "test.sqlite3", environ={
            "WHATSAPP_APP_SECRET": "fixture-secret", "WHATSAPP_VERIFY_TOKEN": "fixture-verify",
            "WHATSAPP_PHONE_NUMBER_ID": "123456", "MODEL_API_KEY": "fixture-key"})

    def tearDown(self):
        self.server.server_close()
        self.directory.cleanup()

    def handler(self, path, body=b"", headers=None):
        handler = object.__new__(self.server.RequestHandlerClass)
        handler.path = path
        handler.server = self.server
        handler.headers = Message()
        handler.headers["Content-Length"] = str(len(body))
        for key, value in (headers or {}).items():
            handler.headers[key] = value
        handler.rfile = io.BytesIO(body)
        handler.respond = Mock()
        return handler

    def test_verification_and_signed_delivery_deduplicate(self):
        challenge = self.handler("/webhooks/meta?hub.mode=subscribe&hub.verify_token=fixture-verify&hub.challenge=123")
        challenge.do_GET()
        self.assertEqual(challenge.respond.call_args.args[0], 200)
        raw = json.dumps(payload()).encode()
        signature = "sha256=" + hmac.new(b"fixture-secret", raw, hashlib.sha256).hexdigest()
        bad = self.handler("/webhooks/meta", raw, {"X-Hub-Signature-256": "sha256=wrong"})
        bad.do_POST()
        self.assertEqual(bad.respond.call_args.args[0], 403)
        for _ in range(2):
            request = self.handler("/webhooks/meta", raw, {"X-Hub-Signature-256": signature})
            request.do_POST()
            self.assertEqual(request.respond.call_args.args[0], 200)
        listing = self.handler("/api/conversations")
        listing.do_GET()
        self.assertEqual(listing.respond.call_args.args[1][0]["message_count"], 1)
        status = self.handler("/api/status")
        status.do_GET()
        activity = status.respond.call_args.args[1]["ingestion"]
        self.assertEqual(activity["signed_deliveries"], 2)
        self.assertEqual(activity["messages_added_by_webhook"], 1)
        self.assertEqual(activity["stored_messages"], 1)
        self.assertIsNotNone(activity["last_signed_delivery_at"])
        self.assertEqual(activity["last_delivery_summary"]["text_messages"], 1)
        self.assertEqual(activity["last_delivery_summary"]["statuses"], 1)
        self.assertNotIn("wamid.fixture", json.dumps(activity))

    def test_panel_rejects_unexpected_host_and_status_contains_no_secrets(self):
        request = self.handler("/api/conversations", headers={"Host": "attacker.example"})
        request.do_GET()
        self.assertEqual(request.respond.call_args.args[0], 403)
        request = self.handler("/api/business", b'{}', {"Host": "attacker.example", "Content-Type": "application/json"})
        request.do_POST()
        self.assertEqual(request.respond.call_args.args[0], 403)
        status = self.handler("/api/status")
        status.do_GET()
        data = status.respond.call_args.args[1]
        self.assertEqual(data["ingestion"]["signed_deliveries"], 0)
        self.assertNotIn("fixture-", json.dumps(data))

    def test_webhook_only_port_denies_panel_and_apis(self):
        self.server.server_close()
        self.server = create_server(port=0, db_path=Path(self.directory.name) / "test.sqlite3",
                                    environ={"WHATSAPP_VERIFY_TOKEN": "fixture-verify"}, webhook_only=True)
        for path in ("/", "/api/status", "/api/conversations", "/api/business", "/api/assistant/history"):
            request = self.handler(path)
            request.do_GET()
            self.assertEqual(request.respond.call_args.args[0], 404)
        request = self.handler("/api/business", b'{"nombre":"x"}', {"Content-Type": "application/json"})
        request.do_POST()
        self.assertEqual(request.respond.call_args.args[0], 404)
        challenge = self.handler("/webhooks/meta?hub.mode=subscribe&hub.verify_token=fixture-verify&hub.challenge=123")
        challenge.do_GET()
        self.assertEqual(challenge.respond.call_args.args[0], 200)

    def test_muse_never_called_without_explicit_consent(self):
        request = self.handler("/api/conversations/573000000000/analyze", b"{}", {"Content-Type": "application/json"})
        with patch("src.live_app.analyze_messages") as analyze:
            request.do_POST()
        self.assertEqual(request.respond.call_args.args[0], 400)
        analyze.assert_not_called()

    def test_assistant_and_voice_do_not_call_providers_without_consent(self):
        question = self.handler("/api/assistant/ask", b'{"question":"Que debo hacer?"}', {"Content-Type": "application/json"})
        voice = self.handler("/api/assistant/voice", b'{"text":"Hola"}', {"Content-Type": "application/json"})
        transcript = self.handler("/api/assistant/transcribe", b'{"audio":"Zml4dHVyZQ==","mime":"audio/webm"}', {"Content-Type": "application/json"})
        with patch("src.live_app.ask") as ask, patch("src.live_app.synthesize") as synthesize, patch("src.live_app.transcribe") as transcribe:
            question.do_POST()
            voice.do_POST()
            transcript.do_POST()
        self.assertEqual(question.respond.call_args.args[0], 400)
        self.assertEqual(voice.respond.call_args.args[0], 400)
        self.assertEqual(transcript.respond.call_args.args[0], 400)
        ask.assert_not_called()
        synthesize.assert_not_called()
        transcribe.assert_not_called()

    def test_transcription_receives_only_validated_audio_after_consent(self):
        request = self.handler("/api/assistant/transcribe", b'{"audio":"Zml4dHVyZQ==","mime":"audio/webm","consent_to_send_audio_to_elevenlabs":true}',
                               {"Content-Type": "application/json"})
        with patch("src.live_app.transcribe", return_value="Pregunta ficticia") as transcribe:
            request.do_POST()
        self.assertEqual(request.respond.call_args.args, (200, {"text": "Pregunta ficticia"}))
        self.assertEqual(transcribe.call_args.args[0], b"fixture")

    def test_voice_returns_audio_only_after_elevenlabs_consent(self):
        voice = self.handler("/api/assistant/voice", b'{"text":"Hola","consent_to_send_to_elevenlabs":true}',
                             {"Content-Type": "application/json"})
        with patch("src.live_app.synthesize", return_value=b"fake-mp3") as synthesize:
            voice.do_POST()
        synthesize.assert_called_once()
        self.assertEqual(voice.respond.call_args.args, (200, b"fake-mp3", "audio/mpeg"))

    def test_signed_message_to_analyzed_and_reviewed_conversation(self):
        raw = json.dumps(payload()).encode()
        signature = "sha256=" + hmac.new(b"fixture-secret", raw, hashlib.sha256).hexdigest()
        event = self.handler("/webhooks/meta", raw, {"X-Hub-Signature-256": signature})
        event.do_POST()
        result = {"resumen": "Solicita cotización", "etapa": "cotizacion", "siguiente_paso": "Revisar solicitud",
                  "incertidumbre": "Faltan detalles", "evidencia_ids": ["wamid.fixture"], "model": "muse-spark-1.3"}
        request = self.handler("/api/conversations/573000000000/analyze", b'{"consent_to_send_to_meta":true}',
                               {"Content-Type": "application/json"})
        with patch("src.live_app.analyze_messages", return_value=result) as analyze:
            request.do_POST()
        self.assertEqual(request.respond.call_args.args[0], 200)
        self.assertEqual(analyze.call_args.args[0][0]["id"], "wamid.fixture")
        review = self.handler("/api/conversations/573000000000/review", b"{}", {"Content-Type": "application/json"})
        review.do_POST()
        self.assertEqual(review.respond.call_args.args[0], 200)
        listing = self.handler("/api/conversations")
        listing.do_GET()
        self.assertTrue(listing.respond.call_args.args[1][0]["analysis"]["reviewed"])

    def test_nvidia_does_not_accept_consent_for_meta(self):
        self.server.server_close()
        self.server = create_server(port=0, db_path=Path(self.directory.name) / "test.sqlite3", environ={
            "PENDIVA_AI_PROVIDER": "nvidia", "NVIDIA_API_KEY": "fixture-key"})
        request = self.handler("/api/conversations/573000000000/analyze", b'{"consent_to_send_to_meta":true}',
                               {"Content-Type": "application/json"})
        with patch("src.live_app.analyze_messages") as analyze:
            request.do_POST()
        self.assertEqual(request.respond.call_args.args[0], 400)
        self.assertIn("NVIDIA", request.respond.call_args.args[1]["error"])
        analyze.assert_not_called()

    def test_nebius_requires_its_own_consent(self):
        self.server.server_close()
        self.server = create_server(port=0, db_path=Path(self.directory.name) / "test.sqlite3", environ={
            "PENDIVA_AI_PROVIDER": "nebius", "NEBIUS_API_KEY": "fixture-key"})
        request = self.handler("/api/conversations/573000000000/analyze", b'{"consent_to_send_to_nvidia":true}',
                               {"Content-Type": "application/json"})
        with patch("src.live_app.analyze_messages") as analyze:
            request.do_POST()
        self.assertEqual(request.respond.call_args.args[0], 400)
        self.assertIn("Nebius", request.respond.call_args.args[1]["error"])
        analyze.assert_not_called()
        status = self.handler("/api/status")
        status.do_GET()
        self.assertTrue(status.respond.call_args.args[1]["ai_configured"])
        self.assertEqual(status.respond.call_args.args[1]["ai_providers"],
                         {"meta": False, "nvidia": False, "nebius": True})

    def test_analysis_can_select_another_configured_provider_with_its_consent(self):
        self.server.server_close()
        self.server = create_server(port=0, db_path=Path(self.directory.name) / "test.sqlite3", environ={
            "PENDIVA_AI_PROVIDER": "nebius", "NEBIUS_API_KEY": "nebius-key", "MODEL_API_KEY": "meta-key",
            "WHATSAPP_APP_SECRET": "fixture-secret", "WHATSAPP_PHONE_NUMBER_ID": "123456"})
        raw = json.dumps(payload()).encode()
        signature = "sha256=" + hmac.new(b"fixture-secret", raw, hashlib.sha256).hexdigest()
        self.handler("/webhooks/meta", raw, {"X-Hub-Signature-256": signature}).do_POST()
        request = self.handler("/api/conversations/573000000000/analyze",
                               b'{"provider":"meta","consent_to_send_to_meta":true}',
                               {"Content-Type": "application/json"})
        result = {"resumen": "Consulta", "incertidumbre": "", "recomendaciones": [], "model": "muse-spark-1.3"}
        with patch("src.live_app.analyze_messages", return_value=result) as analyze:
            request.do_POST()
        self.assertEqual(request.respond.call_args.args[0], 200)
        self.assertEqual(analyze.call_args.kwargs["provider"], "meta")

    def test_profile_and_individual_recommendation_review(self):
        business = self.handler("/api/business", json.dumps({"nombre": "Negocio de prueba", "sector": "Servicios"}).encode(),
                                {"Content-Type": "application/json"})
        business.do_POST()
        self.assertEqual(business.respond.call_args.args[0], 200)
        raw = json.dumps(payload()).encode()
        signature = "sha256=" + hmac.new(b"fixture-secret", raw, hashlib.sha256).hexdigest()
        self.handler("/webhooks/meta", raw, {"X-Hub-Signature-256": signature}).do_POST()
        recommendation = {"tipo": "cotizacion", "accion": "Revisar solicitud", "motivo": "Pidió precio",
                          "prioridad": "alta", "evidencia_ids": ["wamid.fixture"]}
        result = {"resumen": "Consulta", "incertidumbre": "", "recomendaciones": [recommendation, recommendation], "model": "test"}
        request = self.handler("/api/conversations/573000000000/analyze", b'{"consent_to_send_to_meta":true}', {"Content-Type": "application/json"})
        with patch("src.live_app.analyze_messages", return_value=result) as analyze:
            request.do_POST()
        self.assertEqual(analyze.call_args.kwargs["business_context"]["nombre"], "Negocio de prueba")
        listing = self.handler("/api/conversations")
        listing.do_GET()
        revision = listing.respond.call_args.args[1][0]["analysis"]["created_at"]
        review_body = json.dumps({"revision": revision, "status": "completada", "note": "Revisada"}).encode()
        review = self.handler("/api/conversations/573000000000/recommendations/0", review_body, {"Content-Type": "application/json"})
        review.do_POST()
        self.assertEqual(review.respond.call_args.args[0], 200)
        listing.do_GET()
        recs = listing.respond.call_args.args[1][0]["analysis"]["recomendaciones"]
        self.assertEqual([item["estado"] for item in recs], ["completada", "pendiente"])

    def test_priority_queue_orders_pending_recommendations_and_omits_stale(self):
        raw = json.dumps(payload()).encode()
        signature = "sha256=" + hmac.new(b"fixture-secret", raw, hashlib.sha256).hexdigest()
        self.handler("/webhooks/meta", raw, {"X-Hub-Signature-256": signature}).do_POST()
        result = {"resumen": "Consulta", "incertidumbre": "", "recomendaciones": [
            {"tipo": "seguimiento", "accion": "Llamar hoy", "motivo": "Compromiso explícito",
             "prioridad": "media", "evidencia_ids": ["wamid.fixture"]},
            {"tipo": "cotizacion", "accion": "Enviar precio", "motivo": "Pidió una cotización",
             "prioridad": "alta", "evidencia_ids": ["wamid.fixture"]}], "model": "test"}
        request = self.handler("/api/conversations/573000000000/analyze",
                               b'{"consent_to_send_to_meta":true}', {"Content-Type": "application/json"})
        with patch("src.live_app.analyze_messages", return_value=result):
            request.do_POST()
        priorities = self.handler("/api/priorities")
        priorities.do_GET()
        items = priorities.respond.call_args.args[1]
        self.assertEqual([item["accion"] for item in items], ["Enviar precio", "Llamar hoy"])
        self.assertEqual(items[0]["evidencia"], ["Quiero una cotización"])

    def test_owner_summary_reports_period_and_data_limits(self):
        raw = json.dumps(payload()).encode()
        signature = "sha256=" + hmac.new(b"fixture-secret", raw, hashlib.sha256).hexdigest()
        self.handler("/webhooks/meta", raw, {"X-Hub-Signature-256": signature}).do_POST()
        summary = self.handler("/api/summary?days=7")
        summary.do_GET()
        data = summary.respond.call_args.args[1]
        self.assertEqual(data["conversations"], 1)
        self.assertEqual(data["messages_received"], 1)
        self.assertEqual(data["coverage"]["includes_outbound"], False)
        self.assertIn("ingresos", data["coverage"]["note"])


if __name__ == "__main__":
    unittest.main()
