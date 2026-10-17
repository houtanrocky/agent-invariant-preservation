# Benchmark workbench

Eight YAML candidate specifications cover the requested domains. **Zero tasks are validated**.
Some requested safety behavior is already claimed by the subject README, so each candidate needs a
meaningful extension. Source inspection now verifies the relevant implementations and records a
pre-existing daily-limit defect. See [the inspection](../research/subject-inspection.md) and
[baseline report](../docs/target-baseline.md). Task metadata is pinned and source-backed; references and
independent oracles remain unvalidated.

Use `researchctl list-tasks`, `researchctl new-task T009 --title "A concrete change"`, then
`researchctl validate-task benchmark/tasks/T009.yaml`. Ordinary validation checks candidate metadata
and reports missing evidence. `--require-validated` enforces pin/reference/oracle/mutant gates.
The schema is data/schemas/task.schema.json; the canonical template is task-template/task.yaml.

Place human-written patches in reference-solutions/, evaluator-only tests in oracles/, deterministic
seed definitions in fixtures/, and frozen task inventories in manifests/. The demo fixture is a
self-contained infrastructure check and is ineligible as a backend benchmark task.

No agent receives this research repository. Expose only a clean subject workspace and approved shared
documentation. Worktrees alone do not enforce filesystem isolation. See docs/agent-execution.md.
Next: decide task eligibility and exposure policy, then validate two selected feature changes using
protocol/task-construction.md. A green baseline suite does not override the known invariant violation.
