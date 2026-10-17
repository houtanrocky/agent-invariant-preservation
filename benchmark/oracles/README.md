# Independent evaluation oracles — hidden during collection

T001 and T002 have externally held feature and SQL-state assertions, concurrent retries, fault injection
and feature-passing deliberate defects rejected by invariants. Independent human review is pending.
Use ignored config/evaluator.local.yaml to locate the private package; keep all held code outside this
public repository. Public packages record hashes and execution summaries only.

Tests run in an evaluator environment against the captured agent patch after the coding session ends.
Store assertion-level output; require every invariant ID in the task contract. Repeated scheduling
is evidence over selected histories, not a proof of serializability. Next: independently review expected
values, fixture validity and coverage gaps before approving oracle-rationale evidence.
