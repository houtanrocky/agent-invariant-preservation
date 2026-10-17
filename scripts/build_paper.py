"""Compile the manuscript; fail explicitly when TeX prerequisites are missing."""

import shutil
import subprocess
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    for command in ("pdflatex", "bibtex"):
        if not shutil.which(command):
            raise SystemExit(f"Not compiled: {command} is unavailable. See paper/README.md.")
    commands = [
        ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"],
        ["bibtex", "main"],
        ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"],
        ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"],
    ]
    for command in commands:
        subprocess.run(command, cwd=root / "paper", check=True)
    print(root / "paper/main.pdf")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
