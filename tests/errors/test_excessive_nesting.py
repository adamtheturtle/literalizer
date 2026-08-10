"""Errors for backends that stringify nested collections."""

import pytest

from literalizer import InputFormat, Language, literalize
from literalizer.exceptions import ExcessiveNestingError
from literalizer.languages import Bash, SystemVerilog


def _nested_array_source(depth: int) -> str:
    """Return a JSON scalar nested inside *depth* arrays."""
    return "[" * depth + "1" + "]" * depth


@pytest.mark.parametrize(
    argnames="language", argvalues=[Bash(), SystemVerilog()]
)
def test_stringifying_backends_accept_depth_twelve(
    language: Language,
) -> None:
    """The documented supported boundary remains renderable."""
    result = literalize(
        source=_nested_array_source(depth=12),
        input_format=InputFormat.JSON,
        language=language,
    )

    assert result.code


@pytest.mark.parametrize(
    argnames="language", argvalues=[Bash(), SystemVerilog()]
)
def test_stringifying_backends_reject_depth_thirteen(
    language: Language,
) -> None:
    """The first unsafe depth raises before exponential rendering."""
    with pytest.raises(
        expected_exception=ExcessiveNestingError,
        match=(
            r"supports collection nesting only through depth 12; "
            r"received depth 13"
        ),
    ):
        literalize(
            source=_nested_array_source(depth=13),
            input_format=InputFormat.JSON,
            language=language,
        )
