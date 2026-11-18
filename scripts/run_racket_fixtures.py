"""Compile and execute selected Racket fixtures using private
artifacts.
"""

import concurrent.futures
import os
import shutil
import tempfile
from pathlib import Path

import click

from scripts.bounded_command import run_bounded_command
from tests.integration.list_fixtures import fixture_paths


def _validate(
    *,
    fixtures: tuple[Path, ...],
    tools: dict[str, str],
    phase: str,
    jobs: int | None,
    timeout: float,
) -> None:
    """Keep compilation artifacts outside the source checkout."""
    with tempfile.TemporaryDirectory(
        suffix="-literalizer-racket"
    ) as directory:
        sources: list[Path] = []
        for index, fixture in enumerate(iterable=fixtures):
            destination = Path(directory) / str(object=index) / fixture.name
            destination.parent.mkdir()
            _ = shutil.copyfile(src=fixture, dst=destination)
            click.echo(message=f"{destination} <- {fixture}")
            sources.append(destination)
        if phase == "syntax":
            for start in range(0, len(sources), 256):
                run_bounded_command(
                    args=[
                        tools["raco"],
                        "make",
                        *sources[start : start + 256],
                    ],
                    fixture=f"Racket compile: {fixtures[start]}",
                    timeout_seconds=timeout,
                    cwd=None,
                )
        else:
            with concurrent.futures.ThreadPoolExecutor(
                max_workers=jobs
            ) as executor:
                futures = [
                    executor.submit(
                        run_bounded_command,
                        args=[tools["racket"], source],
                        fixture=f"Racket execution: {fixture}",
                        timeout_seconds=timeout,
                        cwd=None,
                    )
                    for fixture, source in zip(fixtures, sources, strict=True)
                ]
                for future in futures:
                    future.result()


@click.command()
def main() -> None:
    """Run the same native phases locally and in CI."""
    jobs = os.cpu_count()
    timeout = 600.0
    fixtures = fixture_paths(extension=".rkt")
    if len(fixtures) == 0:
        raise click.ClickException(message="No Racket fixtures.")
    tools: dict[str, str] = {}
    for name in ("raco", "racket"):
        executable = shutil.which(cmd=name)
        if executable is None:
            raise click.ClickException(
                message=f"Missing required tool: {name}"
            )
        tools[name] = executable
    for phase in ("syntax", "execution"):
        _validate(
            fixtures=fixtures,
            tools=tools,
            phase=phase,
            jobs=jobs,
            timeout=timeout,
        )


if __name__ == "__main__":
    main()
