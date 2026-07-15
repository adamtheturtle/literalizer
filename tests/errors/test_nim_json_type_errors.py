"""Nim ``json_type`` rejection paths."""

import pytest

from literalizer import InputFormat, NewVariable, literalize
from literalizer.exceptions import (
    IncompatibleFormatsError,
    UnrepresentableInputError,
)
from literalizer.languages import Nim


def test_nim_json_type_rejects_non_string_dict_keys() -> None:
    """``JsonNode`` object keys must be strings."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="dict key of type int",
    ):
        literalize(
            source="{1: one}",
            input_format=InputFormat.YAML,
            language=Nim(json_type=Nim.json_types.JSON_NODE),
            variable_form=NewVariable(name="my_data", modifiers=frozenset()),
        )


def test_nim_json_type_rejects_const_declarations() -> None:
    """``%*`` is not a Nim constant-expression initializer."""
    with pytest.raises(
        expected_exception=IncompatibleFormatsError,
        match="constant-expression initializer",
    ):
        Nim(
            json_type=Nim.json_types.JSON_NODE,
            declaration_style=Nim.declaration_styles.CONST,
        )
