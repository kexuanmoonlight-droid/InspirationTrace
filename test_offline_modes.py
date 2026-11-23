import json, unittest, unittest.mock
import server
from offline_modes import mock_chat, demo_evidence, ollama_available

class OfflineModesTests(unittest.TestCase):
    def test_initial_memory_demo_and_link(self):
        r=mock_chat({'message':'我想写记忆交易的城市'})
        self.assertTrue(r['updated']);self.assertTrue(r['demo'])
        e=demo_evidence({'outline':r['outline']})
        self.assertEqual(len(e['records']),1)
        self.assertTrue(e['records'][0]['url'].startswith('https://www.penguin.co.uk/'))
    def test_scripted_multiturn_dragon_changes_plot(self):
        first=mock_chat({'message':'强壮的公主救王子'})
        second=mock_chat({'message':'加入龙元素','currentOutline':first['outline']})
        self.assertTrue(second['updated'])
        self.assertIn('龙', ' '.join(x['text'] for x in second['outline']['sections']))
        self.assertNotEqual(first['outline']['title'],second['outline']['title'])
        self.assertEqual(second['outline']['demo_stage'],2)
    def test_three_round_fantasy_revision_and_verified_links(self):
        first=mock_chat({'message':'强壮的公主救王子'})
        second=mock_chat({'message':'加入龙元素','currentOutline':first['outline']})
        third=mock_chat({'message':'我想让龙和王子产生多一些的关系','currentOutline':second['outline']})
        self.assertTrue(third['updated'])
        self.assertEqual(third['outline']['demo_stage'],3)
        body=' '.join(x['text'] for x in third['outline']['sections'])
        self.assertIn('王子',body)
        self.assertIn('龙族',body)
        self.assertNotEqual(second['outline']['sections'][1]['text'], third['outline']['sections'][1]['text'])
        evidence=demo_evidence({'outline':third['outline']})
        self.assertEqual(len(evidence['records']),2)
        for record in evidence['records']:
            self.assertTrue(record['url'].startswith('https://'))
            self.assertIn('人工', record['comparison'] if '人工' in record['comparison'] else evidence['notice'])
            self.assertIsInstance(record['sectionIndex'],int)
    def test_fantasy_stage_one_has_broad_but_explicitly_limited_links(self):
        first=mock_chat({'message':'强壮的公主救王子'})
        evidence=demo_evidence({'outline':first['outline']})
        self.assertEqual(len(evidence['records']),2)
        self.assertTrue(all(isinstance(r['sectionIndex'],int) and r['highlightText'] for r in evidence['records']))
        self.assertIn('V1', evidence['records'][0]['comparison'])
    def test_any_unknown_request_not_misrepresented(self):
        r=mock_chat({'message':'请写一个关于量子花店的故事'})
        self.assertFalse(r['updated']);self.assertIn('无法智能创作',r['message'])
    def test_unrecognized_followup_does_not_fake_semantic_understanding(self):
        start=mock_chat({'message':'公主救王子'})
        r=mock_chat({'message':'把地面换成积木','currentOutline':start['outline']})
        self.assertFalse(r['updated'])
        self.assertIn('没有匹配',r['message'])
    def test_generic_local_story_has_no_fake_references(self):
        out={'title':'试验','sections':[{'heading':'a','text':'b'}]}
        r=demo_evidence({'outline':out})
        self.assertEqual(r['records'],[])
    def test_no_ollama_available_no_cloud_fallback(self):
        with unittest.mock.patch('offline_modes.ollama_available',return_value=[]):
            with self.assertRaises(RuntimeError):server.ollama_chat({'message':'test'},server.SYSTEM,server.valid_outline)
    def test_mock_endpoint_without_api_key(self):
        with unittest.mock.patch.dict('os.environ',{'OPENAI_API_KEY':''}):
            result=mock_chat({'message':'一位小镇邮递员收到来自十年后的信'})
            self.assertTrue(result['updated'])

if __name__=='__main__':unittest.main()
