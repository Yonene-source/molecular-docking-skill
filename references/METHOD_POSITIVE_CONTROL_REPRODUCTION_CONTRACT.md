# Method-positive control reproduction contract

## Purpose

A positive control asks whether the current method implementation can recover a known, relevant result under a bounded protocol. It does not prove that the study ligand binds, and it is not satisfied by pointing to an earlier local notebook, CSV, pose or report.

## Evidence classes

- `PRIMARY_INPUT`: raw experimental coordinates, deposited ligand identity, a curated benchmark source, or another authorized starting asset.
- `CURRENT_EXECUTION`: receptor/ligand preparation, commands, logs, outputs and QC created by the current Agent workflow.
- `HISTORICAL_REFERENCE`: an older notebook, prepared input, output, score, plot, pass label or local report.

Only `CURRENT_EXECUTION` built from `PRIMARY_INPUT` can satisfy the current positive-control gate. `HISTORICAL_REFERENCE` may be read only after the current gate is determined, then used to describe concordance, drift or regression. Its gate influence must be recorded as `NONE`.

## Required workflow

1. Define what method property the control tests: known-site recovery, pose recovery, covalent geometry, metal coordination, peptide placement, protein-interface recovery, or another bounded capability.
2. Select controls by an explicit rule before inspecting historical pass labels. Record included and excluded candidates.
   Prefer an offline deposited complex or a redistributable packaged benchmark so the gate can run without an external API. If no single positive control spans a modified-peptide method, split the gate into a chemistry/preparation control and a peptide pose- or interface-recovery control, then preserve the narrower method-domain claims.
   This Skill package does not itself redistribute third-party experimental coordinates. Follow `benchmarks/positive_control_asset_policy.json`: package an authorized asset with source/accession, citation or license note, selection rule and SHA256, or acquire it during separately authorized `EXECUTE`. If neither route is available, record `status: BLOCKED` with `reason_code: USER_INPUT` or `SOFTWARE`; do not replace it with historical output.
3. Start from raw or primary inputs. Re-extract the receptor and deposited ligand or regenerate the benchmark input.
4. Rebuild chemistry, protonation, atom mapping and preparation with the current tools. Record commands, versions, executable hashes, return codes and logs.
5. Write the gate before computation. For self-redocking this normally includes an atom-mapping definition, RMSD threshold, replicate/seed rule, grid definition and failure interpretation.
6. Execute fresh replicates with atomic status checkpoints. Preserve every output, including failures and timeouts.
7. Independently compute the gate metric from the fresh output. Do not copy an old RMSD column or pass flag.
8. Run artifact and content audits: nonempty outputs, exit codes, timeouts, hashes, source lineage, current-path isolation and figure provenance.
9. Only now read historical results for a post-hoc comparison. Never change the fresh threshold to force agreement.
10. State the method-domain boundary. Small-ligand pose recovery does not validate a modified peptide, protein-protein docking or affinity ranking.

## Failure and recovery

- A failed scientific gate is evidence about the current protocol. Diagnose preparation, grid inclusion, atom mapping, sampling and method-domain causes before choosing a causally different bounded alternative.
- A software or post-processing error is not a scientific negative. Fix the isolated cause and resume from valid atomic outputs when possible.
- If all compute finished and CSV, plotting or report generation fails, do not blindly rerun compute. Re-parse the same outputs, record the recovery reason, and preserve hashes.
- Never silently reuse historical outputs to hide a failed or missing current execution.

## Minimum artifacts

- control-selection register;
- fresh preparation manifest;
- per-job command, seed, timing, exit code, timeout, output path and SHA256;
- per-pose QC table with the metric definition;
- per-system gate summary;
- raw-coordinate or method-native figure plus provenance;
- explicit historical-reference comparison with `gate_influence: NONE`;
- independent artifact audit and stage handoff.

## Generalization

The same logic applies beyond docking. For enzyme optimization, a workflow-positive control might reproduce a known wild-type or benchmark variant under the current predictor; for structure prediction, it might blind-recover a known fold; for sequence models, it might reproduce a held-out labeled benchmark. The domain-specific metric changes, but the separation of primary input, current execution and historical reference does not.
