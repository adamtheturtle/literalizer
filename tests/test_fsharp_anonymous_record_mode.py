"""Public API coverage for opt-in F# anonymous records."""

import pytest

from literalizer import (
    BothVariableForms,
    InputFormat,
    NewVariable,
    literalize,
    literalize_call,
)
from literalizer.exceptions import (
    HeterogeneousScalarCollectionError,
    UnrepresentableInputError,
)
from literalizer.languages import FSharp


def test_anonymous_record_mode_preserves_tagged_default() -> None:
    """The opt-in form must not change the existing default output."""
    source = '{"name": "Ada", "active": true, "scores": [1, 2, 3]}'
    default = literalize(
        source=source, input_format=InputFormat.JSON, language=FSharp()
    )
    native = literalize(
        source=source,
        input_format=InputFormat.JSON,
        language=FSharp(dict_format=FSharp.dict_formats.ANONYMOUS_RECORD),
        variable_form=NewVariable(name="my_data", modifiers=frozenset()),
        wrap_in_file=True,
    )
    assert "FMap" in default.code
    assert "type Val =" not in native.code
    assert 'name = "Ada"' in native.code
    assert "active = true" in native.code
    assert "scores = [" in native.code
    assert "1L" in native.code


@pytest.mark.parametrize(
    argnames=("source", "input_format", "message"),
    argvalues=[
        ('{"not-a-field": 1}', InputFormat.JSON, "field"),
        ('{"let": 1}', InputFormat.JSON, "field"),
        ("1: one\n", InputFormat.YAML, "field"),
        ("{}", InputFormat.JSON, "empty records"),
        ('{"x": null}', InputFormat.JSON, "NoneType"),
        ('[{"x": 1}, {"x": "one"}]', InputFormat.JSON, "uniform"),
        ('[{"x": 1}, {"y": 1}]', InputFormat.JSON, "uniform"),
        ("--- !!omap\n- a: 1\n", InputFormat.YAML, "ordered maps"),
        ("--- !!set\na:\n", InputFormat.YAML, "set"),
    ],
)
def test_anonymous_record_mode_rejects_unsupported_input(
    source: str, input_format: InputFormat, message: str
) -> None:
    """Invalid native shapes fail clearly instead of emitting bad F#."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError, match=message
    ):
        _ = literalize(
            source=source,
            input_format=input_format,
            language=FSharp(dict_format=FSharp.dict_formats.ANONYMOUS_RECORD),
        )


def test_anonymous_record_mode_conflicts_with_json_node() -> None:
    """The two independent representations cannot be selected together."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError, match="json_type"
    ):
        _ = literalize(
            source='{"x": 1}',
            input_format=InputFormat.JSON,
            language=FSharp(
                dict_format=FSharp.dict_formats.ANONYMOUS_RECORD,
                json_type=FSharp.json_types.SYSTEM_TEXT_JSON_NODE,
            ),
        )


def test_anonymous_record_mode_rejects_mixed_scalar_list() -> None:
    """Native F# lists cannot contain unrelated scalar types."""
    with pytest.raises(expected_exception=HeterogeneousScalarCollectionError):
        _ = literalize(
            source='[1, "hello"]',
            input_format=InputFormat.JSON,
            language=FSharp(dict_format=FSharp.dict_formats.ANONYMOUS_RECORD),
        )


def test_anonymous_record_mode_nested_list_fields() -> None:
    """Lists inside sibling records have the same inferred field type."""
    result = literalize(
        source='[{"scores": [1, 2]}, {"scores": [3, 4]}]',
        input_format=InputFormat.JSON,
        language=FSharp(dict_format=FSharp.dict_formats.ANONYMOUS_RECORD),
    )
    assert result.code.find("scores = [") != result.code.rfind("scores = [")


def test_anonymous_record_mode_formats_epoch_datetime() -> None:
    """Epoch values remain native ``int64`` fields."""
    result = literalize(
        source="event_time = 2024-01-15T12:30:00Z\n",
        input_format=InputFormat.TOML,
        language=FSharp(
            dict_format=FSharp.dict_formats.ANONYMOUS_RECORD,
            datetime_format=FSharp.datetime_formats.EPOCH,
        ),
    )
    assert "event_time = 1705321800L" in result.code


def test_anonymous_record_mode_call_argument() -> None:
    """Calls pass the anonymous record, not a ``Val`` constructor."""
    result = literalize_call(
        source='[[{"x": 1}]]',
        input_format=InputFormat.JSON,
        language=FSharp(dict_format=FSharp.dict_formats.ANONYMOUS_RECORD),
        target_function="consume",
        parameter_names=("item",),
        wrap_in_file=True,
    )
    assert "consume({| x = 1L |})" in result.code


def test_anonymous_record_mode_both_variable_forms() -> None:
    """Declaration and assignment both use the native expression."""
    result = literalize(
        source='{"x": 1}',
        input_format=InputFormat.JSON,
        language=FSharp(
            dict_format=FSharp.dict_formats.ANONYMOUS_RECORD,
            declaration_style=FSharp.declaration_styles.LET_MUTABLE,
        ),
        variable_form=BothVariableForms(name="my_data", modifiers=frozenset()),
        wrap_in_file=True,
    )
    assert "let mutable my_data = {|" in result.code
    assert "let my_data = {|" in result.code
