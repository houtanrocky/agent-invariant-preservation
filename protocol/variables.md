# Variables

| Role | Variable | Representation/control |
| --- | --- | --- |
| Intervention | prompt condition | A or B; frozen prompt text and hash |
| Blocking | task and agent system | IDs and versions; same task in both conditions |
| Primary response | full_task_success | Boolean only for completed evaluations; otherwise null |
| Components | feature, build, per-invariant outcomes | Separate booleans/nulls and evidence links |
| Exploratory | seconds, tokens, cost, tool interactions | Nonnegative values or null; retain measurement source |
| Controls | baseline, docs, tools, timeout, tokens, retries | Frozen per protocol; report deviations |
| Environment | OS, Go, DB digest/isolation, dependencies | Record exact observed versions and configuration |

Model version and agent version are separate. A provider model alias is insufficient if a versioned
identifier exists. Token counts from different providers may not be directly comparable.
Next: fill config/environment.local.yaml and save redacted effective configuration per execution.
