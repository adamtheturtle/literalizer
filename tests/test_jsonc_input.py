"""JSONC input accepts comments while keeping JSON syntax rules."""

import pytest

from literalizer import InputFormat, literalize
from literalizer.exceptions import JSONCParseError, JSONParseError
from literalizer.languages import Jsonc, Python


def test_jsonc_comments_and_string_slashes() -> None:
    """Both comment styles work without changing quoted content."""
    result = literalize(
        source=(
            "// heading\r\n"
            '{"url": "https://example.org/a/*b*/", /* detail\n'
            'continued */ "count": 2 // tail\n}'
        ),
        input_format=InputFormat.JSONC,
        language=Python(),
    )

    assert result.code == (
        '{\n    "url": "https://example.org/a/*b*/",\n    "count": 2,\n}'
    )


def test_jsonc_output_can_be_read_as_jsonc_input() -> None:
    """Rendered comments are accepted by the public input path."""
    output = literalize(
        source="# heading\ncount: 2\n",
        input_format=InputFormat.YAML,
        language=Jsonc(),
    )
    result = literalize(
        source=output.code,
        input_format=InputFormat.JSONC,
        language=Python(),
    )

    assert result.code == '{\n    "count": 2,\n}'


def test_jsonc_escaped_quote_keeps_slashes_inside_string() -> None:
    """An escaped quote does not turn later string content into a
    comment.
    """
    result = literalize(
        source='{"text": "a\\"//b"}',
        input_format=InputFormat.JSONC,
        language=Python(),
    )

    assert result.code == '{\n    "text": "a\\"//b",\n}'


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
