"""Tests for intentionally incomplete literal fragments."""

from literalizer import InputFormat, literalize
from literalizer.languages import Python


def test_binary_without_sequence_delimiters() -> None:
    """YAML binary renders when the enclosing sequence is omitted."""
    result = literalize(
        source="- !!binary SGVsbG8=\n",
        input_format=InputFormat.YAML,
        language=Python(),
        pre_indent_level=0,
        include_delimiters=False,
        variable_form=None,
    )
    assert result.code == '"48656c6c6f",'
