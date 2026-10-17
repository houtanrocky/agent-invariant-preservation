# Frozen benchmark inventories

No main-study manifest is frozen. At the week-2 gate save an immutable inventory containing accepted
task IDs, baseline SHAs, task/prompt/oracle/reference hashes, reviewers, validation dates and protocol
commit. Keep rejected candidates and reasons in a separate inventory rather than deleting their history.

Next: produce a pilot inventory for two tasks; freeze the main inventory only after pilot revisions.

The current `baseline-review.json` proposes a candidate without changing the configured study pin.
`shared-files.json` is an explicit draft export inventory, not a frozen study manifest. Each executable
task package also retains concrete shared-input hashes and A/B prompt hashes for parity review.
