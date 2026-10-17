# Operational definitions

A **task** is a bounded, meaningful change to a pinned backend, with a human-reviewed expected behavior.
A **run** is one independent coding-agent session for one task, system, condition and repetition.
An **invariant** is a declared predicate over states or operation histories that must survive the change.
Passing tests is observed test adequacy, not a proof of the predicate for all executions.

`full_task_success = requested_feature_passes AND all_required_invariants_pass`.
Every required invariant must be evaluated; a missing assertion cannot count as passing. Build success
is recorded separately; feature pass is inconsistent with a failed build. Atomicity, idempotency,
concurrency, ownership and audit checks apply only where declared by a task.

An **environment error** prevents meaningful evaluation (for example unavailable PostgreSQL), and yields
null overall outcome until investigated. A completed evaluation can report an agent build failure as
feature failure. A budget timeout is preserved as interrupted/timeout, with a preplanned sensitivity
analysis counting exhausted-budget attempts as unsuccessful under the execution policy.

Next: agree which timeout/error categories permit evaluation of partial patches before main collection.
