# Sources and credits

The recovery did not begin from a blank slate. Several earlier public discoveries were essential.

## Critical starting points

### Ken — Sui Lab

**Article:** “Recovering a broken Retro Freak”  
https://sui-lab.info/archives/3342

Published 2021-01-04. This article documented applying the RetroN 5 full-reset recovery SD image to Retro Freak, reaching recovery mode and using `Wipe data/factory reset`. It was the practical reference that motivated the initial recovery attempt in this case.

### Anonymous 5ch contributor `f0xHXxH1`, post #10

**Thread:** Retro Freak CFW analysis thread  
https://medaka.5ch.io/test/read.cgi/gameurawaza/1447594308

Post #10, 2015-11-16 01:07:01, described a hidden switch near the left USB port, visible through the opening, and connecting the opposite USB port to a PC while holding the switch as power is applied. The reference RF-1 later confirmed that this sequence exposes the RK3066 service path as Rockchip MaskROM (`2207:300A`).

This attribution is preserved from the research-session reference record. The
thread could not be fetched again by the final review browser on 2026-09-12, so
the post number/handle/time are not presented as newly verified. The retained
record describes a switch and PC connection, not an explicit MaskROM label;
MaskROM identification came from the separate hardware observation. No archive
of the complete thread or third-party photographs is redistributed here.

## Foundational Retro Freak reverse engineering

### hissorii — `retrofd`

https://github.com/hissorii/retrofd

Foundational work on Retro Freak Android/SD boot behavior, root/ADB, the right-side USB/OTG role and the `mountfs.sh -> /data/bootscript.sh` chain. This work established much of the public vocabulary for modifying and observing the platform.

### nosuke — RetroN 5 / Retro Freak hacking diary

https://www.dentsubo.net/~nosuke/diary/diary.php?d=0&m=10&n=0&y=2017

Useful experiments involving `RETRON5___BOOTSD`, SD boot behavior and recovery/bootscript paths.

### Duddyfinger — independent Retro Freak repair case

https://ameblo.jp/duddyfinger/entry-12856374336.html

A later independent example of using the RetroN 5 full-reset recovery image on a faulty Retro Freak, showing that the method was not unique to a single earlier case.

## Official / firmware references

### CYBER Gadget

- Update history: https://cybergadget.co.jp/support/retrofreak/update/
- English update instructions: https://cybergadget.co.jp/support/retrofreak/en/update.html
- Product site: https://cybergadget.co.jp/retrofreak/

Used to cross-check application/system versions and official update behavior.

### GoobyCorp — RetroFreak Toolkit

https://github.com/GoobyCorp/RetroFreak_Toolkit

Public reference for the encrypted Retro Freak update container and the nested Rockchip firmware/package structure.

## Rockchip / low-level references

### Rockchip `rkdeveloptool`

https://github.com/rockchip-linux/rkdeveloptool

Protocol, RKBoot container and command-layout reference. Upstream code is not redistributed by this archive unless separately covered by its own license/notice.

### Rockchip U-Boot `boot_merger.c`

https://github.com/rockchip-linux/u-boot

Reference used when comparing old Rockchip boot-container handling.

### RK3066 BootROM publication by `dw`

https://gist.github.com/dw/9300925

Used as an external BootROM reference during USB length/control-flow research. The exact ROM revision was **not** proven identical to the RF-1's internal ROM, so conclusions derived from it were treated as bounded evidence rather than device truth.

## Filesystem references

Linux ext4 documentation was used to interpret on-disk error fields and structures:

https://www.kernel.org/doc/html/latest/filesystems/ext4/

`e2fsprogs`/`e2fsck` were used for offline and on-device filesystem checks; see `third_party/` for preserved notices and version metadata.

## RetroN 5 recovery image provenance

The historical full-reset package was distributed from:

`http://www.retron5.in/downloads/boot-recovery-SD-fullreset-v0.2.2.zip`

The old site is not reliably available today. A public archival collection exists at:

https://archive.org/details/retron-5

No third-party recovery image is redistributed in this repository.
