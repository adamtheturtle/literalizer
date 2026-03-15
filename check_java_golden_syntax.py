"""Check syntax of Java golden files using javac."""

import shutil
import subprocess
import sys
import tempfile


def main() -> None:
    """Check syntax of each given Java golden file."""
    javac_path = shutil.which(cmd="javac") or "javac"
    for filename in sys.argv[1:]:
        with tempfile.TemporaryDirectory() as tmpdir:
            result = subprocess.run(
                args=[javac_path, "-d", tmpdir, filename],
                capture_output=True,
                text=True,
                check=False,
            )
        if result.returncode != 0:
            msg = f"{filename}: Java syntax error\n{result.stderr}"
            sys.stderr.write(msg)
            sys.exit(1)


if __name__ == "__main__":
    main()
