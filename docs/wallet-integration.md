# Wallet integration and operational pin update — 2026-10-18

The user explicitly requested fixing the remaining known defects and pushing the project. Dragon
Market commit `f4ba21185d1ba7b4bbb56f5addcc27d1b75bdec7` merges the repaired wallet branch into
the current default-branch deployment code. The research operational pin advances from `162c5ca`
to this exact commit. This user-authorized integration is not independent human correctness review
or permission to begin the main study.

The integration removes the misleading `.baseline-review` Git link from the project index while
retaining the local worktree, includes the actual accounting repair and migration 11, fixes the review
initializer's ten-migration assumption, and reports the repaired wallet in the hosted review notice.
The Render blueprint selects `master`; automatic deployment stays disabled. No hosted service or
existing database is modified by a code push.

Fresh review startup and restart now work with eleven migrations plus the seed. A regression also
recreates a populated previous review schema and verifies that migration refusal leaves gold, spent
counters and the migration ledger unchanged. The new initializer fails before its integration fix;
the failing execution is retained in the integration archive. Established-data conversion remains
outside scope because the defective old counter cannot safely reconstruct completed debits.

Fresh verification includes Go build/full tests/daily regressions/race/vet on the exact integrated pin,
frontend typecheck/lint/tests/build, three rejected wallet mutants, a clean Docker review-image build,
and the real image smoke suite using disposable TLS PostgreSQL. The image smoke checks access
control, real purchase/replay, independent SQL effects, desktop/mobile rendering and restart
persistence. Inspect the [archived report](../artifacts/target-baseline/f4ba21185d1ba7b4bbb56f5addcc27d1b75bdec7/report.json)
and adjacent integration artifacts for executed outcomes and hashes. Windows/local Docker were
verified; remote CI and a hosted deployment are separate observations.

Old baseline/candidate reports and the earlier manifest are retained. T001/T002 remain exact,
separate task snapshots at `58913f2`, now an ancestor of the integrated project. Their references,
held oracles and mutation evidence remain tied to that starting commit. Do not relabel them as
validated at `f4ba211`; changing their start would require a separate reconstruction and review.
Independent baseline/reference/oracle approval, agent containment and the pilot remain pending.
