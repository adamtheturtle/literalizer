"""Error contracts for JSONC parsing and rendering."""

import pytest

from literalizer import InputFormat, literalize
from literalizer.exceptions import (
    JSONCParseError,
)
from literalizer.languages import Python


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
    """Parser metadata preserves original JSONC error columns."""
    with pytest.raises(expected_exception=JSONCParseError) as caught:
        _ = literalize(
            source='{"a": /* note */ ]}',
            input_format=InputFormat.JSONC,
            language=Python(),
        )

    assert (caught.value.line, caught.value.column) == (1, 18)
