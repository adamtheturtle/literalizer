"""Tests for variable declaration and assignment in literalizer
converter.
"""

import re
import textwrap

import pytest

from literalizer import (
    InputFormat,
    NewVariable,
    literalize,
)
from literalizer.exceptions import (
    IncompatibleFormatsError,
    VariableNamesNotSupportedByLanguageError,
)
from literalizer.languages import CSharp, Nim, Python, Rust, Yaml

PYTHON_ALWAYS_HINTS = Python(
    date_format=Python.date_formats.PYTHON,
    datetime_format=Python.datetime_formats.PYTHON,
    bytes_format=Python.bytes_formats.HEX,
    sequence_format=Python.sequence_formats.TUPLE,
    set_format=Python.set_formats.SET,
    variable_type_hints=Python.variable_type_hints_formats.ALWAYS,
)


def test_python_always_type_hints_set_with_colon_in_string() -> None:
    """A set element containing ``": `` is not misidentified as a dict."""
    yaml_string = "!!set\n? 'a\": b'\n"
    result = literalize(
        source=yaml_string,
        input_format=InputFormat.YAML,
        language=PYTHON_ALWAYS_HINTS,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=NewVariable(name="my_var"),
    )
    expected = textwrap.dedent(
        text="""\
        my_var: set[str] = {
            "a\\": b",
        }"""
    )
    assert result.code == expected


def test_python_always_type_hints_dict_with_uniform_list_values() -> None:
    """Dict whose values are all lists collapses to a single value type
    (no union), distinct from the mixed-value path covered by the
    ``dict_with_list_value`` golden.
    """
    result = literalize(
        source='{"key": [1, 2, 3]}',
        input_format=InputFormat.JSON,
        language=PYTHON_ALWAYS_HINTS,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=NewVariable(name="my_var"),
    )
    expected = textwrap.dedent(
        text="""\
        my_var: dict[str, tuple[int, ...]] = {
            "key": (1, 2, 3),
        }"""
    )
    assert result.code == expected


def test_python_always_type_hints_ordered_dicts_in_sequence() -> None:
    """Multiple OrderedDicts in a sequence merge value types into one
    hint.  OrderedDict value-merging uses a separate code path from
    plain dict value-merging, so the ``mixed_type_dicts_in_sequence``
    golden does not cover it.
    """
    yaml_input = textwrap.dedent(
        text="""\
        ---
        - !!omap
          - name: Alice
          - draft: true
        - !!omap
          - name: Bob"""
    )
    result = literalize(
        source=yaml_input,
        input_format=InputFormat.YAML,
        language=PYTHON_ALWAYS_HINTS,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=NewVariable(name="my_var"),
    )
    expected = textwrap.dedent(
        text="""\
        my_var: tuple[OrderedDict[str, str | bool], ...] = (
            OrderedDict([("name", "Alice"), ("draft", True)]),
            OrderedDict([("name", "Bob")]),
        )""",
    )
    assert result.code == expected


RUST_CONST = Rust(
    date_format=Rust.date_formats.ISO,
    datetime_format=Rust.datetime_formats.ISO,
    bytes_format=Rust.bytes_formats.HEX,
    sequence_format=Rust.sequence_formats.ARRAY,
    declaration_style=Rust.declaration_styles.CONST,
)


def test_rust_const_single_element_tuple() -> None:
    """Rust CONST single-element tuple has trailing comma in type."""
    rust_tuple = Rust(
        date_format=Rust.date_formats.ISO,
        datetime_format=Rust.datetime_formats.ISO,
        bytes_format=Rust.bytes_formats.HEX,
        sequence_format=Rust.sequence_formats.TUPLE,
        declaration_style=Rust.declaration_styles.CONST,
    )
    result = literalize(
        source="[42]",
        input_format=InputFormat.JSON,
        language=rust_tuple,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=NewVariable(name="my_var"),
    )
    expected = textwrap.dedent(
        text="""\
        const my_var: (i32,) = (
            42,
        );"""
    )
    assert result.code == expected


def test_rust_const_set() -> None:
    """Rust CONST with set produces ``HashSet`` type annotation."""
    yaml_input = "!!set\n? a\n? b\n"
    result = literalize(
        source=yaml_input,
        input_format=InputFormat.YAML,
        language=RUST_CONST,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=NewVariable(name="my_var"),
    )
    expected = textwrap.dedent(
        text="""\
        const my_var: HashSet<&str> = HashSet::from([
            "a",
            "b",
        ]);"""
    )
    assert result.code == expected


def test_rust_const_empty_set() -> None:
    """Rust CONST with empty set uses default element type."""
    yaml_input = "!!set {}"
    result = literalize(
        source=yaml_input,
        input_format=InputFormat.YAML,
        language=RUST_CONST,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=NewVariable(name="my_var"),
    )
    assert result.code == (
        "const my_var: HashSet<String> = HashSet::<String>::new();"
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


def test_rust_const_btree_set() -> None:
    """Rust CONST with ``BTREE_SET`` uses ``BTreeSet`` type annotation."""
    rust_btree_set = Rust(
        date_format=Rust.date_formats.ISO,
        datetime_format=Rust.datetime_formats.ISO,
        bytes_format=Rust.bytes_formats.HEX,
        sequence_format=Rust.sequence_formats.ARRAY,
        set_format=Rust.set_formats.BTREE_SET,
        declaration_style=Rust.declaration_styles.CONST,
    )
    result = literalize(
        source="!!set\n? a\n? b\n",
        input_format=InputFormat.YAML,
        language=rust_btree_set,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=NewVariable(name="my_var"),
    )
    expected = textwrap.dedent(
        text="""\
        const my_var: BTreeSet<&str> = BTreeSet::from([
            "a",
            "b",
        ]);"""
    )
    assert result.code == expected


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


def test_rust_const_widened_int_array() -> None:
    """Rust CONST with mixed-size integers widens to the largest type."""
    result = literalize(
        source="[1, 2147483648]",
        input_format=InputFormat.JSON,
        language=RUST_CONST,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=NewVariable(name="my_var"),
    )
    expected = textwrap.dedent(
        text="""\
        const my_var: [i64; 2] = [
            1,
            2147483648i64,
        ];"""
    )
    assert result.code == expected


def test_rust_const_i128_array() -> None:
    """Rust CONST with an integer exceeding i64 range uses i128."""
    result = literalize(
        source="[9223372036854775808]",
        input_format=InputFormat.JSON,
        language=RUST_CONST,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=NewVariable(name="my_var"),
    )
    expected = textwrap.dedent(
        text="""\
        const my_var: [i128; 1] = [
            9223372036854775808i128,
        ];"""
    )
    assert result.code == expected


def test_rust_const_nested_list() -> None:
    """Rust CONST with nested list produces recursive type."""
    result = literalize(
        source="[[1, 2], [3, 4]]",
        input_format=InputFormat.JSON,
        language=RUST_CONST,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=NewVariable(name="my_var"),
    )
    expected = textwrap.dedent(
        text="""\
        const my_var: [[i32; 2]; 2] = [
            [1, 2],
            [3, 4],
        ];"""
    )
    assert result.code == expected


def test_rust_tuple_format_type_annotation_raises() -> None:
    """TUPLE.format_type_annotation raises for incompatible format."""
    with pytest.raises(expected_exception=IncompatibleFormatsError):
        Rust.sequence_formats.TUPLE.format_type_annotation(
            element_type="i32",
            length=2,
        )


def test_rust_vec_format_type_annotation() -> None:
    """``format_type_annotation`` returns ``Vec<T>`` for vector format."""
    result = Rust.sequence_formats.VEC.format_type_annotation(
        element_type="i32",
        length=3,
    )
    assert result == "Vec<i32>"


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


RUST_LAZY_STATIC = Rust(
    date_format=Rust.date_formats.ISO,
    datetime_format=Rust.datetime_formats.ISO,
    bytes_format=Rust.bytes_formats.HEX,
    declaration_style=Rust.declaration_styles.LAZY_STATIC,
)


def test_rust_lazy_static_set() -> None:
    """Rust LAZY_STATIC with a set wraps ``HashSet`` in ``LazyLock``.

    The integration matrix pairs ``declaration_style`` with the
    ``set`` case only for ``LAZY_STATIC`` / ``LET_MUT`` via this
    unit test because Rust ``CONST`` / ``STATIC`` combined with
    ``HashSet::from`` produces non-const code that does not compile,
    a pre-existing limitation outside the scope of this change.
    """
    result = literalize(
        source="!!set\n? a\n? b\n",
        input_format=InputFormat.YAML,
        language=RUST_LAZY_STATIC,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=NewVariable(name="names"),
    )
    expected = (
        "static names: LazyLock<HashSet<&str>> = "
        "LazyLock::new(|| HashSet::from([\n"
        '    "a",\n'
        '    "b",\n'
        "]));"
    )
    assert result.code == expected


def test_rust_lazy_static_dict_btree_map() -> None:
    """Rust LAZY_STATIC composes with ``BTREE_MAP`` for sorted maps.

    The ``dict_format`` x ``declaration_style`` cross-product is
    not part of the integration-test variant matrix, so the
    combination is exercised here.
    """
    lang = Rust(
        date_format=Rust.date_formats.ISO,
        datetime_format=Rust.datetime_formats.ISO,
        bytes_format=Rust.bytes_formats.HEX,
        dict_format=Rust.dict_formats.BTREE_MAP,
        declaration_style=Rust.declaration_styles.LAZY_STATIC,
    )
    result = literalize(
        source='{"a": 1}',
        input_format=InputFormat.JSON,
        language=lang,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=NewVariable(name="counts"),
    )
    expected = (
        "static counts: LazyLock<BTreeMap<&str, i32>> = "
        "LazyLock::new(|| BTreeMap::from([\n"
        '    ("a", 1),\n'
        "]));"
    )
    assert result.code == expected


def test_rust_lazy_static_preamble_includes_lazy_lock() -> None:
    """``LAZY_STATIC`` adds ``use std::sync::LazyLock;`` to the
    preamble.
    """
    assert RUST_LAZY_STATIC.static_preamble == ("use std::sync::LazyLock;",)


def test_rust_static_preamble_excludes_lazy_lock() -> None:
    """Non-``LAZY_STATIC`` declaration styles emit no ``LazyLock``
    import.
    """
    assert RUST_CONST.static_preamble == ()


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


def test_yaml_variable_name_not_in_language() -> None:
    """YAML has no variable declaration syntax; requesting one raises."""
    with pytest.raises(
        expected_exception=VariableNamesNotSupportedByLanguageError,
    ):
        literalize(
            source="key: value",
            input_format=InputFormat.YAML,
            language=Yaml(),
            variable_form=NewVariable(name="my_data"),
        )
