"""Check syntax of Erlang golden files using erlc."""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def main() -> None:
    """Check syntax of each given Erlang golden file."""
    erlc_path = shutil.which(cmd="erlc")
    if erlc_path is None:
        return
    for filename in sys.argv[1:]:
        content = Path(filename).read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as tmpdir:
            erl_path = Path(tmpdir) / "check.erl"
            erl_path.write_text(data=content, encoding="utf-8")
            result = subprocess.run(
                args=[erlc_path, "check.erl"],
                capture_output=True,
                text=True,
                check=False,
                cwd=tmpdir,
            )
        if result.returncode != 0:
            msg = (
                f"{filename}: Erlang syntax error\n"
                f"{result.stderr}{result.stdout}"
            )
            sys.stderr.write(msg)
            sys.exit(1)


if __name__ == "__main__":
    main()
