"""Structural syntax check for Solidity golden files.

Solidity is statically typed, so bare literals (without explicit types)
cannot be compiled by ``solc``.  This script performs lightweight
structural validation instead: balanced brackets, balanced strings,
and proper semicolons.
"""

import sys
from pathlib import Path


def _scan_brackets(lines: list[str]) -> str | None:
    """Return an error if square brackets are unbalanced."""
    depth = 0
    for line_num, line in enumerate(iterable=lines, start=1):
        in_string = False
        i = 0
        while i < len(line):
            ch = line[i]
            if ch == "\\" and in_string:
                i += 2
                continue
            if ch == '"':
                in_string = not in_string
            elif not in_string and ch == "[":
                depth += 1
            elif not in_string and ch == "]":
                depth -= 1
                if depth < 0:
                    return f"Unmatched ']' at line {line_num}"
            i += 1

    if depth != 0:
        return f"Unbalanced '[': {depth} unclosed bracket(s)"
    return None


def _scan_braces(lines: list[str]) -> str | None:
    """Return an error if curly braces are unbalanced."""
    depth = 0
    for line_num, line in enumerate(iterable=lines, start=1):
        in_string = False
        i = 0
        while i < len(line):
            ch = line[i]
            if ch == "\\" and in_string:
                i += 2
                continue
            if ch == '"':
                in_string = not in_string
            elif not in_string and ch == "{":
                depth += 1
            elif not in_string and ch == "}":
                depth -= 1
                if depth < 0:
                    return f"Unmatched '}}' at line {line_num}"
            i += 1

    if depth != 0:
        return f"Unbalanced '{{': {depth} unclosed brace(s)"
    return None


def _check_strings(lines: list[str]) -> str | None:
    """Return an error if a string literal is unterminated."""
    for line_num, line in enumerate(iterable=lines, start=1):
        stripped = line.lstrip()
        if stripped.startswith(("//", "/*")):
            continue
        in_string = False
        i = 0
        while i < len(line):
            ch = line[i]
            if ch == "\\" and in_string:
                i += 2
                continue
            if ch == '"':
                in_string = not in_string
            i += 1
        if in_string:
            return f"Unterminated string at line {line_num}"

    return None


def _check_file(path: Path) -> str | None:
    """Return an error message if *path* has a structural error."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    error = _scan_brackets(lines=lines)
    if error is not None:
        return error

    error = _scan_braces(lines=lines)
    if error is not None:
        return error

    return _check_strings(lines=lines)


def main() -> None:
    """Check syntax of the given Solidity golden file."""
    filename = sys.argv[1]
    src = Path(filename)
    error = _check_file(path=src)
    if error is not None:
        sys.stderr.write(f"{filename}: Solidity syntax error: {error}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
