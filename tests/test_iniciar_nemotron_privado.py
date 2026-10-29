import io
import json
import os
import unittest
from contextlib import redirect_stdout
from unittest.mock import MagicMock, Mock, patch
from urllib.error import HTTPError

from scripts.iniciar_nemotron_privado import main, test_connection as check_connection


class PrivateNvidiaStartTests(unittest.TestCase):
    def test_smoke_request_is_neutral_and_has_no_key_in_payload(self):
        response = MagicMock()
        response.__enter__.return_value = response
        response.read.return_value = json.dumps({"choices": [{"message": {"content": "listo"}}]}).encode()
        opener = Mock(return_value=response)
        check_connection("fixture-key", opener=opener)
        request = opener.call_args.args[0]
        self.assertNotIn("fixture-key", request.data.decode())
        self.assertEqual(request.full_url, "https://integrate.api.nvidia.com/v1/chat/completions")
        self.assertEqual(json.loads(request.data)["messages"][0]["content"], "Responde: listo.")

    def test_failed_request_does_not_expose_key_or_start_server(self):
        with patch("scripts.iniciar_nemotron_privado.getpass.getpass", return_value="fixture-key"), \
             patch("scripts.iniciar_nemotron_privado.test_connection", side_effect=RuntimeError("Error de conexión")), \
             patch("scripts.iniciar_nemotron_privado.runpy.run_module") as run, \
             redirect_stdout(io.StringIO()) as output:
            main()
        run.assert_not_called()
        self.assertNotIn("fixture-key", output.getvalue())

    def test_http_error_is_sanitized(self):
        opener = Mock(side_effect=HTTPError("https://example.invalid/fixture-key", 401, "fixture-key", None, None))
        with self.assertRaises(RuntimeError) as error:
            check_connection("fixture-key", opener=opener)
        self.assertIn("401", str(error.exception))
        self.assertNotIn("fixture-key", str(error.exception))

    def test_success_starts_local_server_with_explicit_nvidia_provider(self):
        with patch("scripts.iniciar_nemotron_privado.getpass.getpass", return_value="fixture-key"), \
             patch("scripts.iniciar_nemotron_privado.test_connection") as check, \
             patch("scripts.iniciar_nemotron_privado.runpy.run_module") as run, \
             patch.dict(os.environ, {}, clear=True), redirect_stdout(io.StringIO()) as output:
            main()
            self.assertEqual(os.environ["PENDIVA_AI_PROVIDER"], "nvidia")
            self.assertEqual(os.environ["NVIDIA_API_KEY"], "fixture-key")
            self.assertEqual(os.environ["PENDIVA_PORT"], "8768")
            check.assert_called_once_with("fixture-key")
            run.assert_called_once_with("src.live_app", run_name="__main__")
        self.assertNotIn("fixture-key", output.getvalue())
