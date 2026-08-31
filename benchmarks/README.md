# Portable benchmark

This benchmark verifies the Skill's portable decision contract without running scientific docking or external APIs. It is intentionally small and uses Python standard library only.

Run from the Skill directory:

```text
python scripts/validate_portable_skill.py --skill-root .
```

Expected result: JSON with `status: PASSED`, all scenario ids listed, no missing references, no broken local Markdown links, no `__pycache__` or `.pyc` package files, no known mode/status/membrane semantic contradiction, and all required entry modes, MD boundaries and molecular-figure views detected.

The scenarios are contract fixtures, not scientific accuracy benchmarks. The validator performs static package and contract checks; it cannot prove that an arbitrary host model will obey the contract. A receiving Agent runtime must additionally perform end-to-end output tests that verify each generated plan or audit contains the scenario's `must_include` invariants and excludes `must_not_include` behavior. Record that separate run instead of describing static validation as model-behavior validation.

The package intentionally does not redistribute third-party experimental coordinates. `benchmarks/positive_control_asset_policy.json` defines the acquisition and blocking rules. Consequently, `PACKAGE_VALIDATE` is fully offline, while a fresh scientific positive-control execution is offline only when an authorized deposited complex has already been packaged with source, license/citation and SHA256 provenance. Otherwise it remains `status: BLOCKED` with `reason_code: USER_INPUT` or `SOFTWARE`; historical result files cannot substitute.

Tested baseline requirements:

- Python 3.10 or newer;
- no network access;
- no third-party Python package required for this validator;
- read-only access to the unpacked Skill directory.
