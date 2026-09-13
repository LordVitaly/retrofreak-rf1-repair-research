# Live Linux repair: offline review

No hardware/device commands were executed by this reviewer.

The narrowed repair of four verified bad 2 MiB system regions is preferable to rewriting the whole filesystem. It preserves the runtime superblock bytes and needs only 8 MiB of RAM staging. The root agent must use the measured offsets 12, 18, 24 and 36 MiB, corresponding to 4096-byte seeks 3072, 4608, 6144 and 9216, and exactly 512 blocks per region.

The locally retrieved BusyBox is static: 1,807,056 bytes, SHA256 `e9ad9c4e899984f68a960ee2302dc0db1bf34d60d3573d266d575825ab0a4ee5`; PT_INTERP/PT_DYNAMIC are absent. The original ramdisk adbd, init and e2fsck are also static ELF files. adbd's live maps still need to match the root agent's already observed RAM-only mapping; static linkage does not prove absence of open file descriptors or a cwd on a mounted filesystem.

## Critical unmount sequence

1. Stage and verify all four source files, scripts and required diagnostics first. Stop unrelated init services using ctl.stop before unmounting; an ordinary kill alone permits init to restart them.
2. Use one existing ADB shell which immediately replaces its dynamic executable with `exec /sbin/busybox sh /mnt/ram/script`. The script starts with `cd /` and invokes every utility through `/sbin/busybox` or the verified `/sbin/e2fsck`.
3. Unmount nested mounts first if any exist. Require a real successful unmount of `/system` and independently check its absence from `/proc/mounts`. Do not use lazy or forced unmount.
4. Only after confirming the system mount is absent, ensure the RAM-rootfs `/system/bin/sh` points to `/sbin/busybox`. If unmount failed, creating/replacing that link would modify the NAND filesystem, so the script must exit first. The existing ADB transport remains live; the link enables subsequent ADB shell launches.
5. `/data` similarly requires a real unmount before writable e2fsck. For EBUSY, inspect BusyBox fuser and `/proc/PID/{cwd,root,fd,maps}`; do not bypass the busy check. Keep adbd/ueventd/init only after their mappings, cwd and descriptors permit unmounting.

After the bounded writes, run sync before cache invalidation and comparison through newly opened read descriptors. BusyBox's blockdev applet was not found in the binary, so do not assume `blockdev --flushbufs` exists. Use O_DIRECT only if this exact dd advertises support; otherwise sync followed by `/proc/sys/vm/drop_caches=3` and reopening is the available kernel cache-clearing route. Compare each exact repaired region with its staged source, then remount system read-only and verify the formerly bad library bytes.

For unmounted `/data`, e2fsck exit 1 means errors were corrected; a script with unconditional `set -e` would misclassify that as failure. Handle exit codes explicitly: 0 clean, 1 corrected, 2 corrected/reboot needed; 4 or higher is not a successful repair. Require the complete verified data backup before this operation. Do not run writable e2fsck against the mounted data filesystem.
