"""Local publication helpers. No network, device access, or source execution."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re

SELF_MANIFESTS = frozenset({'MANIFEST.json', 'MANIFEST.sha256'})
IGNORED_DIRS = frozenset({'.git', '__pycache__', '.pytest_cache', '.venv', 'venv'})
HEX256 = re.compile(r'[0-9a-f]{64}\Z')


def canonical_path(value: object) -> str:
    """Reject absolute, ambiguous, traversal, and Windows-special paths."""
    if not isinstance(value, str) or not value or any(ord(c) < 32 for c in value):
        raise ValueError('Invalid manifest path')
    if '\\' in value or ':' in value or value.startswith('/'):
        raise ValueError('Non-relative manifest path: ' + value)
    parts = value.split('/')
    if any(part in ('', '.', '..') or part.endswith((' ', '.')) for part in parts):
        raise ValueError('Noncanonical manifest path: ' + value)
    if PurePosixPath(value).is_absolute():
        raise ValueError('Absolute manifest path')
    return value


def publication_files(root: Path) -> list[Path]:
    """List regular files, without following links or traversing local caches."""
    root = root.resolve()
    result: list[Path] = []
    for current, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in IGNORED_DIRS)
        for name in dirs:
            if (Path(current) / name).is_symlink():
                raise ValueError('Symlink directory not allowed: ' + name)
        for name in sorted(files):
            path = Path(current) / name
            if path.is_symlink() or not path.is_file():
                raise ValueError('Non-regular publication entry: ' + str(path.relative_to(root)))
            canonical_path(path.relative_to(root).as_posix())
            result.append(path)
    result.sort(key=lambda p: p.relative_to(root).as_posix())
    return result


def sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open('rb') as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b''):
            value.update(chunk)
    return value.hexdigest()


def load_json(path: Path):
    """Reject duplicate keys, NaN and Infinity in publication JSON."""
    def pairs(items):
        result = {}
        for key, val in items:
            if key in result:
                raise ValueError('Duplicate JSON key: ' + key)
            result[key] = val
        return result
    def bad_constant(value):
        raise ValueError('Non-finite JSON value: ' + value)
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=pairs,
                      parse_constant=bad_constant)


def write_json(path: Path, value) -> None:
    text = json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + '\n'
    path.write_text(text, encoding='utf-8', newline='\n')
