"""Check syntax of a Solidity golden file using ``solc``.

The golden files are bare literals (no pragma / contract wrapper), so
this script wraps them in a minimal contract before compiling.

Files that contain features Solidity cannot represent (mapping/dict
literals, control characters in strings) are silently skipped.
"""

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# Patterns that indicate the file cannot be valid Solidity.
_DICT_LITERAL = re.compile(r"= \{")
_CONTROL_CHAR = re.compile(r"[\x00-\x08\x0e-\x1f]")


def main() -> None:
    """Check syntax of the given Solidity golden file."""
    filename = sys.argv[1]
    content = Path(filename).read_text(encoding="utf-8")

    if _DICT_LITERAL.search(string=content):
        return

    if _CONTROL_CHAR.search(string=content):
        return

    wrapped = (
        "// SPDX-License-Identifier: MIT\n"
        "pragma solidity >=0.8.0;\n"
        "\n"
        "contract Generated {\n"
        "    function run() public pure {\n"
        f"{content}\n"
        "    }\n"
        "}\n"
    )

    solc_path: str = shutil.which(cmd="solc") or "solc"
    with tempfile.TemporaryDirectory() as tmpdir:
        sol_path = Path(tmpdir) / "check.sol"
        sol_path.write_text(data=wrapped, encoding="utf-8")
        result = subprocess.run(
            args=[solc_path, "--no-color", sol_path.as_posix()],
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
