# Final publication review — 2026-09-12

## Input and scope

The supplied English archive was opened and ZIP CRC checked. Its SHA-256 matched
`179e7ff734e263e50b37b1e21ea254af72fb3a7e85f7f97825735603c75dbf22`.
Both sanitized source archives were also opened and CRC checked. The definitive
public handoffs were used to qualify the consolidated technical conclusions.
No device was connected; no archived repair program was executed.

## Findings corrected

1. A recovery-image SHA-256 had lost one character in two documentation tables.
   It was recomputed from the supplied recovery ZIP member, not guessed from the
   malformed text: `951d8777eaed7eca15de2cc65c3ebd488e4f977b17c698ae9906c36b1761f042`.
2. The previous evidence guide linked conceptually to a missing phase-1 directory.
   Thirty-seven sanitized source records are restored with only their editorial
   interpretation translated. All remaining JSON fields compare equal.
3. The English summary omitted the late warning about unguarded USBplug init
   reaching a destructive geometry probe. It is now prominent in the safety and
   technical documents. A RAM download is not a promise of no persistent writes.
4. Causal overstatements were narrowed: different boot FTL mappings were observed,
   but the timing/cause of every later system defect is not established.
5. Final binary readback, cold functional confirmation and the preceding save-import
   test are separated. Remaining unclassified startup diagnostics are retained.
6. An acquisition script that uses the network was moved out of `toolkit/offline`.
   Synthetic tests moved to `tests/`; no historical repair source was changed.
7. Broken evidence filename references, inaccurate omission text and phase dates
   were corrected. Documentation and evidence now have navigable indexes.
8. Manifest verification now detects missing, altered and extra files; malformed,
   duplicate and traversal paths are rejected. Both manifest formats must agree.
9. `.gitattributes` preserves archival CRLF/LF bytes across Git checkouts. Root-only
   ignores for local `work`/`outputs` do not hide archived folders with those names.
10. GitHub CI is limited to publication checks and synthetic tests, with pinned
    action commits and read-only permissions. No hosted run was performed here.

## Checks actually performed

- Every included file read as UTF-8; JSON parsed and maintained Python syntax checked.
- Every included historical source snapshot compared byte-for-byte with the English
  input: **456 preserved**. Snapshot headers remain deliberately non-executable.
- Relative Markdown links and catalog targets checked, including manifest coverage.
- Automated scans for Cyrillic/CJK prose, chat artifacts, private-key/token patterns,
  absolute personal host paths and excluded binary/private artifact extensions.
- Public upstream notices retained; their author attributions are not device-owner
  information and were not removed.
- **32 synthetic tests passed**: digest checks, CLI behavior, manifest failure cases,
  and mocked package downloads. No firmware, device or live network used by tests.
- Local Git staging/checkout and final ZIP re-extraction are checked during packaging.
  Their exact outcomes are recorded in [VALIDATION_LOG.txt](VALIDATION_LOG.txt).

## External attribution check

The Sui Lab article, hissorii repository, nosuke diary, Duddyfinger article,
CYBER Gadget update page, RetroFreak Toolkit, published BootROM gist and archival
collection pages were retrievable during review. The old 5ch thread was not;
its attribution is retained from the research record and explicitly marked as
not newly verified. No claim is made that every historical external download or
license-notice URL is live or that downloaded third-party binaries were scanned.

## Limits

This audit validates the publication, not another repair of an RF-1. It does not
certify all archival code as safe, reproduce missing private-data tests, establish
full chip health, or assign a repository-wide license. The exact file counts and
hashes are in `MANIFEST.json`, `toolkit/INDEX.json` and `evidence/INDEX.json`.
