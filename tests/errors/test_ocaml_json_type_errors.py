"""OCaml ``json_type`` rejection paths."""

import pytest

from literalizer import InputFormat, NewVariable, literalize
from literalizer.exceptions import UnrepresentableInputError
from literalizer.languages import OCaml


def test_ocaml_json_type_rejects_non_string_dict_keys() -> None:
    """``Yojson.Safe.t`` ``Assoc`` keys must be strings."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="cannot represent dict key",
    ):
        literalize(
            source="{1: one}",
            input_format=InputFormat.YAML,
            language=OCaml(json_type=OCaml.json_types.YOJSON_SAFE_T),
            variable_form=NewVariable(name="my_data", modifiers=frozenset()),
        )
