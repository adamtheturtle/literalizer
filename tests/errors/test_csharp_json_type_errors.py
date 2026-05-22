"""C# ``json_type`` rejection paths."""

import pytest

from literalizer import InputFormat, NewVariable, literalize
from literalizer.exceptions import (
    IncompatibleFormatsError,
    UnrepresentableInputError,
)
from literalizer.languages import CSharp


def test_csharp_json_type_rejects_non_string_dict_keys() -> None:
    """``JsonObject`` keys must be strings."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="dict keys as JSON object strings",
    ):
        literalize(
            source="{1: one}",
            input_format=InputFormat.YAML,
            language=CSharp(
                json_type=CSharp.json_types.SYSTEM_TEXT_JSON_NODE,
            ),
            variable_form=NewVariable(name="my_data"),
        )


def test_csharp_json_type_rejects_const_declarations() -> None:
    """The ``new JsonObject``/``new JsonArray`` constructors and the
    ``(JsonNode?)`` cast applied to scalars are not C#
    constant-expression initializers, so the ``const`` modifier is
    rejected.
    """
    with pytest.raises(
        expected_exception=IncompatibleFormatsError,
        match="not constant",
    ):
        literalize(
            source="[1, 2, 3]",
            input_format=InputFormat.JSON,
            language=CSharp(
                json_type=CSharp.json_types.SYSTEM_TEXT_JSON_NODE,
            ),
            variable_form=NewVariable(
                name="my_data",
                modifiers=frozenset({CSharp.modifiers.CONST}),
            ),
        )
