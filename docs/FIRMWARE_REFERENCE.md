# Official firmware reference used in the investigation

The reference update was independently inspected and matched CYBER Gadget's application 1.5 / system software 0.2.0 release, with GUI resource build 2764.

## Container chain

```text
RetroFreak-SystemUpdate-0.2.0.zip
  -> encrypted Retro Freak update container
  -> Rockchip RKFW
  -> RKAF package
  -> RetronLoader.bin / parameter / boot.img / recovery.img / system.img / update-script
```

The outer Retro Freak image is an encrypted container with signature fields,
not a raw disk image. ZIP CRC, the internal RKFW checksum and structural/version
consistency were checked in the source analysis. The outer RSA signatures were
**not independently verified**. Initial/final byte ranges and length matched an
official server response then available; a full independent server-file hash was
not obtained. These are strong provenance indicators, not a cryptographic claim
of vendor-signature verification.

## Reference package hashes

### ZIP

- size: 173,482,307 bytes
- SHA-256: `d285379b5a1367239a3368be7605bada253b2a2ca5e95a22872c331aa23293e8`

### Encrypted outer IMG

- size: 173,429,248 bytes
- SHA-256: `10ddc9babb5878f975eee7bce1324dc6b0691e9f76dac188c82589226409a9ff`

### Official system image

- size: 155,185,152 bytes
- SHA-256: `b9ca511124e6c3d9ee2a1e31220f6bf5a858f06d88f9003f5fd7f7e25cf5676a`
- MD5: `04130d8d95d155dc377569b06e750b4b`

### Verified boot payload extracted from NAND during the early investigation

- size: 8,781,824 bytes
- SHA-256: `416c84c67be71e89d63530c1902112ebbe54845aca3e377a79506ce5c90b090d`

The public repository does not redistribute these vendor binary images.

## RKBoot components observed in the official package

- `30_LPDDR2_300MHz_DD` — 10,352 bytes
- `rk30usbplug` — 56,520 bytes
- `FlashData` — 10,752 bytes
- `FlashBoot` — 110,080 bytes

## Android boot/recovery

Both images use `ANDROID!`, a 16 KiB page size, and the same Linux 3.0.8+ kernel build. Recovery contains `RetroFreak Recovery System v1.1`.

## Partition table from `parameter`

```text
misc      0x2000@0x2000
dummy1    0x2000@0x4000
boot      0x8000@0x6000
recovery  0x8000@0xE000
backup    0x2000@0x16000
cache     0x20000@0x18000
userdata  0x80000@0x38000
kpanic    0x2000@0xB8000
system    0x80000@0xBA000
user      0x27F000@0x13A000
```

Lengths and start addresses above are hexadecimal counts of 512-byte logical sectors. For this observed map, system begins at logical FTL block 186 (`0xBA000 / 4096`); block 192 is therefore 12 MiB into system. See [Address spaces](ADDRESS_SPACES.md).

This is the logical partition map. It must not be applied directly to physical NAND dump offsets without the correct FTL interpretation.
