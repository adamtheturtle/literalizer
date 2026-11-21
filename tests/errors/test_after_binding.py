"""Reject caller statements when a literal cannot host them."""

import pytest

from literalizer import InputFormat, Language, NewVariable, literalize
from literalizer.exceptions import InvalidRenderArgumentError
from literalizer.languages import CSharp, Jsonc


@pytest.mark.parametrize(
    argnames=("language", "wrap_in_file", "variable_form", "message"),
    argvalues=[
        (
            CSharp(),
            False,
            NewVariable(name="value", modifiers=frozenset()),
            "requires wrap_in_file=True and NewVariable",
        ),
        (CSharp(), True, None, "requires wrap_in_file=True and NewVariable"),
        (
            Jsonc(),
            True,
            NewVariable(name="value", modifiers=frozenset()),
            "Jsonc does not support after_binding",
        ),
        (
            CSharp(),
            True,
            NewVariable(
                name="value", modifiers=frozenset({CSharp.modifiers.STATIC})
            ),
            "does not support class-field bindings",
        ),
    ],
)
def test_after_binding_requires_executable_scope(
    *,
    language: Language,
    wrap_in_file: bool,
    variable_form: NewVariable | None,
    message: str,
) -> None:
    """Decline caller statements that would have no valid placement."""
    with pytest.raises(
        expected_exception=InvalidRenderArgumentError, match=message
    ):
        _ = literalize(
            source="1",
            input_format=InputFormat.JSON,
            language=language,
            variable_form=variable_form,
            wrap_in_file=wrap_in_file,
            after_binding=("_ = value;",),
        )
