"""Erlang ``json_type`` rejection paths."""

import pytest

from literalizer import InputFormat, NewVariable, literalize
from literalizer.exceptions import UnrepresentableInputError
from literalizer.languages import Erlang


def test_erlang_json_type_rejects_non_string_dict_keys() -> None:
    """Erlang's ``json:encode/1`` requires string keys."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="cannot represent dict key",
    ):
        literalize(
            source="{1: one}",
            input_format=InputFormat.YAML,
            language=Erlang(json_type=Erlang.json_types.OTP_JSON),
            variable_form=NewVariable(name="myData"),
        )
