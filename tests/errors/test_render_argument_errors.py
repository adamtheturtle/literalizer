"""Invalid combinations of public rendering arguments."""

import pytest

from literalizer import ExistingVariable, InputFormat, NewVariable, literalize
from literalizer._language import Language
from literalizer.exceptions import (
    ExistingVariableNotSelfContainedError,
    InvalidRenderArgumentError,
)
from literalizer.languages import (
    Cpp,
    CSharp,
    Go,
    Java,
    Kotlin,
    Python,
    Rust,
    Swift,
)


def test_negative_pre_indent_level_is_rejected() -> None:
    """Negative indentation is an argument error, not an alias for
    zero.
    """
    with pytest.raises(
        expected_exception=InvalidRenderArgumentError,
        match="pre_indent_level must be greater than or equal to zero",
    ):
        literalize(
            source='{"a": 1}',
            input_format=InputFormat.JSON,
            language=Python(),
            pre_indent_level=-1,
        )


@pytest.mark.parametrize(
    argnames="variable_form",
    argvalues=[
        NewVariable(name="x", modifiers=frozenset()),
        ExistingVariable(name="x"),
    ],
)
def test_delimiter_stripped_variable_binding_is_rejected(
    variable_form: NewVariable | ExistingVariable,
) -> None:
    """A fragment cannot be assigned as though it were one value."""
    with pytest.raises(
        expected_exception=InvalidRenderArgumentError,
        match="include_delimiters=False cannot be combined with variable_form",
    ):
        literalize(
            source="[1, 2]",
            input_format=InputFormat.JSON,
            language=Python(),
            include_delimiters=False,
            variable_form=variable_form,
        )


@pytest.mark.parametrize(
    argnames="language",
    argvalues=[Java(), Cpp(), CSharp(), Go(), Rust(), Swift(), Kotlin()],
)
def test_existing_variable_complete_file_requires_declaration(
    language: Language,
) -> None:
    """A complete typed wrapper cannot assign an undeclared variable."""
    with pytest.raises(
        expected_exception=ExistingVariableNotSelfContainedError,
        match="assignment has no prior declaration",
    ):
        literalize(
            source="1",
            input_format=InputFormat.JSON,
            language=language,
            variable_form=ExistingVariable(name="x"),
            wrap_in_file=True,
        )


def test_self_declaring_existing_variable_file_remains_supported() -> None:
    """Python's assignment form is identical to its declaration form."""
    result = literalize(
        source="1",
        input_format=InputFormat.JSON,
        language=Python(),
        variable_form=ExistingVariable(name="x"),
        wrap_in_file=True,
    )

    assert "x = 1" in result.code
