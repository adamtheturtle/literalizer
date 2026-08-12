"""Structured source positions on public errors."""

import json

import pytest

from literalizer import InputFormat, literalize
from literalizer.exceptions import (
    HeterogeneousScalarCollectionError,
    JSON5ParseError,
    JSONParseError,
    ParseError,
    TOMLParseError,
    YAMLParseError,
)
from literalizer.languages import Rust


@pytest.mark.parametrize(
    argnames=("input_format", "source", "exception_type", "position"),
    argvalues=[
        (InputFormat.JSON, '{\n "a": ]\n}', JSONParseError, (2, 7)),
        (InputFormat.JSON5, "{\n a: ]\n}", JSON5ParseError, (2, 5)),
        (InputFormat.YAML, "a:\n  - [x\n", YAMLParseError, (3, 1)),
        (InputFormat.TOML, "a = ?", TOMLParseError, (1, 5)),
    ],
)
def test_parse_errors_expose_parser_position(
    input_format: InputFormat,
    source: str,
    exception_type: type[ParseError],
    position: tuple[int, int],
) -> None:
    """Malformed input exposes one-based line and column attributes."""
    with pytest.raises(expected_exception=exception_type) as caught:
        literalize(
            source=source,
            input_format=input_format,
            language=Rust(),
        )

    assert (caught.value.line, caught.value.column) == position


def test_collection_error_exposes_deep_input_path() -> None:
    """A nested shape error identifies its precise input collection."""
    data = {
        "users": [
            {"name": "a", "tags": ["x", "y"]},
            {"name": "b", "tags": [1, "z"]},
        ],
    }

    with pytest.raises(
        expected_exception=HeterogeneousScalarCollectionError
    ) as caught:
        literalize(
            source=json.dumps(obj=data),
            input_format=InputFormat.JSON,
            language=Rust(),
        )

    assert caught.value.path == ("users", 1, "tags")
