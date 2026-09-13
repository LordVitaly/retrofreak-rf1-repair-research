# Evidence

This is selected, redacted evidence, not a new device test or a complete private
forensic acquisition. [INDEX.json](INDEX.json) lists every included record.
[The evidence map](../docs/EVIDENCE_MAP.md) connects conclusions to records.

- `phase1/selected/` — 37 early public records. The editorial `interpretation`
  field was translated into English; other JSON fields were preserved. These
  cover acquisition, diagnostic experiments, modeled repair and actual early
  writes, including unsuccessful attempts and limited validation.
- `phase2/primary/` — late redacted results for IDB/BBT, boot, cache, Linux-visible
  system and userdata work. A filename containing `final` is local to that stage,
  not necessarily the final state of the console.
- `phase2/usb_stock_final_evidence.json` — curated stock-boot return and USB tests.
- `phase2/functional_cold_boot_confirmation.json` — neutral final functional
  observation after physical power removal, not another binary NAND comparison.

The primary entries are sanitized public copies: missing hashes, device selectors,
private images and raw logs were intentionally not reconstructed. Internal `work/`
paths indicate provenance in the original task and are not guaranteed to be local
repository paths. Do not follow them as instructions to recreate a device state.

A `PASS` may mean a completed measurement of damaged data. A final host `FAIL` may
follow a successful hardware write. Read the interpretation and phase boundaries.
