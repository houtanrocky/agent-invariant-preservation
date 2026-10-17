# Agent adapter and execution boundary

The implemented CommandAdapter accepts argv, an existing workspace, UTF-8 stdin prompt, a positive
wall-clock timeout and an explicit environment mapping. It returns exit/timeout, duration and stdout/
stderr paths. It uses shell=False, streams traces to disk and attempts process-tree termination on
timeout (Windows taskkill; POSIX process group). It does not assume any commercial CLI flags.

The adapter has tests using deterministic Python subprocesses. **No real coding-agent integration has
been verified.** Agent executable/version/model and authentication must be supplied by the researcher.
Use config/agents.example.yaml as a configuration contract; token/cost budgets require a tested external
wrapper or provider mechanism. The adapter enforces wall time only and reports no invented token/cost data.
It does not yet orchestrate a whole funded study or automatically turn CLI output into backend evaluations.

Do not point an agent at this research checkout. `researchctl prepare-workspace RUN-ID` creates a detached
subject worktree at the pin, but cwd and worktrees are **not access controls**: their .git metadata can point
outside the workspace. Use a separate OS account/container/mount exposing only an exported clean subject
and permitted docs. Keep research/oracle/reference files unreachable, end the agent session, capture patch,
then evaluate in a separate trusted environment. An agent must not modify its hidden evaluator.

`researchctl prepare-snapshot RUN-ID --task T001` now creates a history-free export with an explicit
file inventory and hashed shared contract. Use this export for the future containment check; see
[evaluation isolation](../protocol/evaluation-isolation.md). The exporter does not launch an agent,
approve the candidate baseline, or enforce host/network isolation.

Integration checklist:

- [ ] Verify actual documented prompt ingestion/noninteractive contract and version command.
- [ ] Verify explicit model/version, allowed tools, clean session reset and auth via local environment.
- [ ] Enforce recorded wall/time/token/cost budgets and test cancellation/child cleanup on the target OS.
- [ ] Test filesystem/network boundary: agent cannot read research/oracle/reference files or prior sessions.
- [ ] Capture prompts, patch, stdout/stderr, config names, timestamps and available resource measurements.
- [ ] Reset database and run frozen trusted build/feature/invariant evaluations after coding ends.
- [ ] Validate schema and retain attempts/unknowns; do not infer correctness from an agent exit code.

Next: implement one real system wrapper against its verified CLI contract; record the integration test
and cost authorization separately before any paid execution. Never commit authentication tokens.
