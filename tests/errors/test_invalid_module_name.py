"""Validation tests for target-language module names."""

import pytest

from literalizer.exceptions import InvalidModuleNameError
from literalizer.languages import Erlang


def test_erlang_rejects_module_name_beyond_atom_limit() -> None:
    """An Erlang module name must fit in the VM's atom limit."""
    with pytest.raises(
        expected_exception=InvalidModuleNameError,
        match="Erlang cannot use module_name",
    ):
        Erlang(module_name="a" * 256)


def test_erlang_accepts_module_name_at_atom_limit() -> None:
    """The 255-character atom boundary remains valid."""
    Erlang(module_name="a" * 255)
