"""Check and execute OCaml fixtures with the same commands locally and in
CI.
"""

import concurrent.futures
import os
import shutil
import tempfile
from pathlib import Path

import click

from scripts.bounded_command import run_bounded_command
from tests.integration.list_fixtures import fixture_paths

_PRELUDE = """# use "topfind";;
# require "yojson";;
let fixture = Sys.argv.(1);;
let fixture =
  if Filename.is_relative fixture then
    Filename.concat (Sys.getcwd ()) fixture
  else fixture;;
if not (Toploop.use_file Format.err_formatter fixture) then exit 1;;
"""


def _run(
    *, fixture: Path, phase: str, tools: dict[str, str], timeout: float
) -> None:
    """Keep the dependency-aware compiler and execution prelude."""
    with tempfile.TemporaryDirectory(suffix="-literalizer-ocaml") as directory:
        root = Path(directory)
        arguments: list[str | Path] = [tools["opam"], "exec", "--"]
        if phase == "syntax":
            arguments += [
                "ocamlfind",
                "ocamlopt",
                "-warn-error",
                "+a",
                "-package",
                "yojson",
                "-c",
                "-o",
                root / "check.o",
                fixture,
            ]
        else:
            prelude = root / "yojson_prelude.ml"
            _ = prelude.write_text(data=_PRELUDE)
            arguments += ["ocaml", "-warn-error", "+a", prelude, fixture]
        run_bounded_command(
            args=arguments,
            fixture=f"OCaml {phase}: {fixture}",
            timeout_seconds=timeout,
            cwd=None,
        )


@click.command()
def main() -> None:
    """Validate selected fixtures with isolated temporary compiler
    output.
    """
    jobs = os.cpu_count()
    timeout = 60.0
    fixtures = fixture_paths(extension=".ml")
    if len(fixtures) == 0:
        raise click.ClickException(message="No OCaml fixtures.")
    tools: dict[str, str] = {}
    for name in ("opam",):
        executable = shutil.which(cmd=name)
        if executable is None:
            raise click.ClickException(
                message=f"Missing required tool: {name}"
            )
        tools[name] = executable
    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as executor:
        for phase in ("syntax", "execution"):
            futures = [
                executor.submit(
                    _run,
                    fixture=fixture,
                    phase=phase,
                    tools=tools,
                    timeout=timeout,
                )
                for fixture in fixtures
            ]
            for future in futures:
                future.result()


if __name__ == "__main__":
    main()
