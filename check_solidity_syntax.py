"""Check syntax of a Solidity golden file using ``solc``.

Solidity cannot represent every data structure that the library
outputs (e.g. heterogeneous arrays, mapping literals, empty inline
arrays).  This script runs ``solc`` and treats known-limitation
errors as a silent skip rather than a failure, so that files which
*can* compile are still verified.
"""

import re
import shutil
import subprocess
import sys
from pathlib import Path

# Control characters that solc rejects inside string literals.
_CONTROL_CHAR = re.compile(pattern=r"[\x00-\x08\x0e-\x1f]")

# Error messages from solc that are expected for data structures
# Solidity cannot represent.  These are treated as a skip.
_KNOWN_LIMITATION_PATTERNS: tuple[str, ...] = (
    # Dict/mapping literals — no map literal syntax.
    "Expected primary expression",
    # Dict keys — string keys are not valid Solidity identifiers.
    "Expected identifier but got",
    # Heterogeneous arrays — all elements must share a type.
    "Unable to deduce common type for array elements",
    # Empty inline arrays — solc cannot infer element type.
    "Expected expression (inline array elements cannot be omitted)",
    # Negative literals in unsigned context.
    "not implicitly convertible to expected type",
)


def main() -> None:
    """Check syntax of the given Solidity golden file."""
    filename = sys.argv[1]
    content = Path(filename).read_text(encoding="utf-8")

    # Skip files with control characters before invoking solc.
    if _CONTROL_CHAR.search(string=content):
        return

    solc_path: str = shutil.which(cmd="solc") or "solc"
    result = subprocess.run(
        args=[solc_path, "--no-color", filename],
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode == 0:
        return

    combined = result.stderr + result.stdout
    for pattern in _KNOWN_LIMITATION_PATTERNS:
        if pattern in combined:
            return

    sys.stderr.write(f"{filename}: solc failed\n{combined}")
    sys.exit(1)


if __name__ == "__main__":
    main()
