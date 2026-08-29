"""Errors for declaration modifiers from another language.

A manifest names a modifier and the runner resolves it against the
language under test, which is the opposite of what these need: a
modifier belonging to some other language.
"""

import re
from collections.abc import Callable

import pytest

from literalizer import InputFormat, NewVariable, literalize, literalize_call
from literalizer.exceptions import InvalidVariableModifierError
from literalizer.languages import Java, Kotlin

_FOREIGN_MODIFIER = NewVariable(
    name="value",
    modifiers=frozenset({Java.modifiers.FINAL}),
)


def _assert_foreign_modifier_rejected(render: Callable[[], object]) -> None:
    """Assert that *render* rejects the shared foreign modifier."""
    with pytest.raises(
        expected_exception=InvalidVariableModifierError,
        match=re.escape(
            pattern=(
                "Kotlin cannot apply variable modifier "
                "_JavaModifiers.FINAL: it is not a member"
            )
        ),
    ):
        render()


def test_literalize_rejects_foreign_variable_modifier() -> None:
    """Value declarations reject another language's modifier."""
    _assert_foreign_modifier_rejected(
        render=lambda: literalize(
            source="[1]",
            input_format=InputFormat.JSON,
            language=Kotlin(),
            variable_form=_FOREIGN_MODIFIER,
        )
    )


def test_literalize_call_rejects_foreign_variable_modifier() -> None:
    """Call declarations reject another language's modifier."""
    _assert_foreign_modifier_rejected(
        render=lambda: literalize_call(
            source="[[1]]",
            input_format=InputFormat.JSON,
            language=Kotlin(),
            target_function="consume",
            parameter_names=("value",),
            variable_form=_FOREIGN_MODIFIER,
        )
    )


def test_target_language_modifier_remains_valid() -> None:
    """A modifier from the target language still reaches its renderer."""
    result = literalize(
        source="1",
        input_format=InputFormat.JSON,
        language=Java(),
        variable_form=NewVariable(
            name="value",
            modifiers=frozenset({Java.modifiers.FINAL}),
        ),
    )

    assert result.code == "final int value = 1;"
