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
            variable_form=NewVariable(name="my_data"),
        )


def test_cpp_json_type_rejects_raw_string_terminator_in_key() -> None:
    r"""Reject dict keys that close the ``R"json(...)json"`` literal.

    A key whose name ends with ``)json`` collides with the raw-string
    terminator because :func:`json.dumps` writes ``")json"`` as a
    literal byte sequence, which would close the C++ raw-string literal
    mid-document.  String *values* containing literal ``"`` characters
    are escaped to ``\"`` and so cannot reach the terminator unless they
    end with ``)json`` themselves (covered by the same check).
    """
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="raw-string terminator",
    ):
        literalize(
            source='{")json": "x"}',
            input_format=InputFormat.JSON,
            language=Cpp(json_type=Cpp.json_types.NLOHMANN_JSON),
            variable_form=NewVariable(name="my_data"),
        )


def test_cpp_json_type_rejects_record_strategy() -> None:
    """``parse`` rendering cannot coexist with generated ``struct``s."""
    with pytest.raises(
        expected_exception=IncompatibleFormatsError,
        match="incompatible with heterogeneous_strategy=RECORD",
    ):
        Cpp(
            json_type=Cpp.json_types.NLOHMANN_JSON,
            heterogeneous_strategy=Cpp.heterogeneous_strategies.RECORD,
        )


def test_cpp_json_type_rejects_tuple_strategy() -> None:
    """``parse`` rendering cannot coexist with generated tuple aliases."""
    with pytest.raises(
        expected_exception=IncompatibleFormatsError,
        match="incompatible with heterogeneous_strategy=TUPLE",
    ):
        Cpp(
            json_type=Cpp.json_types.NLOHMANN_JSON,
            heterogeneous_strategy=Cpp.heterogeneous_strategies.TUPLE,
        )
