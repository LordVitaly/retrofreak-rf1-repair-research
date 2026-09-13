"""Synthetic-only tests; no firmware, device access or image writes."""
import hashlib
import struct
import unittest

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "toolkit" / "offline"))
from rf1_boot_digest import UnsupportedImage, inspect_image


def synthetic_image():
    page = 16384
    kernel = b"synthetic-kernel\x00" * 17
    ramdisk = b"synthetic-ramdisk\x7f" * 19
    header = bytearray(page)
    header[:8] = b"ANDROID!"
    struct.pack_into("<10I", header, 8, len(kernel), 0x61000000,
                     len(ramdisk), 0x62000000, 0, 0, 0x63000000, page, 0, 0)
    header[48:57] = b"SYNTHETIC"
    # Independent concatenation of the documented input, not the checker itself.
    hashed = (kernel + struct.pack("<I", len(kernel)) + ramdisk
              + struct.pack("<I", len(ramdisk)) + struct.pack("<I", 0)
              + bytes(header[32:576]))
    header[576:608] = hashlib.sha1(hashed).digest() + bytes(12)
    return bytes(header) + kernel.ljust(page, b"\x00") + ramdisk.ljust(page, b"\x00")


class DigestTests(unittest.TestCase):
    def test_positive_unchanged(self):
        image = synthetic_image()
        before = hashlib.sha256(image).digest()
        self.assertTrue(inspect_image(image)["match"])
        self.assertEqual(hashlib.sha256(image).digest(), before)

    def test_changed_kernel_and_ramdisk(self):
        for offset in (16384, 32768):
            with self.subTest(offset=offset):
                image = bytearray(synthetic_image())
                image[offset] ^= 1
                self.assertFalse(inspect_image(bytes(image))["match"])

    def test_changed_hashed_header(self):
        image = bytearray(synthetic_image())
        image[64] ^= 1
        self.assertFalse(inspect_image(bytes(image))["match"])

    def test_changed_stored_id(self):
        image = bytearray(synthetic_image())
        image[576] ^= 1
        self.assertFalse(inspect_image(bytes(image))["match"])

    def test_invalid_magic(self):
        with self.assertRaises(UnsupportedImage):
            inspect_image(b"BADMAGIC" + synthetic_image()[8:])

    def test_truncated(self):
        for count in (0, 607, 16383, 32768, 49151):
            with self.subTest(count=count), self.assertRaises(UnsupportedImage):
                inspect_image(synthetic_image()[:count])

    def test_unsupported_header(self):
        for offset, value in ((36, 0), (36, 4096), (24, 1), (40, 1), (44, 1), (8, 0), (16, 0)):
            image = bytearray(synthetic_image())
            struct.pack_into("<I", image, offset, value)
            with self.subTest(offset=offset, value=value), self.assertRaises(UnsupportedImage):
                inspect_image(bytes(image))

    def test_partition_tail_is_not_hashed(self):
        report = inspect_image(synthetic_image() + b"synthetic partition tail")
        self.assertTrue(report["match"])
        self.assertEqual(report["trailing_bytes_not_hashed"], 24)


if __name__ == "__main__":
    unittest.main()
