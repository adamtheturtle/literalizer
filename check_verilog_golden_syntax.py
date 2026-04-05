"""Check syntax of Verilog golden files.

Validates structure and balanced delimiters of the generated
SystemVerilog output without requiring a full compiler.  The Ubuntu
``iverilog`` package does not support ``typedef struct``, so this
script provides a lightweight alternative.
"""

import re
import sys
from pathlib import Path


def _strip_strings(text: str) -> str:
    """Replace string contents with empty strings to simplify parsing."""
    result: list[str] = []
    i = 0
    while i < len(text):
        char = text[i]
        if char != '"':
            result.append(char)
            i += 1
            continue
        result.append('"')
        i += 1
        while i < len(text) and text[i] != '"':
            if text[i] == "\\":
                i += 1  # skip next char
            i += 1
        if i < len(text):
            result.append('"')
            i += 1
        else:
            return ""  # unterminated string
    return "".join(result)


def _check_delimiters(text: str) -> list[str]:
    """Check balanced braces and string quotes."""
    stripped = _strip_strings(text=text)
    if not stripped:
        return ["unterminated string literal"]
    depth = 0
    for char in stripped:
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth < 0:
                return ["unmatched closing brace"]
    if depth != 0:
        return [f"unbalanced braces (depth {depth})"]
    return []


def _check_keywords(text: str) -> list[str]:
    """Check preamble types and keyword balance."""
    errors: list[str] = []
    if "typedef enum" in text and "_VTag" not in text:
        errors.append("typedef enum missing _VTag")
    if "typedef struct" in text and "_VVal" not in text:
        errors.append("typedef struct missing _VVal")

    module_count = len(re.findall(pattern=r"\bmodule\b", string=text))
    endmodule_count = len(re.findall(pattern=r"\bendmodule\b", string=text))
    if module_count != endmodule_count:
        errors.append(
            f"module/endmodule mismatch ({module_count} vs {endmodule_count})"
        )

    begin_count = len(re.findall(pattern=r"\bbegin\b", string=text))
    end_kw_count = len(re.findall(pattern=r"\bend\b", string=text))
    if begin_count != end_kw_count:
        errors.append(f"begin/end mismatch ({begin_count} vs {end_kw_count})")
    return errors


def main() -> None:
    """Check syntax of each given Verilog golden file."""
    for filename in sys.argv[1:]:
        path = Path(filename)
        text = path.read_text(encoding="utf-8")
        errors = _check_delimiters(text=text) + _check_keywords(text=text)
        if errors:
            for err in errors:
                sys.stderr.write(f"{filename}: {err}\n")
            sys.exit(1)


if __name__ == "__main__":
    main()
