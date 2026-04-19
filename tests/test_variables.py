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
from literalizer.exceptions import IncompatibleFormatsError
from literalizer.languages import Python, Rust

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
    coerce_heterogeneous_scalars=True,
    coerce_heterogeneous_sibling_lists=True,
    coerce_mixed_dict_values=True,
    coerce_mixed_list_values=True,
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


def test_rust_const_dict() -> None:
    """Rust CONST with dict produces ``HashMap`` type annotation."""
    result = literalize(
        source='{"a": "b"}',
        input_format=InputFormat.JSON,
        language=RUST_CONST,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=NewVariable(name="my_var"),
    )
    expected = textwrap.dedent(
        text="""\
        const my_var: HashMap<&str, &str> = HashMap::from([
            ("a", "b"),
        ]);"""
    )
    assert result.code == expected


def test_rust_const_empty_dict() -> None:
    """Rust CONST with empty dict uses default key/value types."""
    result = literalize(
        source="{}",
        input_format=InputFormat.JSON,
        language=RUST_CONST,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=NewVariable(name="my_var"),
    )
    assert result.code == (
        "const my_var: HashMap<String, String>"
        " = HashMap::<String, String>::from([]);"
    )


def test_rust_const_dict_mixed_values() -> None:
    """Rust CONST with mixed dict values falls back to ``&str``."""
    result = literalize(
        source='{"a": 1, "b": "x"}',
        input_format=InputFormat.JSON,
        language=RUST_CONST,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=NewVariable(name="my_var"),
    )
    expected = textwrap.dedent(
        text="""\
        const my_var: HashMap<&str, &str> = HashMap::from([
            ("a", "1"),
            ("b", "x"),
        ]);"""
    )
    assert result.code == expected


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


def test_rust_const_btree_map() -> None:
    """Rust CONST with ``BTREE_MAP`` uses ``BTreeMap`` type annotation."""
    rust_btree_map = Rust(
        date_format=Rust.date_formats.ISO,
        datetime_format=Rust.datetime_formats.ISO,
        bytes_format=Rust.bytes_formats.HEX,
        sequence_format=Rust.sequence_formats.ARRAY,
        dict_format=Rust.dict_formats.BTREE_MAP,
        declaration_style=Rust.declaration_styles.CONST,
    )
    result = literalize(
        source='{"a": "b"}',
        input_format=InputFormat.JSON,
        language=rust_btree_map,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=NewVariable(name="my_var"),
    )
    expected = textwrap.dedent(
        text="""\
        const my_var: BTreeMap<&str, &str> = BTreeMap::from([
            ("a", "b"),
        ]);"""
    )
    assert result.code == expected


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
