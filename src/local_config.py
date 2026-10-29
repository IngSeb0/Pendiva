"""Load the optional local .env without printing or executing its contents."""
from pathlib import Path
import os
import re


def load_local_config(path: Path, environment=None) -> dict:
    config = {}
    path = Path(path)
    if path.is_file():
        for number, raw in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            key, separator, value = line.partition("=")
            key, value = key.strip(), value.strip()
            if not separator or not re.fullmatch(r"[A-Z][A-Z0-9_]*", key):
                raise ValueError(f"Formato de .env inválido en la línea {number}.")
            if len(value) >= 2 and value[0] in "\"'" and value[-1] == value[0]:
                value = value[1:-1]
            elif value.startswith(("\"", "'")):
                raise ValueError(f"Comillas incompletas en .env, línea {number}.")
            config[key] = value
    config.update(os.environ if environment is None else environment)
    return config
