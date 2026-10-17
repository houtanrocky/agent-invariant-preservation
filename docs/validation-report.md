# Foundation validation record — 2026-10-17

**Historical initialization record.** The initially blocked subject and Git states below have changed:
see the follow-up at the end and [the executed target baseline](target-baseline.md). Initial artifacts
remain preserved with their original counts and limitations.

This file records infrastructure verification, not empirical findings. No Dragon Market agent run or
benchmark task is validated. The working foundation is implemented; the empirical study remains planned.

Installation was exercised using a real editable wheel and uv into `.venv`, with inherited installed
PyYAML/jsonschema dependencies. Standard pip/ensurepip failed under this managed Windows sandbox because
CPython 3.13 mode-0700 temporary directories denied access. A local, ignored build helper restricted to
`.local/` used inherited workspace ACLs for disposable build directories; setuptools produced the actual
editable wheel, and uv installed it offline. No global Python/Git configuration was modified.

The installed `researchctl doctor` and `researchctl smoke` executed. The smoke checked a deterministic
transfer fixture, validated its record, emitted a summary and preserved traces plus checksums under
`.local/demos/`. Tokens/cost/tool counts remained null. The output is infrastructure data only.

Initial tests exposed Windows cleanup timing/readonly-file issues, which were corrected. Git local
cloning still cannot execute its MSYS upload-pack shell in this sandbox. That prerequisite-specific
test is explicitly skipped only for the observed signal-pipe error; all other clone errors remain failures.
An existing artificial Git checkout was used to execute real pin discovery, clean-state checks and
detached worktree creation. Its commit is a software-test fixture, never the Dragon Market baseline.
LaTeX compilation has not occurred because pdflatex/BibTeX are absent. A separate CI job will compile
the manuscript when run in GitHub; creating CI does not prove that hosted CI has run.

Subject checkout/build/tests are blocked: terminal network proxy unreachable, source/commit browser
endpoints inaccessible, Docker engine unavailable. The subject README is a discovery source only.
The baseline commit remains null rather than invented. No upstream changes, remote or push occurred.

Executed acceptance checks:

| Check | Observed outcome |
| --- | --- |
| Editable wheel build and offline uv installation | Passed; actual installed console entry point used |
| `python scripts/check.py --strict` | Exit 0; 41 tests discovered, 40 passed, 1 explicit sandbox-prerequisite skip |
| Black 25.9.0 formatting | Passed, 17 Python files unchanged at final check |
| Pyflakes 3.2.0 static analysis | Passed, no reported findings |
| Task, run, evidence and four configuration schemas | Schema definitions valid; candidate/example configs/data checked |
| Structure, local Markdown links, Python syntax/whitespace and TeX input/citation keys | Passed |
| Installed `researchctl smoke --output .local/acceptance-demo` | Passed; evaluated actual deterministic command and wrote provenance/checksums |
| Candidate `validate-task --require-validated` | Correctly refused incomplete task with readable missing-gate report |
| Synthetic summary without opt-in | Correctly refused; no example data enter observation summaries |
| Default observation summary | Empty observations, no manufactured rates or token/cost values |
| Matched synthetic analysis with bootstrap requested | Ran; labeled nonresearch, declined interval for only one task |
| Matplotlib PDF/SVG export and captions | Passed on explicit synthetic opt-in; output/caption hashes rechecked |
| `setup-target --discover-pin` against intended upstream | Implemented command returned network prerequisite error; no SHA recorded |
| `python scripts/build_paper.py` | Explicitly refused: pdflatex unavailable; manuscript compilation remains unverified locally |

Smoke run ID: `demo-eb97a1e0ae3845c08b35e5d59858f7e5`. The original run/summary/traces/manifest are retained
under `.local/acceptance-demo/`. Synthetic figures are retained under ignored `analysis/output/` and
never copied to the manuscript. See artifacts/manifest.csv for integrity pointers and access labels.

The installed environment uses Python 3.13.9, PyYAML 6.0.3, jsonschema 4.26.0, Black 25.9.0 and
Pyflakes 3.2.0. Installation used inherited system-site dependencies because network access is unavailable;
a fresh fully isolated dependency installation and hosted Windows/Linux CI were not executed here.
The exact tested fallback commands are in troubleshooting.md; normal setup scripts are provided for
PowerShell and POSIX. Git ignore assertions and final status are checked before handoff.

Not completed: exact subject pin/source inspection, baseline Go build/tests and database integration;
real coding-agent CLI verification and budget wrappers; human references and hidden backend oracles;
full-text literature review; preregistration/sample-size justification; pilot/main executions; empirical
analysis and manuscript findings; local TeX compilation; project licensing and external release.
These are research/prerequisite gates, not simulated successes. Token/cost enforcement is delegated to
a future verified agent wrapper; the generic adapter currently enforces only wall time.

Git handoff: `git init -b main` succeeded and an existing configured identity was preserved. Staging and
commit creation were attempted, but the managed workspace's read-only `.git` policy denied creation of
`.git/index.lock`. Therefore **there are no project commits or commit hashes**, HEAD is unborn on main,
and all 145 foundation files are untracked. No lock file was left behind. Git status and other read-only
inspection work. Local test-fixture commits under ignored .local/ are unrelated to project history.

Run the commands in git-workflow.md from an environment permitting `.git` writes to create the logical
foundation commits. No permission bypass, global identity change, remote, push or external publication
was performed. This Git limitation remains incomplete at handoff; it is not a clean committed repository.

## Follow-up: supplied checkout and restored environment

The researcher subsequently created foundation commit `3a5a1c2` and configured the research remote.
Those were present when follow-up work began. The current session can write Git metadata, and the
local clone test that was previously skipped now passes. No remote was created or pushed by this session.

`researchctl setup-target --discover-pin` verified and recorded subject SHA
`162c5cab9fa886445dd102f4a99961027f90aebb`. The actual Go build, full test suite, targeted known-issue
reproduction, race-enabled suite and vet commands all exited zero. Both full test invocations have 92
passing test/subtest events (8 are subtests), zero failures and zero skips. The known-issue reproduction
emitted `KNOWN-01 CONFIRMED`; an intended daily-limit invariant is already violated. This is not an
agent correctness outcome. Raw nonempty logs and environment/checksum metadata are committed under
artifacts/target-baseline/162c5cab9fa886445dd102f4a99961027f90aebb/.

The updated strict Python check passed all 41 tests without skips, including real local clone/pin/worktree
integration. Black, Pyflakes, schemas, task metadata and documentation checks passed. Tests now isolate
their unpinned fixtures from the real study pin; repeated setup preserves a recorded review status.
The CLI status reads the matching archived baseline report rather than always claiming execution is pending.
No task has been promoted, and no new agent observation was added. TeX compilation, real agent integration,
human reference/oracle review, protocol freeze and empirical work remain pending.

Next: review candidate eligibility, public-source exposure and KNOWN-01 handling before the pilot.
