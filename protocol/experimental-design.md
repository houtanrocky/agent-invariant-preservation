# Experimental design — draft

Use a controlled 2-condition comparison blocked by task and agent system. The provisional maximum is
8 × 2 × 2 × 3 = 96 main executions. Repetitions are independent sessions, not independent sampled tasks.
No task is validated yet; the design is not frozen or statistically powered.

Both conditions receive the same feature request, source commit, public project documentation and
requirements contract. B adds a structured attention/checking procedure referencing those requirements.
The manipulation is salience and workflow, not privileged correctness information. Prompt length and
attention are bundled in the intervention; do not attribute an effect to one mechanism alone.

Pilot two validated tasks, both systems, both conditions, initially one execution per cell (8 pilot runs).
Use the pilot to assess budgets, feasibility, oracle discrimination and the defensible sample size.
Keep pilot data separate, including if a task is later reused. Update the protocol before main outcomes.

After freeze, enumerate task × agent × condition × repetition cells and randomize their order using
the recorded seed. Balance order within task/system blocks across execution batches. Never run A then
B in a shared agent conversation. Record schedule, session identity and any provider drift.

Each run starts from the exact task SHA in an isolated environment, with reset database and pinned
dependency versions. No automatic retries; environment recovery creates linked attempts, preserving
original evidence. Human editing of an agent patch disqualifies it from being an unassisted outcome.

Next: finish two task gates, review manipulation parity, confirm both system contracts, and freeze a
schedule and versioned preregistration. See the analysis plan for the estimand and dependence assumptions.
