# Evidence map and claim boundaries

The final state is summarized in [STATUS](../STATUS.md). Intermediate records are
historical observations; a PASS from one stage must not replace a later outcome.
No private dump or vendor binary is included. Links below resolve to public,
redacted records, not to the original private workspace.

| Finding | Included evidence | Limit |
|---|---|---|
| Native-ECC40 acquisition completed | [Acquisition verification](../evidence/phase1/selected/outputs/native_dump_complete_verification.json) | File completeness and independent-copy equality, not proof of every native ECC result. |
| Original boot content matched | [Extracted boot record](../evidence/phase1/selected/outputs/boot.from_nand.verified.json) | That acquisition, before later diagnostic-boot writes; no donor fill. |
| Original system damage | [Block candidates](../evidence/phase1/selected/outputs/native_system_block_audit_2048blocks.json), [vold evidence](../evidence/phase1/selected/outputs/vold_nand_evidence.json) | Base candidates and inode evidence, not the whole active Linux view. |
| System rewrite in a model | [Offline roundtrip](../evidence/phase1/selected/outputs/flashboot_system_rewrite_attempt3.json) | ARM/FTL model, not physical NAND programming behavior. |
| First bridge-based logical read | [Hardware read](../evidence/phase1/selected/work/ftl_bridge_read_hardware_attempt01/result.json) | One verified boot sector. |
| Early full-system write | [Finish record](../evidence/phase1/selected/work/system_finish236_259_attempt01/result.json) | Exact same-path readback; `cold_boot_verified=false`; not proof of later Linux data. |
| Invalid-capacity mechanism | [Bounded replay](../evidence/phase2/primary/work/zero_capacity_replay_v3.json) | Reproduces a mechanism; does not date or attribute the historical corruption. |
| Original IDB0 / BBT12 result | [BBT restoration](../evidence/phase2/primary/work/bbt_restore_after_copy0_attempt04/result.json), [original-path check](../evidence/phase2/primary/work/original_boot_after_idb0_attempt01/result.json) | Geometry/BBT acceptance in the measured path; no claim of an independent PMIC hardware diagnosis. |
| Vendor boot ID validation | [ARM verifier audit](../evidence/phase2/primary/work/boot_header_validation_audit/report.json) | Formula applies to the investigated boot format/binary. |
| Different boot maps | [Diagnostic boot verification](../evidence/phase2/primary/work/boot_final_verified/result.json) | Historical mode0/mode1 owners differ. Not the final stock-return mapping. |
| Cache rebuild | [Selective live verification](../evidence/phase2/primary/work/cache_last_attempt/live_verify_result.json) | Necessary allocated regions restored; not all cache bytes erased. |
| Linux-visible system damage | [Full comparison](../evidence/phase2/primary/work/live_system_audit/live_compare_report.json) | Four active damaged ranges; historical origin of each defect unknown. |
| Four-block system repair | [Repair result](../evidence/phase2/primary/work/linux_system_four_repair_attempt01/result.json), [cold checks](../evidence/phase2/primary/work/live_system_audit/cold_boot_file_checks.json) | Four ranges and selected files verified; history fields deliberately retained. |
| Userdata fsck | [Offline trial](../evidence/phase2/primary/work/userdata_repair_trial/report.json), [actual repair](../evidence/phase2/primary/work/userdata_native_repair_attempt02/result.json) | Unmounted filesystem repaired; no proof of every recovered file's content. |
| Working Android state | [Functional measurement](../evidence/phase2/primary/work/live_adb_after_data_repair/functional_validation.json) | Earlier diagnostic boot still installed at this point. |
| Stock boot and host return | [Final-stage record](../evidence/phase2/usb_stock_final_evidence.json) | Native/both-mode readback before the last power removal. |
| Final cold start and game | [Functional confirmation](../evidence/phase2/functional_cold_boot_confirmation.json) | Reported functional outcome, not new binary readback; save import observed at the earlier host test. |

## Corrected interpretations

- Runtime mapping divergence was directly measured for boot. It must not be used
  as proof of exactly when or how every later system defect appeared.
- No single “read-only” command name or RAM download proves the executed code
  cannot write NAND. The dangerous unguarded init path is documented in
  [Safety and scope](SAFETY_AND_SCOPE.md) and the phase-1 source handoff provenance.
- Early PMIC experiments were temporary diagnostics. The stable early-boot
  result followed original IDB0/BBT restoration, not a proven PMIC replacement.
- Successful recovery of the GUI did not yet restore the stock USB role. The
  later stock-boot return and cold peripheral test are separate final evidence.

## Why some source records are not direct links

The supplied public handoffs contain more explanation than the selected English
JSON subset. Publication inputs and hashes are listed in
[Input provenance](../provenance/INPUTS.json); non-English narrative originals are
not included in this English-only repository. The historical sources and redacted
results are finite snapshots, not a complete replayable trace. No missing result
or private artifact has been fabricated to make the repair look reproducible.
