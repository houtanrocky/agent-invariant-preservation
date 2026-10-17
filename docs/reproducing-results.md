# Reproducing infrastructure and future study results

At initialization there are **no empirical results to reproduce**. After installation, run
`researchctl reproduce` to display executable infrastructure steps, or `researchctl reproduce --run`
to run unit tests and a fresh provenance smoke test. `python scripts/check.py` checks the full fast suite.

Smoke output: run.json, summary.json, trace/stdout.txt, trace/stderr.txt and manifest.json under .local/demos/.
Verify the manifest checksums and data_kind=infrastructure. Repeating it yields fresh IDs/timestamps;
the fixture assertion results are deterministic. No paid API, Docker or downloaded subject is involved.

Future empirical reproduction needs the frozen research commit, task manifest, exact subject SHA,
resolved environment, database fixtures, agent/model versions, prompt hashes, original attempt records
and evaluator histories. Regenerate descriptive.py/statistical_analysis.py outputs from observations;
record input/output hashes and code/environment. Hosted models may drift or cease to be available;
re-evaluation of preserved patches should remain possible even if regeneration is not.
Baseline subject verification is now documented in target-baseline.md and executable with
`python scripts/check_target.py`; its command results and KNOWN-01 reproduction are setup evidence,
not coding-agent study outcomes. Next: add exact task-specific commands as tasks become validated, without pretending
that current schema checks reproduce a transactional experiment.
