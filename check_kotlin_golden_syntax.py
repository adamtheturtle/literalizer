"""Check syntax of Kotlin golden files using ``kotlinc``."""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def main() -> None:
    """Check syntax of each given Kotlin golden file."""
    kotlinc_path = shutil.which(cmd="kotlinc") or "kotlinc"
    for filename in sys.argv[1:]:
        content = Path(filename).read_text(encoding="utf-8")
        wrapped = f"val x: Any? = {content}\n"

        with tempfile.NamedTemporaryFile(
            suffix=".kts",
            mode="w",
            encoding="utf-8",
            delete=True,
            delete_on_close=False,
        ) as tmp:
            tmp.write(wrapped)
            tmp.close()
            result = subprocess.run(
                args=[kotlinc_path, "-script", tmp.name],
                capture_output=True,
                text=True,
                check=False,
            )

        if result.returncode != 0:
            msg = f"{filename}: Kotlin syntax error\n{result.stderr}"
            sys.stderr.write(msg)
            sys.exit(1)


if __name__ == "__main__":
    main()
