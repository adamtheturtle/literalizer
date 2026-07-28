"""PureScript ``json_type`` rejection paths."""

import pytest

from literalizer import InputFormat, NewVariable, literalize
from literalizer.exceptions import (
    UnrepresentableInputError,
    UnrepresentableSpecialFloatError,
)
from literalizer.languages import PureScript


def test_purescript_json_type_rejects_non_string_dict_keys() -> None:
    """``Data.Argonaut.Core.Json`` object keys must be strings."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="dict keys as JSON object",
    ):
        literalize(
            source="{1: one}",
            input_format=InputFormat.YAML,
            language=PureScript(
                json_type=PureScript.json_types.ARGONAUT_JSON,
            ),
            variable_form=NewVariable(name="my_data", modifiers=frozenset()),
        )


def test_purescript_json_type_rejects_special_float_nan() -> None:
    """Reject ``NaN`` since JSON has no syntax for it."""
    with pytest.raises(
        expected_exception=UnrepresentableSpecialFloatError,
        match="NaN or infinity",
    ):
        literalize(
            source="[NaN]",
            input_format=InputFormat.JSON5,
            language=PureScript(
                json_type=PureScript.json_types.ARGONAUT_JSON,
            ),
            variable_form=NewVariable(name="my_data", modifiers=frozenset()),
        )


def test_purescript_json_type_rejects_special_float_infinity() -> None:
    """Reject ``Infinity`` since JSON has no syntax for it."""
    with pytest.raises(
        expected_exception=UnrepresentableSpecialFloatError,
        match="NaN or infinity",
    ):
        literalize(
            source="[Infinity]",
            input_format=InputFormat.JSON5,
            language=PureScript(
                json_type=PureScript.json_types.ARGONAUT_JSON,
            ),
            variable_form=NewVariable(name="my_data", modifiers=frozenset()),
        )
