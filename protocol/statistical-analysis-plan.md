# Statistical analysis plan — draft, before main data

Describe counts and rates by condition, system and task. Retain individual runs and invariant assertions.
The primary estimand is the B−A success-probability difference, equally weighted across validated tasks
and selected systems. First average repetitions within task/system/condition; difference B−A within
task/system; then average across systems within task and across tasks. Missing blocks are disclosed;
do not silently change the target weighting to available cases. Rerun tables under preplanned timeout
and unresolved-environment sensitivity rules.

Wilson 95% intervals are implemented as **marginal descriptive intervals**, and do not model dependence.
Repeated runs on a task are nested. Do not run Fisher's exact test on all 96 as if tasks were independent
or pair repetition numbers as if they shared stochastic seeds. Preserve matching at task/system level.
An optional equal-task bootstrap summarizes uncertainty only with at least two complete task clusters;
eight purposively chosen tasks still give fragile intervals and no population-general sampling inference.

After the pilot, consider logistic regression with condition and system effects and a task intercept.
Use a mixed-effects task intercept only if supported by observations/clusters and identifiable variation;
two agent systems are fixed effects, not a reliable random-effects sample. Separation, sparse failures
and too few tasks can make this model inappropriate. No mixed-effects fit is implemented by default.
If inference is unjustified, publish descriptive estimates and limitations instead.

Pilot data are excluded from confirmatory results. Pilot feasibility, task count, repetitions, power
and detectable effect sizes must be reassessed; 96 is only a ceiling. Set a minimum effect of interest
and simulate dependence-aware precision/power once plausible pilot rates are available. Log changes.

RQ3 is descriptive, with counts and denominators per applicable invariant. RQ4 is exploratory; show
scatterplots/strata, missingness and censored durations, avoiding causal interpretation or cross-provider
token equivalence. Choose one primary contrast; label subgroup analyses exploratory and address multiple
comparisons if formal secondary tests are later added. No outcome-driven stopping or deletion of failures.
Next: supervisor review and preregistration freeze after pilot and before main runs.
