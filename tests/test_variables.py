"""Tests for variable declaration and assignment in literalizer
converter.
"""

import datetime
import re

import pytest

from literalizer import (
    InputFormat,
    NewVariable,
    literalize,
)
from literalizer.exceptions import (
    IncompatibleFormatsError,
)
from literalizer.languages import CSharp, Nim, Rust

RUST_CONST = Rust(
    date_format=Rust.date_formats.ISO,
    datetime_format=Rust.datetime_formats.ISO,
    bytes_format=Rust.bytes_formats.HEX,
    sequence_format=Rust.sequence_formats.ARRAY,
    declaration_style=Rust.declaration_styles.CONST,
)


def test_rust_const_dict_raises() -> None:
    """Rust CONST rejects dict data — ``HashMap::from`` is not a const
    expression, and Rust has no const-compatible dict format.
    """
    with pytest.raises(expected_exception=IncompatibleFormatsError):
        literalize(
            source='{"a": "b"}',
            input_format=InputFormat.JSON,
            language=RUST_CONST,
            pre_indent_level=0,
            include_delimiters=True,
            variable_form=NewVariable(name="my_var"),
        )


def test_rust_const_empty_dict_raises() -> None:
    """Rust CONST rejects empty dict data for the same reason."""
    with pytest.raises(expected_exception=IncompatibleFormatsError):
        literalize(
            source="{}",
            input_format=InputFormat.JSON,
            language=RUST_CONST,
            pre_indent_level=0,
            include_delimiters=True,
            variable_form=NewVariable(name="my_var"),
        )


def test_rust_const_btree_map_raises() -> None:
    """Rust CONST rejects dict data with ``BTREE_MAP`` too —
    ``BTreeMap::from``
    is equally non-const.
    """
    rust_btree_map = Rust(
        date_format=Rust.date_formats.ISO,
        datetime_format=Rust.datetime_formats.ISO,
        bytes_format=Rust.bytes_formats.HEX,
        sequence_format=Rust.sequence_formats.ARRAY,
        dict_format=Rust.dict_formats.BTREE_MAP,
        declaration_style=Rust.declaration_styles.CONST,
    )
    with pytest.raises(expected_exception=IncompatibleFormatsError):
        literalize(
            source='{"a": "b"}',
            input_format=InputFormat.JSON,
            language=rust_btree_map,
            pre_indent_level=0,
            include_delimiters=True,
            variable_form=NewVariable(name="my_var"),
        )


def test_rust_tuple_format_type_annotation_raises() -> None:
    """TUPLE.format_type_annotation raises for incompatible format."""
    with pytest.raises(expected_exception=IncompatibleFormatsError):
        Rust.sequence_formats.TUPLE.format_type_annotation(
            element_type="i32",
            length=2,
        )


def test_rust_static_single_element_tuple_annotation_has_comma() -> None:
    """Single-element tuple annotations include the required comma."""
    rust = Rust(
        declaration_style=Rust.declaration_styles.STATIC,
        sequence_format=Rust.sequence_formats.TUPLE,
    )
    result = literalize(
        source="[1]",
        input_format=InputFormat.JSON,
        language=rust,
        variable_form=NewVariable(name="DATA"),
    )

    assert result.code == ("static DATA: (i32,) = (\n    1,\n);")


def test_rust_tagged_enum_epoch_datetime_uses_integer_variant() -> None:
    """Epoch datetime variants use the configured integer type."""
    rust = Rust(
        datetime_format=Rust.datetime_formats.EPOCH,
        heterogeneous_strategy=Rust.heterogeneous_strategies.TAGGED_ENUM,
    )
    timestamp = datetime.datetime(
        year=2024,
        month=1,
        day=1,
        tzinfo=datetime.UTC,
    )
    result = literalize(
        source=f"- {timestamp.isoformat()}\n- 1\n",
        input_format=InputFormat.YAML,
        language=rust,
        variable_form=None,
    )

    assert result.preamble == (
        "enum Value {",
        "    I64(i64),",
        "    I32(i32),",
        "}",
    )
    assert result.code == (
        "vec![\n    Value::I64(1704067200),\n    Value::I32(1),\n]"
    )


def test_rust_const_vec_raises() -> None:
    """Rust CONST with vector format raises."""
    expected_msg = (
        "Rust CONST requires a constant-expression initializer, "
        "but the VEC sequence format produces vec![…] which is "
        "not a constant expression. Use ARRAY or TUPLE instead."
    )
    with pytest.raises(
        expected_exception=IncompatibleFormatsError,
        match=f"^{re.escape(pattern=expected_msg)}$",
    ):
        Rust(
            declaration_style=Rust.declaration_styles.CONST,
            sequence_format=Rust.sequence_formats.VEC,
        )


def test_rust_static_vec_raises() -> None:
    """Rust STATIC with vector format raises."""
    expected_msg = (
        "Rust STATIC requires a constant-expression initializer, "
        "but the VEC sequence format produces vec![…] which is "
        "not a constant expression. Use ARRAY or TUPLE instead."
    )
    with pytest.raises(
        expected_exception=IncompatibleFormatsError,
        match=f"^{re.escape(pattern=expected_msg)}$",
    ):
        Rust(
            declaration_style=Rust.declaration_styles.STATIC,
            sequence_format=Rust.sequence_formats.VEC,
        )


def test_rust_lazy_static_config_formatter_raises_if_called_directly() -> None:
    """The LAZY_STATIC ``DeclarationStyleConfig`` formatter is a
    placeholder.

    The real formatter is built by
    :meth:`Rust.DeclarationStyles.build_formatter`; calling the
    stored one directly would silently emit invalid Rust, so it
    raises instead.
    """
    style = Rust.declaration_styles.LAZY_STATIC
    with pytest.raises(expected_exception=NotImplementedError):
        style.value.formatter("x", "v", None, frozenset())


@pytest.mark.parametrize(
    argnames="source",
    argvalues=[
        "[1, 2, 3]",
        "{a: 1}",
        "!!set {1, 2}",
        "2024-01-15",
        "2024-01-15T12:30:00Z",
    ],
    ids=["list", "dict", "set", "date", "datetime"],
)
def test_csharp_const_with_non_constant_raises(source: str) -> None:
    """C# ``const`` combined with a non-constant value raises.

    C# ``const`` requires a compile-time constant expression, which
    collection literals (list, dict, set) and date/datetime values
    are not.
    """
    expected_msg = (
        "C# 'const' requires a compile-time constant initializer, "
        "but collection and date/datetime literals are not constant "
        "expressions. Use 'readonly' or remove the 'const' modifier."
    )
    with pytest.raises(
        expected_exception=IncompatibleFormatsError,
        match=f"^{re.escape(pattern=expected_msg)}$",
    ):
        literalize(
            source=source,
            input_format=InputFormat.YAML,
            language=CSharp(),
            pre_indent_level=0,
            include_delimiters=True,
            variable_form=NewVariable(
                name="my_data",
                modifiers=frozenset({CSharp.modifiers.CONST}),
            ),
            wrap_in_file=True,
        )


def test_nim_object_variant_const_raises() -> None:
    """Nim ``CONST`` rejects the ``OBJECT_VARIANT`` strategy.

    ``OBJECT_VARIANT`` renders dicts as ``{…}.toTable`` and sequences
    as ``@[…]``, both of which are runtime constructors and cannot
    initialize a ``const`` declaration.
    """
    expected_msg = (
        "Nim CONST requires a constant-expression initializer, "
        "but OBJECT_VARIANT produces runtime .toTable / @[] calls "
        "which are not constant expressions. Use VAR or LET instead."
    )
    with pytest.raises(
        expected_exception=IncompatibleFormatsError,
        match=f"^{re.escape(pattern=expected_msg)}$",
    ):
        Nim(
            heterogeneous_strategy=(
                Nim.heterogeneous_strategies.OBJECT_VARIANT
            ),
            declaration_style=Nim.declaration_styles.CONST,
        )
