# Publication provenance

- Publication language: English.
- Review date: 2026-09-12.
- Base: supplied English archive plus the two sanitized public repair archives
  and their final handoffs; see [INPUTS.json](INPUTS.json).
- No new hardware activity, private dump import, or executable firmware import.
- All 456 historical source snapshots are byte-preserved from the English input;
  see [SNAPSHOT_PRESERVATION.json](SNAPSHOT_PRESERVATION.json).
- Thirty-seven early public evidence records were restored by translating only
  their editorial `interpretation` field; see [RESTORED_EVIDENCE.json](RESTORED_EVIDENCE.json).
- Consolidated explanations preserve the distinction between observations,
  proposed mechanisms, failed attempts, and final functional confirmation.
- The independent boot-ID checker was introduced in an earlier publication pass.
  New final-review scripts/tests maintain this archive, not the repair device.
- A network package downloader is separated from offline tools. No real package
  download or installer run occurs in the test suite.
- Sources retained original attribution; the old 5ch thread was not retrievable
  during this review and is explicitly marked as inherited attribution metadata.

The final audit is in [RELEASE_AUDIT.md](RELEASE_AUDIT.md). This is a reviewed public
research archive, not a reconstruction of omitted private inputs or a runnable
recovery distribution.
