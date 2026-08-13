"""Groovy negative-zero rendering tests."""

import pytest

from literalizer import InputFormat, literalize
from literalizer._language import Language
from literalizer.languages import Groovy


@pytest.mark.parametrize(
    argnames="language",
    argvalues=[
        Groovy(float_format=float_format)
        for float_format in Groovy.float_formats
    ],
)
def test_negative_zero_uses_double_suffix(language: Language) -> None:
    """Keep the sign bit by forcing the ``Double`` literal type in
    Groovy.
    """
    result = literalize(
        source="-0.0",
        input_format=InputFormat.JSON,
        language=language,
    )

    assert result.code.endswith("d")


@pytest.mark.parametrize(
    argnames="source",
    argvalues=["0.0", "1.5", "-1.5"],
)
def test_other_floats_keep_existing_rendering(source: str) -> None:
    """Avoid changing ordinary Groovy float literal spelling."""
    result = literalize(
        source=source,
        input_format=InputFormat.JSON,
        language=Groovy(),
    )

    assert result.code == source
