"""Deep inputs retain their format's error without replacing rendering."""

import pytest

from literalizer import InputFormat, literalize
from literalizer.exceptions import (
    JSON5ParseError,
    JSONCParseError,
    JSONParseError,
    ParseError,
    YAMLParseError,
)
from literalizer.languages import Python


@pytest.mark.parametrize(
    argnames=("input_format", "error"),
    argvalues=[
        pytest.param(InputFormat.JSON, JSONParseError, id="json"),
        pytest.param(InputFormat.JSONC, JSONCParseError, id="jsonc"),
        pytest.param(InputFormat.JSON5, JSON5ParseError, id="json5"),
        pytest.param(InputFormat.YAML, YAMLParseError, id="yaml"),
    ],
)
def test_rendering_recursion_has_a_typed_error(
    input_format: InputFormat, error: type[ParseError]
) -> None:
    """Bounded nested values exhaust rendering and keep a typed cause."""
    source = "[" * 180 + "0" + "]" * 180
    with pytest.raises(
        expected_exception=error,
        match="input exceeds the supported nesting depth",
    ) as caught:
        _ = literalize(
            source=source, input_format=input_format, language=Python()
        )
    assert isinstance(caught.value.__cause__, RecursionError)
