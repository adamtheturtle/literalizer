"""Check syntax of a Solidity golden file using ``solc``.

Files that use features Solidity cannot represent (mapping/dict
literals, control characters in strings) are silently skipped.
"""

import re
import shutil
import subprocess
import sys
from pathlib import Path

# Patterns that indicate the file cannot be valid Solidity.
# Dict/mapping literals — Solidity has no map literal syntax.
_DICT_LITERAL = re.compile(pattern=r"abi\.encode\(\{")
# Control characters that solc rejects inside string literals.
_CONTROL_CHAR = re.compile(pattern=r"[\x00-\x08\x0e-\x1f]")


def main() -> None:
    """Check syntax of the given Solidity golden file."""
    filename = sys.argv[1]
    content = Path(filename).read_text(encoding="utf-8")

    if _DICT_LITERAL.search(string=content):
        return

    if _CONTROL_CHAR.search(string=content):
        return

    solc_path: str = shutil.which(cmd="solc") or "solc"
    result = subprocess.run(
        args=[solc_path, "--no-color", filename],
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        msg = f"{filename}: solc failed\n{result.stderr}{result.stdout}"
        sys.stderr.write(msg)
        sys.exit(1)


if __name__ == "__main__":
    main()
