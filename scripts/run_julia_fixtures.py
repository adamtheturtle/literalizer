"""Run selected Julia fixtures in an explicitly prepared project."""

import concurrent.futures
import os
import shutil
import subprocess
from pathlib import Path

import click

from scripts.bounded_command import bounded_command


def _run(
    *, executable: str, project: Path, fixture: Path, timeout: float
) -> None:
    """Preserve project dependencies and disable startup customization."""
    _ = subprocess.run(
        args=bounded_command(
            args=[
                executable,
                "--startup-file=no",
                f"--project={project}",
                fixture,
            ],
            fixture=f"Julia execution: {fixture}",
            timeout_seconds=timeout,
        ),
        check=True,
    )


@click.command()
@click.option(
    "--project",
    type=click.Path(path_type=Path, exists=True, file_okay=False),
    required=True,
)
@click.option("--jobs", type=click.IntRange(min=1), default=os.cpu_count)
@click.option(
    "--timeout", type=click.FloatRange(min=0, min_open=True), default=60.0
)
def main(*, project: Path, jobs: int, timeout: float) -> None:
    """Execute every fixture with the same native command."""
    fixtures = sorted(
        path for path in Path("tests/integration/cases").rglob(pattern="*.jl")
    )
    if len(fixtures) == 0:
        raise click.ClickException(message="No Julia fixtures.")
    if not (project / "Project.toml").is_file():
        raise click.ClickException(
            message=f"Missing prepared Project.toml: {project}"
        )
    executable = shutil.which(cmd="julia")
    if executable is None:
        raise click.ClickException(message="The julia executable is required.")
    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as executor:
        futures = [
            executor.submit(
                _run,
                executable=executable,
                project=project.resolve(),
                fixture=fixture,
                timeout=timeout,
            )
            for fixture in fixtures
        ]
        for future in futures:
            future.result()


if __name__ == "__main__":
    main()
