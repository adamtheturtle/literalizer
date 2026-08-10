"""Tests for Crystal tuple token separation."""

from literalizer import InputFormat, literalize
from literalizer.languages import Crystal


def test_nested_tuple_openers_do_not_form_macro_tokens() -> None:
    """Nested Crystal tuples separate each adjacent ``{`` opener."""
    result = literalize(
        source='{"deep": [[[[1]]]]}',
        input_format=InputFormat.JSON,
        language=Crystal(sequence_format=Crystal.sequence_formats.TUPLE),
    )

    assert "{{" not in result.code
    assert '"deep" => { { { {1}}}}' in result.code
