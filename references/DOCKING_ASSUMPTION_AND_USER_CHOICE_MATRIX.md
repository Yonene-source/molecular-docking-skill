# Docking assumption and user-choice matrix

## Purpose

Use this reference while drafting a plan, after a surprising control, and before final synthesis. It prevents the Agent from treating an unmentioned biological condition as irrelevant. The goal is not to run every method. The goal is to expose every material assumption, propose bounded low-cost previews in `PLAN`, execute them only in approved `EXECUTE` scope, ask the user only when their real conditions or budget matter, and preserve uncertainty when a branch is deferred.

In `PLAN`, present the proposed register without writing it. In approved `EXECUTE`, every relevant item enters `03_analysis/docking_assumption_register.json` with: `id`, `group`, `question`, `why_it_matters`, canonical `assessment_status`, `evidence`, `assumed_values`, `assumption_source`, `low_cost_preview`, `user_question`, `user_options`, `escalation_gate`, `claim_limit_if_deferred`, and `result_files`. Canonical values are `ASSESSED`, `PARTIALLY_ASSESSED`, `NOT_ASSESSED`, `BLOCKED`, and `USER_DEFERRED`; a host UI lowercase adapter is not the persisted scientific contract.

## Action classes

- `AUTO_PREVIEW`: in `PLAN`, propose the reversible bounded calculation; in approved `EXECUTE`, the Agent may run it without another scientific-scope prompt when it remains within the persisted budget and side-effect boundary. State all assumed values and use more than one setting only when defensible bounds exist and the comparison can change a decision.
- `PREVIEW_THEN_ASK`: in `PLAN`, propose the preview and approval point; in approved `EXECUTE`, run the inexpensive preview, report sensitivity and estimated expansion cost, then ask whether to supply real conditions or continue under assumptions.
- `ASK_BEFORE_HEAVY`: preparation and budgeting may proceed, but production MD, enhanced sampling, free-energy calculations, paid APIs, cloud/HPC, or materially long runs require user approval.
- `REAL_INPUT_REQUIRED`: do not fabricate private sequences, assay conditions, known constructs, concentrations, mutations, or unpublished structures. Ask the user or mark the branch blocked.
- `EXPERT_REVIEW`: propose experimental discriminators and expected observations, but label them for expert review and do not present them as executed evidence.

## Coverage matrix

### A. Biological identity and construct

1. **Isoform, mature chain, signal peptide and termini.** Check splice isoforms, cleavage, missing tails, tags, fusion partners and whether the assayed construct differs from the reference sequence. `AUTO_PREVIEW` for public annotations and model comparison; `REAL_INPUT_REQUIRED` for the actual private construct.
2. **Domain context versus isolated domain.** Test whether a focused domain removes steric, membrane or allosteric context. Compare full-length and domain-preserving models when locally feasible. Never assume a short fragment folds independently.
3. **Cellular side and compartment.** Ask whether ligand and site can meet in apoplast, cytosol, lumen, membrane leaflet or organelle. Use topology/localization prediction as `AUTO_PREVIEW`; ask for the actual assay compartment when it changes accessibility.
4. **Tissue, developmental and stress context.** Public expression and phenotype evidence may change plausibility without changing docking geometry. Retrieve as supporting context, not as proof of binding.

### B. Receptor structural state

5. **Functional state.** Consider apo, agonist-bound, antagonist-bound, desensitized, open, closed and inactive states when relevant. Homolog mapping and predicted-state comparison are `AUTO_PREVIEW`; state-resolved MD or experimental structures may require escalation.
6. **Oligomeric state and stoichiometry.** Monomer, dimer, tetramer, heteromer and receptor-accessory complexes can create or remove interfaces. Search experimental/family evidence, model plausible assemblies, and include interface sites when warranted.
7. **Alternative domain orientation.** Prediction diversity may reflect uncertain domain packing. Cluster models by stable domains and compare site accessibility across non-redundant orientations instead of choosing one model.
8. **Missing loops, side chains and termini.** Repair only with confidence/provenance, then test sensitivity to the repaired region. A low-confidence loop touching the pose is a claim limitation.
9. **Conformationally active waters and cavities.** Retain crystallographic waters when justified; compare dry and selected-water states. Do not add arbitrary waters and call them observed.

### C. Receptor chemical environment

10. **pH, protonation and histidine microstates.** Run at least a plausible pH bracket when ionization can change charge complementarity. Ask for assay pH if available. Record the protonation tool and microstate.
11. **Salt, ionic strength and counterions.** Compare at least low/physiological/high ionic-strength interpretations for strongly charged interfaces when feasible; do not equate vacuum/effective electrostatics with solution behavior.
12. **Metal, cofactor and endogenous ion occupancy.** Preserve supported ions/cofactors; examine occupied and unoccupied states if both are plausible. Unsupported removal can destroy the site.
13. **Glycosylation, disulfides and PTMs.** Map predicted/known glycans, disulfides, phosphorylation and lipidation to site accessibility. Perform steric envelope checks before detailed glycoform simulation.
14. **Redox or covalent chemistry.** If covalent capture, oxidation or metal coordination is plausible, general noncovalent docking is insufficient; branch to a suitable method or state unsupported.

### D. Membrane and solvent context

15. **Membrane orientation and side accessibility.** Predict topology/orientation, map sites to membrane planes, and test thickness sensitivity. This is an `AUTO_PREVIEW`, not production membrane dynamics.
16. **Lipid composition.** Consider plant-relevant phospholipids, sterols, anionic lipids, leaflet asymmetry and local lipid-binding sites. If the real composition is unknown, compare two bounded hypothetical membrane settings only when literature/biology supplies defensible bounds and the chosen method can discriminate them. Otherwise keep composition `NOT_ASSESSED`, state the claim limit, and ask for the smallest assay or material input.
17. **Membrane potential and ion gradient.** Charged ligands, channels and transporters may be state-dependent. Geometry cannot substitute for a potential; ask before production electrodynamics/MD.
18. **Receptor-free membrane control.** For amphipathic or hydrophobic ligands, compare membrane partitioning/perturbation with and without receptor under matched conditions. This distinguishes receptor dependence from generic membrane activity.
19. **Explicit solvent and water-mediated contacts.** Use local solvation/minimization or selected-water sensitivity before claiming a polar network. Production solvent MD follows the dynamics gate.
20. **Detergent, nanodisc or micelle context.** The experimental carrier can alter oligomerization and site exposure. Ask for it when interpreting direct binding assays.

### E. Ligand chemical and physical state

21. **Connectivity, stereochemistry, termini and nonstandard residues.** Verify machine-readable chemistry, rejected inputs, sequence-to-structure mapping and parameter coverage.
22. **Ligand protonation, tautomer and charge states.** Enumerate plausible microstates, not every combinatorial possibility. Use a bounded sensitivity matrix.
23. **Conformer populations and cis/trans states.** Generate chemically valid diverse conformers and cluster them. Do not treat arbitrary prediction samples as equilibrium populations.
24. **Peptide secondary structure and induced folding.** Compare helical, extended and intermediate starting states when supported. Flexible refinement must include a materially different fallback after one failure.
25. **Aggregation, oligomerization and concentration.** Amphipathic peptides may self-associate. Use sequence/structure heuristics and coarse concentration regimes as hypotheses; ask for experimental concentration and vehicle.
26. **Membrane partitioning and local concentration.** A weak solution interaction may be promoted by membrane enrichment. Estimate partitioning qualitatively or with bounded models, while keeping receptor-free controls.
27. **Chemical stability and degradation.** Proteolysis, oxidation, hydrolysis or epimerization may change the active species. Ask whether the assayed material was characterized; do not assume the nominal compound is the only species.

### F. Binding-site and mechanism space

28. **Orthosteric, allosteric, surface, pore, transmembrane and lipid-exposed sites.** Maintain competing site classes and apply topology/accessibility vetoes before score ranking.
29. **Oligomer-interface and composite sites.** Include sites formed only in an assembly; monomer docking cannot test them.
30. **Multisite, sequential and transient binding.** A ligand can partition, encounter the surface and then occupy another site. A single-box workflow may miss this mechanism.
31. **Competition with endogenous ligands or ions.** Include occupied/unoccupied comparisons and known-ligand controls where relevant.
32. **Indirect or allosteric functional effects.** A functional phenotype need not imply stable direct occupancy. Preserve membrane perturbation, receptor-state modulation and assay-context hypotheses.

### G. Sampling, scoring and controls

33. **Ligand flexibility.** Choose peptide-aware, ensemble or flexible strategies proportional to torsions; a rigid baseline is only a screen.
34. **Receptor side-chain and backbone flexibility.** Use side-chain relaxation, induced-fit or ensemble methods when contact residues or loops are uncertain. Record exactly what moved.
35. **Search-space sensitivity.** Test boxes/regions, blind versus focused search and boundary effects. One failed large box does not close flexible docking.
36. **Seed, exhaustiveness and mode sensitivity.** Use fixed recorded seeds and sufficient independent replicates. Repeated deterministic outputs are not replication.
37. **Scoring-function and engine sensitivity.** Compare a materially different method when the main conclusion depends on one scoring model. Agreement is supporting evidence; disagreement is a result.
38. **Pose clustering and atom mapping.** Judge recurrent pose families, not only the best score. Define RMSD atom maps and preserve chemically invalid or clashing poses as rejected evidence.
39. **Method-positive control.** Use a known complex/site/ligand where the method should recover geometry. Failure limits interpretation of case results.
40. **Sequence/composition controls.** One scrambled peptide is not a complete null panel. Consider multiple composition-, charge-, hydrophobicity-, length- and stereochemistry-matched controls.
41. **Receptor specificity controls.** Compare homologs, paralogs or matched decoy surfaces when scientifically interpretable. Avoid unrelated controls whose site physics are incomparable.
42. **Algorithmic null and label permutation.** Test whether the analysis pipeline creates apparent enrichment under shuffled labels or randomized placements.

### H. Dynamics, energetics and causal discrimination

43. **Local relaxation versus dynamics.** Minimization checks geometry; it does not establish residence, stability or binding.
44. **Production MD question.** Name the decision it could change: site comparison, peptide escape, loop accommodation, membrane partitioning or state coupling. Benchmark first, then ask before heavy execution.
45. **Enhanced sampling.** Consider replica, metadynamics, umbrella or weighted-ensemble methods only when the coordinate and decision are defined. More sampling without a discriminating question is not automatically useful.
46. **Relative or absolute free energy.** Require a valid thermodynamic comparison, parameter coverage, sampling plan, uncertainty and controls. Do not promote docking scores to affinity.
47. **Concentration, kinetics and residence.** Docking is not a kinetic assay. Preserve on-rate, off-rate, transient encounter and cooperative mechanisms as unknown unless an appropriate method or experiment addresses them.

### I. Biological and experimental closure

48. **Direct binding versus function.** Pair a direct-binding hypothesis with functional, membrane-only and vehicle controls. A functional effect can be indirect; a weak direct signal can still be context dependent.
49. **Dose, time and vehicle.** Ask for concentration range, exposure time, solvent/surfactant and assay temperature when they change interpretation.
50. **Mutation, rescue and epistasis.** Select mutations that discriminate mechanisms, not merely disrupt folding. Include conservative substitutions, remote controls and expression/trafficking checks; mark for expert review.
51. **Orthogonal readouts.** Consider biophysical binding, electrophysiology, leakage, imaging/localization, crosslinking and competition. Explain what each outcome would strengthen or weaken.
52. **Material provenance and batch quality.** Ask whether peptide purity, receptor construct, membrane preparation and batch metadata are available. If absent, retain them as experimental uncertainty rather than inventing values.

## User-facing choice contract

When the host UI supports the Plant AI Lab three-choice card, show every unresolved high-impact group with current evidence and these three routes. Other runtimes may adapt presentation, but must preserve all three decisions and their provenance:

1. **Agent先做假设敏感性预检** - run only the bounded, reversible preview and label all conditions hypothetical.
2. **我提供真实条件/材料** - list the smallest useful inputs, such as lipid composition, pH, ions, concentration, construct, oligomeric state or control ligand.
3. **本轮暂缓** - keep the branch open or user-deferred and state which claims remain unsupported.

Do not show a generic “do more analysis” button. The button text must name the assumption being added. If selecting a route materially changes an approved plan or invalidates a final report, archive the previous plan/report, generate a revised plan, and require approval again before compute.

## Required fallback ladder

Every planned computational branch must declare the following before launch. A failed first attempt may close only `A`, never the entire branch.

- **A - preferred method/configuration:** the scientifically strongest locally reasonable setup, with explicit time, memory and output/QC bounds.
- **B - causally different bounded fallback:** change a dimension that can plausibly remove the failure, such as algorithm, representation, receptor/ligand flexibility, search-space partition, restraint strategy, parameter set, model subset or hardware route. Repeating the same command with a longer timeout is not sufficient by itself.
- **C - lower-resolution discriminator:** use geometry, topology, local relaxation, coarse-grained treatment, surrogate property, homolog mapping, reduced matrix or analytical sensitivity only if it still distinguishes at least two live hypotheses. Label the weaker claim it supports.
- **D - external or user-assisted route:** request the smallest missing real condition, specialist tool, cloud/HPC budget or experimental datum. State the exact branch it would unlock.
- **Terminal condition:** close the branch only after success, two causally different evidenced failures with no safe high-value fallback, verified tool/parameter unavailability, user deferment after seeing the budget, or a higher-quality upstream result that makes the branch irrelevant.

The webpage must display A/B/C/D, the currently selected rung, measured runtime when available, and the next rung that will be attempted automatically. `BLOCKED` without attempted alternatives and evidence is not a terminal state. The Completion Critic must return the task to analysis whenever a high-value locally feasible rung remains unattempted.

## Completion Critic additions

Before a docking task can close, ask:

- Does every relevant assumption have a status and provenance?
- Did any missing user condition silently become a default value without a sensitivity check?
- Are hypothetical membrane, pH, ion, oligomer or concentration models clearly labeled?
- Were multiple plausible mechanism classes retained after a narrow negative control?
- Did the Agent expose the most informative user-supplied condition instead of asking for an unbounded data dump?
- Does every deferred item state exactly which claim it prevents?

Any high-impact `assessment_status: NOT_ASSESSED` item with a safe, locally feasible preview in approved `EXECUTE` scope returns the task to analysis. In `PLAN`, it remains a proposed branch and approval point rather than triggering compute.
