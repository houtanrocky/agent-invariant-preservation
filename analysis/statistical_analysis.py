"""Matched descriptive contrasts and optional exploratory task-cluster bootstrap."""

import argparse
import random
import statistics
from pathlib import Path

from researchctl.analysis import matched_differences, summarize
from researchctl.io import ResearchError, root_at
from researchctl.validation import load_records


def cluster_interval(
    differences: list[float], seed: int, samples: int = 5000
) -> list[float] | None:
    if len(differences) < 2:
        return None
    rng = random.Random(seed)
    estimates = sorted(
        statistics.mean(rng.choices(differences, k=len(differences))) for _ in range(samples)
    )
    return [estimates[int(samples * 0.025)], estimates[int(samples * 0.975)]]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--allow-nonresearch", action="store_true")
    parser.add_argument("--bootstrap", action="store_true")
    parser.add_argument("--seed", type=int, default=20261017)
    args = parser.parse_args()
    root = root_at(Path.cwd())
    records = load_records(root, args.path)
    summary = summarize(records, allow_nonresearch=args.allow_nonresearch)
    contrast = matched_differences(records)
    if contrast["incomplete_task_agent_blocks"]:
        raise ResearchError("Incomplete blocks: inspect missingness before comparing conditions.")
    if args.bootstrap:
        contrast["exploratory_cluster_95_percentile"] = cluster_interval(
            list(contrast["task_differences_B_minus_A"].values()), args.seed
        )
    import json

    print(
        json.dumps(
            {
                "label": summary["label"],
                "contrast": contrast,
                "inference_status": "Descriptive/exploratory; not an automatically justified test.",
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ResearchError, OSError, ValueError) as error:
        raise SystemExit(str(error)) from error
