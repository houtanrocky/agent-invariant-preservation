"""Infrastructure tests use explicitly artificial local fixtures, never empirical evidence."""

import copy
import io
import json
import os
import shutil
import stat
import subprocess
import sys
import time
import unittest
import uuid
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

import yaml

from researchctl.adapters import AgentRequest, CommandAdapter
from researchctl.analysis import matched_differences, summarize, wilson
from researchctl.cli import main
from researchctl.demo import smoke
from researchctl.io import (
    ResearchError,
    contained,
    digest,
    read_json,
    read_yaml,
    write_json,
)
from researchctl.target import setup, worktree
from researchctl.validation import load_records, result_check, schema_check, task_check

ROOT = Path(__file__).resolve().parents[1]


class ScratchTest(unittest.TestCase):
    def setUp(self) -> None:
        self.scratch = ROOT / ".local/test-work" / uuid.uuid4().hex
        self.scratch.mkdir(parents=True)

    def tearDown(self) -> None:
        resolved = self.scratch.resolve()
        self.assertTrue(resolved.is_relative_to((ROOT / ".local/test-work").resolve()))

        def writable_retry(function, path, _error):
            os.chmod(path, stat.S_IWRITE | stat.S_IREAD)
            function(path)

        for attempt in range(20):
            try:
                shutil.rmtree(resolved, onerror=writable_retry)
                break
            except PermissionError:
                if attempt == 19:
                    raise
                time.sleep(0.1)


class ValidationTests(ScratchTest):
    def setUp(self) -> None:
        super().setUp()
        self.record = read_json(ROOT / "data/examples/synthetic-runs.json")[0]
        self.task = read_yaml(ROOT / "benchmark/tasks/T001.yaml")

    def test_candidate_reports_incomplete_gates(self) -> None:
        missing = task_check(ROOT, self.task)
        self.assertIn("pinned baseline commit", missing)
        self.assertIn("mutant evidence", missing)

    def test_configuration_schema_rejects_negative_timeout(self) -> None:
        agents = read_yaml(ROOT / "config/agents.example.yaml")
        schema_check(ROOT, "agents-config", agents)
        agents["agents"][0]["timeout_seconds"] = -1
        with self.assertRaises(ResearchError):
            schema_check(ROOT, "agents-config", agents)

    def test_unproven_promotion_rejected(self) -> None:
        self.task["validation_status"] = "validated"
        with self.assertRaisesRegex(ResearchError, "not validated"):
            task_check(ROOT, self.task)

    def test_candidate_require_validated_rejected(self) -> None:
        with self.assertRaises(ResearchError):
            task_check(ROOT, self.task, require_validated=True)

    def test_floating_commit_rejected(self) -> None:
        self.task["baseline_commit"] = "main"
        with self.assertRaises(ResearchError):
            task_check(ROOT, self.task)

    def test_duplicate_invariant_rejected(self) -> None:
        self.task["existing_invariants"] *= 2
        with self.assertRaisesRegex(ResearchError, "unique"):
            task_check(ROOT, self.task)

    def test_empty_command_rejected(self) -> None:
        self.task["evaluation_commands"] = [[]]
        with self.assertRaises(ResearchError):
            task_check(ROOT, self.task)

    def test_unknown_fields_rejected(self) -> None:
        self.record["invented_measurement"] = 0
        with self.assertRaises(ResearchError):
            result_check(ROOT, self.record)

    def test_outcome_conjunction_enforced(self) -> None:
        self.record["full_task_success"] = True
        with self.assertRaisesRegex(ResearchError, "feature AND"):
            result_check(ROOT, self.record)

    def test_missing_invariant_cannot_pass(self) -> None:
        self.record["invariant_results"]["refund-once"] = None
        with self.assertRaisesRegex(ResearchError, "outcomes"):
            result_check(ROOT, self.record)

    def test_empty_invariant_map_rejected(self) -> None:
        self.record["invariant_results"] = {}
        with self.assertRaises(ResearchError):
            result_check(ROOT, self.record)

    def test_environment_error_kept_unknown(self) -> None:
        self.record.update(
            execution_status="environment_error",
            full_task_success=None,
            failure_category="environment",
            functional_passes=None,
            build_passes=None,
        )
        result_check(ROOT, self.record)
        self.record["full_task_success"] = False
        with self.assertRaises(ResearchError):
            result_check(ROOT, self.record)

    def test_environment_error_not_ordinary_completed_failure(self) -> None:
        self.record["failure_category"] = "environment"
        with self.assertRaises(ResearchError):
            result_check(ROOT, self.record)

    def test_no_fabricated_zero_for_missing_resources(self) -> None:
        result_check(ROOT, self.record)
        self.assertIsNone(self.record["input_tokens"])
        self.record["input_tokens"] = -1
        with self.assertRaises(ResearchError):
            result_check(ROOT, self.record)

    def test_nonfinite_resources_rejected(self) -> None:
        self.record["duration_seconds"] = float("nan")
        with self.assertRaises(ResearchError):
            result_check(ROOT, self.record)

    def test_reversed_timestamps_rejected(self) -> None:
        self.record["ended_at"] = "2025-01-01T00:00:00Z"
        with self.assertRaisesRegex(ResearchError, "before"):
            result_check(ROOT, self.record)

    def test_synthetic_label_required(self) -> None:
        self.record["data_label"] = "research results"
        with self.assertRaises(ResearchError):
            result_check(ROOT, self.record)

    def test_observation_requires_pin_and_validated_task(self) -> None:
        self.record["data_kind"] = "observation"
        with self.assertRaisesRegex(ResearchError, "pinned"):
            result_check(ROOT, self.record)
        self.record["baseline_commit"] = "a" * 40
        with self.assertRaisesRegex(ResearchError, "not validated"):
            result_check(ROOT, self.record)

    def test_duplicate_run_ids_rejected(self) -> None:
        path = self.scratch / "runs.json"
        write_json(path, [self.record, self.record])
        with self.assertRaisesRegex(ResearchError, "Duplicate"):
            load_records(ROOT, path)

    def test_jsonl_and_empty_input(self) -> None:
        path = self.scratch / "runs.jsonl"
        path.write_text(json.dumps(self.record) + "\n\n", encoding="utf-8")
        self.assertEqual(len(load_records(ROOT, path)), 1)
        path.write_text("", encoding="utf-8")
        self.assertEqual(load_records(ROOT, path), [])

    def test_path_traversal_rejected(self) -> None:
        with self.assertRaisesRegex(ResearchError, "escapes"):
            contained(ROOT, "../outside")

    def test_validated_evidence_hash_and_mutant_contract(self) -> None:
        # Artificial reports test validator behavior; they are never retained as study evidence.
        root = self.scratch
        shutil.copytree(ROOT / "data/schemas", root / "data/schemas")
        task = copy.deepcopy(self.task)
        task.update(
            baseline_commit="a" * 40,
            validation_status="validated",
            human_reviewer="software-test-reviewer",
            reference_solution_status="human_validated",
            evaluation_commands=[["python", "artificial-evaluator.py"]],
        )
        artifact = root / "fixture.txt"
        artifact.write_text("SYNTHETIC SOFTWARE-TEST ARTIFACT", encoding="utf-8")
        for role in task["evidence"]:
            code = 1 if role == "mutant" else 0
            report = {
                "task_id": task["task_id"],
                "baseline_commit": task["baseline_commit"],
                "role": role,
                "command": ["synthetic-software-test"],
                "executed_at": "2026-01-01T00:00:00Z",
                "expected_exit_code": code,
                "actual_exit_code": code,
                "reviewer": "software-test-reviewer",
                "artifacts": [{"path": "fixture.txt", "sha256": digest(artifact)}],
                "rationale": "Artificial validator contract fixture only",
            }
            path = root / f"{role}.json"
            write_json(path, report)
            task["evidence"][role] = {"path": path.name, "sha256": digest(path)}
        self.assertEqual(task_check(root, task), [])
        mutant = root / "mutant.json"
        report = read_json(mutant)
        report.update(actual_exit_code=0, expected_exit_code=0)
        write_json(mutant, report)
        task["evidence"]["mutant"]["sha256"] = digest(mutant)
        with self.assertRaisesRegex(ResearchError, "defective"):
            task_check(root, task)
        artifact.write_text("altered", encoding="utf-8")
        with self.assertRaisesRegex(ResearchError, "altered"):
            task_check(root, task)


class AnalysisTests(unittest.TestCase):
    def setUp(self) -> None:
        self.records = read_json(ROOT / "data/examples/synthetic-runs.json")

    def test_default_rejects_synthetic(self) -> None:
        with self.assertRaisesRegex(ResearchError, "Non-research"):
            summarize(self.records)

    def test_rates_and_missingness(self) -> None:
        result = summarize(self.records, allow_nonresearch=True)
        self.assertEqual(result["groups"]["condition"]["A"]["rate"], 0.5)
        self.assertEqual(result["groups"]["condition"]["B"]["rate"], 1)
        self.assertEqual(result["resources"]["input_tokens"]["n_missing"], 4)
        self.assertIsNone(result["resources"]["input_tokens"]["sum"])

    def test_mixed_kinds_rejected_even_with_opt_in(self) -> None:
        self.records[0]["data_kind"] = "observation"
        with self.assertRaisesRegex(ResearchError, "mix"):
            summarize(self.records, allow_nonresearch=True)

    def test_empty_summary_is_not_results(self) -> None:
        result = summarize([])
        self.assertEqual(result["n_records"], 0)
        self.assertEqual(result["data_kind"], "no_data")

    def test_environment_errors_have_separate_denominator(self) -> None:
        self.records[0].update(
            execution_status="environment_error",
            full_task_success=None,
            failure_category="environment",
        )
        result = summarize(self.records, allow_nonresearch=True)
        self.assertEqual(result["n_records"], 4)
        self.assertEqual(result["n_evaluated"], 3)
        self.assertEqual(result["n_environment_errors"], 1)

    def test_matched_contrast_averages_repetitions(self) -> None:
        result = matched_differences(self.records)
        self.assertEqual(result["equal_task_mean_difference"], 0.5)

    def test_missing_condition_block_disclosed(self) -> None:
        result = matched_differences(self.records[:2])
        self.assertEqual(result["incomplete_task_agent_blocks"], [["T001", "fake-system"]])
        self.assertIsNone(result["equal_task_mean_difference"])

    def test_all_environment_block_still_disclosed(self) -> None:
        for row in self.records:
            row["execution_status"] = "environment_error"
        self.assertTrue(matched_differences(self.records)["incomplete_task_agent_blocks"])

    def test_entirely_absent_task_system_combination_disclosed(self) -> None:
        extra = copy.deepcopy(self.records)
        for row in extra:
            row.update(task_id="T002", agent_id="second-fake-system")
        result = matched_differences(self.records + extra)
        self.assertEqual(len(result["incomplete_task_agent_blocks"]), 2)

    def test_wilson_zero_and_all_success(self) -> None:
        self.assertIsNone(wilson(0, 0))
        self.assertAlmostEqual(wilson(0, 10)[0], 0)
        self.assertAlmostEqual(wilson(10, 10)[1], 1)
        self.assertGreater(wilson(0, 10)[1], 0)


class ExecutionTests(ScratchTest):
    def test_adapter_reads_stdin_and_filters_unrelated_credentials(self) -> None:
        env_name = "RESEARCHCTL_TEST_UNRELATED_SECRET"
        previous = os.environ.get(env_name)
        os.environ[env_name] = "artificial-test-value"
        try:
            code = f"import os,sys; assert {env_name!r} not in os.environ; print(sys.stdin.read())"
            response = CommandAdapter().execute(
                AgentRequest([sys.executable, "-c", code], self.scratch, "hello", 5, {}),
                self.scratch / "trace",
            )
        finally:
            if previous is None:
                os.environ.pop(env_name, None)
            else:
                os.environ[env_name] = previous
        self.assertEqual(response.returncode, 0)
        self.assertEqual(response.stdout_path.read_text().strip(), "hello")

    def test_adapter_timeout(self) -> None:
        response = CommandAdapter().execute(
            AgentRequest(
                [sys.executable, "-c", "import time; time.sleep(20)"], self.scratch, "", 1, {}
            ),
            self.scratch / "trace",
        )
        self.assertTrue(response.timed_out)
        self.assertLess(response.duration_seconds, 10)

    def test_adapter_nonzero_exit_retained(self) -> None:
        response = CommandAdapter().execute(
            AgentRequest([sys.executable, "-c", "raise SystemExit(7)"], self.scratch, "", 5, {}),
            self.scratch / "trace",
        )
        self.assertEqual(response.returncode, 7)

    def test_actual_end_to_end_smoke_and_provenance(self) -> None:
        output = self.scratch / "demo"
        result = smoke(ROOT, output)
        record = read_json(output / "run.json")
        result_check(ROOT, record)
        self.assertEqual(record["data_kind"], "infrastructure")
        self.assertEqual(result["summary"]["n_evaluated"], 1)
        for name, sha in read_json(output / "manifest.json")["files"].items():
            self.assertEqual(digest(output / name), sha)
        with self.assertRaisesRegex(ResearchError, "already exists"):
            smoke(ROOT, output)

    def test_cli_commands_and_readable_error(self) -> None:
        for command in (
            ["doctor"],
            ["status"],
            ["list-tasks"],
            ["summarize"],
            ["reproduce"],
            ["validate-task", "benchmark/tasks/T001.yaml"],
            ["validate-data", "data/examples/synthetic-runs.json"],
        ):
            with redirect_stdout(io.StringIO()) as stream:
                self.assertEqual(main(["--root", str(ROOT), *command]), 0)
            json.loads(stream.getvalue())
        with redirect_stderr(io.StringIO()) as stream:
            self.assertEqual(main(["--root", str(ROOT), "setup-target"]), 2)
        self.assertIn("unpinned", stream.getvalue())

    def test_new_task_is_candidate_and_never_overwrites(self) -> None:
        root = self.scratch
        (root / "config").mkdir()
        (root / "config/study.yaml").write_text("{}", encoding="utf-8")
        shutil.copytree(ROOT / "benchmark/task-template", root / "benchmark/task-template")
        (root / "benchmark/tasks").mkdir()
        command = ["--root", str(root), "new-task", "T009", "--title", "Software-test task"]
        with redirect_stdout(io.StringIO()):
            self.assertEqual(main(command), 0)
        self.assertEqual(
            read_yaml(root / "benchmark/tasks/T009.yaml")["validation_status"], "candidate"
        )
        with redirect_stderr(io.StringIO()):
            self.assertEqual(main(command), 2)


@unittest.skipUnless(shutil.which("git"), "Git is required for local target mechanism integration")
class TargetTests(ScratchTest):
    def run_git(self, path: Path, *args: str) -> str:
        return subprocess.run(
            ["git", "-C", str(path), *args], check=True, capture_output=True, text=True
        ).stdout.strip()

    def test_pinned_existing_checkout_worktree_and_dirty_preservation(self) -> None:
        source = self.scratch / "source"
        source.mkdir()
        self.run_git(source, "init", "-b", "main")
        (source / "fixture.txt").write_text("artificial local clone fixture", encoding="utf-8")
        self.run_git(source, "add", ".")
        self.run_git(
            source,
            "-c",
            "user.name=Software Test",
            "-c",
            "user.email=test@example.invalid",
            "commit",
            "-m",
            "test fixture",
        )
        sha = self.run_git(source, "rev-parse", "HEAD")
        project = self.scratch / "project"
        (project / "config").mkdir(parents=True)
        config_path = project / "config/target-repository.yaml"
        config_path.write_text(
            yaml.safe_dump({"origin_url": source.as_posix(), "baseline_commit": None}),
            encoding="utf-8",
        )
        # Prepare an existing subject checkout without Git's MSYS upload-pack subprocess.
        existing = project / ".local/dragon-market"
        shutil.copytree(source, existing)
        self.run_git(existing, "remote", "add", "origin", source.as_posix())
        result = setup(project, discover_pin=True)
        self.assertEqual(result["baseline_commit"], sha)
        self.assertEqual(setup(project)["baseline_commit"], sha)
        checkout = worktree(project, "test-run", sha)
        self.assertEqual(self.run_git(checkout, "rev-parse", "HEAD"), sha)
        self.assertTrue((checkout / "fixture.txt").is_file())
        with self.assertRaisesRegex(ResearchError, "already exists"):
            worktree(project, "test-run", sha)
        with self.assertRaises(ResearchError):
            worktree(project, "../outside", sha)
        target = project / ".local/dragon-market/fixture.txt"
        target.write_text("preserve local edit", encoding="utf-8")
        with self.assertRaisesRegex(ResearchError, "local edits"):
            setup(project)
        self.assertEqual(target.read_text(), "preserve local edit")

    def test_local_clone_and_pin(self) -> None:
        source = self.scratch / "source"
        source.mkdir()
        self.run_git(source, "init", "-b", "main")
        (source / "fixture.txt").write_text("artificial local clone fixture", encoding="utf-8")
        self.run_git(source, "add", ".")
        self.run_git(
            source,
            "-c",
            "user.name=Software Test",
            "-c",
            "user.email=test@example.invalid",
            "commit",
            "-m",
            "test fixture",
        )
        project = self.scratch / "project"
        (project / "config").mkdir(parents=True)
        (project / "config/target-repository.yaml").write_text(
            yaml.safe_dump({"origin_url": source.as_posix(), "baseline_commit": None}),
            encoding="utf-8",
        )
        try:
            result = setup(project, discover_pin=True)
        except ResearchError as error:
            if "couldn't create signal pipe" in str(error):
                self.skipTest("Managed Windows sandbox blocks Git MSYS upload-pack subprocess")
            raise
        self.assertEqual(result["baseline_commit"], self.run_git(source, "rev-parse", "HEAD"))

    def test_floating_setup_pin_rejected_without_network(self) -> None:
        project = self.scratch
        (project / "config").mkdir()
        (project / "config/target-repository.yaml").write_text(
            yaml.safe_dump(
                {"origin_url": "https://example.invalid/subject", "baseline_commit": "main"}
            ),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(ResearchError, "exact"):
            setup(project)


if __name__ == "__main__":
    unittest.main()
