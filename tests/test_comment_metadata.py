"""YAML comments preserved through the public interface."""

from literalizer import InputFormat, literalize
from literalizer.languages import Python


def test_scalar_inline_comment() -> None:
    """A scalar retains its inline comment without a preceding comment."""
    result = literalize(
        source="1 # inline\n",
        input_format=InputFormat.YAML,
        language=Python(),
    )
    assert result.code == "1  # inline"
