"""Check syntax of Java golden files using javac."""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def main() -> None:
    """Check syntax of each given Java golden file."""
    javac_path = shutil.which(cmd="javac") or "javac"
    for filename in sys.argv[1:]:
        content = Path(filename).read_text(encoding="utf-8").strip()

        wrapped = (
            "import java.util.Map;\n"
            "public class Check {\n"
            f"    Object x = {content};\n"
            "}\n"
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            java_file_path = f"{tmpdir}/Check.java"
            Path(java_file_path).write_text(data=wrapped, encoding="utf-8")
            result = subprocess.run(
                args=[javac_path, java_file_path],
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
