"""Check syntax of TypeScript golden files using node."""

import shutil
import subprocess
import sys
from pathlib import Path


def main() -> None:
    """Check syntax of each given TypeScript file."""
    node_path = shutil.which(cmd="node") or "node"
    for filename in sys.argv[1:]:
        content = Path(filename).read_text(encoding="utf-8")
        # Wrap in void(...) to allow top-level object and array literals.
        # Without wrapping, `{ "key": value }` is parsed as a block statement,
        # causing a SyntaxError.
        wrapped = f"void (\n{content}\n)"
        result = subprocess.run(
            args=[node_path, "--check", "--input-type=commonjs"],
            input=wrapped,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            msg = f"{filename}: TypeScript syntax error\n{result.stderr}"
            sys.stderr.write(msg)
            sys.exit(1)


if __name__ == "__main__":
    main()
