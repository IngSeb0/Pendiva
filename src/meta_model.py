"""Optional Meta Model API analysis of bundled fictional cases only."""

from __future__ import annotations

import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

MODEL = "muse-spark-1.3"
URL = "https://api.meta.ai/v1/responses"


class MetaModelError(RuntimeError):
    """Safe, sanitized error for the local demo."""


def analyze_case(case: dict, api_key: str, opener=urlopen) -> dict:
    """Request a single synthetic analysis and validate the evidence reference."""
    if not api_key:
        raise MetaModelError("Falta configurar MODEL_API_KEY en el servidor local.")
    messages = case["messages"]
    prompt = (
        "Analiza esta conversación ficticia de ventas. Devuelve SOLO JSON con "
        "las claves resumen y siguiente_paso (textos breves en español) y "
        "evidencia_indice (entero cero-basado de un mensaje que apoye el resumen). "
        "No inventes hechos, no confirmes pagos, no marques ventas como perdidas; "
        "si faltan datos, dilo. La salida es una sugerencia para revisión humana.\n"
        + json.dumps(messages, ensure_ascii=False)
    )
    payload = json.dumps({"model": MODEL, "input": prompt, "store": False,
                          "max_output_tokens": 1024}, ensure_ascii=False).encode("utf-8")
    request = Request(URL, data=payload, method="POST", headers={
        "Authorization": f"Bearer {api_key}", "Content-Type": "application/json",
    })
    try:
        with opener(request, timeout=30) as response:
            body = json.loads(response.read())
        texts = [part["text"] for item in body.get("output", []) if item.get("type") == "message"
                 for part in item.get("content", []) if part.get("type") == "output_text"]
        result = json.loads("".join(texts))
        summary, action, index = result["resumen"], result["siguiente_paso"], result["evidencia_indice"]
        if (not isinstance(summary, str) or not summary.strip() or len(summary) > 800
                or not isinstance(action, str) or not action.strip() or len(action) > 800
                or isinstance(index, bool) or not isinstance(index, int) or not 0 <= index < len(messages)):
            raise ValueError("invalid result")
    except (HTTPError, URLError, TimeoutError, OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        # Provider response and exceptions can contain sensitive details; never expose them.
        raise MetaModelError("Meta no devolvió un análisis válido. Revisa acceso y configuración.") from exc
    return {"summary": summary.strip(), "action": action.strip(),
            "evidence": messages[index]["text"], "model": MODEL}
