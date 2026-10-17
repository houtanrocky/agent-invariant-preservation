"""Shell-free command adapter. A working directory is not a security sandbox."""

import os
import signal
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from researchctl.io import ResearchError


@dataclass(frozen=True)
class AgentRequest:
    command: list[str]
    workspace: Path
    prompt: str
    timeout_seconds: int
    environment: dict[str, str]


@dataclass(frozen=True)
class AgentResponse:
    returncode: int | None
    timed_out: bool
    duration_seconds: float
    stdout_path: Path
    stderr_path: Path


class AgentAdapter(Protocol):
    def execute(self, request: AgentRequest, trace_dir: Path) -> AgentResponse: ...


class CommandAdapter:
    """Prompt via stdin; callers must verify their actual CLI supports this contract."""

    def execute(self, request: AgentRequest, trace_dir: Path) -> AgentResponse:
        if not request.command or request.timeout_seconds <= 0:
            raise ResearchError("A command and positive wall-clock limit are required.")
        if not request.workspace.is_dir():
            raise ResearchError("Agent workspace does not exist.")
        trace_dir.mkdir(parents=True, exist_ok=False)
        stdout_path, stderr_path = trace_dir / "stdout.txt", trace_dir / "stderr.txt"
        # Only explicit runtime variables; do not inherit unrelated credentials or session state.
        permitted = ("PATH", "SystemRoot", "COMSPEC", "PATHEXT", "TEMP", "TMP", "LANG")
        env = {key: os.environ[key] for key in permitted if key in os.environ}
        env.update(request.environment)
        started = time.monotonic()
        kwargs = (
            {"start_new_session": True}
            if os.name != "nt"
            else {
                "creationflags": subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.CREATE_NO_WINDOW
            }
        )
        timed_out = False
        with stdout_path.open("xb") as out, stderr_path.open("xb") as err:
            process = subprocess.Popen(
                request.command,
                cwd=request.workspace,
                env=env,
                stdin=subprocess.PIPE,
                stdout=out,
                stderr=err,
                shell=False,
                **kwargs,
            )
            try:
                process.communicate(request.prompt.encode("utf-8"), timeout=request.timeout_seconds)
            except subprocess.TimeoutExpired:
                timed_out = True
                if os.name == "nt":
                    subprocess.run(
                        ["taskkill", "/PID", str(process.pid), "/T", "/F"],
                        capture_output=True,
                        check=False,
                    )
                else:
                    os.killpg(process.pid, signal.SIGKILL)
                if process.poll() is None:
                    process.kill()
                process.communicate()
        return AgentResponse(
            process.returncode, timed_out, time.monotonic() - started, stdout_path, stderr_path
        )
