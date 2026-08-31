# Molecular Docking Research Workflow

This is the default user-visible research direction, not a mandatory pipeline. Each phase contains decision gates from the decision tree and may be skipped, restricted, repeated, or stopped with a recorded reason.

## Phase 1: Question, identity, and evidence

Define the claims, verify receptor construct and ligand chemistry, establish source lineage, and retrieve family-specific domains, topology, homologs, known ligands/sites, and direct experiments.

## Phase 2: Structural assessment

Audit experimental structures when available. Otherwise quantify prediction diversity across nonredundant models, confidence, missing regions, domain arrangements, and biological constructs. Do not label prediction samples as a physical ensemble without evidence.

## Phase 3: Ligand and method assessment

Validate termini, stereochemistry, charge, nonstandard components, conformers, and parameter coverage. Classify the interaction and choose methods only after determining whether geometric screening, peptide-specific docking, flexible refinement, or no current docking is justified.

## Phase 4: Site investigation and protocol

Rank direct/homologous sites, conserved functional regions, consensus predicted pockets, and exploratory blind sites. Apply topology and accessibility vetoes. Write the complete reproducible protocol and control matrix before execution.

## Phase 5: Controlled interaction prediction

Run approved receptor-model, ligand-conformer, site, replicate, control, and sensitivity branches. A method-positive control must be freshly selected, prepared, executed and independently QC-audited by the current Agent workflow; prior local results are post-hoc references only. Preserve raw outputs and failures. Judge clusters, reproducibility, chemistry, geometry, contacts, and model/parameter dependence rather than score alone.

## Phase 6: Conditional dynamics

Ask whether dynamics can discriminate a live hypothesis. Require complete parameters, valid starting geometry, and a short performance benchmark. Production MD is a separately approved branch; a short pilot is setup/local-relaxation evidence only.

## Phase 7: Synthesis and experimental closure

Build a claim-evidence matrix, separate computational from biological plausibility, state contradictions and uncertainty, and rank hypotheses. Propose the smallest expert-reviewed binding, functional, and mutation experiments that can distinguish leading sites or mechanisms.

## Required visible plan

Show the user the intended phases, conditional branches, expected artifacts, time/resource ranges, and approval points. Preserve enough structure for informed review without implying that every phase will run.
