# Analysis workflow

No real observations exist. Run `python analysis/descriptive.py PATH` on validated observation records.
For software tests only append --allow-nonresearch. statistical_analysis.py reports matched descriptive
B−A task differences and optional exploratory task-cluster bootstrap intervals. It does not fit an
unjustified mixed-effects model or treat all executions as independent tasks.

visualizations.py generates labeled PDF/SVG rate and duration figures, captions and input provenance.
It requires the plots extra. Nonresearch inputs require an explicit flag and receive a visible watermark.
Default output is analysis/output/, never paper/. Inspect and trace real-data outputs before copying them
to paper/figures or tables. The manuscript build does not run analysis or ingest example data.

Follow protocol/statistical-analysis-plan.md; report missing cells, excluded environments and denominators.
Next: freeze the analysis plan after pilot, then analyze main observations using the frozen version.
