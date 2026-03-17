"""Check syntax of Elixir golden files using elixirc."""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def main() -> None:
    """Check syntax of each given Elixir golden file."""
    elixirc_path = shutil.which(cmd="elixirc")
    if elixirc_path is None:
        return
    for filename in sys.argv[1:]:
        content = Path(filename).read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as tmpdir:
            ex_path = Path(tmpdir) / "check.ex"
            ex_path.write_text(data=content, encoding="utf-8")
            result = subprocess.run(
                args=[elixirc_path, "check.ex"],
                capture_output=True,
                text=True,
                check=False,
                cwd=tmpdir,
            )
        if result.returncode != 0:
            msg = f"{filename}: Elixir syntax error\n{result.stderr}"
            sys.stderr.write(msg)
            sys.exit(1)


if __name__ == "__main__":
    main()
