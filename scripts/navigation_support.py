"""Read-only navigation metadata helpers. Never import archival source code."""
from __future__ import annotations

from pathlib import Path
import json
import re

from repo_support import canonical_path, load_json, publication_files

CATALOGS = ('CASES.json', 'toolkit/SOURCE_FAMILIES.json', 'docs/EVIDENCE_FIELDS.json')
ARCHIVE_PREFIXES = ('toolkit/phase1_', 'toolkit/phase2_')


def local_file(root: Path, name: str) -> Path:
    name = canonical_path(name)
    path = (root / name).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file():
        raise ValueError('Missing/nonlocal navigation reference: ' + name)
    return path


def pointer_value(document, pointer: str):
    """Resolve an RFC 6901 JSON Pointer without eval or permissive list indexes."""
    if pointer == '':
        return document
    if not isinstance(pointer, str) or not pointer.startswith('/'):
        raise ValueError('Invalid JSON Pointer: ' + str(pointer))
    value = document
    for token in pointer[1:].split('/'):
        if re.search(r'~(?![01])', token):
            raise ValueError('Invalid JSON Pointer escape: ' + pointer)
        token = token.replace('~1', '/').replace('~0', '~')
        if isinstance(value, list):
            if not re.fullmatch(r'0|[1-9][0-9]*', token):
                raise ValueError('Invalid JSON Pointer array index: ' + pointer)
            value = value[int(token)]
        elif isinstance(value, dict):
            value = value[token]
        else:
            raise ValueError('JSON Pointer traverses a scalar: ' + pointer)
    return value


def unique_by_id(entries: list[dict]) -> dict:
    result = {}
    for entry in entries:
        key = entry['id']
        if not isinstance(key, str) or not key or key in result:
            raise ValueError('Missing/duplicate navigation ID: ' + str(key))
        result[key] = entry
    return result


def family_members(families: list[dict]) -> dict:
    unique_by_id(families)
    members = {}
    for family in families:
        if not family['purpose'] or not family['members']:
            raise ValueError('Empty source family: ' + family['id'])
        for name in family['members']:
            name = canonical_path(name)
            if name in members:
                raise ValueError('Duplicate source-family membership: ' + name)
            if not name.startswith(ARCHIVE_PREFIXES) or not name.endswith('.txt'):
                raise ValueError('Family member is not an archival snapshot: ' + name)
            members[name] = family
    return members


def toolkit_entries(root: Path, files: list[Path]) -> list[dict]:
    """Retain the original array/path/kind contract; add source navigation fields."""
    source_names = {p.relative_to(root).as_posix() for p in files
                    if p.relative_to(root).as_posix().startswith(ARCHIVE_PREFIXES)}
    members = {}
    if source_names:
        members = family_members(load_json(root / CATALOGS[1])['families'])
        if set(members) != source_names:
            raise ValueError('Source-family coverage differs from archival snapshots')
    result = []
    for path in files:
        name = path.relative_to(root).as_posix()
        if not name.startswith('toolkit/') or name == 'toolkit/INDEX.json':
            continue
        historical = name in source_names
        kind = ('inert_historical_source_snapshot' if historical else
                'executable_local_file_checker' if path.suffix == '.py' else 'documentation')
        entry = {'path': name, 'kind': kind}
        if historical:
            family = members[name]
            header = '\n'.join(path.read_text('utf-8').splitlines()[:6])
            match = re.search(r'^Role: (.+)$', header, re.M)
            role = match.group(1) if match else 'historical_redacted_source_snapshot'
            disposition = 'historical_case_specific'
            if role == 'historical_unexecuted_superseded_boot1028':
                disposition = 'superseded_or_unexecuted'
            elif role == 'historical_incomplete_builder_old_boot_id_must_not_be_final_recipe':
                disposition = 'incomplete_historical_builder'
            elif role == 'completed_stock_return_or_temporary_USB_probe_historical_source':
                disposition = 'completed_stage_historical'
            entry.update(family_id=family['id'], purpose=family['purpose'],
                         case_ids=family['case_ids'], role_from_header=role,
                         disposition=disposition)
        result.append(entry)
    return result


def validate_navigation(root: Path) -> tuple[list[str], dict]:
    """Check coverage, references, case routing, and field-note pins as data only."""
    root = root.resolve()
    cases, sources, fields = [load_json(local_file(root, name)) for name in CATALOGS]
    for catalog in (cases, sources, fields):
        if catalog['schema_version'] != 1 or catalog['path_base'] != 'repository_root':
            raise ValueError('Unsupported navigation catalog schema/path base')
    bycase = unique_by_id(cases['cases'])
    byfamily = unique_by_id(sources['families'])
    unique_by_id(fields['notes'])
    errors = []

    def check_cases(ids):
        for case_id in ids:
            if case_id not in bycase:
                errors.append('Unknown case ID: ' + case_id)

    def check_files(names):
        for name in names:
            try:
                local_file(root, name)
            except ValueError as exc:
                errors.append(str(exc))

    for case in bycase.values():
        if case['recovery_access'] not in ('working', 'unavailable', 'unknown'):
            errors.append('Unknown recovery access: ' + case['id'])
        check_files(case['related_docs'] + case['related_evidence'])
        if 'summary_path' in case:
            check_files([case['summary_path']])
    routing = cases['routing']
    if sorted(row['recovery_access'] for row in routing) != ['unavailable', 'unknown', 'working']:
        errors.append('Recovery routing must cover working, unavailable and unknown exactly once')
    for route in routing:
        check_cases(route['case_ids'])
        check_files(route['read_next'])
        if route['recovery_access'] == 'unknown' and route['case_ids']:
            errors.append('Unknown recovery access must not silently select a case')
        for case_id in route['case_ids']:
            if case_id in bycase and bycase[case_id]['recovery_access'] != route['recovery_access']:
                errors.append('Case routed under a different recovery condition: ' + case_id)
    for family in byfamily.values():
        check_cases(family['case_ids'])
        check_files(family['related_docs'] + family['related_evidence'])
        for key in ('inputs', 'dependencies', 'interpretation', 'topics'):
            if not family[key]:
                errors.append('Missing source-family detail: ' + family['id'] + '/' + key)
    expected_index = toolkit_entries(root, publication_files(root))
    if load_json(root / 'toolkit/INDEX.json') != expected_index:
        errors.append('Detailed toolkit index is stale or changed outside its catalog')
    for note in fields['notes']:
        check_cases([note['case_id']])
        check_files(note['related_sources'])
        record = load_json(local_file(root, note['record']))
        if not note['expected_values'] or not note['meaning'] or not note['do_not_infer']:
            errors.append('Incomplete field note: ' + note['id'])
        for pointer, expected in note['expected_values'].items():
            try:
                actual = pointer_value(record, pointer)
                if json.dumps(actual, sort_keys=True) != json.dumps(expected, sort_keys=True):
                    errors.append('Field-note pin changed: ' + note['id'] + pointer)
            except (KeyError, IndexError, ValueError, TypeError):
                errors.append('Unresolved field-note pointer: ' + note['id'] + pointer)
    return errors, {'repair_cases': len(bycase), 'source_families': len(byfamily),
                    'field_annotations': len(fields['notes'])}
