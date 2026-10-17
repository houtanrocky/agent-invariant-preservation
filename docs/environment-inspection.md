# Initial environment inspection — 2026-10-17

Historical record of the initial restricted session. The follow-up below and
[target verification](target-baseline.md) supersede its checkout/Docker/Git blockers.

Workspace: S:/Repos/agent-invariant-preservation, initially empty. Windows PowerShell; existing Git identity
was present and left unchanged. Git 2.50.1; Python 3.13.9; Go 1.26.0; uv 0.8.15. Docker CLI exists but its
Linux engine named pipe was unavailable. pdflatex/latexmk were not found. PyYAML, jsonschema, setuptools
and Matplotlib were importable. Black 25.9.0 and Pyflakes 3.2.0 were subsequently found installed;
Ruff and pytest were absent. The suite uses stdlib unittest.

Credential/proxy inspection listed variable **names only**; no secret values were printed or stored.
No real agent configuration or authentication was validated. Git clone of the intended origin failed
because the configured proxy endpoint at 127.0.0.1:9 was unreachable. No proxy bypass was attempted.

The public GitHub landing README was accessible through the browser, but source/blob/tree/commit endpoints
were not. Thus exact SHA, go.mod, migrations, implementation, test names and baseline outcomes remain
TO VERIFY. README claims are discovery leads only. It describes wallets, auctions, retries, limits,
audit records and concurrency tests; this project does not certify those claims.

Source: <https://github.com/houtanrocky/dragon-market> (observed 2026-10-17, floating documentation only).
No precise implementation evidence can yet support task promotion. No upstream code was modified.
## Follow-up after researcher supplied the clone

The researcher committed the foundation as `3a5a1c2` (`Initialize`) and configured the research remote.
This session found that state already present and left the remote/history intact. Git metadata writes
and the previously skipped local-clone test can now run. Docker's Linux engine responds (29.1.5).
Go 1.26.0 builds the supplied Go 1.25.0 module. No TeX executables were found.

The clean subject checkout is pinned to `162c5cab9fa886445dd102f4a99961027f90aebb`. Build, test, race
and vet commands passed; a targeted test reproduced KNOWN-01. Source files, migrations, contracts and
tests were inspected, and the subject's MIT LICENSE was read. Original setup limitations remain above
as a historical record rather than being silently erased. No paid agent run or upstream code change occurred.
Next: review source-backed candidates and the known invariant defect before constructing two tasks.
