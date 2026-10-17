# Literature search strategy and screening record

Scope: coding agents modifying repositories; invariant/property-oriented evaluation; transactional
correctness; oracle strength and benchmark validity. Search ACM DL, IEEE Xplore, arXiv, DBLP and
institutional repositories. Scholar can discover sources; verify metadata with original authors/publishers.

Queries: `(coding agent OR repository-level LLM) AND (invariant OR transaction OR regression)`;
`(LLM code generation) AND (property-based OR metamorphic testing)`; `(agent benchmark) AND
(oracle OR contamination OR validity)`; `(database isolation) AND (anomaly OR concurrency testing)`.
Include empirical methods, foundational oracle techniques and closest recent overlaps. Exclude
marketing claims, unverifiable citations and unrelated single-function accuracy without stating why.

On 2026-10-17, supplied URLs plus targeted searches for oracle surveys, isolation critique, metamorphic,
mutation, regression, Chess and Elle were screened through primary/institutional sources. Fourteen
version-specific records were initialized. This was seed discovery, **not an exhaustive systematic search**;
result counts and full-text eligibility were not recorded and must not be fabricated retrospectively.

For future searches log date/database/exact query/filters/result count; record deduplication, inclusion
decision and reason per candidate. Snowball references and citing papers from PGS/LISA/SWE-Bench+.
Maintain a novelty-overlap table: change unit, state setting, intervention, oracle, data and limitations.
Next: perform a documented full-text pass and record negative overlap findings as carefully as supportive ones.
