"""Java ``json_type`` rejection paths."""

import pytest

from literalizer import InputFormat, NewVariable, literalize
from literalizer.exceptions import (
    IncompatibleFormatsError,
    UnrepresentableInputError,
)
from literalizer.languages import Java


def test_java_json_type_rejects_non_string_dict_keys() -> None:
    """Jackson ``JsonNode`` object keys must be strings."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="dict keys as JSON object strings",
    ):
        literalize(
            source="{1: one}",
            input_format=InputFormat.YAML,
            language=Java(json_type=Java.json_types.JACKSON_JSON_NODE),
            variable_form=NewVariable(name="my_data", modifiers=frozenset()),
        )


def test_java_json_type_rejects_record_strategy() -> None:
    """``readTree`` rendering cannot coexist with generated records."""
    with pytest.raises(
        expected_exception=IncompatibleFormatsError,
        match="incompatible with heterogeneous_strategy=RECORD",
    ):
        Java(
            json_type=Java.json_types.JACKSON_JSON_NODE,
            heterogeneous_strategy=Java.heterogeneous_strategies.RECORD,
        )
