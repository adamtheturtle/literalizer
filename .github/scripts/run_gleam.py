"""Run a Gleam golden file using ``gleam run``."""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def main() -> None:
    """Run the given Gleam golden file."""
    primed_dir = Path(os.environ["LINT_GLEAM_PRIMED_DIR"])
    filename = sys.argv[1]
    gleam_path = shutil.which(cmd="gleam") or "gleam"
    with tempfile.TemporaryDirectory() as tmpdir:
        # Copy the primed project so each parallel worker has its own
        # writable working tree and skips `gleam deps download` -- 168
        # parallel downloads otherwise hammer hex.pm and trip transient
        # network failures.
        shutil.copytree(src=primed_dir, dst=tmpdir, dirs_exist_ok=True)
        src_dir = Path(tmpdir) / "src"
        src_dir.mkdir(exist_ok=True)
        src = Path(filename)
        target = src_dir / "check.gleam"
        target.write_text(
            data=src.read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        result = subprocess.run(
            args=[gleam_path, "run"],
            capture_output=True,
            text=True,
            check=False,
            cwd=tmpdir,
        )
        if result.returncode != 0:
            msg = (
                f"{filename}: gleam run failed\n{result.stderr}{result.stdout}"
            )
            sys.stderr.write(msg)
            sys.exit(1)


if __name__ == "__main__":
    main()
