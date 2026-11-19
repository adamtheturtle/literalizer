"""Build and stage the libraries shared by Rust native checks."""

import json
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import TypeGuard

import click

from scripts.bounded_command import bounded_command


def _build(*, cargo: str, project: Path) -> str:
    """Build the dependency graph once and collect Cargo's artifact
    paths.
    """
    project.mkdir()
    for args in (
        ["init", "--bin", "--vcs", "none", "--name", "literalizer-rust-deps"],
        ["add", "chrono", "serde_json"],
    ):
        _ = subprocess.run(
            args=bounded_command(
                args=[cargo, *args],
                fixture=f"Prepare Rust fixture dependencies ({args[0]})",
                timeout_seconds=180.0,
            ),
            cwd=project,
            stdout=sys.stderr,
            check=True,
        )
    _ = (project / "src" / "main.rs").write_text(
        data="use {chrono as _, serde_json as _};\nfn main() {}\n",
        encoding="utf-8",
    )
    return subprocess.run(
        args=bounded_command(
            args=[cargo, "build", "--message-format=json"],
            fixture="Build Rust fixture dependencies",
            timeout_seconds=300.0,
        ),
        cwd=project,
        stdout=subprocess.PIPE,
        encoding="utf-8",
        check=True,
    ).stdout


def _json_object(value: object, /) -> TypeGuard[dict[object, object]]:
    """Narrow a decoded JSON object before reading its fields."""
    return isinstance(value, dict)


def _json_array(value: object, /) -> TypeGuard[list[object]]:
    """Narrow a decoded JSON array before inspecting its values."""
    return isinstance(value, list)


def _libraries(*, messages: str) -> set[Path]:
    """Use Cargo's reported library paths across build directory
    layouts.
    """
    libraries: set[Path] = set()
    for line in messages.splitlines():
        event: object = json.loads(s=line)
        if _json_object(event) and event.get("reason") == "compiler-artifact":
            filenames = event.get("filenames")
            if _json_array(filenames):
                libraries.update(
                    Path(filename)
                    for filename in filenames
                    if isinstance(filename, str) and filename.endswith(".rlib")
                )
    return libraries


def _required_library(*, libraries: set[Path], crate: str) -> str:
    """Require a single library for each directly linked crate."""
    matches = [
        library.name
        for library in libraries
        if library.name.startswith(f"lib{crate}-")
    ]
    if len(matches) != 1:
        raise click.ClickException(
            message=f"Expected one {crate} library, found {len(matches)}."
        )
    return matches[0]


@click.command()
@click.argument(
    "destination", type=click.Path(path_type=Path, file_okay=False)
)
@click.option(
    "--github-env", is_flag=True, help="Emit GitHub environment file entries."
)
def main(destination: Path, *, github_env: bool) -> None:
    """Stage dependencies in a new directory and print shell exports."""
    cargo = shutil.which(cmd="cargo")
    if cargo is None:
        raise click.ClickException(message="The cargo executable is required.")
    destination = destination.absolute()
    if github_env and any(
        character in str(object=destination) for character in ("\n", "\r")
    ):
        raise click.ClickException(
            message="GitHub environment paths must fit on one line."
        )
    if destination.exists():
        raise click.ClickException(
            message=f"Destination already exists: {destination}"
        )
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        dir=destination.parent, suffix="-literalizer-rust-deps"
    ) as temporary:
        workspace = Path(temporary)
        libraries = _libraries(
            messages=_build(cargo=cargo, project=workspace / "project")
        )
        chrono = _required_library(libraries=libraries, crate="chrono")
        serde_json = _required_library(libraries=libraries, crate="serde_json")

        staged = workspace / "deps"
        staged.mkdir()
        for library in sorted(libraries):
            target = staged / library.name
            if target.exists():
                raise click.ClickException(
                    message=f"Duplicate Cargo library: {library.name}"
                )
            _ = shutil.copyfile(src=library, dst=target)
        _ = staged.rename(target=destination)
    for name, path in {
        "RUST_DEPS": destination,
        "RUST_CHRONO_RLIB": destination / chrono,
        "RUST_SERDE_JSON_RLIB": destination / serde_json,
    }.items():
        value = str(object=path)
        if github_env:
            click.echo(message=f"{name}={value}")
        else:
            click.echo(message=f"export {name}={shlex.quote(s=value)}")


if __name__ == "__main__":
    main()
