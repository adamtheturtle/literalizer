"""Compile and execute Java goldens through the existing warm JVM host."""

import shutil
import subprocess
import tempfile
from pathlib import Path

import click

from scripts.bounded_command import bounded_command
from tests.integration.list_fixtures import fixture_paths

_HOST = Path(__file__).resolve().parents[1] / "CheckJavaSyntax.java"


@click.command()
@click.option(
    "--release",
    "releases",
    multiple=True,
    type=click.Choice(choices=("11", "16")),
    default=("11", "16"),
    show_default=True,
)
@click.option(
    "--case", "case_name", type=str, help="Select one case directory."
)
@click.option("--batch-size", type=click.IntRange(min=1, max=512), default=512)
@click.option(
    "--timeout",
    type=click.FloatRange(min=0, min_open=True),
    default=300.0,
    show_default=True,
    help="Deadline in seconds for each warm compiler batch.",
)
def main(
    releases: tuple[str, ...],
    case_name: str | None,
    batch_size: int,
    timeout: float,
) -> None:
    """Check selected releases with fatal warnings and native execution.

    LITERALIZER_LINT_CLASSPATH supplies supporting jars to the existing
    host's compiler and class loader, exactly as in CI.
    """
    java = shutil.which(cmd="java")
    if java is None:
        raise click.ClickException(message="A JDK with java is required.")
    selections = {
        release: tuple(
            path
            for path in fixture_paths(
                extension=".java", version=f"jdk_{release}"
            )
            if case_name is None or path.parent.name == case_name
        )
        for release in releases
    }
    for release, fixtures in selections.items():
        if len(fixtures) == 0:
            raise click.ClickException(
                message=f"No Java jdk_{release} fixtures: {case_name!r}"
            )
    for release, fixtures in selections.items():
        for offset in range(0, len(fixtures), batch_size):
            batch = fixtures[offset : offset + batch_size]
            # The host creates one private compilation directory per file.
            # Own its JVM temporary root so successes, failures and timeouts
            # all remove those directories on return.
            with tempfile.TemporaryDirectory(
                suffix="-literalizer-java"
            ) as temporary:
                _ = subprocess.run(
                    args=bounded_command(
                        args=[
                            java,
                            f"-Djava.io.tmpdir={temporary}",
                            str(object=_HOST),
                            release,
                            *(str(object=fixture) for fixture in batch),
                        ],
                        fixture=(
                            f"Java jdk_{release} compile/execution: {batch[0]}"
                        ),
                        timeout_seconds=timeout,
                    ),
                    check=True,
                )


if __name__ == "__main__":
    main()
