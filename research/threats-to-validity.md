# Threats to validity

| Dimension | Threat | Planned mitigation and residual risk |
| --- | --- | --- |
| Construct | Weak oracles equate passing with correctness | Reference review, deliberate defects, history assertions; incomplete behavior coverage remains |
| Internal | B receives otherwise absent requirements | Shared requirements contract and prompt information-parity audit |
| Internal | Session memory, order or environment drift | Independent sessions, clean checkouts, randomized blocked order, recorded versions |
| Conclusion | Repetitions treated as independent tasks | Task-level summaries; cluster-aware plan; few tasks limit inference |
| External | Single educational backend and purposive tasks | Bounded claims, document rejected tasks and selection rationale |
| External | Training contamination or prior author familiarity | Record repository publicity, task creation dates and human involvement |
| Reliability | Concurrency flakiness and database variance | Fixed schedules/seeds, repeated baseline checks, retained histories |
| Researcher | Author constructs tasks, prompts and oracles | Independent supervisor/human review; blind failure labeling when feasible |

Next: assign an owner and evidence link to each mitigation at protocol freeze. Report residual threats
in the manuscript even when mitigations succeed. Never substitute Go's race detector for SQL history checks.
