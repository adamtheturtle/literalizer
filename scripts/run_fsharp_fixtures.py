"""Load the F# fixture corpus through one warm F# Interactive process."""

import os
import shutil
import subprocess
import tempfile
from pathlib import Path

import click

from scripts.bounded_command import bounded_command
from tests.integration.list_fixtures import fixture_paths


@click.command()
def main() -> None:
    """Load every F# 8.0 fixture with warnings treated as errors."""
    dotnet = shutil.which(cmd="dotnet")
    if dotnet is None:
        raise click.ClickException(message="The dotnet SDK is required.")
    fixtures = fixture_paths(
        extension=None, language="FSharp", include_default_module_names=True
    )
    if len(fixtures) == 0:
        raise click.ClickException(message="No F# fixtures.")
    with tempfile.TemporaryDirectory(
        suffix="-literalizer-fsharp"
    ) as temporary:
        driver = Path(temporary) / "driver.fsx"
        lines: list[str] = []
        for fixture in fixtures:
            absolute = str(object=fixture.resolve())
            escaped = absolute.replace('"', '""')
            lines.append(f'#load @"{escaped}"\n')
        _ = driver.write_text(data="".join(lines), encoding="utf-8")
        _ = subprocess.run(
            args=bounded_command(
                args=[
                    dotnet,
                    "fsi",
                    "--nologo",
                    "--warnaserror+",
                    "--langversion:8.0",
                    "--exec",
                    driver,
                ],
                fixture=f"F# 8.0 execution: {len(fixtures)} fixtures",
                timeout_seconds=600.0,
            ),
            env={
                **os.environ,
                "DOTNET_SKIP_FIRST_TIME_EXPERIENCE": "1",
                "DOTNET_NOLOGO": "1",
            },
            check=True,
        )


if __name__ == "__main__":
    main()
