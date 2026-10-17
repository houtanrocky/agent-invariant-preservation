# Research proposal

**Researcher:** Houtan Rocky. **Status:** planned MSc study; no empirical findings.
**Title:** Preserving Transactional Invariants in AI-Assisted Software Development: An Empirical Study of Coding Agents on Stateful Backend Systems.

Coding agents can propose repository-wide changes, but a feature can appear correct while damaging
financial state, retries, rollback or ownership under concurrent execution. We will study whether such
agents preserve explicitly specified pre-existing invariants when implementing bounded backend changes.
The intended subject is Dragon Market, a public Go backend. Its suitability remains conditional on
source inspection, reproducible baseline tests, and validated feature-change tasks.

RQ1 measures joint feature and invariant success. RQ2 compares standard and invariant-oriented guidance.
RQ3 categorizes observed violations. RQ4 explores resources and correctness without claiming causality.
The preliminary hypothesis predicts a positive effect of guidance; rejection or uncertainty are valid outcomes.

The provisional ceiling is eight tasks, two agent systems, two prompt conditions and three independent
executions per cell (96 main runs). Tasks and systems are selected purposively, so conclusions concern
this bounded setting. Task and agent blocks support comparisons; repeated runs are nested observations.
Pilot runs are labeled and excluded from confirmatory analysis. No power justification exists yet.

Each accepted task needs a pinned baseline, a feature instruction, a human-reviewed reference solution,
functional and invariant tests, and a test-rejected deliberate defect. Evaluation occurs outside the agent
workspace. The primary binary outcome is feature correctness AND all required invariants, with each
component retained. Environment errors remain unresolved outcomes pending investigation.

Expected deliverables are a validated small benchmark, auditable run records, a cautious empirical
comparison, a failure taxonomy and a reproducible manuscript. These are intended contributions.
Week 1 establishes evidence and two tasks; week 2 completes validation and freezes the protocol;
week 3 executes runs; week 4 analyzes and communicates. Reduce scope rather than weaken validation.

Next: inspect the pinned code; read the closest invariant-testing and benchmark-validity papers in full;
ask a supervisor to review the gap and two pilot tasks before committing to the main study.
