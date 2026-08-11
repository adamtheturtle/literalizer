"""Tests for Java rendering helpers."""

# pylint: disable=protected-access,wrong-spelling-in-comment
# ruff: noqa: SLF001

from literalizer.languages import java as java_module


def test_java_split_trailing_line_comments() -> None:
    """Split trailing comments from the Java expression they annotate."""
    result = java_module._java_split_trailing_line_comments(  # pyright: ignore[reportPrivateUsage]
        value="value\n// trailing",
    )

    assert result.code == "value"
    assert result.trailing == "\n// trailing"
