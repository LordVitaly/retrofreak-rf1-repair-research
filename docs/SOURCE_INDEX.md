# Finding the relevant historical sources

Start with the [case catalog](CASE_CATALOG.md), then choose a topic below.
[SOURCE_FAMILIES.json](../toolkit/SOURCE_FAMILIES.json) supplies purpose, inputs,
external dependencies, related documents/evidence and an explicit member list
for each family. All catalog paths are relative to the repository root.

The generated [toolkit index](../toolkit/INDEX.json) remains an array with its
existing `path` and `kind` fields. Every historical entry additionally carries
`family_id`, `purpose`, `case_ids`, `role_from_header` and `disposition`.
Shared context is stored once in the family catalog to avoid repeating long
explanations for hundreds of sources.

| Topic / family ID | Read to answer |
|---|---|
| `nand-acquisition-and-layout` | What was acquired, and how do raw528, native pages and partition offsets differ? |
| `idb-ecc24` | How were IDB boot-order pages and copy-specific guards investigated? |
| `early-geometry-and-bbt` | How did geometry/FlashInfo/BBT state affect capacity and power hold? |
| `ftl-and-early-system` | What did early FTL reads/models/writes prove, and where did they differ from Linux? |
| `boot-id-and-diagnostic-image` | Why did modified boot need the vendor ID, and what was incomplete? |
| `boot-owners-and-writers` | How were active owners, header writes and changing baselines investigated? |
| `cache-filesystem` | Which allocated cache ranges were repaired, and which bytes were reconstructed? |
| `live-system-repair` | How did Linux expose the four damaged system ranges? |
| `userdata-filesystem` | How were backup, offline trial, unmount and fsck results separated? |
| `stock-boot-return` | Which fresh-owner and readback checks preceded final stock return? |
| `usb-host-validation` | How was temporary USB host mode gated on cable disconnection? |
| `power-diagnostics` | Which PMIC/DEV_ON observations were temporary diagnostics? |
| `ram-and-usb-startup` | Which RAM/USB startup experiments and fixtures were explored? |
| `console-and-transport` | How could host output/completion checks fail independently of device activity? |
| `static-binary-analysis` | Which kernel, ELF, disassembly and external-ROM references were examined? |

## Status and interpretation

- `historical_case_specific`: retained analysis, payload source, runner or test;
  no automatic claim that it succeeded, is current or can be executed.
- `superseded_or_unexecuted`: the original header labels the old block1028
  variant superseded/unexecuted. Do not use it as the final boot recipe.
- `incomplete_historical_builder`: the original header identifies the incomplete
  builder with the old boot ID. Consult the vendor-ID audit and later case history.
- `completed_stage_historical`: the header identifies completed stock-return or
  temporary-USB work. A completed historical stage is not a portable tool.

`role_from_header` preserves the phase-2 role verbatim. Phase-1 snapshots receive
`historical_redacted_source_snapshot`, since their original header has no Role
field. Family membership is editorial navigation, not a fresh code-safety audit
or proof that every member produced the family's cited result. Consult the
specific source, evidence map and stage boundaries before drawing a conclusion.

All 456 original snapshots remain inert and byte-preserved. Case-specific
private images, hash pins, generated binaries and session state remain omitted.
The second owner's SD-recovery method does not require these historical writers.

## Query one slice rather than loading the entire index

```sh
python -B scripts/query_research.py --topic boot
python -B scripts/query_research.py --family live-system-repair
python -B scripts/query_research.py --source toolkit/phase2_20260908/work/repair_linux_system_four.py.txt
```

Topic queries return matching family context/counts; family queries include the
explicit member paths. Source queries return the entry and shared context without
echoing every sibling. Unknown IDs/paths exit with status 2 instead of silently
selecting a different case or source.

## Maintaining the index

Edit the additive family catalog, never historical headers. Every source must
belong to exactly one primary family; an omitted or duplicate member blocks index
refresh. Run `scripts/refresh_metadata.py` after reviewing intentional changes.
The repository check verifies family/case references, local evidence links and
the complete generated index. Existing `path`/`kind` consumers remain supported.
