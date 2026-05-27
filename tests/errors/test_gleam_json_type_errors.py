"""Gleam ``json_type`` rejection paths."""

import pytest

from literalizer import InputFormat, NewVariable, literalize
from literalizer.exceptions import (
    UnrepresentableInputError,
    UnrepresentableSpecialFloatError,
)
from literalizer.languages import Gleam


def test_gleam_json_type_rejects_non_string_dict_keys() -> None:
    """``json.object`` entries must use string keys."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="dict key of type int",
    ):
        literalize(
            source="{1: one}",
            input_format=InputFormat.YAML,
            language=Gleam(json_type=Gleam.json_types.GLEAM_JSON_JSON),
            variable_form=NewVariable(name="my_data"),
        )


def test_gleam_json_type_rejects_special_floats() -> None:
    """``json.float`` cannot encode non-finite values on the Erlang
    target.
    """
    with pytest.raises(
        expected_exception=UnrepresentableSpecialFloatError,
        match="special float inf",
    ):
        literalize(
            source="Infinity",
            input_format=InputFormat.JSON5,
            language=Gleam(json_type=Gleam.json_types.GLEAM_JSON_JSON),
            variable_form=NewVariable(name="my_data"),
        )
