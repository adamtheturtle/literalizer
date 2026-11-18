"""Compile and execute Java fixtures through the existing warm compiler
host.
"""

import shutil
import subprocess
import tempfile
from pathlib import Path

import click

from scripts.bounded_command import bounded_command
from tests.integration.list_fixtures import CASES_DIR, fixture_paths

_HOST = Path(__file__).resolve().parents[1] / "CheckJavaSyntax.java"
_DEFAULT_MODULES = CASES_DIR.parent / "default_module_names"


@click.command()
@click.option(
    "--release",
    "releases",
    multiple=True,
    type=click.Choice(choices=("11", "16")),
    default=("11", "16"),
    show_default=True,
)
def main(releases: tuple[str, ...]) -> None:
    """Check selected releases with fatal warnings and native execution.

    LITERALIZER_LINT_CLASSPATH supplies supporting jars to the existing
    host's compiler and class loader, exactly as in CI.
    """
    batch_size = 512
    timeout = 300.0
    java = shutil.which(cmd="java")
    if java is None:
        raise click.ClickException(message="A JDK with java is required.")
    selections: dict[str, tuple[Path, ...]] = {}
    for release in releases:
        version = f"jdk_{release}"
        ordinary = fixture_paths(
            extension=".java", version=version, root=CASES_DIR
        )
        defaults = fixture_paths(
            extension=".java", version=version, root=_DEFAULT_MODULES
        )
        if len(ordinary) == 0:
            raise click.ClickException(
                message=f"No ordinary Java {version} fixtures."
            )
        if len(defaults) == 0:
            raise click.ClickException(
                message=f"No default-module Java {version} fixtures."
            )
        selections[release] = (*ordinary, *defaults)
    for release, fixtures in selections.items():
        for offset in range(0, len(fixtures), batch_size):
            batch = fixtures[offset : offset + batch_size]
            # The host creates one private compilation directory per file.
            # Own its temporary root so successes, failures and timeouts
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
