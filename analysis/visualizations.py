"""Export labeled rate and duration figures with captions and provenance."""

import argparse
import sys
from pathlib import Path

from researchctl.analysis import summarize
from researchctl.io import ResearchError, digest, root_at, write_json
from researchctl.validation import load_records


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--output", type=Path, default=Path("analysis/output"))
    parser.add_argument("--allow-nonresearch", action="store_true")
    args = parser.parse_args()
    root = root_at(Path.cwd())
    records = load_records(root, args.path)
    report = summarize(records, allow_nonresearch=args.allow_nonresearch)
    if not report["n_evaluated"]:
        raise ResearchError("No completed observations to plot.")
    if report["data_kind"] != "observation" and args.output.resolve().is_relative_to(
        root / "paper"
    ):
        raise ResearchError("Non-research figures may not be exported into paper/.")
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    if args.output.exists() and any(args.output.iterdir()):
        raise ResearchError(
            "Output directory is not empty; preserve prior outputs or use a new path."
        )
    args.output.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.size": 10, "figure.dpi": 150, "savefig.dpi": 300})
    caption = (
        "Joint task success by prompt condition. Whiskers are marginal 95% Wilson intervals, "
        "which ignore task dependence. Durations show all attempts with measurements; missing values are omitted. "
        + report["label"]
    )
    figure, axes = plt.subplots(1, 2, figsize=(8, 3.2), constrained_layout=True)
    groups = report["groups"]["condition"]
    names = sorted(groups)
    rates = [groups[key]["rate"] for key in names]
    low = [
        rate - groups[key]["wilson_95_marginal"][0] for key, rate in zip(names, rates, strict=True)
    ]
    high = [
        groups[key]["wilson_95_marginal"][1] - rate for key, rate in zip(names, rates, strict=True)
    ]
    axes[0].bar(names, rates, color="#38678c", yerr=[low, high], capsize=4)
    axes[0].set(xlabel="Prompt condition", ylabel="Full task success proportion", ylim=(0, 1.05))
    for index, key in enumerate(names):
        axes[0].text(index, 0.03, f"n={groups[key]['n']}", ha="center", color="white")
    for condition in names:
        values = sorted(
            row["duration_seconds"]
            for row in records
            if row["condition"] == condition and row["duration_seconds"] is not None
        )
        if values:
            axes[1].step(
                values,
                [(i + 1) / len(values) for i in range(len(values))],
                where="post",
                label=condition,
            )
    axes[1].set(
        xlabel="Run duration (seconds)", ylabel="Empirical cumulative proportion", ylim=(0, 1.05)
    )
    axes[1].legend(title="Condition")
    figure.suptitle(report["label"], fontsize=10)
    for extension in ("pdf", "svg"):
        figure.savefig(args.output / f"overview.{extension}")
    plt.close(figure)
    (args.output / "caption.txt").write_text(caption + "\n", encoding="utf-8")
    write_json(
        args.output / "provenance.json",
        {
            "label": report["label"],
            "input": str(args.path),
            "input_sha256": digest(args.path),
            "command": sys.argv,
            "python": sys.version,
            "matplotlib": matplotlib.__version__,
            "script_sha256": digest(Path(__file__)),
            "summary": report,
            "outputs": {
                name: digest(args.output / name)
                for name in ("overview.pdf", "overview.svg", "caption.txt")
            },
        },
        exclusive=True,
    )
    print(args.output.resolve())
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ResearchError, OSError, ValueError) as error:
        raise SystemExit(str(error)) from error
