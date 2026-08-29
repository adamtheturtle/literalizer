"""Structured source positions on public errors.

The subject is the ``line``, ``column`` and ``path`` attributes an
error carries, not the message a rejection manifest keeps in a golden
file.
"""

import json

import pytest

from literalizer import InputFormat, literalize
from literalizer._language import Language
from literalizer.exceptions import (
    HeterogeneousScalarCollectionError,
    JSON5ParseError,
    JSONParseError,
    ParseError,
    TOMLParseError,
    UnrepresentableIntegerError,
    UnrepresentableStringError,
    YAMLParseError,
)
from literalizer.languages import Bash, PureScript, Rust


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


@pytest.mark.parametrize(
    argnames=("language", "value", "exception_type"),
    argvalues=[
        (PureScript(), 2**70, UnrepresentableIntegerError),
        (Bash(), "a\0b", UnrepresentableStringError),
    ],
)
def test_renderer_error_exposes_deep_input_path(
    language: Language,
    value: int | str,
    exception_type: type[UnrepresentableIntegerError]
    | type[UnrepresentableStringError],
) -> None:
    """A nested renderer failure identifies its deepest scalar value."""
    data = {"outer": [[value]]}

    with pytest.raises(expected_exception=exception_type) as caught:
        literalize(
            source=json.dumps(obj=data),
            input_format=InputFormat.JSON,
            language=language,
        )

    assert caught.value.path == ("outer", 0, 0)
