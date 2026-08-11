"""C ``json_type=CJSON`` rejection paths."""

import pytest

from literalizer import InputFormat, literalize_call
from literalizer.exceptions import (
    UnrepresentableInputError,
)
from literalizer.languages import C


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
