# Address spaces and units

The same number can refer to different layers. Establish the layer before
comparing bytes or interpreting a historical target.

| Term | Meaning in this investigation |
|---|---|
| Physical NAND block | An erase unit on the chip; 2 MiB on the reference unit |
| Global logical FTL block | A 2-MiB block in the translation layer's logical space; its physical owner can change |
| Partition-relative offset | A byte offset from the start of a partition, after FTL translation |
| Logical sector | 512 bytes; `parameter` lengths/starts use hexadecimal sector counts |
| Native page | 8 KiB main data; 256 pages per physical block on this unit |
| raw528 / RS record | Transport: 512 main bytes plus 16 auxiliary bytes; not a linear partition image or complete physical OOB dump |
| Native auxiliary u16 | The two meaningful auxiliary bytes per investigated 528-byte record in the normal ECC40 path; remaining bytes are not exported ECC parity |
| IDB boot-order page | A page selected through ECC24/MLC low-page ordering, not interchangeable with a linear ECC40 read |
| mode0 / mode1 | The investigated early/full FTL views; equality must be measured, not assumed |

## Interpreting the system-repair table

The [observed partition map](FIRMWARE_REFERENCE.md) starts system at sector
`0xBA000`. With 4096 sectors per 2-MiB logical block, that is global logical block
186. The repaired numbers **192, 195, 198 and 204 are global logical FTL blocks**,
not block indexes within system and not physical NAND owners.

```text
system-relative offset of global logical block 192
  = (192 - 186) * 2 MiB
  = 12 MiB
  = 12,582,912 bytes
```

This explains one recorded layout. Other firmware versions and hardware states
must be inspected independently. Complete device-specific FTL maps are omitted;
selected owners and map changes are retained where they explain a finding.
In the cache results, logical 24 changed owner 52 to 1056 and logical 26 changed
owner 948 to 1052. These are historical observations, not targets for another unit.
