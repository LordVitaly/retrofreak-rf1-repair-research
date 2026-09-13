"""Subprocess checks of local-file digest CLI exit codes using synthetic inputs."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from test_rf1_boot_digest import synthetic_image

SCRIPT = Path(__file__).resolve().parents[1] / 'toolkit/offline/rf1_boot_digest.py'


class DigestCliTests(unittest.TestCase):
    def test_help(self):
        p = subprocess.run([sys.executable, '-B', str(SCRIPT), '--help'], capture_output=True)
        self.assertEqual(p.returncode, 0)

    def test_pass_mismatch_unsupported_and_no_input_change(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'synthetic.img'
            original = synthetic_image()
            for data, code in ((original, 0),
                               (original[:16384] + b'x' + original[16385:], 1),
                               (b'not a boot image', 2)):
                p.write_bytes(data)
                result = subprocess.run([sys.executable, '-B', str(SCRIPT), str(p)], capture_output=True)
                self.assertEqual(result.returncode, code, result.stderr.decode())
                self.assertEqual(p.read_bytes(), data)

    def test_missing_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = subprocess.run([sys.executable, '-B', str(SCRIPT), str(Path(tmp) / 'missing.img')], capture_output=True)
            self.assertEqual(p.returncode, 2)


if __name__ == '__main__':
    unittest.main()
