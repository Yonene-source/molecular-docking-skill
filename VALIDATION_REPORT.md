# Validation report

## Release candidate scope

- Date: 2026-08-28
- Skill: `molecular-docking-research`
- Intended private repository: `Yonene-source/molecular-docking-skill`
- Validation mode: `PACKAGE_VALIDATE`
- Scientific case compute: none
- Network/API use during validation: none

## Defects corrected before packaging

1. Replaced the stale publication snapshot with a source tree that includes the compact runtime contract.
2. Made `PLAN` and `AUDIT` read-only by contract; only approved `EXECUTE` can write scientific task artifacts, run previews, install software or compute.
3. Routed references progressively instead of loading every long reference for every task.
4. Standardized task, stage and assumption statuses. Canonical assumption persistence now uses uppercase `assessment_status`; the Plant AI Lab lowercase `current_status` is an explicit compatibility adapter.
5. Replaced mandatory two-membrane generation with a conditional rule requiring defensible biological/literature bounds and an informative method.
6. Added 10 portable contract scenarios, including plan side effects, canonical status normalization and conditional membrane bounds.
7. Added physical/logical CPU inventory, lightweight MD engine/version discovery, concurrency-aware wall-time projection and an explicit statement that the profiler does not complete Q0/Q2.
8. Added a positive-control asset policy. The Skill does not redistribute third-party coordinates; a scientific positive-control gate blocks honestly when no authorized primary asset is available.
9. Added deterministic manifest creation and manifest-required validation.
10. Added the report figure/file-map contract: whole-system 3D, local 3D and coordinate-derived 2D molecular views are primary; bars and coordinate scatters are auxiliary.

## Executed checks

| Check | Environment | Result |
|---|---|---|
| Portable static validator v2 | Bundled Windows Python | PASSED; 10/10 scenarios present; 0 missing files; 0 broken links; 0 cache files; 0 semantic contradictions |
| Official Skill Creator validator | Biomni WSL Python 3.11 + PyYAML | PASSED (`Skill is valid!`) |
| Project Python tests | Biomni WSL Python 3.11 | PASSED, 37/37 |
| Plant AI Lab rendered/web tests | Windows Node/pnpm | PASSED, 14/14 |
| Vinext production build | Windows Node/pnpm | PASSED |
| Resource-profiler smoke | Biomni WSL | PASSED; 16 physical / 32 logical CPU cores and concurrency arithmetic recorded; no MD simulation launched |

The synthetic benchmark inputs in the resource-profiler smoke test test arithmetic only. They are not measurements of this computer's MD throughput.

## What this validates

- package structure and local reference links;
- absence of cache bytecode from the publication tree;
- explicit mode/side-effect boundaries;
- canonical status and reason-code contracts;
- conditional membrane and MD/free-energy gates;
- fallback, positive-control and figure-delivery contract presence;
- deterministic manifest integrity;
- current Plant AI Lab backend compatibility and webpage rendering.

## What this does not validate

- scientific accuracy for an unseen target/ligand;
- availability or license of a docking/MD engine on another computer;
- a fresh scientific positive control without authorized primary coordinates;
- that an arbitrary receiving chat model obeys the Skill;
- persistence, leases, checkpoint recovery or completion gates in a host other than Plant AI Lab;
- actual MD ns/day, parameter validity, convergence or free-energy uncertainty.

A receiving runtime must therefore run the scenario behavior checks, a fresh authorized method-positive control, local tool/resource discovery, and its own persistence/completion tests before claiming autonomous execution readiness.
