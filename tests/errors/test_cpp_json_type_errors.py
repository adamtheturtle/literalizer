"""C++ ``json_type`` rejection paths."""

import pytest

from literalizer import InputFormat, NewVariable, literalize
from literalizer.exceptions import (
    IncompatibleFormatsError,
    UnrepresentableInputError,
)
from literalizer.languages import Cpp


def test_cpp_json_type_rejects_non_string_dict_keys() -> None:
    """``nlohmann::json`` object keys must be strings."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="dict keys as JSON object strings",
    ):
        literalize(
            source="{1: one}",
            input_format=InputFormat.YAML,
            language=Cpp(json_type=Cpp.json_types.NLOHMANN_JSON),
            variable_form=NewVariable(name="my_data", modifiers=frozenset()),
        )


def test_cpp_json_type_rejects_record_strategy() -> None:
    """JSON rendering cannot coexist with generated ``struct``s."""
    with pytest.raises(
        expected_exception=IncompatibleFormatsError,
        match="incompatible with heterogeneous_strategy=RECORD",
    ):
        Cpp(
            json_type=Cpp.json_types.NLOHMANN_JSON,
            heterogeneous_strategy=Cpp.heterogeneous_strategies.RECORD,
        )


def test_cpp_json_type_rejects_tuple_strategy() -> None:
    """JSON rendering cannot coexist with generated tuple aliases."""
    with pytest.raises(
        expected_exception=IncompatibleFormatsError,
        match="incompatible with heterogeneous_strategy=TUPLE",
    ):
        Cpp(
            json_type=Cpp.json_types.NLOHMANN_JSON,
            heterogeneous_strategy=Cpp.heterogeneous_strategies.TUPLE,
        )
