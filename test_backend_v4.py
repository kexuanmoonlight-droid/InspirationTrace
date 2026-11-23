"""Offline contract tests (mock provider; does not verify real AI or web search)."""
import unittest, unittest.mock, importlib.util, pathlib, json
p=pathlib.Path(__file__).with_name('server.py');spec=importlib.util.spec_from_file_location('server',p);server=importlib.util.module_from_spec(spec);spec.loader.exec_module(server)

class Tests(unittest.TestCase):
    def test_multiturn_revision(self):
        captured=[]
        def fake(endpoint,body):
            captured.append((endpoint,body))
            output={'message':'已把新的创意融入故事。','update_outline':True,'outline':{'title':'新版','sections':[{'heading':'开端','text':'先前设定仍然存在，新想法推动了冲突。'}]},'change_summary':'新元素改变冲突'}
            return {'choices':[{'message':{'content':json.dumps(output,ensure_ascii=False)}}]}
        with unittest.mock.patch.object(server,'provider',fake):
            x=server.chat({'message':'把新元素融入故事','currentOutline':{'title':'上一版','sections':[{'heading':'开端','text':'老故事'}]},'history':[{'role':'user','text':'最初的想法'},{'role':'assistant','text':'旧大纲'}],'selectedReferences':[{'title':'参考作品','url':'https://example.org'}]})
        self.assertTrue(x['updated']);self.assertEqual(x['outline']['sections'][0]['heading'],'开端')
        c=json.loads(captured[0][1]['messages'][1]['content']);self.assertEqual(c['current_outline']['title'],'上一版');self.assertEqual(c['new_message'],'把新元素融入故事');self.assertEqual(c['author_selected_reference_records'][0]['title'],'参考作品')
    def test_free_chat_does_not_force_outline(self):
        with unittest.mock.patch.object(server,'provider',lambda a,b:{'choices':[{'message':{'content':json.dumps({'message':'我们可以先讨论动机。','update_outline':False,'outline':None})}}]}):
            out=server.chat({'message':'我们先聊聊人物动机'});self.assertFalse(out['updated']);self.assertIsNone(out['outline'])
    def test_search_only_cited_urls(self):
        source={'title':'Test Work','url':'https://publisher.example.org/work','start_index':50,'end_index':61}
        def fake(endpoint,body):
            return {'output':[{'type':'message','content':[{'type':'output_text','text':'SECTION 1: shares a broad motif, differs in character motivation.','annotations':[{'type':'url_citation',**source},{'type':'url_citation','title':'Unsafe','url':'javascript:alert(1)'}]}]}]}
        with unittest.mock.patch.object(server,'provider',fake):
            r=server.candidate_sources({'outline':{'title':'Example','sections':[{'heading':'One','text':'A story'}]}})
        self.assertEqual(len(r['records']),1);self.assertEqual(r['records'][0]['sectionIndex'],0);self.assertTrue(r['records'][0]['url'].startswith('https://'))
    def test_no_sources_if_no_citations(self):
        with unittest.mock.patch.object(server,'provider',lambda a,b:{'output':[{'type':'message','content':[{'type':'output_text','text':'Could not locate a reliable source.','annotations':[]}]}]}):
            r=server.candidate_sources({'outline':{'title':'X','sections':[{'heading':'H','text':'T'}]}})
        self.assertEqual(r['records'],[])
    def test_bad_outline_rejected(self):
        with self.assertRaises(ValueError):server.valid_outline({'title':'bad','sections':[]})

if __name__=='__main__':unittest.main()
