# Molecular Docking Decision Tree

## Entry classification

Translate the user question into explicit scientific claims: possible interaction, candidate site, pose or conformer preference, relative ranking, mutation effect, and experimental priority. For each claim, define support, contradiction, inconclusive evidence, and what computation cannot prove.

## State transitions

1. `INPUT_AUDIT`: establish source lineage and exclude unauthorized historical derived results. Unresolved identity moves to `ASK_USER` or `STOP`.
2. `IDENTITY_QC`: verify receptor construct and ligand chemistry. A wrong identity stops derived computation. A missing region triggers Agent-owned classification and repair attempts using supplied/public full-length models or context-preserving remodeling before any user escalation.
3. `EVIDENCE_GATHERING`: retrieve family/domain/topology, homolog complexes, known sites, and relevant experimental evidence. Direct or homologous site evidence may skip broad pocket scanning.
4. `STRUCTURE_ASSESSMENT`: compare experimental structures first, then prediction diversity, then any dynamics-derived ensemble. Low confidence branches to repair, domain restriction, alternative modeling, or stop.
5. `LIGAND_ASSESSMENT`: classify the ligand. Modified peptides require explicit nonstandard-component support. Invalid chemistry stops; incomplete energetic parameters limit work to justified geometric screening.
6. `METHOD_DECISION`: compare peptide-specific and general methods, site knowledge, receptor flexibility, sampling needs, controls, and resources. Record selected, control, rejected, and unavailable methods.
7. `SITE_DECISION`: prioritize experimental/homologous sites over conserved regions, consensus pockets, and blind discoveries; topology or inaccessibility can veto a site.
8. `PROTOCOL_REVIEW`: write models, conformers, sites, parameters, replicates, controls, stop conditions, and resource bounds before compute. Material plan changes return to human approval.
9. `CONTROLLED_COMPUTE`: execute only approved information-bearing branches. Failures return to method/protocol review rather than silently falling through.
10. `POSE_QC`: invalidate broken chemistry, clashes, tunneling, inaccessible sites, unsupported polar burial, and nonreproducible poses. No valid pose means stop before MD.
11. `DYNAMICS_DECISION`: start MD only for a named discriminating question with complete parameterization and a measured benchmark. Otherwise mark `NOT_APPLICABLE` or `BLOCKED`.
12. `EVIDENCE_SYNTHESIS`: keep computational and biological plausibility separate, expose contradictions, and assign ordinal support rather than certainty.
13. `EXPERIMENT_REVIEW`: propose the smallest discriminating assays and residue perturbations, all marked for expert review.

## Human states

- `ASK_USER` only for identity conflicts, irreducible objective choices, private data, paid/material resource expansion, or explicit approval gates. Do not ask whether to perform a necessary method/QC/repair step that is already within the approved scope.
- Method selection, public evidence retrieval, model clustering, QC thresholds, and branch selection are Agent decisions with auditable reasons.
- Plan rejection or external review creates a new plan revision; the previous plan is archived and cannot be executed until the revision is approved.
