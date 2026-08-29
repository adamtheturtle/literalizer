"""Where a once-bound declaration modifier still belongs.

The rejections are declared in ``tests/errors/rejections`` and run by
``test_rejections.py``.  What is left here is the acceptance side --
the modifier that names a storage class rather than a binding, and the
single form these modifiers were made for.
"""

import enum

import pytest

from literalizer import (
    BothVariableForms,
    InputFormat,
    Language,
    NewVariable,
    literalize,
)
from literalizer.languages import Cpp, CSharp, Java


@pytest.mark.parametrize(
    argnames=("language", "modifier"),
    argvalues=[
        pytest.param(Cpp(), Cpp.modifiers.STATIC, id="cpp"),
        pytest.param(Java(), Java.modifiers.STATIC, id="java"),
        pytest.param(CSharp(), CSharp.modifiers.STATIC, id="csharp"),
    ],
)
def test_rebindable_modifier_accepted(
    language: Language,
    modifier: enum.Enum,
) -> None:
    """``static`` names a storage class, not a once-only binding."""
    result = literalize(
        source="[1, 2]",
        input_format=InputFormat.JSON,
        language=language,
        variable_form=BothVariableForms(
            name="my_val",
            modifiers=frozenset({modifier}),
        ),
        wrap_in_file=True,
    )
    assert "static" in result.code


@pytest.mark.parametrize(
    argnames=("language", "modifier"),
    argvalues=[
        pytest.param(Cpp(), Cpp.modifiers.CONST, id="cpp-const"),
        pytest.param(Java(), Java.modifiers.FINAL, id="java-final"),
    ],
)
def test_immutable_modifier_accepted_for_one_form(
    language: Language,
    modifier: enum.Enum,
) -> None:
    """A single declaration is where such a modifier belongs."""
    result = literalize(
        source="[1, 2]",
        input_format=InputFormat.JSON,
        language=language,
        variable_form=NewVariable(
            name="my_val",
            modifiers=frozenset({modifier}),
        ),
        wrap_in_file=True,
    )
    assert modifier.value in result.code
