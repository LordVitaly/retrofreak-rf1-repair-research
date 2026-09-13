#!/usr/bin/env python3
"""Verify every published file against both manifests; read-only, local only."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

from repo_support import (HEX256, SELF_MANIFESTS, canonical_path, load_json,
                          publication_files, sha256)


def verify(root: Path) -> tuple[list[str], int]:
    root = root.resolve()
    errors: list[str] = []
    manifest = load_json(root / 'MANIFEST.json')
    rows = manifest.get('files')
    if not isinstance(rows, list):
        raise ValueError('MANIFEST.json must contain a files array')
    expected = {}
    folded = set()
    for item in rows:
        if not isinstance(item, dict):
            raise ValueError('Manifest entry must be an object')
        name = canonical_path(item.get('path'))
        if name in SELF_MANIFESTS:
            raise ValueError('Manifests must not hash themselves')
        if name in expected or name.casefold() in folded:
            raise ValueError('Duplicate/case-colliding manifest path: ' + name)
        digest, size = item.get('sha256'), item.get('bytes')
        if not isinstance(digest, str) or not HEX256.fullmatch(digest):
            raise ValueError('Invalid SHA-256: ' + name)
        if type(size) is not int or size < 0:
            raise ValueError('Invalid byte count: ' + name)
        expected[name] = item
        folded.add(name.casefold())

    actual = {p.relative_to(root).as_posix(): p for p in publication_files(root)
              if p.relative_to(root).as_posix() not in SELF_MANIFESTS}
    errors += ['Missing: ' + n for n in sorted(expected.keys() - actual.keys())]
    errors += ['Unlisted: ' + n for n in sorted(actual.keys() - expected.keys())]
    for name in sorted(actual.keys() & expected.keys()):
        p, item = actual[name], expected[name]
        if p.stat().st_size != item['bytes']:
            errors.append('Size mismatch: ' + name)
        if sha256(p) != item['sha256']:
            errors.append('SHA-256 mismatch: ' + name)

    checksum_rows = {}
    for line in (root / 'MANIFEST.sha256').read_text('utf-8').splitlines():
        if len(line) < 67 or line[64:66] != '  ' or not HEX256.fullmatch(line[:64]):
            raise ValueError('Malformed MANIFEST.sha256 line')
        name = canonical_path(line[66:])
        if name in checksum_rows:
            raise ValueError('Duplicate checksum line: ' + name)
        checksum_rows[name] = line[:64]
    if checksum_rows != {n: x['sha256'] for n, x in expected.items()}:
        errors.append('MANIFEST.sha256 and MANIFEST.json disagree')
    return errors, len(expected)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args(argv)
    try:
        errors, count = verify(args.root)
    except (OSError, ValueError, TypeError) as exc:
        print('FAIL:', exc)
        return 1
    if errors:
        for error in errors:
            print('FAIL:', error)
        return 1
    print(f'PASS: {count} files match both manifests; no unlisted publication files')
    return 0


if __name__ == '__main__':
    sys.exit(main())
