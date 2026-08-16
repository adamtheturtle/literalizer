"""Module-name validation errors."""

from collections.abc import Callable

import pytest

from literalizer.exceptions import InvalidModuleNameError
from literalizer.languages import (
    Ada,
    C,
    Cpp,
    Crystal,
    D,
    Fortran,
    FSharp,
    Haskell,
    Haxe,
    ObjectiveC,
    Occam,
    Scala,
    SystemVerilog,
)


@pytest.mark.parametrize(
    argnames=("language_cls", "module_name"),
    argvalues=[
        (Ada, "begin"),
        (C, "if"),
        (Cpp, "class"),
        (Crystal, "class"),
        (D, "class"),
        (FSharp, "module"),
        (Fortran, "module"),
        (Haxe, "class"),
        (ObjectiveC, "if"),
        (Occam, "IF"),
        (Scala, "class"),
        (SystemVerilog, "module"),
    ],
)
def test_reserved_module_name_raises(
    language_cls: Callable[..., object],
    module_name: str,
) -> None:
    """A wrapper declaration cannot use a target-language keyword."""
    with pytest.raises(expected_exception=InvalidModuleNameError):
        language_cls(module_name=module_name)


def test_haskell_lowercase_module_name_raises() -> None:
    """Haskell module components must begin with an uppercase letter."""
    with pytest.raises(expected_exception=InvalidModuleNameError):
        Haskell(module_name="lower")
