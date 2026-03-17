"""Check syntax of MATLAB golden files using ``octave``."""

import shutil
import subprocess
import sys


def main() -> None:
    """Check syntax of each given MATLAB golden file using Octave."""
    octave_path = shutil.which(cmd="octave") or "octave"
    for filename in sys.argv[1:]:
        try:
            result = subprocess.run(
                args=[octave_path, "--norc", "--no-gui", filename],
                capture_output=True,
                text=True,
                check=False,
            )
        except FileNotFoundError:
            # octave not installed - skip check
            continue
        if result.returncode != 0:
            msg = f"{filename}: MATLAB syntax error\n{result.stderr}"
            sys.stderr.write(msg)
            sys.exit(1)


if __name__ == "__main__":
    main()
