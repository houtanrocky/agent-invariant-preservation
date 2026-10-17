# LISA v1 — targeted full-text review

Reviewed 2026-10-18: [versioned full text](https://arxiv.org/html/2607.18711v1), §§III-G, IV-B/C and VI-B. Title and authors remain recorded in the matrix and bibliography.

API sequences receive assertions informed by documentation and mined invariants, including manual curation. Persistent failures require human verification (§III-G). Evaluation covers seven C/C++ libraries; historical-bug detection uses 25 bugs across five libraries (§IV). A test must pass the fixed revision and fail the buggy revision. §VI-B acknowledges corpus and oracle limitations. These are author descriptions, not independently reproduced outcomes.

Our assessment: invariant testing and human review are overlapping foundations. Joint maintenance-feature correctness is the proposed outcome here. Synthetic mutants establish sensitivity to selected faults, not real-world defect coverage. Artifacts and appendices remain unaudited.
