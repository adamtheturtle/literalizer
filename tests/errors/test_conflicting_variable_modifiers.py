"""Errors for declaration modifiers that cannot be combined."""

import re

import pytest

from literalizer import InputFormat, NewVariable, literalize
from literalizer.exceptions import ConflictingVariableModifiersError
from literalizer.languages import CSharp, Java


def test_java_rejects_two_visibilities() -> None:
    """A field has one visibility, so ``public private`` would not compile."""
    with pytest.raises(
        expected_exception=ConflictingVariableModifiersError,
        match=re.escape(
            pattern=(
                "Java accepts at most one visibility modifier; "
                "received public, private"
            )
        ),
    ):
        literalize(
            source="1",
            input_format=InputFormat.JSON,
            language=Java(),
            variable_form=NewVariable(
                name="value",
                modifiers=frozenset(
                    {Java.modifiers.PUBLIC, Java.modifiers.PRIVATE},
                ),
            ),
        )


def test_csharp_rejects_two_visibilities() -> None:
    """C# fields have a single visibility too."""
    with pytest.raises(expected_exception=ConflictingVariableModifiersError):
        literalize(
            source="1",
            input_format=InputFormat.JSON,
            language=CSharp(),
            variable_form=NewVariable(
                name="value",
                modifiers=frozenset(
                    {CSharp.modifiers.PUBLIC, CSharp.modifiers.PROTECTED},
                ),
            ),
        )


def test_csharp_rejects_const_with_readonly() -> None:
    """``const`` is already immutable, so ``readonly`` conflicts with
    it.
    """
    with pytest.raises(
        expected_exception=ConflictingVariableModifiersError,
        match=re.escape(
            pattern=(
                "CSharp accepts at most one mutability modifier; "
                "received const, readonly"
            )
        ),
    ):
        literalize(
            source="1",
            input_format=InputFormat.JSON,
            language=CSharp(),
            variable_form=NewVariable(
                name="value",
                modifiers=frozenset(
                    {CSharp.modifiers.CONST, CSharp.modifiers.READONLY},
                ),
            ),
        )


def test_one_modifier_per_group_is_accepted() -> None:
    """Modifiers from different groups still combine."""
    result = literalize(
        source="1",
        input_format=InputFormat.JSON,
        language=Java(),
        variable_form=NewVariable(
            name="value",
            modifiers=frozenset(
                {
                    Java.modifiers.PUBLIC,
                    Java.modifiers.STATIC,
                    Java.modifiers.FINAL,
                },
            ),
        ),
    )

    assert result.code == "public static final int value = 1;"
