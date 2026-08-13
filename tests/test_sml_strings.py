"""Tests for Standard ML string literal formatting."""

from literalizer.languages import Sml


def test_sml_escapes_del_and_non_ascii_as_utf8_bytes() -> None:
    """The compiler receives legal decimal escapes with the original bytes."""
    assert Sml().format_string("del\x7fd café") == (
        '"del\\127d caf\\195\\169"'
    )
