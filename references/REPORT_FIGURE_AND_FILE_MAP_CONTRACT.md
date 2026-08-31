# Report figure and file-map contract

## Goal

Figures are evidence interfaces, not decoration. A reader must be able to see where the ligand or peptide is, which local contacts support the interpretation, how controls differ, and where the underlying files can be audited.

## Default structural figure triad

When valid atomic coordinates exist, the main report should normally include three complementary views for each hypothesis-changing representative pose family:

1. **Whole-system 3D location:** receptor cartoon or surface plus highlighted ligand/peptide, site marker and orientation context. It answers where the pose lies. Do not crowd it with every residue label.
2. **Local 3D interaction view:** zoomed pocket/interface with only mechanism-relevant residues, measured distances or geometry, clashes and unsatisfied polar groups where material. It answers what the proposed local interaction is.
3. **Coordinate-derived 2D interaction map:** hydrogen bonds, ionic contacts, hydrophobic contacts, aromatic interactions, metal coordination and residue identities, produced by a named tool or auditable script. It answers which interaction types are present.

If a view cannot be generated, record the missing tool/input, attempted fallback, prevented claim and recovery condition. Do not replace all three with a docking-score bar chart or a generic coordinate scatter plot.

## Comparative evidence panels

Prefer matched panels with identical camera, representation, labeling and scale for:

- receptor models/conformers or alternative sites;
- native versus composition/charge/hydrophobicity-matched controls;
- method-positive control reference versus recovered pose;
- representative pose families or cluster overlays;
- pre/post local relaxation;
- wild type versus geometry-only mutation controls;
- membrane orientation/environment assumptions when that context is material.

Show rank or docking score only as metadata. It is not affinity. Raw pose ensembles, convergence/cluster plots, contact tables and execution diagnostics remain available as supporting evidence.

## Dynamics and energetics figures

Only when those branches actually ran, use source-resolution raw traces and convergence diagnostics: RMSD/RMSF with atom selections, contacts or distances over time, replicate overlays, membrane/solvent context, energy/temperature/pressure sanity, overlap/window diagnostics and uncertainty. A single smoothed line or terminal snapshot cannot establish stability or free-energy convergence.

## Visual and resolution rules

- Preserve original tool colors for raw tool figures unless they are inaccessible; explanatory figures use a restrained low-saturation CNS/Morandi-compatible palette with color-blind-safe contrast.
- Prefer vector SVG/PDF or lossless source-resolution PNG. Never create a low-resolution screenshot of a sharper source merely to embed it.
- Use readable labels at final PDF size, consistent cameras and explicit scale/distance units.
- Store raw/process figures in `04_figures`; store page-render QA in `99_logs/final_report_qa`; keep final-report folders free of loose image files.
- The final PDF embeds source-resolution images directly. It must not link to temporary files or silently downsample molecular detail.

## Figure provenance record

For every figure record:

- figure id and scientific question;
- raw versus derived classification;
- source coordinate/table/log paths and SHA256;
- generating tool/script, version, command and parameters;
- selection rule, camera/orientation, atom/residue selections and distance definitions;
- output path, dimensions/DPI or vector status and SHA256;
- how to read it, what it supports, what it contradicts and what it cannot establish.

## File map

The final report must explain, by stage, where raw coordinates, prepared inputs, grids/configs, commands, logs, pose ensembles, CSV/TSV tables, JSON checkpoints, trajectories, figures, manifests and audits live. For each important file type state:

- what one row/model/frame represents;
- the meaning and units of key columns or fields;
- which values are QC, ranks or scores rather than physical measurements;
- how it connects to the figure and stage conclusion;
- whether it is primary input, current execution, historical reference, derived explanation or rejected/superseded output.

Pointing to a directory without explaining how to read its files does not satisfy this contract.
