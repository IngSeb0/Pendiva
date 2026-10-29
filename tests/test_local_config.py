import tempfile
import unittest
from pathlib import Path

from src.local_config import load_local_config


class LocalConfigTests(unittest.TestCase):
    def test_parses_values_without_expansion_and_environment_takes_precedence(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as directory:
            path = Path(directory) / "test-config"
            path.write_text("# local\nTOKEN='fixture#literal'\nPROVIDER=nebius\n", encoding="utf-8")
            config = load_local_config(path, {"PROVIDER": "meta"})
            self.assertEqual(config, {"TOKEN": "fixture#literal", "PROVIDER": "meta"})

    def test_bad_line_does_not_report_content(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as directory:
            path = Path(directory) / "test-config"
            path.write_text("bad fixture-secret", encoding="utf-8")
            with self.assertRaises(ValueError) as error:
                load_local_config(path, {})
            self.assertNotIn("fixture-secret", str(error.exception))

    def test_missing_file_is_allowed(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as directory:
            self.assertEqual(load_local_config(Path(directory) / "missing", {"A": "b"}), {"A": "b"})

