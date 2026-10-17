# Machine-readable contracts

task.schema.json describes candidate/validated task metadata; run.schema.json records completed and
unevaluated attempts; task-evidence.schema.json links validation reports and hashed evidence artifacts.
JSON Schema Draft 2020-12 provides structural validation; researchctl adds cross-field and provenance checks.
The four *-config schemas validate study targets, agent examples, environment controls and subject metadata.

All run fields are required so missing measurements are explicit nulls. Controlled outcomes and failure
categories prevent accidental status conflation. Schema version 1.0 is part of every task/run record.
Next: version any incompatible schema change and supply a documented migration without rewriting raw data.
