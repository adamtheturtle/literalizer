"""Errors for explicit hints over empty/non-empty sibling sequences."""

import pytest

from literalizer import InputFormat, NewVariable, literalize
from literalizer.exceptions import UnrepresentableInputError
from literalizer.languages import Kotlin


def test_kotlin_rejects_empty_sibling_sequence_type_hints() -> None:
    """Kotlin rejects a nested shape its explicit annotation cannot
    hold.
    """
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match=(
            "Kotlin cannot represent explicit type hints for sibling "
            "sequences that mix empty and non-empty values"
        ),
    ):
        literalize(
            source="mixed = [[09:30:00], []]\n",
            input_format=InputFormat.TOML,
            language=Kotlin(
                variable_type_hints=Kotlin.variable_type_hints_formats.ALWAYS,
            ),
            variable_form=NewVariable(name="my_data", modifiers=frozenset()),
            wrap_in_file=True,
        )
