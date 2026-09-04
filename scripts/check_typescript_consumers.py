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
    declarations = _DECLARATION.findall(string=text)
    if not declarations:
        return ""
    name, annotation, value = declarations[-1]
    # An object literal without an annotation has no index signature,
    # so indexing it with a ``string`` is a known TS7053 under the
    # ``NEVER`` default (issue #4836); only annotated ones are indexed.
    if value.startswith("{") and annotation:
        return f'const k: string = "k";\nvoid {name}[k];\n'
    if value.startswith("new Map"):
        return f'const k: string = "k";\nvoid {name}.get(k);\n'
    # Iterate rather than index: a typed empty tuple is ``readonly []``
    # and ``[0]`` on it is a legitimate error.
    if value.startswith(("[", "new Set")):
        return f"for (const item of {name}) {{\n  void item;\n}}\n"
    return f"void {name};\n"


def main() -> None:
    """Type-check the given TypeScript golden files with probes."""
    tsc = shutil.which(cmd="tsc") or "tsc"
    with tempfile.TemporaryDirectory() as tmpdir:
        names: list[str] = []
        for golden in sys.argv[1:]:
            path = Path(golden)
            text = path.read_text(encoding="utf-8")
            names.append(f"{path.parent.name}__{path.name}")
            (Path(tmpdir) / names[-1]).write_text(
                data=text + _probe(text=text),
                encoding="utf-8",
            )
        result = subprocess.run(
            args=[tsc, *_TSC_FLAGS, *names],
            capture_output=True,
            text=True,
            check=False,
            cwd=tmpdir,
            encoding="utf-8",
        )
    if result.returncode != 0:
        sys.stderr.write(
            f"tsc --strict failed\n{result.stdout}{result.stderr}"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
