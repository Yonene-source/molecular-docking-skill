#!/usr/bin/env python3
"""Create the publication SHA256 manifest for an already finalized Skill tree."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


MANIFEST_NAME = "PUBLICATION_MANIFEST.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill-root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.skill_root.resolve()
    output = root / MANIFEST_NAME
    files = sorted(
        path for path in root.rglob("*")
        if path.is_file()
        and path != output
        and ".git" not in path.parts
        and "__pycache__" not in path.parts
        and path.suffix != ".pyc"
    )
    payload = {
        "schema_version": "molecular_docking_skill_publication_manifest_v1",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "manifest_excludes": [MANIFEST_NAME, ".git/", "__pycache__/", "*.pyc"],
        "file_count": len(files),
        "files": {path.relative_to(root).as_posix(): sha256(path) for path in files},
    }
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASSED", "manifest": str(output), "file_count": len(files)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
