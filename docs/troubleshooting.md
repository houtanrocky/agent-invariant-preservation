# Troubleshooting

CLI not found: invoke the environment's `python -m researchctl` and confirm editable installation.
Wrong directory: pass `researchctl --root ABSOLUTE-CHECKOUT status` before the subcommand.
Offline dependencies: use a trusted local wheel cache or a documented environment with PyYAML/jsonschema;
do not replace schema checks with fake success. In the managed Windows sandbox, Python 3.13 temporary
directory ACLs may block pip/ensurepip. The following fallback was exercised here using already installed
dependencies and uv. It changes only this build process's disposable-directory creation under .local/;
it does not modify global ACLs or settings:

```powershell
python -m venv --without-pip --system-site-packages .venv
python scripts/build_editable.py --sandbox-temp-acl
$env:UV_CACHE_DIR = (Resolve-Path .local).Path + '\uv-cache'
uv pip install --python .venv --no-deps --offline .local/wheels/agent_invariant_preservation-0.1.0-0.editable-py3-none-any.whl
.venv\Scripts\researchctl.exe doctor
.venv\Scripts\python.exe scripts/check.py --strict
```

This fallback needs preinstalled setuptools, PyYAML, jsonschema, Black and Pyflakes. It is not a clean
dependency-isolated installation; record that limitation. Ordinary machines should use README's venv/pip
workflow. The source checkout is required for task/config/schema files even when the CLI is installed.

Target clone failure: check configured proxy/network in your environment without printing credentials.
Do not change the study origin or invent a pin. Docker executable without daemon: start the engine and
verify it before integration; preserve setup failures separately. Baseline fail: capture full command,
tool versions and logs, compare with pristine pinned code, then classify before any agent attribution.

Task candidate: ordinary metadata validation may succeed while listing missing evidence. Use
--require-validated to enforce promotion gates. Unknown measurements: use null rather than zero.
Synthetic summary refused: only --allow-nonresearch permits isolated software-test data; never use in paper.
LaTeX unavailable: use the separate CI job or install TeX Live/MiKTeX and BibTeX, then rerun the actual build.
Next: add newly encountered blockers with commands and exact observed outcomes, excluding secrets.
