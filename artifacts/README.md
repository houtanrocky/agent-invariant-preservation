# Artifact preservation

manifest.csv inventories local infrastructure-validation artifacts and committed subject-baseline evidence;
it has no coding-agent observation rows. validation-summary.json preserves the initial acceptance checks
and source hashes as a historical record. target-baseline/ stores the inspected subject's checks and
nonempty raw outputs; empty streams retain hashes in the baseline report. For each retained artifact record
ID, run ID, kind, immutable relative path or storage URI, SHA-256, byte count, capture time, access level
and notes. Prefer repository-relative paths for small non-sensitive evidence; large logs may use Git LFS
or researcher-controlled immutable storage. A URI alone is not integrity evidence.

Before removing ignored local workspaces, archive raw traces, patches and evaluation histories and
verify checksums by re-reading storage. Never discard failed attempts silently. Preserve restricted
originals of redacted traces and document redaction; never put signed download URLs or credentials in Git.
The smoke command produces a local SHA-256 manifest for infrastructure verification only.
Next: choose artifact retention/storage and backup policy before paid runs or database integration.
