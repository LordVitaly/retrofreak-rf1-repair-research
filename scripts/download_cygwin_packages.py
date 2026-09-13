"""Download pinned Cygwin archives only. Never extract, install or execute them."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import urllib.parse
import urllib.request


def package_specs(manifest: dict) -> list[dict]:
    packages = manifest.get("packages")
    if not isinstance(packages, list) or not packages:
        raise ValueError("Manifest must contain a nonempty packages list")
    specs = []
    seen = set()
    for package in packages:
        if not isinstance(package, dict):
            raise ValueError("Each package must be an object")
        url = package.get("url", "")
        parsed = urllib.parse.urlsplit(url)
        if (parsed.scheme != "https" or not parsed.hostname or parsed.username
                or parsed.password or parsed.query or parsed.fragment):
            raise ValueError("Package URLs must be plain HTTPS URLs without credentials")
        name = parsed.path.rsplit("/", 1)[-1]
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._+~-]*\.tar\.(?:xz|zst)", name):
            raise ValueError("Unexpected package filename")
        if name in seen:
            raise ValueError("Duplicate package filename")
        seen.add(name)
        size, digest = package.get("bytes"), package.get("sha512", "")
        if type(size) is not int or size <= 0 or not re.fullmatch(r"[0-9a-fA-F]{128}", digest):
            raise ValueError("Each package needs a positive byte count and SHA512")
        specs.append({"name": name, "url": url, "bytes": size, "sha512": digest.lower()})
    return specs


def verified_file(path: Path, size: int, expected: str) -> bool:
    if not path.is_file() or path.stat().st_size != size:
        return False
    digest = hashlib.sha512()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest() == expected


def download_packages(manifest: dict, destination: Path) -> None:
    specs = package_specs(manifest)
    destination.mkdir(parents=True, exist_ok=True)
    root = destination.resolve()
    for spec in specs:
        target = root / spec["name"]
        if target.exists():
            if not verified_file(target, spec["bytes"], spec["sha512"]):
                raise ValueError("Existing destination file differs: " + spec["name"])
            print(json.dumps({"file": spec["name"], "status": "existing_verified"}))
            continue
        created = False
        try:
            # Exclusive creation: a pre-existing file is never overwritten.
            with target.open("xb") as output:
                created = True
                digest = hashlib.sha512()
                count = 0
                with urllib.request.urlopen(spec["url"], timeout=30) as source:
                    if urllib.parse.urlsplit(source.geturl()).scheme != "https":
                        raise ValueError("Download redirected away from HTTPS")
                    while True:
                        chunk = source.read(1024 * 1024)
                        if not chunk:
                            break
                        count += len(chunk)
                        if count > spec["bytes"]:
                            raise ValueError("Download exceeds pinned package size")
                        digest.update(chunk)
                        output.write(chunk)
                if count != spec["bytes"] or digest.hexdigest() != spec["sha512"]:
                    raise ValueError("Package size or SHA512 mismatch")
            print(json.dumps({"file": spec["name"], "status": "downloaded_verified"}))
        except BaseException:
            if created:
                target.unlink(missing_ok=True)
            raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path, help="Local portable_manifest.json")
    parser.add_argument("--dest", type=Path, required=True, help="Explicit download directory")
    args = parser.parse_args()
    try:
        download_packages(json.loads(args.manifest.read_text(encoding="utf-8")), args.dest)
    except (OSError, ValueError) as exc:
        print(json.dumps({"error": str(exc), "type": type(exc).__name__}))
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
