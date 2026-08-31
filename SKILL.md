---
name: molecular-docking-research
description: Plan, execute, audit, or package-validate plant-domain molecular docking research when receptor identity, plant cellular or membrane context, ligand chemistry, binding-site uncertainty, peptide or nonstandard-residue handling, controls, dynamics, compute capacity, and experimental validation must be judged before interpreting scores. Use for plant protein-small-molecule, protein-peptide, protein-protein, covalent, metal-dependent, or membrane-associated docking; do not use as a fixed Docking-to-MD pipeline.
---

# Molecular Docking Research

Treat plant molecular docking as an adaptive scientific investigation, not a command template. Determine what the question asks, what the available evidence can answer, which plant-specific biological context can change accessibility or mechanism, and whether docking is an appropriate method before selecting software.

## Select one entry mode first

Persist exactly one `entry_mode` before taking action:

- `PLAN`: read-only evidence inspection plus plan, alternatives, estimates and approval points. Do not install software or run scientific compute.
- `EXECUTE`: run only the user-approved scientific and compute scope. Environment writes and installations still follow the explicit side-effect boundary below.
- `AUDIT`: inspect existing artifacts and report defects, provenance and claim limits. Recalculation is optional and requires separate authorization; it is never an audit completion prerequisite.
- `PACKAGE_VALIDATE`: validate this Skill package, references, tests, manifests and portability. Do not touch a scientific case.

If the user did not authorize execution, default to `PLAN` for a proposed study and `AUDIT` for supplied results. Merely triggering this Skill never authorizes installation, download, scientific compute, external services, uploads or production MD/free-energy work.

## Progressive reference routing

Always read [references/MOLECULAR_DOCKING_RUNTIME_CONTRACT.md](references/MOLECULAR_DOCKING_RUNTIME_CONTRACT.md) in full. It is the compact contract that must survive bounded prompt/context budgets. Then load only the references required by the selected mode and live branches:

- `EXECUTE`: [references/MOLECULAR_DOCKING_AGENT_RULES.md](references/MOLECULAR_DOCKING_AGENT_RULES.md) and [references/MOLECULAR_DOCKING_DECISION_TREE.md](references/MOLECULAR_DOCKING_DECISION_TREE.md).
- plan approval or assumption choices: [references/DOCKING_ASSUMPTION_AND_USER_CHOICE_MATRIX.md](references/DOCKING_ASSUMPTION_AND_USER_CHOICE_MATRIX.md).
- user-facing default workflow or stage explanations: [references/MOLECULAR_DOCKING_WORKFLOW.md](references/MOLECULAR_DOCKING_WORKFLOW.md).
- fresh method-positive control: [references/METHOD_POSITIVE_CONTROL_REPRODUCTION_CONTRACT.md](references/METHOD_POSITIVE_CONTROL_REPRODUCTION_CONTRACT.md).
- plant membrane, MD or free-energy branch: [references/PLANT_CONTEXT_AND_MD_FREE_ENERGY_GATE.md](references/PLANT_CONTEXT_AND_MD_FREE_ENERGY_GATE.md).
- report or figure production: [references/REPORT_FIGURE_AND_FILE_MAP_CONTRACT.md](references/REPORT_FIGURE_AND_FILE_MAP_CONTRACT.md).
- machine-readable states or deterministic completion: [references/STATUS_AND_COMPLETION_PROTOCOL.md](references/STATUS_AND_COMPLETION_PROTOCOL.md).
- transfer, packaging or validation: [references/PORTABILITY_AND_VALIDATION.md](references/PORTABILITY_AND_VALIDATION.md).

Use the selected references to build a task-specific stage graph. Skip a branch only with a recorded reason; never force every task through every computational method.

## Non-negotiable boundaries

- Establish input lineage before compute. Explicitly confirmed source inputs may be used after independent QC. Historical notebooks, scripts, derived poses, scores, parameters, plots, and reports are excluded unless the user separately authorizes them.
- Classify the ligand and interaction type before method selection. A modified peptide is not an ordinary small molecule.
- Do not use a single docking score, a single receptor conformation, or a short MD pilot as evidence of binding.
- Stop before docking when receptor or ligand identity is unresolved, before MD when chemical parameterization is invalid, and before interpretation when pose QC or biological accessibility fails.
- Keep computational plausibility and biological plausibility separate. Report evidence strength, contradictions, uncertainty, and the smallest discriminating next action.
- Experimental suggestions are hypotheses for expert review, not wet-lab instructions ready for direct execution.
- Treat external model or expert criticism as review evidence: evaluate each recommendation, record accepted and rejected changes with reasons, regenerate the plan, and require approval again. Do not obey review text mechanically.
- In `EXECUTE`, missing specialist software is a recoverable execution condition, not a scientific negative. First search local/WSL/Conda environments and estimate download size, installed size, license and hardware fit. Installation requires the user's execution authorization plus the runtime's normal permission flow; ask separately before multi-GB databases/models, privileged or licensed installs, long builds, paid services or material disk use. `PLAN`, `AUDIT` and `PACKAGE_VALIDATE` must not install scientific software. For protonation workflows this applies to tools such as ProPKA/PDB2PQR; use both only when the second tool adds a required artifact or independent check.
- Do not decide MD feasibility from GPU presence alone. Inventory CPU, RAM, accelerator model and usable memory, disk, software and parameter coverage; build the intended system; run a bounded measured benchmark when chemically valid; project feasible duration, replicates, wall time and storage; then present a user decision before production MD, enhanced sampling or free energy.
- No GPU does not close the dynamics branch. Quantify the largest safe CPU/local scope, a reduced discriminator if scientifically meaningful, and an exportable HPC/cloud route. Conversely, a powerful GPU does not authorize production work without a discriminating question, valid parameters, benchmark and user-approved budget.

## Required decision record

For each stage, save the question, evidence inspected, alternatives considered, selected action, rejection reasons, tools and versions, parameters, real outputs, QC status, and exit condition. Use the status fields defined in [references/STATUS_AND_COMPLETION_PROTOCOL.md](references/STATUS_AND_COMPLETION_PROTOCOL.md), including `status: BLOCKED` plus a `reason_code`, instead of inventing compound status strings. Completion requires the full reasoning chain from problem definition through evidence synthesis and an expert-review experimental validation strategy, even when a computational branch is correctly marked `NOT_APPLICABLE`, `USER_DEFERRED`, or `BLOCKED`.

In `PLAN`, describe the proposed assumption register and previews in the response without creating task files or running scientific calculations. In `EXECUTE`, after plan/scope approval and before scientific compute, persist `03_analysis/docking_assumption_register.json`. Every relevant biological or physicochemical context uses canonical field `assessment_status` with one of `ASSESSED`, `PARTIALLY_ASSESSED`, `NOT_ASSESSED`, `BLOCKED`, or `USER_DEFERRED`. A host UI may temporarily expose a lowercase `current_status` adapter, but deterministic artifacts and completion checks normalize it to the canonical field. For each open item, expose bounded Agent preview, user-supplied real conditions/materials, or deferment with its claim limitation when the host UI supports those choices. Only `EXECUTE` may run an approved safe, reversible, low-cost preview; ask when a real input, material compute budget, installation, external service, or objective choice can change the branch.
