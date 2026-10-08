"""Reject Jackson declarations that require Java field scope."""

import enum
import re

import pytest

from literalizer import (
    BothVariableForms,
    InputFormat,
    NewVariable,
    literalize,
)
from literalizer.exceptions import (
    ConflictingVariableModifiersError,
    ImmutableVariableModifierError,
    IncompatibleFormatsError,
)
from literalizer.languages import Java


@pytest.mark.parametrize(
    argnames="modifiers",
    argvalues=[
        frozenset({Java.modifiers.PUBLIC}),
        frozenset({Java.modifiers.PRIVATE}),
        frozenset({Java.modifiers.PROTECTED}),
        frozenset({Java.modifiers.STATIC}),
        frozenset({Java.modifiers.PUBLIC, Java.modifiers.STATIC}),
    ],
)
@pytest.mark.parametrize(
    argnames=("variable_form_type", "wrap_in_file"),
    argvalues=[
        (NewVariable, False),
        (NewVariable, True),
        (BothVariableForms, True),
    ],
)
def test_json_field_modifiers(
    *,
    modifiers: frozenset[enum.Enum],
    variable_form_type: type[NewVariable] | type[BothVariableForms],
    wrap_in_file: bool,
) -> None:
    """Field modifiers fail explicitly in declarations and combined
    forms.
    """
    with pytest.raises(
        expected_exception=IncompatibleFormatsError,
        match=re.escape(
            pattern=(
                "Java json_type renders data through "
                "ObjectMapper.readTree(...) "
                "and does not support class-field modifiers "
                "(public, private, protected, static), which require handling "
                "the checked parsing exception in a field initializer. "
                "Remove these modifiers to use a local declaration."
            ),
        ),
    ):
        _ = literalize(
            source="42",
            input_format=InputFormat.JSON,
            language=Java(json_type=Java.json_types.JACKSON_JSON_NODE),
            variable_form=variable_form_type(name="data", modifiers=modifiers),
            wrap_in_file=wrap_in_file,
        )


def test_json_static_final_declaration() -> None:
    """Finality does not make a checked field initializer valid."""
    with pytest.raises(
        expected_exception=IncompatibleFormatsError,
        match="does not support class-field modifiers",
    ):
        _ = literalize(
            source="42",
            input_format=InputFormat.JSON,
            language=Java(json_type=Java.json_types.JACKSON_JSON_NODE),
            variable_form=NewVariable(
                name="data",
                modifiers=frozenset(
                    {Java.modifiers.STATIC, Java.modifiers.FINAL}
                ),
            ),
            wrap_in_file=True,
        )


def test_json_conflicting_visibility_modifiers() -> None:
    """Conflicting visibility retains its specific modifier error."""
    with pytest.raises(
        expected_exception=ConflictingVariableModifiersError,
        match="visibility",
    ):
        _ = literalize(
            source="42",
            input_format=InputFormat.JSON,
            language=Java(json_type=Java.json_types.JACKSON_JSON_NODE),
            variable_form=NewVariable(
                name="data",
                modifiers=frozenset(
                    {Java.modifiers.PUBLIC, Java.modifiers.PRIVATE}
                ),
            ),
        )


@pytest.mark.parametrize(
    argnames="modifiers",
    argvalues=[
        frozenset({Java.modifiers.FINAL}),
        frozenset({Java.modifiers.STATIC, Java.modifiers.FINAL}),
    ],
)
def test_json_final_combined_form(modifiers: frozenset[enum.Enum]) -> None:
    """Immutable JSON declarations cannot be reassigned."""
    with pytest.raises(
        expected_exception=ImmutableVariableModifierError,
        match=re.escape(pattern="_JavaModifiers.FINAL"),
    ):
        _ = literalize(
            source="42",
            input_format=InputFormat.JSON,
            language=Java(json_type=Java.json_types.JACKSON_JSON_NODE),
            variable_form=BothVariableForms(name="data", modifiers=modifiers),
            wrap_in_file=True,
        )
