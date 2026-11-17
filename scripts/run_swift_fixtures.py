"""Check and execute Swift fixtures with the same commands locally and in
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
            fixture=f"Swift {phase}: {fixture}",
            timeout_seconds=timeout,
        ),
        cwd=directory,
        check=True,
    )


def _run(
    *, fixture: Path, phase: str, tools: dict[str, str], timeout: float
) -> None:
    """Check types in a private copy before interpreting the unchanged
    consumer.
    """
    if phase == "execution":
        _command(
            arguments=[
                tools["swift"],
                "-swift-version",
                "5",
                "-warnings-as-errors",
                fixture,
            ],
            fixture=fixture,
            phase=phase,
            timeout=timeout,
            directory=None,
        )
        return
    with tempfile.TemporaryDirectory(suffix="-literalizer-swift") as directory:
        source = Path(directory) / "check.swift"
        _ = shutil.copyfile(src=fixture, dst=source)
        _command(
            arguments=[
                tools["swiftc"],
                "-swift-version",
                "5",
                "-typecheck",
                "-warnings-as-errors",
                source,
            ],
            fixture=fixture,
            phase=phase,
            timeout=timeout,
            directory=None,
        )


@click.command()
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
def main(*, check_kind: str, jobs: int, timeout: float) -> None:
    """Validate selected fixtures with isolated temporary compiler
    output.
    """
    fixtures = sorted(
        path
        for root in (Path("tests/integration/cases"),)
        for path in root.rglob(pattern="*.swift")
    )
    if len(fixtures) == 0:
        raise click.ClickException(message="No Swift fixtures.")
    tools: dict[str, str] = {}
    for name in ("swiftc", "swift"):
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
