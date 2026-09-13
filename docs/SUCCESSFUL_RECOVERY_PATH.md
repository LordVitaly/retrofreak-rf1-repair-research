# Successful recovery path

This document separates the sequence that ultimately contributed to a working RF-1 from dead ends, temporary hypotheses and experiments that were useful only for diagnosis.

## Preconditions

This is a retrospective sequence for one unit, **not authorization to repeat a
command or use the listed block numbers**. A RAM-loaded program can still erase
or program NAND during its own initialization; the command list alone does not
prove a read-only session. See [Safety and scope](SAFETY_AND_SCOPE.md).

The reference repair had all of the following before invasive work was attempted:

- working hardware MaskROM access;
- verified private NAND backups;
- the official Retro Freak update corresponding to application 1.5 / system 0.2.0 / build 2764;
- a way to load temporary code into RAM;
- logging and guards around potential NAND erase/program operations.

Do not copy the physical block numbers from this case to another unit.

## 1. Restore a valid early NAND geometry and BBT path

The early failure was not simply “bad power”. The original NAND initialization path could discover a new block size but continue using a candidate index derived from the earlier geometry. On the reference unit this caused FlashInfo to be read from the wrong physical location, produced an invalid capacity path, and prevented the bad-block/remap table from being accepted.

The stable early-boot fix was to restore an **original IDB0** and the required **BBT12** data. After a true power cycle, the unmodified early code then reported 2048 physical blocks and accepted the BBT with 1896 logical blocks. Stable power hold returned.

Temporary PMIC `DEV_ON` experiments were useful diagnostics but were not the final repair.

## 2. Build a diagnostic normal boot with root ADB

A diagnostic boot was required to observe the Android/Linux system directly. This introduced two important lessons:

- the early and full FTL views could select different physical owners for the same logical boot blocks;
- modified Android boot images required the vendor-specific boot ID/SHA-1 calculation used by the original FlashBoot verifier.

A successful write/readback through one FTL view did not prove that normal boot would select the same copy.

## 3. Repair only the necessary parts of `/cache`

A valid-looking ext filesystem signature was not enough: the root directory/journal state was damaged. A compatible empty cache filesystem was prepared offline, checked with `e2fsck`, and only the allocated regions required to establish the new filesystem were written.

This step enabled a useful normal Linux/ADB path but did not by itself fix the white screen.

## 4. Audit the **Linux-visible** `/system`

This was the decisive change in methodology.

Once root ADB was available, the complete `/system` used by the running kernel was read from `/dev/block/mtdblock8` and compared with the official system image. Exactly four damaged 2 MiB logical FTL blocks were found in the active Linux view:

| Global logical FTL block | Offset within `/system` | Repair size |
|---:|---:|---:|
| 192 | 12,582,912 | 2 MiB |
| 195 | 18,874,368 | 2 MiB |
| 198 | 25,165,824 | 2 MiB |
| 204 | 37,748,736 | 2 MiB |

The damage affected graphics/framework content, including the path that supplied `libGLESv1_CM.so`, and explained why SurfaceFlinger / the Retro Freak GUI could not progress.

## 5. Repair only those four `/system` blocks

With Android services stopped and `/system` genuinely unmounted, those four 2 MiB ranges were replaced with the corresponding data from the verified official system image. The remaining system data and historical error fields in the live superblock were preserved.

After cache drop, readback, and a cold boot, all four blocks, the GUI APK and the GLES library matched the expected data. The symptom advanced from the white screen to the Retro Freak splash screen.

## 6. Repair `/data` with the stock filesystem checker instead of formatting

The next blocker was different: `/data` contained bitmap/group-descriptor inconsistencies, the journal aborted, and Android remounted userdata read-only. SystemServer then could not create required databases/directories.

The safe sequence was:

1. capture a fresh full userdata backup while unmounted;
2. test `e2fsck -f -n` and a repair trial on a **copy** off-device;
3. on the RF-1, verify root access and that `/data` was unmounted;
4. run the stock static `e2fsck -f -y` once;
5. run `e2fsck -f -n` afterward and require a clean result;
6. perform a small write/read/delete probe and unmount again.

Userdata was not reformatted. After this step the GUI completed startup and settings persisted.

## 7. Validate USB host / cartridge adapter, then restore stock boot

The diagnostic boot intentionally forced the PC-facing port into USB-device/ADB mode. A temporary RAM-only host-mode test confirmed the cartridge adapter path without committing a permanent boot change.

Before restoring stock boot, the active boot mappings were measured again. The then-current mode0/mode1 owners were not the same historical physical addresses seen earlier in the investigation. The stock boot was therefore restored only to the **freshly measured active owners**, with full native page readback and map verification.

## 8. Final cold-boot validation

The final same-session binary checks verified restored stock boot through both FTL modes. After complete removal of PSU and PC USB power, an operator-reported test confirmed ordinary startup, the adapter, controller and the same Game Boy Color game. Save import was separately reported in the preceding temporary-host test; a fresh import after the final power cycle was not independently recorded. No new binary NAND read was performed after that final power cycle. These evidence levels are kept separate in [Final validation](../STATUS.md).

## What did not become the final solution

- Factory reset through recovery did not repair this unit.
- Repeating the recovery-SD experiment did not help once recovery stopped being reached; marker tests did not establish the exclusive cause.
- Swapping RAM loaders v1.24/v2.15 did not change the low-level read result.
- An early full-system rewrite through a diagnostic FTL path did not prove what normal Linux would later read.
- Temporary PMIC `DEV_ON` was diagnostic, not the final power fix.
- Repairing IDB5 alone did not restore normal boot.
- Repairing BBT12 without correcting the geometry source was not persistent.
- Bringing up FlashBoot's own USB stack remained a dead end; the successful approach preserved the working USB bridge and called only the required original NAND/FTL functions.

## Core rule

**Validate every repair through the same software layer that normal boot actually uses.**
