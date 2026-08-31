#!/usr/bin/env python3
"""Validate the portable molecular-docking Skill without scientific compute."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


MANIFEST_NAME = "PUBLICATION_MANIFEST.json"
REQUIRED_FILES = [
    "SKILL.md",
    "README.md",
    "VALIDATION_REPORT.md",
    ".gitignore",
    "agents/openai.yaml",
    "references/MOLECULAR_DOCKING_RUNTIME_CONTRACT.md",
    "references/STATUS_AND_COMPLETION_PROTOCOL.md",
    "references/REPORT_FIGURE_AND_FILE_MAP_CONTRACT.md",
    "references/METHOD_POSITIVE_CONTROL_REPRODUCTION_CONTRACT.md",
    "references/PLANT_CONTEXT_AND_MD_FREE_ENERGY_GATE.md",
    "references/PORTABILITY_AND_VALIDATION.md",
    "references/DOCKING_ASSUMPTION_AND_USER_CHOICE_MATRIX.md",
    "references/docking_assumption_catalog.json",
    "scripts/profile_md_resources.py",
    "scripts/build_publication_manifest.py",
    "scripts/package_release.py",
    "benchmarks/portable_scenarios.json",
    "benchmarks/positive_control_asset_policy.json",
    "benchmarks/README.md",
]

REQUIRED_TOKENS = [
    "`PLAN`",
    "`EXECUTE`",
    "`AUDIT`",
    "`PACKAGE_VALIDATE`",
    "status: BLOCKED",
    "reason_code",
    "USER_DEFERRED",
    "whole-system 3D",
    "local 3D",
    "2D interaction map",
    "Production MD job count remains zero",
]

REQUIRED_SCENARIO_IDS = {
    "audit_small_molecule",
    "modified_peptide_fallback",
    "unknown_membrane_user_deferred",
    "md_parameterization_block",
    "no_gpu_capacity",
    "package_integrity",
    "coordinate_figure_delivery",
    "plan_side_effect_boundary",
    "canonical_assumption_status",
    "conditional_membrane_bounds",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def package_files(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file()
        and path.name != MANIFEST_NAME
        and "__pycache__" not in path.parts
        and path.suffix != ".pyc"
    )


def local_markdown_links(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    return [
        target
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text)
        if not re.match(r"^[a-z]+://", target)
    ]


def semantic_contract_errors(root: Path) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    skill = (root / "SKILL.md").read_text(encoding="utf-8")
    runtime = (root / "references" / "MOLECULAR_DOCKING_RUNTIME_CONTRACT.md").read_text(encoding="utf-8")
    matrix = (root / "references" / "DOCKING_ASSUMPTION_AND_USER_CHOICE_MATRIX.md").read_text(encoding="utf-8")
    status = (root / "references" / "STATUS_AND_COMPLETION_PROTOCOL.md").read_text(encoding="utf-8")
    catalog = json.loads((root / "references" / "docking_assumption_catalog.json").read_text(encoding="utf-8"))

    forbidden_plan_phrases = [
        "Before plan approval create",
        "Before plan approval, also create",
        "PLAN may run a reversible",
    ]
    for phrase in forbidden_plan_phrases:
        if phrase in skill or phrase in runtime or phrase in matrix:
            errors.append({"rule": "plan_is_read_only", "detail": f"forbidden phrase: {phrase}"})

    if "canonical field `assessment_status`" not in skill or "`assessment_status`" not in status:
        errors.append({"rule": "canonical_assumption_field", "detail": "assessment_status is not canonical"})
    if "`current_status`" in matrix:
        errors.append({"rule": "canonical_assumption_field", "detail": "matrix persists legacy current_status"})

    protocol = catalog.get("status_protocol") if isinstance(catalog, dict) else None
    expected_values = ["ASSESSED", "PARTIALLY_ASSESSED", "NOT_ASSESSED", "BLOCKED", "USER_DEFERRED"]
    if not isinstance(protocol, dict) or protocol.get("canonical_field") != "assessment_status":
        errors.append({"rule": "catalog_status_protocol", "detail": "catalog canonical field mismatch"})
    elif protocol.get("canonical_values") != expected_values:
        errors.append({"rule": "catalog_status_protocol", "detail": "catalog canonical values mismatch"})

    old_membrane_phrases = ["show at least two plausible model membranes", "两种合理假想膜"]
    catalog_text = json.dumps(catalog, ensure_ascii=False)
    for phrase in old_membrane_phrases:
        if phrase in matrix or phrase in catalog_text:
            errors.append({"rule": "conditional_membrane", "detail": f"unconditional phrase: {phrase}"})
    if "defensible bounds" not in runtime or "可辩护边界" not in catalog_text:
        errors.append({"rule": "conditional_membrane", "detail": "defensible-bound condition missing"})

    if re.search(r"status\s*:\s*BLOCKED_[A-Z_]+", "\n".join([skill, runtime, matrix, status])):
        errors.append({"rule": "status_reason_split", "detail": "compound blocked status remains"})
    return errors


def manifest_errors(root: Path, required: bool) -> list[dict[str, Any]]:
    path = root / MANIFEST_NAME
    if not path.is_file():
        return [{"error": "missing publication manifest"}] if required else []
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError) as exc:
        return [{"error": "invalid publication manifest", "detail": str(exc)}]
    declared = manifest.get("files") if isinstance(manifest, dict) else None
    if not isinstance(declared, dict):
        return [{"error": "publication manifest files must be an object"}]
    actual = {file.relative_to(root).as_posix(): sha256(file) for file in package_files(root)}
    errors: list[dict[str, Any]] = []
    if set(declared) != set(actual):
        errors.append({
            "error": "publication manifest file set mismatch",
            "missing_from_manifest": sorted(set(actual) - set(declared)),
            "extra_in_manifest": sorted(set(declared) - set(actual)),
        })
    mismatched = sorted(name for name in set(declared) & set(actual) if declared[name] != actual[name])
    if mismatched:
        errors.append({"error": "publication manifest hash mismatch", "files": mismatched})
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--require-manifest", action="store_true")
    args = parser.parse_args()
    root = args.skill_root.resolve()

    missing = [relative for relative in REQUIRED_FILES if not (root / relative).is_file()]
    broken_links: list[str] = []
    markdown_files = sorted(root.rglob("*.md"))
    for path in markdown_files:
        for target in local_markdown_links(path):
            target_path = (path.parent / target.split("#", 1)[0]).resolve()
            if target.split("#", 1)[0] and not target_path.exists():
                broken_links.append(f"{path.relative_to(root).as_posix()} -> {target}")

    forbidden = sorted(
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file() and ("__pycache__" in path.parts or path.suffix == ".pyc")
    )
    combined = "\n".join(path.read_text(encoding="utf-8") for path in markdown_files)
    missing_tokens = [token for token in REQUIRED_TOKENS if token not in combined]

    benchmark_path = root / "benchmarks" / "portable_scenarios.json"
    scenarios = []
    if benchmark_path.is_file():
        scenarios = json.loads(benchmark_path.read_text(encoding="utf-8")).get("scenarios", [])
    scenario_errors: list[dict[str, Any]] = []
    ids = {row.get("id") for row in scenarios if isinstance(row, dict)}
    if ids != REQUIRED_SCENARIO_IDS:
        scenario_errors.append({
            "expected": sorted(REQUIRED_SCENARIO_IDS),
            "actual": sorted(value for value in ids if value),
        })
    for row in scenarios:
        if not isinstance(row, dict) or not row.get("must_include") or not row.get("must_not_include"):
            scenario_errors.append({"id": row.get("id") if isinstance(row, dict) else None, "error": "missing invariant lists"})

    semantic_errors = [] if missing else semantic_contract_errors(root)
    publication_manifest_errors = manifest_errors(root, args.require_manifest)
    passed = not any([
        missing,
        broken_links,
        forbidden,
        missing_tokens,
        scenario_errors,
        semantic_errors,
        publication_manifest_errors,
    ])
    files = package_files(root)
    payload = {
        "schema_version": "portable_skill_validation_v2",
        "status": "PASSED" if passed else "FAILED",
        "skill_root": str(root),
        "required_files_missing": missing,
        "broken_local_markdown_links": broken_links,
        "forbidden_package_files": forbidden,
        "required_contract_tokens_missing": missing_tokens,
        "semantic_contract_errors": semantic_errors,
        "scenario_errors": scenario_errors,
        "scenario_ids": sorted(value for value in ids if value),
        "publication_manifest_required": args.require_manifest,
        "publication_manifest_errors": publication_manifest_errors,
        "file_count_excluding_manifest": len(files),
        "file_sha256_excluding_manifest": {path.relative_to(root).as_posix(): sha256(path) for path in files},
        "scope_note": "Static package validation does not prove scientific accuracy or host-model behavior; run and record separate end-to-end Agent scenario tests.",
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
