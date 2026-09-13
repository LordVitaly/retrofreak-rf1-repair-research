"""Synthetic publication fixtures only; never examine or modify device storage."""
from pathlib import Path
import json
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from repo_support import canonical_path, load_json, publication_files
from refresh_metadata import refresh
from verify_manifest import verify


class IntegrityTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for folder in ('toolkit', 'evidence', 'scripts'):
            (self.root / folder).mkdir()
        (self.root / 'README.md').write_text('# Synthetic fixture\n', encoding='utf-8')
        refresh(self.root)

    def test_valid_fixture(self):
        errors, count = verify(self.root)
        self.assertEqual(errors, [])
        self.assertGreater(count, 0)

    def test_changed_content(self):
        (self.root / 'README.md').write_text('# Changed fixture\n')
        errors, _ = verify(self.root)
        self.assertTrue(any('SHA-256 mismatch' in e for e in errors))

    def test_missing_file(self):
        (self.root / 'README.md').unlink()
        self.assertIn('Missing: README.md', verify(self.root)[0])

    def test_unlisted_file_is_not_ignored(self):
        (self.root / 'unexpected.txt').write_text('Do not publish silently')
        self.assertIn('Unlisted: unexpected.txt', verify(self.root)[0])

    def test_two_manifests_must_agree(self):
        p = self.root / 'MANIFEST.sha256'
        p.write_text('0' * 64 + '  README.md\n')
        self.assertIn('MANIFEST.sha256 and MANIFEST.json disagree', verify(self.root)[0])

    def test_traversal_and_windows_paths(self):
        for name in ('../secret', '/tmp/file', 'C:/file', 'dir\\file', './file', 'a//b', 'a/../b'):
            with self.subTest(name=name), self.assertRaises(ValueError):
                canonical_path(name)

    def test_duplicate_manifest_entry_rejected(self):
        p = self.root / 'MANIFEST.json'
        doc = json.loads(p.read_text())
        doc['files'].append(doc['files'][0])
        p.write_text(json.dumps(doc))
        with self.assertRaises(ValueError):
            verify(self.root)

    def test_duplicate_json_keys_rejected(self):
        p = self.root / 'test.json'
        p.write_text('{"same": 1, "same": 2}')
        with self.assertRaises(ValueError):
            load_json(p)

    def test_non_finite_json_rejected(self):
        p = self.root / 'test.json'
        p.write_text('{"value": NaN}')
        with self.assertRaises(ValueError):
            load_json(p)

    def test_symlink_is_rejected(self):
        target = self.root / 'alias'
        try:
            target.symlink_to(self.root / 'README.md')
        except OSError:
            self.skipTest('Symlink creation unavailable')
        with self.assertRaises(ValueError):
            publication_files(self.root)

    def test_git_and_python_cache_are_ignored(self):
        for name in ('.git', '__pycache__'):
            folder = self.root / name
            folder.mkdir()
            (folder / 'local-only').write_text('ignored')
        self.assertEqual(verify(self.root)[0], [])

    def test_refresh_is_deterministic(self):
        first = (self.root / 'MANIFEST.json').read_bytes()
        refresh(self.root)
        self.assertEqual(first, (self.root / 'MANIFEST.json').read_bytes())


if __name__ == '__main__':
    unittest.main()
