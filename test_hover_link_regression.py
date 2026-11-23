"""Regression checks for the original author's mandatory evidence↔outline hover behavior."""
import unittest
from pathlib import Path
from offline_modes import mock_chat, demo_evidence

class HoverLinkRegression(unittest.TestCase):
    def setUp(self):
        self.frontend = Path(__file__).with_name('index.html').read_text(encoding='utf-8')

    def test_original_hover_contract_not_removed(self):
        for feature in ("function focusRecord(id,scroll)", "function clearRecord()", "function renderLinkedText(p,text,related)", "mark.addEventListener('mouseenter'", "mark.addEventListener('mouseleave'", "mark.addEventListener('focus'", "c.addEventListener('mouseenter'", "c.addEventListener('mouseleave'", "classList.toggle('focused'", "'marked'"):
            with self.subTest(feature=feature):
                self.assertIn(feature,self.frontend)

    def test_two_and_three_stage_anchors_resolve_to_exact_phrases(self):
        current=None
        for query,stage in [('A strong princess rescues a prince',1),('Add dragons',2),('Give the prince and dragons a deeper relationship',3)]:
            result=mock_chat({'message':query,'currentOutline':current})
            self.assertTrue(result['updated'])
            current=result['outline']
            self.assertEqual(current['demo_stage'],stage)
            records=demo_evidence({'outline':current})['records']
            self.assertEqual(len(records),2)
            for item in records:
                self.assertTrue(item['url'].startswith('https://'))
                self.assertTrue(item['highlightText'])
                self.assertIsInstance(item['sectionIndex'],int)
                self.assertIn(item['highlightText'],current['sections'][item['sectionIndex']]['text'])

    def test_v1_has_visible_hover_anchors(self):
        first=mock_chat({'message':'A princess rescues a prince'})['outline']
        cards=demo_evidence({'outline':first})['records']
        self.assertEqual({r['id'] for r in cards},{'fantasy-priory','fantasy-hobbit'})
        self.assertEqual(len([r for r in cards if r['highlightText']]),2)

    def test_saved_v51_evidence_is_migrated_without_erasing_review_state(self):
        self.assertIn('function needsDemoAnnotations()', self.frontend)
        self.assertIn('function refreshSavedDemoAnnotations()', self.frontend)
        self.assertIn('refreshSavedDemoAnnotations();', self.frontend)
        self.assertIn('selected:old?Boolean(old.selected):false', self.frontend)
        self.assertIn('reviewed:old?Boolean(old.reviewed):false', self.frontend)

    def test_memory_anchor_is_present(self):
        result=mock_chat({'message':'A story about selling memories'})
        records=demo_evidence({'outline':result['outline']})['records']
        self.assertEqual(len(records),1)
        self.assertIn(records[0]['highlightText'],result['outline']['sections'][0]['text'])

if __name__ == '__main__': unittest.main()
