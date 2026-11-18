"""Share the warm Scala compiler and include public default modules."""

import shutil
import subprocess
import tempfile
from pathlib import Path

import click

from scripts.bounded_command import bounded_command, run_bounded_command
from scripts.fixture_staging import stage_fixture_modules
from tests.integration.list_fixtures import fixture_paths


def _validate(
    *, executable: str, names: list[str], workspace: Path, timeout: float
) -> None:
    """Retain strict compilation and launch Java through an argument
    file.
    """
    source = (
        "@main def __run(): Unit = {\n"
        + "".join(f"  val _{name} = {name}\n" for name in names)
        + "}\n"
    )
    _ = (workspace / "Main.scala").write_text(data=source)
    compiled = subprocess.run(
        args=bounded_command(
            args=[
                executable,
                "run",
                workspace,
                "--server=false",
                "-S",
                "3",
                "--scalac-option",
                "-deprecation",
                "--scalac-option",
                "-Werror",
                "--dep",
                "io.circe::circe-core:0.14.10",
                "--main-class",
                "__run",
                "--command",
            ],
            fixture="Scala compile",
            timeout_seconds=timeout,
        ),
        stdout=subprocess.PIPE,
        text=True,
        check=True,
    )
    command = compiled.stdout.splitlines()
    if len(command) == 0:
        raise click.ClickException(
            message="Scala compilation produced an empty Java command."
        )
    arguments = workspace / "java-args"
    escaped = (
        argument.replace("\\", "\\\\").replace('"', '\\"')
        for argument in command[1:]
    )
    _ = arguments.write_text(
        data="".join(f'"{argument}"\n' for argument in escaped)
    )
    run_bounded_command(
        args=[command[0], f"@{arguments}"],
        fixture="Scala execution",
        timeout_seconds=timeout,
        cwd=workspace,
    )


@click.command()
def main() -> None:
    """Compile and run the complete native fixture collection."""
    timeout = 600.0
    fixtures = fixture_paths(
        extension=".scala", include_default_module_names=True
    )
    if len(fixtures) == 0:
        raise click.ClickException(message="No Scala fixtures.")
    executable = shutil.which(cmd="scala-cli")
    if executable is None:
        raise click.ClickException(
            message="The scala-cli executable is required."
        )
    with tempfile.TemporaryDirectory(suffix="-literalizer-scala") as directory:
        workspace = Path(directory)
        names = stage_fixture_modules(
            fixtures=fixtures, workspace=workspace, default_module_name="Check"
        )
        _validate(
            executable=executable,
            names=names,
            workspace=workspace,
            timeout=timeout,
        )


if __name__ == "__main__":
    main()
