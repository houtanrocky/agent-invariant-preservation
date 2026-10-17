# Preserving Transactional Invariants in AI-Assisted Software Development

**An Empirical Study of Coding Agents on Stateful Backend Systems**  
Researcher: **Houtan Rocky** · MSc foundation · initial horizon: four weeks.

How reliably can coding agents modify stateful backends while preserving existing transactional invariants?
This repository supports a **planned study**, from paper reading through provenance-preserving execution,
analysis and manuscript preparation. There are **no empirical results and no validated benchmark tasks yet**.
The intervention hypothesis is that invariant-oriented guidance improves correctness; it remains untested.

## Quick start

Python 3.11+ and Git are required. From this checkout, create and use an environment:

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -e ".[dev,plots]"
.venv\Scripts\researchctl doctor
.venv\Scripts\researchctl smoke
.venv\Scripts\python scripts/check.py
```

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -e '.[dev,plots]'
.venv/bin/researchctl doctor
.venv/bin/researchctl smoke
.venv/bin/python scripts/check.py
```

No paid API or database is needed for infrastructure tests. Run `researchctl --help` for all commands.
This workspace already has a tested `.venv`; invoke its executables directly. If standard pip setup
fails in the managed Windows sandbox, use the tested [offline fallback](docs/troubleshooting.md).
`researchctl summarize` reads only `data/raw/` by default and reports no observations when empty.
To test analysis explicitly: `researchctl summarize data/examples/synthetic-runs.json --allow-nonresearch`.
Demo outputs go to ignored `.local/demos/`, with records, traces, summaries and SHA-256 manifests.

## Start the actual research

Read [the roadmap](ROADMAP.md), [proposal](research/proposal.md), [design](protocol/experimental-design.md),
[literature list](literature/reading-list.md), and [environment report](docs/environment-inspection.md).
Use `researchctl status` to inspect outstanding validation. The maximum provisional design is
8 tasks × 2 agent systems × 2 conditions × 3 repetitions = 96 main-study executions; pilot runs are separate.
This is a feasibility ceiling, not a justified sample size.

Dragon Market is the intended subject: <https://github.com/houtanrocky/dragon-market>.
The operational target pin is now `f4ba21185d1ba7b4bbb56f5addcc27d1b75bdec7`, integrating the repaired
wallet into Dragon Market's current deployment code. The user authorized fixing and publishing it.
The [historical baseline report](docs/target-baseline.md) preserves the old `162c5ca` failure;
the [integration verification](docs/wallet-integration.md) records the new checks and pin decision.
Independent human baseline approval remains pending; an operational pin update does not approve a study.

Two executable draft packages now have references, separate feature/state checks and rejected faulty
variants: [purchase retries](benchmark/packages/T001/README.md) and
[bid cancellation retries](benchmark/packages/T002/README.md). Each reference passes existing-suite,
race and vet checks. Both faulty variants pass features but fail state assertions. Private patches,
oracles and raw logs are held outside this public repository; only hashes and summaries are public.
Neither task is human-validated. The other six candidates remain deferred.

The [PGS/LISA comparison](literature/pgs-lisa-comparison.md) narrows the proposed contribution.
`researchctl prepare-snapshot RUN-ID --task T001` exports an explicit, history-free shared inventory;
real agent filesystem/network containment remains to be demonstrated. `setup-target` prepares the
integrated repair. The task packages retain their exact `58913f2` starting snapshots and evidence;
they do not silently inherit results from a different revision. Do not start agent runs until review,
isolation and protocol gates pass.

## Repository map

- `research/`, `literature/`, `protocol/`: questions, evidence and controlled study decisions.
- `benchmark/`, `config/`: candidate tasks, schemas, subject pin and environment controls.
- `src/researchctl/`, `tests/`, `scripts/`: working research automation and independent infrastructure tests.
- `data/`, `experiments/`, `artifacts/`: observations, reviews and provenance; raw evidence is retained.
- `analysis/`, `paper/`, `presentation/`: real-data analysis, LaTeX source and supervisor communication.
- `progress/`, `docs/`: daily reasoning, weekly deliverables and operating instructions.

`python scripts/check.py` runs available infrastructure checks. `--strict` also requires Black/Pyflakes;
CI installs both and runs strict checks on Windows and Linux. LaTeX has a separate CI job.
Real agent integration, independent oracle review, statistical inference and manuscript results remain pending.
See [licensing decisions](LICENSE-DECISIONS.md) before redistribution. The researcher initialized the
foundation commit and configured the remote after the initial restricted session. Current Git writes
are available; no push is performed as part of local baseline verification.
