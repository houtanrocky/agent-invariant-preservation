# SWE-bench: Can Language Models Resolve Real-World GitHub Issues?

Status: metadata and abstract screened on 2026-10-17; **full-text review pending**.
This is an initial note, not a completed critical review.

- Authors: Carlos E. Jimenez; John Yang; Alexander Wettig; Shunyu Yao; Kexin Pei; Ofir Press; Karthik Narasimhan.
- Year/status: 2024; ICLR 2024 (as listed on arXiv); preprint first posted 2023.
- Source/version: <https://arxiv.org/abs/2310.06770v3>.
- DOI: 10.48550/arXiv.2310.06770.
- Complete bibliography: metadata above and paper/references.bib; any unlisted proceedings details TO VERIFY.
- Research problem/focus: repository-level agents (abstract-level).
- Research questions: TO VERIFY explicit formulation in full text.
- Methodology: benchmark construction and model evaluation (abstract-level; detailed design TO VERIFY).
- Dataset/experimental environment: GitHub issue resolution in Python repositories.
- Evaluation metrics: TO VERIFY exact definitions and denominators.
- Main findings: source abstract describes: Introduces a repository issue-resolution benchmark. No numerical outcomes extracted or independently replicated.
- Limitations: Abstract screening only; detailed oracle and sampling limitations TO VERIFY.
- Threats to validity: TO VERIFY author discussion; assess oracle quality, sampling and confounding.
- Relevance to this study: Distinguish repository resolution from state-invariant preservation.
- Possible overlap with novelty claim: compare whether it studies coding-agent maintenance of existing
  transactional requirements, the same intervention, and independent hidden correctness oracles.
- Questions to investigate further: What is independently evaluated? What failures can the oracle miss?
  Does its setting justify transferring any claims to a stateful Go backend?
- Reproduction/artifacts/license: TO VERIFY before download or reuse.

Next: read the full paper, add page/section citations, distinguish author claims from own interpretation,
and update literature-matrix.csv. Do not cite this note as experimental evidence.
