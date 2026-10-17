# Evaluation isolation and leakage controls

The public subject history and workbench can reveal implementation hints. The research repository
must never be the coding agent's workspace. Removing a file from a checkout does not hide its history.

`researchctl prepare-snapshot RUN-ID --task T001` exports only the exact names in
`benchmark/manifests/shared-files.json` from the task's exact commit. It rejects Git links, symlinks,
unsafe paths and existing output directories. It emits no `.git`, source history, remote configuration,
research reports, workbench, reference solution or held test. The explicit inventory remains subject
to human leakage and information-parity review. Both conditions receive identical source and the
same generated REQUEST.md and CONTRACT.md. File hashes and a content digest are retained outside
the snapshot. A detached worktree remains useful to researchers but is not an agent export.

Reference patches, deliberate faults, held tests, evaluator source and raw validation logs are stored
in a separate researcher-controlled directory outside this public checkout. Public packages contain
hashes and execution summaries only. The local locator is `config/evaluator.local.yaml` (ignored).
Back up this directory privately; cloning the public repository alone does not reproduce held checks.

Before any agent execution, a separate account/container must expose only one exported snapshot,
the selected prompt and allowed tools. Deny host filesystem access, the Docker socket, researcher
credentials, other sessions and repository/remotes/web browsing. Preinstall dependencies before
network isolation. No launcher or tested real-agent containment is provided by this exporter; enforce
and probe those boundaries with the actual selected agent wrapper before recording an observation.

After the agent stops, collect only allowlisted production-source changes. Reject symlinks, changed
tests, migrations outside the approved task scope, environment scripts and evaluator replacements.
Apply the patch to a fresh trusted evaluator snapshot; mount held checks there and reset disposable
database fixtures. Run builds, feature assertions and invariant assertions separately. Never accept
the agent's test output as the held verdict. Keep every attempt, timeout and environment failure.

Local copies of hidden files remain accessible to a host-level agent with unrestricted permissions.
Paths and `.gitignore` are organizational safeguards, not security boundaries. Main runs remain gated
on a demonstrated boundary. Public task wording and historical source can still contaminate model
training; isolated snapshots reduce retrieval leakage but cannot establish absence of prior exposure.
