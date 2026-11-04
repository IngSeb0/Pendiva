import base64
from contextlib import closing
from datetime import date
import io
import json
import hashlib
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch
import wave

from src.business_assistant import init_assistant, snapshot
from src.custom_tools import activate, get_view, init_tools, list_views, preview, propose, quote_date_import
from src.demo_seed import DEMO_TENANT, seed_demo
from src.live_pipeline import LiveStore, parse_webhook, verify_signature
from src.multimodal import MediaError, add_media, analyze_media, get_media, init_media, list_media, save_result, pending_whatsapp_media, fetch_whatsapp_media
from tests import test_live_http

PNG = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAusB9Y9ZQmcAAAAASUVORK5CYII=')
SENDER = '573000000101'


def response(payload):
    mock = Mock()
    mock.__enter__ = Mock(return_value=mock)
    mock.__exit__ = Mock(return_value=False)
    mock.read.return_value = json.dumps(payload).encode()
    return mock


class StudioTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1])
        self.store = LiveStore(Path(self.directory.name) / 'studio.sqlite3')
        seed_demo(self.store)
        init_media(self.store); init_tools(self.store); init_assistant(self.store)

    def tearDown(self): self.directory.cleanup()

    def test_media_scoped_and_mime_checked(self):
        ident = add_media(self.store, DEMO_TENANT, SENDER, 'photo.png', 'image/png', base64.b64encode(PNG).decode())
        self.assertEqual(get_media(self.store, DEMO_TENANT, ident)['content'], PNG)
        self.assertIsNone(get_media(self.store, 'other-tenant', ident))
        self.assertIn(ident, [item['id'] for item in list_media(self.store, DEMO_TENANT, SENDER)])
        self.assertEqual(list_media(self.store, 'other-tenant', SENDER), [])
        with self.assertRaises(MediaError): add_media(self.store, DEMO_TENANT, SENDER, 'fake.jpg', 'image/jpeg', base64.b64encode(PNG).decode())
        with self.assertRaises(MediaError): add_media(self.store, 'other-tenant', SENDER, 'photo.png', 'image/png', base64.b64encode(PNG).decode())

    def test_image_request_uses_inline_media_and_preserves_observation(self):
        opener = Mock(return_value=response({'status':'completed','output':[{'type':'message','content':[{'type':'output_text','text':'Se ve un sofá; dimensiones desconocidas.'}]}]}))
        asset = {'mime':'image/png','content':PNG}
        self.assertIn('dimensiones desconocidas', analyze_media(asset, 'fixture-key', opener=opener))
        sent=json.loads(opener.call_args.args[0].data)
        self.assertEqual(sent['model'],'muse-spark-1.3')
        self.assertTrue(sent['input'][0]['content'][1]['image_url'].startswith('data:image/png;base64,'))
        self.assertFalse(sent['store'])

    def test_voice_transcript_uses_dedicated_api(self):
        wav=io.BytesIO()
        with wave.open(wav,'wb') as audio:
            audio.setnchannels(1); audio.setsampwidth(2); audio.setframerate(16000); audio.writeframes(b'\0\0'*800)
        ident=add_media(self.store, DEMO_TENANT, SENDER, 'clip.wav','audio/wav',base64.b64encode(wav.getvalue()).decode())
        opener=Mock(return_value=response({'transcript':'Hola, necesito limpieza.'}))
        text=analyze_media(get_media(self.store, DEMO_TENANT, ident),'fixture-key',opener=opener)
        self.assertEqual(text,'Hola, necesito limpieza.')
        self.assertIn(b'muse-voice-transcribe-1.0',opener.call_args.args[0].data)

    def test_media_observations_are_retrievable_with_sources(self):
        ident=add_media(self.store, DEMO_TENANT, SENDER,'photo.png','image/png',base64.b64encode(PNG).decode())
        save_result(self.store, DEMO_TENANT, ident, 'Sofá verde; dimensiones desconocidas.')
        selected, coverage, _, _ = snapshot(self.store, 'sofá verde', DEMO_TENANT)
        self.assertTrue(any(x['id']=='media:'+ident and 'Sofá verde' in x['text'] for x in selected))
        self.assertEqual(coverage['media_analyses'],1)
        self.assertEqual(snapshot(self.store, 'sofá', 'other-tenant')[1]['media_analyses'],0)

    def test_whatsapp_download_checks_scope_url_checksum_and_deduplicates(self):
        self.store.add_messages([{'id':'wamid.fake','sender':SENDER,'name':'Ana','timestamp':1,
                                  'text':'[imagen]','kind':'image','raw':{'image':{'id':'112233'}}}],tenant_id=DEMO_TENANT)
        self.assertEqual(pending_whatsapp_media(self.store,DEMO_TENANT,SENDER)[0]['message_id'],'wamid.fake')
        self.assertEqual(pending_whatsapp_media(self.store,'other',SENDER),[])
        metadata={'id':'112233','url':'https://lookaside.fbsbx.com/whatsapp_business/attachments/?fixture=1',
                  'mime_type':'image/png','file_size':len(PNG),'sha256':hashlib.sha256(PNG).hexdigest()}
        raw_response=Mock();raw_response.__enter__=Mock(return_value=raw_response);raw_response.__exit__=Mock(return_value=False);raw_response.read.return_value=PNG
        opener=Mock(side_effect=[response(metadata),raw_response])
        ident=fetch_whatsapp_media(self.store,DEMO_TENANT,SENDER,'wamid.fake','fixture-token','123','v25.0',opener)
        self.assertEqual(get_media(self.store,DEMO_TENANT,ident)['content'],PNG)
        self.assertEqual(pending_whatsapp_media(self.store,DEMO_TENANT,SENDER),[])
        self.assertEqual(sum(item['source_message_id']=='wamid.fake' for item in list_media(self.store,DEMO_TENANT,SENDER)),1)

    def test_whatsapp_download_rejects_untrusted_url_before_token_is_sent(self):
        self.store.add_messages([{'id':'wamid.fake','sender':SENDER,'name':'Ana','timestamp':1,
                                  'text':'[imagen]','kind':'image','raw':{'image':{'id':'112233'}}}],tenant_id=DEMO_TENANT)
        metadata={'id':'112233','url':'https://example.com/steal','mime_type':'image/png','file_size':len(PNG)}
        opener=Mock(return_value=response(metadata))
        with self.assertRaises(MediaError): fetch_whatsapp_media(self.store,DEMO_TENANT,SENDER,'wamid.fake','fixture','123','v25.0',opener)
        self.assertEqual(opener.call_count,1)

    def test_simulated_signed_whatsapp_image_and_audio_through_analysis(self):
        import hmac
        fixtures = [('image', '112233', 'image/png', PNG), ('audio', '112234', 'audio/ogg', b'OggS' + b'fixture')]
        messages = [{'id': 'wamid.' + kind, 'from': SENDER, 'timestamp': '1793100000',
                     'type': kind, kind: {'id': media_id}} for kind, media_id, _, _ in fixtures]
        payload = {'object': 'whatsapp_business_account', 'entry': [{'changes': [{'field': 'messages',
            'value': {'metadata': {'phone_number_id': '123'}, 'contacts': [], 'messages': messages}}]}]}
        raw = json.dumps(payload).encode()
        signature = 'sha256=' + hmac.new(b'fixture-secret', raw, hashlib.sha256).hexdigest()
        self.assertTrue(verify_signature(raw, signature, 'fixture-secret'))
        self.assertFalse(verify_signature(raw + b' ', signature, 'fixture-secret'))
        parsed = parse_webhook(payload, '123')
        self.assertEqual(self.store.add_messages(parsed, tenant_id=DEMO_TENANT), 2)
        self.assertEqual(self.store.add_messages(parsed, tenant_id=DEMO_TENANT), 0)
        self.assertEqual(len(pending_whatsapp_media(self.store, DEMO_TENANT, SENDER)), 2)
        for kind, media_id, mime, content in fixtures:
            metadata = {'id': media_id, 'url': 'https://lookaside.fbsbx.com/fixture', 'mime_type': mime,
                        'file_size': len(content), 'sha256': hashlib.sha256(content).hexdigest()}
            download = Mock(); download.__enter__ = Mock(return_value=download); download.__exit__ = Mock(return_value=False); download.read.return_value = content
            ident = fetch_whatsapp_media(self.store, DEMO_TENANT, SENDER, 'wamid.' + kind,
                                         'fixture-token', '123', opener=Mock(side_effect=[response(metadata), download]))
            asset = get_media(self.store, DEMO_TENANT, ident)
            model_response = response({'transcript': 'Necesito una limpieza.'}) if kind == 'audio' else response({'status':'completed','output':[{'type':'message','content':[{'type':'output_text','text':'Se observa un sofá.'}]}]})
            with patch('src.multimodal._convert_ogg', return_value=b'fixture-wav'):
                result = analyze_media(asset, 'fixture-key', opener=Mock(return_value=model_response))
            self.assertTrue(save_result(self.store, DEMO_TENANT, ident, result))
        self.assertEqual(pending_whatsapp_media(self.store, DEMO_TENANT, SENDER), [])
        selected, _, _, _ = snapshot(self.store, 'limpieza sofá', DEMO_TENANT)
        self.assertTrue(any(item['id'].startswith('media:') for item in selected))

    def test_builder_requires_clarification_and_validates_output(self):
        config={'name':'Seguimiento','template':'follow_up','days':2}
        output={'status':'ready','message':'Lista preparada.','config':config}
        opener=Mock(return_value=response({'output':[{'type':'message','content':[{'type':'output_text','text':json.dumps(output)}]}]}))
        first=propose([{'role':'user','text':'Quiero seguimiento'}],'fixture',opener=opener)
        self.assertEqual(first['status'],'clarify')
        result=propose([{'role':'user','text':'Quiero seguimiento'}, {'role':'assistant','text':'¿Cuánto tiempo?'}, {'role':'user','text':'Dos días'}],'fixture',opener=opener)
        self.assertEqual(result['config'],config)
        output['config']['template']='execute_code'
        opener.return_value=response({'output':[{'type':'message','content':[{'type':'output_text','text':json.dumps(output)}]}]})
        with self.assertRaises(ValueError): propose([{'role':'user','text':'a'},{'role':'assistant','text':'b'},{'role':'user','text':'c'}],'fixture',opener=opener)

    def test_preview_does_not_invent_quote_dates_and_views_are_scoped(self):
        self.store.save_conversation_workflow(SENDER, {'stage':'quoted','service':'sofá'}, DEMO_TENANT)
        config={'name':'Seguimiento','template':'follow_up','days':2}
        result=preview(self.store,DEMO_TENANT,config,today=date(2026,10,29))
        self.assertEqual(result['rows'],[]); self.assertEqual(result['missing'][0]['field'],'quote_date')
        self.store.save_conversation_workflow(SENDER, {'stage':'quoted','service':'sofá','quote_date':'2026-10-26'}, DEMO_TENANT)
        result=preview(self.store,DEMO_TENANT,config,today=date(2026,10,29))
        self.assertEqual(result['rows'][0]['days_elapsed'],3)
        ident=activate(self.store,DEMO_TENANT,config)
        self.assertEqual(get_view(self.store,DEMO_TENANT,ident),config)
        self.assertIsNone(get_view(self.store,'other',ident)); self.assertEqual(list_views(self.store,'other'),[])

    def test_csv_import_requires_preview_and_validates_all_rows(self):
        self.store.save_conversation_workflow(SENDER, {'stage':'quoted','service':'sofá'}, DEMO_TENANT)
        data='sender,quote_date\n573000000101,2026-10-26\n'
        quote_date_import(self.store, DEMO_TENANT, data, False)
        self.assertFalse(self.store.conversation_workflow(SENDER,DEMO_TENANT).get('quote_date'))
        with self.assertRaises(ValueError): quote_date_import(self.store,DEMO_TENANT,data+'999,2026-10-27\n',True)
        self.assertFalse(self.store.conversation_workflow(SENDER,DEMO_TENANT).get('quote_date'))
        quote_date_import(self.store, DEMO_TENANT, data, True)
        self.assertEqual(self.store.conversation_workflow(SENDER,DEMO_TENANT)['service'],'sofá')
        self.assertEqual(self.store.conversation_workflow(SENDER,DEMO_TENANT)['quote_date'],'2026-10-26')

    def test_scoped_profiles_finance_and_summary_do_not_mix_businesses(self):
        self.store.save_business_profile({'nombre':'Otra empresa','zonas':'Norte','tarifas':'Desde 100','politicas':'Confirmar horario'}, 'other')
        self.assertNotEqual(self.store.business_profile(DEMO_TENANT)['nombre'],'Otra empresa')
        self.assertEqual(self.store.business_profile('other')['nombre'],'Otra empresa')
        self.assertEqual(self.store.business_profile('other')['zonas'],'Norte')
        self.store.import_financial_csv('fecha,tipo,monto,categoria\n2026-10-01,venta,700,servicio\n','other')
        self.assertEqual(self.store.financial_summary('other')['sales'],700)
        self.assertNotEqual(self.store.financial_summary(DEMO_TENANT)['sales'],700)
        self.assertEqual(self.store.owner_summary(7,'other')['conversations'],0)

    def test_responsible_and_workflow_changes_are_scoped(self):
        self.store.save_conversation_workflow(SENDER, {'stage':'quoted','responsible':'Asesor ficticio'}, DEMO_TENANT, 'fixture-user')
        events=self.store.workflow_history(SENDER,DEMO_TENANT)
        self.assertTrue(any(event['field']=='responsible' and event['value']=='Asesor ficticio' for event in events))
        self.assertEqual(self.store.workflow_history(SENDER,'other'),[])


class StudioHTTPTests(unittest.TestCase):
    setUp=test_live_http.LiveHandlerTests.setUp
    tearDown=test_live_http.LiveHandlerTests.tearDown
    handler=test_live_http.LiveHandlerTests.handler

    def test_media_analysis_and_builder_require_explicit_consent(self):
        for path, fn in [('/api/media/analyze','analyze_media'),('/api/media/fetch','fetch_whatsapp_media'),('/api/custom-views/propose','propose')]:
            request=self.handler(path,b'{}',{'Content-Type':'application/json'})
            with patch('src.live_app.'+fn) as external:
                request.do_POST(); self.assertEqual(request.respond.call_args.args[0],400); external.assert_not_called()

    def test_assistant_provider_selection_requires_matching_consent(self):
        headers={'Content-Type':'application/json'}
        bad=self.handler('/api/assistant/ask', b'{"provider":"nebius","consent_to_send_to_meta":true,"question":"test"}', headers)
        with patch('src.live_app.ask') as ask:
            bad.do_POST(); self.assertEqual(bad.respond.call_args.args[0],400); ask.assert_not_called()
        good=self.handler('/api/assistant/ask', b'{"provider":"meta","consent_to_send_to_meta":true,"question":"test","language":"en"}', headers)
        with patch('src.live_app.ask',return_value={'respuesta':'ok'}) as ask:
            good.do_POST(); self.assertEqual(good.respond.call_args.args[0],200)
            self.assertEqual(ask.call_args.args[3],'meta'); self.assertEqual(ask.call_args.kwargs['language'],'en')

    def test_demo_cookie_is_isolated_from_normal_local_panel(self):
        self.server.server_close()
        from src.live_app import create_server
        self.server=create_server(port=0,db_path=Path(self.directory.name)/'test.sqlite3',
                                  environ={'PENDIVA_DEMO_MODE':'1','PENDIVA_AUTH_PASSWORD':'fixture-pass'})
        request=self.handler('/api/auth/login',b'{"password":"fixture-pass"}',{'Content-Type':'application/json'})
        request.do_POST()
        cookie=next(call.args[1] for call in request.send_header.call_args_list if call.args[0]=='Set-Cookie')
        self.assertTrue(cookie.startswith('pendiva_demo_'+str(self.server.server_port)+'='))
        self.assertIn('Path=/',cookie)
