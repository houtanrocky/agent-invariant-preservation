# Task construction and validation gates

Inspect pinned source, migrations, ADRs and tests before selecting a candidate. Record exact paths/lines
and a rationale for a meaningful new change. Existing supported behavior alone is not a new feature task.
Avoid underspecified refunds or cancellation policies; state ownership, spending, retry and audit rules.

Required gates: reproducible baseline; clear change instruction; human-validated reference implementation;
functional tests; invariant regressions; at least one deliberately defective patch rejected by tests;
and documented expected-behavior rationale. A baseline may lack a requested feature, but existing
invariants must pass its regression tests. The reference must pass both suites. A mutant must fail a
relevant assertion, not merely fail to compile.

Machine evidence uses data/schemas/task-evidence.schema.json. Each role report identifies task, baseline,
executed command, timestamp, reviewer, expected/actual exit code, rationale, and hashed artifacts.
The task's evidence map references reports with SHA-256. Human review of test relevance remains necessary;
schema validation cannot establish oracle soundness or genuine execution.

`validate-task` accepts honest candidate metadata and lists missing gates. `--require-validated` fails
when evidence is incomplete. Set validated status only after named human review; do not promote on metadata
alone. Keep reference and oracle files outside the agent filesystem mount/account.
Two executable drafts are now T001/T002; their prior underspecified/redundant specifications are
preserved in artifacts/task-spec-history/. References, mutants and held checks remain private, with
public hash-bound execution summaries. Next: independent human review of baseline, references,
oracle rationale and information parity before promotion. The other six tasks remain deferred.
