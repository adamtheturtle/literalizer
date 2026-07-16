"""Validation tests for reserved ``NewVariable`` names."""

import pytest

from literalizer import InputFormat, NewVariable, literalize, literalize_call
from literalizer.exceptions import ReservedVariableNameError
from literalizer.languages import (
    JavaScript,
    Sml,
    Swift,
    TypeScript,
    V,
    Zig,
)


@pytest.mark.parametrize(
    argnames=("language_cls", "language_name", "reserved_name"),
    argvalues=[
        (JavaScript, "JavaScript", "class"),
        (Sml, "Sml", "op"),
        (Sml, "Sml", "val"),
        (Swift, "Swift", "class"),
        (TypeScript, "TypeScript", "class"),
        (V, "V", "type"),
        (Zig, "Zig", "error"),
    ],
    ids=(
        "javascript-class",
        "sml-op",
        "sml-val",
        "swift-class",
        "typescript-class",
        "v-type",
        "zig-error",
    ),
)
def test_reserved_new_variable_name_raises(
    language_cls: type[JavaScript]
    | type[Sml]
    | type[Swift]
    | type[TypeScript]
    | type[V]
    | type[Zig],
    language_name: str,
    reserved_name: str,
) -> None:
    """Reserved names are rejected instead of silently being rewritten."""
    with pytest.raises(
        expected_exception=ReservedVariableNameError,
        match=rf"^{language_name} cannot use NewVariable name "
        rf"'{reserved_name}': "
        r"it is a reserved identifier$",
    ):
        literalize(
            source="1",
            input_format=InputFormat.JSON,
            language=language_cls(),
            variable_form=NewVariable(
                name=reserved_name,
                modifiers=frozenset(),
            ),
            wrap_in_file=True,
        )


@pytest.mark.parametrize(
    argnames="language_cls",
    argvalues=[JavaScript, TypeScript],
    ids=("javascript", "typescript"),
)
def test_ecmascript_reserved_property_call_remains_valid(
    language_cls: type[JavaScript] | type[TypeScript],
) -> None:
    """Reserved variable names do not block valid property calls."""
    result = literalize_call(
        source="[1]",
        input_format=InputFormat.JSON,
        language=language_cls(),
        target_function="foo.class",
        parameter_names=["value"],
    )

    assert result.code
