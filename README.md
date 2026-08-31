# Molecular Docking Skill

An auditable plant-domain molecular-docking Skill for planning, executing, auditing, and validating docking research without treating docking score as affinity or forcing every case into MD.

Licensed under the [MIT License](LICENSE).

## Entry modes

- `PLAN`: read-only study design, assumptions, alternatives, budgets and approval points.
- `EXECUTE`: only the approved scientific and compute scope; installations and external services remain separate side effects.
- `AUDIT`: inspect existing inputs/results without requiring recalculation.
- `PACKAGE_VALIDATE`: validate the Skill tree, manifest, references and portable contract without touching a scientific case.

Read [SKILL.md](SKILL.md) and the compact [runtime contract](references/MOLECULAR_DOCKING_RUNTIME_CONTRACT.md) first. The runtime contract carries the safety, recovery, control, MD/free-energy, figure and completion invariants that must survive a bounded prompt.

## What is portable

The folder contains the scientific decision contract, assumption/status schemas, flexible-peptide fallback, method-positive-control rules, conditional plant-membrane logic, MD resource profiler, report/figure contract, 10 portable contract scenarios and deterministic manifest validation. It does not include private case data, historical result files, third-party experimental coordinates, a docking engine, an MD engine or an autonomous host runtime.

A receiving system must supply tool execution, permissions, persistent checkpoints/leases and a deterministic completion gate. Plant AI Lab provides such a host integration; copying this directory alone does not turn another chat model into a persistent Agent.

## Validate

From this directory:

```text
python scripts/validate_portable_skill.py --skill-root .
python scripts/profile_md_resources.py --task-root <safe-task-directory>
```

For a finalized publication tree:

```text
python scripts/build_publication_manifest.py --skill-root .
python scripts/validate_portable_skill.py --skill-root . --require-manifest
python scripts/test_release_contract.py --skill-root .
python scripts/package_release.py --skill-root . --output-dir <release-directory> --release-id <YYYYMMDD-HHMMSS>
```

See [portability and validation](references/PORTABILITY_AND_VALIDATION.md) and [benchmark notes](benchmarks/README.md). Static validation does not prove host-model behavior or scientific accuracy; record separate Agent end-to-end tests.

## Try the Skill

Clone the repository into a Codex skills directory using the Skill folder name declared in `SKILL.md`:

```text
git clone https://github.com/Yonene-source/molecular-docking-skill.git <CODEX_HOME>/skills/molecular-docking-research
```

Restart or reload the receiving Agent runtime, then invoke `molecular-docking-research` in `PLAN`, `AUDIT`, `EXECUTE`, or `PACKAGE_VALIDATE` mode. `EXECUTE` never authorizes downloads, installations, external services, production MD, or free-energy calculations by itself.

## Reports and figures

Final reports prioritize source-resolution molecular evidence: whole-system 3D placement, local 3D interaction geometry and coordinate-derived 2D interaction maps. Raw/process figures live in `04_figures`; PDF render QA belongs in `99_logs/final_report_qa`; final report folders contain documents and manifests, not copied image files. Explanatory plots use restrained CNS/Morandi-compatible colors, while raw tool figures retain source colors.
