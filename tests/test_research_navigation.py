"""Navigation regressions: wrong-case selection, stale claims and lost sources."""
from pathlib import Path
import json
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from navigation_support import pointer_value, toolkit_entries, validate_navigation
from query_research import query
from repo_support import publication_files, write_json


class NavigationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for folder in ('toolkit/phase2_fixture', 'docs', 'evidence'):
            (self.root / folder).mkdir(parents=True)
        self.source = 'toolkit/phase2_fixture/old.py.txt'
        (self.root / self.source).write_bytes(
            b'ARCHIVAL SNAPSHOT\r\nRole: historical_unexecuted_superseded_boot1028\r\n')
        write_json(self.root / 'evidence/result.json', {'all_pass': True, 'data_writes': False, 'nested': [False]})
        self.cases = {'schema_version': 1, 'path_base': 'repository_root', 'scope': 'fixture',
            'cases': [{'id': 'original', 'recovery_access': 'unavailable',
                       'related_docs': [], 'related_evidence': ['evidence/result.json']}],
            'routing': [{'recovery_access': access, 'case_ids': ['original'] if access == 'unavailable' else [],
                         'read_next': []} for access in ('working', 'unavailable', 'unknown')]}
        self.families = {'schema_version': 1, 'path_base': 'repository_root', 'scope': 'fixture',
            'families': [{'id': 'boot', 'purpose': 'Review boot experiment', 'members': [self.source],
                          'case_ids': ['original'], 'inputs': ['private input omitted'],
                          'dependencies': ['old bridge'], 'related_docs': [],
                          'related_evidence': ['evidence/result.json'], 'topics': ['boot'],
                          'interpretation': 'Historical; not executable'}]}
        self.fields = {'schema_version': 1, 'path_base': 'repository_root', 'scope': 'fixture',
            'general_rules': [], 'notes': [{'id': 'userdata', 'case_id': 'original',
                'record': 'evidence/result.json', 'expected_values': {'/data_writes': False},
                'meaning': 'Userdata flag', 'do_not_infer': 'No NAND writes', 'related_sources': [self.source]}]}
        self.save()

    def save(self):
        for path, data in [('CASES.json', self.cases), ('toolkit/SOURCE_FAMILIES.json', self.families),
                           ('docs/EVIDENCE_FIELDS.json', self.fields)]:
            write_json(self.root / path, data)
        write_json(self.root / 'toolkit/INDEX.json', toolkit_entries(self.root, publication_files(self.root)))

    def test_enrichment_keeps_old_fields_all_sources_and_original_bytes(self):
        before = (self.root / self.source).read_bytes()
        entries = toolkit_entries(self.root, publication_files(self.root))
        entry = next(e for e in entries if e['path'] == self.source)
        self.assertEqual(entry['kind'], 'inert_historical_source_snapshot')
        self.assertEqual(entry['disposition'], 'superseded_or_unexecuted')
        self.assertEqual((self.root / self.source).read_bytes(), before)
        self.assertEqual(validate_navigation(self.root)[0], [])

    def test_unknown_access_does_not_choose_original_repair(self):
        self.assertEqual(query(self.root, 'recovery', 'unknown')['case_ids'], [])
        self.cases['routing'][2]['case_ids'] = ['original']
        self.save()
        self.assertTrue(any('silently select' in e for e in validate_navigation(self.root)[0]))

    def test_source_cannot_disappear_or_belong_to_two_families(self):
        self.families['families'][0]['members'].append(self.source)
        write_json(self.root / 'toolkit/SOURCE_FAMILIES.json', self.families)
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            toolkit_entries(self.root, publication_files(self.root))
        self.families['families'][0]['members'] = [self.source]
        write_json(self.root / 'toolkit/SOURCE_FAMILIES.json', self.families)
        (self.root / 'toolkit/phase2_fixture/new.py.txt').write_text('SNAPSHOT')
        with self.assertRaisesRegex(ValueError, 'coverage'):
            toolkit_entries(self.root, publication_files(self.root))

    def test_stale_or_type_changed_field_pin_is_rejected(self):
        for pointer, expected in (('/data_writes', True), ('/data_writes', 0), ('/nested', [0])):
            self.fields['notes'][0]['expected_values'] = {pointer: expected}
            self.save()
            self.assertTrue(any('pin changed' in e for e in validate_navigation(self.root)[0]))

    def test_missing_field_pointer_and_evidence_reference_are_rejected(self):
        self.fields['notes'][0]['expected_values'] = {'/missing': False}
        self.families['families'][0]['related_evidence'] = ['evidence/missing.json']
        self.save()
        errors = validate_navigation(self.root)[0]
        self.assertTrue(any('Unresolved field-note pointer' in e for e in errors))
        self.assertTrue(any('Missing/nonlocal' in e for e in errors))

    def test_json_pointer_escaping_and_invalid_indexes(self):
        self.assertEqual(pointer_value({'a/b': {'~': [7]}}, '/a~1b/~0/0'), 7)
        for pointer in ('/x/-1', '/x/00', '/x/~2'):
            with self.subTest(pointer=pointer), self.assertRaises(ValueError):
                pointer_value({'x': [7]}, pointer)

    def test_stale_detailed_index_is_rejected(self):
        index = json.loads((self.root / 'toolkit/INDEX.json').read_text())
        next(e for e in index if e['path'] == self.source)['disposition'] = 'ready'
        write_json(self.root / 'toolkit/INDEX.json', index)
        self.assertTrue(any('index is stale' in e for e in validate_navigation(self.root)[0]))

    def test_cli_missing_case_and_traversal_fail_without_a_fallback(self):
        for args in (['--case', 'missing'], ['--case', ''], ['--source', '../outside']):
            result = subprocess.run([sys.executable, '-B', str(ROOT / 'scripts/query_research.py'),
                                     '--root', str(self.root), *args], capture_output=True)
            self.assertEqual(result.returncode, 2)
            self.assertIn('error', json.loads(result.stdout))


if __name__ == '__main__':
    unittest.main()
