"""Descriptive summaries; no synthetic data enter observation summaries implicitly."""

import math
import statistics
from collections import defaultdict
from typing import Any

from researchctl.io import ResearchError


def wilson(successes: int, count: int) -> list[float] | None:
    """Marginal 95% Wilson interval; does not account for clustered observations."""
    if not count:
        return None
    z = 1.959963984540054
    p = successes / count
    denominator = 1 + z * z / count
    center = (p + z * z / (2 * count)) / denominator
    radius = z * math.sqrt(p * (1 - p) / count + z * z / (4 * count * count)) / denominator
    return [max(0, center - radius), min(1, center + radius)]


def measured(values: list[float | int | None]) -> dict[str, Any]:
    known = [v for v in values if v is not None]
    return {
        "n_measured": len(known),
        "n_missing": len(values) - len(known),
        "sum": sum(known) if known else None,
        "median": statistics.median(known) if known else None,
        "min": min(known) if known else None,
        "max": max(known) if known else None,
    }


def summarize(records: list[dict[str, Any]], *, allow_nonresearch: bool = False) -> dict[str, Any]:
    kinds = {r["data_kind"] for r in records}
    if kinds - {"observation"} and not allow_nonresearch:
        raise ResearchError(
            "Non-research data require --allow-nonresearch; never use in the paper."
        )
    if len(kinds) > 1:
        raise ResearchError("Do not mix synthetic, infrastructure and observation records.")
    eligible = [r for r in records if r["execution_status"] == "completed"]
    groups = {}
    for field in ("condition", "agent_id", "task_id"):
        bins = defaultdict(list)
        for record in eligible:
            bins[record[field]].append(record)
        groups[field] = {}
        for key, rows in sorted(bins.items()):
            successes = sum(r["full_task_success"] is True for r in rows)
            groups[field][key] = {
                "n": len(rows),
                "successes": successes,
                "rate": successes / len(rows),
                "wilson_95_marginal": wilson(successes, len(rows)),
            }
    violations = defaultdict(lambda: {"failed": 0, "evaluated": 0})
    for row in eligible:
        for key, value in row["invariant_results"].items():
            if value is not None:
                violations[key]["evaluated"] += 1
                violations[key]["failed"] += int(value is False)
    return {
        "data_kind": next(iter(kinds), "no_data"),
        "label": "RESEARCH OBSERVATIONS" if kinds == {"observation"} else "NOT RESEARCH RESULTS",
        "n_records": len(records),
        "n_evaluated": len(eligible),
        "n_environment_errors": sum(r["execution_status"] == "environment_error" for r in records),
        "n_other_unevaluated": len(records)
        - len(eligible)
        - sum(r["execution_status"] == "environment_error" for r in records),
        "groups": groups,
        "invariant_violations": dict(violations),
        "resources": {
            field: measured([r[field] for r in records])
            for field in (
                "duration_seconds",
                "input_tokens",
                "output_tokens",
                "cost_usd",
                "tool_interactions",
            )
        },
        "warning": "Small samples; marginal intervals ignore task/run dependence. No causal inference.",
    }


def matched_differences(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Equal weight per task; repetitions are averaged, never falsely treated as paired seeds."""
    bins = defaultdict(lambda: {"A": [], "B": []})
    # Disclose entirely absent task/system combinations among the supplied tasks and systems.
    for task in {row["task_id"] for row in records}:
        for agent in {row["agent_id"] for row in records}:
            bins[(task, agent)]
    for row in records:
        cells = bins[(row["task_id"], row["agent_id"])]
        if row["execution_status"] == "completed":
            cells[row["condition"]].append(int(row["full_task_success"]))
    deltas = defaultdict(list)
    incomplete = []
    for (task, agent), cells in sorted(bins.items()):
        if not cells["A"] or not cells["B"]:
            incomplete.append([task, agent])
            continue
        deltas[task].append(statistics.mean(cells["B"]) - statistics.mean(cells["A"]))
    task_means = {task: statistics.mean(values) for task, values in sorted(deltas.items())}
    return {
        "task_differences_B_minus_A": task_means,
        "equal_task_mean_difference": statistics.mean(task_means.values()) if task_means else None,
        "incomplete_task_agent_blocks": incomplete,
        "warning": "Descriptive only. Missing cells can bias comparisons; consult frozen analysis plan.",
    }
