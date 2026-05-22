"""Crystal ``json_type`` rejection paths."""

import pytest

from literalizer import InputFormat, NewVariable, literalize
from literalizer.exceptions import UnrepresentableInputError
from literalizer.languages import Crystal


def test_crystal_json_type_rejects_non_string_dict_keys() -> None:
    """``JSON::Any`` object keys must be strings."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="dict keys as JSON object strings",
    ):
        literalize(
            source="{1: one}",
            input_format=InputFormat.YAML,
            language=Crystal(json_type=Crystal.json_types.JSON_ANY),
            variable_form=NewVariable(name="my_data"),
        )


def test_crystal_json_type_rejects_overflow_integers() -> None:
    """``JSON::Any#as_i`` only exposes signed 64-bit integers."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="outside the signed 64-bit range",
    ):
        literalize(
            source=str(object=2**64),
            input_format=InputFormat.JSON,
            language=Crystal(json_type=Crystal.json_types.JSON_ANY),
            variable_form=NewVariable(name="my_data"),
        )


def test_crystal_json_type_rejects_double_quote_in_string() -> None:
    """Embedded ``"`` would break Crystal's ``%(...)`` percent literal."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="double quote",
    ):
        literalize(
            source='{"greeting": "say \\"hi\\""}',
            input_format=InputFormat.JSON,
            language=Crystal(json_type=Crystal.json_types.JSON_ANY),
            variable_form=NewVariable(name="my_data"),
        )


def test_crystal_json_type_rejects_string_interpolation_sequence() -> None:
    """Embedded ``#{`` would be interpreted as Crystal interpolation."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="string interpolation",
    ):
        literalize(
            source='{"template": "value=#{x}"}',
            input_format=InputFormat.JSON,
            language=Crystal(json_type=Crystal.json_types.JSON_ANY),
            variable_form=NewVariable(name="my_data"),
        )
