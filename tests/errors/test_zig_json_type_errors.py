"""Zig ``json_type`` rejection paths."""

import pytest

from literalizer import InputFormat, NewVariable, literalize
from literalizer.exceptions import (
    IncompatibleFormatsError,
    UnrepresentableInputError,
    UnrepresentableSpecialFloatError,
)
from literalizer.languages import Zig


def test_zig_json_type_rejects_non_string_dict_keys() -> None:
    """``std.json.Value`` object keys must be strings."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="dict keys as JSON object strings",
    ):
        literalize(
            source="{1: one}",
            input_format=InputFormat.YAML,
            language=Zig(json_type=Zig.json_types.STD_JSON_VALUE),
            variable_form=NewVariable(name="my_data", modifiers=frozenset()),
        )


def test_zig_json_type_rejects_record_strategy() -> None:
    """``parseFromSlice`` rendering cannot coexist with generated
    records.
    """
    with pytest.raises(
        expected_exception=IncompatibleFormatsError,
        match="incompatible with heterogeneous_strategy=RECORD",
    ):
        Zig(
            json_type=Zig.json_types.STD_JSON_VALUE,
            heterogeneous_strategy=Zig.heterogeneous_strategies.RECORD,
        )


def test_zig_json_type_rejects_special_floats() -> None:
    """``std.json.parseFromSlice`` accepts only finite numbers."""
    with pytest.raises(
        expected_exception=UnrepresentableSpecialFloatError,
        match="parseFromSlice accepts only finite numbers",
    ):
        literalize(
            source="[.inf]",
            input_format=InputFormat.YAML,
            language=Zig(json_type=Zig.json_types.STD_JSON_VALUE),
            variable_form=NewVariable(name="my_data", modifiers=frozenset()),
        )
