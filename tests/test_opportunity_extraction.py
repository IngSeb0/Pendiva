"""Muse extraction contract; all responses are simulated."""
import json
import csv
from pathlib import Path
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
        response = self.response({'service': 'Sofá', 'value': '100', 'amount_type':'customer_budget', 'next_action': 'Confirmar medidas y preparar cotización', 'source': 'mensaje_1'})
        opener = Mock(return_value=response)
        result = propose_opportunities(self.messages, 'fixture', opener=opener)
        body = json.loads(opener.call_args.args[0].data)
        self.assertNotIn('private-message-id', body['input'])
        self.assertNotIn('private-number', body['input'])
        self.assertNotIn('Imagen recibida', body['input'])
        self.assertFalse(body['store'])
        self.assertEqual(result[0]['source'], 'private-message-id')
        self.assertEqual(result[0]['value'], '100')
        self.assertEqual(result[0]['amount_type'], 'customer_budget')
        self.assertEqual(result[0]['amount_verification'], 'unverified')
        self.assertIn('business_quote', body['text']['format']['schema']['properties']['suggestions']['items']['properties']['amount_type']['enum'])
        self.assertEqual(result[0]['source_timestamp'], 100)

    def test_invented_sources_rejected_and_unquoted_amount_removed(self):
        suggestion = {'service': 'Sofá', 'value': '999', 'amount_type':'business_quote', 'next_action': 'Confirmar medidas', 'source': 'mensaje_1'}
        result = propose_opportunities(self.messages, 'fixture', opener=Mock(return_value=self.response(suggestion)))
        self.assertEqual(result[0]['value'], '')
        self.assertEqual(result[0]['amount_type'], 'unknown')
        self.assertEqual(result[0]['amount_verification'], 'unverified')
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
        opener = Mock(return_value=self.response({'service':'Limpieza de sofá','value':'100','amount_type':'estimate',
                                                  'next_action':'Confirmar tipo','source':'archivo_1'}))
        result = propose_opportunities(self.messages, 'fixture', opener=opener, media=media)
        self.assertEqual(result[0]['source_type'], 'media')
        self.assertEqual(result[0]['source'], 'private-file-id')
        self.assertEqual(result[0]['value'], '')
        self.assertEqual(result[0]['amount_type'], 'unknown')
        self.assertEqual(len(result[0]['source_digest']),64)
        self.assertNotIn('private-file-id',json.loads(opener.call_args.args[0].data)['input'])

    def test_quote_request_budget_and_payment_claim_are_semantically_distinct(self):
        cases = [
            ('Mi presupuesto es 120000 pesos para limpiar el sofá.', '120000 pesos', 'customer_budget'),
            ('El negocio cotizó el servicio en 120000 pesos.', '120000 pesos', 'business_quote'),
            ('Ya pagué 120000 pesos por el servicio.', '120000 pesos', 'payment_claim'),
        ]
        for text, amount, amount_type in cases:
            with self.subTest(amount_type=amount_type):
                message = {'id':'source-message','sender':'contact','timestamp':1,'text':text,'kind':'text'}
                suggestion = {'service':'Limpieza de sofá','value':amount,'amount_type':amount_type,
                              'next_action':'Verificar el contexto y el siguiente paso','source':'mensaje_1'}
                result = propose_opportunities([message], 'fixture', opener=Mock(return_value=self.response(suggestion)))
                self.assertEqual(result[0]['value'], amount)
                self.assertEqual(result[0]['amount_type'], amount_type)
                self.assertEqual(result[0]['amount_verification'], 'unverified')

    def test_missing_price_never_receives_an_amount_classification(self):
        message = {'id':'source-message','sender':'contact','timestamp':1,'text':'¿Cuánto cuesta limpiar el sofá?','kind':'text'}
        suggestion = {'service':'Limpieza de sofá','value':'','amount_type':'unknown',
                      'next_action':'Preparar cotización tras confirmar el tamaño','source':'mensaje_1'}
        result = propose_opportunities([message], 'fixture', opener=Mock(return_value=self.response(suggestion)))
        self.assertEqual(result[0]['value'], '')
        self.assertEqual(result[0]['amount_type'], 'unknown')

    def test_bilingual_evaluation_fixture_has_24_synthetic_cases_and_safety_labels(self):
        path = Path(__file__).resolve().parents[1] / 'fixtures' / 'demo' / 'muse-commercial-evaluation-en-es.csv'
        with path.open(encoding='utf-8', newline='') as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 24)
        self.assertEqual({row['language'] for row in rows}, {'English', 'Spanish'})
        self.assertTrue(all(row['message'] and row['forbidden_inference'] for row in rows))
        self.assertTrue({'customer_budget','business_quote','payment_claim','unknown'}.issubset(
            {row['expected_amount_type'] for row in rows}))
