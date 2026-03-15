"""Check syntax of Java golden files using javac."""

import re
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

        # Every { in golden files is a collection open (array initializer).
        # Java requires "new Object[]" before bare array initializers used
        # as expressions.
        content = content.replace("{", "new Object[]{")

        # Top-level lists use [...] wrapping from literalize().
        # Replace with new Object[]{...} for valid Java.
        if content.startswith("["):
            content = "new Object[]{" + content[1:]
            # Replace last ] with }
            idx = content.rfind("]")
            content = content[:idx] + "}" + content[idx + 1 :]

        # Remove trailing commas before ) in method calls (Java forbids them).
        content = re.sub(pattern=r",(\s*\))", repl=r"\1", string=content)

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
