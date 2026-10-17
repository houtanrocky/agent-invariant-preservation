"""Executed infrastructure example, deliberately separate from empirical observations."""

import platform
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from researchctl.adapters import AgentRequest, CommandAdapter
from researchctl.analysis import summarize
from researchctl.io import ResearchError, digest, read_json, read_yaml, write_json
from researchctl.validation import result_check, task_check


def smoke(root: Path, output: Path | None = None) -> dict[str, Any]:
    task_path = root / "benchmark/fixtures/demo-task.yaml"
    task = read_yaml(task_path)
    task_check(root, task)
    output = output or root / ".local/demos" / str(uuid.uuid4())
    if output.exists():
        raise ResearchError("Demo output already exists; choose a new directory.")
    output.mkdir(parents=True)
    started = datetime.now(timezone.utc).isoformat()
    fixture = root / "benchmark/fixtures/deterministic_check.py"
    response = CommandAdapter().execute(
        AgentRequest([sys.executable, str(fixture)], fixture.parent, "", 10, {}), output / "trace"
    )
    if response.returncode != 0 or response.timed_out:
        raise ResearchError("Deterministic fixture failed; preserve its trace for investigation.")
    evaluation = read_json(response.stdout_path)
    record = {
        "schema_version": "1.0",
        "data_kind": "infrastructure",
        "data_label": "INFRASTRUCTURE SMOKE TEST — NOT RESEARCH RESULTS",
        "run_id": "demo-" + uuid.uuid4().hex,
        "task_id": task["task_id"],
        "agent_id": "deterministic-python-fixture",
        "model_id": "not_applicable",
        "agent_version": "fixture-v1",
        "model_version": "not_applicable",
        "condition": "A",
        "repetition": 1,
        "baseline_commit": None,
        "started_at": started,
        "ended_at": datetime.now(timezone.utc).isoformat(),
        "duration_seconds": response.duration_seconds,
        "input_tokens": None,
        "output_tokens": None,
        "cost_usd": None,
        "tool_interactions": None,
        "build_passes": True,
        "functional_passes": evaluation["functional_passes"],
        "invariant_results": evaluation["invariant_results"],
        "full_task_success": evaluation["functional_passes"]
        and all(evaluation["invariant_results"].values()),
        "execution_status": "completed",
        "failure_category": "none",
        "trace_location": str(response.stdout_path.resolve()),
        "environment": {"python": platform.python_version(), "platform": platform.platform()},
        "provenance": {
            "task_sha256": digest(task_path),
            "fixture_sha256": digest(fixture),
            "stdout_sha256": digest(response.stdout_path),
            "runner_version": "0.1.0",
        },
        "notes": "Deterministic software check, no coding agent or backend modification involved.",
    }
    result_check(root, record)
    write_json(output / "run.json", record, exclusive=True)
    summary = summarize([record], allow_nonresearch=True)
    write_json(output / "summary.json", summary, exclusive=True)
    manifest = {
        "label": record["data_label"],
        "files": {
            name: digest(output / name)
            for name in ("run.json", "summary.json", "trace/stdout.txt", "trace/stderr.txt")
        },
    }
    write_json(output / "manifest.json", manifest, exclusive=True)
    return {"output": str(output.resolve()), "run_id": record["run_id"], "summary": summary}
