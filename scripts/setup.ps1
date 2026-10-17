$ErrorActionPreference = 'Stop'
python -m venv .venv
if ($LASTEXITCODE -ne 0) { throw 'Virtual environment creation failed' }
& .\.venv\Scripts\python.exe -m pip install -e '.[dev,plots]'
if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed' }
& .\.venv\Scripts\python.exe scripts/check.py --strict
if ($LASTEXITCODE -ne 0) { throw 'Validation failed' }
