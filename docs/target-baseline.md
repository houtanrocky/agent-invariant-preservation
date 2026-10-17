# Dragon Market baseline verification — 2026-10-17

Subject commit: `162c5cab9fa886445dd102f4a99961027f90aebb`. Origin:
<https://github.com/houtanrocky/dragon-market>. The researcher supplied the clone under
`.local/dragon-market/`; `researchctl setup-target --discover-pin` verified the origin, recorded the
exact commit and checked out that commit detached. Tracked subject files were clean before and after
execution. No subject code, migrations or tests were changed.

The module specifies Go 1.25.0. Checks ran on Windows using Go 1.26.0 and Docker Desktop's Linux engine
29.1.5. PostgreSQL was provisioned by the existing Testcontainers TestMain, using fresh disposable
databases and migrations 1–10. No Compose development database was started or reset. The observed
`postgres:16-alpine` resolution before and after execution was
`postgres@sha256:e013e867e712fec275706a6c51c966f0bb0c93cfa8f51000f85a15f9865a28cb`.
The upstream harness uses a mutable image tag and default database isolation through `BeginTx(ctx, nil)`;
the execution evidence records these settings rather than pretending the harness pins a digest/isolation.

| Check | Outcome |
| --- | --- |
| `go build -mod=readonly ./...` | Passed |
| `go test -mod=readonly -json -count=1 -timeout=5m ./...` | Passed; 92 pass events including 8 subtest events; no failures/skips |
| Targeted KNOWN-01 characterization | Passed and emitted `KNOWN-01 CONFIRMED`; the defect was reproduced |
| `go test -mod=readonly -race -json -count=1 -timeout=5m ./...` | Passed; 92 pass events including 8 subtest events; no failures/skips |
| `go vet -mod=readonly ./...` | Passed |

Commands, timestamps, durations, environment and checksums are in the committed
[machine-readable report](../artifacts/target-baseline/162c5cab9fa886445dd102f4a99961027f90aebb/report.json).
Nonempty raw JSONL outputs are archived alongside it. Empty stdout/stderr streams retain their hashes
in the report; originals remain under ignored `.local/baselines/20261017T073715Z-d92279cd/`.
The artifact manifest records the archived files. This is subject setup evidence, **not a coding-agent run**
and not part of `data/raw/` or the manuscript's empirical results.

## Pre-existing invariant violation

The test `TestKnownIssuePriorDayReleaseReducesTodaySpending` starts with a prior-day reservation of
500, spends 300 today, releases the old reservation, then spends another 500 under a daily limit of 500.
It passes because it observes that flawed behavior: total current-day spending is 800 while the stored
daily counter is 500. The reproduction is independently present in this execution's raw output.
This must never be counted as a passing daily-limit invariant or an agent-introduced defect.

T007 remains a candidate blocked for scoring preservation of that bound. Before main collection,
either exclude the affected requirement/task, adopt a separately reviewed fixed baseline with a new
pin, or explicitly preregister a distinct repair-study design. Removing the failing behavior's test
without replacing its specification would conceal evidence and is not an acceptable resolution.

## Reproduce and continue

From the research checkout with the Python package installed, Go and Docker available:

```text
researchctl setup-target
python scripts/check_target.py
researchctl status
```

The script requires a clean checkout at the configured SHA, uses read-only Go module resolution,
and saves every invocation to a new ignored directory. It runs commands sequentially, preserving
nonzero outcomes and logs. Inspect a new report before archiving it; do not overwrite the current
execution evidence. Python infrastructure checks remain independent of Docker and the target.

Next: review [source-backed task eligibility](../research/subject-inspection.md), define concrete new
changes and validate references/oracles. All eight tasks remain candidates; no human review or agent
integration is implied by passing the baseline commands.
