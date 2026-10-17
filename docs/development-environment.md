# Development environment

Python 3.11+, Git, PyYAML and jsonschema support ordinary tooling. Dev extras add pinned Black and Pyflakes; plots add
Matplotlib. Go, Docker and a healthy database are required only for subject integration; LaTeX is optional
locally. Read the pinned go.mod rather than assuming the README's version is authoritative.

Follow README for PowerShell/POSIX setup. If activation is inconvenient, use the environment's Python
directly. `python -m researchctl` is equivalent to the console script. `python scripts/check.py --strict`
is the common developer check. See troubleshooting.md for sandbox/offline setup.

Record exact installed dependencies using `python -m pip freeze` in each run environment; keep provider
secrets out of the capture. Infrastructure requirements are bounded rather than a universal binary lock;
CI tests Python 3.11/3.13, and experiment environments need their own exact resolved inventory.
Next: pin the actual database image digest and operating system before protocol freeze.
