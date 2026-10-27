# Navigation revision after Yamanotsume's successful RF-1 recovery

Baseline commit: `0d5c5c60bed924c4fbbf0267a46b46b322de8148`.

Yamanotsume's [issue #1 report](https://github.com/LordVitaly/retrofreak-rf1-repair-research/issues/1#issuecomment-6445589262)
motivated a navigation revision for future readers and agents. This revision
adds a two-case catalog, explicit source-family membership, and record-specific
field annotations. No device was accessed and no hardware test was repeated.

## Preservation contract

- All 456 historical source snapshots retain their original paths and bytes.
- Existing evidence JSON/logs and historical review records, board photographs,
  upstream notices and earlier provenance records remain byte-identical to the
  baseline. Navigation links are appended to the evidence landing README.
- `REPAIR_SUMMARY.json` retains every original field/value and its original case
  scope. The new case catalog references it rather than converting it in place.
- Every old toolkit index entry retains its `path` and `kind`. Added fields refer
  to the new family catalog; no old source entry is removed or merged.
- Existing documentation is retained; new navigation links/sections are additive.
- New local helpers read metadata/text only and never execute historical code.

The family classifications are editorial reading aids. Header-derived special
statuses distinguish superseded/unexecuted and incomplete sources without
rewriting their headers. Field annotations use exact pointers and pinned values
so that their interpretations cannot silently drift from the retained records.

Baseline comparison confirmed all 632 original files still present, 573 protected
files byte-identical, and all 459 original toolkit entries retaining every old
field/value. Protection covers historical source snapshots, retained evidence
records/index, board assets, upstream material, earlier provenance and the original
repair summary. Existing Markdown edits add navigation without deleting old text.

## Validation

The existing checks now also validate catalog coverage, case routing, source
membership, local references, generated-index consistency and annotation pins.
Synthetic regression tests cover missing/duplicate sources, unknown-case routing,
stale annotations/indexes, JSON Pointer escaping and failed lookups.

Run the commands in [Validation](../docs/VALIDATION.md). Publication checks and
synthetic tests do not certify the safety of a hardware repair.
