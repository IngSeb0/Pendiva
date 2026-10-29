import io
import json
from pathlib import Path
import tempfile
from unittest import TestCase
from unittest.mock import MagicMock, Mock, patch
from urllib.error import HTTPError
from urllib.parse import parse_qs

from scripts.iniciar_demo import check_config, check_model, main
from scripts.configurar_webhook import configure, graph_request, validate_receiver


class DemoSetupTests(TestCase):
    def config(self, **extra):
        return {"WHATSAPP_PHONE_NUMBER_ID": "123", "WHATSAPP_TEST_PHONE_NUMBER_ID": "123",
                "WHATSAPP_APP_SECRET": "fixture-secret", "WHATSAPP_VERIFY_TOKEN": "fixture-verify",
                "WHATSAPP_TEST_GRAPH_VERSION": "v25.0", "PENDIVA_AI_PROVIDER": "nebius",
                "NEBIUS_API_KEY": "fixture-ai", **extra}

    def response(self, data):
        response = MagicMock()
        response.read.return_value = json.dumps(data).encode()
        response.status = 200
        response.__enter__.return_value = response
        return response

    def test_check_does_not_expose_secret_or_recipient(self):
        config = self.config(WHATSAPP_TEST_RECIPIENT="573000000000", WHATSAPP_TEST_ACCESS_TOKEN="fixture-access")
        report = check_config(config)
        self.assertTrue(report["configured"])
        for value in ("fixture-secret", "fixture-ai", "fixture-access", "573000000000", "fixture-verify"):
            self.assertNotIn(value, json.dumps(report))

    def test_missing_provider_key_and_mismatched_senders_block_start(self):
        self.assertFalse(check_config(self.config(NEBIUS_API_KEY=""))["configured"])
        report = check_config(self.config(WHATSAPP_TEST_PHONE_NUMBER_ID="999"))
        self.assertFalse(report["configured"])
        self.assertTrue(report["problems"])

    def test_invalid_provider_or_ports_block_start(self):
        for extra in ({"PENDIVA_AI_PROVIDER": "unknown"}, {"PENDIVA_PORT": "8772"},
                      {"PENDIVA_PORT": "oops"}, {"PENDIVA_WEBHOOK_PORT": "80"}):
            with self.subTest(extra=extra):
                self.assertFalse(check_config(self.config(**extra))["configured"])

    def test_model_check_uses_only_fictional_data_and_reports_metadata(self):
        analyzer = Mock(return_value={"model": "fixture-model", "recomendaciones": []})
        result = check_model(self.config(), analyzer)
        messages = analyzer.call_args.args[0]
        self.assertEqual(len(messages), 1)
        self.assertTrue(messages[0]["id"].startswith("synthetic."))
        self.assertEqual(set(messages[0]), {"id", "timestamp", "text"})
        self.assertEqual(result["data"], "synthetic")
        self.assertNotIn("fixture-ai", json.dumps(result))

    def test_model_check_can_select_muse_without_changing_environment(self):
        config = self.config(MODEL_API_KEY="fixture-muse")
        result = {"provider": "meta", "model": "fixture-model", "recommendations": 1, "data": "synthetic", "valid": True}
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as directory, \
             patch("scripts.iniciar_demo.ROOT", Path(directory)), \
             patch("scripts.iniciar_demo.load_local_config", return_value=config), \
             patch("scripts.iniciar_demo.check_model", return_value=result) as run, \
             patch("sys.stdout", new_callable=io.StringIO), \
             patch.dict("os.environ", {"PENDIVA_AI_PROVIDER": "nebius"}, clear=True):
            self.assertEqual(main(["--check-model", "--provider", "meta"]), 0)
            self.assertEqual(run.call_args.args[0]["PENDIVA_AI_PROVIDER"], "meta")
            self.assertEqual(json.loads((Path(directory) / "data" / "model-check-meta.json").read_text())["provider"], "meta")
            import os
            self.assertEqual(os.environ["PENDIVA_AI_PROVIDER"], "nebius")

    def test_graph_refuses_other_app_before_network(self):
        opener = Mock()
        with self.assertRaises(ValueError):
            graph_request(self.config(WHATSAPP_APP_ID="other"), opener=opener)
        opener.assert_not_called()

    def test_rejects_nonlocal_tunnel_targets_before_request(self):
        opener = Mock()
        for url in ("http://example.com/webhooks/meta", "https://evil.example/webhooks/meta",
                    "https://fixture.trycloudflare.com/api/status", "https://fixture.trycloudflare.com/webhooks/meta?x=y"):
            with self.assertRaises(ValueError):
                validate_receiver(url, "fixture-verify", opener)
        opener.assert_not_called()

    def test_public_probe_requires_blocked_panel_and_unsigned_events(self):
        def opener(request, **kwargs):
            url = request if isinstance(request, str) else request.full_url
            if "hub.challenge=" in url:
                response = self.response({})
                response.read.return_value = parse_qs(url.split("?", 1)[1])["hub.challenge"][0].encode()
                return response
            code = 403 if not isinstance(request, str) else 404
            raise HTTPError(url, code, "fixture", {}, io.BytesIO())
        self.assertTrue(validate_receiver("https://fixture.trycloudflare.com/webhooks/meta", "fixture-verify", opener)["panel_blocked"])
        with self.assertRaises(ValueError):
            validate_receiver("https://fixture.trycloudflare.com/webhooks/meta", "fixture-verify", lambda *a, **k: self.response({}))

    def test_configure_preserves_fields_and_confirms_by_reading_back(self):
        callback = "https://fixture.trycloudflare.com/webhooks/meta"
        def row(url):
            return {"data": [{"object": "whatsapp_business_account", "callback_url": url, "active": True,
                              "fields": [{"name": "messages"}, {"name": "account_update"}]}]}
        opener = Mock(side_effect=[self.response(row("https://old.trycloudflare.com/webhooks/meta")),
                                  self.response({"success": True}), self.response(row(callback))])
        with patch("scripts.configurar_webhook.validate_receiver", return_value={"panel_blocked": True}) as validate:
            result = configure(self.config(), callback, opener)
        validate.assert_called_once()
        post = opener.call_args_list[1].args[0]
        values = parse_qs(post.data.decode())
        self.assertEqual(set(values["fields"][0].split(",")), {"messages", "account_update"})
        self.assertEqual(values["callback_url"], [callback])
        self.assertEqual(result["callback_url"], callback)
        self.assertNotIn("fixture-secret", json.dumps(result))
        self.assertNotIn("fixture-verify", json.dumps(result))

    def test_receiver_failure_never_mutates_meta(self):
        opener = Mock(return_value=self.response({"data": [{"object": "whatsapp_business_account", "fields": []}]}))
        with patch("scripts.configurar_webhook.validate_receiver", side_effect=ValueError("unsafe")):
            with self.assertRaises(ValueError):
                configure(self.config(), "https://fixture.trycloudflare.com/webhooks/meta", opener)
        self.assertEqual(opener.call_count, 1)
