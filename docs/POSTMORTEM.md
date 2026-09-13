# Postmortem: dead ends, mistakes and high-value lessons

## 1. Recovery was useful, but not sufficient

The RetroN5-derived recovery image was a valuable first path and did reach Retro Freak Recovery System v1.1 once. Factory reset did not repair this unit, and later marker tests produced no persisted marker. This supported investigating an earlier BOOTSD-selection failure, but did not independently exclude an unsuccessful marker write. Repeated SD modifications did not resolve the observed failure.

## 2. The first raw NAND interpretation was too simple

`RS` returned 512+16-byte records. Treating those records as a normal linear partition image produced misleading comparisons. The IDB boot path also required ECC24 and MLC low-page ordering, while normal data used an ECC40 path.

## 3. Swapping similar RAM loaders did not change the result

The official loader, v1.24 and v2.15 returned the same low-level data in the tested region. Loader version hunting was therefore not a solution.

## 4. Full FlashBoot USB startup became an expensive detour

A large amount of effort went into transporting FlashBoot into RAM, reconstructing startup state, and localizing why its own USB stack failed. The decisive simplification was to **keep the already-working USB bridge** and call only the original NAND/FTL functions that were needed.

## 5. Emulation helped, but full-platform emulation was not the goal

Unicorn/ARM replay was valuable for testing arithmetic, guards, call flow and FTL behavior. Extending the model toward complete RK3066 timers/UART/MMIO consumed effort without proving hardware startup. Narrow emulation with explicit stop conditions was more productive.

## 6. A successful write/readback can still be the wrong view

A full official system image was written and read back exactly through the diagnostic FTL path, yet later Linux reads exposed four corrupted blocks. Different physical boot owners were directly measured in mode0 and mode1. It remains unproven when and how each later system defect arose; attributing all of them to the earlier writer or to mapping selection would overstate the evidence.

**Rule: verify through the layer that will actually consume the data.**

## 7. Host-side assertions can be wrong

Several operations stopped because a host expectation was stale or too strict:

- wrong expected USB mode label;
- stale FTL map baseline;
- malformed expectation of `id` output;
- cached read state producing a false failure for address zero;
- terminal completion messages lost after data had already been read correctly.

These failures were not automatically device failures and must not trigger blind rewriting.

## 8. The vendor boot ID mattered

Changing the ramdisk while preserving the old Android boot ID produced an image that was written correctly but rejected by the original FlashBoot verifier. The real verifier, not a generic Android assumption, became the authority.

## 9. Fix the source of metadata corruption, not only the symptom

Repairing BBT12 alone was not persistent while the early geometry/FlashInfo path could regenerate invalid metadata. The durable repair restored the original IDB0/geometry path and then BBT.

## 10. RAM-loaded code can still write persistent storage

The old unguarded USBplug initialization included a destructive geometry probe.
A DB transfer itself targets RAM, but execution can immediately reach NAND writes.
Likewise some FTL reads allocate metadata. Claiming an entire session read-only
from its host command names was too strong. Guard coverage, native call counters,
explicit error statuses and fresh readback are separate evidence.

## 11. Filesystem repair was safer than formatting

The userdata failure was resolved by backup + offline trial + stock `e2fsck` on an unmounted partition. A full format was unnecessary and would have destroyed salvageable content.
