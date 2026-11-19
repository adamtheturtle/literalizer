"""Syntax-check and execute Python fixtures under the requested
runtime.
"""

import concurrent.futures
import os
import shutil
import subprocess

import click

from scripts.bounded_command import bounded_command, run_bounded_command
from tests.integration.list_fixtures import fixture_paths


def _find_runtime(*, runtime: str) -> str:
    """Resolve the runtime through uv without loading the project."""
    uv = shutil.which(cmd="uv")
    if uv is None:
        raise click.ClickException(message="The uv executable is required.")
    result = subprocess.run(
        args=bounded_command(
            args=[
                uv,
                "run",
                "--python",
                runtime,
                "--no-project",
                "python",
                "-c",
                "import sys; print(sys.executable)",
            ],
            fixture=f"Python {runtime} interpreter resolution",
            timeout_seconds=180.0,
        ),
        stdout=subprocess.PIPE,
        text=True,
        check=True,
    )
    return result.stdout.strip()


@click.command()
@click.argument("version", type=click.Choice(choices=("py38", "py39")))
@click.option("--runtime", required=True)
def main(version: str, *, runtime: str) -> None:
    """Check both stages for every fixture in the selected VERSION."""
    executable = _find_runtime(runtime=runtime)
    fixtures = fixture_paths(extension=".py", version=version)
    if len(fixtures) == 0:
        raise click.ClickException(message=f"No Python {version} fixtures.")
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=os.cpu_count()
    ) as executor:
        for stage, arguments in (
            ("syntax", ("-m", "py_compile")),
            ("execution", ()),
        ):
            checks = [
                executor.submit(
                    run_bounded_command,
                    args=[executable, *arguments, fixture],
                    fixture=f"Python {runtime} ({version}) {stage}: {fixture}",
                    timeout_seconds=60.0,
                    cwd=None,
                )
                for fixture in fixtures
            ]
            for check in checks:
                check.result()


if __name__ == "__main__":
    main()
