"""Focused tests for MATLAB formatting helpers."""

from literalizer.languages.matlab import _matlab_char_key


def test_empty_matlab_char_key() -> None:
    """Render an empty ``containers.Map`` key as an empty char vector."""
    assert _matlab_char_key("") == "''"
