# QuickCheck: A Lightweight Tool for Random Testing of Haskell Programs

Status: metadata and abstract screened on 2026-10-17; **full-text review pending**.
This is an initial note, not a completed critical review.

- Authors: Koen Claessen; John Hughes.
- Year/status: 2000; ICFP 2000; institutional metadata verified.
- Source/version: <https://research.chalmers.se/en/publication/237427>.
- DOI: 10.1145/357766.351266.
- Complete bibliography: metadata above and paper/references.bib; any unlisted proceedings details TO VERIFY.
- Research problem/focus: property-based testing (abstract-level).
- Research questions: TO VERIFY explicit formulation in full text.
- Methodology: properties as functions and random custom generators (abstract-level; detailed design TO VERIFY).
- Dataset/experimental environment: Haskell programs/case studies.
- Evaluation metrics: TO VERIFY exact definitions and denominators.
- Main findings: source abstract describes: Presents randomized property checking and custom generators. No numerical outcomes extracted or independently replicated.
- Limitations: Detailed case-study pitfalls TO VERIFY; finite tests do not establish universal correctness.
- Threats to validity: TO VERIFY author discussion; assess oracle quality, sampling and confounding.
- Relevance to this study: Foundation for stateful property generators and shrinking decisions.
- Possible overlap with novelty claim: compare whether it studies coding-agent maintenance of existing
  transactional requirements, the same intervention, and independent hidden correctness oracles.
- Questions to investigate further: What is independently evaluated? What failures can the oracle miss?
  Does its setting justify transferring any claims to a stateful Go backend?
- Reproduction/artifacts/license: TO VERIFY before download or reuse.

Next: read the full paper, add page/section citations, distinguish author claims from own interpretation,
and update literature-matrix.csv. Do not cite this note as experimental evidence.
