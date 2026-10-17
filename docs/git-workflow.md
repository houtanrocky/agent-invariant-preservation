# Git research record

main holds coherent reviewed infrastructure/protocol/source. Suggested branches:
research/week1-foundation, literature/swe-bench-review, experiment/task-t001, analysis/pilot-results,
paper/initial-draft and fix/schema-validation. Use focused conventional messages such as
`research: freeze pilot protocol`, `test: reject duplicate-credit mutant`, or `paper: draft methodology`.

Tag immutable protocol/benchmark freezes (for example protocol-v1, benchmark-v1) and final artifact
releases after review. Never reuse a tag for revised evidence. Keep task baseline SHAs independent of
the research repository commit. Do not amend/rewrite a published research history to conceal failures.

Use `git status --short`, `git diff --check` and `python scripts/check.py --strict` before committing.
Do not commit ignored credentials, downloaded source, databases or large private traces. Raw non-sensitive
records and provenance belong in Git or checksummed artifact storage. Git is not the only research log.
The researcher has configured an origin remote; no push is authorized for local baseline work.
Next: commit baseline/protocol decisions separately from future results.

## Initialization handoff in this managed workspace

The initial restricted session could initialize main but could not create `.git/index.lock`.
The researcher subsequently created `3a5a1c2` (`Initialize`) and configured origin. That foundation
history is retained. Git metadata writes are now available. Use focused follow-up commits:

```text
git status --short
git diff --check
git log --oneline -3
```

Retain the existing configured identity and origin. Do not rewrite history or push without authorization.
The source clone and database-test artifacts are distinct from coding-agent observations; commit names
and paper prose must retain that distinction.
