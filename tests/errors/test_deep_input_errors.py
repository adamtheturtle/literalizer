"""Typed errors for inputs that exceed parser recursion limits."""

from typing import Never

import pytest

from literalizer import InputFormat, _parsing, literalize
from literalizer.exceptions import (
    JSON5ParseError,
    JSONParseError,
    ParseError,
    TOMLParseError,
    YAMLParseError,
)
from literalizer.languages import Python


@pytest.mark.parametrize(
    argnames=("input_format", "expected_exception", "depth"),
    argvalues=[
        (InputFormat.JSON, JSONParseError, 5_000),
        (InputFormat.JSON5, JSON5ParseError, 5_000),
        (InputFormat.YAML, YAMLParseError, 500),
    ],
)
def test_deep_input_raises_typed_parse_error(
    input_format: InputFormat,
    expected_exception: type[ParseError],
    depth: int,
) -> None:
    """Parser recursion failures do not escape the public API raw."""
    source = "[" * depth + "]" * depth

    with pytest.raises(
        expected_exception=expected_exception,
        match="supported nesting depth",
    ):
        literalize(
            source=source,
            input_format=input_format,
            language=Python(),
        )


def test_render_recursion_raises_typed_parse_error() -> None:
    """Recursion after successful parsing is typed too."""
    source = "[" * 200 + "]" * 200

    with pytest.raises(
        expected_exception=JSONParseError,
        match="supported nesting depth",
    ):
        literalize(
            source=source,
            input_format=InputFormat.JSON,
            language=Python(),
        )


def test_toml_recursion_raises_typed_parse_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """TOML parser recursion failures use the TOML-specific error."""

    def raise_recursion(*, source: str, input_format: InputFormat) -> Never:
        """Stand in for a parser that exhausts the Python stack."""
        del source, input_format
        raise RecursionError

    monkeypatch.setattr(
        target=_parsing,
        name="_parse_by_format",
        value=raise_recursion,
    )

    with pytest.raises(
        expected_exception=TOMLParseError,
        match="supported nesting depth",
    ):
        _parsing.parse_input(source="value = 1", input_format=InputFormat.TOML)
