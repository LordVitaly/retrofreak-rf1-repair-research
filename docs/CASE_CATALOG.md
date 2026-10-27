# Repair case catalog

[CASES.json](../CASES.json) is the machine-readable entry point. Its paths are
relative to the repository root. It supplements the complete case narratives;
the original [REPAIR_SUMMARY.json](../REPAIR_SUMMARY.json) retains its original
single-unit scope and every existing field.

| Case ID | Owner | Access during successful repair | Reported path and evidence |
|---|---|---|---|
| `rf1-lordvitaly-2026-09` | [LordVitaly](https://github.com/LordVitaly) | Recovery unavailable; MaskROM available | [Original deeper repair](SUCCESSFUL_RECOVERY_PATH.md), [measured records and functional limits](../STATUS.md) |
| `rf1-yamanotsume-2026-10` | [Yamanotsume](https://github.com/Yamanotsume) / [u/yamanotsume](https://www.reddit.com/user/yamanotsume/) | Working SD Recovery System v1.1 | [Plain-rkimage update case](COMMUNITY_RECOVERY_CASE_01.md), [owner's issue report](https://github.com/LordVitaly/retrofreak-rf1-repair-research/issues/1#issuecomment-6445589262) |

## Choose a reading route

1. Record symptoms, hardware/firmware observations, and whether recovery is
   actually reachable. Keep an unmeasured condition `unknown`.
2. With working recovery, read Yamanotsume's case and its firmware/write-scope
   prerequisites. A symptom/access match does not prove an identical fault.
3. With recovery unavailable, read the original case and [Safety and scope](SAFETY_AND_SCOPE.md).
   Unavailable recovery alone does not establish the same NAND damage or make
   the original addresses, hashes or writers portable.
4. For an unknown condition, use the [decision tree](DECISION_TREE.md) to collect
   evidence first. The catalog deliberately selects no case for `unknown`.
5. Follow the [source index guide](SOURCE_INDEX.md) only for the relevant topic,
   and the [field guide](EVIDENCE_FIELD_GUIDE.md) before interpreting JSON flags.

The second case is an external owner report. It does not independently repeat
the original low-level repair. Original-unit measurements and community-reported
results retain their separate sources and validation limits.

## Local JSON queries

```sh
python -B scripts/query_research.py --cases
python -B scripts/query_research.py --recovery unknown
python -B scripts/query_research.py --case rf1-yamanotsume-2026-10
```

These commands read local navigation metadata only. They do not choose or run a
repair, download firmware, connect hardware or execute historical sources.
