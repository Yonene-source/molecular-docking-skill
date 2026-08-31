# Portability and validation

## Portable unit

Copy the whole `skills/molecular-docking-research/` directory. Do not copy only `SKILL.md`: the decision tree, scientific rules, plant context, assumption matrix, method-positive control contract, UI metadata and deterministic resource profiler are all part of the Skill.

Expected structure:

```text
molecular-docking-research/
├── SKILL.md
├── PUBLICATION_MANIFEST.json
├── agents/openai.yaml
├── benchmarks/
│   ├── README.md
│   ├── portable_scenarios.json
│   └── positive_control_asset_policy.json
├── references/
│   ├── DOCKING_ASSUMPTION_AND_USER_CHOICE_MATRIX.md
│   ├── METHOD_POSITIVE_CONTROL_REPRODUCTION_CONTRACT.md
│   ├── MOLECULAR_DOCKING_AGENT_RULES.md
│   ├── MOLECULAR_DOCKING_DECISION_TREE.md
│   ├── MOLECULAR_DOCKING_RUNTIME_CONTRACT.md
│   ├── MOLECULAR_DOCKING_WORKFLOW.md
│   ├── PLANT_CONTEXT_AND_MD_FREE_ENERGY_GATE.md
│   ├── PORTABILITY_AND_VALIDATION.md
│   ├── REPORT_FIGURE_AND_FILE_MAP_CONTRACT.md
│   ├── STATUS_AND_COMPLETION_PROTOCOL.md
│   └── docking_assumption_catalog.json
└── scripts/
    ├── build_publication_manifest.py
    ├── package_release.py
    ├── profile_md_resources.py
    └── validate_portable_skill.py
```

## Runtime requirements

- The scientific Skill text itself has no Python dependency.
- `scripts/profile_md_resources.py` uses the Python standard library. `psutil` is optional; Windows and POSIX memory/physical-core fallbacks are implemented.
- `nvidia-smi` or `rocm-smi` is queried only when present. Absence is recorded and never converted into a scientific negative.
- Common MD executables and version probes are inventoried when present. This is discovery only: the script does not build a system, validate parameters or run an engine benchmark, so it cannot complete Q0/Q2 alone.
- `agents/openai.yaml` is UI metadata and has no network dependency.
- The Skill may discover or propose docking/MD tools, but installations and production runs remain governed by its size, license, hardware and user-approval gates.

## Validation

Run the Codex skill validator from an environment containing PyYAML:

```text
python <skill-creator>/scripts/quick_validate.py <path>/molecular-docking-research
```

Run the portable standard-library contract benchmark:

```text
python scripts/validate_portable_skill.py --skill-root .
```

After all publication-tree edits are complete, create and then require the manifest:

```text
python scripts/build_publication_manifest.py --skill-root .
python scripts/validate_portable_skill.py --skill-root . --require-manifest
```

The manifest hashes every packaged file except itself and excludes cache bytecode. Any later edit invalidates it and requires deterministic regeneration.

Build a clean ZIP and sidecar manifest only after the manifest-required validation passes:

```text
python scripts/package_release.py --skill-root . --output-dir <release-directory> --release-id <YYYYMMDD-HHMMSS>
```

The archive has one `molecular-docking-skill/` root, includes hidden `.gitignore`, uses deterministic ZIP member timestamps, and excludes Git metadata and Python caches. The sidecar records archive SHA256, size, member list and the packaged publication-manifest SHA256.

Smoke-test the resource inventory without starting MD:

```text
python scripts/profile_md_resources.py --task-root <task-directory> --output hardware_inventory.json
```

Test projection arithmetic with measured benchmark values:

```text
python scripts/profile_md_resources.py --task-root <task-directory> --benchmark-ns 0.1 --wall-hours 1.0 --output-bytes 10485760 --atom-count 100000 --engine <engine> --device <device> --replicates 3 --concurrent-replicates 2 --target-ns 50
```

The second command does not run a benchmark; it projects from benchmark values supplied by the caller. The workflow must preserve the engine-native command, log and QC that generated those values.

## Plant AI Lab integration

Plant AI Lab loads the compact runtime contract before longer routed references so prompt truncation cannot remove recovery, control, MD or completion boundaries. The persistent ERA/co-scientist runtime owns leases, checkpoints, retries, A/B/C/D recovery and the deterministic completion contract. Copying this Skill into a different agent system does not automatically supply that runtime; the receiving system must implement equivalent persistence and gate semantics or disclose that limitation.

The canonical assumption artifact uses uppercase `assessment_status`. Plant AI Lab currently exposes a lowercase `current_status` field to its UI for compatibility, but the backend normalizes both old and new records before deterministic completion. Other runtimes should persist the canonical field and need not reproduce that adapter.

The package benchmark is deliberately offline and does not redistribute experimental coordinates. A real method-positive control requires an authorized primary coordinate asset with accession/source, citation or license note, selection rule and SHA256. If that asset is unavailable, the scientific control gate remains `status: BLOCKED` with `reason_code: USER_INPUT` or `SOFTWARE`; static package validation may still pass because it does not claim scientific execution.

## GitHub publication checklist

Before publishing:

1. exclude task inputs, private structures, trajectories, reports, credentials, `.env`, `__pycache__`, `.pyc`, caches and local absolute paths;
2. include all Skill files listed above and a fresh `PUBLICATION_MANIFEST.json` generated from the publication tree;
3. rerun the Skill validator, portable benchmark and resource-profiler smoke test on the target computer;
4. record the tested OS, Python version and validator result;
5. tag releases only after the package manifest matches the published commit.
