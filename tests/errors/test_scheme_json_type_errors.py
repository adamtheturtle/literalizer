"""Scheme ``json_type`` rejection paths."""

import pytest

from literalizer import InputFormat, NewVariable, literalize
from literalizer.exceptions import (
    UnrepresentableInputError,
    UnrepresentableSpecialFloatError,
)
from literalizer.languages import Scheme


def test_scheme_json_type_rejects_non_string_dict_keys() -> None:
    """``scm->json`` object keys must be strings."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="dict keys as JSON object",
    ):
        literalize(
            source="{1: one}",
            input_format=InputFormat.YAML,
            language=Scheme(
                json_type=Scheme.json_types.GUILE_JSON,
            ),
            variable_form=NewVariable(name="my-data"),
        )


def test_scheme_json_type_rejects_special_float_nan() -> None:
    """Reject ``NaN`` since JSON has no syntax for it."""
    with pytest.raises(
        expected_exception=UnrepresentableSpecialFloatError,
        match="NaN or infinity",
    ):
        literalize(
            source="[NaN]",
            input_format=InputFormat.JSON5,
            language=Scheme(
                json_type=Scheme.json_types.GUILE_JSON,
            ),
            variable_form=NewVariable(name="my-data"),
        )


def test_scheme_json_type_rejects_special_float_infinity() -> None:
    """Reject ``Infinity`` since JSON has no syntax for it."""
    with pytest.raises(
        expected_exception=UnrepresentableSpecialFloatError,
        match="NaN or infinity",
    ):
        literalize(
            source="[Infinity]",
            input_format=InputFormat.JSON5,
            language=Scheme(
                json_type=Scheme.json_types.GUILE_JSON,
            ),
            variable_form=NewVariable(name="my-data"),
        )
