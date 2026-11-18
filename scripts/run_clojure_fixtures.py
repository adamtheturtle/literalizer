"""Lint and execute selected Clojure fixtures with the native tools."""

import concurrent.futures
import os
import shutil

import click

from scripts.bounded_command import run_bounded_command
from tests.integration.list_fixtures import fixture_paths


@click.command()
def main() -> None:
    """Batch the static checks before running fixtures independently."""
    jobs = os.cpu_count()
    timeout = 60.0
    fixtures = fixture_paths(extension=".clj")
    if len(fixtures) == 0:
        raise click.ClickException(message="No Clojure fixtures.")
    tools: dict[str, str] = {}
    for name in ("clj-kondo", "bb"):
        executable = shutil.which(cmd=name)
        if executable is None:
            raise click.ClickException(
                message=f"Missing required tool: {name}"
            )
        tools[name] = executable
    for start in range(0, len(fixtures), 256):
        batch = fixtures[start : start + 256]
        run_bounded_command(
            args=[
                tools["clj-kondo"],
                "--config",
                "{:linters {:unresolved-namespace {:level :off}}}",
                "--lint",
                *batch,
            ],
            fixture=f"Clojure syntax: {batch[0]} through {batch[-1]}",
            timeout_seconds=timeout,
            cwd=None,
        )
    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as executor:
        futures = [
            executor.submit(
                run_bounded_command,
                args=[tools["bb"], fixture],
                fixture=f"Clojure execution: {fixture}",
                timeout_seconds=timeout,
                cwd=None,
            )
            for fixture in fixtures
        ]
        for future in futures:
            future.result()


if __name__ == "__main__":
    main()
