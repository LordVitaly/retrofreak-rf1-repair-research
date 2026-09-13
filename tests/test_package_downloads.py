"""Package acquisition tests use mock responses; no live network requests."""
import contextlib
import hashlib
import io
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from download_cygwin_packages import download_packages, package_specs

DATA = b'synthetic package archive for unit tests'
URL = 'https://example.invalid/packages/synthetic-1.tar.xz'


def manifest(data=DATA):
    return {'packages': [{'url': URL, 'bytes': len(data),
                          'sha512': hashlib.sha512(data).hexdigest()}]}


class Response(io.BytesIO):
    def geturl(self):
        return URL


class DownloadTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.destination = Path(self.tmp.name)

    def download(self, spec, response):
        with patch('urllib.request.urlopen', return_value=response), contextlib.redirect_stdout(io.StringIO()):
            download_packages(spec, self.destination)

    def test_valid_spec(self):
        self.assertEqual(package_specs(manifest())[0]['name'], 'synthetic-1.tar.xz')

    def test_https_only(self):
        for bad in ('http://example.invalid/a.tar.xz', 'https://a:b@example.invalid/a.tar.xz',
                    'https://example.invalid/a.tar.xz?token=x', 'file:///a.tar.xz'):
            spec = manifest();spec['packages'][0]['url'] = bad
            with self.subTest(url=bad), self.assertRaises(ValueError):
                package_specs(spec)

    def test_invalid_or_duplicate_package(self):
        for spec in ({}, {'packages': []}, {'packages': ['bad']},
                     {'packages': manifest()['packages'] * 2}):
            with self.subTest(spec=spec), self.assertRaises(ValueError):
                package_specs(spec)

    def test_invalid_hash_or_size(self):
        for key, val in (('bytes', -1), ('bytes', True), ('sha512', 'abcdef')):
            spec = manifest();spec['packages'][0][key] = val
            with self.subTest(key=key), self.assertRaises(ValueError):
                package_specs(spec)

    def test_valid_download_verifies(self):
        self.download(manifest(), Response(DATA))
        self.assertEqual((self.destination / 'synthetic-1.tar.xz').read_bytes(), DATA)

    def test_mismatch_removes_new_file(self):
        with self.assertRaises(ValueError):
            self.download(manifest(), Response(b'x' * len(DATA)))
        self.assertFalse((self.destination / 'synthetic-1.tar.xz').exists())

    def test_oversized_download_stops_and_removes_file(self):
        with self.assertRaises(ValueError):
            self.download(manifest(), Response(DATA + b'extra'))
        self.assertFalse((self.destination / 'synthetic-1.tar.xz').exists())

    def test_existing_file_not_overwritten(self):
        p = self.destination / 'synthetic-1.tar.xz';p.write_bytes(b'preserve me')
        with self.assertRaises(ValueError):
            self.download(manifest(), Response(DATA))
        self.assertEqual(p.read_bytes(), b'preserve me')

    def test_existing_verified_file_skips_network(self):
        (self.destination / 'synthetic-1.tar.xz').write_bytes(DATA)
        with patch('urllib.request.urlopen') as get, contextlib.redirect_stdout(io.StringIO()):
            download_packages(manifest(), self.destination)
            get.assert_not_called()


if __name__ == '__main__':
    unittest.main()
