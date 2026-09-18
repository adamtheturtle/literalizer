"""Public API coverage for opt-in native Elm records."""

import pytest

from literalizer import InputFormat, NewVariable, literalize, literalize_call
from literalizer.exceptions import (
    HeterogeneousScalarCollectionError,
    UnrepresentableInputError,
)
from literalizer.languages import Elm


def test_record_mode_preserves_tagged_default() -> None:
    """Selecting native records does not change the default ``Val``
    form.
    """
    source = '{"name": "Ada", "active": true, "scores": [1, 2, 3]}'
    default = literalize(
        source=source, input_format=InputFormat.JSON, language=Elm()
    )
    native = literalize(
        source=source,
        input_format=InputFormat.JSON,
        language=Elm(dict_format=Elm.dict_formats.RECORD),
        variable_form=NewVariable(name="my_data", modifiers=frozenset()),
        wrap_in_file=True,
    )
    assert "EDict" in default.code
    assert "type Val" not in native.code
    assert 'name = "Ada"' in native.code
    assert "active = True" in native.code
    assert "scores = [" in native.code


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


def test_record_mode_nested_list_fields() -> None:
    """List-valued fields agree across sibling records."""
    result = literalize(
        source='[{"scores": [1, 2]}, {"scores": [3, 4]}]',
        input_format=InputFormat.JSON,
        language=Elm(dict_format=Elm.dict_formats.RECORD),
    )
    assert result.code.find("scores = [") != result.code.rfind("scores = [")


def test_record_mode_formats_epoch_datetime() -> None:
    """Epoch timestamps become bare Elm integers."""
    result = literalize(
        source="event_time = 2024-01-15T12:30:00Z\n",
        input_format=InputFormat.TOML,
        language=Elm(
            dict_format=Elm.dict_formats.RECORD,
            datetime_format=Elm.datetime_formats.EPOCH,
        ),
    )
    assert "event_time = 1705321800" in result.code


def test_record_mode_formats_base64_bytes() -> None:
    """The alternate bytes option still yields a bare string field."""
    result = literalize(
        source="---\npayload: !!binary YWJj\n",
        input_format=InputFormat.YAML,
        language=Elm(
            dict_format=Elm.dict_formats.RECORD,
            bytes_format=Elm.bytes_formats.BASE64,
        ),
    )
    assert 'payload = "YWJj"' in result.code


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
