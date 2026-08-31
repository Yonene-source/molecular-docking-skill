#!/usr/bin/env python3
"""Exercise manifest and ZIP release invariants without network or scientific compute."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path


ARCHIVE_ROOT = "molecular-docking-skill"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def run(command: list[str], cwd: Path, expect_success: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )
    if expect_success and result.returncode != 0:
        raise RuntimeError(result.stdout + result.stderr)
    if not expect_success and result.returncode == 0:
        raise RuntimeError("command unexpectedly succeeded: " + " ".join(command))
    return result


def copy_skill(source: Path, destination: Path) -> None:
    def ignore(_directory: str, names: list[str]) -> set[str]:
        return {
            name for name in names
            if name in {".git", "__pycache__"} or name.endswith(".pyc")
        }

    shutil.copytree(source, destination, ignore=ignore)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill-root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    source = args.skill_root.resolve()

    with tempfile.TemporaryDirectory(prefix="molecular-docking-release-contract-") as temp_name:
        temp = Path(temp_name)
        skill = temp / "skill"
        copy_skill(source, skill)

        git_metadata = skill / ".git"
        git_metadata.mkdir()
        (git_metadata / "config").write_text(
            "credential = MUST_NOT_PACKAGE\n",
            encoding="utf-8",
        )

        python = sys.executable
        run([python, "scripts/build_publication_manifest.py", "--skill-root", "."], skill)
        validated = run(
            [python, "scripts/validate_portable_skill.py", "--skill-root", ".", "--require-manifest"],
            skill,
        )
        validation = json.loads(validated.stdout)
        if validation.get("status") != "PASSED":
            raise RuntimeError("portable validation did not pass")

        output_a = temp / "release-a"
        output_b = temp / "release-b"
        for output in (output_a, output_b):
            run(
                [
                    python,
                    "scripts/package_release.py",
                    "--skill-root",
                    ".",
                    "--output-dir",
                    str(output),
                    "--release-id",
                    "v0.1.0",
                ],
                skill,
            )

        archive_name = "molecular-docking-skill-v0.1.0.zip"
        sidecar_name = "molecular-docking-skill-v0.1.0.manifest.json"
        archive_a = output_a / archive_name
        archive_b = output_b / archive_name
        if sha256_file(archive_a) != sha256_file(archive_b):
            raise RuntimeError("deterministic ZIP hashes differ")

        sidecar = json.loads((output_a / sidecar_name).read_text(encoding="utf-8"))
        with zipfile.ZipFile(archive_a) as handle:
            members = handle.namelist()
            if any("/.git/" in name or "/__pycache__/" in name or name.endswith(".pyc") for name in members):
                raise RuntimeError("forbidden metadata entered ZIP")
            if f"{ARCHIVE_ROOT}/LICENSE" not in members:
                raise RuntimeError("LICENSE missing from ZIP")
            actual_member_hashes = {
                name: sha256_bytes(handle.read(name))
                for name in members
            }
        if sidecar.get("member_sha256") != actual_member_hashes:
            raise RuntimeError("sidecar member hashes do not match ZIP")

        readme = skill / "README.md"
        readme.write_text(readme.read_text(encoding="utf-8") + "\nStale manifest test.\n", encoding="utf-8")
        stale = run(
            [
                python,
                "scripts/package_release.py",
                "--skill-root",
                ".",
                "--output-dir",
                str(temp / "stale-release"),
                "--release-id",
                "stale-test",
            ],
            skill,
            expect_success=False,
        )
        if "stale PUBLICATION_MANIFEST.json" not in stale.stdout + stale.stderr:
            raise RuntimeError("stale manifest failed for an unexpected reason")

        payload = {
            "schema_version": "molecular_docking_release_contract_test_v1",
            "status": "PASSED",
            "checks": {
                "git_metadata_excluded": True,
                "portable_validation": validation["status"],
                "deterministic_zip": True,
                "zip_member_sha256": True,
                "license_packaged": True,
                "stale_manifest_rejected": True,
            },
            "archive_sha256": sha256_file(archive_a),
            "member_count": len(sidecar["member_sha256"]),
            "scope_note": "Offline package test only; no docking, MD, free energy, API, download, or installation.",
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
