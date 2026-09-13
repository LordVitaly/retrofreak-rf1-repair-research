# Historical report index

The original repair sessions generated many intermediate status reports. The English-only public archive does not retain the Russian narrative reports themselves; their validated findings are consolidated into `TECHNICAL_REPORT.md`, `SUCCESSFUL_RECOVERY_PATH.md` and `POSTMORTEM.md`.

The preserved machine-readable evidence and tool snapshots still reflect the two major work phases:

## Phase 1 — 3–8 September 2026

Key topics:

- MaskROM/Rockusb access
- native ECC40 NAND acquisition
- IDB ECC24 analysis
- FTL/F100/F200/BBT work
- FlashBoot reverse engineering
- RAM bridge
- guarded system write experiments
- power-hold diagnostics

## Phase 2 — 8–9 September 2026

Key topics:

- persistent IDB/FlashInfo/BBT geometry repair
- diagnostic boot and vendor boot-ID validation
- cache recovery
- root ADB
- Linux-visible `/system` audit and four-block repair
- userdata `e2fsck`
- temporary USB host validation
- stock boot restoration and final cold-boot functional verification

The absence of the original prose reports is deliberate: this repository is intended as an English technical reference rather than a verbatim conversation/archive dump.
