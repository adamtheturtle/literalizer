"""Check syntax of Gleam golden files using a single ``gleam check``.

Each Gleam invocation boots the BEAM VM, which costs ~1s. With 350+
fixtures that dominated the lint job's wall-clock (3+ minutes). Instead
we drop every fixture into one project as its own module and run
``gleam check`` once.

Each fixture lives under ``tests/integration/cases/<case>/<gleam>.gleam``
where both ``<case>`` and ``<gleam>`` are valid Gleam module identifiers
(this is enforced by ``make_golden_path`` in the test harness). That
means we can copy each fixture into the lint project at the same
relative path and gleam's own diagnostics already point at a recognisable
filename without any post-processing.
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

_FIXTURE_PREFIX = Path("tests/integration/cases")


def main() -> None:
    """Check syntax of all Gleam golden files passed on stdin."""
    primed_dir = Path(os.environ["LINT_GLEAM_PRIMED_DIR"])
    gleam_path = shutil.which(cmd="gleam") or "gleam"
    fixtures = [Path(line) for line in sys.stdin.read().splitlines() if line]

    with tempfile.TemporaryDirectory() as tmpdir:
        # Copy the primed project (deps already downloaded) so we do not
        # pay `gleam deps download` here.
        shutil.copytree(src=primed_dir, dst=tmpdir, dirs_exist_ok=True)
        src_dir = Path(tmpdir) / "src"
        src_dir.mkdir(exist_ok=True)

        for fixture in fixtures:
            relative = fixture.relative_to(_FIXTURE_PREFIX)
            destination = src_dir / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(
                data=fixture.read_text(encoding="utf-8"),
                encoding="utf-8",
            )

        result = subprocess.run(
            args=[gleam_path, "check"],
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
