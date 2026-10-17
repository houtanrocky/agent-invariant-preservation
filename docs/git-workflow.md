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
No remote or push is authorized. Next: commit baseline/protocol decisions separately from future results.

## Initialization handoff in this managed workspace

Git initialized main, but `.git/index.lock` creation was denied by the read-only metadata policy.
The initial files are untracked and no project commits exist. From a terminal/environment with metadata
write access, review `git status --short` and create the intended logical commits:

```text
git add .gitignore .gitattributes .env.example README.md ROADMAP.md CHANGELOG.md CONTRIBUTING.md LICENSE-DECISIONS.md research literature protocol progress presentation docs
git commit -m "docs: establish research protocol and literature notebook"
git add pyproject.toml src tests scripts config benchmark data analysis .github
git commit -m "feat: add validated research tooling and provenance smoke test"
git add paper artifacts
git commit -m "paper: add manuscript skeleton and infrastructure validation record"
git status --short
git log --oneline -3
```

The existing configured identity should be retained. Do not set a global identity, force history changes
or add/push a remote as part of this handoff. The commands above have not succeeded in the restricted
session, and the commit messages do not imply completed empirical research.
