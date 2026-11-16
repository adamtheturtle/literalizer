"""Lint and execute selected Clojure fixtures with the native tools."""

import concurrent.futures
import os
import shutil
import subprocess
from pathlib import Path

import click

from scripts.bounded_command import bounded_command


def _run(*, arguments: list[str | Path], label: str, timeout: float) -> None:
    """Retain native diagnostics and label each bounded invocation."""
    _ = subprocess.run(
        args=bounded_command(
            args=arguments, fixture=label, timeout_seconds=timeout
        ),
        check=True,
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
    """Batch the static checks before running fixtures independently."""
    fixtures = sorted(
        path
        for path in Path("tests/integration/cases").rglob(pattern="*.clj")
        if case_name is None or path.parent.name == case_name
    )
    if len(fixtures) == 0:
        raise click.ClickException(
            message=f"No Clojure fixtures: {case_name!r}"
        )
    tools = {}
    for name in (
        ("clj-kondo",)
        if check_kind == "syntax"
        else ("bb",)
        if check_kind == "execution"
        else ("clj-kondo", "bb")
    ):
        executable = shutil.which(cmd=name)
        if executable is None:
            raise click.ClickException(
                message=f"Missing required tool: {name}"
            )
        tools[name] = executable
    if check_kind in {"all", "syntax"}:
        for start in range(0, len(fixtures), 256):
            batch = fixtures[start : start + 256]
            _run(
                arguments=[
                    tools["clj-kondo"],
                    "--config",
                    "{:linters {:unresolved-namespace {:level :off}}}",
                    "--lint",
                    *batch,
                ],
                label=f"Clojure syntax: {batch[0]} through {batch[-1]}",
                timeout=timeout,
            )
    if check_kind in {"all", "execution"}:
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=jobs
        ) as executor:
            futures = [
                executor.submit(
                    _run,
                    arguments=[tools["bb"], fixture],
                    label=f"Clojure execution: {fixture}",
                    timeout=timeout,
                )
                for fixture in fixtures
            ]
            for future in futures:
                future.result()


if __name__ == "__main__":
    main()
