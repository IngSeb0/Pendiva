"""Optional ElevenLabs speech output. The key never reaches the browser."""
import json
import re
import secrets
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

DEFAULT_VOICE = "JBFqnCBsd6RMkjVDRZzb"  # Public example voice from ElevenLabs documentation.
MAX_VOICE_CHARS = 1200
MAX_AUDIO_BYTES = 4 * 1024 * 1024
MAX_RECORDING_BYTES = 128000
RECORDING_MIMES = frozenset({"audio/webm", "audio/ogg", "audio/mp4", "audio/wav", "audio/mpeg"})


class VoiceError(RuntimeError):
    pass


def synthesize(text, api_key, voice_id=DEFAULT_VOICE, opener=urlopen):
    if not isinstance(text, str) or not text.strip() or len(text) > MAX_VOICE_CHARS:
        raise VoiceError("La respuesta para escuchar debe tener entre 1 y 1200 caracteres.")
    if not api_key:
        raise VoiceError("Falta configurar la clave de ElevenLabs.")
    if not re.fullmatch(r"[A-Za-z0-9]{1,64}", voice_id):
        raise VoiceError("La voz de ElevenLabs no tiene un identificador válido.")
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}?output_format=mp3_44100_128"
    payload = json.dumps({"text": text.strip(), "model_id": "eleven_multilingual_v2"}, ensure_ascii=False).encode()
    request = Request(url, data=payload, method="POST", headers={"xi-api-key": api_key,
                      "Content-Type": "application/json", "Accept": "audio/mpeg"})
    try:
        with opener(request, timeout=30) as response:
            audio = response.read(MAX_AUDIO_BYTES + 1)
        if not audio or len(audio) > MAX_AUDIO_BYTES:
            raise ValueError("invalid audio size")
        return audio
    except (HTTPError, URLError, TimeoutError, OSError, ValueError) as exc:
        raise VoiceError("ElevenLabs no pudo generar el audio; revisa la clave, la voz y los créditos.") from exc


def transcribe(audio, mime, api_key, opener=urlopen):
    if not isinstance(audio, bytes) or not audio or len(audio) > MAX_RECORDING_BYTES or mime not in RECORDING_MIMES:
        raise VoiceError("La grabación no es válida o supera el límite de esta demo.")
    if not api_key:
        raise VoiceError("Falta configurar la clave de ElevenLabs.")
    boundary = "pendiva-" + secrets.token_hex(16)
    parts = []
    for name, value in (("model_id", "scribe_v2"), ("language_code", "es"), ("tag_audio_events", "false")):
        parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"\r\n\r\n{value}\r\n'.encode())
    parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="pregunta"\r\nContent-Type: {mime}\r\n\r\n'.encode())
    parts.append(audio)
    parts.append(f"\r\n--{boundary}--\r\n".encode())
    request = Request("https://api.elevenlabs.io/v1/speech-to-text", data=b"".join(parts), method="POST",
                      headers={"xi-api-key": api_key, "Content-Type": f"multipart/form-data; boundary={boundary}"})
    try:
        with opener(request, timeout=45) as response:
            body = json.loads(response.read(1024 * 1024))
        text = body.get("text")
        if not isinstance(text, str) or not text.strip() or len(text) > 1000:
            raise ValueError("invalid transcript")
        return text.strip()
    except (HTTPError, URLError, TimeoutError, OSError, ValueError, TypeError, AttributeError) as exc:
        raise VoiceError("ElevenLabs no pudo transcribir el audio; revisa acceso y créditos.") from exc
