"""Validation for Erlang module names."""

import pytest

from literalizer.exceptions import InvalidModuleNameError
from literalizer.languages import Erlang


def test_erlang_rejects_variable_as_module_name() -> None:
    """A capitalized Erlang word is a variable, not an atom."""
    with pytest.raises(
        expected_exception=InvalidModuleNameError,
        match="cannot use module_name",
    ):
        Erlang(module_name="Module")
