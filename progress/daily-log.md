# Daily research log

## 2026-10-17 — infrastructure initialization

Time spent: TO RECORD by researcher (automated build duration is not researcher effort).
Work: foundation and protocol drafted; sources screened at metadata/abstract level; CLI and smoke prepared.
Papers studied: metadata/abstract screening only, not full-text reading. Experiments: no agent/main-study runs.
Observations/problems: terminal network blocked subject clone; Docker daemon and LaTeX unavailable;
Windows temporary-directory permissions affected installation. Decisions: see D001–D005 and validation report.
Git commits: none; managed `.git` write restriction blocked staging/commit. Strict checks: 40 tests passed,
1 explicit environment-prerequisite skip, formatting/static/schema/structure checks passed. The actual
smoke and synthetic figure export passed; neither is research evidence. Next: Git handoff, full-text
overlap check and pinned baseline. See docs/validation-report.md for all limitations.

## 2026-10-17 — supplied subject inspected and baseline executed

Time spent: TO RECORD by researcher. The researcher supplied the clone, foundation commit `3a5a1c2`
and remote before this follow-up. Work completed: pinned subject
`162c5cab9fa886445dd102f4a99961027f90aebb`, inspected code/contracts/migrations/tests/license, and
updated all eight candidate assessments. No subject source changes and no agent-study runs occurred.

Experiments/checks: actual Go build, full test, targeted known-issue characterization, race-enabled test
and vet commands passed. Each full suite recorded 92 passing test/subtest events, including 8 subtests.
KNOWN-01 was reproduced; it is a pre-existing daily-limit violation and remains unresolved. Small raw
outputs and checksummed environment metadata are archived under artifacts/target-baseline/ at the pin.
Problems resolved: Docker responds, Git writes work and the previously skipped local clone test passes.
Updated Python infrastructure: all 41 tests pass without skips; formatter/static/schema checks pass.
Decisions: D006–D008. Papers studied: no new full-text review claimed. No model/token/cost results exist.
Git commits: see local history for follow-up tooling and pinned evidence; no push performed.
Next actions: human scope/contract review, KNOWN-01 decision, export policy, then two validated tasks.

## Daily entry template

- Date and time spent:
- Work completed:
- Papers studied (versions/pages and note links):
- Experiments performed (all attempts and run IDs):
- Observations:
- Problems encountered and failed approaches:
- Decisions made, alternatives and rationale:
- Git commits and evidence artifacts:
- Next actions and blockers:

Record reasoning and adverse evidence as well as successful changes. Next: add the first researcher-led entry.
