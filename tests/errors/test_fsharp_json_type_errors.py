"""F# ``json_type`` rejection paths."""

import pytest

from literalizer import InputFormat, NewVariable, literalize
from literalizer.exceptions import UnrepresentableInputError
from literalizer.languages import FSharp


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
