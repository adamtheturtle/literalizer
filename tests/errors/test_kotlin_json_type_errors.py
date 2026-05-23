"""Kotlin ``json_type`` rejection paths."""

import pytest

from literalizer import InputFormat, NewVariable, literalize
from literalizer.exceptions import (
    IncompatibleFormatsError,
    UnrepresentableInputError,
)
from literalizer.languages import Kotlin


def test_kotlin_json_type_rejects_non_string_dict_keys() -> None:
    """``JsonElement`` object keys must be strings."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="dict keys as JSON object strings",
    ):
        literalize(
            source="{1: one}",
            input_format=InputFormat.YAML,
            language=Kotlin(
                json_type=Kotlin.json_types.KOTLINX_JSON_ELEMENT,
            ),
            variable_form=NewVariable(name="my_data"),
        )


def test_kotlin_json_type_rejects_record_strategy() -> None:
    """``parseToJsonElement`` rendering cannot coexist with records."""
    with pytest.raises(
        expected_exception=IncompatibleFormatsError,
        match="incompatible with heterogeneous_strategy=RECORD",
    ):
        Kotlin(
            json_type=Kotlin.json_types.KOTLINX_JSON_ELEMENT,
            heterogeneous_strategy=Kotlin.heterogeneous_strategies.RECORD,
        )
