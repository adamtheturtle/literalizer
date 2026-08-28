"""Errors for a once-bound declaration the assignment would rebind.

``BothVariableForms`` writes a declaration and then an assignment to the
same name.  A modifier that binds the name once makes the second half
impossible, which no compiler lets pass.  The rejection manifests cannot
express ``variable_form = "both"``, so these stay ordinary tests.
"""

import enum
import re

import pytest

from literalizer import (
    BothVariableForms,
    InputFormat,
    Language,
    NewVariable,
    literalize,
)
from literalizer.exceptions import ImmutableVariableModifierError
from literalizer.languages import Cpp, CSharp, Java


@pytest.mark.parametrize(
    argnames=("language", "modifier", "spelling"),
    argvalues=[
        pytest.param(
            Cpp(),
            Cpp.modifiers.CONST,
            "_CppModifiers.CONST",
            id="cpp-const",
        ),
        pytest.param(
            Java(),
            Java.modifiers.FINAL,
            "_JavaModifiers.FINAL",
            id="java-final",
        ),
        pytest.param(
            CSharp(),
            CSharp.modifiers.READONLY,
            "_CSharpModifiers.READONLY",
            id="csharp-readonly",
        ),
        pytest.param(
            CSharp(),
            CSharp.modifiers.CONST,
            "_CSharpModifiers.CONST",
            id="csharp-const",
        ),
    ],
)
def test_immutable_modifier_rejected(
    language: Language,
    modifier: enum.Enum,
    spelling: str,
) -> None:
    """A modifier binding the name once cannot take both forms."""
    with pytest.raises(
        expected_exception=ImmutableVariableModifierError,
        match=re.escape(
            pattern=(
                f"{type(language).__name__} cannot combine "
                f"BothVariableForms with {spelling}"
            )
        ),
    ):
        literalize(
            source="[1, 2]",
            input_format=InputFormat.JSON,
            language=language,
            variable_form=BothVariableForms(
                name="my_val",
                modifiers=frozenset({modifier}),
            ),
            wrap_in_file=True,
        )


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
