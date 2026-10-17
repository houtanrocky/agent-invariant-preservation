# Prompt conditions and experimental manipulation

**Shared information package:** pinned source, ordinary README/ADRs, complete feature request, and the
same requirements contract listing all invariants needed for correctness. Hash the package. If a
requirement is essential, A must be able to access it with the same permissions as B.

**A template:** “Implement [feature request] in this repository. Follow the provided project documentation
and requirements contract. Use the permitted tools and stay within the recorded execution budget.”

**B template:** the exact A text, followed by: “Before editing, identify the affected state transitions and
map them to requirements in the shared contract. Consider transaction boundaries, retries, concurrent
operations and rollback where applicable. After editing, check the affected requirements and explain
which tests support them. Do not assume that feature examples establish invariant preservation.”

B must not contain hidden test cases, reference patches, undisclosed policy decisions or additional
invariants. Even reminders that accidentally introduce a previously unavailable requirement violate parity.
Maintain a table mapping each B sentence to an A-accessible source; have a reviewer approve it before freeze.
The treatment includes extra text and planning attention, so its mechanism cannot be isolated further.

Next: render per-task prompt pairs, store hashes and conduct an information-parity review on two pilot tasks.
