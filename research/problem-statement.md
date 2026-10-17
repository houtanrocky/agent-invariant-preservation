# Problem statement

Passing a requested feature example does not establish preservation of stateful behavior. A purchase
may return a plausible response while a retry duplicates payment, a failed transaction leaves an audit
entry, or competing operations break ownership consistency. These are motivating possibilities, not
reported Dragon Market defects.

The study separates feature success from invariant preservation, then measures their conjunction.
The practical problem is maintaining a documented state contract across repository modifications.
The measurement problem is constructing trustworthy oracles for sequential and concurrent histories.

Next: map every selected invariant to pinned source, requirements, fixtures, and observable database
assertions. Reject tasks for which the intended behavior cannot be independently justified.
