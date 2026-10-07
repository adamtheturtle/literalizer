"""Error contracts for JSONC parsing and rendering."""

import pytest

from literalizer import InputFormat, literalize
from literalizer.exceptions import (
    JSONCParseError,
    JSONParseError,
    UnrepresentableSpecialFloatError,
)
from literalizer.languages import Jsonc, Python


@pytest.mark.parametrize(
    argnames="source",
    argvalues=[
        '{"a": 1,}',
        "{a: 1}",
        "{'a': 1}",
        '{"a": NaN}',
        '{"a": 1, "a": 2}',
        "1/",
        "1/2",
    ],
)
def test_jsonc_rejects_non_json_syntax(source: str) -> None:
    """Only comments extend the JSON grammar."""
    with pytest.raises(expected_exception=JSONCParseError):
        _ = literalize(
            source=source,
            input_format=InputFormat.JSONC,
            language=Python(),
        )


def test_jsonc_unterminated_comment_has_source_position() -> None:
    """An open block comment reports its start in the original text."""
    with pytest.raises(expected_exception=JSONCParseError) as caught:
        _ = literalize(
            source='{"a": 1,\n  /* missing',
            input_format=InputFormat.JSONC,
            language=Python(),
        )

    assert (caught.value.line, caught.value.column) == (2, 3)


def test_jsonc_syntax_error_keeps_source_position() -> None:
    """Replacing comments with spaces preserves JSON error columns."""
    with pytest.raises(expected_exception=JSONCParseError) as caught:
        _ = literalize(
            source='{"a": /* note */ ]}',
            input_format=InputFormat.JSONC,
            language=Python(),
        )

    assert (caught.value.line, caught.value.column) == (1, 18)


def test_json_remains_strict() -> None:
    """Selecting JSON does not silently accept JSONC comments."""
    with pytest.raises(expected_exception=JSONParseError):
        _ = literalize(
            source='{"a": 1 // note\n}',
            input_format=InputFormat.JSON,
            language=Python(),
        )


def test_jsonc_output_rejects_nonfinite_numbers() -> None:
    """Non-finite numeric tokens cannot leak into JSONC output."""
    with pytest.raises(expected_exception=UnrepresentableSpecialFloatError):
        _ = literalize(
            source="value: .nan",
            input_format=InputFormat.YAML,
            language=Jsonc(),
        )
