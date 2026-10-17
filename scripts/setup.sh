#!/usr/bin/env sh
set -eu
python3 -m venv .venv
.venv/bin/python -m pip install -e '.[dev,plots]'
.venv/bin/python scripts/check.py --strict
