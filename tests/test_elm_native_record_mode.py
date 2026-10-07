"""Public API coverage for opt-in native Elm records."""

import pytest

from literalizer import InputFormat, NewVariable, literalize, literalize_call
from literalizer.exceptions import (
    HeterogeneousScalarCollectionError,
    UnrepresentableInputError,
)
from literalizer.languages import Elm


@pytest.mark.parametrize(
    argnames=("source", "input_format", "message"),
    argvalues=[
        ('{"not-a-field": 1}', InputFormat.JSON, "field"),
        ('{"if": 1}', InputFormat.JSON, "field"),
        ('{"Bad": 1}', InputFormat.JSON, "field"),
        ("1: one\n", InputFormat.YAML, "field"),
        ("{}", InputFormat.JSON, "empty records"),
        ('{"x": null}', InputFormat.JSON, "NoneType"),
        ('[{"x": 1}, {"x": "one"}]', InputFormat.JSON, "uniform"),
        ('[{"x": 1}, {"y": 1}]', InputFormat.JSON, "uniform"),
        ("--- !!omap\n- a: 1\n", InputFormat.YAML, "ordered maps"),
        ("--- !!set\na:\n", InputFormat.YAML, "set"),
    ],
)
def test_record_mode_rejects_unsupported_input(
    source: str, input_format: InputFormat, message: str
) -> None:
    """Unsupported shapes fail before emitting invalid Elm syntax."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError, match=message
    ):
        _ = literalize(
            source=source,
            input_format=input_format,
            language=Elm(dict_format=Elm.dict_formats.RECORD),
        )


def test_record_mode_conflicts_with_json_encode() -> None:
    """Native records and Json.Encode values are different representations."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError, match="json_type"
    ):
        _ = literalize(
            source='{"x": 1}',
            input_format=InputFormat.JSON,
            language=Elm(
                dict_format=Elm.dict_formats.RECORD,
                json_type=Elm.json_types.JSON_ENCODE_VALUE,
            ),
        )


def test_record_mode_rejects_mixed_scalar_list() -> None:
    """A native Elm list must infer one scalar element type."""
    with pytest.raises(expected_exception=HeterogeneousScalarCollectionError):
        _ = literalize(
            source='[1, "hello"]',
            input_format=InputFormat.JSON,
            language=Elm(dict_format=Elm.dict_formats.RECORD),
        )


def test_record_mode_call_argument() -> None:
    """Calls consume the native record expression, not ``Val``."""
    result = literalize_call(
        source='[[{"x": 1}]]',
        input_format=InputFormat.JSON,
        language=Elm(dict_format=Elm.dict_formats.RECORD),
        target_function="consume",
        parameter_names=("item",),
        wrap_in_file=True,
    )
    assert "consume ({ x = 1 })" in result.code


def test_record_mode_respects_custom_indent() -> None:
    """The closing record brace tracks the configured indent width."""
    result = literalize(
        source='{"name": "Ada"}',
        input_format=InputFormat.JSON,
        language=Elm(dict_format=Elm.dict_formats.RECORD, indent="  "),
        variable_form=NewVariable(name="my_data", modifiers=frozenset()),
        wrap_in_file=True,
    )
    assert "\n  }" in result.code
