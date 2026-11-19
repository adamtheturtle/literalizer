"""Compile and execute Java fixtures through the existing warm compiler
host.
"""

import shutil
import subprocess
import tempfile
from collections.abc import Sequence
from pathlib import Path

import click

from scripts.bounded_command import bounded_command
from tests.integration.fixture_names import is_default_module_fixture
from tests.integration.list_fixtures import fixture_paths

_HOST = Path(__file__).resolve().parents[1] / "CheckJavaSyntax.java"


def verify_coverage(
    *, release: str, fixtures: Sequence[Path], records: Sequence[str]
) -> None:
    """Compare the planned fixture population with successful native
    stages.
    """
    if len(fixtures) == 0:
        raise click.ClickException(message=f"No Java {release} fixtures.")
    expected = {
        f"{release}\t{stage}\t{fixture}"
        for fixture in fixtures
        for stage in ("compile", "execute")
    }
    observed = set(records)
    if len(records) != len(observed):
        raise click.ClickException(
            message=f"Duplicate Java {release} coverage records."
        )
    missing = sorted(expected - observed)
    unexpected = sorted(observed - expected)
    if len(missing) > 0 or len(unexpected) > 0:
        raise click.ClickException(
            message=(
                f"Java {release} fixture coverage mismatch. "
                f"Missing ({len(missing)}): {missing[:1]}; "
                f"unexpected ({len(unexpected)}): {unexpected[:1]}."
            )
        )


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
    host's compiler and class loader.
    """
    batch_size = 512
    timeout = 300.0
    java = shutil.which(cmd="java")
    if java is None:
        raise click.ClickException(message="A JDK with java is required.")
    selections: dict[str, tuple[Path, ...]] = {}
    for release in releases:
        version = f"jdk_{release}"
        fixtures = fixture_paths(
            extension=".java",
            version=version,
            include_default_module_names=True,
        )
        ordinary = tuple(
            path
            for path in fixtures
            if not is_default_module_fixture(path=path)
        )
        defaults = tuple(
            path for path in fixtures if is_default_module_fixture(path=path)
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
        records: list[str] = []
        for offset in range(0, len(fixtures), batch_size):
            batch = fixtures[offset : offset + batch_size]
            # The host creates one private compilation directory per file.
            # Own its temporary root so successes, failures and timeouts
            # all remove those directories on return.
            with tempfile.TemporaryDirectory(
                suffix="-literalizer-java"
            ) as temporary:
                report = Path(temporary) / "coverage.tsv"
                _ = subprocess.run(
                    args=bounded_command(
                        args=[
                            java,
                            f"-Djava.io.tmpdir={temporary}",
                            f"-Dliteralizer.java.coverage={report}",
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
                records.extend(report.read_text(encoding="utf-8").splitlines())
        verify_coverage(release=release, fixtures=fixtures, records=records)
        click.echo(
            message=(
                f"Java {release}: {len(fixtures)} fixtures "
                "compiled and executed."
            )
        )


if __name__ == "__main__":
    main()
