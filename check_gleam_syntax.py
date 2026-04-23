"""Check syntax of a Gleam golden file using ``gleam check``."""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

_GLEAM_TOML_PATH = (
    Path(__file__).parent / ".github" / "scripts" / "lint-gleam.toml"
)


def main() -> None:
    """Check syntax of the given Gleam golden file."""
    gleam_toml = _GLEAM_TOML_PATH.read_text(encoding="utf-8")
    filename = sys.argv[1]
    gleam_path = shutil.which(cmd="gleam") or "gleam"
    with tempfile.TemporaryDirectory() as tmpdir:
        src_dir = Path(tmpdir) / "src"
        src_dir.mkdir()
        gleam_toml_path = Path(tmpdir) / "gleam.toml"
        gleam_toml_path.write_text(data=gleam_toml, encoding="utf-8")
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
