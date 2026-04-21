"""Unit tests for Rust's tagged-enum heterogeneous-value strategy.

Golden-file coverage for the main rendering paths (dict-mixed,
sibling-list, and sibling-dict heterogeneity) lives in
``tests/integration/cases/*/Rust_heterogeneous_strategy_tagged_enum*.rs``.
These unit tests cover the behaviors that don't fit the golden-file
workflow: error-raising on the default strategy, configurable enum
name, and the homogeneous-input no-op.
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
