"""Muse extraction contract; all responses are simulated."""
import json
import unittest
from unittest.mock import MagicMock, Mock

from src.live_pipeline import AnalysisError
from src.opportunity_extraction import propose_opportunities


class ExtractionTests(unittest.TestCase):
    def setUp(self):
        self.messages = [{'id': 'private-message-id', 'sender': 'private-number', 'timestamp': 100,
                          'text': 'Necesito limpiar un sofá. Mi presupuesto es 100.', 'kind': 'text'},
                         {'id': 'image-id', 'sender': 'private-number', 'timestamp': 101,
                          'text': 'Imagen recibida', 'kind': 'image'}]

    def response(self, suggestion):
        response = MagicMock()
        response.__enter__.return_value.read.return_value = json.dumps({'status': 'completed', 'output': [
            {'type': 'message', 'content': [{'type': 'output_text', 'text': json.dumps({'suggestions': [suggestion]})}]}]}).encode()
        return response

    def test_aliases_text_only_and_validated_source(self):
        response = self.response({'service': 'Sofá', 'value': '100', 'next_action': 'Pedir medidas', 'source': 'mensaje_1'})
        opener = Mock(return_value=response)
        result = propose_opportunities(self.messages, 'fixture', opener=opener)
        body = json.loads(opener.call_args.args[0].data)
        self.assertNotIn('private-message-id', body['input'])
        self.assertNotIn('private-number', body['input'])
        self.assertNotIn('Imagen recibida', body['input'])
        self.assertFalse(body['store'])
        self.assertEqual(result[0]['source'], 'private-message-id')
        self.assertEqual(result[0]['value'], '100')
        self.assertEqual(result[0]['source_timestamp'], 100)

    def test_invented_sources_rejected_and_unquoted_amount_removed(self):
        suggestion = {'service': 'Sofá', 'value': '999', 'next_action': 'Pedir medidas', 'source': 'mensaje_1'}
        result = propose_opportunities(self.messages, 'fixture', opener=Mock(return_value=self.response(suggestion)))
        self.assertEqual(result[0]['value'], '')
        suggestion['source'] = 'mensaje_2'
        with self.assertRaises(AnalysisError):
            propose_opportunities(self.messages, 'fixture', opener=Mock(return_value=self.response(suggestion)))

    def test_missing_key_and_incomplete_response_fail(self):
        opener = Mock()
        with self.assertRaises(ValueError):
            propose_opportunities(self.messages, '', opener=opener)
        opener.assert_not_called()
        response = MagicMock()
        response.__enter__.return_value.read.return_value = b'{"status":"incomplete"}'
        with self.assertRaises(AnalysisError):
            propose_opportunities(self.messages, 'fixture', opener=Mock(return_value=response))

    def test_media_observation_is_aliased_and_amount_is_never_inferred(self):
        media = [{'id':'private-file-id', 'name':'sofa.jpg', 'result':'Parece un sofá; precio 100', 'analyzed_at':'2026-10-01T10:00:00Z'}]
        opener = Mock(return_value=self.response({'service':'Limpieza de sofá','value':'100',
                                                  'next_action':'Confirmar tipo','source':'archivo_1'}))
        result = propose_opportunities(self.messages, 'fixture', opener=opener, media=media)
        self.assertEqual(result[0]['source_type'], 'media')
        self.assertEqual(result[0]['source'], 'private-file-id')
        self.assertEqual(result[0]['value'], '')
        self.assertEqual(len(result[0]['source_digest']),64)
        self.assertNotIn('private-file-id',json.loads(opener.call_args.args[0].data)['input'])
