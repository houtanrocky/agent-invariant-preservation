# T001: Retry-safe purchase service outcome

Status: **executable draft; human reference/oracle review pending**. Starting commit:
`58913f27161296bab0d3d223e7452a370cba580d`. The old candidate specification is preserved under
`artifacts/task-spec-history/2026-10-17/` and in Git history. Scope is the service boundary; the
requested outcome does not already exist there. Existing HTTP replay and settlement are regressions.

The complete shared request and requirements are in [the task specification](../../tasks/T001.yaml).
[Execution summary](validation.json) binds commands, expected/actual outcomes and private artifact hashes.
Baseline invariants pass and its new feature assertions fail. The independent task reference passes
feature/invariant, full existing-suite, race and vet checks. A deliberately faulty variant passes
feature assertions and fails a named persisted-state invariant with a compiling program and live database.
Each reference starts separately from the same candidate; they are not stacked patches.

“Independent” here means separate fixtures and SQL observations rather than reading service responses;
the reference and held checks were authored by the same assistant. Independent author review has not
occurred. Raw outputs, full references, faulty patches, evaluator code and a subject Git bundle are
outside the public checkout. The ignored evaluator locator names their private directory. The public
summaries cannot replace inspection of those artifacts. No study observations have been collected.

The evaluator's golden rows check exactly-once effects, authorization, state preservation and rollback.
Task fixtures use unlimited daily allowance so the newly repaired spending policy is excluded from
scoring. Existing repair tests remain in full reference verification. These are two similar feasibility
tasks, not a representative backend benchmark or a proof of correctness.

## Independent human review

- [ ] Approve the exact candidate baseline or require a new SHA and rerun all validation.
- [ ] Confirm the service feature is meaningful and accept every request/requirements clause.
- [ ] Read the private reference and compute expected state independently from the implementation.
- [ ] Reproduce passing baseline invariants, failing baseline features and passing reference suites.
- [ ] Inspect why the mutant passes features and fails a business assertion, excluding compile/environment errors.
- [ ] Review ownership/authorization, transaction/lock ordering, concurrent retries and rollback coverage.
- [ ] Record gaps, additional adversarial cases, reviewer identity, date, environment and decisions.
- [ ] Review the exact export inventory and both prompts for equal information and containment.

Reviewer/date: pending. Reference verdict: pending. Oracle rationale evidence: pending. Only after
named human review may metadata be promoted to `human_validated`/`validated`. The CLI must continue
rejecting `--require-validated` until those gates are actually satisfied.
