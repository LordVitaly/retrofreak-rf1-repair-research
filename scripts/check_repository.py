#!/usr/bin/env python3
"""Audit the public archive without executing archival code or accessing devices."""
from __future__ import annotations

import argparse
import ast
from collections import Counter
from pathlib import Path
import re
import urllib.parse

from repo_support import load_json, publication_files, sha256, canonical_path
from verify_manifest import verify
from photo_support import validate_photo

BAD_ENDINGS = ('.img', '.raw', '.dump', '.dmp', '.bin', '.apk', '.so', '.exe', '.dll',
               '.sys', '.pem', '.key', '.zip', '.7z', '.pyc')
SECRET = re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY|\bgh[pousr]_[A-Za-z0-9]{20,}')
HOSTPATH = re.compile(r'(?i)[A-Z]:[\\/](?:Users|Documents|Downloads)[\\/]|' + '/' + r'Users/[^/\s]+/')
CITATION = re.compile(r'\ue200|\ue201|' + 'sandbox' + r':/|' + 'utm_source' + r'=chatgpt|\bturn\d+(?:file|view|search)\d+\b')
NON_ENGLISH_SCRIPT = re.compile(r'[\u0400-\u052f\u3040-\u30ff\u3400-\u9fff]')
LINK = re.compile(r'\[[^\]\n]*\]\(([^\s)]+)(?:\s+"[^"\n]*")?\)')


def private_device_arrays(value, path: str = '') -> list[str]:
    """Find complete numeric device maps/lists, not selected owners or statuses."""
    found = []
    if isinstance(value, dict):
        for key, child in value.items():
            current = path + '/' + key
            if isinstance(child, list) and child and all(type(x) is int for x in child):
                name = key.lower()
                full_map = ('map' in name or 'logical_to_physical' in name) and len(child) > 64
                full_list = name in {'baseline_protected_blocks', 'bad_block_list',
                                     'physical_bad_blocks', 'complete_bad_blocks'}
                if full_map or full_list:
                    found.append(current)
            found.extend(private_device_arrays(child, current))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            if isinstance(child, (dict, list)):
                found.extend(private_device_arrays(child, path + '/' + str(index)))
    return found


def without_fences(text: str) -> str:
    return re.sub(r'^```[^\n]*\n.*?^```\s*$', '', text, flags=re.S | re.M)


def anchors(text: str) -> set[str]:
    result = set(re.findall(r'<a\s+(?:id|name)=["\']([^"\']+)', text))
    counts = Counter()
    for title in re.findall(r'^#{1,6}\s+(.+?)\s*#*\s*$', without_fences(text), re.M):
        title = re.sub(r'\[([^]]+)\]\([^)]+\)', r'\1', title)
        value = re.sub(r'[^\w\- ]', '', title.lower()).replace(' ', '-')
        occurrence = counts[value]
        counts[value] += 1
        result.add(value if occurrence == 0 else f'{value}-{occurrence}')
    return result


def audit(root: Path) -> tuple[list[str], dict]:
    root = root.resolve()
    files = publication_files(root)
    names = [p.relative_to(root).as_posix() for p in files]
    errors = []
    counts = {'files': len(files), 'json_files': 0, 'python_files': 0,
              'markdown_files': 0, 'relative_links_checked': 0,
              'archival_snapshots': 0, 'reviewed_photos': 0}
    photo_entries = load_json(root / 'docs/assets/board/PHOTOS.json')['files']
    photos = {canonical_path(entry['path']): entry for entry in photo_entries}
    if len(photos) != len(photo_entries):
        errors.append('Duplicate photo catalog entries')
    for rel in photos:
        if not rel.startswith('docs/assets/board/') or not rel.endswith('.jpg') or rel not in names:
            errors.append('Invalid/missing reviewed photo: ' + rel)
    if len({n.casefold() for n in names}) != len(names):
        errors.append('Case-insensitive path collision')
    for path, rel in zip(files, names):
        if rel.lower().endswith(BAD_ENDINGS):
            errors.append('Excluded binary/private artifact extension: ' + rel)
        if rel in photos:
            entry = photos[rel]
            if path.stat().st_size != entry['bytes'] or sha256(path) != entry['sha256']:
                errors.append('Reviewed photo changed: ' + rel)
            try:
                validate_photo(path.read_bytes())
            except ValueError as exc:
                errors.append(f'Invalid/private photo metadata: {rel}: {exc}')
            counts['reviewed_photos'] += 1
            continue
        try:
            text = path.read_text('utf-8')
        except UnicodeDecodeError:
            errors.append('Non-UTF-8/binary file: ' + rel)
            continue
        if '\x00' in text:
            errors.append('NUL/binary content: ' + rel)
        for label, pattern in [('non-English script', NON_ENGLISH_SCRIPT),
                               ('chat artifact', CITATION), ('private-key/token pattern', SECRET),
                               ('absolute personal host path', HOSTPATH)]:
            if pattern.search(text):
                errors.append(f'{label}: {rel}')
        if path.suffix == '.json':
            counts['json_files'] += 1
            try:
                document = load_json(path)
                for location in private_device_arrays(document):
                    errors.append(f'Complete device-specific numeric map/list: {rel} {location}')
            except (ValueError, TypeError) as exc:
                errors.append(f'Invalid JSON {rel}: {exc}')
        if rel.startswith(('toolkit/phase1_', 'toolkit/phase2_')):
            counts['archival_snapshots'] += 1
            if not rel.endswith('.txt'):
                errors.append('Historical source is not inert .txt: ' + rel)
            if 'SNAPSHOT' not in text.split('\n', 1)[0]:
                errors.append('Missing archival warning: ' + rel)
        elif path.suffix == '.py':
            counts['python_files'] += 1
            try:
                ast.parse(text, filename=rel)
            except SyntaxError as exc:
                errors.append(f'Invalid executable Python {rel}: {exc}')
        if path.suffix == '.md':
            counts['markdown_files'] += 1
            for target in LINK.findall(without_fences(text)):
                parsed = urllib.parse.urlsplit(target)
                if parsed.scheme or target.startswith('//'):
                    continue
                dest = (path.parent / urllib.parse.unquote(parsed.path)).resolve() if parsed.path else path
                if not dest.is_relative_to(root):
                    errors.append(f'Link leaves repository: {rel} -> {target}')
                    continue
                counts['relative_links_checked'] += 1
                if not dest.exists():
                    errors.append(f'Broken relative link: {rel} -> {target}')
                elif parsed.fragment and dest.is_file() and dest.suffix == '.md':
                    if urllib.parse.unquote(parsed.fragment) not in anchors(dest.read_text('utf-8')):
                        errors.append(f'Broken heading link: {rel} -> {target}')
            for digest in re.findall(r'`([A-Fa-f0-9]{60,70})`', text):
                if len(digest) != 64:
                    errors.append(f'Malformed SHA-256 length in {rel}: {len(digest)}')
    # Check real catalog paths, not redacted historical private-workspace references.
    for index in ['toolkit/INDEX.json', 'evidence/INDEX.json']:
        obj = load_json(root / index)
        entries = obj if isinstance(obj, list) else obj['files']
        catalog = [canonical_path(item['path']) for item in entries]
        prefix = index.rsplit('/', 1)[0] + '/'
        expected = {n for n in names if n.startswith(prefix) and n != index}
        if set(catalog) != expected or len(set(catalog)) != len(catalog):
            errors.append('Incomplete/duplicate file index: ' + index)
    expected_lines = names
    if (root / 'REPO_FILE_INDEX.txt').read_text('utf-8').splitlines() != expected_lines:
        errors.append('REPO_FILE_INDEX.txt is stale')
    preserved = load_json(root / 'provenance/SNAPSHOT_PRESERVATION.json')
    for entry in preserved['files']:
        rel = canonical_path(entry['path'])
        p = root / rel
        if not p.is_file() or p.stat().st_size != entry['bytes'] or sha256(p) != entry['sha256']:
            errors.append('Historical snapshot changed: ' + rel)
    counts['preserved_snapshots_checked'] = len(preserved['files'])
    return errors, counts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        errors, counts = audit(args.root)
        manifest_errors, covered = verify(args.root)
        errors.extend(manifest_errors)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print('FAIL:', exc)
        return 1
    if errors:
        for error in errors:
            print('FAIL:', error)
        return 1
    print('PASS:', ', '.join(f'{key}={value}' for key, value in counts.items()))
    print(f'PASS: {covered} checksummed files; no device/network operations performed')
    print('Scope: publication checks and syntax; archival hardware programs are not executed or certified safe.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
