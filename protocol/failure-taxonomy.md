# Failure taxonomy and review procedure

| Category | Candidate evidence |
| --- | --- |
| feature | Required new behavior rejected by functional oracle |
| atomicity | Failed operation leaves partial committed effects |
| idempotency | Repeated operation duplicates a committed effect |
| concurrency | Recorded interleaving violates the declared history predicate |
| ownership | Final owner/listing state violates the contract |
| balance | Conservation/availability/nonnegativity predicate fails |
| spending_limit | Effective limit or reset rule violated |
| audit | Missing, duplicate or non-atomic audit linkage |
| build | Agent-introduced compilation failure |
| timeout | Execution budget exhausted; outcome not silently treated as tested |
| environment | Evaluation prevented by setup/infra failure |
| unclassified | Failure preserved pending evidence review |

Label using assertions and traces, not assumptions about model intent. Keep multiple secondary labels
in the failure review and one primary category in the record. If a reviewer discovers an oracle defect,
version the correction, reevaluate all affected conditions and preserve old outcomes. A second reviewer
should independently code a subset if available; record disagreements and adjudication.
Next: classify pilot counterexamples and refine categories before freeze.
