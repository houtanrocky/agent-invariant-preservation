# Pinned subject inspection and candidate eligibility

Inspected commit: `162c5cab9fa886445dd102f4a99961027f90aebb` of Dragon Market. All source paths below
refer to this commit, not a floating branch. [Baseline execution](../docs/target-baseline.md) separately
records which tests ran. These are bounded code observations, not proofs of all transactional properties.

| Concern | Inspected implementation | Existing test evidence | Interpretation |
| --- | --- | --- | --- |
| Transaction boundaries | `internal/postgres/tx.go:33`, context-shared nested transactions and rollback on returned errors | `internal/postgres/research_test.go:318`, late order-update failure | Existing atomic purchase rollback checks; not proof for every failure mode |
| Purchase ownership and funds | `internal/order/service.go:93`, item/order locks then Spend/Earn/ownership updates | `internal/postgres/concurrency_test.go:16`, `research_test.go:86` | Concurrent purchase safety already implemented; a new task needs an extension |
| HTTP retry identity | `internal/idempotency/service.go:52`, claim/operation/completion in transaction; repository checks request hash | `research_test.go:135,168,219` | Purchase/bid replay and concurrent same-key effects already tested |
| Settlement | `internal/auction/service.go:254,267`, transaction and locked auction state | `research_test.go:263,365` | Worker, repeat and concurrent settlement already have coverage |
| Cancellation/reservation | `internal/auction/service.go:221`, active highest-bid checks and Release inside transaction | `internal/auction/service_test.go:266`; concurrent bids in `concurrency_test.go:76` | Highest-bid cancellation is existing behavior; cross-day accounting has a separate defect |
| Wallet bounds | `internal/guild/service.go`; migration 10 checks gold/reserved bounds | `research_test.go:435`, 120 bounded single-day operations with fixed seed | Selected sequences covered; not every integer combination or cross-day history |
| Daily policy | `internal/guild/service.go:62,139,189`, reset and aggregate Release subtraction | `internal/postgres/known_issue_test.go:11` | KNOWN-01 independently reproduced; intended cross-day bound fails |
| Audit coupling | `internal/guild/service.go:74`, `internal/postgres/guild_repo.go:15`, context-shared insert | Purchase counts and rollback assertions in `research_test.go` | Coupling exists; migration 10 does not enforce universal append-only immutability |

Source anchor: <https://github.com/houtanrocky/dragon-market/tree/162c5cab9fa886445dd102f4a99961027f90aebb>.
The inspected LICENSE grants MIT terms with the subject's notices. This does not select a license for
this research repository or remove the requirement to preserve upstream attribution.

## Meaningful changes still to define

No refund operation or direct guild-to-guild transfer route/method was found in the inspected router
and service contracts. T001/T004 are plausible new features, conditional on reviewed refund/ownership,
spending and retry policies. Their novelty is bounded to this subject, not to software engineering.
Refund-once is a prospective feature requirement, not an existing baseline invariant; candidate
metadata now distinguishes it from preserved financial constraints.

T002/T003/T005/T006/T008 concern already-supported settlement, purchase, cancellation, rollback and
audit behavior. Select genuine extensions before reference work, or retire these candidates. T007 cannot
score preservation of the already-violated daily bound without a prior scope/baseline decision. None
has a human-validated reference, hidden evaluation suite or task-specific rejected mutant yet.

## Public research material and exposure control

This commit includes an optional web workbench, `docs/research-readiness/`, source tests, known-issue
reproductions and `scripts/mutation-check.mjs`. These are public baseline material, not hidden tests
created by this study. Do not present them as independent human-validated benchmark oracles.
An upstream human-review status also remains pending; do not inherit a readiness claim as approval.

Before freeze, document whether the complete pinned repository or a deterministic backend-only export
is exposed to agents. Any export must have a versioned file inventory/hash and identical permissions
in both conditions. Do not silently remove documentation or preserve a floating snapshot. Independent
study oracles/reference patches remain outside agent access; public source can still create contamination
and solution-leakage risks even when A/B information parity is maintained.

Next: obtain human agreement on scope and two change contracts; map each preserved invariant to an
independent assertion, then construct references and deliberately defective implementations.
