"""Validation for Erlang module names."""

import pytest

from literalizer.languages import Erlang


def test_erlang_rejects_variable_as_module_name() -> None:
    """A capitalized Erlang word is a variable, not an atom."""
    with pytest.raises(
        expected_exception=ValueError,
        match="Erlang module_name must be an unquoted atom",
    ):
        Erlang(module_name="Module")
