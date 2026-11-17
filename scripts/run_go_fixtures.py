"""Check and execute Go fixtures with the same commands locally and in
CI.
"""

import concurrent.futures
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

import click

from scripts.bounded_command import bounded_command


def _command(
    *,
    arguments: list[str | Path],
    fixture: Path,
    phase: str,
    timeout: float,
    directory: Path | None,
) -> None:
    """Report the original fixture and retain native diagnostics."""
    _ = subprocess.run(
        args=bounded_command(
            args=arguments,
            fixture=f"Go {phase}: {fixture}",
            timeout_seconds=timeout,
        ),
        cwd=directory,
        check=True,
    )


def _run(
    *, fixture: Path, phase: str, tools: dict[str, str], timeout: float
) -> None:
    """Retain formatting diagnostics and create a separate module per
    program.
    """
    if phase == "syntax":
        _command(
            arguments=[tools["gofmt"], "-e", fixture],
            fixture=fixture,
            phase=phase,
            timeout=timeout,
            directory=None,
        )
        return
    with tempfile.TemporaryDirectory(suffix="-literalizer-go") as directory:
        root = Path(directory)
        _ = shutil.copyfile(src=fixture, dst=root / "main.go")
        _ = (root / "go.mod").write_text(data="module fixture\n\ngo 1.18\n")
        for command in ("vet", "run"):
            _command(
                arguments=[tools["go"], command, "./..."],
                fixture=fixture,
                phase=command,
                timeout=timeout,
                directory=root,
            )


@click.command()
@click.option("--case", "case_name", type=str)
@click.option(
    "--check",
    "check_kind",
    type=click.Choice(choices=("all", "syntax", "execution")),
    default="all",
)
@click.option("--jobs", type=click.IntRange(min=1), default=os.cpu_count)
@click.option(
    "--timeout", type=click.FloatRange(min=0, min_open=True), default=60.0
)
def main(
    *, case_name: str | None, check_kind: str, jobs: int, timeout: float
) -> None:
    """Validate selected fixtures with isolated temporary compiler
    output.
    """
    fixtures = sorted(
        path
        for root in (Path("tests/integration/cases"),)
        for path in root.rglob(pattern="*.go")
        if case_name is None or path.parent.name == case_name
    )
    if len(fixtures) == 0:
        raise click.ClickException(message=f"No Go fixtures: {case_name!r}")
    tools: dict[str, str] = {}
    for name in ("go", "gofmt"):
        executable = shutil.which(cmd=name)
        if executable is None:
            raise click.ClickException(
                message=f"Missing required tool: {name}"
            )
        tools[name] = executable
    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as executor:
        for phase in ("syntax", "execution"):
            if check_kind not in {"all", phase}:
                continue
            futures = [
                executor.submit(
                    _run,
                    fixture=fixture,
                    phase=phase,
                    tools=tools,
                    timeout=timeout,
                )
                for fixture in fixtures
            ]
            for future in futures:
                future.result()


if __name__ == "__main__":
    main()
