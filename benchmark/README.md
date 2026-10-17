# Benchmark workbench

Eight YAML candidate specifications cover the requested domains. **Zero tasks are validated**.
Some requested safety behavior is already claimed by the subject README, so each candidate needs a
meaningful extension after source inspection. No repository APIs, function names or defects are asserted.

Use `researchctl list-tasks`, `researchctl new-task T009 --title "A concrete change"`, then
`researchctl validate-task benchmark/tasks/T009.yaml`. Ordinary validation checks candidate metadata
and reports missing evidence. `--require-validated` enforces pin/reference/oracle/mutant gates.
The schema is data/schemas/task.schema.json; the canonical template is task-template/task.yaml.

Place human-written patches in reference-solutions/, evaluator-only tests in oracles/, deterministic
seed definitions in fixtures/, and frozen task inventories in manifests/. The demo fixture is a
self-contained infrastructure check and is ineligible as a backend benchmark task.

No agent receives this research repository. Expose only a clean subject workspace and approved shared
documentation. Worktrees alone do not enforce filesystem isolation. See docs/agent-execution.md.
Next: pin and inspect the subject; validate two selected feature changes using protocol/task-construction.md.
