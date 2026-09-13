# Reproducibility and evidence model

The investigation deliberately separates different classes of proof.

## Evidence levels

1. **Host-side success** — a script completed without an exception.
2. **Transport success** — USB/Rockusb returned the expected response.
3. **Native read/program status** — the underlying NAND routine returned success.
4. **Structural validity** — the bytes form a valid FlashInfo/BBT/filesystem/image structure.
5. **Immediate readback** — the newly written target compares exactly.
6. **FTL reopen persistence** — the mapping survives a new FTL initialization.
7. **Cold persistence** — data survives complete power removal.
8. **Normal-boot consumption** — the same layer used by the operating system reads and uses the repaired data.
9. **Functional validation** — GUI/peripheral/game behavior is actually restored.

A result at one level must not be silently promoted to a higher level.

## Key example

The early system writer achieved exact loader-level readback; later Linux-visible reads exposed four corrupt blocks. Different FTL boot mappings were independently measured, but the timing and cause of the later system defects were not established. These observations demonstrate the limit of one readback path, not proof of a single mechanism for all corruption.

## Manifest

[MANIFEST.sha256](../MANIFEST.sha256) and [MANIFEST.json](../MANIFEST.json)
cover every published file except the two manifests themselves. The verifier
also rejects unlisted files and disagreement between the two formats. They
verify publication integrity, not unavailable private images or hardware safety.
See [Validation](VALIDATION.md) for the local commands and regeneration procedure.
