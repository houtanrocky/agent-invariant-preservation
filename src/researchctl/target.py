"""Pinned subject setup and clean, detached execution worktrees."""

import re
import subprocess
from pathlib import Path
from typing import Any

import yaml

from researchctl.io import ResearchError, contained, read_yaml, write_json


def git(cwd: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(cwd), *args], capture_output=True, text=True, timeout=180, check=False
    )
    if result.returncode:
        raise ResearchError(f"Git failed ({args[0]}): {result.stderr.strip()}")
    return result.stdout.strip()


def setup(root: Path, pin: str | None = None, discover_pin: bool = False) -> dict[str, Any]:
    config_path = root / "config/target-repository.yaml"
    config = read_yaml(config_path)
    sha = pin or config["baseline_commit"]
    if sha is not None and not re.fullmatch(r"[0-9a-f]{40}", sha):
        raise ResearchError("Use an exact 40-character lowercase commit SHA.")
    if sha is None and not discover_pin:
        raise ResearchError("Baseline is unpinned. Supply --pin SHA, or --discover-pin once.")
    checkout = root / ".local/dragon-market"
    checkout.parent.mkdir(exist_ok=True)
    if not checkout.exists():
        local_options = ["--local"] if Path(config["origin_url"]).is_dir() else []
        result = subprocess.run(
            ["git", "clone", *local_options, config["origin_url"], str(checkout)],
            capture_output=True,
            text=True,
            timeout=180,
            check=False,
        )
        if result.returncode:
            raise ResearchError(
                "Target clone failed; inspect network access. " + result.stderr.strip()
            )
    if git(checkout, "remote", "get-url", "origin") != config["origin_url"]:
        raise ResearchError("Local target origin differs from configured origin.")
    if git(checkout, "status", "--porcelain"):
        raise ResearchError("Target has local edits; preserve them before setup.")
    sha = git(checkout, "rev-parse", "HEAD") if sha is None else sha
    try:
        git(checkout, "cat-file", "-e", sha + "^{commit}")
    except ResearchError:
        git(checkout, "fetch", "origin", sha)
    if git(checkout, "rev-parse", sha + "^{commit}") != sha:
        raise ResearchError("Pin did not resolve to exactly the requested commit.")
    git(checkout, "checkout", "--detach", sha)
    previous_pin = config["baseline_commit"]
    config["baseline_commit"] = sha
    if previous_pin != sha:
        config["pin_status"] = "pinned_not_baseline_validated"
    config_path.write_text(yaml.safe_dump(config, sort_keys=False), encoding="utf-8", newline="\n")
    provenance = {
        "origin_url": config["origin_url"],
        "baseline_commit": sha,
        "checkout": ".local/dragon-market",
        "baseline_status": config["pin_status"],
    }
    write_json(root / ".local/target-provenance.json", provenance)
    return provenance


def worktree(root: Path, run_id: str, sha: str) -> Path:
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,79}", run_id):
        raise ResearchError("Run ID must contain only letters, digits, underscores and hyphens.")
    if not re.fullmatch(r"[0-9a-f]{40}", sha):
        raise ResearchError("A worktree needs an exact commit SHA.")
    path = contained(root, ".local/workspaces/" + run_id)
    if path.exists():
        raise ResearchError("Run workspace already exists; never overwrite prior evidence.")
    path.parent.mkdir(parents=True, exist_ok=True)
    git(root / ".local/dragon-market", "worktree", "add", "--detach", str(path), sha)
    return path
