"""Small research CLI. Missing prerequisites are errors, never simulated success."""

import argparse
import json
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

from researchctl.analysis import summarize
from researchctl.demo import smoke
from researchctl.io import ResearchError, read_json, read_yaml, root_at
from researchctl.target import setup, worktree
from researchctl.snapshot import export_snapshot
from researchctl.validation import load_records, task_check


def doctor(root: Path) -> dict[str, Any]:
    dependencies = {
        name: shutil.which(name) is not None
        for name in ("git", "go", "docker", "pdflatex", "bibtex")
    }
    return {
        "python": platform.python_version(),
        "root": str(root),
        "dependencies_available": dependencies,
        "note": "Executable presence does not verify daemon, network, credentials or agent integration.",
    }


def execute(args: argparse.Namespace, root: Path) -> Any:
    if args.command == "doctor":
        return doctor(root)
    if args.command == "setup-target":
        return setup(root, args.pin, args.discover_pin)
    if args.command == "prepare-workspace":
        config = read_yaml(root / "config/target-repository.yaml")
        return {"workspace": str(worktree(root, args.run_id, config["baseline_commit"] or ""))}
    if args.command == "prepare-snapshot":
        return export_snapshot(root, args.run_id, args.task)
    if args.command == "list-tasks":
        return [
            {
                "task_id": (t := read_yaml(p))["task_id"],
                "title": t["title"],
                "status": t["validation_status"],
            }
            for p in sorted((root / "benchmark/tasks").glob("*.yaml"))
        ]
    if args.command == "new-task":
        if not re.fullmatch(r"T\d{3}", args.task_id):
            raise ResearchError("Use a task ID such as T009.")
        target = root / "benchmark/tasks" / f"{args.task_id}.yaml"
        task = read_yaml(root / "benchmark/task-template/task.yaml")
        task.update(task_id=args.task_id, title=args.title)
        with target.open("x", encoding="utf-8", newline="\n") as stream:
            yaml.safe_dump(task, stream, sort_keys=False, allow_unicode=True)
        return {"created": str(target), "status": "candidate"}
    if args.command == "validate-task":
        task = read_yaml(args.path)
        missing = task_check(root, task, require_validated=args.require_validated)
        return {
            "metadata_valid": True,
            "validation_status": task["validation_status"],
            "outstanding": missing,
        }
    if args.command in ("validate-data", "summarize"):
        paths = (
            args.paths
            if args.command == "validate-data"
            else ([args.path] if args.path else sorted((root / "data/raw").glob("*.json*")))
        )
        records = [row for path in paths for row in load_records(root, path)]
        if len({r["run_id"] for r in records}) != len(records):
            raise ResearchError("Duplicate run ID across input files.")
        if args.command == "validate-data":
            return {"valid_records": len(records), "files": len(paths)}
        return summarize(records, allow_nonresearch=args.allow_nonresearch)
    if args.command == "smoke":
        return smoke(root, args.output)
    if args.command == "reproduce":
        steps = [
            [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
            [sys.executable, "-m", "researchctl", "smoke"],
        ]
        if args.run:
            for command in steps:
                subprocess.run(command, cwd=root, check=True)
        return {
            "implemented_steps": steps,
            "study_reproduction": "blocked: no empirical runs yet",
            "instructions": "docs/reproducing-results.md",
        }
    if args.command == "status":
        tasks = [read_yaml(p) for p in (root / "benchmark/tasks").glob("*.yaml")]
        validated = []
        for task in tasks:
            task_check(root, task)
            if task["validation_status"] == "validated":
                validated.append(task["task_id"])
        target = read_yaml(root / "config/target-repository.yaml")
        report_path = (
            root
            / "artifacts/target-baseline"
            / (target["baseline_commit"] or "unpinned")
            / "report.json"
        )
        baseline = read_json(report_path) if report_path.is_file() else None
        candidate_path = root / "benchmark/manifests/baseline-review.json"
        candidate = read_json(candidate_path) if candidate_path.is_file() else None
        if baseline and baseline["baseline_commit"] != target["baseline_commit"]:
            raise ResearchError("Stored baseline report identifies a different commit.")
        pending_baseline = (
            []
            if baseline and baseline["all_commands_passed"]
            else ["baseline execution/investigation"]
        )
        return {
            "phase": (
                "baseline and task packages; independent human review pending"
                if candidate
                else "foundation; protocol draft"
            ),
            "candidate_tasks": len(tasks),
            "validated_tasks": validated,
            "target": target,
            "proposed_baseline_review": candidate,
            "executable_draft_tasks": [
                task["task_id"]
                for task in tasks
                if task["reference_solution_status"] == "draft"
                and all(
                    task["evidence"][role]
                    for role in ("baseline", "reference", "functional", "invariant", "mutant")
                )
            ],
            "baseline_verification": (
                None
                if baseline is None
                else {
                    "report": str(report_path.relative_to(root)),
                    "all_commands_passed": baseline["all_commands_passed"],
                    "interpretation": baseline["interpretation"],
                }
            ),
            "implemented": [
                "metadata/data validation",
                "descriptive analysis",
                "smoke",
                "pinned clone/worktree mechanism",
                "command adapter",
            ],
            "blocked_or_future": pending_baseline
            + [
                "independent baseline correctness review and approval",
                "human reference and oracle rationale review",
                "filesystem/network isolation demonstration and prompt parity review",
                "real agent integration",
                "oracle validation",
                "preregistration freeze",
                "main study",
                "empirical paper",
            ],
        }
    raise ResearchError("Unknown command.")


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(prog="researchctl")
    result.add_argument(
        "--root", type=Path, help="Research checkout (defaults to current checkout)"
    )
    sub = result.add_subparsers(dest="command", required=True)
    for name in ("doctor", "list-tasks", "status"):
        sub.add_parser(name)
    target = sub.add_parser("setup-target")
    pins = target.add_mutually_exclusive_group()
    pins.add_argument("--pin")
    pins.add_argument(
        "--discover-pin", action="store_true", help="Resolve and persist remote HEAD once"
    )
    workspace = sub.add_parser("prepare-workspace")
    workspace.add_argument("run_id")
    snapshot = sub.add_parser("prepare-snapshot")
    snapshot.add_argument("run_id")
    snapshot.add_argument("--task", required=True)
    new = sub.add_parser("new-task")
    new.add_argument("task_id")
    new.add_argument("--title", required=True)
    task = sub.add_parser("validate-task")
    task.add_argument("path", type=Path)
    task.add_argument("--require-validated", action="store_true")
    data = sub.add_parser("validate-data")
    data.add_argument("paths", nargs="+", type=Path)
    summary = sub.add_parser("summarize")
    summary.add_argument("path", nargs="?", type=Path)
    summary.add_argument("--allow-nonresearch", action="store_true")
    demo = sub.add_parser("smoke")
    demo.add_argument("--output", type=Path)
    repro = sub.add_parser("reproduce")
    repro.add_argument("--run", action="store_true")
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        root = root_at(args.root or Path.cwd())
        output = execute(args, root)
        print(json.dumps(output, indent=2, ensure_ascii=False, allow_nan=False))
    except (
        ResearchError,
        OSError,
        ValueError,
        TypeError,
        KeyError,
        yaml.YAMLError,
        subprocess.SubprocessError,
    ) as error:
        print(f"researchctl: {error}", file=sys.stderr)
        return 2
    return 0
