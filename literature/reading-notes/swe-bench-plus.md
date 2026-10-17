# SWE-Bench+: Enhanced Coding Benchmark for LLMs

Status: metadata and abstract screened on 2026-10-17; **full-text review pending**.
This is an initial note, not a completed critical review.

- Authors: Reem Aleithan; Haoran Xue; Mohammad Mahdi Mohajer; Elijah Nnorom; Gias Uddin; Song Wang.
- Year/status: 2024; arXiv v2; venue TO VERIFY.
- Source/version: <https://arxiv.org/abs/2410.06992v2>.
- DOI: 10.48550/arXiv.2410.06992.
- Complete bibliography: metadata above and paper/references.bib; any unlisted proceedings details TO VERIFY.
- Research problem/focus: agent benchmark validity (abstract-level).
- Research questions: TO VERIFY explicit formulation in full text.
- Methodology: manual review of successful patches (abstract-level; detailed design TO VERIFY).
- Dataset/experimental environment: SWE-bench and variants.
- Evaluation metrics: TO VERIFY exact definitions and denominators.
- Main findings: source abstract describes: Reports solution leakage and weak-test concerns in apparently successful resolutions. No numerical outcomes extracted or independently replicated.
- Limitations: Sampling and manual-labeling limitations TO VERIFY; not a universal benchmark failure claim.
- Threats to validity: TO VERIFY author discussion; assess oracle quality, sampling and confounding.
- Relevance to this study: Require mutants and manual suspicious-pass review.
- Possible overlap with novelty claim: compare whether it studies coding-agent maintenance of existing
  transactional requirements, the same intervention, and independent hidden correctness oracles.
- Questions to investigate further: What is independently evaluated? What failures can the oracle miss?
  Does its setting justify transferring any claims to a stateful Go backend?
- Reproduction/artifacts/license: TO VERIFY before download or reuse.

Next: read the full paper, add page/section citations, distinguish author claims from own interpretation,
and update literature-matrix.csv. Do not cite this note as experimental evidence.
