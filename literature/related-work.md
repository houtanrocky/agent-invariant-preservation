# Related-work synthesis — preliminary abstract screening

Repository agents: SWE-bench supplies repository issue-resolution tasks; SWE-agent studies an interface
for interacting with code and tools. Our planned outcome separates requested-feature checks from
preservation of pre-existing state constraints. This is a study-design distinction, not proof of novelty.

Oracle validity: SWE-Bench+ motivates inspecting apparent passes. The oracle survey provides terminology
for the difficulty of recognizing correct behavior; mutation and metamorphic testing suggest complementary
oracle checks. A rejected deliberate defect supplies evidence of discrimination, not complete adequacy.

Properties and invariants: PGS uses property-based feedback for LLM refinement; LISA generates invariant
tests for functional bugs. The [targeted full-text comparison](pgs-lisa-comparison.md) now narrows this
study to fixed-contract planning guidance during transactional maintenance. Do not claim that
invariant-guided LLM evaluation is new. Other literature still needs full-text critical review.

Stateful correctness: the isolation critique and Elle motivate histories and anomaly predicates; Chess
motivates systematic schedule exploration and counterexample reproduction. None alone establishes
that this project's future database oracles are sound. Regression testing connects preservation to change.

Sources and checked metadata: literature-matrix.csv and individual linked reading notes. All passages
above are a preliminary synthesis, not a systematic-review conclusion.
Next: add full-text evidence, competing studies and explicit disagreements before reusing prose in the paper.
