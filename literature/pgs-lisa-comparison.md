# PGS/LISA comparison and study decision — 2026-10-18

Targeted full-text method/evaluation review is recorded in the versioned reading notes. This is a
critical comparison by the research assistant; artifacts, appendices and reported results have not
been independently reproduced. Other papers in the matrix remain at their recorded reading stage.

| Work | Intervention and evaluation emphasis | Source |
| --- | --- | --- |
| PGS v1 | Generated properties and iterative program refinement | [§III](https://arxiv.org/html/2506.18315v1#S3) |
| PGS v2 | Property feedback, minimized counterexamples, hidden-test correctness | [§§3–5](https://arxiv.org/html/2506.18315v2#S4) |
| LISA v1 | Generated API sequences/assertions; historical functional-bug detection | [§§III–VI](https://arxiv.org/html/2607.18711v1#S3) |
| Proposed study | Fixed shared requirements, planning guidance, feature AND persisted-state outcomes | [prompt conditions](../protocol/prompt-conditions.md) |

Our inference: “invariants help LLMs” is already an overlapping idea. We should position this as a
bounded extension into maintenance of a transactional backend, with a deliberately simpler intervention.
PGS's repository setting also prevents claiming that repository maintenance alone establishes novelty.
LISA's human involvement prevents claiming human-reviewed contracts as unique.

The defensible question is: **With the same requirements, source, tools and budgets, does an explicit
state-transition/retry/rollback planning instruction change joint feature and invariant correctness on
the selected Dragon Market tasks?** Evaluation checks are frozen and unavailable during coding. B
gets no extra requirements or held counterexamples. This differs operationally from generating
feedback during repair, but is not a direct comparison or a claim of superiority over either system.

Two closely related retry tasks are a feasibility package. They cannot establish broad backend
reliability, explain a causal reasoning mechanism, or justify treating repeated runs as independent
task samples. Prompt length and planning attention remain bundled with the treatment. Report joint
success and feature-only false confidence separately; retain environment errors as unknown outcomes.

Before freezing: obtain supervisor agreement on this narrower question, independently review the
contracts and oracle assumptions, check information parity, extend citation searching, and decide
whether more varied tasks are needed. No model run or positive empirical claim follows from this note.
