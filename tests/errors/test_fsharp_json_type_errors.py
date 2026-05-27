"""F# ``json_type`` rejection paths."""

import pytest

from literalizer import InputFormat, NewVariable, literalize
from literalizer.exceptions import (
    UnrepresentableInputError,
    UnrepresentableIntegerError,
)
from literalizer.languages import FSharp


def test_fsharp_json_type_rejects_out_of_range_integer() -> None:
    """Integers outside the ``Int64`` / ``UInt64`` ranges have no
    ``JsonValue.Create`` overload and are rejected.
    """
    with pytest.raises(
        expected_exception=UnrepresentableIntegerError,
        match=r"JsonValue\.Create has no overload",
    ):
        literalize(
            source="-99999999999999999999",
            input_format=InputFormat.JSON,
            language=FSharp(
                json_type=FSharp.json_types.SYSTEM_TEXT_JSON_NODE,
            ),
            variable_form=NewVariable(name="my_data"),
        )


def test_fsharp_json_type_rejects_non_string_dict_keys() -> None:
    """``JsonObject`` keys must be strings."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="dict keys as JSON object strings",
    ):
        literalize(
            source="{1: one}",
            input_format=InputFormat.YAML,
            language=FSharp(
                json_type=FSharp.json_types.SYSTEM_TEXT_JSON_NODE,
            ),
            variable_form=NewVariable(name="my_data"),
        )
