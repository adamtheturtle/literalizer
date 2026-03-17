"""Check syntax of occam-pi golden files using ``kroc``."""

import shutil
import subprocess
import sys
import tempfile


def main() -> None:
    """Check syntax of each given occam-pi golden file."""
    kroc_path = shutil.which(cmd="kroc") or "kroc"
    for filename in sys.argv[1:]:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = f"{tmpdir}/check"
            try:
                result = subprocess.run(
                    args=[kroc_path, "-o", output_path, filename],
                    capture_output=True,
                    text=True,
                    check=False,
                )
            except FileNotFoundError:
                # kroc not installed - skip check
                continue
        if result.returncode != 0:
            msg = f"{filename}: occam-pi syntax error\n{result.stderr}"
            sys.stderr.write(msg)
            sys.exit(1)


if __name__ == "__main__":
    main()
