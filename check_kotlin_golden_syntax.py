"""Check syntax of Kotlin golden files using kotlinc.

Golden files use ``[`` / ``]`` for top-level lists (the generic wrap
format shared by all languages).  We replace these with ``listOf(`` /
``)`` to produce valid Kotlin before feeding the result to ``kotlinc``.
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def _transform(content: str) -> str:
    """Replace the generic outer ``[``/``]`` list wrap with
    ``listOf(``/``)``.
    """
    stripped = content.strip()
    if stripped.startswith("["):
        stripped = "listOf(" + stripped[1:]
        # The closing ``]`` is always the last non-whitespace character.
        idx = stripped.rfind("]")
        stripped = stripped[:idx] + ")" + stripped[idx + 1 :]
    # Empty collections need explicit type parameters for kotlinc.
    return stripped.replace("listOf()", "listOf<Any?>()").replace(
        "mapOf()", "mapOf<String, Any?>()"
    )


def main() -> None:
    """Check syntax of each given Kotlin golden file."""
    kotlinc_path = shutil.which(cmd="kotlinc") or "kotlinc"
    for filename in sys.argv[1:]:
        content = Path(filename).read_text(encoding="utf-8")
        transformed = _transform(content)
        wrapped = f"val x: Any? = {transformed}\n"

        with tempfile.NamedTemporaryFile(
            suffix=".kts",
            mode="w",
            encoding="utf-8",
            delete=True,
        ) as tmp:
            tmp.write(wrapped)
            tmp.flush()
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
