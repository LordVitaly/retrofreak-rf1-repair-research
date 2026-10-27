# Community case #1: RF-1 splash hang with working recovery

**Reported solved on 2026-10-27 by [Yamanotsume on GitHub](https://github.com/Yamanotsume)
/ [u/yamanotsume on Reddit](https://www.reddit.com/user/yamanotsume/).** Thank you
for testing a recovery route on a second RF-1 and sharing the steps, hashes and
hardware observations for future repairers.

Primary source: [issue #1](https://github.com/LordVitaly/retrofreak-rf1-repair-research/issues/1),
especially the author's [successful-repair report](https://github.com/LordVitaly/retrofreak-rf1-repair-research/issues/1#issuecomment-6445589262).
The author also documented the result in the [original Reddit thread](https://www.reddit.com/r/retron5/comments/1w2g6rc/original_retro_freak_2016_stuck_on_logo_any_way/)
([linked comment](https://www.reddit.com/r/retron5/comments/1w2g6rc/comment/19rqjk118t3kz/)).
This page summarizes that report; it is not an independent maintainer hardware test.

## Which case this covers

The second unit was an early RF-1 bought in 2016 and stuck on the Retro Freak
splash screen. **Recovery System v1.1 was reachable via microSD.** Factory reset,
cache wipe and earlier recovery-SD attempts had not restored normal startup.

The original unit in this repository had a white screen and unreliable power
hold, and recovery was no longer being reached during the successful repair.
That forced the [deeper diagnostic and repair path](SUCCESSFUL_RECOVERY_PATH.md)
through MaskROM, boot-chain/NAND/FTL investigation and filesystem repairs. The
recovery-menu method below cannot be followed when that menu is unavailable.
See the [decision tree](DECISION_TREE.md) for the two access conditions.

## Preconditions and write scope

- Working SD recovery with **Update rkimage from external storage** available.
- A matching official update; the reported case used system software 0.2.0.
  Its extracted manifest listed `SYSVER=0.2.0` and `SUPPORTED_PCBA=0x6,0x2`.
  This is not evidence of compatibility with every Retro Freak revision.
- Preservation of accessible saves/settings and acceptance of the update's write
  scope before proceeding. This is a firmware update: the owner reports writes
  and verification of boot, system, backup, recovery and bootloader. Preservation
  of all userdata was not established.
- Stable power throughout the update. If the matching image cannot be established,
  recovery cannot be reached, or the update fails, stop and collect evidence
  before attempting another write; the report does not establish a retry method.

Read [Safety and scope](SAFETY_AND_SCOPE.md). Low-level RAM-loader access is not
required by this SD-recovery sequence and must not be assumed read-only.

## Sequence reported by the owner

1. Obtain `RetroFreak-SystemUpdate-0.2.0.zip`. Its
   `retrofreak-system-update.img` is the encrypted outer Retro Freak container.
   The owner reports the same outer-image SHA-256 as our [reference](REFERENCE_HASHES.md).
2. Extract it with `RetroFreak.py` from
   [GoobyCorp's RetroFreak Toolkit](https://github.com/GoobyCorp/RetroFreak_Toolkit).
   The reported output included `manifest.txt` and
   `update-RetroFreak-0.2.0-v2.img`, a plain Rockchip RKFW/RKAF image.
3. Write the RetroN 5 `boot-recovery-SD-fullreset-v0.2.2` image to a microSD,
   then replace `update.img` on its FAT partition with the extracted plain
   Rockchip image, renamed to `update.img`. Preparing the SD overwrites its
   existing contents. See [recovery-SD provenance](RECOVERY_SD.md) for the source.
4. Boot with the SD, enter **Recovery System v1.1**, and select
   **Update rkimage from external storage**. The owner reports verification of
   boot, system, backup, recovery and bootloader, followed by
   **Update rkimage complete**.
5. After completion, remove the SD and reboot. The owner reports normal startup
   for the first time since 2016 and closed the issue as solved.

The distinction is the encrypted outer update versus the extracted plain
Rockchip image accepted by this recovery option. Renaming the encrypted file
alone does not perform that extraction. This report is separate from a
`Wipe data/factory reset` operation, which had already failed to solve this unit.

## Reported image identity and validation limits

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| Encrypted `retrofreak-system-update.img`, reported matching our reference | 173,429,248 (reference size) | `10ddc9babb5878f975eee7bce1324dc6b0691e9f76dac188c82589226409a9ff` |
| Extracted `update-RetroFreak-0.2.0-v2.img`, reported by the owner | 173,428,496 | `8be4cfc8cd92f03cefae48dee8b2e42ea1f44b7bd0988e1d1b5741dad28ead9a` |

The owner also reports that the contained `system.img` and `boot.img` match our
reference hashes. These values are attributed to the issue; the maintainers did
not reacquire or rehash this owner's files. No vendor firmware is redistributed.

Normal startup and recovery's update/verification messages are owner-reported
observations. This case does not establish full post-update NAND readback,
power-removal cold persistence, cartridge/peripheral tests, NAND endurance or
success on every hardware revision. It does not independently reproduce our
original low-level repair. Additional MaskROM, NAND geometry and unconfirmed UART
observations remain available in the author's full issue report.
