"""Check syntax of F# golden files using ``dotnet fsi``."""

import shutil
import subprocess
import sys


def main() -> None:
    """Check syntax of each given F# golden file."""
    dotnet_path: str = shutil.which(cmd="dotnet") or "dotnet"
    for filename in sys.argv[1:]:
        result = subprocess.run(
            args=[dotnet_path, "fsi", "--nologo", "--exec", filename],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            msg = (
                f"{filename}: F# syntax error\n{result.stderr}{result.stdout}"
            )
            sys.stderr.write(msg)
            sys.exit(1)


if __name__ == "__main__":
    main()
