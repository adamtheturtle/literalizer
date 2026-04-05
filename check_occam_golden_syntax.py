"""Check syntax of an Occam-pi golden file."""

import sys
from pathlib import Path


def _strip_comment(line: str) -> str:
    """Strip an occam-pi inline comment (``--`` to end of line)."""
    in_string = False
    i = 0
    while i < len(line):
        ch = line[i]
        if ch == "\\" and in_string:
            i += 2
            continue
        if ch == '"':
            in_string = not in_string
        elif not in_string and line[i : i + 2] == "--":
            return line[:i].rstrip()
        i += 1
    return line


def _check_type_block(lines: list[str], term_index: int) -> str | None:
    """Validate the first top-level block is a well-formed MOBILE DATA
    TYPE definition.
    """
    first_block = lines[:term_index]
    code = [
        line
        for line in first_block
        if line.strip() and not line.strip().startswith("--")
    ]

    if not code:
        return "First top-level block is empty"

    if not code[0].startswith("MOBILE DATA TYPE "):
        return (
            "First top-level block should start with 'MOBILE DATA TYPE', "
            f"got: {code[0]!r}"
        )

    if " IS" not in code[0]:
        first = code[0]
        return f"MOBILE DATA TYPE declaration missing 'IS': {first!r}"

    if not any(line.strip() == "CASE" for line in code):
        return "MOBILE DATA TYPE definition missing 'CASE'"

    return None


def _check_proc(lines: list[str]) -> str | None:
    """Return an error if there is no PROC definition."""
    has_proc = any(
        line.startswith("PROC ") and "(" in line and ")" in line
        for line in lines
    )
    if not has_proc:
        return "No PROC definition found"
    return None


def _check_brackets(lines: list[str]) -> str | None:
    """Return an error if square brackets are unbalanced."""
    depth = 0
    for line_num, line in enumerate(iterable=lines, start=1):
        clean = _strip_comment(line=line)
        in_string = False
        i = 0
        while i < len(clean):
            ch = clean[i]
            if ch == "\\" and in_string:
                i += 2
                continue
            if ch == '"':
                in_string = not in_string
            elif not in_string:
                if ch == "[":
                    depth += 1
                elif ch == "]":
                    depth -= 1
                    if depth < 0:
                        return f"Unmatched ']' at line {line_num}"
            i += 1

    if depth != 0:
        return f"Unbalanced '[': {depth} unclosed bracket(s)"

    return None


def _check_file(path: Path) -> str | None:
    """Return an error message if *path* has an occam-pi structural
    error.
    """
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    # Locate top-level ':' terminators (lines that are exactly ":").
    # In occam-pi every top-level definition ends with a bare ':'.
    top_level_term_indices = [
        i for i, line in enumerate(iterable=lines) if line == ":"
    ]

    min_top_level_terminators = 2
    if len(top_level_term_indices) < min_top_level_terminators:
        count = len(top_level_term_indices)
        return (
            f"Expected at least {min_top_level_terminators} top-level ':' "
            f"terminators (type definition + PROC), found {count}"
        )

    error = _check_type_block(
        lines=lines, term_index=top_level_term_indices[0]
    )
    if error is not None:
        return error

    error = _check_proc(lines=lines)
    if error is not None:
        return error

    return _check_brackets(lines=lines)


def main() -> None:
    """Check syntax of the given Occam-pi golden file."""
    filename = sys.argv[1]
    src = Path(filename)
    error = _check_file(path=src)
    if error is not None:
        sys.stderr.write(f"{filename}: Occam-pi syntax error: {error}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
