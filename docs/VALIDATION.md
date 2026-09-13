# Validate this publication

This is a script-and-documentation research archive, not an installable flasher
package. The maintained helpers use Python's standard library; no package install
or device connection is needed for the checks below.

From the repository root, using Python 3.10 or newer:

```sh
python -B scripts/check_repository.py
python -B -m unittest discover -s tests -v
python -B scripts/verify_manifest.py
```

The repository check reads every included file, checks text/JSON/Python syntax,
relative Markdown links, indexes, excluded artifact types, basic private-data
patterns and byte preservation of the historical source snapshots. The manifest
check detects modified, missing **and unlisted** publication files and requires
both checksum formats to agree. Git internals and normal Python environment/cache
directories are intentionally excluded from file enumeration.

These are bounded publication/privacy checks, not a guarantee of secret detection,
a malware scan of external installers, or hardware validation of archived writers.

## After intentional edits

Review the diff first, especially changes to evidence and source snapshots. Then:

```sh
python -B scripts/refresh_metadata.py --date 2026-09-12
python -B scripts/check_repository.py
python -B -m unittest discover -s tests -v
```

Set the date to the publication revision being built. Refreshing metadata changes
only the two indexes, file list and two manifests; it does not rewrite source
snapshots or access devices. It must not be used to bless unexplained data changes.
The manifests exclude themselves to avoid recursive hashes; a separately supplied
ZIP SHA-256 covers the complete delivered archive.

## Git and line endings

`.gitattributes` fixes maintained text to LF and leaves archival snapshots and
upstream notices byte-preserved, including their original CRLF where present.
This prevents a checkout from changing archived bytes and invalidating manifests.

## CI scope

The included GitHub Actions workflow runs only these local checks and synthetic
tests. It uses read-only repository permissions and pinned action commits. It
never builds or executes historical writers, downloads vendor firmware, or
accesses hardware. Local checks were run during packaging; a hosted GitHub run
requires the repository to be uploaded and has not happened as part of this review.
