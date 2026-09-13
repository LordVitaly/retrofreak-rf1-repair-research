# Publication and privacy boundary

This public repository intentionally excludes:

- complete NAND, RAM, boot, userdata, cache, or removable-media dumps from the test unit;
- saves, ROMs and other user content;
- ADB private keys;
- serial numbers and unique USB instance identifiers;
- device-specific complete FTL maps and physical bad-block lists;
- commercial APK/SO files and official firmware binary payloads;
- ready-to-run device-specific destructive payloads.

Historical source snapshots use redacted placeholders where original paths, hashes, selectors or device-specific values were intentionally removed. Those files are research artifacts and should not be treated as ready-made configuration.

No private personal profile, account information or unrelated personal photographs
are included. The owner-supplied [board photographs](docs/BOARD_PHOTOS.md) show
hardware with incidental hands and background. Camera metadata, comments and
trailing data were removed; only image orientation remains. No explicit console
serial labels or personal text were identified in the reviewed images. Public
attribution uses the maintainer's GitHub handle.

Complete numeric mapping arrays and device-specific protected-target lists are also checked structurally in JSON. Selected owner changes remain public evidence; full arrays removed in the September 13 edition are described in [Publication update](provenance/PUBLICATION_UPDATE_2026-09-13.md).
