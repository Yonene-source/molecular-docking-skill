#!/usr/bin/env python3
"""Build a clean ZIP and adjacent manifest from a validated Skill tree."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from datetime import datetime, timezone
from pathlib import Path


MANIFEST_NAME = "PUBLICATION_MANIFEST.json"
ARCHIVE_ROOT = "molecular-docking-skill"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def included_files(root: Path) -> list[Path]:
    return sorted(
        path for path in root.rglob("*")
        if path.is_file()
        and ".git" not in path.parts
        and "__pycache__" not in path.parts
        and path.suffix != ".pyc"
    )


def verify_publication_manifest(root: Path) -> None:
    manifest_path = root / MANIFEST_NAME
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError) as exc:
        raise SystemExit(f"invalid {MANIFEST_NAME}: {exc}") from exc
    declared = manifest.get("files") if isinstance(manifest, dict) else None
    if not isinstance(declared, dict):
        raise SystemExit(f"invalid {MANIFEST_NAME}: files must be an object")
    actual = {
        path.relative_to(root).as_posix(): sha256(path)
        for path in included_files(root)
        if path.name != MANIFEST_NAME
    }
    if declared != actual:
        raise SystemExit(
            f"stale {MANIFEST_NAME}; regenerate and validate it before packaging"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--release-id", required=True, help="Safe filename token such as 20260828-183000")
    args = parser.parse_args()
    root = args.skill_root.resolve()
    output_dir = args.output_dir.resolve()
    if not (root / MANIFEST_NAME).is_file():
        raise SystemExit(f"missing {MANIFEST_NAME}; build and validate it first")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", args.release_id):
        raise SystemExit("--release-id contains unsupported characters")
    verify_publication_manifest(root)
    output_dir.mkdir(parents=True, exist_ok=True)
    archive = output_dir / f"molecular-docking-skill-{args.release_id}.zip"
    sidecar = output_dir / f"molecular-docking-skill-{args.release_id}.manifest.json"
    if archive.exists() or sidecar.exists():
        raise SystemExit("release output already exists; choose a new release id")

    files = included_files(root)
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as handle:
        for path in files:
            relative = path.relative_to(root).as_posix()
            info = zipfile.ZipInfo(f"{ARCHIVE_ROOT}/{relative}", date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            handle.writestr(info, path.read_bytes())

    payload = {
        "schema_version": "molecular_docking_skill_release_manifest_v1",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "release_id": args.release_id,
        "archive": archive.name,
        "archive_root": ARCHIVE_ROOT,
        "archive_size_bytes": archive.stat().st_size,
        "archive_sha256": sha256(archive),
        "publication_manifest_sha256": sha256(root / MANIFEST_NAME),
        "file_count": len(files),
        "files": [path.relative_to(root).as_posix() for path in files],
        "member_sha256": {
            f"{ARCHIVE_ROOT}/{path.relative_to(root).as_posix()}": sha256(path)
            for path in files
        },
        "license": "MIT",
        "exclusions": [".git/", "__pycache__/", "*.pyc"],
    }
    sidecar.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASSED", "archive": str(archive), "manifest": str(sidecar), "file_count": len(files)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
