"""Synthetic repositories exercise the export boundary, never scientific correctness."""

import json
from pathlib import Path

import yaml

from researchctl.io import ResearchError, write_json
from researchctl.snapshot import export_snapshot
from researchctl.target import git
from test_researchctl import ScratchTest


class SnapshotTests(ScratchTest):
    def setUp(self):
        super().setUp()
        self.root = self.scratch
        self.checkout = self.root / ".local/dragon-market"
        self.checkout.mkdir(parents=True)
        git(self.checkout, "init")
        for name, content in {
            "go.mod": "module fixture\n",
            "internal/order/service.go": "package order\n",
            "docs/research-secret.txt": "must not be exported\n",
        }.items():
            path = self.checkout / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        git(self.checkout, "add", ".")
        git(
            self.checkout,
            "-c",
            "user.name=Artificial fixture",
            "-c",
            "user.email=fixture@example.invalid",
            "-c",
            "commit.gpgsign=false",
            "commit",
            "-m",
            "Synthetic fixture",
        )
        self.sha = git(self.checkout, "rev-parse", "HEAD")
        self.inventory = {
            "baseline_commit": self.sha,
            "files": ["go.mod", "internal/order/service.go"],
        }
        self.inventory_path = self.root / "benchmark/manifests/shared-files.json"
        self.task_path = self.root / "benchmark/tasks/T001.yaml"
        self.task_path.parent.mkdir(parents=True)
        self.task_path.write_text(
            yaml.safe_dump(
                {
                    "baseline_commit": self.sha,
                    "problem_description": "Artificial export fixture",
                    "expected_behavior": ["Preserve fixture"],
                    "existing_invariants": [{"id": "fixture", "definition": "Artificial only"}],
                }
            ),
            encoding="utf-8",
        )
        write_json(self.inventory_path, self.inventory)

    def test_exact_inventory_without_history_and_with_deterministic_hashes(self):
        (self.checkout / "go.mod").write_text("dirty source must not escape\n", encoding="utf-8")
        first = export_snapshot(self.root, "one", "T001")
        second = export_snapshot(self.root, "two", "T001")
        path = Path(first["snapshot"])
        self.assertEqual((path / "go.mod").read_text(), "module fixture\n")
        self.assertFalse((path / ".git").exists())
        self.assertFalse((path / "docs").exists())
        self.assertEqual(first["manifest"]["content_sha256"], second["manifest"]["content_sha256"])
        self.assertEqual(
            set(first["manifest"]["files"]),
            {
                "go.mod",
                "internal/order/service.go",
                "REQUEST.md",
                "CONTRACT.md",
            },
        )
        saved = json.loads((self.root / ".local/snapshot-manifests/one.json").read_text())
        self.assertEqual(saved, first["manifest"])

    def test_does_not_overwrite_and_rejects_path_escapes(self):
        export_snapshot(self.root, "one", "T001")
        with self.assertRaisesRegex(ResearchError, "already exists"):
            export_snapshot(self.root, "one", "T001")
        for run_id in ("../escape", "C:/escape", "bad/id"):
            with self.assertRaises(ResearchError):
                export_snapshot(self.root, run_id, "T001")
        with self.assertRaises(ResearchError):
            export_snapshot(self.root, "valid", "../T001")

    def test_inventory_mismatch_and_unsafe_paths_rejected_before_writing(self):
        for name in ("../go.mod", "/go.mod", "C:/go.mod", ".git/config", "missing.go"):
            self.inventory["files"] = [name]
            write_json(self.inventory_path, self.inventory)
            with self.assertRaisesRegex(ResearchError, "Unsafe"):
                export_snapshot(self.root, "unsafe", "T001")
            self.assertFalse((self.root / ".local/snapshots/unsafe").exists())
        self.inventory["baseline_commit"] = "f" * 40
        write_json(self.inventory_path, self.inventory)
        with self.assertRaisesRegex(ResearchError, "commits differ"):
            export_snapshot(self.root, "mismatch", "T001")

    def test_git_symlink_rejected(self):
        oid = git(self.checkout, "hash-object", "go.mod")
        git(self.checkout, "update-index", "--add", "--cacheinfo", "120000," + oid + ",link")
        git(
            self.checkout,
            "-c",
            "user.name=Artificial fixture",
            "-c",
            "user.email=fixture@example.invalid",
            "-c",
            "commit.gpgsign=false",
            "commit",
            "-m",
            "Synthetic symlink",
        )
        sha = git(self.checkout, "rev-parse", "HEAD")
        self.inventory.update(baseline_commit=sha, files=["link"])
        write_json(self.inventory_path, self.inventory)
        task = yaml.safe_load(self.task_path.read_text())
        task["baseline_commit"] = sha
        self.task_path.write_text(yaml.safe_dump(task), encoding="utf-8")
        with self.assertRaisesRegex(ResearchError, "nonregular"):
            export_snapshot(self.root, "symlink", "T001")
