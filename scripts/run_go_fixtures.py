"""Check and execute Go fixtures with the same commands locally and in
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
    """Retain formatting diagnostics and create a separate module per
    program.
    """
    if phase == "syntax":
        run_bounded_command(
            args=[tools["gofmt"], "-e", fixture],
            fixture=f"Go {phase}: {fixture}",
            timeout_seconds=timeout,
            cwd=None,
        )
        return
    with tempfile.TemporaryDirectory(suffix="-literalizer-go") as directory:
        root = Path(directory)
        _ = shutil.copyfile(src=fixture, dst=root / "main.go")
        _ = (root / "go.mod").write_text(data="module fixture\n\ngo 1.18\n")
        for command in ("vet", "run"):
            run_bounded_command(
                args=[tools["go"], command, "./..."],
                fixture=f"Go {command}: {fixture}",
                timeout_seconds=timeout,
                cwd=root,
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
        for path in root.rglob(pattern="*.go")
    )
    if len(fixtures) == 0:
        raise click.ClickException(message="No Go fixtures.")
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
