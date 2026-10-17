"""Record actual pinned-subject baseline checks without modifying its tracked source."""

import argparse
import json
import platform
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

from researchctl.io import ResearchError, digest, read_yaml, write_json
from researchctl.target import git


def test_counts(path: Path) -> dict[str, int]:
    counts = {"passed": 0, "failed": 0, "skipped": 0}
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        action = {"pass": "passed", "fail": "failed", "skip": "skipped"}.get(event.get("Action"))
        if event.get("Test") and action:
            counts[action] += 1
    return counts


def observe(command: list[str], cwd: Path) -> dict:
    try:
        result = subprocess.run(command, cwd=cwd, capture_output=True, text=True, timeout=30)
        return {
            "command": command,
            "exit_code": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
        }
    except (OSError, subprocess.TimeoutExpired) as error:
        return {"command": command, "exit_code": None, "error": str(error)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeout-seconds", type=int, default=600)
    args = parser.parse_args()
    if args.timeout_seconds <= 0:
        parser.error("--timeout-seconds must be positive")
    root = Path(__file__).resolve().parents[1]
    target = root / ".local/dragon-market"
    config = read_yaml(root / "config/target-repository.yaml")
    sha = git(target, "rev-parse", "HEAD")
    if sha != config["baseline_commit"] or git(target, "status", "--porcelain"):
        raise ResearchError("Subject must be clean and match the configured exact commit.")
    if git(target, "remote", "get-url", "origin") != config["origin_url"]:
        raise ResearchError("Subject origin does not match configuration.")
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]
    output = root / ".local/baselines" / run_id
    output.mkdir(parents=True, exist_ok=False)
    report = {
        "label": "SUBJECT BASELINE VERIFICATION — NOT A CODING-AGENT EXPERIMENT",
        "baseline_commit": sha,
        "origin_url": config["origin_url"],
        "started_at": datetime.now(timezone.utc).isoformat(),
        "platform": platform.platform(),
        "python": platform.python_version(),
        "go": observe(["go", "version"], target),
        "go_environment": observe(
            ["go", "env", "-json", "GOVERSION", "GOOS", "GOARCH", "CGO_ENABLED", "CC"], target
        ),
        "docker_server": observe(["docker", "version", "--format", "{{json .Server}}"], target),
        "postgres_image_before": observe(
            [
                "docker",
                "image",
                "inspect",
                "postgres:16-alpine",
                "--format",
                "{{json .RepoDigests}} {{.Id}}",
            ],
            target,
        ),
        "input_sha256": {
            name: digest(target / name)
            for name in ("go.mod", "go.sum", "internal/postgres/setup_test.go")
        },
        "checks": [],
    }
    commands = [
        ("build", ["go", "build", "-mod=readonly", "./..."]),
        ("tests", ["go", "test", "-mod=readonly", "-json", "-count=1", "-timeout=5m", "./..."]),
        (
            "known_issue",
            [
                "go",
                "test",
                "-mod=readonly",
                "-json",
                "-count=1",
                "-timeout=2m",
                "./internal/postgres",
                "-run",
                "^TestKnownIssuePriorDayReleaseReducesTodaySpending$",
            ],
        ),
        (
            "race",
            ["go", "test", "-mod=readonly", "-race", "-json", "-count=1", "-timeout=5m", "./..."],
        ),
        ("vet", ["go", "vet", "-mod=readonly", "./..."]),
    ]
    for name, command in commands:
        print(f"Running {name}: {' '.join(command)}", flush=True)
        stdout_path, stderr_path = output / f"{name}.stdout.log", output / f"{name}.stderr.log"
        started = time.monotonic()
        entry = {
            "name": name,
            "command": command,
            "started_at": datetime.now(timezone.utc).isoformat(),
            "timeout_seconds": args.timeout_seconds,
        }
        with stdout_path.open("xb") as stdout, stderr_path.open("xb") as stderr:
            try:
                result = subprocess.run(
                    command,
                    cwd=target,
                    stdout=stdout,
                    stderr=stderr,
                    timeout=args.timeout_seconds,
                    check=False,
                )
                entry.update(exit_code=result.returncode, execution_status="completed")
            except subprocess.TimeoutExpired:
                entry.update(exit_code=None, execution_status="timeout")
            except OSError as error:
                entry.update(
                    exit_code=None, execution_status="prerequisite_error", error=str(error)
                )
        entry.update(
            duration_seconds=time.monotonic() - started,
            ended_at=datetime.now(timezone.utc).isoformat(),
            logs={
                str(path.relative_to(root)).replace("\\", "/"): digest(path)
                for path in (stdout_path, stderr_path)
            },
        )
        if name in ("tests", "known_issue", "race"):
            entry["test_events"] = test_counts(stdout_path)
        if name == "known_issue":
            entry["defect_reproduced"] = "KNOWN-01 CONFIRMED" in stdout_path.read_text(
                encoding="utf-8", errors="replace"
            )
            entry["interpretation"] = (
                "A passing characterization reproduces a pre-existing defect; it is not invariant success."
            )
        report["checks"].append(entry)
        write_json(output / "report.json", report)
        print(f"{name}: exit={entry['exit_code']}, {entry['duration_seconds']:.1f}s", flush=True)
    report["postgres_image_after"] = observe(
        [
            "docker",
            "image",
            "inspect",
            "postgres:16-alpine",
            "--format",
            "{{json .RepoDigests}} {{.Id}}",
        ],
        target,
    )
    report["subject_status_after"] = git(target, "status", "--porcelain")
    report["ended_at"] = datetime.now(timezone.utc).isoformat()
    report["all_commands_passed"] = all(check["exit_code"] == 0 for check in report["checks"])
    report["interpretation"] = (
        "Command success is separate from invariant truth; KNOWN-01 requires task/scope review."
    )
    write_json(output / "report.json", report)
    print(f"Report: {output / 'report.json'}", flush=True)
    return 0 if report["all_commands_passed"] and not report["subject_status_after"] else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ResearchError, OSError, ValueError, subprocess.SubprocessError) as error:
        print(f"check_target: {error}", file=sys.stderr)
        raise SystemExit(2) from error
