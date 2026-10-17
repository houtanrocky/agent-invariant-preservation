"""One cross-platform command for fast infrastructure validation."""

import argparse
import ast
import csv
import importlib.util
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

from jsonschema import Draft202012Validator

from researchctl.io import read_json, read_yaml
from researchctl.validation import load_records, schema_check, task_check

ROOT = Path(__file__).resolve().parents[1]


def structure_checks() -> None:
    required_dirs = [
        "research",
        "literature/reading-notes",
        "protocol",
        "benchmark/task-template",
        "benchmark/tasks",
        "benchmark/reference-solutions",
        "benchmark/oracles",
        "benchmark/fixtures",
        "benchmark/manifests",
        "config",
        "src/researchctl",
        "tests",
        "scripts",
        "data/raw",
        "data/processed",
        "data/schemas",
        "data/examples",
        "experiments/pilot",
        "experiments/runs",
        "experiments/failure-reviews",
        "analysis",
        "paper/sections",
        "paper/figures",
        "paper/tables",
        "progress/meetings",
        "presentation",
        "artifacts",
        "docs",
    ]
    for name in required_dirs:
        assert (ROOT / name).is_dir(), f"Missing required directory: {name}"
    for path in ROOT.rglob("*.md"):
        if any(part.startswith(".") for part in path.relative_to(ROOT).parts):
            continue
        text = path.read_text(encoding="utf-8")
        assert len(text.split()) >= 20, f"Unhelpful empty document: {path}"
        for link in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
            url = urlsplit(link.strip("<>"))
            if url.scheme or not url.path:
                continue
            target = (path.parent / unquote(url.path)).resolve()
            assert target.is_file(), f"Broken relative link in {path}: {link}"
    for path in [
        *(ROOT / "src").rglob("*.py"),
        *(ROOT / "analysis").glob("*.py"),
        *(ROOT / "scripts").glob("*.py"),
        *(ROOT / "tests").glob("*.py"),
    ]:
        source = path.read_text(encoding="utf-8")
        ast.parse(source, filename=str(path))
        assert all(
            line.rstrip() == line for line in source.splitlines()
        ), f"Trailing whitespace: {path}"
    for path in (ROOT / "data/schemas").glob("*.json"):
        Draft202012Validator.check_schema(read_json(path))
    for path in [
        *(ROOT / "benchmark/tasks").glob("*.yaml"),
        ROOT / "benchmark/task-template/task.yaml",
        ROOT / "benchmark/fixtures/demo-task.yaml",
    ]:
        task_check(ROOT, read_yaml(path))
    for name, filename in (
        ("study", "study.yaml"),
        ("target", "target-repository.yaml"),
        ("agents", "agents.example.yaml"),
        ("environment", "environment.example.yaml"),
    ):
        schema_check(ROOT, f"{name}-config", read_yaml(ROOT / "config" / filename))
    study = read_yaml(ROOT / "config/study.yaml")
    assert study["maximum_main_executions"] == (
        study["maximum_tasks"]
        * study["agent_systems"]
        * len(study["conditions"])
        * study["repetitions"]
    )
    assert study["conditions"] == ["A", "B"] and study["protocol_status"] in ("draft", "frozen")
    target = read_yaml(ROOT / "config/target-repository.yaml")
    assert target["origin_url"] == "https://github.com/houtanrocky/dragon-market"
    assert target["baseline_commit"] is None or re.fullmatch(
        "[0-9a-f]{40}", target["baseline_commit"]
    )
    agents = read_yaml(ROOT / "config/agents.example.yaml")["agents"]
    assert len(agents) == study["agent_systems"]
    assert all(a["command"] and a["timeout_seconds"] > 0 for a in agents)
    assert read_yaml(ROOT / "config/environment.example.yaml")["timezone"] == "UTC"
    records = load_records(ROOT, ROOT / "data/examples/synthetic-runs.json")
    assert records and all(row["data_kind"] == "synthetic" for row in records)
    for path in (ROOT / "data/raw").glob("*.json*"):
        assert all(row["data_kind"] == "observation" for row in load_records(ROOT, path))
    with (ROOT / "literature/literature-matrix.csv").open(encoding="utf-8", newline="") as stream:
        papers = list(csv.DictReader(stream))
    assert len(papers) >= 6 and all(row["source_url"].startswith("https://") for row in papers)
    main = (ROOT / "paper/main.tex").read_text(encoding="utf-8")
    for name in re.findall(r"\\input\{([^}]+)\}", main):
        assert (ROOT / "paper" / f"{name}.tex").is_file()
    bib = (ROOT / "paper/references.bib").read_text(encoding="utf-8")
    keys = set(re.findall(r"@\w+\{([^,]+),", bib))
    for section in (ROOT / "paper/sections").glob("*.tex"):
        for citations in re.findall(r"\\cite\{([^}]+)\}", section.read_text(encoding="utf-8")):
            assert set(citations.split(",")) <= keys
    print(
        "PASS: structure, local links, Python syntax/whitespace, configurations, schemas, tasks, data, citations"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--strict", action="store_true", help="Fail if Black/Pyflakes are unavailable"
    )
    args = parser.parse_args()
    structure_checks()
    subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], cwd=ROOT, check=True
    )
    if all(importlib.util.find_spec(name) for name in ("black", "pyflakes")):
        for command in (
            [
                sys.executable,
                "-m",
                "black",
                "--check",
                "src",
                "analysis",
                "scripts",
                "tests",
                "benchmark/fixtures",
            ],
            [
                sys.executable,
                "-m",
                "pyflakes",
                "src",
                "analysis",
                "scripts",
                "tests",
                "benchmark/fixtures",
            ],
        ):
            subprocess.run(command, cwd=ROOT, check=True)
    elif args.strict:
        raise SystemExit("Black/Pyflakes unavailable: install dev extras before strict checks.")
    else:
        print("NOT RUN: Black/Pyflakes (unavailable); syntax/whitespace checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
