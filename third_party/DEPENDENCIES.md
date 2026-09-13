# External dependencies and provenance

Third-party binaries, vendor firmware and complete upstream source trees are not redistributed by this archive. The items below describe dependencies observed in the preserved research scripts.

## Development / analysis tools

| Dependency | Observed use | Upstream |
|---|---|---|
| Zig | 0.14.1; ARM freestanding/Cortex-A9 builds | https://ziglang.org/download/0.14.1/ |
| LZMA SDK | 26.03; RAM bootstrap experiments | https://www.7-zip.org/sdk.html |
| Unicorn | 2.1.4; ARM execution and hooks | https://github.com/unicorn-engine/unicorn |
| Capstone | ARM/Thumb disassembly | https://www.capstone-engine.org/ |
| pyelftools | ELF section/relocation inspection | https://github.com/eliben/pyelftools |
| dissect.extfs | read-only ext filesystem inspection | https://github.com/fox-it/dissect.extfs |
| pywinpty / WinPTY | automation of the old Rockchip console tool | https://github.com/andfoy/pywinpty |
| Rockchip Android Console Tool | historical Windows Rockusb console environment | external tool; no redistribution link asserted here |

## Upstream Rockchip source references

The investigation consulted Rockchip open-source material including `rkdeveloptool` and Rockchip U-Boot boot-merger logic. These upstream files are not copied into the archive merely because they were consulted.

- https://github.com/rockchip-linux/rkdeveloptool
- https://github.com/rockchip-linux/u-boot

## External BootROM reference

A published RK3066 BootROM listing was used for bounded USB length/control-flow experiments:

https://gist.github.com/dw/9300925

The ROM revision was not proven identical to the RF-1 internal ROM.

## Filesystem tools

The later repair used e2fsprogs/e2fsck and Cygwin packaging in a Windows host environment. Exact acquisition metadata and notices are preserved under `third_party/phase2/`.

## Android tools

Android platform-tools 37.0.1 were downloaded during the later investigation, but the successful ADB session used an older ADB environment after adding vendor ID `0x2207`. The repository does not claim that installing a newer driver/toolchain was required for success.

## Licensing

Each upstream component remains governed by its own license. See the preserved notice files under `third_party/phase2/notices/`.
