# First research day

For the current follow-up, begin with [the review package](review-ready-package.md): a repaired
candidate and two executable drafts now exist. The [operational pin now includes the integrated repair](wallet-integration.md).
The checklist below preserves the initial workflow; independent human review and real agent containment
remain outstanding.

1. Install with README commands, run `researchctl doctor`, `researchctl smoke`, and `python scripts/check.py`.
2. Read the proposal and questions. Spend a focused session on LISA/PGS full text; update notes and gap.
3. Run `researchctl setup-target` using the recorded pin. Inspect the source-backed map in
   research/subject-inspection.md and its exact code/test evidence.
4. Read docs/target-baseline.md, including the independently reproduced pre-existing spending defect.
   To repeat setup checks with Docker available, run `python scripts/check_target.py`; it uses isolated
   Testcontainers databases. Never attribute the pre-existing defect to an agent.
5. Build an invariant-to-code/test map; select two meaningful new changes and plan reference/oracle review.
6. Log time, evidence, failed attempts and next actions in progress/daily-log.md; make a focused Git commit.

Expected first-day result: working infrastructure, a more defensible gap and a specific baseline/task
blocker list. Do not aim to manufacture study outcomes. The network and Docker blockers observed at
initialization are historical; the supplied clone and responding Docker engine resolved them in the
follow-up. Your own machine still needs the recorded tools and a clean pinned checkout.
