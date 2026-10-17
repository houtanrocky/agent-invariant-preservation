# Experiment operations

There are no coding-agent executions yet. pilot/ and runs/ hold plans and reviewed run pointers;
large traces/checkouts are ignored under .local/ and preserved via artifacts storage before cleanup.

For each attempt retain run ID, task/system/condition/repetition, prompt hash, baseline, isolated session,
effective config, timestamps, patch, evaluation output and trace checksums. Record unexpected deviations
and environment incidents. Avoid repeated retries until success; use the frozen retry policy.
Next: execute a permitted dry run only after entry gates in protocol/pilot-protocol.md are satisfied.
