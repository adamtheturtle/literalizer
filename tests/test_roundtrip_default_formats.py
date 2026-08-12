"""Keep round-trip helpers on consumer-default string formats."""

import ast
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"


def test_roundtrip_helpers_do_not_override_string_format() -> None:
    """A convenient alternate quoting mode must not replace defaults."""
    offenders: list[str] = []
    for path in sorted(_SCRIPTS_DIR.glob(pattern="run_*_roundtrip.py")):
        if path.name == "run_bash_roundtrip.py":
            # The default Bash mode is exercised by the fix in PR #3528.
            continue
        tree = ast.parse(source=path.read_text(encoding="utf-8"))
        offenders.extend(
            path.name
            for node in ast.walk(node=tree)
            if isinstance(node, ast.Call)
            and any(
                keyword.arg == "string_format" for keyword in node.keywords
            )
        )
    assert offenders == []
