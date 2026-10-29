import json
from unittest import TestCase
from unittest.mock import MagicMock, Mock

from scripts.verificar_sandbox import PENDIVA_APP_ID, SandboxError, inspect_sandbox


class SandboxSubscriptionTests(TestCase):
    def setUp(self):
        self.config = {"WHATSAPP_APP_SECRET": "secret-fixture", "WHATSAPP_TEST_ACCESS_TOKEN": "token-fixture",
                       "WHATSAPP_PHONE_NUMBER_ID": "123", "WHATSAPP_TEST_PHONE_NUMBER_ID": "123",
                       "WHATSAPP_TEST_GRAPH_VERSION": "v25.0"}
        self.token = {"data": {"app_id": PENDIVA_APP_ID, "is_valid": True, "expires_at": 1793206800,
                               "scopes": ["whatsapp_business_management"]}}
        self.phone = {"data": [{"id": "123"}]}
        self.subscribed = {"data": [{"whatsapp_business_api_data": {"id": PENDIVA_APP_ID}}]}

    @staticmethod
    def response(data):
        response = MagicMock()
        response.read.return_value = json.dumps(data).encode()
        response.__enter__.return_value = response
        return response

    def test_read_only_inspection_sends_no_write_and_hides_credentials(self):
        opener = Mock(side_effect=[self.response(self.token), self.response(self.phone), self.response(self.subscribed)])
        report = inspect_sandbox(self.config, opener=opener)
        self.assertTrue(report["app_subscribed"])
        self.assertFalse(report["subscription_added"])
        self.assertTrue(all(call.args[0].get_method() == "GET" for call in opener.call_args_list))
        self.assertNotIn("fixture", json.dumps(report))

    def test_subscribe_adds_only_when_absent_and_reads_back(self):
        opener = Mock(side_effect=[self.response(self.token), self.response(self.phone), self.response({"data": []}),
                                   self.response({"success": True}), self.response(self.subscribed)])
        report = inspect_sandbox(self.config, subscribe=True, opener=opener)
        self.assertTrue(report["subscription_added"])
        self.assertTrue(report["app_subscribed"])
        self.assertEqual(opener.call_args_list[3].args[0].get_method(), "POST")
        self.assertEqual(opener.call_count, 5)

    def test_subscribe_is_noop_when_already_subscribed(self):
        opener = Mock(side_effect=[self.response(self.token), self.response(self.phone), self.response(self.subscribed)])
        report = inspect_sandbox(self.config, subscribe=True, opener=opener)
        self.assertFalse(report["subscription_added"])
        self.assertEqual(opener.call_count, 3)

    def test_rejects_mismatched_sender_before_changing_subscription(self):
        opener = Mock(side_effect=[self.response(self.token), self.response({"data": [{"id": "999"}]})])
        with self.assertRaises(SandboxError):
            inspect_sandbox(self.config, subscribe=True, opener=opener)
        self.assertEqual(opener.call_count, 2)

    def test_invalid_token_or_app_never_queries_account(self):
        for token in ({"data": {**self.token["data"], "is_valid": False}},
                      {"data": {**self.token["data"], "app_id": "another-app"}},
                      {"data": {**self.token["data"], "scopes": []}}):
            with self.subTest(token=token):
                opener = Mock(return_value=self.response(token))
                with self.assertRaises(SandboxError):
                    inspect_sandbox(self.config, subscribe=True, opener=opener)
                self.assertEqual(opener.call_count, 1)

    def test_partial_list_refuses_to_subscribe(self):
        phones = {**self.phone, "paging": {"next": "https://example.test/next"}}
        opener = Mock(side_effect=[self.response(self.token), self.response(phones)])
        with self.assertRaises(SandboxError):
            inspect_sandbox(self.config, subscribe=True, opener=opener)
        self.assertEqual(opener.call_count, 2)
