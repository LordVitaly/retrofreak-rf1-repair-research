# Safety and scope

## Do not reuse physical addresses from this case

Physical blocks such as 0, 12, 22, 74, 77, 78, 960, 1028 and others appearing in evidence are measurements from one changing FTL state on one RF-1. They are not constants of the platform.

Always re-measure the current mapping immediately before any device-specific operation.

## Keep address spaces separate

Do not conflate:

- physical NAND block/page/sector addresses;
- logical FTL block numbers;
- Android partition LBA;
- IDB boot-order records;
- normal ECC40 page layout;
- `RS` 528-byte transport records;
- early FTL mode0 vs full mode1 views.

## A RAM download or a command named “read” is not a safety guarantee

Late phase-1 analysis identified a destructive geometry probe in the original
**unguarded USBplug** initialization path (`0x6D7C -> 0x4230` in the investigated
binary). It can reach erase/program operations. `DB` transfers code to RAM;
that code may still write NAND as soon as it executes. A log containing only
DB/RID/RFI/RS is therefore not proof that no NAND writes occurred.

Original FTL read/remap paths can also allocate blocks or update service metadata
when a mapping is missing. The restrictions in the tested guarded variants apply
to those exact binaries and observed paths, not to every similarly named tool.
Offline guards and successful tests are evidence, not an absolute hardware write
barrier. The historical cause and timing of the device's corruption remain unknown.

## Back up before any repair

At minimum:

- preserve an untouched raw acquisition;
- verify checksums on an independent copy;
- capture the current active map before a write;
- record the exact source image and expected target range.

## No blind retries

A host-side timeout or a final `all_pass=false` can occur **after** a NAND write has already completed successfully. Before repeating anything, determine whether erase/program happened and whether readback already proved the new state.

## Prefer the layer used by normal boot

If live Linux is available, use it to validate `/system`, `/data` and `/cache`. It is stronger evidence for normal Android behavior than a separate service loader with a potentially different mapping view.

## Device-specific writers

Historical writer sources are kept as inert `.txt` snapshots. Redacted hashes, paths and selectors make them unsuitable for direct replay. This is intentional.

## Mounted filesystems

The successful Linux repairs stopped relevant Android services and genuinely
unmounted the target filesystem. Read-only mounting is not equivalent to
unmounting for a repair beneath the filesystem. The userdata checker was tested
on a copy and run once on the unmounted target. Historical destructive commands
are evidence of what happened, not copy-and-paste instructions for another unit.

## Power and USB roles

Never remove power during erase/program. A cold-persistence test must remove both
PSU and PC USB power after all activity has stopped; USB can keep circuitry
powered. The diagnostic boot forced device/ADB mode and was later replaced with
stock boot to restore ordinary host behavior.

This archive does not establish the electrical safety of arbitrary USB-A-to-A
cables or the VBUS topology of other revisions. Do not infer connector orientation
from an unspecified photo angle, connect two host power outputs blindly, or change
USB role with the PC cable still attached. The documented temporary host test
waited for confirmed physical disconnection before switching.

## Limits of this archive

There is no universal runnable flasher or guaranteed rollback here. The public
sources deliberately omit private images, hash pins and complete device maps.
Do not re-enable or execute an archival writer merely to reproduce a published PASS.
