"""Odin ``json_type`` rejection paths."""

import pytest

from literalizer import InputFormat, NewVariable, literalize
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
