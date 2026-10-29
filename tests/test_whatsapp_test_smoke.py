import json
import unittest
from unittest.mock import Mock

from scripts.whatsapp_test_smoke import TestConfig, load_config, send_hello_world


class WhatsAppTestSmokeTests(unittest.TestCase):
    def setUp(self):
        self.environment = {
            "WHATSAPP_TEST_GRAPH_VERSION": "v99.0",
            "WHATSAPP_TEST_PHONE_NUMBER_ID": "123456789",
            "WHATSAPP_TEST_ACCESS_TOKEN": "test-only-token",
            "WHATSAPP_TEST_RECIPIENT": "+573001112233",
        }

    def test_loads_config_without_printing_or_changing_secret(self):
        config = load_config(self.environment)
        self.assertEqual(config.access_token, "test-only-token")
        self.assertEqual(self.environment["WHATSAPP_TEST_ACCESS_TOKEN"], "test-only-token")

    def test_rejects_missing_and_malformed_values(self):
        with self.assertRaisesRegex(ValueError, "ACCESS_TOKEN"):
            load_config({})
        self.environment["WHATSAPP_TEST_GRAPH_VERSION"] = "latest"
        with self.assertRaisesRegex(ValueError, "GRAPH_VERSION"):
            load_config(self.environment)

    def test_sends_fixed_hello_world_payload_to_fixed_meta_host(self):
        response = Mock(status=200)
        response.read.return_value = json.dumps({"messages": [{"id": "wamid.test-1"}]}).encode()
        connection = Mock()
        connection.getresponse.return_value = response
        factory = Mock(return_value=connection)
        config = load_config(self.environment)

        message_id = send_hello_world(config, factory)

        self.assertEqual(message_id, "wamid.test-1")
        factory.assert_called_once()
        self.assertEqual(factory.call_args.args[0], "graph.facebook.com")
        request = connection.request.call_args
        self.assertEqual(request.args[0], "POST")
        self.assertEqual(request.args[1], "/v99.0/123456789/messages")
        body = json.loads(request.kwargs["body"])
        self.assertEqual(body["template"]["name"], "hello_world")
        self.assertEqual(body["to"], "+573001112233")
        self.assertEqual(request.kwargs["headers"]["Authorization"], "Bearer test-only-token")
        connection.close.assert_called_once()

    def test_http_errors_do_not_expose_response_body_and_close(self):
        response = Mock(status=400)
        response.read.return_value = b"sensitive diagnostic"
        connection = Mock()
        connection.getresponse.return_value = response
        with self.assertRaisesRegex(RuntimeError, "HTTP 400") as caught:
            send_hello_world(
                TestConfig("v99.0", "123456789", "secret", "573001112233"),
                lambda *args, **kwargs: connection,
            )
        self.assertNotIn("sensitive", str(caught.exception))
        connection.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
