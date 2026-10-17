# Data policy

raw/ contains reviewed non-sensitive **observations only**; currently none. Store one immutable run
object per file or unique-ID JSONL batches, following schemas/run.schema.json. processed/ contains
regenerable outputs with commands, input hashes, code commit and environment provenance.

examples/synthetic-runs.json is **SYNTHETIC SOFTWARE-TEST DATA — NOT RESEARCH RESULTS**.
It tests analysis software and is refused by default summaries. Demo executions use data_kind=infrastructure
and live under ignored .local/demos/. Neither automatically populates the manuscript.

Run `researchctl validate-data PATH` before analysis. Semantic checks enforce the primary outcome,
completed invariant coverage, environment-error distinction, unique run IDs, dates and observed task pins.
For observations, the referenced task must have validation evidence. A schema does not prove truthful data.

Missing tokens/cost/tool interactions remain null. Preserve failures and original traces. Corrections
append a linked record and rationale; do not overwrite the original. Large/private logs use artifacts/manifest.csv
with immutable storage locations and checksums. Next: define a raw-observation review/sign-off procedure.
