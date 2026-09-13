"""Read-only local RF-1 boot digest checker; newly extracted for publication."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import struct


class UnsupportedImage(ValueError):
    """Invalid image or format outside the scope verified in this repair."""


def inspect_image(image: bytes) -> dict:
    """Compute the observed vendor ID without modifying the supplied bytes."""
    if len(image) < 608:
        raise UnsupportedImage("Truncated Android header: at least 608 bytes required")
    if image[:8] != b"ANDROID!":
        raise UnsupportedImage("Invalid ANDROID! magic")
    fields = struct.unpack_from("<10I", image, 8)
    kernel_size, _, ramdisk_size, _, second_size, _, _, page, dt_size, unused = fields
    if page != 16384:
        raise UnsupportedImage("Only the observed 16384-byte page format is supported")
    if second_size != 0:
        raise UnsupportedImage("second_size must be zero: other cases were not verified")
    if dt_size != 0 or unused != 0:
        raise UnsupportedImage("Only the observed legacy header with dt_size=unused=0 is supported")
    if not kernel_size or not ramdisk_size:
        raise UnsupportedImage("Both kernel and ramdisk must be present")
    align = lambda count: ((count + page - 1) // page) * page
    ramdisk_offset = page + align(kernel_size)
    image_end = ramdisk_offset + align(ramdisk_size)
    if len(image) < image_end:
        raise UnsupportedImage("Truncated image or missing final page padding")

    digest = hashlib.sha1()
    for part in (
        image[page:page + kernel_size], image[8:12],
        image[ramdisk_offset:ramdisk_offset + ramdisk_size], image[16:20],
        image[24:28],  # Empty second payload followed by second_size LE32.
        image[32:576],
    ):
        digest.update(part)
    computed = digest.digest() + bytes(12)
    stored = image[576:608]
    return {
        "format_scope": "RF-1 observed legacy ANDROID!, page=16384, second_size=0",
        "kernel_size": kernel_size,
        "ramdisk_size": ramdisk_size,
        "ramdisk_offset": ramdisk_offset,
        "padded_image_bytes": image_end,
        "trailing_bytes_not_hashed": len(image) - image_end,
        "stored_id": stored.hex(),
        "computed_id": computed.hex(),
        "match": stored == computed,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", type=Path, help="Path to a local boot image; opened read-only")
    args = parser.parse_args(argv)
    try:
        result = inspect_image(args.image.read_bytes())
    except UnsupportedImage as exc:
        print(json.dumps({"error": str(exc)}))
        return 2
    except OSError as exc:
        print(json.dumps({"error": "Cannot read local file", "type": type(exc).__name__}))
        return 2
    print(json.dumps(result, indent=2))
    return 0 if result["match"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
