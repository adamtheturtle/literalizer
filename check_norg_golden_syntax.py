"""Check syntax of Norg golden files.

Validates that each file has a well-formed Norg structure (optional
``=name``/``=end`` macro wrapper) and that the embedded JSON payload
parses correctly after stripping ``% … %`` inline comments.
"""

import json
import re
import sys
from pathlib import Path


def _strip_norg_comments(text: str) -> str:
    """Remove ``% … %`` Norg inline comments from *text*.

    Comments may span content within a single line but do not cross
    line boundaries in the golden files produced by literalizer.
    """
    return re.sub(pattern=r"%[^%]*%", repl="", string=text)


def _check_file(path: Path) -> str | None:
    """Return an error message if *path* has a Norg structural error."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    if not lines:
        return "File is empty"

    # Determine whether the file uses a macro wrapper.
    if lines[0].startswith("=") and lines[0] != "=end":
        macro_name = lines[0]
        if lines[-1] != "=end":
            return (
                f"Macro {macro_name!r} opened but file does not"
                " end with '=end'"
            )
        json_text = "\n".join(lines[1:-1])
    else:
        json_text = text

    # Strip Norg comments before JSON validation.
    json_text = _strip_norg_comments(text=json_text)

    try:
        json.loads(json_text)
    except json.JSONDecodeError as exc:
        return f"Invalid JSON payload: {exc}"

    return None


def main() -> None:
    """Check syntax of each given Norg golden file."""
    for filename in sys.argv[1:]:
        src = Path(filename)
        error = _check_file(path=src)
        if error is not None:
            sys.stderr.write(f"{filename}: Norg syntax error: {error}\n")
            sys.exit(1)


if __name__ == "__main__":
    main()
