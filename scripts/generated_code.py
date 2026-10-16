"""Run generated source projects through compilers and consumers locally.

Only project materialization, command execution and failure reporting belong
here. Callers select compiler paths, flags, deadlines, batching and
assertions. In particular this module imports neither Literalizer nor pytest.
"""

import subprocess
import tempfile
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

__all__ = ["Step", "run_project"]


@dataclass(frozen=True)
class Step:
    """A command and its diagnostic label, run in the temporary
    project.
    """

    args: Sequence[str]
    failure_label: str


def run_project(
    *, label: str, files: Mapping[str, str], steps: Sequence[Step]
) -> tuple[subprocess.CompletedProcess[str], ...]:
    """Run steps in one fresh project and return their captured output.

    Files must have project-relative paths. Every step must succeed; failures
    raise an assertion containing the fixture label, command, output and all
    source/supporting files. The temporary project is removed on every exit.
    Commands run without a shell. Callers wrap commands that need deadlines
    or process-group cleanup before passing them here.

    No output equality is implied. A caller can snapshot sources without
    running commands, type-check without running a program, or assert on any
    step's output using its own semantic comparison.
    """
    for name in files:
        path = Path(name)
        if len(path.anchor) > 0 or ".." in path.parts or path == Path():
            msg = f"{label}: expected a project-relative file path: {name!r}"
            raise ValueError(msg)
    results: list[subprocess.CompletedProcess[str]] = []
    with tempfile.TemporaryDirectory() as tmpdir_name:
        tmpdir = Path(tmpdir_name)
        for name, content in files.items():
            path = tmpdir / name
            path.parent.mkdir(parents=True, exist_ok=True)
            _ = path.write_text(data=content, encoding="utf-8")
        for step in steps:
            args = list(step.args)
            try:
                result = subprocess.run(
                    args=args,
                    capture_output=True,
                    text=True,
                    check=False,
                    cwd=tmpdir,
                    encoding="utf-8",
                )
            except OSError as exc:
                msg = f"{label}: {step.failure_label}\n{args!r}: {exc}"
                raise AssertionError(msg) from exc
            if result.returncode != 0:
                sources = "\n".join(
                    f"{name}:\n{content}" for name, content in files.items()
                )
                msg = (
                    f"{label}: {step.failure_label} "
                    f"(status {result.returncode})\n"
                    f"Command: {args!r}\n{result.stdout}{result.stderr}"
                    f"\nProject files:\n{sources}\n"
                )
                raise AssertionError(msg)
            results.append(result)
    return tuple(results)
