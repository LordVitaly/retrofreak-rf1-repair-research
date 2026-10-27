# Project status

**Functional recovery is confirmed on the investigated RF-1. Stock boot was restored.**

| Result | Evidence and timing |
|---|---|
| Stock boot restored | Native main/meaningful-aux readback for three freshly selected physical targets; unchanged complete FTL maps; 10 MiB checked through both modes before power removal. |
| Ordinary cold startup | Functional confirmation after both PSU and PC USB were disconnected. No post-cold full NAND read was performed. |
| Power, HDMI, GUI and settings | Working-state measurements plus repeated functional restarts; language/agreement persisted. |
| Writable `/data` and `/cache` | Measured in the working Linux state after userdata repair. |
| Adapter, controller, GBC game | Reported during temporary host testing and again after the final stock-boot cold start. |
| Save import / accessory update | Reported successful during the temporary host test before stock-boot return; no separate new save-import measurement on the last cold start. |

See the [evidence map](docs/EVIDENCE_MAP.md) and
[final-stage record](evidence/phase2/usb_stock_final_evidence.json).

## Community follow-up (2026-10-27)

[Yamanotsume](https://github.com/Yamanotsume) reports normal startup on a second
early RF-1 after a plain-rkimage update through working SD recovery; the unit had
been stuck on the splash screen since 2016. Thank you for documenting the steps
and hashes in [issue #1](https://github.com/LordVitaly/retrofreak-rf1-repair-research/issues/1#issuecomment-6445589262).
See the [case summary](docs/COMMUNITY_RECOVERY_CASE_01.md) for the method and limits.

This is an external owner report, not a second maintainer-tested instance of the
original low-level repair. The original unit's recovery was no longer being
reached; it required the deeper boot-chain/NAND/FTL and filesystem work documented
here. The second report does not add new cold-persistence, binary readback or
peripheral measurements to the original evidence table.

## Not established for the original unit

- Physical health or endurance of every NAND cell.
- Recovery of every previous userdata/lost+found object.
- Validation of every supported cartridge, port, accessory, or game.
- The time or cause of each original or later corruption event.
- A tested complete rollback from a public archive (private images are excluded).
- Classification/resolution of the three startup NAND diagnostic dumps and
  readahead restart noted in an earlier working-state capture.

The repaired unit's maps and addresses are historical measurements, not a layout
for another console. The original measured repair and the separate community
recovery report do not constitute a universal flasher.
