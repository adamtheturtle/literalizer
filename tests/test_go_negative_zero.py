"""Go negative-zero rendering tests."""

import pytest

from literalizer import InputFormat, literalize
from literalizer._language import Language
from literalizer.languages import Go


@pytest.mark.parametrize(
    argnames="language",
    argvalues=[
        Go(float_format=float_format) for float_format in Go.float_formats
    ],
)
def test_negative_zero_uses_copysign(language: Language) -> None:
    """Construct negative zero at runtime so Go retains its sign bit."""
    result = literalize(
        source="-0.0",
        input_format=InputFormat.JSON,
        language=language,
    )

    assert result.code == "math.Copysign(0, -1)"
    assert result.preamble == ("package main", 'import "math"')


@pytest.mark.parametrize(
    argnames="source",
    argvalues=["0.0", "1.5", "-1.5"],
)
def test_other_floats_do_not_import_math(source: str) -> None:
    """Avoid an unused Go import when no negative zero is rendered."""
    result = literalize(
        source=source,
        input_format=InputFormat.JSON,
        language=Go(),
    )

    assert result.code == source
    assert result.preamble == ("package main",)
