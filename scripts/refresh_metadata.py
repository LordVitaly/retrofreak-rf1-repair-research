#!/usr/bin/env python3
"""Refresh public indexes and manifests after review; never touches device data."""
from __future__ import annotations

import argparse
from pathlib import Path

from repo_support import SELF_MANIFESTS, publication_files, sha256, write_json


def refresh(root: Path, date: str = '2026-09-12') -> int:
    root = root.resolve()
    files = publication_files(root)
    toolkit = []
    for p in files:
        rel = p.relative_to(root).as_posix()
        if not rel.startswith('toolkit/') or rel == 'toolkit/INDEX.json':
            continue
        if rel.startswith(('toolkit/phase1_', 'toolkit/phase2_')):
            kind = 'inert_historical_source_snapshot'
        elif p.suffix == '.py':
            kind = 'executable_local_file_checker'
        else:
            kind = 'documentation'
        toolkit.append({'path': rel, 'kind': kind})
    write_json(root / 'toolkit/INDEX.json', toolkit)

    evidence = []
    for p in files:
        rel = p.relative_to(root).as_posix()
        if rel.startswith('evidence/') and rel != 'evidence/INDEX.json':
            kind = ('translated_public_record' if rel.startswith('evidence/phase1/')
                    else 'curated_public_record' if p.suffix == '.json'
                    else 'supporting_text')
            evidence.append({'path': rel, 'kind': kind})
    write_json(root / 'evidence/INDEX.json', {'scope': 'Selected public evidence, not private raw acquisitions',
                                           'files': evidence})
    # Include these files themselves by name, but never recursive self-hashes.
    names = {p.relative_to(root).as_posix() for p in publication_files(root)}
    names.update(SELF_MANIFESTS)
    names.add('REPO_FILE_INDEX.txt')
    (root / 'REPO_FILE_INDEX.txt').write_text('\n'.join(sorted(names)) + '\n',
                                            encoding='utf-8', newline='\n')
    entries = [{'path': p.relative_to(root).as_posix(), 'bytes': p.stat().st_size,
                'sha256': sha256(p)} for p in publication_files(root)
               if p.relative_to(root).as_posix() not in SELF_MANIFESTS]
    write_json(root / 'MANIFEST.json', {'schema_version': 2, 'generated': date,
                                       'language': 'English',
                                       'excluded_self_manifests': sorted(SELF_MANIFESTS),
                                       'files': entries})
    (root / 'MANIFEST.sha256').write_text(
        ''.join(f"{e['sha256']}  {e['path']}\n" for e in entries),
        encoding='utf-8', newline='\n')
    return len(entries)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--date', default='2026-09-12', help='ISO date for this publication build')
    args = parser.parse_args()
    from datetime import date
    date.fromisoformat(args.date)
    print(f'Updated metadata for {refresh(args.root, args.date)} files. Run validation and tests next.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
