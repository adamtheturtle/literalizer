"""Hex escapes must not consume following hexadecimal text."""

import pytest

from literalizer import InputFormat, Language, literalize
from literalizer.languages import Haskell, PureScript


@pytest.mark.parametrize(
    argnames=("language", "expected"),
    argvalues=[
        (Haskell(), r'HStr "a\x07\&face"'),
        (PureScript(), r'PStr "a\x07\x66\x61\x63\x65"'),
    ],
    ids=["haskell", "purescript"],
)
def test_control_escape_before_hex_run_is_unambiguous(
    language: Language,
    expected: str,
) -> None:
    """A BEL followed by hex digits remains five source characters."""
    result = literalize(
        source='"a\\u0007face"',
        input_format=InputFormat.JSON,
        language=language,
        variable_form=None,
    )

    assert result.code.splitlines()[-1] == expected
