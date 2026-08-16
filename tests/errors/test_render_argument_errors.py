"""Invalid combinations of public rendering arguments."""

import pytest

from literalizer import ExistingVariable, InputFormat, NewVariable, literalize
from literalizer.exceptions import InvalidRenderArgumentError
from literalizer.languages import Python


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
