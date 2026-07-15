"""Rust ``json_type`` rejection paths."""

import pytest

from literalizer import InputFormat, NewVariable, literalize
from literalizer.exceptions import (
    IncompatibleFormatsError,
    UnrepresentableInputError,
)
from literalizer.languages import Rust


def test_rust_json_type_rejects_non_string_dict_keys() -> None:
    """``serde_json::Value`` object keys must be strings."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="dict keys as JSON object strings",
    ):
        literalize(
            source="{1: one}",
            input_format=InputFormat.YAML,
            language=Rust(json_type=Rust.json_types.SERDE_JSON_VALUE),
            variable_form=NewVariable(name="my_data", modifiers=frozenset()),
        )


def test_rust_json_type_rejects_const_declarations() -> None:
    """``serde_json::json!`` is not a Rust const initializer."""
    with pytest.raises(
        expected_exception=IncompatibleFormatsError,
        match="not a constant-expression initializer",
    ):
        Rust(
            json_type=Rust.json_types.SERDE_JSON_VALUE,
            declaration_style=Rust.declaration_styles.CONST,
        )
