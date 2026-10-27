# Reading ambiguous evidence fields

[EVIDENCE_FIELDS.json](EVIDENCE_FIELDS.json) is an additive annotation catalog.
Original evidence JSON, source snapshots and the original repair summary remain
unchanged. Each note identifies an original record, exact RFC 6901 JSON Pointers,
expected values, meaning, and an inference the record does not support.
All file paths are relative to the repository root.

## Common traps

| Field or label | Meaning to establish before using it |
|---|---|
| `all_pass` | The script's checks at one stage passed. In the BBT measurement, it means damaged copies were successfully measured. |
| `all_pass: false` | Determine whether a write was already dispatched and what readback showed. A host assertion is not permission to retry. |
| `data_writes: false` in the system-repair result | The `/data` userdata partition was not written by that runner. Four `/system` ranges were written. |
| `hardware_ready` | Historical build/readiness status for exact old inputs and guards; not current authorization or a physical safety guarantee. |
| A filename containing `final` | Local to that stage. `boot_final_verified` still describes diagnostic boot, before stock return. |
| `pending` | Read the observation time. Earlier pending flags and a later current-status confirmation can both be correct. |
| `first_6MiB_exact` in the cache reconstruction | Distinguish actual block readbacks from clean-image free space supplied during reconstruction. |
| `stock_boot_confirmed_by_functional_test` | Operator functional observation; not a fresh post-power-cycle binary NAND comparison. |
| `final_validation` in the original summary | Consolidated observations across repair stages; consult `validation_limits` for timing of save import and other checks. |
| Redacted hashes, selectors and `work/` paths | Omitted old inputs/provenance, not runnable configuration or necessarily repository-local files. |

## Record-specific notes and queries

The catalog currently covers the BBT measurement, IDB write with a later failed
check, both userdata runner attempts, Linux system repair, diagnostic boot,
cache preparation/reconstruction, stock-return timing, final functional report
and the original summary. Generic rules are reading aids, not universal meanings
for similarly named fields in every script.

```sh
python -B scripts/query_research.py --field data_writes
python -B scripts/query_research.py --field all_pass
python -B scripts/query_research.py --field stock-readback-before-cold-test
```

The first two select an exact field name; the last selects an annotation ID.
Repository checks resolve every annotated pointer and check its pinned value,
including its JSON type. A changed record or stale pointer requires review of
the explanation; regenerating manifests alone cannot hide that mismatch.

Use the [evidence model](REPRODUCIBILITY.md) and [evidence map](EVIDENCE_MAP.md)
with these annotations. No boolean flag authorizes executing an archival writer.
