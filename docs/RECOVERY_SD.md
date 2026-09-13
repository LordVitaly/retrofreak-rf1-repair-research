# RetroN5 recovery SD on Retro Freak

A community-documented path uses the RetroN 5 full-reset SD image to reach
recovery on Retro Freak. It was an earlier, less invasive access route than board
level work, not a manufacturer-supported RF-1 repair procedure. Executing factory
reset can erase internal data and requires its own informed decision and backup.

## Source image used in the investigation

`boot-recovery-SD-fullreset-v0.2.2.img`

Observed image properties:

- size: 199,229,440 bytes
- SHA-256: `951d8777eaed7eca15de2cc65c3ebd488e4f977b17c698ae9906c36b1761f042`
- sector 0 begins with `RETRON5___BOOTSD`
- partition 1: FAT32
- partition 2: Linux/ext filesystem labelled `data`
- partition 3: Linux/ext filesystem labelled `cache`

The `data` partition contains `/bootscript.sh` whose essential action is to request recovery boot.

## Observed success and later failure

The method reached `RetroFreak Recovery System v1.1` once on the reference RF-1. `Wipe data/factory reset` completed but did not fix the white-screen failure.

Later, a diagnostic marker was inserted into `/data/bootscript.sh`. The partition was written and read back exactly. After multiple controlled boot attempts the partition remained byte-identical and the marker was never created. No persisted marker was observed in those attempts. This does not by itself prove that the script was never entered or that the marker write succeeded.

An earlier BOOTSD-selection or SD-device-availability failure remained a plausible explanation, rather than an established exclusive cause.

## Practical recommendation

Consider the documented recovery access path before low-level repair when its
limitations are acceptable. The unsuccessful marker tests do not prove a dead
microSD slot; they show that the marker was not reached or persisted in those
attempts. Repeated script edits are not a diagnosis of the earlier failure.

See [Sources and credits](SOURCES_AND_CREDITS.md) and the
[local recovery-SD analysis](../references/RECOVERY_SD_READONLY_REPORT.md).
