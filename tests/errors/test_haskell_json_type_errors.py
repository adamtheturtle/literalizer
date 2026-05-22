"""Haskell ``json_type`` rejection paths."""

import pytest

from literalizer import InputFormat, NewVariable, literalize
from literalizer.exceptions import UnrepresentableInputError
from literalizer.languages import Haskell


def test_haskell_json_type_rejects_non_string_dict_keys() -> None:
    """The ``Data.Aeson.Value`` object keys must be strings."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="cannot represent dict key",
    ):
        literalize(
            source="{1: one}",
            input_format=InputFormat.YAML,
            language=Haskell(json_type=Haskell.json_types.AESON_VALUE),
            variable_form=NewVariable(name="my_data"),
        )
