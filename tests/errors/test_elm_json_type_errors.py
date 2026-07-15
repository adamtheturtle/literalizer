"""Elm ``json_type`` rejection paths."""

import pytest

from literalizer import InputFormat, NewVariable, literalize
from literalizer.exceptions import UnrepresentableInputError
from literalizer.languages import Elm


def test_elm_json_type_rejects_non_string_dict_keys() -> None:
    """``Json.Encode.object`` keys must be strings."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="cannot represent dict key",
    ):
        literalize(
            source="{1: one}",
            input_format=InputFormat.YAML,
            language=Elm(json_type=Elm.json_types.JSON_ENCODE_VALUE),
            variable_form=NewVariable(name="my_data", modifiers=frozenset()),
        )


def test_elm_json_type_rejects_nested_non_string_dict_keys() -> None:
    """Non-string keys nested inside a list are caught upfront."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="cannot represent dict key",
    ):
        literalize(
            source="[{1: one}]",
            input_format=InputFormat.YAML,
            language=Elm(json_type=Elm.json_types.JSON_ENCODE_VALUE),
            variable_form=NewVariable(name="my_data", modifiers=frozenset()),
        )
