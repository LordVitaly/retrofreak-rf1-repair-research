"""Synthetic container checks; no camera files or imaging dependencies needed."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from photo_support import sanitized_jpeg, validate_photo, segments


def segment(marker, payload):
    return bytes([255, marker]) + (len(payload)+2).to_bytes(2, 'big') + payload


class PhotoMetadataTests(unittest.TestCase):
    # Synthetic entropy contains stuffed FF and a restart marker.
    scan = segment(0xDA, b'header') + b'abc\xff\x00def\xff\xd0ghi'
    primary = b'\xff\xd8' + scan + b'\xff\xd9'

    def test_strip_metadata_and_trailer_preserve_scans(self):
        source = (b'\xff\xd8' + segment(0xE1, b'private EXIF')
                  + segment(0xFE, b'private comment') + self.scan
                  + b'\xff\xd9private trailer')
        cleaned = sanitized_jpeg(source, 8)
        validate_photo(cleaned)
        self.assertNotIn(b'private', cleaned)
        self.assertIn(self.scan, cleaned)

    def test_all_orientation_values(self):
        for orientation in range(1, 9):
            validate_photo(sanitized_jpeg(self.primary, orientation))

    def test_added_metadata_and_trailers_rejected(self):
        clean = sanitized_jpeg(self.primary, 1)
        for extra in [segment(0xE1, b'GPS'), segment(0xFE, b'comment'),
                      segment(0xE2, b'profile')]:
            with self.assertRaises(ValueError):
                validate_photo(clean[:2]+extra+clean[2:])
        with self.assertRaises(ValueError):
            validate_photo(clean+b'trailing')

    def test_truncated_or_non_jpeg_rejected(self):
        for data in [b'not a jpeg', b'\xff\xd8\xff', self.primary[:-2],
                     b'\xff\xd8\xff\xe1\x00\x40short']:
            with self.assertRaises(ValueError):
                list(segments(data))

    def test_multiple_scans_are_preserved(self):
        source = self.primary[:-2]+segment(0xC4, b'table')+self.scan+b'\xff\xd9'
        clean = sanitized_jpeg(source, 6)
        validate_photo(clean)
        self.assertEqual(clean.count(self.scan), 2)


if __name__ == '__main__':
    unittest.main()
