# Synthetic tests

Run from the repository root with Python 3.10 or newer:

```sh
python -B -m unittest discover -s tests -v
```

These tests cover the standalone boot-ID checker, metadata integrity and the
optional package downloader (mock responses only). Fixtures are created in
system temporary directories and removed afterward. No firmware, USB/ADB device,
raw disk, network service, or historical writer is used.

Historical tests inside `.txt` source snapshots are **not** part of this suite.
Their hardware claims remain limited to the included repair evidence.
