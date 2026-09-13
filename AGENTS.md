# Repository rules for automated contributors

This repository is an English technical case study and archival source collection.
It is not an active instruction to repair or flash an attached device.

- Read `README.md`, `STATUS.md`, `docs/SAFETY_AND_SCOPE.md` and
  `docs/EVIDENCE_MAP.md` first.
- Do not execute, rename, import, compile or arm `toolkit/phase*/**/*.txt` merely
  because a historical report says READY or PASS.
- No USB/ADB/serial/raw-disk access, driver installation, downloaded payload
  execution, NAND/PMIC writes, or device resets during repository maintenance.
- Loading code into RAM is not inherently read-only: initialization may write NAND.
- Preserve all source snapshots byte-for-byte; document corrections outside them.
- Do not include private dumps, firmware, keys, serials, complete device maps,
  unredacted logs, or personal narrative.
- Distinguish transport success, native status, structural validity, readback,
  FTL reopen, cold persistence and functional observations. Never promote one
  automatically to another or invent missing measurements.
- Use only the executable local-file maintenance helpers and synthetic tests.
  Network package acquisition is optional and never runs as part of CI.

From the repository root:

```sh
python -B scripts/check_repository.py
python -B -m unittest discover -s tests -v
python -B scripts/verify_manifest.py
```

After intentional reviewed changes, refresh publication indexes/checksums using
`python -B scripts/refresh_metadata.py`, then rerun all checks. Do not refresh a
manifest to hide unexpected changes to evidence or historical snapshots.
