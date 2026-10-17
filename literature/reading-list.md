# Reading list and paper-reading workflow

All entries have linked metadata checked on 2026-10-17. PGS v1/v2 and LISA received a targeted full-text
method/evaluation review on 2026-10-18; see [the comparison](pgs-lisa-comparison.md). Other critical reading is pending. The
matrix distinguishes publication dates and preprint versions. Missing details remain TO VERIFY.
No extracted number should enter this study's results.

1. Read SWE-bench, SWE-agent and SWE-Bench+ for task construction, execution and validity concerns.
2. Read PGS v1/v2 and LISA together; these are the closest overlap checks before claiming novelty.
3. Read QuickCheck, the oracle survey, mutation and metamorphic surveys for oracle construction.
4. Read isolation critique, Elle and Chess for state/history assertions and concurrency limits.
5. Read the regression survey for preservation under change and suite-management tradeoffs.

For each paper: verify the version, create/update a note from reading-notes/template.md, read in two
passes (problem/design, then methods/limitations), record source locations, update the CSV, synthesize
cross-paper contrasts in related-work.md, and log remaining questions. Commit reasoning, not just PDFs.

The requested title “Use Property-Based Testing to Bridge LLM Code Generation and Validation” matches
[arXiv v1](https://arxiv.org/abs/2506.18315v1). [v2](https://arxiv.org/abs/2506.18315v2) changes both title
and author list. Both are tracked separately. LISA's arXiv page reports ISSRE 2026 acceptance; final
proceedings metadata remain TO VERIFY. Avoid silently treating preprints as verified published versions.

Next: independently review the comparison, audit artifacts/appendices, and continue citation searching.
