"""Check syntax of Go golden files using gofmt."""

import shutil
import subprocess
import sys
from pathlib import Path


def main() -> None:
    """Check syntax of each given Go golden file."""
    gofmt_path = shutil.which(cmd="gofmt") or "gofmt"
    for filename in sys.argv[1:]:
        content = Path(filename).read_text(encoding="utf-8").strip()
        # Wrap in a package-level variable declaration to make valid Go.
        # gofmt accepts elided-type composite literals inside a typed
        # outer literal, so nested {…} elements parse without error.
        if content.startswith("map[string]any{"):
            # Already a typed composite literal — use it directly.
            wrapped = f"package main\n\nvar _ = {content}\n"
        else:
            inner = content[1:-1]
            if content.startswith("{"):
                # Bare dict literal — wrap with an outer typed map.
                wrapped = (
                    f"package main\n\nvar _ = map[string]interface{{}}{{\n"
                    f"{inner}\n}}\n"
                )
            else:
                wrapped = (
                    f"package main\n\nvar _ = []interface{{}}{{\n{inner}\n}}\n"
                )
        result = subprocess.run(
            args=[gofmt_path, "-e"],
            input=wrapped,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            msg = f"{filename}: Go syntax error\n{result.stderr}"
            sys.stderr.write(msg)
            sys.exit(1)


if __name__ == "__main__":
    main()
