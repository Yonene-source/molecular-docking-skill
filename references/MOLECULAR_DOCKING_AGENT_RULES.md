# Molecular Docking Agent Rules

## Purpose and scope

Use these rules to decide whether and how molecular docking can answer a scientific question. They apply to small molecules, peptides, proteins, covalent ligands, metal-dependent systems, and membrane-associated systems. They are a decision framework, not a mandatory linear pipeline.

Every conclusion must distinguish:

- what was directly observed or experimentally established;
- what came from databases or literature;
- what was computed in the current approved result chain;
- what is analogy, hypothesis, or unknown;
- what the selected method cannot answer.

Docking may propose sites, poses, and relative priorities. It cannot by itself prove binding, affinity, activation, inhibition, or biological function.

## Source-use boundary

1. Record every input as an identity anchor, external source artifact, user-generated source artifact, historical derived result, or reference-only material.
2. A user-confirmed source artifact may enter the current task only after independent identity and integrity QC.
3. Do not read or reuse historical notebooks, workflow steps, scripts, parameters, prepared structures, predicted pockets, docking poses, scores, trajectories, plots, or reports unless the user explicitly authorizes those derived results.
4. An allowed source file does not authorize reuse of the workflow that previously consumed it. Re-plan from the scientific question.
5. External prediction ZIPs are evidence packages, not proof that the current environment can reproduce the prediction. Audit sequence, model/version, settings, confidence metrics, structure count, chain composition, and file hashes.

## Adaptive decision chain

### D01. Scientific question definition

State which questions are in scope: possible interaction, candidate site, pose hypothesis, conformational preference, relative ranking, mutation effect, or experimental prioritization. Define what would count as support, contradiction, and an inconclusive result. Separate claims that docking can address from claims requiring experiment.

Create an assumption register before fixing the protocol. Absence of user-supplied membrane composition, pH, ion concentrations, oligomeric state, receptor functional state, ligand concentration, or positive controls is not permission to ignore those variables. Where feasible, the Agent first builds a clearly labeled bounded assumption or sensitivity screen, then shows the user what was assumed, how much the result changed, and which real condition would most improve the study. Read `DOCKING_ASSUMPTION_AND_USER_CHOICE_MATRIX.md` for the full coverage contract.

### D02. Receptor identity and sequence QC

Verify species, gene/protein identifiers, sequence version and length, unexpected residues, mature protein versus precursor, N/C-terminal completeness, signal peptide, transmembrane topology, domain architecture, splice isoforms, localization, and the biologically relevant construct. Decide whether docking should use full length, a domain, a multimer, or no current construct.

When a required region is missing, the Agent owns the repair decision within the approved scientific and resource scope. First determine whether the region is a signal peptide, cleaved propeptide, disordered tail, transmembrane element, or part of a structured functional domain. Then inspect already supplied full-length models and public models, compare confidence and context, and if necessary generate a full-length or context-preserving construct model. Do not model a very short fragment such as 22 residues in isolation and treat it as a reliable domain structure without evidence that it folds independently.

Do not ask the user whether a scientifically necessary, locally feasible repair should be attempted. Ask only when receptor identity anchors conflict, required private data are missing, a paid or materially larger resource expansion is needed, or alternative user objectives would change the research question. If all reasonable repair routes fail, record `BLOCKED` with attempted alternatives and the concrete evidence; do not convert a method decision into a user preference question.

Exit with `receptor_sequence_qc = PASS | CONDITIONAL | BLOCKED` and a stated biological boundary.

### D03. Receptor structure and ensemble QC

For every receptor model, record source and version, experimental resolution or prediction confidence, pLDDT/PAE when available, missing residues/atoms/side chains, low-confidence loops, chain completeness, oligomeric state, retained metals/cofactors/waters/known ligands, protonation, histidine states, charges, and any minimization.

Align models by stable domains, measure structural diversity, and cluster redundant predictions. Multiple stochastic samples count as a useful ensemble only when they show relevant, quantified structural diversity. Select non-redundant representatives and retain per-model uncertainty.

Before residue-level joins, establish an explicit numbering map among structure-local residue IDs, canonical FASTA positions, mature-chain positions, and any alignment/homolog coordinates. Preserve both source and canonical IDs in derived tables. A structure that is a strict subsequence or has renumbered residues must never be joined directly to full-length site IDs without validating the offset or alignment residue by residue.

Call differences among independently predicted structures `prediction diversity` until evidence supports a physical conformational ensemble. Do not imply Boltzmann populations or real receptor dynamics from AlphaFold, Boltz, ESMFold, or other prediction samples alone. A dynamics-derived ensemble must state its sampling method and limitations separately.

Exit with `receptor_quality = HIGH | MEDIUM | LOW | BLOCKED`. Low-quality or biologically wrong structures branch to structure repair, alternative modeling, domain restriction, or a documented stop.

### D04. Ligand identity and chemistry QC

Verify formula, atom connectivity, bond orders, stereochemistry, cis/trans state, tautomers, protonation, net charge, termini, acetylation/amidation, cyclization, disulfides, nonstandard residues/bonds, and conformer identity. Preserve a machine-readable chemical definition and rejected-input evidence.

For peptides, explicitly verify sequence-to-structure mapping and terminal chemistry. A parseable file is not proof of correct chemistry.

Exit with `ligand_chemistry_qc = PASS | CONDITIONAL | BLOCKED`.

### D05. Interaction and ligand-type classification

Classify the system before selecting tools:

- small-molecule-protein;
- peptide-protein or modified-peptide-protein;
- protein-protein;
- covalent;
- metal-dependent;
- membrane-associated;
- mixed or unsupported.

A peptide with nonstandard residues must enter the modified-peptide branch. Do not silently treat it as an ordinary small molecule because a PDBQT converter accepts it.

### D06. Method suitability and parameterization gate

Compare materially plausible methods for the classified system. Record why each candidate is selected, retained as a control, or rejected. Consider ligand flexibility, receptor flexibility, induced fit, peptide-specific sampling, scoring-function domain, membrane context, covalent/metal constraints, and available resources.

For modified peptides, verify whether preparation, charges, torsions, residue templates, and force fields correctly support every nonstandard component. A general-purpose Vina run may be a bounded exploratory baseline, but it cannot be the sole evidence path for a flexible modified peptide.

If parameterization is incomplete:

- docking may proceed only as an explicitly limited geometric screen when its input representation is valid;
- minimization, MD, and energetic interpretation remain blocked;
- failed parameterization attempts and materially different fallbacks must be preserved.

### D07. Binding-site evidence and accessibility

Classify sites from independent evidence: co-crystal structures, literature, curated annotations, functional/conserved residues, homolog structures, pocket predictors, electrostatics, blind searches, topology, and membrane orientation. Record competing sites rather than collapsing uncertainty into one box.

Use an evidence hierarchy unless case-specific evidence justifies another order: direct experimental site or complex > well-supported homologous site mapped with residue/domain correspondence > conserved functional region > consensus pocket prediction > blind-docking discovery. Family-specific domain architecture and topology must constrain this ranking before scores are considered.

Assign site evidence such as `HIGH`, `MEDIUM`, or `EXPLORATORY`. Reject or downgrade sites that the ligand cannot biologically access, even if their docking score is favorable.

### D08. Protocol design before execution

Write the protocol before running it: receptor models, ligand conformers, site definitions, preparation path, protonation/charges, software/version, grid centers and sizes, search settings, number of modes, random seeds, replicate count, controls, stop conditions, and resource budget.

Use replicates and sensitivity analysis proportional to uncertainty. Avoid claiming reproducibility from repeated deterministic runs or from redundant receptor samples.

The protocol must identify which conditions are measured, user-supplied, literature-derived, predicted, or hypothetical. Hypothetical environments are legitimate sensitivity models but must never be relabeled as the biological condition. When two or more plausible conditions could reverse site accessibility, protonation, oligomerization, or membrane orientation, expose the alternatives in the webpage before expensive execution.

### D09. Controlled computation

Execute only approved, information-bearing branches. Preserve commands, environment, versions, inputs, outputs, logs, exit codes, wall time, and random seeds. Do not overwrite failed attempts.

At minimum, when scientifically applicable, include:

- method-positive or known-site control;
- receptor/site specificity or matched-surface control;
- ligand/conformer/stereochemical or composition-matched control;
- algorithmic null;
- sensitivity to receptor models, ligand conformers, pockets, boxes, parameters, and preferably a materially different method.

A method-positive control passes the current stage only when the current Agent workflow executes it from an authorized primary or raw source through fresh preparation, computation and independent QC. Historical notebooks, prepared inputs, docking outputs, CSVs, plots and previous pass labels may be registered as references and compared after the fresh gate; they cannot satisfy the gate. Follow `METHOD_POSITIVE_CONTROL_REPRODUCTION_CONTRACT.md`, including its checkpoint-resume rule when post-processing fails after compute has completed.

### D10. Docking and pose QC

Do not rank by score alone. Check pose clusters and populations, cross-run and cross-conformer reproducibility, RMSD with a defined atom mapping, clashes, buried surface, pocket membership, orientation, hydrogen bonds, salt bridges, hydrophobic contacts, aromatic/cation interactions, unsatisfied polar atoms, and dependence on a single receptor model or parameter choice.

Do not invent fixed numeric weights for these dimensions unless the weighting model is calibrated and justified for the current task. Prefer an evidence table with independent dimensions, hard invalidation rules, ordinal support levels, sensitivity analysis, and explicit contradictions.

Flag tunneling through protein, impossible burial, broken chemistry, or unsupported polar burial as invalid rather than merely low confidence.

### D11. Biological plausibility

Score computational plausibility separately from biological plausibility. Ask whether the ligand can reach the site, whether orientation fits topology and localization, whether the site lies in a plausible functional domain, and whether residues/mechanisms agree with homologs, conservation, mutations, phenotypes, or other biology.

A computationally favorable but biologically inaccessible pose is downgraded or rejected.

### D12. Dynamics gate and analysis

MD is conditional, not automatic. Consider it when peptide flexibility, competing poses, receptor-model uncertainty, or local stability questions justify the cost. Do not begin MD until the full complex is chemically parameterized and passes geometry/minimization QC.

Record the exact MD trigger question, such as discriminating competing sites or poses, testing a flexible loop/interface, assessing a highly flexible peptide pose, or comparing local relaxation across receptor predictions. If no result could change a decision, mark MD `NOT_APPLICABLE`. If force-field coverage is incomplete, mark it `BLOCKED` rather than substituting a short trajectory.

First run a measured short benchmark and report system size, hardware, throughput, storage growth, and projected time for meaningful durations and replicates. A short pilot checks setup/local relaxation; it does not prove long-term binding.

If MD is scientifically justified and valid, analyze protein and ligand RMSD with alignment definitions, RMSF, radius of gyration when relevant, SASA, hydrogen-bond and residue-contact occupancy, key distances, center-of-mass separation, ligand escape, pocket stability, clustering, representative structures, and interaction persistence. MM/PBSA or MM/GBSA may be used as approximate comparative evidence with assumptions recorded; neither is an experimental Kd.

### D13. Multi-evidence synthesis and experimental validation

Create an evidence matrix covering docking, pose consistency, receptor/conformer sensitivity, structural plausibility, biological accessibility, dynamics if valid, conservation/homology, literature, and experimental evidence. For each row record direction, confidence, contradictions, and provenance.

Report an evidence-qualified hypothesis such as low, moderate, or high support; never translate a docking score into certainty or binding probability without calibration.

End with the smallest experiments that discriminate the leading hypotheses. Depending on the system, candidates may include SPR, MST, ITC, pull-down, Co-IP, competitive binding, functional assays, and site-directed mutagenesis. Connect predicted residues to testable perturbations and expected discriminating outcomes. Mark all experimental suggestions `待专家审核` and do not present them as validated protocols.

## Branch and stopping rules

- Wrong or unresolved identity: stop derived compute.
- Receptor structure `LOW/BLOCKED`: repair, remodel, restrict the construct, or stop; do not hide the issue with more docking.
- Modified peptide unsupported by preparation/scoring: switch to a suitable peptide/ensemble path or keep only a limited geometric screen.
- Unknown site: run site identification and competing-site analysis before focused docking.
- Single or redundant receptor model: obtain, audit, cluster, and compare an ensemble when model uncertainty can change the conclusion.
- Invalid or nonreproducible poses: do not spend resources on MD.
- Parameterization or geometry failure: no MD-derived stability or free-energy claims.
- No experimental calibration: restrict conclusions to structural compatibility and hypothesis prioritization.
- A branch is complete only when its exit condition is met, it is `NOT_APPLICABLE` with a reason, or it is `BLOCKED` with attempted alternatives and evidence.

## Required auditable outputs

Produce equivalent machine-readable artifacts in the current task result chain:

- question and claim-boundary record;
- input lineage and source-use policy;
- receptor sequence/topology QC;
- receptor structure/ensemble QC and clustering;
- ligand chemistry and nonstandard-component QC;
- interaction classification and method-suitability decision;
- binding-site evidence table;
- approved protocol and control matrix;
- raw computation manifest and failure logs;
- pose and biological-plausibility QC;
- dynamics gate and, only if valid, trajectory-analysis manifest;
- claim-evidence matrix, uncertainty register, and expert-review experimental suggestions;
- docking assumption register with user choices, assumed-condition provenance, and claim limitations;
- completion-gate status proving no high-value runnable gap was silently skipped.
