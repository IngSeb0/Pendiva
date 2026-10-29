import json
import unittest
from unittest.mock import Mock

from spikes.meta_embedded_signup.server import (
    MetaConfig,
    MetaSignupClient,
    MetaSignupError,
    load_config,
    render_page,
)


class MetaEmbeddedSignupTests(unittest.TestCase):
    def setUp(self):
        self.config = MetaConfig("123456", "654321", "secret-app-value", "v99.0")

    def test_config_requires_complete_values_and_validates_versions(self):
        self.assertIsNone(load_config({}))
        with self.assertRaisesRegex(ValueError, "GRAPH_VERSION"):
            load_config({
                "META_APP_ID": "123",
                "META_EMBEDDED_SIGNUP_CONFIG_ID": "456",
                "META_APP_SECRET": "secret",
                "META_GRAPH_VERSION": "latest",
            })
        config = load_config({
            "META_APP_ID": "123",
            "META_EMBEDDED_SIGNUP_CONFIG_ID": "456",
            "META_APP_SECRET": "secret",
            "META_GRAPH_VERSION": "v99.0",
        })
        self.assertEqual(config.app_id, "123")

    def test_signup_extras_are_optional_and_limited_to_known_fields(self):
        env = {
            "META_APP_ID": "123",
            "META_EMBEDDED_SIGNUP_CONFIG_ID": "456",
            "META_APP_SECRET": "secret",
            "META_GRAPH_VERSION": "v99.0",
            "META_EMBEDDED_SIGNUP_EXTRAS": '{"featureType":"whatsapp_business_app_onboarding"}',
        }
        config = load_config(env)
        self.assertEqual(config.signup_extras["featureType"], "whatsapp_business_app_onboarding")
        env["META_EMBEDDED_SIGNUP_EXTRAS"] = '{"access_token":"do-not-expose"}'
        with self.assertRaisesRegex(ValueError, "unsupported keys"):
            load_config(env)

    def test_page_embeds_public_configuration_but_not_app_secret(self):
        html = render_page(self.config).decode()
        self.assertIn('"appId": "123456"', html)
        self.assertIn('"configId": "654321"', html)
        self.assertNotIn("secret-app-value", html)

    def test_code_exchange_and_phone_lookup_keep_token_server_side(self):
        token_response = Mock()
        token_response.__enter__ = Mock(return_value=token_response)
        token_response.__exit__ = Mock(return_value=False)
        token_response.read.return_value = json.dumps({"access_token": "private-token"}).encode()
        phone_response = Mock()
        phone_response.__enter__ = Mock(return_value=phone_response)
        phone_response.__exit__ = Mock(return_value=False)
        phone_response.read.return_value = json.dumps({"data": [{
            "id": "987654321",
            "display_phone_number": "+57 300 111 2233",
            "verified_name": "Demo Business",
        }]}).encode()
        opener = Mock(side_effect=[token_response, phone_response])

        result = MetaSignupClient(self.config, opener).complete("auth-code", "112233")

        self.assertEqual(result, {
            "waba_id": "112233",
            "phone_numbers": [{
                "id": "987654321",
                "display_phone_number": "+57 300 111 2233",
                "verified_name": "Demo Business",
            }],
        })
        token_request = opener.call_args_list[0].args[0]
        self.assertIn("client_secret=secret-app-value", token_request.full_url)
        phone_request = opener.call_args_list[1].args[0]
        self.assertEqual(phone_request.get_header("Authorization"), "Bearer private-token")
        self.assertNotIn("private-token", repr(result))
        self.assertEqual(opener.call_count, 2)

    def test_invalid_ids_and_meta_errors_are_sanitized(self):
        with self.assertRaises(MetaSignupError):
            MetaSignupClient(self.config).complete("code", "not-an-id")

        failing = Mock(side_effect=OSError("sensitive response detail"))
        with self.assertRaises(MetaSignupError) as caught:
            MetaSignupClient(self.config, failing).complete("code", "112233")
        self.assertNotIn("sensitive", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
