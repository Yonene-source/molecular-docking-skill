# Molecular docking runtime contract

## Purpose and scientific boundary

Load this compact contract in full for every molecular-docking task before longer routed references. All outputs are predictive evidence for hypothesis ranking and experiment design, never a binary binding verdict. Docking scores are not affinity; a parseable pose does not prove correct chemistry; prediction diversity is not equilibrium; short relaxation or MD is not proof of stability.

Separate primary input, current execution, historical reference, assumptions and unknowns. Historical notebooks, scripts, poses, scores, plots and reports cannot pass a current gate unless reuse is explicitly authorized and independently validated. Verify receptor construct/assembly and ligand connectivity, stereochemistry, termini, charge, nonstandard residues and parameters before derived compute.

## Entry mode and side effects

Persist exactly one mode: `PLAN`, `EXECUTE`, `AUDIT`, or `PACKAGE_VALIDATE`.

- `PLAN`: read-only inspection, options, budgets and approval points; no scientific compute or installation.
- `EXECUTE`: run only the approved scientific and compute scope.
- `AUDIT`: inspect existing artifacts; recalculation is optional and separately authorized, never a completion prerequisite.
- `PACKAGE_VALIDATE`: test the Skill package only; do not touch a scientific case.

Triggering the Skill never authorizes installation, download, external services, uploads, production MD or free-energy work. Missing software is recoverable: search local/WSL/managed environments, estimate size/license/hardware fit and use the normal permission flow. Ask before multi-GB, privileged, licensed, paid or long-running changes.

## Adaptive graph, statuses and assumptions

Build task-specific stages for question/claim limits; lineage; receptor and ligand QC; topology/assembly/plant context; method suitability; competing sites/mechanisms; controls; bounded compute; pose QC; biological plausibility; conditional dynamics/energetics; synthesis; and expert-review experimental discriminators.

Stage `status` is `PENDING`, `RUNNING`, `PASSED`, `FAILED`, `BLOCKED`, `NOT_APPLICABLE`, `USER_DEFERRED`, or `SUPERSEDED`. Put causes in `reason_code`, not compound statuses. Every terminal non-pass records reason, attempts, evidence, claim limit and recovery condition. `USER_DEFERRED` may be terminal inside an explicitly reduced approved scope. A model-authored completion statement never overrides deterministic stage, artifact, hash, QC, plan-identity or user-boundary checks.

In `PLAN`, propose the assumption register and bounded previews without writing task artifacts or running scientific compute. In `EXECUTE`, after plan/scope approval and before scientific compute, persist `03_analysis/docking_assumption_register.json`. Mark each relevant construct/compartment, receptor state, pH/ions/cofactors/PTMs, membrane orientation/lipids, ligand states/aggregation, competing mechanism, controls, dynamics and experimental closure in canonical field `assessment_status` as `ASSESSED`, `PARTIALLY_ASSESSED`, `NOT_ASSESSED`, `BLOCKED`, or `USER_DEFERRED`. A host UI may display a legacy lowercase `current_status`, but persistence and completion normalize it to canonical form. Only `EXECUTE` may run safe approved previews, with every assumed value labeled hypothetical. Offer Agent preview, user-supplied real condition or deferment when the host UI supports them.

If membrane context is material and literature or biology provides defensible bounds that the method can discriminate, preview two hypothetical plant membrane/environment settings plus receptor-free behavior when interpretable. Otherwise preserve the unknown and request the smallest useful input. These previews do not recreate an assay or prove membrane activity.

## Bounded funnel and recovery

Before a matrix launch persist task-specific maximum jobs, concurrent jobs, per-job wall time, aggregate CPU/GPU hours, RAM/VRAM stop threshold, disk growth, checkpoints and termination rules. A branch is a scientific decision or causal route, not each matrix cell. Pilot broadly, prune by predeclared QC and expand only informative survivors.

Every critical branch declares:

- **A:** preferred bounded method/configuration;
- **B:** causally different fallback changing algorithm, representation, flexibility, search partition, parameter route, model subset or hardware path;
- **C:** lower-resolution discriminator that separates at least two live hypotheses with a weaker claim;
- **D:** smallest user input, authorization, specialist tool or experiment that unlocks the branch.

One failure or timeout closes only A. Diagnose and checkpoint before B/C. Repeating the same command longer is not a causal fallback. Close only after success, user deferment, verified impossibility, two causally different evidenced failures without informative fallback, or a stronger upstream result.

For flexible or modified peptides, rigid docking is only a geometric baseline. Compare valid conformers/secondary states and use peptide-aware, local-flexibility, ensemble or another materially different route when feasible. Record moved ligand/receptor degrees of freedom. Do not abandon flexible refinement after one infeasible all-torsion attempt.

Preserve a machine-readable modified-peptide bundle when available: 3D SDF/MOL2, canonical or atom-mapped SMILES and/or HELM, parent FASTA, residue/atom map, terminal state, cyclization/crosslinks, stereochemistry, formal charge and parameter provenance. Missing representations remain explicit uncertainty.

## Controls and pose QC

Use controls proportional to the claim: a freshly executed method-positive control from authorized primary input; matched composition/charge/hydrophobicity controls; receptor/site or matched-surface controls; multiple receptor models/conformers/sites/seeds; algorithmic nulls; and a materially different method when one scorer dominates the conclusion.

Prefer an offline deposited complex or redistributable benchmark. If no single control spans a modified-peptide method, separate chemistry/preparation validation from peptide pose/interface recovery and keep their narrower domains. Historical positive outputs have `gate_influence: NONE`. Reuse valid atomic compute outputs when only parsing/plotting fails.

Judge recurrent pose families, defined-atom RMSD, clashes, burial, pocket membership, orientation, contacts, unsatisfied polar atoms, topology/accessibility and sensitivity to model/conformer/seed/box/parameters. Invalid chemistry, tunneling, impossible burial or inaccessible topology invalidates a pose. Matched scrambled results can weaken sequence specificity but cannot prove absence of biological interaction.

## MD and free-energy gate

MD requires a named discriminating question, valid full-system chemistry, geometry/setup QC and user-approved production budget. Q0 records CPU physical/logical cores, RAM, accelerator/usable memory, disk, engine/version and parameter coverage. The resource profiler is inventory/arithmetic only, not an engine benchmark or complete Q0/Q2.

If the user has not deferred, persist absolute task ceilings, run only a bounded Q1 setup/restart smoke test, then a measured Q2 benchmark on the intended or explicit reduced system. Record atoms, command, hardware, precision, timestep, ensemble, throughput, peak RAM/VRAM, energy sanity and bytes/ns; project 1/10/100 ns and proposed replicates. No GPU is a resource fact, not a scientific negative; quantify the largest safe CPU scope and HPC/cloud export.

Before production persist one choice: `RUN_LOCAL_BOUNDED`, `RUN_LOCAL_REDUCED_DISCRIMINATOR`, `EXPORT_HPC_OR_CLOUD`, or `DEFER`. Production MD job count remains zero until that decision exists. A short pilot proves setup/local relaxation only.

Free energy is separately approved after valid MD setup. Require a named thermodynamic comparison, suitable method/reaction coordinate/transformation, parameters and charge handling, restraints/standard state, windows/lambdas, repeats, overlap/convergence, uncertainty, controls and measured budget. Docking scores and MM/PBSA or MM/GBSA are not rigorous affinity measurements.

## Figures, files and delivery

Preserve reasoning summary, competing hypotheses, support/contradiction/unknown tables, strategy journal, plan revisions, checkpoints and handoffs. Explain what each important coordinate, table, CSV, log, trajectory, figure, manifest and checkpoint means, how to read it and where it lives.

Use raw/source-resolution structure, pose, process and tool figures as primary evidence. With valid coordinates, default to a whole-system 3D location view, a local 3D residue/geometry view and a coordinate-derived 2D interaction map for every hypothesis-changing representative pose family. Use identical-camera matched panels for native/control, receptor state and pre/post comparisons. Coordinate scatter plots and score bars cannot substitute for molecular views. Explanatory graphics use low-saturation CNS/Morandi-compatible colors; raw tool figures retain source colors.

Store raw/process figures in `04_figures`, page QA in `99_logs/final_report_qa`, and only Markdown/DOCX/PDF plus manifests/audits/hashes in final report folders. Embed source-resolution figures directly into PDF. Every figure records source paths/hashes, tool/script/version/parameters, selection/camera, how to read it and claim limits.

Completion requires entry mode, approved scope, non-deferred branches, assumptions, controls/QC, provenance, hashes, figure/file maps, content/artifact audits, plan identity and user decisions to agree. Report uncertainty and the smallest next computation or expert-reviewed experiment that would most reduce it.
