# Public repository preparation - 2026-09-13

This edition prepares the English research archive for public GitHub publication.
No console was accessed and no hardware test was repeated during this work.

Input ZIP SHA-256:
`17cc53e67c50ba5a71c44f0d1810469ad6c290c9410dc756b78a91fcdccd9ed6`.

## Changes from the reviewed English archive

1. Removed four complete 1896-entry FTL arrays from the block24/block26 cache
   results. Computed public summaries retain their actual owner changes:
   logical 24: 52 to 1056; logical 26: 948 to 1052. Neither pair of maps was equal.
2. Replaced the 1458-entry protected-target list in the cache writer manifest
   with its count and an explicit omission note. It was not a bad-block list.
3. Added publication-checker regression coverage for complete numeric device maps
   and target lists. This extends a bounded scan, not a guarantee against secrets.
4. Qualified the recovery-SD marker inference: no persisted marker does not
   independently prove the script was never entered or its write succeeded.
5. Separated final cold-start observations from earlier save import and settings
   persistence. Original repair outcomes and unsuccessful attempts remain intact.
6. Added a reader-oriented landing README and an address-space reference.
7. At the maintainer's direction, licensed original code under MIT and original
   documentation under CC BY 4.0. Third-party rights and notices remain separate.

Historical source snapshots and upstream notices are byte-preserved. Three
selected JSON records were deliberately reduced as described above, rather than
silently treating full-device maps as public-safe. Existing command/status fields
in those records were not rewritten to imply a different hardware outcome.

The new manifests describe this publication edition. Earlier dated audit logs
are historical records, including their original test counts and license status.
