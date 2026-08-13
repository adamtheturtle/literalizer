"""PHP integer literals must remain integer-typed at runtime."""

import pytest

from literalizer._formatters.format_integers import I64_MAX, I64_MIN
from literalizer.exceptions import UnrepresentableIntegerError
from literalizer.languages import Php


@pytest.mark.parametrize(
    argnames="value",
    argvalues=[I64_MIN - 1, I64_MAX + 1],
)
@pytest.mark.parametrize(
    argnames="integer_format",
    argvalues=list(Php.IntegerFormats),
)
def test_php_rejects_integers_outside_runtime_range(
    value: int,
    integer_format: Php.IntegerFormats,
) -> None:
    """Every PHP integer spelling rejects values parsed as floats."""
    language = Php(integer_format=integer_format)
    with pytest.raises(expected_exception=UnrepresentableIntegerError):
        language.format_integer(value)


@pytest.mark.parametrize(
    argnames="value",
    argvalues=[I64_MIN, I64_MAX],
)
def test_php_accepts_signed_64_bit_boundaries(value: int) -> None:
    """The platform integer boundaries remain representable."""
    assert Php().format_integer(value)
