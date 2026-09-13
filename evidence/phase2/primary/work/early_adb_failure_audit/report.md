# Offline early ADB failure audit

No hardware or USB calls. No boot/NAND image changes.

Audited fixed boot SHA256: `3e9556dc6195a7d6616685f9d58a439c23fe55dbe760ba9254f4d233ba79df0f`.
Its kernel is byte-exact to the reference kernel: 6,971,428 bytes, SHA256 `af7e01d68227df6f1936b3bd35fac398e0f7f5be1a42060dfb713a196013963f`.

## Concrete code finding

`dwc_otg_pcd_check_vbus_timer` at `0xc06a4fcc` reads hardware status at virtual address `0xfed0815c` (GRF offset `0x15c`). With gadget pullup requested, connection work is scheduled only when status bits **20 and 17 are both set**. The actual ARM replay in `timer_arm_proof.json` verifies all eight combinations of the two status bits and the pullup request. No USB controller is emulated; external kernel function calls are fixtures.

`force_usb_mode_store` at `0xc069f4ec` changes the core's forced role; the timer above still tests raw status and never reads that forced-role setting. Consequently, **force mode 2 plus gadget enable does not guarantee enumeration**: either raw status bit remaining zero prevents the connection work. This is a specific unhandled condition in the diagnostic setup. Whether it occurred during the failed Linux boot is not yet measured.

The stock kernel's `enable_store` at `0xc06b53f4` directly requests gadget pullup after adding the USB configuration. `adb_open` at `0xc06ad2ac` only handles its exclusive-open/error state; `adb_function_bind_config` does not wait for adbd. Thus a missing/late adbd process alone does not explain the complete absence of USB enumeration in this kernel.

## Entire ramdisk import review

All 30 CPIO entries were inspected; text is preserved in `ramdisk_texts.txt`. With `ro.hardware=rk30board`, the import chain is `init.rc` → `init.rk30board.rc` → `init.rk30board.usb.rc`, plus `init.trace.rc`. The separate `init.usb.rc` is present but not imported.

The inserted early ADB commands belong to the existing `on init` action and precede `on fs`, NAND module insertion and the synchronous mountfs script. There is one adbd service; the original static adbd/busybox executables remain unchanged. The board's duplicate `sys.usb.config=adb` action switches the ID to `2207:0006`, then enables the gadget and starts adbd. It does not force host mode or leave USB disabled. The active host_pwr and persisted-config handlers redirect to adb. The explicit stop path is `sys.usb.config=none`, which requires a later property change.

**No deterministic init/import error that necessarily disables this candidate was found.** Neither USB VID changes nor the stock-header checksum failure should be reused as explanations: the header was already corrected, and Windows looked for all devices.

## Next discriminating evidence

The useful evidence is whether Linux reaches the early block, its sysfs write errors, and the actual role/VBUS/gadget state. Search any preserved kernel log for `force_usb_mode_store`, `vbus detect`, `soft connect`, and `USB RESET`. If a Linux-side observation becomes available, read `force_usb_mode`, `vbus_status`, platform USB `mode`, and android0 `enable/functions/state`; raw GRF status would distinguish the timer condition directly. A MaskROM status value alone does not establish the earlier Linux state.

Rockchip's primary USB application note separately documents VBUS state, connection enable, and role forcing in sections 3.2, 3.4 and 3.6: [RK USB Application Note v2.0](https://www.haoyuelectronics.com/service/RK3066/Docs/RK%20USB%20Application%20Note_V2.0%20%28chinese%20Language%29.pdf). The exact bit-level finding above comes from the candidate kernel itself.
