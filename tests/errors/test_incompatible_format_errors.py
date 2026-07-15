"""Rejection of declaration styles and modifiers that cannot accept the
value's rendered literal.

Each case pairs a constant-context declaration (Rust ``CONST`` /
``STATIC`` / ``LAZY_STATIC``, C# ``const``, Nim ``CONST``) or a typed
record component with a value whose only literal form is a runtime
constructor or a non-constant collection.  ``literalize`` raises
:class:`~literalizer.exceptions.IncompatibleFormatsError` (or, for the
placeholder formatter, :class:`NotImplementedError`) rather than emitting
output that fails to compile.  The integration framework only exercises
golden output that compiles, so these contracts have no golden-file
surface and need unit coverage.
"""

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
from literalizer.languages import CSharp, Java, Nim, Rust

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
            variable_form=NewVariable(name="my_var", modifiers=frozenset()),
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
            variable_form=NewVariable(name="my_var", modifiers=frozenset()),
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
            variable_form=NewVariable(name="my_var", modifiers=frozenset()),
        )


def test_rust_tuple_format_type_annotation_raises() -> None:
    """TUPLE.format_type_annotation raises for incompatible format."""
    with pytest.raises(expected_exception=IncompatibleFormatsError):
        Rust.sequence_formats.TUPLE.format_type_annotation(
            element_type="i32",
            length=2,
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


def test_java_record_non_array_sequence_raises() -> None:
    """Java ``RECORD`` rejects a non-ARRAY ``sequence_format``.

    A list-valued record component is typed from the array opener
    (``new <type>[]{``) the value formatter emits; ``LIST`` renders
    ``List.of(...)``, whose opener carries no element type, so the
    combination would emit a ``record`` that fails to compile and is
    rejected.
    """
    expected_msg = (
        "Java heterogeneous_strategy=RECORD requires "
        "sequence_format=ARRAY: a list-valued record component "
        "is typed from the array opener the value formatter "
        "emits, and other sequence formats (e.g. LIST -> "
        "List.of(...)) carry no element type. "
        "Use sequence_format=ARRAY."
    )
    java_record_list = Java(
        heterogeneous_strategy=Java.heterogeneous_strategies.RECORD,
        sequence_format=Java.sequence_formats.LIST,
    )
    with pytest.raises(
        expected_exception=IncompatibleFormatsError,
        match=f"^{re.escape(pattern=expected_msg)}$",
    ):
        literalize(
            source='{"name": "Alice", "scores": [1, 2, 3]}',
            input_format=InputFormat.JSON,
            language=java_record_list,
            pre_indent_level=0,
            include_delimiters=True,
            variable_form=NewVariable(name="my_var", modifiers=frozenset()),
        )
