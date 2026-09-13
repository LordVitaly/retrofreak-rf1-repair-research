# Offline boot-ID checker

`rf1_boot_digest.py` computes the observed RF-1 vendor boot ID for a local image.
It opens the input read-only, does not patch it and has no USB or network code.
It supports only the validated legacy ANDROID! variant: 16384-byte page,
nonempty kernel/ramdisk, no second payload, dt_size=unused=0.

```sh
python toolkit/offline/rf1_boot_digest.py /path/to/local/boot.img
```

Exit status: `0` = supported image and matching ID, `1` = supported image with
mismatching ID, `2` = unreadable or unsupported input. A matching ID is not a
signature/authenticity test or permission to flash. Partition tails are reported
but excluded from the observed digest.

This helper was extracted for publication from the documented formula; it is not
claimed to be the device-side historical verifier. Its tests use synthetic bytes:

```sh
python -B -m unittest discover -s tests -v
```

The [technical report](../../docs/TECHNICAL_REPORT.md) gives the formula and the
scope of validation against the original ARM verifier during the repair.
