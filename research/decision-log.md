# Decision log

| ID/date | Decision | Reason | Consequence/revisit trigger |
| --- | --- | --- | --- |
| D001 / 2026-10-17 | Treat all eight tasks as candidates | No pinned source, reference or oracle evidence | Promote only through validation gates |
| D002 / 2026-10-17 | Use argparse, YAML and JSON Schema | Small cross-platform infrastructure | Avoid platform-specific experiment services |
| D003 / 2026-10-17 | Pin property-testing citation to v1 | Requested title belongs to v1; v2 changes title/authors | Read both versions before making claims |
| D004 / 2026-10-17 | No selected project license yet | Researcher approval needed | Decide before external release |
| D005 / 2026-10-17 | No agent runs until isolation verified | cwd/worktree is not hidden-test access control | Require separate mount/account/container |
| D006 / 2026-10-17 | Record supplied subject commit 162c5cab9fa886445dd102f4a99961027f90aebb as inspected candidate baseline | Clean checkout, exact origin, source inspection and executed build/test/race/vet evidence | Command checks passed; this is not human approval of all invariants |
| D007 / 2026-10-17 | Block T007 preservation scoring of the cross-day limit | Independently reproduced pre-existing KNOWN-01 despite a passing characterization test | Human scope/baseline decision required before freeze; no upstream fix made |
| D008 / 2026-10-17 | Require explicit shared export inventory before agent runs | Supplied baseline includes public workbench, research-readiness and mutation material | Preserve A/B parity and disclose leakage; no automatic filtering decision |

For each new entry record date, alternatives, evidence, decision owner, affected artifacts, whether main
outcomes were visible, and a commit. Preserve rejected approaches and reasons in the daily log.
Next: review two concrete new change contracts, KNOWN-01 handling and shared source exposure; then select agents.
