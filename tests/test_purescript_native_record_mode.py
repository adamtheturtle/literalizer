"""Public API coverage for opt-in PureScript records."""

import pytest

from literalizer import InputFormat, NewVariable, literalize, literalize_call
from literalizer.exceptions import (
    HeterogeneousScalarCollectionError,
    UnrepresentableInputError,
    UnrepresentableIntegerError,
)
from literalizer.languages import PureScript


def test_record_mode_preserves_tagged_default() -> None:
    """The native option does not alter the default ``Val`` output."""
    source = '{"name": "Ada", "active": true, "scores": [1, 2, 3]}'
    default = literalize(
        source=source, input_format=InputFormat.JSON, language=PureScript()
    )
    native = literalize(
        source=source,
        input_format=InputFormat.JSON,
        language=PureScript(dict_format=PureScript.dict_formats.RECORD),
        variable_form=NewVariable(name="my_data", modifiers=frozenset()),
        wrap_in_file=True,
    )
    assert "PDict" in default.code
    assert "data Val" not in native.code
    assert 'name: "Ada"' in native.code
    assert "active: true" in native.code
    assert "scores: [" in native.code


@pytest.mark.parametrize(
    argnames=("source", "input_format", "message"),
    argvalues=[
        ('{"not-a-field": 1}', InputFormat.JSON, "field"),
        ('{"case": 1}', InputFormat.JSON, "field"),
        ('{"Bad": 1}', InputFormat.JSON, "field"),
        ("1: one\n", InputFormat.YAML, "field"),
        ("{}", InputFormat.JSON, "empty records"),
        ('{"x": null}', InputFormat.JSON, "NoneType"),
        ('[{"x": 1}, {"x": "one"}]', InputFormat.JSON, "uniform"),
        ('[{"x": 1}, {"y": 1}]', InputFormat.JSON, "uniform"),
        ("[1, 2147483648]", InputFormat.JSON, "integer widths"),
        ("--- !!omap\n- a: 1\n", InputFormat.YAML, "ordered maps"),
        ("--- !!set\na:\n", InputFormat.YAML, "set"),
    ],
)
def test_record_mode_rejects_unsupported_input(
    source: str, input_format: InputFormat, message: str
) -> None:
    """Unsupported shapes fail before producing invalid code."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError, match=message
    ):
        _ = literalize(
            source=source,
            input_format=input_format,
            language=PureScript(dict_format=PureScript.dict_formats.RECORD),
        )


def test_record_mode_conflicts_with_argonaut() -> None:
    """Native records and dynamic Argonaut values cannot be combined."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError, match="json_type"
    ):
        _ = literalize(
            source='{"x": 1}',
            input_format=InputFormat.JSON,
            language=PureScript(
                dict_format=PureScript.dict_formats.RECORD,
                json_type=PureScript.json_types.ARGONAUT_JSON,
            ),
        )


def test_record_mode_rejects_mixed_scalar_array() -> None:
    """A native array cannot infer both Int and String elements."""
    with pytest.raises(expected_exception=HeterogeneousScalarCollectionError):
        _ = literalize(
            source='[1, "hello"]',
            input_format=InputFormat.JSON,
            language=PureScript(dict_format=PureScript.dict_formats.RECORD),
        )


def test_record_mode_nested_array_fields() -> None:
    """Sibling records with matching array field types infer one row."""
    result = literalize(
        source='[{"scores": [1, 2]}, {"scores": [3, 4]}]',
        input_format=InputFormat.JSON,
        language=PureScript(dict_format=PureScript.dict_formats.RECORD),
    )
    assert result.code.find("scores: [") != result.code.rfind("scores: [")


def test_record_mode_boolean_fields_in_record_array() -> None:
    """Boolean fields share one inferred record type across siblings."""
    result = literalize(
        source='[{"active": true}, {"active": false}]',
        input_format=InputFormat.JSON,
        language=PureScript(dict_format=PureScript.dict_formats.RECORD),
    )
    assert "active: true" in result.code
    assert "active: false" in result.code


def test_record_mode_formats_epoch_datetime() -> None:
    """Epoch timestamps become bare native numbers."""
    result = literalize(
        source="event_time = 2024-01-15T12:30:00Z\n",
        input_format=InputFormat.TOML,
        language=PureScript(
            dict_format=PureScript.dict_formats.RECORD,
            datetime_format=PureScript.datetime_formats.EPOCH,
        ),
    )
    assert "event_time: 1705321800" in result.code


def test_record_mode_formats_base64_bytes() -> None:
    """The alternate bytes option remains a bare String field."""
    result = literalize(
        source="---\npayload: !!binary YWJj\n",
        input_format=InputFormat.YAML,
        language=PureScript(
            dict_format=PureScript.dict_formats.RECORD,
            bytes_format=PureScript.bytes_formats.BASE64,
        ),
    )
    assert 'payload: "YWJj"' in result.code


def test_record_mode_formats_large_integer_as_number() -> None:
    """Values beyond Int32 use an exact Number literal."""
    result = literalize(
        source='{"value": 2147483648}',
        input_format=InputFormat.JSON,
        language=PureScript(dict_format=PureScript.dict_formats.RECORD),
    )
    assert "value: 2147483648.0" in result.code


def test_record_mode_rejects_integer_beyond_number_precision() -> None:
    """Avoid silently rounding beyond the safe integer range."""
    with pytest.raises(expected_exception=UnrepresentableIntegerError):
        _ = literalize(
            source='{"value": 9007199254740993}',
            input_format=InputFormat.JSON,
            language=PureScript(dict_format=PureScript.dict_formats.RECORD),
        )


def test_record_mode_call_argument() -> None:
    """Calls receive a native record rather than a ``Val`` constructor."""
    result = literalize_call(
        source='[[{"x": 1}]]',
        input_format=InputFormat.JSON,
        language=PureScript(dict_format=PureScript.dict_formats.RECORD),
        target_function="consume",
        parameter_names=("item",),
        wrap_in_file=True,
    )
    assert "consume ({ x: 1 })" in result.code
