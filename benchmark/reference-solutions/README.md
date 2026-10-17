# Human reference implementations — evaluator only

T001 and T002 now have assistant-authored draft references in the external private evaluator directory,
located through ignored config/evaluator.local.yaml. No reference patch belongs in this public folder.
Public packages retain artifact hashes, execution summaries and pending human-review checklists.

Require feature and invariant tests to pass; capture evidence reports using the task-evidence schema.
Never label reference construction as an observed coding-agent run or as completed human review.
Next: independently inspect and reproduce both references before recording named human approval.
