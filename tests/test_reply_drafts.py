"""Local drafts never make external calls and remain scoped to their conversation."""
from pathlib import Path
import tempfile
import unittest
import json
from unittest.mock import MagicMock, Mock

from src.demo_seed import seed_demo
from src.live_pipeline import LiveStore
from src.reply_drafts import init_reply_drafts, list_drafts, save_draft, suggested_reply, update_draft, generate_reply
from src.live_pipeline import AnalysisError
from contextlib import closing


class ReplyDraftTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1])
        self.store = LiveStore(Path(self.temp.name) / 'drafts.sqlite3')
        self.store.initialize()
        self.tenant = seed_demo(self.store)['tenant_id']
        init_reply_drafts(self.store)

    def tearDown(self):
        self.temp.cleanup()

    def test_save_is_scoped_and_requires_message_in_conversation(self):
        data = {'source_message_id':'demo-ana-message-1','text':' Hola, ¿qué servicio necesitas? '}
        ident = save_draft(self.store,self.tenant,'573000000101','fixture-user',data)
        self.assertEqual(list_drafts(self.store,self.tenant,'573000000101')[0]['id'],ident)
        self.assertEqual(list_drafts(self.store,self.tenant,'573000000101')[0]['state'],'draft')
        self.assertTrue(update_draft(self.store,self.tenant,'573000000101','fixture-user',ident,{'text':'Versión corregida'}))
        self.assertEqual(list_drafts(self.store,self.tenant,'573000000101')[0]['text'],'Versión corregida')
        self.assertFalse(update_draft(self.store,'other','573000000101','other-user',ident,{'text':'Intrusión'}))
        with closing(self.store.connect()) as db:
            actions=[row['action'] for row in db.execute("SELECT action FROM audit_events WHERE entity_id=? ORDER BY rowid",(ident,))]
        self.assertEqual(actions,['reply_draft_created','reply_draft_updated'])
        self.assertEqual(list_drafts(self.store,'other','573000000101'),[])
        self.assertEqual(list_drafts(self.store,self.tenant,'573000000102'),[])
        with self.assertRaises(ValueError):
            save_draft(self.store,self.tenant,'573000000102','fixture-user',data)
        with self.assertRaises(ValueError):
            save_draft(self.store,self.tenant,'573000000101','fixture-user',{**data,'text':' '})

    def test_starter_is_bilingual_and_makes_no_promise(self):
        self.assertIn('ubicación',suggested_reply('es'))
        self.assertIn('location',suggested_reply('en'))
        with self.assertRaises(ValueError):
            suggested_reply('xx')

    def test_muse_reply_uses_alias_and_validates_sources(self):
        result={'reply':'¿Qué fecha prefieres?','evidence_ids':['mensaje_1']}
        response=MagicMock();response.__enter__.return_value.read.return_value=json.dumps({'status':'completed','output':[
            {'type':'message','content':[{'type':'output_text','text':json.dumps(result)}]}]}).encode()
        opener=Mock(return_value=response)
        messages=[{'id':'private-id','text':'Necesito limpiar un sofá.','timestamp':1,'kind':'text'},
                  {'id':'media','text':'Imagen recibida','timestamp':2,'kind':'image'}]
        generated=generate_reply(messages,{'servicios':'Sofá'},'fixture',opener=opener)
        request=json.loads(opener.call_args.args[0].data)
        self.assertNotIn('private-id',request['input'])
        self.assertNotIn('Imagen recibida',request['input'])
        self.assertEqual(generated['sources'][0]['id'],'private-id')
        result['evidence_ids']=['inventado']
        response.__enter__.return_value.read.return_value=json.dumps({'status':'completed','output':[
            {'type':'message','content':[{'type':'output_text','text':json.dumps(result)}]}]}).encode()
        with self.assertRaises(AnalysisError):
            generate_reply(messages,{},'fixture',opener=Mock(return_value=response))
