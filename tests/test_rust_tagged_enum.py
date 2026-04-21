"""Tests for Rust's tagged-enum heterogeneous-value strategy."""

import textwrap

import pytest

from literalizer import InputFormat, NewVariable, literalize
from literalizer.exceptions import (
    HeterogeneousScalarCollectionError,
    HeterogeneousSiblingListsError,
)
from literalizer.languages import Rust

_TAGGED = Rust(
    heterogeneous_strategy=Rust.HeterogeneousStrategies.TAGGED_ENUM,
)


def test_default_strategy_is_error() -> None:
    """Default Rust spec still raises on heterogeneous scalars."""
    with pytest.raises(HeterogeneousScalarCollectionError):
        literalize(
            source='{"a": 1, "b": "x"}',
            input_format=InputFormat.JSON,
            language=Rust(),
        )


def test_dict_mixed_values_wraps_each_value() -> None:
    """A dict with mixed scalar values is rendered with each value
    wrapped in its tagged-enum variant.
    """
    result = literalize(
        source='{"type": "create", "pr_id": "pr_1", "draft": true}',
        input_format=InputFormat.JSON,
        language=_TAGGED,
        variable_form=NewVariable(name="my_data"),
        wrap_in_file=True,
    )
    assert "enum Value {" in result.code
    assert "Str(&'static str)" in result.code
    assert "Bool(bool)" in result.code
    assert 'Value::Str("create")' in result.code
    assert "Value::Bool(true)" in result.code


def test_list_mixed_elements_wraps_each_element() -> None:
    """A list with mixed scalar elements wraps each element."""
    result = literalize(
        source='[1, "a", true]',
        input_format=InputFormat.JSON,
        language=_TAGGED,
        wrap_in_file=True,
    )
    assert "Value::I32(1)" in result.code
    assert 'Value::Str("a")' in result.code
    assert "Value::Bool(true)" in result.code


def test_sibling_lists_wrap_inner_elements() -> None:
    """Sibling lists whose combined elements are heterogeneous have
    each inner list's scalar children wrapped.
    """
    result = literalize(
        source='[[1, 2], ["a", "b"]]',
        input_format=InputFormat.JSON,
        language=_TAGGED,
        wrap_in_file=True,
    )
    assert "Value::I32(1)" in result.code
    assert "Value::I32(2)" in result.code
    assert 'Value::Str("a")' in result.code
    assert 'Value::Str("b")' in result.code


def test_sibling_lists_still_error_without_opt_in() -> None:
    """Default Rust spec raises ``HeterogeneousSiblingListsError`` for
    sibling-list heterogeneity.
    """
    with pytest.raises(HeterogeneousSiblingListsError):
        literalize(
            source='[[1, 2], ["a", "b"]]',
            input_format=InputFormat.JSON,
            language=Rust(),
        )


def test_enum_contains_only_used_variants() -> None:
    """The emitted enum declares only the variants actually present
    in heterogeneous positions.
    """
    result = literalize(
        source='{"a": 1, "b": "x"}',
        input_format=InputFormat.JSON,
        language=_TAGGED,
        wrap_in_file=True,
    )
    assert "I32(i32)" in result.code
    assert "Str(&'static str)" in result.code
    # No other variants should appear.
    for unused in ("Bool(bool)", "F64(f64)", "I64(i64)", "I128(i128)", "Null"):
        assert unused not in result.code


def test_integer_variants_use_narrowest_width() -> None:
    """Integers that fit in i32 use ``I32``; larger values use ``I64``
    or ``I128`` as appropriate.
    """
    result = literalize(
        source='{"a": 1, "b": 3000000000, "c": "x"}',
        input_format=InputFormat.JSON,
        language=_TAGGED,
        wrap_in_file=True,
    )
    assert "I32(i32)" in result.code
    assert "I64(i64)" in result.code
    assert "Value::I32(1)" in result.code
    assert "Value::I64(3000000000i64)" in result.code


def test_configurable_enum_name() -> None:
    """The emitted enum's name comes from
    ``heterogeneous_value_enum_name``.
    """
    result = literalize(
        source='{"a": 1, "b": "x"}',
        input_format=InputFormat.JSON,
        language=Rust(
            heterogeneous_strategy=Rust.HeterogeneousStrategies.TAGGED_ENUM,
            heterogeneous_value_enum_name="JsonValue",
        ),
        wrap_in_file=True,
    )
    assert "enum JsonValue {" in result.code
    assert "JsonValue::I32(1)" in result.code
    assert 'JsonValue::Str("x")' in result.code
    assert "enum Value" not in result.code


def test_null_variant_has_no_payload() -> None:
    """The ``Null`` variant is emitted as a unit variant without
    parentheses.
    """
    result = literalize(
        source='{"a": 1, "b": null}',
        input_format=InputFormat.JSON,
        language=_TAGGED,
        wrap_in_file=True,
    )
    assert "    Null,\n" in result.code
    assert "Value::Null)" in result.code
    # Ensure no payload-form for Null.
    assert "Null(" not in result.code


def test_homogeneous_data_emits_no_enum() -> None:
    """Homogeneous data with tagged-enum opted in still emits no enum
    and no wrapping.
    """
    result = literalize(
        source='{"a": 1, "b": 2}',
        input_format=InputFormat.JSON,
        language=_TAGGED,
        wrap_in_file=True,
    )
    assert "enum Value" not in result.code
    assert "Value::" not in result.code


def test_float_variant() -> None:
    """Mixed scalars including a float emit an ``F64`` variant."""
    result = literalize(
        source='{"a": 1.5, "b": "x"}',
        input_format=InputFormat.JSON,
        language=_TAGGED,
        wrap_in_file=True,
    )
    assert "F64(f64)" in result.code
    assert "Value::F64(1.5)" in result.code


def test_nested_heterogeneous_dicts() -> None:
    """Heterogeneous dicts inside a homogeneous list of dicts render
    with only the inner dicts' values wrapped.
    """
    source = textwrap.dedent(
        """\
        - type: create
          pr_id: pr_1
          draft: true
        - type: create
          pr_id: pr_2
          draft: false
        """
    )
    result = literalize(
        source=source,
        input_format=InputFormat.YAML,
        language=_TAGGED,
        variable_form=NewVariable(name="events"),
        wrap_in_file=True,
    )
    assert 'Value::Str("create")' in result.code
    assert 'Value::Str("pr_1")' in result.code
    assert "Value::Bool(true)" in result.code
    assert "Value::Bool(false)" in result.code
