"""Export an explicit, history-free shared subject inventory for later isolation."""

import io
import hashlib
import json
import re
import subprocess
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any

from researchctl.io import ResearchError, contained, digest, read_json, read_yaml, write_json
from researchctl.target import git


def export_snapshot(root: Path, run_id: str, task_id: str) -> dict[str, Any]:
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,79}", run_id):
        raise ResearchError("Invalid snapshot ID.")
    if not re.fullmatch(r"T[0-9]{3}", task_id):
        raise ResearchError("Invalid task ID.")
    task = read_yaml(root / "benchmark/tasks" / (task_id + ".yaml"))
    inventory = read_json(root / "benchmark/manifests/shared-files.json")
    sha = task["baseline_commit"]
    if sha != inventory["baseline_commit"]:
        raise ResearchError("Task and reviewed export inventory commits differ.")
    checkout = root / ".local/dragon-market"
    if git(checkout, "rev-parse", sha + "^{commit}") != sha:
        raise ResearchError("Snapshot requires an exact available commit.")
    tree = {}
    for line in git(checkout, "ls-tree", "-r", sha).splitlines():
        metadata, name = line.split("\t", 1)
        mode, kind, _oid = metadata.split()
        tree[name] = (mode, kind)
    names = inventory["files"]
    if len(names) != len(set(names)):
        raise ResearchError("Duplicate export path.")
    for name in names:
        path = PurePosixPath(name)
        if (
            path.is_absolute()
            or "\\" in name
            or ":" in name
            or any(part in ("..", ".git") or part.startswith(".") for part in path.parts)
            or tree.get(name) not in (("100644", "blob"), ("100755", "blob"))
        ):
            raise ResearchError("Unsafe or nonregular export path: " + name)
    destination = contained(root, ".local/snapshots/" + run_id)
    if destination.exists():
        raise ResearchError("Snapshot already exists; do not overwrite evidence.")
    result = subprocess.run(
        ["git", "-C", str(checkout), "archive", "--format=zip", sha],
        capture_output=True,
        check=True,
        timeout=180,
    )
    destination.mkdir(parents=True)
    with zipfile.ZipFile(io.BytesIO(result.stdout)) as archive:
        for name in names:
            path = destination / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(archive.read(name))
            if tree[name][0] == "100755":
                path.chmod(0o755)
    request = (
        task["problem_description"]
        + "\n\n"
        + "\n".join("- " + value for value in task["expected_behavior"])
    )
    contract = "Shared requirements for both prompt conditions\n\n" + "\n".join(
        value["id"] + ": " + value["definition"] for value in task["existing_invariants"]
    )
    (destination / "REQUEST.md").write_text(request + "\n", encoding="utf-8", newline="\n")
    (destination / "CONTRACT.md").write_text(contract + "\n", encoding="utf-8", newline="\n")
    hashes = {
        str(path.relative_to(destination)).replace("\\", "/"): digest(path)
        for path in sorted(destination.rglob("*"))
        if path.is_file()
    }
    manifest = {
        "task_id": task_id,
        "baseline_commit": sha,
        "inventory_sha256": digest(root / "benchmark/manifests/shared-files.json"),
        "files": hashes,
        "content_sha256": hashlib.sha256(
            json.dumps(hashes, sort_keys=True).encode("utf-8")
        ).hexdigest(),
        "human_review": "pending; export is not authorization to run agents",
        "isolation": "Requires separate filesystem/account and network controls; path is not a sandbox",
    }
    write_json(root / ".local/snapshot-manifests" / (run_id + ".json"), manifest)
    return {"snapshot": str(destination), "manifest": manifest}
