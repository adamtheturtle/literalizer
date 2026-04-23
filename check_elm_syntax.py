"""Check syntax of Elm golden files using ``elm make``."""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from elm_common import ELM_JSON


def main() -> None:
    """Check syntax of the given Elm golden files."""
    filenames = sys.argv[1:]
    elm_path = shutil.which(cmd="elm") or "elm"
    failed = False
    with tempfile.TemporaryDirectory() as tmpdir:
        src_dir = Path(tmpdir) / "src"
        src_dir.mkdir()
        elm_json_path = Path(tmpdir) / "elm.json"
        elm_json_path.write_text(data=ELM_JSON, encoding="utf-8")
        elm_home = Path(tmpdir) / ".elm"
        elm_home.mkdir()
        env = {**os.environ, "ELM_HOME": str(object=elm_home)}
        target = src_dir / "Check.elm"
        for filename in filenames:
            src = Path(filename)
            target.write_text(
                data=src.read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            result = subprocess.run(
                args=[
                    elm_path,
                    "make",
                    "src/Check.elm",
                    "--output=/dev/null",
                ],
                capture_output=True,
                text=True,
                check=False,
                cwd=tmpdir,
                env=env,
            )
            if result.returncode != 0:
                msg = f"{filename}: elm make failed\n"
                msg += result.stderr + result.stdout
                sys.stderr.write(msg)
                failed = True
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
