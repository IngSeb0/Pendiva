import json
import unittest
from unittest.mock import Mock

from src.demo_cases import CASES
from src.meta_model import MetaModelError, analyze_case


class MetaModelTests(unittest.TestCase):
    def test_builds_meta_request_and_resolves_evidence_from_fixture(self):
        response = Mock()
        response.__enter__ = Mock(return_value=response)
        response.__exit__ = Mock(return_value=False)
        response.read.return_value = json.dumps({"output": [{"type": "message", "content": [{
            "type": "output_text", "text": json.dumps({"resumen": "Solicita una cotización.",
                                                         "siguiente_paso": "Preparar propuesta.",
                                                         "evidencia_indice": 2})}]}]}).encode()
        opener = Mock(return_value=response)
        result = analyze_case(CASES[0], "fixture-key", opener=opener)
        request = opener.call_args.args[0]
        body = json.loads(request.data)
        self.assertEqual(request.full_url, "https://api.meta.ai/v1/responses")
        self.assertEqual(body["model"], "muse-spark-1.3")
        self.assertIs(body["store"], False)
        self.assertEqual(result["evidence"], CASES[0]["messages"][2]["text"])
        self.assertNotIn("fixture-key", json.dumps(result))

    def test_rejects_bad_evidence_and_sanitizes_provider_errors(self):
        response = Mock()
        response.__enter__ = Mock(return_value=response)
        response.__exit__ = Mock(return_value=False)
        response.read.return_value = json.dumps({"output": [{"type": "message", "content": [{
            "type": "output_text", "text": json.dumps({"resumen": "x", "siguiente_paso": "y", "evidencia_indice": 99})}]}]}).encode()
        with self.assertRaises(MetaModelError):
            analyze_case(CASES[0], "fixture-key", opener=Mock(return_value=response))
        with self.assertRaises(MetaModelError) as error:
            analyze_case(CASES[0], "fixture-key", opener=Mock(side_effect=OSError("fixture-key")))
        self.assertNotIn("fixture-key", str(error.exception))

    def test_no_request_without_key(self):
        opener = Mock()
        with self.assertRaises(MetaModelError):
            analyze_case(CASES[0], "", opener=opener)
        opener.assert_not_called()
