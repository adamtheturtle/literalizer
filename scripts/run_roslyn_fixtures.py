"""Build and run the warm Roslyn fixture hosts used by the workflow."""

import os
import shutil
import subprocess
import tempfile
from pathlib import Path

import click

from scripts.bounded_command import bounded_command, run_bounded_command
from tests.integration.list_fixtures import fixture_paths

_HOSTS = {"csharp": ("lint-csharp", ".cs"), "vb": ("lint-vb", ".vb")}
_SCRIPTS = Path(__file__).resolve().parent


@click.command()
@click.argument("backend", type=click.Choice(choices=tuple(_HOSTS)))
def main(backend: str) -> None:
    """Publish the selected BACKEND host, then compile and run its
    fixtures.
    """
    dotnet = shutil.which(cmd="dotnet")
    if dotnet is None:
        raise click.ClickException(message="The dotnet SDK is required.")
    host, extension = _HOSTS[backend]
    fixtures = fixture_paths(extension=extension)
    if len(fixtures) == 0:
        raise click.ClickException(message=f"No {backend} fixtures.")
    with tempfile.TemporaryDirectory(
        suffix="-literalizer-roslyn"
    ) as temporary:
        directory = Path(temporary)
        publication = directory / "publish"
        run_bounded_command(
            args=[
                dotnet,
                "publish",
                _SCRIPTS / host / f"{host}.csproj",
                "-c",
                "Release",
                "-o",
                publication,
                "--nologo",
                "--artifacts-path",
                directory / "artifacts",
            ],
            fixture=f"{backend} host publication",
            timeout_seconds=300.0,
            cwd=None,
        )
        inputs = b"".join(
            os.fsencode(filename=fixture) + b"\0" for fixture in fixtures
        )
        _ = subprocess.run(
            args=bounded_command(
                args=[dotnet, publication / f"{host}.dll"],
                fixture=f"{backend} compile/run: {len(fixtures)} fixtures",
                timeout_seconds=600.0,
            ),
            input=inputs,
            check=True,
        )


if __name__ == "__main__":
    main()
