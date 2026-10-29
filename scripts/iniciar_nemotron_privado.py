"""Prompt for an NVIDIA key, make one neutral smoke request and open Pendiva."""
import getpass
import json
import os
import runpy
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from src.live_pipeline import NVIDIA_MODEL, NVIDIA_URL


def test_connection(api_key: str, opener=urlopen) -> None:
    if not api_key.strip():
        raise ValueError("No se ingresó una clave.")
    payload = {"model": NVIDIA_MODEL, "messages": [{"role": "user", "content": "Responde: listo."}],
               "max_tokens": 512, "stream": False, "reasoning_effort": "none"}
    request = Request(NVIDIA_URL, data=json.dumps(payload).encode(), method="POST", headers={
        "Authorization": f"Bearer {api_key}", "Content-Type": "application/json"})
    try:
        with opener(request, timeout=45) as response:
            body = json.loads(response.read())
        content = body["choices"][0]["message"]["content"]
        if not isinstance(content, str) or not content.strip():
            raise ValueError("NVIDIA no devolvió una respuesta de chat válida.")
    except HTTPError as error:
        raise RuntimeError(f"NVIDIA devolvió HTTP {error.code}; revisa clave, permisos y créditos.") from None
    except (URLError, OSError, ValueError, KeyError, IndexError, TypeError, AttributeError) as error:
        raise RuntimeError("No fue posible validar la conexión con NVIDIA.") from None


def main() -> None:
    print("Se hará una única solicitud breve a NVIDIA para probar la clave; puede consumir créditos.")
    key = getpass.getpass("Pega tu clave de NVIDIA API y pulsa Enter (no se mostrará): ")
    try:
        test_connection(key)
    except (ValueError, RuntimeError) as error:
        print(str(error))
        return
    os.environ["PENDIVA_AI_PROVIDER"] = "nvidia"
    os.environ["NVIDIA_API_KEY"] = key
    os.environ["PENDIVA_PORT"] = "8768"
    print("NVIDIA aceptó la solicitud de prueba. Abre http://127.0.0.1:8768/.")
    print("El webhook de WhatsApp requiere configuración separada. Pulsa Ctrl+C para cerrar.")
    runpy.run_module("src.live_app", run_name="__main__")


if __name__ == "__main__":
    main()
