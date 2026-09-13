# Read-only validation of the 8 GB recovery microSD

Date of the original validation: 2026-09-02.

## Partition layout

The removable 8 GB card used MBR and contained the same three partition offsets/sizes as the source recovery IMG:

| # | Type | Offset | Size |
|---:|---|---:|---:|
| 1 | FAT32 / `0x0B` | 1,048,576 | 178,257,920 |
| 2 | Linux / `0x83` | 180,956,160 | 8,225,280 |
| 3 | Linux / `0x83` | 189,181,440 | 8,225,280 |

The visible FAT partition contained `retrofreak-system-update.img`, 152,708,368 bytes, matching the source `UPDATE.IMG` by size and SHA-256. Only the filename had been changed.

## Source image

`boot-recovery-SD-fullreset-v0.2.2.img`

- size: 199,229,440 bytes
- MD5: `ae6161ce2a291691575a710659ff07a6`
- SHA-1: `5ba6a0a5a08c73b4fa060b1e413bd30155762b08`
- SHA-256: `951d8777eaed7eca15de2cc65c3ebd488e4f977b17c698ae9906c36b1761f042`
- MBR signature: `55 AA`
- magic at offset 0: `RETRON5___BOOTSD`

Partition 2 is an ext filesystem labelled `data` and contains `/bootscript.sh`; partition 3 is labelled `cache`.

The original bootscript requests recovery reboot.

## Marker test

For diagnosis, `/data/bootscript.sh` was replaced by a same-size script that first created `/data/R`, synced, and then requested recovery reboot. The modified partition image was written and read back exactly.

After controlled cold/warm boot attempts:

- the RF-1 still showed the original failure;
- the partition-2 SHA-256 remained unchanged;
- `/R` was absent;
- no persisted marker was observed.

The marker result does not by itself prove that the script was never entered or that its write succeeded. The added sync request does not independently demonstrate a successful persistent write.

## Conclusion

The recovery card itself was consistent with the source image. A failure before or within the BOOTSD/bootscript path was suspected: the branch might not have been selected, the SD block device might have been unavailable, or the marker might not have been written successfully. The available observations do not isolate one exclusive cause.

Repeated edits to the FAT/ext partitions did not resolve the observed failure; the marker test did not establish a dead SD slot.
