"""Opt-in ref-marker API behavior."""

from literalizer import (
    CollectionLayout,
    InputFormat,
    literalize,
    literalize_call,
)
from literalizer.languages import Python


def test_json_schema_ref_is_data_by_default() -> None:
    """The standard JSON Schema ``$ref`` key is not rewritten
    implicitly.
    """
    result = literalize(
        source='{"schema": {"$ref": "#/defs/Foo"}}',
        input_format=InputFormat.JSON,
        language=Python(),
    )

    assert '"$ref": "#/defs/Foo"' in result.code


def test_explicit_ref_key_enables_marker_rendering() -> None:
    """Callers can explicitly request the historical marker syntax."""
    result = literalize(
        source='{"schema": {"$ref": "foo"}}',
        input_format=InputFormat.JSON,
        language=Python(),
        ref_key="$ref",
    )

    assert '"schema": foo' in result.code


def test_explicit_ref_key_handles_nested_collections() -> None:
    """Opted-in refs remain active inside mappings and sequences."""
    result = literalize(
        source=(
            '{"mapping": {"value": {"\\u0024ref": "foo"}}, '
            '"items": [{"other": 1}, {"\\u0024ref": "foo"}]}'
        ),
        input_format=InputFormat.JSON,
        language=Python(),
        ref_key="$ref",
    )

    assert '"value": foo' in result.code
    assert '"items": ({"other": 1}, foo)' in result.code


def test_explicit_ref_key_handles_all_ref_nested_collections() -> None:
    """Collection inference remains valid when every child is a ref."""
    result = literalize(
        source=(
            '{"mapping": {"left": {"$ref": "foo"}}, '
            '"items": [{"$ref": "foo"}]}'
        ),
        input_format=InputFormat.JSON,
        language=Python(),
        ref_key="$ref",
    )

    assert '"left": foo' in result.code
    assert '"items": (foo,)' in result.code


def test_call_ref_key_handles_all_ref_argument_collections() -> None:
    """Call argument openers ignore ref markers during type inference."""
    result = literalize_call(
        source='[[[{"$ref": "foo"}], {"left": {"$ref": "foo"}}]]',
        input_format=InputFormat.JSON,
        language=Python(),
        target_function="consume",
        parameter_names=("items", "mapping"),
        ref_key="$ref",
    )

    assert 'consume(items=(foo,), mapping={"left": foo})' in result.code


def test_multiline_call_ref_openers_ignore_marker_children() -> None:
    """Multiline dict and sequence openers infer from non-ref children."""
    result = literalize_call(
        source=(
            '[[[{"other": 1}, {"\\u0024ref": "foo"}], '
            '{"left": {"\\u0024ref": "foo"}, "other": 1}]]'
        ),
        input_format=InputFormat.JSON,
        language=Python(),
        target_function="consume",
        parameter_names=("items", "mapping"),
        ref_key="$ref",
        collection_layout=CollectionLayout.MULTILINE,
    )

    assert "foo" in result.code
    assert '"other": 1' in result.code
