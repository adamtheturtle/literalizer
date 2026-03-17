"""Check syntax of F# golden files using ``dotnet fsi``."""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

_DOTNET_ENV = {
    "DOTNET_SKIP_FIRST_TIME_EXPERIENCE": "1",
    "DOTNET_NOLOGO": "1",
}


def main() -> None:
    """Check syntax of each given F# golden file."""
    dotnet_path: str = shutil.which(cmd="dotnet") or "dotnet"
    for filename in sys.argv[1:]:
        with tempfile.TemporaryDirectory() as tmpdir:
            dotnet_tmp = Path(tmpdir) / "tmp"
            dotnet_tmp.mkdir()
            env = os.environ.copy()
            env.update(
                {
                    "TMPDIR": dotnet_tmp.as_posix(),
                    "HOME": dotnet_tmp.as_posix(),
                    **_DOTNET_ENV,
                }
            )
            result = subprocess.run(
                args=[dotnet_path, "fsi", "--nologo", "--exec", filename],
                capture_output=True,
                text=True,
                check=False,
                env=env,
            )
        if result.returncode != 0:
            msg = (
                f"{filename}: F# syntax error\n{result.stderr}{result.stdout}"
            )
            sys.stderr.write(msg)
            sys.exit(1)


if __name__ == "__main__":
    main()
