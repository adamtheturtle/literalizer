"""Check syntax of Haskell golden files using ghc."""

import shutil
import subprocess
import sys
import tempfile


def main() -> None:
    """Check syntax of each given Haskell golden file."""
    ghc_path = shutil.which(cmd="ghc") or "ghc"
    for filename in sys.argv[1:]:
        with tempfile.TemporaryDirectory() as tmpdir:
            result = subprocess.run(
                args=[ghc_path, "-fno-code", "-outputdir", tmpdir, filename],
                capture_output=True,
                text=True,
                check=False,
            )
        if result.returncode != 0:
            msg = f"{filename}: Haskell syntax error\n{result.stderr}"
            sys.stderr.write(msg)
            sys.exit(1)


if __name__ == "__main__":
    main()
