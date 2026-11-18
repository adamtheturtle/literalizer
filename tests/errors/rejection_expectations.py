"""Read the rejection suite's authored expectations."""

import re
import tomllib
from pathlib import Path

from beartype import beartype
from pydantic import TypeAdapter

type ExpectedMessage = str | dict[str, str]
type ExpectedMessages = dict[str, dict[str, ExpectedMessage]]

_EXPECTED_MESSAGES = TypeAdapter[ExpectedMessages](type=ExpectedMessages)


@beartype
def load_expected_messages(*, golden_path: Path) -> ExpectedMessages:
    """Read messages and validate each optional Python-version map."""
    if not golden_path.exists():
        return {}
    expected = _EXPECTED_MESSAGES.validate_python(
        tomllib.loads(golden_path.read_text(encoding="utf-8")), strict=True
    )
    for cases in expected.values():
        for message in cases.values():
            if isinstance(message, dict):
                if "default" not in message:
                    msg = "a versioned message requires a default"
                    raise ValueError(msg)
                for version in message:
                    if (
                        version != "default"
                        and re.fullmatch(
                            pattern=r"[0-9]+\.[0-9]+", string=version
                        )
                        is None
                    ):
                        msg = f"invalid Python version key: {version!r}"
                        raise ValueError(msg)
    return expected
