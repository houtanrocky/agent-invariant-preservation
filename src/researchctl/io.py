"""Strict serialization and repository path helpers."""

import hashlib
import json
from pathlib import Path
from typing import Any

import yaml


class ResearchError(ValueError):
    """An actionable validation or prerequisite error."""


def root_at(start: Path) -> Path:
    for path in (start.resolve(), *start.resolve().parents):
        if (path / "config/study.yaml").is_file():
            return path
    raise ResearchError("Run inside this research checkout, or pass --root PATH.")


def read_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any, *, exclusive: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x" if exclusive else "w", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write("\n")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def contained(root: Path, relative: str) -> Path:
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ResearchError(f"Path escapes permitted root: {relative}")
    return path
