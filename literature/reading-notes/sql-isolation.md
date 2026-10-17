# A Critique of ANSI SQL Isolation Levels

Status: metadata and abstract screened on 2026-10-17; **full-text review pending**.
This is an initial note, not a completed critical review.

- Authors: Hal Berenson; Phil Bernstein; Jim Gray; Jim Melton; Elizabeth O'Neil; Patrick O'Neil.
- Year/status: 1995; SIGMOD 1995 pp.1-10; MSR-TR-95-51; arXiv deposited 2007.
- Source/version: <https://arxiv.org/abs/cs/0701157>.
- DOI: TO VERIFY; omitted from BibTeX.
- Complete bibliography: metadata above and paper/references.bib; any unlisted proceedings details TO VERIFY.
- Research problem/focus: database isolation anomalies (abstract-level).
- Research questions: TO VERIFY explicit formulation in full text.
- Methodology: formal analysis of isolation phenomena (abstract-level; detailed design TO VERIFY).
- Dataset/experimental environment: SQL isolation definitions and snapshot isolation.
- Evaluation metrics: TO VERIFY exact definitions and denominators.
- Main findings: source abstract describes: Shows shortcomings in phenomenon-based isolation definitions and defines additional phenomena. No numerical outcomes extracted or independently replicated.
- Limitations: Specific PostgreSQL behavior cannot be inferred from isolation labels alone.
- Threats to validity: TO VERIFY author discussion; assess oracle quality, sampling and confounding.
- Relevance to this study: Use history predicates rather than treating transaction syntax as proof.
- Possible overlap with novelty claim: compare whether it studies coding-agent maintenance of existing
  transactional requirements, the same intervention, and independent hidden correctness oracles.
- Questions to investigate further: What is independently evaluated? What failures can the oracle miss?
  Does its setting justify transferring any claims to a stateful Go backend?
- Reproduction/artifacts/license: TO VERIFY before download or reuse.

Next: read the full paper, add page/section citations, distinguish author claims from own interpretation,
and update literature-matrix.csv. Do not cite this note as experimental evidence.
