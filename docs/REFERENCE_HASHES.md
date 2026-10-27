# Reference hashes

These hashes identify files used during the investigation. The corresponding vendor binaries are not redistributed here.

| Artifact | Size | SHA-256 |
|---|---:|---|
| Official Retro Freak update ZIP | 173,482,307 | `d285379b5a1367239a3368be7605bada253b2a2ca5e95a22872c331aa23293e8` |
| Encrypted update IMG | 173,429,248 | `10ddc9babb5878f975eee7bce1324dc6b0691e9f76dac188c82589226409a9ff` |
| Official `system.img` | 155,185,152 | `b9ca511124e6c3d9ee2a1e31220f6bf5a858f06d88f9003f5fd7f7e25cf5676a` |
| Early verified boot payload | 8,781,824 | `416c84c67be71e89d63530c1902112ebbe54845aca3e377a79506ce5c90b090d` |
| RetroN5 full-reset recovery IMG | 199,229,440 | `951d8777eaed7eca15de2cc65c3ebd488e4f977b17c698ae9906c36b1761f042` |

Official `system.img` MD5: `04130d8d95d155dc377569b06e750b4b`.

## Community-reported extracted update (2026-10-27)

In [issue #1's repair report](https://github.com/LordVitaly/retrofreak-rf1-repair-research/issues/1#issuecomment-6445589262),
Yamanotsume supplied the following identity for the plain Rockchip image used
through working recovery. The maintainers have not independently reacquired or
hashed this file; it is separate from the encrypted outer IMG above.

| Artifact | Size | SHA-256 |
|---|---:|---|
| Extracted `update-RetroFreak-0.2.0-v2.img` (owner-reported) | 173,428,496 | `8be4cfc8cd92f03cefae48dee8b2e42ea1f44b7bd0988e1d1b5741dad28ead9a` |

See [community case #1](COMMUNITY_RECOVERY_CASE_01.md) for prerequisites, the
reported sequence and validation limits.
