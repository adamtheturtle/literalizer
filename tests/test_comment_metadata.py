"""Comment metadata shapes supported by the parser boundary."""

from dataclasses import dataclass

from ruamel.yaml.tokens import CommentToken

from literalizer import InputFormat, literalize
from literalizer._comments import literalize_yaml_scalar
from literalizer.languages import Python


@dataclass
class ScannerToken:
    """A scanner token whose comment association has only an inline
    slot.
    """

    comment: list[CommentToken | list[CommentToken] | None] | None


def test_collection_closing_comment() -> None:
    """A closing collection comment survives without element metadata."""
    result = literalize(
        source="[1] # closing\n",
        input_format=InputFormat.YAML,
        language=Python(),
    )
    assert "# closing" in result.code


def test_scalar_comment_without_before_slot() -> None:
    """A single-slot comment association retains its inline comment."""
    token = ScannerToken(comment=[CommentToken(value="# inline\n", column=2)])
    result = literalize_yaml_scalar(
        tokens=[token],
        base="1",
        comment_prefix="#",
        comment_suffix="",
        line_prefix="",
        supports_scalar_before_comments=True,
        supports_scalar_inline_comments=True,
    )
    assert result.result == "1  # inline"
    assert len(result.pending_before) == 0
