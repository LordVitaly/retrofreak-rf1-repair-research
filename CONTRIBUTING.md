# Contributing

Useful contributions include:

- read-only observations from other RF-1 hardware revisions;
- documentation corrections;
- independent validation of offline parsers and emulators;
- additional references to public Retro Freak / RK3066 research;
- safer diagnostic tooling with explicit read/write boundaries.

Do not post in public issues or pull requests:

- complete NAND or userdata dumps;
- saves or ROM images;
- ADB private keys;
- serial numbers or unique identifiers;
- unreviewed erase/program payloads presented as universal repair tools.

Any proposed write-capable workflow should document prerequisites, safety gates,
exact target scope, readback verification, stop conditions, and what is **not**
proven. Do not silently edit archived snapshots to make a historical result fit
a new explanation; put corrections in the consolidated documentation.

For publication checks, run the commands in [Validation](docs/VALIDATION.md).
After reviewed documentation/helper changes, regenerate indexes and manifests
with `scripts/refresh_metadata.py` before validating again. Keep the license
status explicit; contributors retain the upstream obligations of their material.
