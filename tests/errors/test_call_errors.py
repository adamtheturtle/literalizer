"""Error contracts for internal checks and declaration composition."""

import inspect

import pytest

from literalizer import (
    ExistingVariable,
    InputFormat,
    NewVariable,
    literalize,
    literalize_call,
    literalize_call_with_declarations,
)
from literalizer._language import validate_call_parameter_names
from literalizer.exceptions import UnsupportedCallShapeError
from literalizer.languages import Ada


def test_call_parameter_validation_requires_language_metaclass() -> None:
    """Malformed internal language objects fail immediately."""
    validator = inspect.unwrap(func=validate_call_parameter_names)
    with pytest.raises(
        expected_exception=TypeError,
        match="requires a LanguageCls language",
    ):
        validator(language=object(), names=(), reject_reserved=True)


def test_ada_composition_rejects_declaration_after_assignment() -> None:
    """A flat Ada declarative region cannot preserve this use order."""
    language = Ada()
    forms: list[NewVariable | ExistingVariable] = [
        NewVariable(name="first", modifiers=frozenset()),
        ExistingVariable(name="first"),
        NewVariable(name="second", modifiers=frozenset()),
    ]
    declarations = [
        literalize(
            source=source,
            input_format=InputFormat.JSON,
            language=language,
            variable_form=form,
            ref_key="$ref",
            ref_values={"first": 0},
        )
        for source, form in zip(
            ["0", "1", '{"$ref":"first"}'], forms, strict=True
        )
    ]
    call = literalize_call(
        source="0",
        input_format=InputFormat.JSON,
        language=language,
        target_function="consume",
        parameter_names=["value"],
        per_element=False,
    )
    with pytest.raises(
        expected_exception=UnsupportedCallShapeError,
        match="a declaration after an executable assignment",
    ):
        _ = literalize_call_with_declarations(
            language=language, declarations=declarations, call=call
        )
