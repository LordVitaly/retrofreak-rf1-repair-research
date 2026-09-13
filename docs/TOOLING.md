# Tooling guide

The archive preserves the research tools that were used to understand the RF-1. Most historical sources have an extra `.txt` extension intentionally: they are **reference snapshots**, not click-to-run repair software.

## Directories

### `toolkit/phase1_20260903/`

Early work around:

- MaskROM/Rockusb transport;
- NAND acquisition;
- ECC24/ECC40 experiments;
- FTL mapping and cache reconstruction;
- FlashBoot reverse engineering;
- RAM bridge construction;
- guarded system writer experiments;
- power/PMIC investigation.

### `toolkit/phase2_20260908/`

Later work around:

- IDB/FlashInfo/BBT geometry;
- diagnostic Android boot construction;
- vendor boot-ID verification;
- cache filesystem rebuild;
- live Linux `/system` audit and targeted repair;
- userdata fsck workflow;
- USB host test;
- stock boot restoration.

### `toolkit/offline/`

The standalone local-file checker `rf1_boot_digest.py`. It does not access USB,
write images or reconstruct device-specific state. Tests live in `tests/`.
The optional package downloader lives in `scripts/`, because it uses the network.

## Why the old writers are inert

Many historical writer sources contain case-specific assumptions such as target blocks, mappings, expected hashes and RAM addresses. Even where those values were redacted, the underlying workflow still assumes a particular device state.

They are preserved for review of:

- safety gates;
- control flow;
- readback strategy;
- stop/no-retry behavior;
- FTL and NAND API usage.

They are **not** a universal flasher.

## Publication-only omission

One historical script whose only purpose was to rewrite Russian-language narrative reports was omitted from this English-only archive. It performed no device I/O and contained no repair logic.

## External dependencies

See `third_party/DEPENDENCIES.md` for Zig, Unicorn, Capstone, pyelftools, dissect.extfs, pywinpty, Rockchip tooling, Cygwin/e2fsprogs and source references.
