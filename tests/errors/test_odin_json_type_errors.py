"""Odin ``json_type`` rejection paths."""

import pytest

from literalizer import InputFormat, NewVariable, literalize, literalize_call
from literalizer.exceptions import (
    IncompatibleFormatsError,
    UnrepresentableInputError,
)
from literalizer.languages import Odin


def test_odin_json_type_rejects_non_string_dict_keys() -> None:
    """``json.Value`` object keys must be strings."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="dict keys as JSON object strings",
    ):
        literalize(
            source="{1: one}",
            input_format=InputFormat.YAML,
            language=Odin(json_type=Odin.json_types.JSON_VALUE),
            variable_form=NewVariable(name="my_data"),
        )


def test_odin_json_type_rejects_backtick_in_string_value() -> None:
    """Backticks would terminate the Odin raw-string delimiter."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="backtick",
    ):
        literalize(
            source='{"name": "a`b"}',
            input_format=InputFormat.JSON,
            language=Odin(json_type=Odin.json_types.JSON_VALUE),
            variable_form=NewVariable(name="my_data"),
        )


def test_odin_json_type_rejects_backtick_in_dict_key() -> None:
    """A backtick in a string-typed dict key terminates the raw string too."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="backtick",
    ):
        literalize(
            source='{"a`b": 1}',
            input_format=InputFormat.JSON,
            language=Odin(json_type=Odin.json_types.JSON_VALUE),
            variable_form=NewVariable(name="my_data"),
        )


def test_odin_json_type_call_arg_rejects_non_string_dict_keys() -> None:
    """Call-argument validation also applies the JSON object-key rule."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="dict keys as JSON object strings",
    ):
        literalize_call(
            source="- {1: one}",
            input_format=InputFormat.YAML,
            language=Odin(json_type=Odin.json_types.JSON_VALUE),
            target_function="process",
            parameter_names=["x"],
        )


def test_odin_json_type_call_arg_rejects_backtick_in_string() -> None:
    """Call-argument validation also applies the backtick rule."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="backtick",
    ):
        literalize_call(
            source='- "a`b"',
            input_format=InputFormat.YAML,
            language=Odin(json_type=Odin.json_types.JSON_VALUE),
            target_function="process",
            parameter_names=["x"],
        )


def test_odin_json_type_rejects_nan() -> None:
    """JSON has no syntax for ``NaN``."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="non-finite floats",
    ):
        literalize(
            source=".nan",
            input_format=InputFormat.YAML,
            language=Odin(json_type=Odin.json_types.JSON_VALUE),
            variable_form=NewVariable(name="my_data"),
        )


def test_odin_json_type_rejects_positive_infinity() -> None:
    """JSON has no syntax for ``+Infinity``."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="non-finite floats",
    ):
        literalize(
            source=".inf",
            input_format=InputFormat.YAML,
            language=Odin(json_type=Odin.json_types.JSON_VALUE),
            variable_form=NewVariable(name="my_data"),
        )


def test_odin_json_type_rejects_record_strategy() -> None:
    """``_json_parse`` rendering cannot coexist with generated
    records.
    """
    with pytest.raises(
        expected_exception=IncompatibleFormatsError,
        match="incompatible with heterogeneous_strategy=RECORD",
    ):
        Odin(
            json_type=Odin.json_types.JSON_VALUE,
            heterogeneous_strategy=Odin.heterogeneous_strategies.RECORD,
        )
