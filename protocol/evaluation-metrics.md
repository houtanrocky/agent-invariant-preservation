# Evaluation metrics

Primary: joint feature and required-invariant success among meaningfully evaluated runs, with attempted,
completed, environment-error and budget-timeout counts alongside every denominator. Report a sensitivity
analysis for exhausted budgets and unresolved environment incidents, rather than hiding them.

Secondary: build pass, feature pass, per-invariant pass, task/agent/condition rates and violation counts.
Audit failures can overlap balance or atomicity failures; preserve assertion-level labels and use one
reviewed primary failure category for tabulation. Never infer an invariant pass from a process exit alone
unless the evaluator contract checks that invariant and identifies the assertion.

Exploratory: wall-clock duration distributions, input/output tokens, provider-reported cost, and tool
interactions. Missing measurements stay null. Report measured counts, medians/ranges and measurement scope.
Next: freeze invariant IDs and evaluator output contracts before agent executions.
