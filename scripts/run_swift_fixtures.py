"""Check and execute Swift fixtures with the same commands locally and in
CI.
"""

import concurrent.futures
import os
import shutil
import tempfile
from pathlib import Path

import click

from scripts.bounded_command import run_bounded_command


def _run(
    *, fixture: Path, phase: str, tools: dict[str, str], timeout: float
) -> None:
    """Check types in a private copy before interpreting the unchanged
    consumer.
    """
    if phase == "execution":
        run_bounded_command(
            args=[
                tools["swift"],
                "-swift-version",
                "5",
                "-warnings-as-errors",
                fixture,
            ],
            fixture=f"Swift {phase}: {fixture}",
            timeout_seconds=timeout,
            cwd=None,
        )
        return
    with tempfile.TemporaryDirectory(suffix="-literalizer-swift") as directory:
        source = Path(directory) / "check.swift"
        _ = shutil.copyfile(src=fixture, dst=source)
        run_bounded_command(
            args=[
                tools["swiftc"],
                "-swift-version",
                "5",
                "-typecheck",
                "-warnings-as-errors",
                source,
            ],
            fixture=f"Swift {phase}: {fixture}",
            timeout_seconds=timeout,
            cwd=None,
        )


@click.command()
def main() -> None:
    """Validate selected fixtures with isolated temporary compiler
    output.
    """
    jobs = os.cpu_count()
    timeout = 60.0
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
