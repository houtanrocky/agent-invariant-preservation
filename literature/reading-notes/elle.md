# Elle: Inferring Isolation Anomalies from Experimental Observations

Status: metadata and abstract screened on 2026-10-17; **full-text review pending**.
This is an initial note, not a completed critical review.

- Authors: Kyle Kingsbury; Peter Alvaro.
- Year/status: 2021; PVLDB 14(3):268-280; preprint 2020.
- Source/version: <https://www.vldb.org/pvldb/vol14/p268-alvaro.pdf>.
- DOI: 10.14778/3430915.3430918.
- Complete bibliography: metadata above and paper/references.bib; any unlisted proceedings details TO VERIFY.
- Research problem/focus: transactional correctness (abstract-level).
- Research questions: TO VERIFY explicit formulation in full text.
- Methodology: dependency-graph inference from observed histories (abstract-level; detailed design TO VERIFY).
- Dataset/experimental environment: database histories and case studies.
- Evaluation metrics: TO VERIFY exact definitions and denominators.
- Main findings: source abstract describes: Presents an anomaly checker with stated datatype and history assumptions. No numerical outcomes extracted or independently replicated.
- Limitations: Predicate anomalies and inference assumptions bound coverage; inspect full text.
- Threats to validity: TO VERIFY author discussion; assess oracle quality, sampling and confounding.
- Relevance to this study: Ground history-based correctness checks and avoid overclaiming serialization.
- Possible overlap with novelty claim: compare whether it studies coding-agent maintenance of existing
  transactional requirements, the same intervention, and independent hidden correctness oracles.
- Questions to investigate further: What is independently evaluated? What failures can the oracle miss?
  Does its setting justify transferring any claims to a stateful Go backend?
- Reproduction/artifacts/license: TO VERIFY before download or reuse.

Next: read the full paper, add page/section citations, distinguish author claims from own interpretation,
and update literature-matrix.csv. Do not cite this note as experimental evidence.
