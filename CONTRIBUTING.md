# Contributing and reproducing

Read research/ethics-and-integrity.md before changing data or interpretation. Use Python 3.11+, install
the dev extras, and run `python scripts/check.py --strict`. The same fast suite runs in CI without
credentials, Docker or subject checkout. Keep database/paid-agent checks separate and explicitly labeled.

Use focused branches and conventional commits (docs, feat, test, fix, research, analysis, paper).
Every behavioral change needs an appropriate test; do not create tests that merely restate prose.
Review schemas and semantic validation together. Use null for unavailable measurements.

Never overwrite raw evidence or silently revise evaluation criteria. Attach rationale and provenance
to corrections. Candidate promotion needs named human reference/oracle review, not just green metadata.
Research decisions belong in the decision log and daily reasoning log as well as Git.

No project license is selected yet. Coordinate rights before distributing contributions; see
LICENSE-DECISIONS.md. Next: run the smoke test and inspect its manifest before proposing a change.
