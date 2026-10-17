# First research day

1. Install with README commands, run `researchctl doctor`, `researchctl smoke`, and `python scripts/check.py`.
2. Read the proposal and questions. Spend a focused session on LISA/PGS full text; update notes and gap.
3. Resolve terminal network access, then run `researchctl setup-target --discover-pin`; inspect the exact
   commit, go.mod, migrations, ADRs and tests before making implementation claims.
4. Start Docker/PostgreSQL as required by the pinned subject docs. Run baseline build/tests and record
   commands, versions, exit codes and failures; never attribute pre-existing failures to an agent.
5. Build an invariant-to-code/test map; select two meaningful new changes and plan reference/oracle review.
6. Log time, evidence, failed attempts and next actions in progress/daily-log.md; make a focused Git commit.

Expected first-day result: working infrastructure, a more defensible gap and a specific baseline/task
blocker list. Do not aim to manufacture study outcomes. The network and Docker blockers observed at
initialization are recorded in environment-inspection.md and must be reassessed on your machine.
