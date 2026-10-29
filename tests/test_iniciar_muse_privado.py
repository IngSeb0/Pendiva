import os
import unittest
from unittest.mock import patch

from scripts.iniciar_muse_privado import main


class PrivateMuseStartTests(unittest.TestCase):
    def test_empty_key_does_not_start_server(self):
        with patch("scripts.iniciar_muse_privado.getpass.getpass", return_value=""), \
             patch("scripts.iniciar_muse_privado.runpy.run_module") as run, \
             patch.dict(os.environ, {}, clear=True):
            main()
        run.assert_not_called()

    def test_key_is_passed_only_to_local_process_environment(self):
        with patch("scripts.iniciar_muse_privado.getpass.getpass", return_value="fixture-key"), \
             patch("scripts.iniciar_muse_privado.runpy.run_module") as run, \
             patch.dict(os.environ, {"PENDIVA_AI_PROVIDER": "nebius"}, clear=True):
            main()
            self.assertEqual(os.environ["MODEL_API_KEY"], "fixture-key")
            self.assertEqual(os.environ["PENDIVA_AI_PROVIDER"], "meta")
            self.assertEqual(os.environ["PENDIVA_PORT"], "8767")
            run.assert_called_once_with("src.live_app", run_name="__main__")


if __name__ == "__main__":
    unittest.main()
