# Review package — 2026-10-18

This package prepares the next research decisions. It contains no coding-agent study observations,
human signatures or main-study results. Review against the exact recorded SHAs and artifact hashes.

| Deliverable | Evidence | Remaining decision |
| --- | --- | --- |
| Correctness baseline | [Review](transactional-correctness-baseline-review.md) and [integration](wallet-integration.md) | Independent human approval of integrated `f4ba211`; operational pin updated at user's request |
| Purchase retries | [T001 reference/oracle package](../benchmark/packages/T001/README.md) | Independent reference, expected-state and fault-sensitivity review |
| Bid cancellation retries | [T002 reference/oracle package](../benchmark/packages/T002/README.md) | Same review, including expiry and settlement |
| Leakage control | [Isolation protocol](../protocol/evaluation-isolation.md) | Inventory, prompt parity and actual agent containment review |
| Scientific framing | [PGS/LISA comparison](../literature/pgs-lisa-comparison.md) | Supervisor agreement on the bounded question and continued searching |

Each task package contains rendered A/B prompts and hashes in `prompts.json`, plus the concrete
shared-input inventory in `shared-inputs.json`. Both are review drafts. References start separately
from the candidate; neither includes the other feature. Held task scoring excludes daily-limit behavior.
Both faulty variants pass feature checks and fail persisted-state assertions.

Ignored `config/evaluator.local.yaml` locates the private source bundle, reference/faulty patches,
held checks, validation script and raw logs. Back them up privately. The public checkout alone cannot
reproduce hidden evaluations. The same assistant authored references and checks; independent review
is outstanding. Inspect private artifacts rather than relying only on public summaries.

```powershell
.venv/Scripts/python -m researchctl status
.venv/Scripts/python -m researchctl validate-task benchmark/tasks/T001.yaml
.venv/Scripts/python -m researchctl validate-task benchmark/tasks/T002.yaml
.venv/Scripts/python scripts/check.py --strict
```

`validate-task --require-validated` intentionally fails until human reference review, a named reviewer
and rationale evidence exist. Record decisions before promoting metadata. Real agent adapters,
filesystem/network containment, pilot feasibility and preregistration remain later gates. The main
study has not been launched.
