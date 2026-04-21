"""Unit tests for Rust's tagged-enum heterogeneous-value strategy.

Golden-file coverage for the main rendering paths (dict-mixed,
sibling-list, and sibling-dict heterogeneity) lives in
``tests/integration/cases/*/Rust_heterogeneous_strategy_tagged_enum*.rs``.
These unit tests cover the behaviors that don't fit the golden-file
workflow: error-raising on the default strategy, and variant-set
shaping (integer widths, enum name, null payload, homogeneous no-op).
"""

import pytest

from literalizer import InputFormat, literalize
from literalizer.exceptions import (
    HeterogeneousScalarCollectionError,
    HeterogeneousSiblingListsError,
)
from literalizer.languages import Rust

_TAGGED = Rust(
    heterogeneous_strategy=Rust.heterogeneous_strategies.TAGGED_ENUM,
)


def test_default_strategy_is_error() -> None:
    """Default Rust spec still raises on heterogeneous scalars."""
    with pytest.raises(expected_exception=HeterogeneousScalarCollectionError):
        literalize(
            source='{"a": 1, "b": "x"}',
            input_format=InputFormat.JSON,
            language=Rust(),
        )


def test_sibling_lists_still_error_without_opt_in() -> None:
    """Default Rust spec raises ``HeterogeneousSiblingListsError`` for
    sibling-list heterogeneity.
    """
    with pytest.raises(expected_exception=HeterogeneousSiblingListsError):
        literalize(
            source='[[1, 2], ["a", "b"]]',
            input_format=InputFormat.JSON,
            language=Rust(),
        )


def test_enum_contains_only_used_variants() -> None:
    """The emitted enum declares only the variants actually present in
    heterogeneous positions — here, only ``I32`` and ``Str``.
    """
    result = literalize(
        source='{"a": 1, "b": "x"}',
        input_format=InputFormat.JSON,
        language=_TAGGED,
        wrap_in_file=True,
    )
    expected = (
        "use std::collections::HashMap;\n"
        "enum Value {\n"
        "    I32(i32),\n"
        "    Str(&'static str),\n"
        "}\n"
        "fn main() {\n"
        "    HashMap::from([\n"
        '        ("a", Value::I32(1)),\n'
        '        ("b", Value::Str("x")),\n'
        "    ])\n"
        "}"
    )
    assert result.code == expected


def test_integer_variants_use_narrowest_width() -> None:
    """Integers that fit in i32 use ``I32``; larger values use ``I64``."""
    result = literalize(
        source='{"a": 1, "b": 3000000000, "c": "x"}',
        input_format=InputFormat.JSON,
        language=_TAGGED,
        wrap_in_file=True,
    )
    expected = (
        "use std::collections::HashMap;\n"
        "enum Value {\n"
        "    I32(i32),\n"
        "    I64(i64),\n"
        "    Str(&'static str),\n"
        "}\n"
        "fn main() {\n"
        "    HashMap::from([\n"
        '        ("a", Value::I32(1)),\n'
        '        ("b", Value::I64(3000000000i64)),\n'
        '        ("c", Value::Str("x")),\n'
        "    ])\n"
        "}"
    )
    assert result.code == expected


def test_configurable_enum_name() -> None:
    """The emitted enum name comes from the
    ``heterogeneous_value_enum_name`` constructor argument.
    """
    result = literalize(
        source='{"a": 1, "b": "x"}',
        input_format=InputFormat.JSON,
        language=Rust(
            heterogeneous_strategy=Rust.heterogeneous_strategies.TAGGED_ENUM,
            heterogeneous_value_enum_name="JsonValue",
        ),
        wrap_in_file=True,
    )
    expected = (
        "use std::collections::HashMap;\n"
        "enum JsonValue {\n"
        "    I32(i32),\n"
        "    Str(&'static str),\n"
        "}\n"
        "fn main() {\n"
        "    HashMap::from([\n"
        '        ("a", JsonValue::I32(1)),\n'
        '        ("b", JsonValue::Str("x")),\n'
        "    ])\n"
        "}"
    )
    assert result.code == expected


def test_null_variant_has_no_payload() -> None:
    """The ``Null`` variant is emitted as a unit variant without
    parentheses; callers use it as ``Value::Null``.
    """
    result = literalize(
        source='{"a": 1, "b": null}',
        input_format=InputFormat.JSON,
        language=_TAGGED,
        wrap_in_file=True,
    )
    expected = (
        "use std::collections::HashMap;\n"
        "enum Value {\n"
        "    I32(i32),\n"
        "    Null,\n"
        "}\n"
        "fn main() {\n"
        "    HashMap::from([\n"
        '        ("a", Value::I32(1)),\n'
        '        ("b", Value::Null),\n'
        "    ])\n"
        "}"
    )
    assert result.code == expected


def test_homogeneous_data_emits_no_enum() -> None:
    """Opting into the tagged-enum strategy is a no-op when the data
    contains no heterogeneous collections.
    """
    result = literalize(
        source='{"a": 1, "b": 2}',
        input_format=InputFormat.JSON,
        language=_TAGGED,
        wrap_in_file=True,
    )
    expected = (
        "use std::collections::HashMap;\n"
        "fn main() {\n"
        "    HashMap::from([\n"
        '        ("a", 1),\n'
        '        ("b", 2),\n'
        "    ])\n"
        "}"
    )
    assert result.code == expected


def test_float_variant() -> None:
    """Mixed scalars including a float emit an ``F64`` variant."""
    result = literalize(
        source='{"a": 1.5, "b": "x"}',
        input_format=InputFormat.JSON,
        language=_TAGGED,
        wrap_in_file=True,
    )
    expected = (
        "use std::collections::HashMap;\n"
        "enum Value {\n"
        "    F64(f64),\n"
        "    Str(&'static str),\n"
        "}\n"
        "fn main() {\n"
        "    HashMap::from([\n"
        '        ("a", Value::F64(1.5)),\n'
        '        ("b", Value::Str("x")),\n'
        "    ])\n"
        "}"
    )
    assert result.code == expected


def test_date_variants() -> None:
    """Mixing a date with other scalar types emits a ``Date`` variant
    carrying the format's produced Rust type.
    """
    source = 'a: 2024-01-15\nb: "x"\n'
    result = literalize(
        source=source,
        input_format=InputFormat.YAML,
        language=_TAGGED,
        wrap_in_file=True,
    )
    expected = (
        "use chrono::NaiveDate;\n"
        "use std::collections::HashMap;\n"
        "enum Value {\n"
        "    Date(NaiveDate),\n"
        "    Str(&'static str),\n"
        "}\n"
        "fn main() {\n"
        "    HashMap::from([\n"
        '        ("a", Value::Date('
        "NaiveDate::from_ymd_opt(2024, 1, 15).unwrap())),\n"
        '        ("b", Value::Str("x")),\n'
        "    ])\n"
        "}"
    )
    assert result.code == expected


def test_datetime_variants() -> None:
    """Mixing a datetime with other scalar types emits a ``DateTime``
    variant carrying the format's produced Rust type.
    """
    source = 'a: 2024-01-15T12:30:00\nb: "x"\n'
    result = literalize(
        source=source,
        input_format=InputFormat.YAML,
        language=_TAGGED,
        wrap_in_file=True,
    )
    expected = (
        "use chrono::NaiveDate;\n"
        "use chrono::NaiveDateTime;\n"
        "use chrono::NaiveTime;\n"
        "use std::collections::HashMap;\n"
        "enum Value {\n"
        "    DateTime(NaiveDateTime),\n"
        "    Str(&'static str),\n"
        "}\n"
        "fn main() {\n"
        "    HashMap::from([\n"
        '        ("a", Value::DateTime(NaiveDateTime::new('
        "NaiveDate::from_ymd_opt(2024, 1, 15).unwrap(), "
        "NaiveTime::from_hms_opt(12, 30, 0).unwrap()))),\n"
        '        ("b", Value::Str("x")),\n'
        "    ])\n"
        "}"
    )
    assert result.code == expected


def test_bytes_variant() -> None:
    """Mixing bytes with other scalar types emits a ``Bytes`` variant."""
    source = "a: !!binary SGVsbG8=\nb: 1\n"
    result = literalize(
        source=source,
        input_format=InputFormat.YAML,
        language=_TAGGED,
        wrap_in_file=True,
    )
    expected = (
        "use std::collections::HashMap;\n"
        "enum Value {\n"
        "    Bytes(&'static str),\n"
        "    I32(i32),\n"
        "}\n"
        "fn main() {\n"
        "    HashMap::from([\n"
        '        ("a", Value::Bytes("48656c6c6f")),\n'
        '        ("b", Value::I32(1)),\n'
        "    ])\n"
        "}"
    )
    assert result.code == expected


def test_nested_dict_with_flagged_inner_dict() -> None:
    """An outer dict whose value is a flagged inner dict wraps only
    the inner scalars; the outer dict is untouched.
    """
    result = literalize(
        source='{"outer": {"a": 1, "b": "x"}}',
        input_format=InputFormat.JSON,
        language=_TAGGED,
        wrap_in_file=True,
    )
    expected = (
        "use std::collections::HashMap;\n"
        "enum Value {\n"
        "    I32(i32),\n"
        "    Str(&'static str),\n"
        "}\n"
        "fn main() {\n"
        "    HashMap::from([\n"
        '        ("outer", HashMap::from(['
        '("a", Value::I32(1)), ("b", Value::Str("x"))])),\n'
        "    ])\n"
        "}"
    )
    assert result.code == expected


def test_homogeneous_sibling_lists_emit_no_enum() -> None:
    """Sibling lists whose combined scalars are homogeneous are a
    no-op under the tagged-enum strategy (no enum declared, no
    wrapping).
    """
    result = literalize(
        source="[[1, 2], [3, 4]]",
        input_format=InputFormat.JSON,
        language=_TAGGED,
        wrap_in_file=True,
    )
    expected = (
        "fn main() {\n"
        "    vec![\n"
        "        vec![1, 2],\n"
        "        vec![3, 4],\n"
        "    ]\n"
        "}"
    )
    assert result.code == expected
