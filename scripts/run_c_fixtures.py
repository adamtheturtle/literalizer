"""Compile and execute native fixtures with fatal compiler warnings."""

import concurrent.futures
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

import click

from scripts.bounded_command import bounded_command


def _check(*, fixture: Path, compiler: str, timeout: float) -> None:
    """Build a private executable and preserve public default entry
    names.
    """
    with tempfile.TemporaryDirectory(suffix="-literalizer-c") as temporary:
        directory = Path(temporary)
        source = fixture
        if fixture.parent.name == "default_module_names":
            _ = shutil.copyfile(src=fixture, dst=directory / "module.c")
            source = directory / "check.c"
            _ = source.write_text(
                data=(
                    '#include "module.c"\n'
                    "int main(void) { return Module(); }\n"
                ),
                encoding="utf-8",
            )
        output = directory / "run"
        _ = subprocess.run(
            args=bounded_command(
                args=[
                    compiler,
                    "-std=c99",
                    "-Werror",
                    source,
                    "-o",
                    output,
                    "-lcjson",
                ],
                fixture=f"C compilation: {fixture}",
                timeout_seconds=timeout,
            ),
            check=True,
        )
        _ = subprocess.run(
            args=bounded_command(
                args=[output],
                fixture=f"C execution: {fixture}",
                timeout_seconds=timeout,
            ),
            check=True,
        )


@click.command()
@click.option("--jobs", type=click.IntRange(min=1), default=os.cpu_count)
@click.option(
    "--timeout", type=click.FloatRange(min=0, min_open=True), default=60.0
)
def main(*, jobs: int, timeout: float) -> None:
    """Validate the complete supported native corpus."""
    roots = (
        Path("tests/integration/cases"),
        Path("tests/integration/default_module_names"),
    )
    fixtures = sorted(
        fixture for root in roots for fixture in root.rglob(pattern="*.c")
    )
    if len(fixtures) == 0:
        raise click.ClickException(message="No C fixtures.")
    compiler = shutil.which(cmd="clang")
    if compiler is None:
        raise click.ClickException(message="The clang executable is required.")
    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as executor:
        for future in [
            executor.submit(
                _check, fixture=fixture, compiler=compiler, timeout=timeout
            )
            for fixture in fixtures
        ]:
            future.result()


if __name__ == "__main__":
    main()
