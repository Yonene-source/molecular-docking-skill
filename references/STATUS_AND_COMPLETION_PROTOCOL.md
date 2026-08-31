# Status and completion protocol

## Purpose

Use one machine-readable vocabulary across task, stage and assumption records. Human-facing Chinese or English labels may be added separately, but must not replace these fields.

## Task level

`task_status` is one of:

- `PLANNING`
- `RUNNING`
- `PARTIAL`
- `COMPLETE`
- `FAILED`
- `CANCELLED`

`COMPLETE` means the deterministic contract for the approved scope passed. It does not mean every scientifically imaginable method ran.

## Stage or branch level

`status` is one of:

- `PENDING`
- `RUNNING`
- `PASSED`
- `FAILED`
- `BLOCKED`
- `NOT_APPLICABLE`
- `USER_DEFERRED`
- `SUPERSEDED`

Never encode a cause inside `status`. For example, use `status: BLOCKED` and `reason_code: PARAMETERIZATION`, not `BLOCKED_PARAMETERIZATION`.

Recommended `reason_code` values include `IDENTITY`, `PARAMETERIZATION`, `SOFTWARE`, `LICENSE`, `COMPUTE_BUDGET`, `USER_INPUT`, `QC`, `SCIENTIFIC_IRRELEVANCE`, `UPSTREAM_RESULT`, `TIMEOUT`, and `USER_DECISION`. Add a documented code only when none fits.

## Assumption-item level

`assessment_status` is one of:

- `ASSESSED`
- `PARTIALLY_ASSESSED`
- `NOT_ASSESSED`
- `BLOCKED`
- `USER_DEFERRED`

Also record `basis`, `assumption`, `sensitivity_preview`, `claim_limited`, `recovery_condition`, and `user_choice` when applicable.

## Deterministic completion

Completion passes only when:

1. entry mode and approved scope are persisted;
2. all required stages have terminal status;
3. each `BLOCKED`, `NOT_APPLICABLE`, or `USER_DEFERRED` stage has a reason, evidence, claim limit and recovery condition;
4. plan identity, user decisions and actual job manifests agree;
5. required outputs are nonempty and all declared hashes, exit codes, timeouts and QC checks agree;
6. provenance separates primary input, current execution, historical reference and assumptions;
7. report content, figure provenance, file map and artifact audit agree;
8. production MD/free-energy job counts are zero unless separately approved;
9. no model-authored statement is used as proof of completion.

`USER_DEFERRED` is a valid terminal stage inside an explicitly approved reduced scope. The final report must say which question remains unanswered and how to resume it.
