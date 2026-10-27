"""Query local repair metadata as JSON. No network, hardware or archive execution."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from navigation_support import CATALOGS, local_file
from repo_support import canonical_path, load_json


def query(root: Path, selector: str, value: str | None = None):
    root = root.resolve()
    if selector != 'cases' and (not isinstance(value, str) or not value):
        raise ValueError('A nonempty lookup value is required')
    if selector in ('cases', 'case', 'recovery'):
        data = load_json(local_file(root, CATALOGS[0]))
        if selector == 'cases':
            return {'scope': data['scope'], 'routing': data['routing'], 'cases': data['cases']}
        if selector == 'recovery':
            return next(row for row in data['routing'] if row['recovery_access'] == value)
        return next(case for case in data['cases'] if case['id'] == value)
    if selector == 'field':
        data = load_json(local_file(root, CATALOGS[2]))
        rules = [rule for rule in data['general_rules'] if value.lower() in rule['field'].lower()]
        notes = [note for note in data['notes'] if value == note['id'] or
                 any(value == pointer.rsplit('/', 1)[-1] for pointer in note['expected_values'])]
        if not rules and not notes:
            raise ValueError('Unknown field or annotation: ' + value)
        return {'scope': data['scope'], 'general_rules': rules, 'notes': notes}
    data = load_json(local_file(root, CATALOGS[1]))
    if selector == 'family':
        return next(family for family in data['families'] if family['id'] == value)
    if selector == 'topic':
        families = [{k: v for k, v in family.items() if k != 'members'} |
                    {'source_count': len(family['members'])}
                    for family in data['families'] if value.lower() in family['topics']]
        if not families:
            raise ValueError('Unknown source topic: ' + value)
        return {'scope': data['scope'], 'families': families}
    if selector != 'source':
        raise ValueError('Unknown selector: ' + selector)
    name = canonical_path(value)
    index = load_json(local_file(root, 'toolkit/INDEX.json'))
    entry = next(entry for entry in index if entry['path'] == name)
    family = next((family for family in data['families']
                   if family['id'] == entry.get('family_id')), None)
    # Return family context once; avoid echoing all sibling paths for one lookup.
    return {'source': entry, 'family_context':
            {k: v for k, v in family.items() if k != 'members'} if family else None}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--cases', action='store_true')
    group.add_argument('--case', metavar='CASE_ID')
    group.add_argument('--recovery', choices=('working', 'unavailable', 'unknown'))
    group.add_argument('--topic', metavar='TOPIC')
    group.add_argument('--family', metavar='FAMILY_ID')
    group.add_argument('--source', metavar='REPOSITORY_PATH')
    group.add_argument('--field', metavar='FIELD_OR_NOTE_ID')
    args = parser.parse_args(argv)
    selector = next(key for key in ('cases', 'case', 'recovery', 'topic', 'family', 'source', 'field')
                    if getattr(args, key) is not None and getattr(args, key) is not False)
    try:
        result = query(args.root, selector, getattr(args, selector))
    except (OSError, ValueError, KeyError, TypeError, StopIteration) as exc:
        print(json.dumps({'error': str(exc) or 'No matching navigation record'}))
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
