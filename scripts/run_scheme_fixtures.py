"""Execute native fixtures with the configured interpreter and module path."""

import concurrent.futures
import os
import shutil
import subprocess
from pathlib import Path

import click

from scripts.bounded_command import bounded_command


def _check(
    *, fixture: Path, arguments: tuple[str, ...], timeout: float
) -> None:
    """Preserve module loading and the disabled compilation cache."""
    _ = subprocess.run(
        args=bounded_command(
            args=[*arguments, "-s", fixture],
            fixture=str(object=fixture),
            timeout_seconds=timeout,
        ),
        check=True,
    )


@click.command()
@click.option("--case", "case_name", type=str)
@click.option("--guile", "guile_name", type=str, default="guile-3.0")
@click.option(
    "--json-path",
    type=click.Path(exists=True, path_type=Path),
    envvar="LITERALIZER_GUILE_JSON_PATH",
)
@click.option("--jobs", type=click.IntRange(min=1), default=os.cpu_count)
@click.option(
    "--timeout", type=click.FloatRange(min=0, min_open=True), default=60.0
)
def main(
    *,
    case_name: str | None,
    guile_name: str,
    json_path: Path | None,
    jobs: int,
    timeout: float,
) -> None:
    """Validate a named input or the complete native fixture corpus."""
    fixtures = sorted(
        fixture
        for fixture in Path("tests/integration/cases").rglob(pattern="*.scm")
        if case_name is None or fixture.parent.name == case_name
    )
    if len(fixtures) == 0:
        raise click.ClickException(
            message=f"No Scheme fixtures: {case_name!r}"
        )
    executable = shutil.which(cmd=guile_name)
    if executable is None:
        raise click.ClickException(
            message=f"Missing interpreter: {guile_name}"
        )
    arguments: tuple[str, ...] = (executable, "--no-auto-compile")
    if json_path is not None:
        arguments += ("-L", str(object=json_path))
    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as executor:
        for future in [
            executor.submit(
                _check, fixture=fixture, arguments=arguments, timeout=timeout
            )
            for fixture in fixtures
        ]:
            future.result()


if __name__ == "__main__":
    main()
