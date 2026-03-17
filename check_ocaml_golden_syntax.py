"""Check syntax of OCaml golden files using ``ocamlopt``."""

import shutil
import subprocess
import sys
import tempfile


def main() -> None:
    """Check syntax of each given OCaml golden file."""
    ocamlopt_path = shutil.which(cmd="ocamlopt") or "ocamlopt"
    for filename in sys.argv[1:]:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = f"{tmpdir}/check.o"
            try:
                result = subprocess.run(
                    args=[ocamlopt_path, "-c", "-o", output_path, filename],
                    capture_output=True,
                    text=True,
                    check=False,
                )
            except FileNotFoundError:
                # ocamlopt not installed - skip check
                continue
        if result.returncode != 0:
            msg = f"{filename}: OCaml syntax error\n{result.stderr}"
            sys.stderr.write(msg)
            sys.exit(1)


if __name__ == "__main__":
    main()
