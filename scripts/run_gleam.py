"""Run Gleam golden files in a single ``gleam run`` invocation.

Each Gleam invocation boots the BEAM VM, which costs ~1s. With 350+
fixtures that dominated the lint job's wall-clock (3+ minutes). Instead
we drop every fixture into one project as its own module, generate a
runner module that calls each fixture's ``main`` in sequence, and run
``gleam run`` once.

Each fixture lives under ``tests/integration/cases/<case>/<gleam>.gleam``
where both ``<case>`` and ``<gleam>`` are valid Gleam module identifiers
(enforced by ``make_golden_path`` in the test harness), so the in-project
module path is the fixture's relative path with ``.gleam`` stripped.
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

_FIXTURE_PREFIX = Path("tests/integration/cases")


def _strip_version(*, relative: Path) -> Path:
    """Drop a ``@<version>`` suffix from *relative*'s stem.

    Version-tagged fixtures (e.g. ``gleam_combined@v1.gleam``)
    cannot be copied verbatim into a Gleam project because the ``@``
    is rejected as part of a module identifier.  The runtime path
    only cares about the base stem so we drop the tag on the way in.
    """
    stem = relative.stem
    if "@" in stem:
        stem = stem.rsplit(sep="@", maxsplit=1)[0]
    return relative.with_name(name=stem + relative.suffix)


def main() -> None:
    """Run every Gleam golden file passed on stdin."""
    primed_dir = Path(os.environ["LINT_GLEAM_PRIMED_DIR"])
    gleam_path = shutil.which(cmd="gleam") or "gleam"
    fixtures = [Path(line) for line in sys.stdin.read().splitlines() if line]

    with tempfile.TemporaryDirectory() as tmpdir:
        # Copy the primed project (deps already downloaded) so we do not
        # pay `gleam deps download` here.
        shutil.copytree(src=primed_dir, dst=tmpdir, dirs_exist_ok=True)
        src_dir = Path(tmpdir) / "src"
        src_dir.mkdir(exist_ok=True)

        runner_imports: list[str] = []
        runner_calls: list[str] = []
        for fixture in fixtures:
            relative = _strip_version(
                relative=fixture.relative_to(  # type: ignore[call-arg]
                    _FIXTURE_PREFIX,
                ),
            )
            destination = src_dir / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(
                data=fixture.read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            # Module path is the relative path with ``.gleam`` stripped
            # and slashes preserved (Gleam treats ``foo/bar.gleam`` as
            # module ``foo/bar``).
            module_path = relative.with_suffix(suffix="").as_posix()
            module_alias = module_path.replace("/", "_")
            runner_imports.append(f"import {module_path} as {module_alias}")
            # Print the original fixture path before each call so a
            # runtime crash points at the culprit (the BEAM aborts with
            # no Gleam-level traceback we can post-process reliably).
            # Escape backslashes and quotes so a fixture path containing
            # either does not corrupt the generated Gleam source.
            escaped = str(object=fixture)
            escaped = escaped.replace("\\", "\\\\").replace('"', '\\"')
            runner_calls.append(f'  io.println("RUN: {escaped}")')
            runner_calls.append(f"  {module_alias}.main()")

        runner_src = (
            "import gleam/io\n"
            + "\n".join(runner_imports)
            + "\n\npub fn main() {\n"
            + "\n".join(runner_calls)
            + "\n  Nil\n}\n"
        )
        (src_dir / "runner.gleam").write_text(
            data=runner_src,
            encoding="utf-8",
        )

        result = subprocess.run(
            args=[gleam_path, "run", "-m", "runner"],
            capture_output=True,
            text=True,
            check=False,
            cwd=tmpdir,
        )

    if result.returncode != 0:
        sys.stderr.write(result.stderr)
        sys.stderr.write(result.stdout)
        sys.exit(1)


if __name__ == "__main__":
    main()
