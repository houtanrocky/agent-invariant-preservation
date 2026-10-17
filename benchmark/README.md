# Benchmark workbench

Eight YAML candidate specifications cover the requested domains. **Zero tasks are validated**.
Some requested safety behavior is already claimed by the subject README, so each candidate needs a
meaningful extension. Source inspection now verifies the relevant implementations and records a
pre-existing daily-limit defect. See [the inspection](../research/subject-inspection.md) and
[baseline report](../docs/target-baseline.md). Task metadata is pinned and source-backed; references and
independent oracles remain unvalidated.

2026-10-18: [T001](packages/T001/README.md) and [T002](packages/T002/README.md) now have executable
draft references, held SQL-state checks, passing full/race/vet verification and feature-passing mutants
rejected by invariants. Their starting SHA is the repaired candidate; the other six specifications
remain historical candidates at the old pin. Human baseline/reference/oracle review is still pending.

Use `researchctl list-tasks`, `researchctl new-task T009 --title "A concrete change"`, then
`researchctl validate-task benchmark/tasks/T009.yaml`. Ordinary validation checks candidate metadata
and reports missing evidence. `--require-validated` enforces pin/reference/oracle/mutant gates.
The schema is data/schemas/task.schema.json; the canonical template is task-template/task.yaml.

Keep reference patches and evaluator-only tests in a private directory outside this public checkout;
the ignored `config/evaluator.local.yaml` is its local locator. Store public hash-bound summaries under
packages/ and the shared export inventory under manifests/. The demo fixture is a
self-contained infrastructure check and is ineligible as a backend benchmark task.

No agent receives this research repository. Expose only a clean subject workspace and approved shared
documentation. Worktrees alone do not enforce filesystem isolation. See docs/agent-execution.md.
Next: independently review the two packages and exposure inventory using protocol/task-construction.md.
A green candidate suite does not constitute human baseline approval or independent oracle validation.
