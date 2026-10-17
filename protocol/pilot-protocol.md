# Pilot protocol

Entry: two validated tasks, passing baseline/reference checks, rejected meaningful mutants, two tested
system adapters and independently reviewed A/B information parity. No paid execution is automatic.

Start with one independent run per task × system × condition (8 pilot sessions). Preserve order,
prompts, patches, evaluations, all failed attempts and trace checksums. Run clean database fixtures and
repeat concurrency schedules to identify nondeterminism. Investigate suspicious passes manually.

Exit questions: Is the feature genuinely new? Can an independent reviewer reproduce each oracle?
Are budgets comparable and sufficient? Are outcomes variable enough for a useful comparison? Can
the remaining tasks be validated in week 2? Reassess sample size, detectable effects and scope.
Freeze revised protocol, tool/model versions and analysis rules before main collection.

Pilot runs remain in experiments/pilot and never enter main descriptive summaries by default.
Next: fill a dated pilot report with blockers, decisions, timing and linked artifacts.
