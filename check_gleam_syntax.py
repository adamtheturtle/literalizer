"""Check syntax of Gleam golden files using ``gleam check``."""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

_GLEAM_TOML = """\
name = "check"
version = "1.0.0"
target = "erlang"

[dependencies]
gleam_stdlib = ">= 0.44.0 and < 2.0.0"
"""


def main() -> None:
    """Check syntax of each given Gleam golden file."""
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
        if deps_result.returncode != 0:
            msg = (
                f"gleam deps download failed\n"
                f"{deps_result.stderr}{deps_result.stdout}"
            )
            sys.stderr.write(msg)
            sys.exit(1)
        for filename in sys.argv[1:]:
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
            if result.returncode != 0:
                msg = (
                    f"{filename}: gleam check failed\n"
                    f"{result.stderr}{result.stdout}"
                )
                sys.stderr.write(msg)
                sys.exit(1)


if __name__ == "__main__":
    main()
