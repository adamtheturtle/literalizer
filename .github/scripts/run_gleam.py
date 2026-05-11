"""Run Gleam golden files in a single ``gleam run`` invocation.

Each Gleam invocation boots the BEAM VM, which costs ~1s. With 352
fixtures that dominated the lint job's wall-clock (3+ minutes). Instead
we drop every fixture into one project as its own module, generate a
runner module that calls each fixture's ``main`` in sequence, and run
``gleam run`` once.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


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

        module_to_fixture: dict[str, Path] = {}
        runner_imports: list[str] = []
        runner_calls: list[str] = []
        for index, fixture in enumerate(fixtures):
            module_name = f"f{index}"
            module_to_fixture[module_name] = fixture
            (src_dir / f"{module_name}.gleam").write_text(
                data=fixture.read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            runner_imports.append(f"import {module_name}")
            # Print the original fixture path before each call so a
            # runtime crash points at the culprit (the BEAM aborts with
            # no Gleam-level traceback we can post-process reliably).
            runner_calls.append(f'  io.println("RUN: {fixture}")')
            runner_calls.append(f"  {module_name}.main()")

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
        stderr = _remap_paths(
            text=result.stderr,
            module_to_fixture=module_to_fixture,
        )
        stdout = _remap_paths(
            text=result.stdout,
            module_to_fixture=module_to_fixture,
        )
        sys.stderr.write(stderr)
        sys.stderr.write(stdout)
        sys.exit(1)


def _remap_paths(
    *,
    text: str,
    module_to_fixture: dict[str, Path],
) -> str:
    """Rewrite ``src/fN.gleam`` references back to original fixture
    paths.
    """

    def replace(match: re.Match[str]) -> str:
        """Resolve a single ``src/fN.gleam`` match to its fixture path."""
        module_name = match.group(1)
        fixture = module_to_fixture.get(module_name)
        if fixture is None:
            return match.group(0)
        return str(fixture)

    return re.sub(pattern=r"src/(f\d+)\.gleam", repl=replace, string=text)


if __name__ == "__main__":
    main()
