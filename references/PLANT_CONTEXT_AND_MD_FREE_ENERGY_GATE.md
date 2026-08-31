# Plant context and MD/free-energy compute gate

## Purpose

This reference makes the docking Skill explicitly useful for plant research and prevents MD or free-energy branches from disappearing merely because the user did not specify a membrane, assay environment, or compute budget. It also prevents the opposite failure: launching expensive dynamics just because a GPU exists.

Every result remains predictive evidence for user judgment and experimental design. Docking, MD and free-energy calculations do not by themselves establish binding, affinity, activation, inhibition or in-planta function.

## Plant-domain context gate

Before protocol approval, assess which of the following can change the scientific interpretation:

1. Species, cultivar/accession, gene model, transcript isoform and protein version.
2. Precursor versus mature chain, signal peptide, transit peptide, propeptide, tags and experimentally used construct.
3. Tissue, developmental stage, stress condition and subcellular compartment.
4. Cytosolic, apoplastic, vacuolar, organellar or membrane-leaflet accessibility.
5. Plant membrane composition: phospholipid classes, sterols, sphingolipids, anionic lipids, leaflet asymmetry and plausible thickness. When real conditions are absent, use two clearly hypothetical compositions only if literature or biology supports defensible bounds and the proposed method can discriminate them; otherwise preserve the unknown and state the smallest information needed.
6. Cell wall, cuticle, extracellular matrix, membrane potential, ion gradient, pH and redox environment.
7. Plant-specific or relevant glycosylation, disulfides, phosphorylation, lipidation, proteolysis, metal/cofactor occupancy and endogenous ligand competition.
8. Oligomeric or heteromeric state, accessory proteins and family-specific receptor state.
9. Ligand provenance, formulation, purity, stereochemistry, nonstandard residues, aggregation, concentration, vehicle and degradation.
10. Orthogonal plant-relevant readouts: electrophysiology, leakage, membrane-only controls, localization, dose/time response, phenotype, genetic rescue, direct biophysical binding and expression/trafficking QC.

For each material unknown, use exactly one of these visible states: `ASSESSED`, `PARTIALLY_ASSESSED`, `NOT_ASSESSED`, `BLOCKED`, or `USER_DEFERRED`. Safe bounded previews may use assumptions, but every assumed value must be labeled hypothetical and linked to the claim it limits.

## Dynamics question gate

MD is considered only when it can discriminate at least one live question, for example:

- whether two pose families relax differently;
- whether a flexible peptide leaves or preserves a proposed interface under matched conditions;
- whether a local loop or side-chain arrangement accommodates the ligand;
- whether receptor-free versus receptor-containing membrane behavior differs;
- whether alternative plant membrane compositions change accessibility or partitioning;
- whether two receptor states or models give materially different local behavior.

If no outcome could alter hypothesis ranking or experimental priority, mark MD `NOT_APPLICABLE` with the reason. If chemistry or parameters are invalid, use `status: BLOCKED` and `reason_code: PARAMETERIZATION`; do not substitute a short trajectory or minimization and call it dynamics.

## Mandatory Q0 resource and chemistry audit

Before any benchmark, write `03_analysis/md_feasibility/hardware_inventory.json` and `03_analysis/md_feasibility/q0_parameter_audit.json` containing:

- operating system, WSL/container context and tool versions;
- physical/logical CPU count;
- total and currently available RAM;
- GPU/accelerator model, driver, usable memory and software-visible device list;
- free task-disk space and expected trajectory/checkpoint growth;
- intended receptor, ligand, membrane, solvent and ion composition;
- estimated atoms, restraints, timestep, precision and output interval;
- force-field and charge coverage for every standard and nonstandard component;
- licensing, installation and download constraints;
- a PASS/BLOCKED decision with concrete missing artifacts.

Use `scripts/profile_md_resources.py` for a deterministic local inventory and projection scaffold. It does not replace an engine-specific benchmark.

There is no universal “sufficient GPU” model or VRAM threshold. A device is sufficient only when the intended system fits with safety margin and the measured throughput can satisfy the user-approved scientific duration and replicate plan. CPU-only systems remain eligible for a measured small benchmark when safe.

## Q1 setup and smoke test

When Q0 passes, first persist task-specific hard ceilings for job count, wall time, RAM/VRAM and storage based on current availability and approved scope. Then perform only the smallest reversible setup test needed to verify:

- topology and coordinate generation;
- finite energies and forces;
- no missing parameters or catastrophic clashes;
- stable minimization and equilibration startup;
- checkpoint writing and restart;
- measured peak memory and output growth.

Q1 is setup evidence, not evidence of binding or stability. Preserve all failures, logs, exit codes and hashes.

## Q2 measured benchmark and capacity projection

Run a bounded benchmark on the actual intended or explicitly reduced system. Record engine, version, command, hardware, atom count, ensemble, timestep, precision, PME/cutoffs, constraints, output interval, warmup exclusion, measured simulation time, wall time, ns/day, peak RAM/VRAM, energy sanity and bytes/ns.

Project at least:

- 1 ns, 10 ns and 100 ns per replicate;
- the scientifically proposed duration and replicate count;
- wall time under current concurrency;
- checkpoint, trajectory and analysis storage;
- safety margin and uncertainty range;
- whether laptop/local execution, local unattended execution, workstation/HPC export or cloud execution is the sensible route.

Never extrapolate from another system without labeling it an estimate. Prefer a benchmark from the exact system. If only a reduced system can run, state which scientific question that reduction can still answer.

## User compute decision

After Q2, write `03_analysis/md_feasibility/md_compute_budget.json` and show the user four concrete choices:

1. `RUN_LOCAL_BOUNDED` - named duration, replicates, expected wall time, storage and hard stop.
2. `RUN_LOCAL_REDUCED_DISCRIMINATOR` - smaller system or shorter question that still distinguishes named hypotheses, with weaker claim boundary.
3. `EXPORT_HPC_OR_CLOUD` - reproducible package, scheduler template, resource request, checkpoint/restart and expected cost range; do not upload private data or spend money without approval.
4. `DEFER` - continue all non-MD synthesis and record exactly which claims remain unsupported.

Production MD must not start until this choice is persisted in `03_analysis/md_feasibility/md_user_decision.json`. A user deferment is a valid terminal state for the approved scope, not permission to claim the dynamics question was answered.

## Free-energy gate

Free-energy work is a separate approval after MD setup validity. It requires:

- an explicit comparison or thermodynamic quantity;
- a justified method: relative alchemical, absolute alchemical, umbrella/PMF, metadynamics or another method suited to the question;
- a valid transformation or reaction coordinate and standard-state definition;
- parameter coverage, charge-change treatment and restraint scheme;
- equilibrated starting states and overlap/convergence diagnostics;
- windows/lambda schedule, independent repeats and uncertainty target;
- a measured pilot for throughput and storage;
- positive/negative controls and failure interpretation.

Write `03_analysis/free_energy/feasibility_and_budget.json` before asking the user. Provide local, reduced, HPC/cloud and defer choices. Docking scores, MM/PBSA, MM/GBSA and short nonequilibrium estimates must not be relabeled as experimental affinity or rigorous free energy.

## A/B/C/D fallback ladder

- **A:** preferred engine and full intended system on the best locally available accelerator.
- **B:** causally different feasible route, such as another supported engine, precision/kernel path, partitioned system preparation, checkpoint strategy or workstation/HPC target. Merely extending a timeout is not different.
- **C:** lower-cost discriminator such as minimization, restrained local relaxation, implicit-solvent sensitivity, reduced membrane patch, coarse-grained preview or short matched comparison, only when it still separates named hypotheses.
- **D:** user supplies true membrane/assay conditions, authorizes installation/download, selects an external compute target, or defers.

A failure at A closes only A. The runtime must checkpoint, diagnose, choose B or C, and preserve the weakened claim boundary. The branch closes only after success, user deferment, verified parameter/tool impossibility, or at least two causally different evidenced failures with no safe informative fallback.

## Completion and reporting contract

The final report must state:

- what plant context was observed, predicted, assumed or not assessed;
- the exact local hardware inventory and benchmark basis;
- the maximum feasible local scope and why;
- the user's compute decision;
- which MD/free-energy tasks actually ran, with nonzero job manifests only when they ran;
- what each trajectory or energetic result can and cannot mean;
- where raw coordinates, trajectories, logs, tables, plots, checkpoints and manifests are stored and how to read them;
- the next smallest experiment or computation that would most reduce uncertainty.

The completion contract fails if a material locally feasible preview was silently skipped, if production compute ran without a persisted user decision, if missing GPU was treated as a scientific negative, or if a pilot was promoted to evidence of long-term binding.
