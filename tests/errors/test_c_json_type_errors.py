"""C ``json_type=CJSON`` rejection paths."""

import pytest

from literalizer import InputFormat, NewVariable, literalize, literalize_call
from literalizer.exceptions import (
    IncompatibleFormatsError,
    UnrepresentableInputError,
)
from literalizer.languages import C


def test_c_cjson_rejects_non_string_dict_keys() -> None:
    """A ``cJSON`` object is keyed by JSON strings."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="dict keys as JSON object strings",
    ):
        literalize(
            source="{1: one}",
            input_format=InputFormat.YAML,
            language=C(json_type=C.json_types.CJSON),
            variable_form=NewVariable(name="my_data", modifiers=frozenset()),
        )


def test_c_cjson_rejects_container_call_argument() -> None:
    """A container call argument has no single-expression cJSON form.

    ``per_element`` reads ``[[[1, 2]]]`` as one call whose single
    argument is the list ``[1, 2]``; a container cannot be built inline
    as one ``cJSON_Create*(...)`` expression, so it is rejected.
    """
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="container call argument",
    ):
        literalize_call(
            source="[[[1, 2]]]",
            input_format=InputFormat.JSON,
            language=C(json_type=C.json_types.CJSON),
            target_function="process",
            parameter_names=["x"],
        )


def test_c_cjson_rejects_record_strategy() -> None:
    """A cJSON node tree cannot coexist with generated ``struct``s."""
    with pytest.raises(
        expected_exception=IncompatibleFormatsError,
        match="incompatible with heterogeneous_strategy=RECORD",
    ):
        C(
            json_type=C.json_types.CJSON,
            heterogeneous_strategy=C.heterogeneous_strategies.RECORD,
        )
