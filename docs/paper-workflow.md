# Manuscript workflow

paper/main.tex is the primary source, with section files and a checked BibTeX inventory. Use
`python scripts/build_paper.py`; exact TeX commands and troubleshooting are in paper/README.md.
The skeleton states planned work and contains no fabricated results or empirical conclusions.

Draft introduction and related work while reading; refine methodology after the pilot. Freeze the
protocol before main outcomes. Replace result placeholders only after raw-record review and regeneration.
For each table/figure cite input hashes, command and code commit in a provenance note. Keep synthetic
outputs out of paper directories. The build script compiles sources only and never imports example data.

Next: review closest work in full, revise tentative gap claims, and decide a venue template after
supervisor feedback. A compilable skeleton is not a completed or submission-ready empirical manuscript.
