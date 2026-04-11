"""Check syntax of a Gleam golden file using ``gleam check``."""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from check_syntax_helpers import fail_on_error

_GLEAM_TOML = """\
name = "check"
version = "1.0.0"
target = "erlang"

[dependencies]
gleam_stdlib = ">= 0.44.0 and < 2.0.0"
"""


def main() -> None:
    """Check syntax of the given Gleam golden file."""
    filename = sys.argv[1]
    gleam_path = shutil.which(cmd="gleam") or "gleam"
    with tempfile.TemporaryDirectory() as tmpdir:
        src_dir = Path(tmpdir) / "src"
        src_dir.mkdir()
        gleam_toml_path = Path(tmpdir) / "gleam.toml"
        gleam_toml_path.write_text(data=_GLEAM_TOML, encoding="utf-8")
        deps_result = subprocess.run(
            args=[gleam_path, "deps", "download"],
            capture_output=True,
            text=True,
            check=False,
            cwd=tmpdir,
        )
        fail_on_error(
            result=deps_result,
            filename=filename,
            label="gleam deps download failed",
        )
        src = Path(filename)
        target = src_dir / "check.gleam"
        target.write_text(
            data=src.read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        result = subprocess.run(
            args=[gleam_path, "check"],
            capture_output=True,
            text=True,
            check=False,
            cwd=tmpdir,
        )
        fail_on_error(
            result=result,
            filename=filename,
            label="gleam check failed",
        )


if __name__ == "__main__":
    main()
