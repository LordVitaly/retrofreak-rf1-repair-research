"""Lossless JPEG metadata filtering for reviewed documentation photographs.

This parses the container, not the compressed image. Publication preparation
also decodes and visually reviews each photo outside this standard-library check.
"""
from __future__ import annotations


def orientation_exif(orientation: int) -> bytes:
    if orientation not in range(1, 9):
        raise ValueError('Invalid EXIF orientation')
    return (b'Exif\x00\x00II\x2a\x00\x08\x00\x00\x00\x01\x00'
            b'\x12\x01\x03\x00\x01\x00\x00\x00' + bytes([orientation, 0])
            + b'\x00\x00\x00\x00\x00\x00')


def segments(data: bytes, *, allow_trailing: bool = False):
    """Yield (marker, raw bytes, payload), including entropy spans as marker 0."""
    if not data.startswith(b'\xff\xd8'):
        raise ValueError('Missing JPEG SOI')
    yield 0xD8, data[:2], b''
    pos = 2
    while pos < len(data):
        start = pos
        if data[pos] != 255:
            raise ValueError('Expected JPEG marker')
        while pos < len(data) and data[pos] == 255:
            pos += 1
        if pos == len(data):
            raise ValueError('Truncated marker')
        marker = data[pos]
        pos += 1
        if marker == 0xD9:
            yield marker, data[start:pos], b''
            if pos != len(data) and not allow_trailing:
                raise ValueError('Trailing JPEG data')
            return
        if marker in (0, 0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
            raise ValueError('Unexpected standalone marker')
        length = int.from_bytes(data[pos:pos+2], 'big')
        if length < 2 or pos + length > len(data):
            raise ValueError('Invalid JPEG segment length')
        end = pos + length
        yield marker, data[start:end], data[pos+2:end]
        pos = end
        if marker == 0xDA:
            scan_start = pos
            while True:
                found = data.find(b'\xff', pos)
                if found < 0:
                    raise ValueError('Unterminated JPEG scan')
                cursor = found + 1
                while cursor < len(data) and data[cursor] == 255:
                    cursor += 1
                if cursor == len(data):
                    raise ValueError('Truncated scan marker')
                if data[cursor] == 0 or 0xD0 <= data[cursor] <= 0xD7:
                    pos = cursor + 1
                    continue
                yield 0, data[scan_start:found], b''
                pos = found
                break
    raise ValueError('Missing JPEG EOI')


def sanitized_jpeg(data: bytes, orientation: int) -> bytes:
    """Remove APP/COM metadata; keep only a newly constructed orientation tag."""
    parts = list(segments(data, allow_trailing=True))
    exif = orientation_exif(orientation)
    header = b'\xff\xd8\xff\xe1' + (len(exif)+2).to_bytes(2, 'big') + exif
    return header + b''.join(raw for marker, raw, _ in parts[1:]
                             if not (0xE0 <= marker <= 0xEF or marker == 0xFE))


def validate_photo(data: bytes) -> None:
    parts = list(segments(data))
    metadata = [(marker, payload) for marker, _, payload in parts
                if 0xE0 <= marker <= 0xEF or marker == 0xFE]
    if len(metadata) != 1 or metadata[0][0] != 0xE1:
        raise ValueError('Photo must contain only orientation metadata')
    if metadata[0][1] not in [orientation_exif(i) for i in range(1, 9)]:
        raise ValueError('Unexpected EXIF data')
    if not any(marker == 0xDA for marker, _, _ in parts):
        raise ValueError('Photo has no image scan')
