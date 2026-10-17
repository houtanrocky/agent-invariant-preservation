# Finding and Reproducing Heisenbugs in Concurrent Programs

Status: metadata and abstract screened on 2026-10-17; **full-text review pending**.
This is an initial note, not a completed critical review.

- Authors: Madanlal Musuvathi; Shaz Qadeer; Thomas Ball; Gerard Basler; Piramanayagam Arumuga Nainar; Iulian Neamtiu.
- Year/status: 2008; OSDI 2008; publisher full text inspected at abstract/introduction level.
- Source/version: <https://static.usenix.org/events/osdi08/tech/full_papers/musuvathi/musuvathi_html/index.html>.
- DOI: TO VERIFY; omitted from BibTeX.
- Complete bibliography: metadata above and paper/references.bib; any unlisted proceedings details TO VERIFY.
- Research problem/focus: concurrency testing (abstract-level).
- Research questions: TO VERIFY explicit formulation in full text.
- Methodology: systematic schedule exploration with Chess (abstract-level; detailed design TO VERIFY).
- Dataset/experimental environment: concurrent systems programs.
- Evaluation metrics: TO VERIFY exact definitions and denominators.
- Main findings: source abstract describes: Presents deterministic exploration and reproduction of concurrency bugs. No numerical outcomes extracted or independently replicated.
- Limitations: Not a drop-in PostgreSQL scheduler; study-specific schedule coverage remains limited.
- Threats to validity: TO VERIFY author discussion; assess oracle quality, sampling and confounding.
- Relevance to this study: Record and reproduce selected interleavings and counterexamples.
- Possible overlap with novelty claim: compare whether it studies coding-agent maintenance of existing
  transactional requirements, the same intervention, and independent hidden correctness oracles.
- Questions to investigate further: What is independently evaluated? What failures can the oracle miss?
  Does its setting justify transferring any claims to a stateful Go backend?
- Reproduction/artifacts/license: TO VERIFY before download or reuse.

Next: read the full paper, add page/section citations, distinguish author claims from own interpretation,
and update literature-matrix.csv. Do not cite this note as experimental evidence.
