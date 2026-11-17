"""Select versioned Kotlin fixtures for the existing warm compiler
host.
"""

import os
import shutil
import subprocess
from pathlib import Path

import click

from scripts.bounded_command import bounded_command

_HOST = Path(__file__).resolve().with_name(name="lint-kotlin.kts")


@click.command()
@click.option(
    "--version", type=str, default="v2_4", envvar="KOTLIN_FIXTURE_TAG"
)
@click.option(
    "--kotlin-home",
    type=click.Path(path_type=Path, exists=True, file_okay=False),
    envvar="KOTLIN_HOME",
    required=True,
)
@click.option(
    "--timeout", type=click.FloatRange(min=0, min_open=True), default=1800.0
)
def main(*, version: str, kotlin_home: Path, timeout: float) -> None:
    """Preserve strict compilation, dependencies, execution and script
    timers.
    """
    fixtures = sorted(
        path
        for path in Path("tests/integration/cases").rglob(pattern="*.kts")
        if path.name.endswith(f"@{version}.kts")
    )
    if len(fixtures) == 0:
        raise click.ClickException(message=f"No Kotlin {version} fixtures.")
    compiler = kotlin_home / "lib/kotlin-compiler.jar"
    if not compiler.is_file():
        raise click.ClickException(
            message=f"Missing Kotlin compiler jar: {compiler}"
        )
    executable = shutil.which(cmd="kotlin")
    if executable is None:
        raise click.ClickException(
            message="The kotlin executable is required."
        )
    payload = b"".join(os.fsencode(filename=path) + b"\0" for path in fixtures)
    _ = subprocess.run(
        args=bounded_command(
            args=[executable, "-classpath", compiler, _HOST],
            fixture=f"Kotlin {version}: {len(fixtures)} fixtures",
            timeout_seconds=timeout,
        ),
        input=payload,
        check=True,
    )


if __name__ == "__main__":
    main()
