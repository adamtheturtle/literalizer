"""YAML comments preserved through the public interface."""

from literalizer import InputFormat, literalize
from literalizer.languages import Python


def test_collection_closing_comment() -> None:
    """A closing collection comment survives without element metadata."""
    result = literalize(
        source="[1] # closing\n",
        input_format=InputFormat.YAML,
        language=Python(),
    )
    assert result.code == "(\n    1,\n    # closing\n)"


def test_scalar_inline_comment() -> None:
    """A scalar retains its inline comment without a preceding comment."""
    result = literalize(
        source="1 # inline\n",
        input_format=InputFormat.YAML,
        language=Python(),
    )
    assert result.code == "1  # inline"
