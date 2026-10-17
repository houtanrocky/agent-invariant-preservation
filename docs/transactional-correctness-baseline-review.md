# Dragon Market — Transactional Correctness Baseline Review

Follow-up: the user requested integrating and pushing the fix. The operational pin is now
`f4ba21185d1ba7b4bbb56f5addcc27d1b75bdec7`; see [integration verification](wallet-integration.md).
The original candidate review below preserves its earlier revision identities and approval status.
The pin change is operational; independent human approval remains pending.

Review update: 2026-10-18. **Automated candidate verification passed; independent human correctness
review and study-baseline approval remain pending.** This follows the existing upstream repair package;
the research assistant is not an independent human reviewer.

| Commit | Meaning |
| --- | --- |
| `ac599ff4da21b31171c277c96c7ae808dac012a5` | Original implementation before the workbench |
| `8f31a33ecb6c94c7d26a26a2a6f617772ba27816` | Workbench implementation candidate |
| `162c5cab9fa886445dd102f4a99961027f90aebb` | Old merged subject; previous configured pin; known defect |
| `07bc7e726c8f8228cd62849ef06054edf4f7e624` | Wallet repair implementation, parent is `162c5ca` |
| `58913f27161296bab0d3d223e7452a370cba580d` | Same repair plus evidence binding; proposed task starting commit |
| `52a24b4319a1ee857a1ebe6752cec932ac824cc9` | Later deployment merge; top-level wallet still old; repair is only a Git link |

The repair was fetched from the supplied local Dragon Market branch
`fix/transactional-correctness-baseline`. No remote branch of that name was advertised during this
inspection. Other machines need the repair objects supplied explicitly until the owner publishes an
appropriate branch. No push or merge was performed. The active study pin remains unchanged until the
review decision; constructing drafts against a candidate does not approve it.

## Verified policy and repair scope

For a positive daily limit `L`, completed debits on the current UTC day `S` plus **all outstanding
holds** `R` must satisfy `S + R <= L`. Zero means unlimited. Reserve raises `R`; release lowers `R`
without changing `S`; spend raises `S`; settlement replaces reserved units with completed spending;
earnings do not refund spending allowance. UTC rollover resets `S` and retains `R`.

This is the policy recorded in the upstream repair package. In the original 500/300/500 example,
the carried 500 hold now prevents the first 300 spend. After releasing it, 300 can be spent and the
additional 500 is rejected. This earlier rejection is intentional, and requires explicit human policy
confirmation. The repaired model does not attempt to reconstruct reservation dates.

Inspected implementation: `internal/guild/service.go`, row locking/audit writes in
`internal/postgres/guild_repo.go`, nested transactions in `internal/postgres/tx.go`, and migration 11.
Migration 11 requires empty wallets and establishes accounting version 2. It refuses a populated
legacy database; this candidate is suitable for fresh experimental fixtures, not an established-data
conversion. Its invariant argument assumes valid initial state, a stable configured limit and a
trustworthy UTC clock. These assumptions must remain in the reviewed scope.

## Evidence and reproducibility

The [original baseline report](target-baseline.md) and its archived artifacts remain untouched.
The [new report](../artifacts/target-baseline/58913f27161296bab0d3d223e7452a370cba580d/report.json)
records independently rerun commands, environment, timestamps, input hashes and archived-log hashes:
build, full Go tests, named daily-limit assertions, full race suite and vet all exited zero. This is
an independent execution of the existing tests, not independent test authorship. Windows was tested;
Linux and a fresh browser run were not verified in this follow-up.

Preserved upstream [before](../artifacts/target-baseline/58913f27161296bab0d3d223e7452a370cba580d/upstream-regression-before.txt)
and [after](../artifacts/target-baseline/58913f27161296bab0d3d223e7452a370cba580d/upstream-regression-after.txt)
logs show the same safety regression rejecting 800 persisted debits on the old implementation and
accepting 300 on the repair. These are labelled upstream evidence, not new executions here. The
preserved [candidate ledger](../artifacts/target-baseline/58913f27161296bab0d3d223e7452a370cba580d/upstream-candidate.json)
also records the three rejected wallet mutants and prior browser/frontend verification. Its approval
fields are still pending. Do not inherit old test success as human sign-off.

To repeat without changing the research pin, prepare a clean target checkout at the candidate and run:

```powershell
.venv/Scripts/python scripts/check_target.py --candidate-commit 58913f27161296bab0d3d223e7452a370cba580d
```

Each run creates a fresh ignored evidence directory. The script fails if no daily regression tests
actually execute. The public archive retains the original report hash and copies of raw outputs;
original `.local` paths in the report identify the initial observations.

## Human review decision

- [ ] Confirm the policy, including carried holds, zero limit and earlier rejection in the old example.
- [ ] Review the transition argument, SQL locks, transaction reuse, audit rollback and integer guards.
- [ ] Recalculate mixed-age holds, cancellation, settlement and rollover from independent examples.
- [ ] Reproduce before/after assertions and inspect actual debit/audit rows and rejected mutants.
- [ ] Confirm fresh-data-only migration and legacy refusal meet experimental requirements.
- [ ] Review exact implementation/evidence SHAs, toolchain and platform limitations.
- [ ] Record findings, reviewer identity, date and exact SHA; resolve material findings.
- [ ] Explicitly approve or reject the baseline and deliberately update the study pin if approved.

Reviewer: pending. Decision: pending. Proposed pin: `58913f27161296bab0d3d223e7452a370cba580d`.
Any source change requires new verification and a new decision. The two task packages remain drafts
until baseline approval and their own independent review. No main-study execution is authorized by
this document.
