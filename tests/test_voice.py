import io
import json
import unittest
from unittest.mock import Mock
from src.voice import DEFAULT_VOICE, VoiceError, synthesize, transcribe


class VoiceTests(unittest.TestCase):
    def test_elevenlabs_request_uses_server_key_and_fixed_host(self):
        opener = Mock(return_value=io.BytesIO(b"fake-mp3"))
        self.assertEqual(synthesize("Revisa la cotización.", "fixture-key", opener=opener), b"fake-mp3")
        request = opener.call_args.args[0]
        self.assertTrue(request.full_url.startswith("https://api.elevenlabs.io/v1/text-to-speech/" + DEFAULT_VOICE))
        self.assertEqual(request.get_header("Xi-api-key"), "fixture-key")
        self.assertEqual(json.loads(request.data)["model_id"], "eleven_multilingual_v2")
        self.assertNotIn("fixture-key", request.data.decode())

    def test_refuses_invalid_voice_or_oversized_text_before_network(self):
        opener = Mock()
        for text, key, voice in (("", "key", DEFAULT_VOICE), ("x" * 1201, "key", DEFAULT_VOICE),
                                 ("hola", "", DEFAULT_VOICE), ("hola", "key", "../evil")):
            with self.subTest(text=text[:8], voice=voice):
                with self.assertRaises(VoiceError):
                    synthesize(text, key, voice, opener)
        opener.assert_not_called()

    def test_provider_errors_do_not_expose_credentials(self):
        with self.assertRaises(VoiceError) as error:
            synthesize("hola", "fixture-secret", opener=Mock(side_effect=OSError("fixture-secret")))
        self.assertNotIn("fixture-secret", str(error.exception))

    def test_transcription_sends_only_audio_and_returns_text(self):
        opener = Mock(return_value=io.BytesIO(b'{"text":"Necesito una cotizacion"}'))
        self.assertEqual(transcribe(b"fake-voice", "audio/webm", "fixture-key", opener), "Necesito una cotizacion")
        request = opener.call_args.args[0]
        self.assertEqual(request.full_url, "https://api.elevenlabs.io/v1/speech-to-text")
        self.assertIn(b"fake-voice", request.data)
        self.assertIn(b"scribe_v2", request.data)
        self.assertNotIn(b"fixture-key", request.data)

    def test_transcription_limits_audio_before_any_request(self):
        opener = Mock()
        for audio, mime in ((b"", "audio/webm"), (b"x" * 128001, "audio/webm"), (b"x", "text/html")):
            with self.assertRaises(VoiceError):
                transcribe(audio, mime, "fixture-key", opener)
        opener.assert_not_called()
