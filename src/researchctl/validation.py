"""JSON Schema plus scientific consistency checks, with no execution side effects."""

import math
from datetime import datetime
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from researchctl.io import ResearchError, contained, digest, read_json, read_yaml


def schema_check(root: Path, name: str, value: Any) -> None:
    validator = Draft202012Validator(
        read_json(root / "data/schemas" / f"{name}.schema.json"), format_checker=FormatChecker()
    )
    errors = sorted(validator.iter_errors(value), key=lambda e: str(list(e.path)))
    if errors:
        raise ResearchError("; ".join(f"{list(e.path)}: {e.message}" for e in errors))


def task_check(root: Path, task: dict[str, Any], *, require_validated: bool = False) -> list[str]:
    schema_check(root, "task", task)
    required = [item["id"] for item in task["existing_invariants"]]
    if len(required) != len(set(required)):
        raise ResearchError("Invariant IDs must be unique within a task.")
    missing = []
    if task["baseline_commit"] is None:
        missing.append("pinned baseline commit")
    for key in ("baseline", "reference", "functional", "invariant", "mutant", "rationale"):
        entry = task["evidence"].get(key)
        if not entry:
            missing.append(f"{key} evidence")
            continue
        path = contained(root, entry["path"])
        if not path.is_file() or digest(path) != entry["sha256"]:
            raise ResearchError(f"Missing or altered {key} evidence: {entry['path']}")
        report = read_json(path)
        schema_check(root, "task-evidence", report)
        if (
            report["task_id"] != task["task_id"]
            or report["baseline_commit"] != task["baseline_commit"]
        ):
            raise ResearchError(f"{key} evidence identifies a different task/baseline.")
        if report["role"] != key:
            raise ResearchError(f"Evidence role mismatch for {key}.")
        if report["expected_exit_code"] != report["actual_exit_code"]:
            raise ResearchError(f"Unexpected evaluation outcome in {key} evidence.")
        if key == "mutant" and report["actual_exit_code"] == 0:
            raise ResearchError("The deliberately defective implementation must be rejected.")
        if key != "mutant" and report["actual_exit_code"] != 0:
            raise ResearchError(f"{key} evidence must show a successful check.")
        for artifact in report["artifacts"]:
            source = contained(root, artifact["path"])
            if not source.is_file() or digest(source) != artifact["sha256"]:
                raise ResearchError(f"Missing or altered evidence artifact: {artifact['path']}")
    if task["reference_solution_status"] != "human_validated":
        missing.append("human-validated reference implementation")
    if task["validation_status"] == "validated" or require_validated:
        if task["kind"] != "backend_change" or not task["human_reviewer"]:
            missing.append("backend task and named human reviewer")
        if not task["evaluation_commands"]:
            missing.append("evaluation commands")
        if not required:
            missing.append("invariant definitions")
        if missing:
            raise ResearchError("Task is not validated: " + ", ".join(missing))
    return missing


def result_check(root: Path, record: dict[str, Any]) -> None:
    schema_check(root, "run", record)
    for field in ("duration_seconds", "cost_usd"):
        if record[field] is not None and not math.isfinite(record[field]):
            raise ResearchError(f"{field} must be finite.")
    start = datetime.fromisoformat(record["started_at"].replace("Z", "+00:00"))
    end = datetime.fromisoformat(record["ended_at"].replace("Z", "+00:00"))
    if end < start:
        raise ResearchError("Run ends before it starts.")
    invariants = record["invariant_results"]
    checks = [record["functional_passes"], *invariants.values()]
    expected = all(checks) if checks and invariants and all(v is not None for v in checks) else None
    if record["execution_status"] == "completed":
        if record["failure_category"] == "environment":
            raise ResearchError(
                "Environment errors cannot be classified as completed agent evaluations."
            )
        if expected is None or record["build_passes"] is None:
            raise ResearchError("Completed evaluations need build, feature and invariant outcomes.")
        if record["build_passes"] is False and record["functional_passes"] is True:
            raise ResearchError("Feature success conflicts with a failed build.")
        if record["full_task_success"] is not expected:
            raise ResearchError("full_task_success must equal feature AND all required invariants.")
        if expected and record["failure_category"] != "none":
            raise ResearchError("Successful runs must use failure_category=none.")
        if not expected and record["failure_category"] == "none":
            raise ResearchError("Failed runs need a failure category, possibly unclassified.")
    elif record["full_task_success"] is not None:
        raise ResearchError(
            "Interrupted/environment-error runs must have an unknown overall outcome."
        )
    if (
        record["execution_status"] == "environment_error"
        and record["failure_category"] != "environment"
    ):
        raise ResearchError("Environment errors need a distinct environment category.")
    if record["data_kind"] == "observation":
        if record["baseline_commit"] is None:
            raise ResearchError("Observations require a pinned baseline.")
        task_path = root / "benchmark/tasks" / f"{record['task_id']}.yaml"
        if not task_path.is_file():
            raise ResearchError("Observation references an unknown task.")
        task = read_yaml(task_path)
        task_check(root, task, require_validated=True)
        if record["baseline_commit"] != task["baseline_commit"]:
            raise ResearchError("Run and task baselines differ.")
        if set(invariants) != {v["id"] for v in task["existing_invariants"]}:
            raise ResearchError("Run must retain every required invariant outcome.")


def load_records(root: Path, path: Path) -> list[dict[str, Any]]:
    if path.suffix == ".jsonl":
        import json

        records = [
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
    else:
        records = read_json(path)
        if isinstance(records, dict):
            records = [records]
    if not isinstance(records, list):
        raise ResearchError("Expected a run object, array or JSONL file.")
    seen = set()
    for record in records:
        result_check(root, record)
        if record["run_id"] in seen:
            raise ResearchError(f"Duplicate run ID: {record['run_id']}")
        seen.add(record["run_id"])
    return records
