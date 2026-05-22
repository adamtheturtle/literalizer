"""Scala ``json_type`` rejection paths."""

import pytest

from literalizer import InputFormat, NewVariable, literalize
from literalizer.exceptions import UnrepresentableInputError
from literalizer.languages import Scala


def test_scala_json_type_rejects_non_string_dict_keys() -> None:
    """Circe ``Json.obj`` keys must be JSON object strings."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="dict keys as JSON object strings",
    ):
        literalize(
            source="{1: one}",
            input_format=InputFormat.YAML,
            language=Scala(json_type=Scala.json_types.CIRCE),
            variable_form=NewVariable(name="my_data"),
        )
