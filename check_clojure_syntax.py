"""Check syntax of Clojure golden files using ``clj-kondo``."""

import shutil
import subprocess
import sys


def main() -> None:
    """Check syntax of each given Clojure golden file."""
    clj_kondo_path = shutil.which(cmd="clj-kondo")
    if clj_kondo_path is None:
        return
    result = subprocess.run(
        args=[clj_kondo_path, "--lint", *sys.argv[1:]],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        sys.stderr.write(result.stdout)
        sys.stderr.write(result.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
