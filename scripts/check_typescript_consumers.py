"""Type-check TypeScript golden files under ``tsc --strict`` with a
consumer probe appended (issue #4837).

A declaration that compiles on its own may still be unusable: an
object literal without an annotation infers a closed type that ``tsc``
accepts until something indexes it with a ``string`` (issue #4836).
So each golden is copied to a temporary directory with a probe
appended that uses the declared value the way its shape invites, and
every copy must compile cleanly.  Every golden file ends in ``export
{};`` and so is a module, which lets one ``tsc`` process check them
all.
"""

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import click

from scripts.bounded_command import bounded_command

# ``tsc`` type-checks the fixtures at ``TypeScript.language_version``
# (``V5``) in ``src/literalizer/languages/typescript.py``; ``--target
# es2015 --lib es2015`` matches ``JavaScript.language_version``
# (``ES2015``) in ``src/literalizer/languages/javascript.py``.  Keep
# all three in sync.
_TSC_FLAGS = (
    "--noEmit",
    "--strict",
    "--noResolve",
    "--skipLibCheck",
    "--target",
    "es2015",
    "--lib",
    "es2015",
)

_DECLARATION = re.compile(
    pattern=r"^(?:const|let|var) (\w+)(: [^=]+?)? = (.*)$",
    flags=re.MULTILINE,
)


def _probe(*, text: str) -> str:
    """Return the consumer probe for the last declaration in *text*."""
    declarations = list(_DECLARATION.finditer(string=text))
    if len(declarations) == 0:
        return ""
    declaration = declarations[-1]
    name, annotation, value = declaration[1], declaration[2], declaration[3]
    # An object literal without an annotation has no index signature,
    # so indexing it with a ``string`` is a known TS7053 under the
    # ``NEVER`` default (issue #4836); only annotated ones are indexed.
    if value.startswith("{") and annotation is not None:
        return f'void {name}["k" as string];\n'
    if value.startswith("new Map"):
        return f'void {name}.get("k" as string);\n'
    # Iterate rather than index: a typed empty tuple is ``readonly []``
    # and ``[0]`` on it is a legitimate error. Spread consumes the
    # iterator without introducing a binding that can shadow its source.
    if value.startswith(("[", "new Set")):
        return f"void [...{name}];\n"
    return f"void {name};\n"


def check_files(*, filenames: tuple[str, ...]) -> bool:
    """Type-check staged fixtures with probes and return success."""
    tsc = shutil.which(cmd="tsc")
    if tsc is None or tsc == "":
        tsc = "tsc"
    with tempfile.TemporaryDirectory() as tmpdir:
        names: list[str] = []
        for golden in filenames:
            path = Path(golden)
            text = path.read_text(encoding="utf-8")
            names.append(f"{path.parent.name}__{path.name}")
            _ = (Path(tmpdir) / names[-1]).write_text(
                data=text + _probe(text=text),
                encoding="utf-8",
            )
        result = subprocess.run(
            args=bounded_command(
                args=[tsc, *_TSC_FLAGS, *names],
                fixture=f"TypeScript V5 consumer probes ({len(names)} files)",
                timeout_seconds=240.0,
            ),
            capture_output=True,
            text=True,
            check=False,
            cwd=tmpdir,
            encoding="utf-8",
        )
    if result.returncode != 0:
        _ = sys.stderr.write(
            f"tsc --strict failed\n{result.stdout}{result.stderr}"
        )
    return result.returncode == 0


@click.command()
@click.argument("filenames", nargs=-1)
def main(filenames: tuple[str, ...]) -> None:
    """Type-check the given TypeScript golden files with probes."""
    if not check_files(filenames=filenames):
        sys.exit(1)


if __name__ == "__main__":
    main()
