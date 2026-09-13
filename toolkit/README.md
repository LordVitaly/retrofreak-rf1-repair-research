# Toolkit

This directory contains sanitized source snapshots and one standalone local-file
checker. No runnable device flasher is distributed.

- [Phase 1](phase1_20260903/) — 3–8 September low-level NAND/FTL/FlashBoot research.
- [Phase 2](phase2_20260908/) — 8–9 September boot/cache/system/userdata/USB repair.
- [Offline checker](offline/) — the read-only RF-1 boot-ID verifier.
- [Tooling guide](../docs/TOOLING.md) — scope and usage.
- [Machine-readable index](INDEX.json) — every toolkit file and its role.

Historical sources retain an extra `.txt` extension and a non-executable header.
They are snapshots of a stateful repair environment, including abandoned variants,
not independently runnable programs. Renaming them is not a safety review.

One publication-only script that rewrote a source-language narrative report was
omitted in the earlier English edition; it performed no hardware work. The
recovery-package builder was retained with its generated README translated. This
final review does not change any historical source snapshot.

The optional network-only Cygwin acquisition helper is in
[scripts/download_cygwin_packages.py](../scripts/download_cygwin_packages.py), not
in the offline directory. It downloads pinned packages but never installs or runs
them; tests use mocked responses and require no network.
