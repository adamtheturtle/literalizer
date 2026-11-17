"""Share the warm Scala compiler and include public default modules."""

import shutil
import subprocess
import tempfile
from pathlib import Path

import click

from scripts.bounded_command import bounded_command, run_bounded_command


def _stage(*, fixtures: list[Path], workspace: Path) -> list[str]:
    """Preserve source module identities and report every copied
    fixture.
    """
    names: list[str] = []
    for fixture in fixtures:
        stem = fixture.stem.rsplit(sep="@", maxsplit=1)[0]
        name = (
            "Check"
            if fixture.parent.name == "default_module_names"
            else f"Fixture_{fixture.parent.name}_{stem}"
        )
        destination = workspace / f"{name}.scala"
        _ = shutil.copyfile(src=fixture, dst=destination)
        click.echo(message=f"{destination.name} <- {fixture}")
        names.append(name)
    return names


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
    fixtures = sorted(
        path
        for root in (
            Path("tests/integration/cases"),
            Path("tests/integration/default_module_names"),
        )
        for path in root.rglob(pattern="*.scala")
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
        names = _stage(fixtures=fixtures, workspace=workspace)
        _validate(
            executable=executable,
            names=names,
            workspace=workspace,
            timeout=timeout,
        )


if __name__ == "__main__":
    main()
