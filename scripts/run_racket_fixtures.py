"""Compile and execute selected Racket fixtures using private
artifacts.
"""

import concurrent.futures
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

import click

from scripts.bounded_command import bounded_command


def _run(*, arguments: list[str | Path], label: str, timeout: float) -> None:
    """Label native diagnostics and bound each process."""
    _ = subprocess.run(
        args=bounded_command(
            args=arguments, fixture=label, timeout_seconds=timeout
        ),
        check=True,
    )


def _validate(
    *,
    fixtures: list[Path],
    tools: dict[str, str],
    phase: str,
    jobs: int,
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
                _run(
                    arguments=[
                        tools["raco"],
                        "make",
                        *sources[start : start + 256],
                    ],
                    label=f"Racket compile: {fixtures[start]}",
                    timeout=timeout,
                )
        else:
            with concurrent.futures.ThreadPoolExecutor(
                max_workers=jobs
            ) as executor:
                futures = [
                    executor.submit(
                        _run,
                        arguments=[tools["racket"], source],
                        label=f"Racket execution: {fixture}",
                        timeout=timeout,
                    )
                    for fixture, source in zip(fixtures, sources, strict=True)
                ]
                for future in futures:
                    future.result()


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
    "--timeout", type=click.FloatRange(min=0, min_open=True), default=600.0
)
def main(
    *, case_name: str | None, check_kind: str, jobs: int, timeout: float
) -> None:
    """Run the same native phases locally and in CI."""
    fixtures = sorted(
        path
        for path in Path("tests/integration/cases").rglob(pattern="*.rkt")
        if case_name is None or path.parent.name == case_name
    )
    if len(fixtures) == 0:
        raise click.ClickException(
            message=f"No Racket fixtures: {case_name!r}"
        )
    tools: dict[str, str] = {}
    for name in ("raco", "racket"):
        executable = shutil.which(cmd=name)
        if executable is None:
            raise click.ClickException(
                message=f"Missing required tool: {name}"
            )
        tools[name] = executable
    for phase in ("syntax", "execution"):
        if check_kind in {"all", phase}:
            _validate(
                fixtures=fixtures,
                tools=tools,
                phase=phase,
                jobs=jobs,
                timeout=timeout,
            )


if __name__ == "__main__":
    main()
