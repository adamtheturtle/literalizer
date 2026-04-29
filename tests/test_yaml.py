"""Tests for YAML-related literalizer functionality."""

import re
import textwrap

import pytest

from literalizer import (
    InputFormat,
    NewVariable,
    literalize,
)
from literalizer._comments import (
    CollectionComments,
    ElementComments,
    apply_collection_comments_to_elements,
)
from literalizer.exceptions import (
    HeterogeneousCollectionError,
    InvalidDictKeyError,
    ParseError,
    YAMLParseError,
)
from literalizer.languages import (
    Cpp,
    Dhall,
    Go,
    Mojo,
    Nix,
    Python,
    R,
)

GO = Go(
    date_format=Go.date_formats.GO,
    datetime_format=Go.datetime_formats.GO,
    bytes_format=Go.bytes_formats.HEX,
    sequence_format=Go.sequence_formats.SLICE,
)
MOJO = Mojo(
    date_format=Mojo.date_formats.ISO,
    datetime_format=Mojo.datetime_formats.ISO,
    bytes_format=Mojo.bytes_formats.HEX,
    sequence_format=Mojo.sequence_formats.LIST,
)
PYTHON = Python(
    date_format=Python.date_formats.PYTHON,
    datetime_format=Python.datetime_formats.PYTHON,
    bytes_format=Python.bytes_formats.HEX,
    sequence_format=Python.sequence_formats.TUPLE,
    set_format=Python.set_formats.SET,
    variable_type_hints=Python.variable_type_hints_formats.AUTO,
)


def test_literalize_yaml_sequence() -> None:
    """``literalize_yaml`` parses a YAML sequence string."""
    yaml_string = "- [user_1, 1000.0]\n- [user_2, 2000.0]\n"
    result = literalize(
        source=yaml_string,
        input_format=InputFormat.YAML,
        language=PYTHON,
        pre_indent_level=1,
        include_delimiters=False,
        variable_form=None,
    )
    expected = '    ("user_1", 1000.0),\n    ("user_2", 2000.0),'
    assert result.code == expected


def test_literalize_yaml_indent_override() -> None:
    """User-provided indent overrides the language default for YAML."""
    language = Python(
        date_format=Python.date_formats.PYTHON,
        datetime_format=Python.datetime_formats.PYTHON,
        bytes_format=Python.bytes_formats.HEX,
        sequence_format=Python.sequence_formats.TUPLE,
        set_format=Python.set_formats.SET,
        indent="\t",
    )
    yaml_string = "a: 1\nb: true\n"
    result = literalize(
        source=yaml_string,
        input_format=InputFormat.YAML,
        language=language,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=None,
    )
    expected = '{\n\t"a": 1,\n\t"b": True,\n}'
    assert result.code == expected


def test_literalize_yaml_invalid() -> None:
    """``literalize_yaml`` raises on invalid YAML."""
    with pytest.raises(expected_exception=YAMLParseError):
        literalize(
            source=":\n  :\n    - ][",
            input_format=InputFormat.YAML,
            language=PYTHON,
            pre_indent_level=0,
            include_delimiters=False,
            variable_form=None,
        )


def test_literalize_yaml_invalid_is_parse_error() -> None:
    """``YAMLParseError`` is a subclass of ``ParseError``."""
    with pytest.raises(expected_exception=ParseError):
        literalize(
            source=":\n  :\n    - ][",
            input_format=InputFormat.YAML,
            language=PYTHON,
            pre_indent_level=0,
            include_delimiters=False,
            variable_form=None,
        )


def test_literalize_yaml_after_invalid_uses_cached_instance() -> None:
    """Cached ``YAML`` instances recover after a parse error.

    Guards against ruamel.yaml ever leaving an instance in a broken
    state after an exception, which would compound across calls now
    that we cache instances via ``functools.cache``.
    """
    with pytest.raises(expected_exception=YAMLParseError):
        literalize(
            source=":\n  :\n    - ][",
            input_format=InputFormat.YAML,
            language=PYTHON,
        )
    result = literalize(
        source="foo: bar",
        input_format=InputFormat.YAML,
        language=PYTHON,
    )
    assert result.declaration_code == '{\n    "foo": "bar",\n}'


def test_literalize_yaml_quoted_hash_is_not_comment() -> None:
    """A quoted ``#`` still round-trips as plain scalar content."""
    result = literalize(
        source='"plain#value"\n',
        input_format=InputFormat.YAML,
        language=PYTHON,
    )
    assert result.declaration_code == '"plain#value"'


def test_parse_yaml_invalid_roundtrip_path_raises() -> None:
    """Invalid YAML still raises on the round-trip parsing path."""
    with pytest.raises(expected_exception=YAMLParseError):
        literalize(
            source="value: [1\n# force roundtrip path\n",
            input_format=InputFormat.YAML,
            language=PYTHON,
        )


def test_cpp_array_binary_typed() -> None:
    """C++ ARRAY format infers std::array<std::string, N> for binary
    data.
    """
    cpp_array = Cpp(sequence_format=Cpp.sequence_formats.ARRAY)
    yaml_string = "- !!binary |\n    SGVsbG8=\n"
    result = literalize(
        source=yaml_string,
        input_format=InputFormat.YAML,
        language=cpp_array,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=None,
    )
    expected = textwrap.dedent(
        text="""\
        std::array<std::string, 1>{
            "48656c6c6f",
        }""",
    )
    assert result.code == expected


def test_cpp_array_null_list_fallback() -> None:
    """C++ ARRAY format falls back when schema type is not directly
    convertible (e.g. all-null list).
    """
    cpp_array = Cpp(sequence_format=Cpp.sequence_formats.ARRAY)
    yaml_string = "- null\n- null\n"
    result = literalize(
        source=yaml_string,
        input_format=InputFormat.YAML,
        language=cpp_array,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=None,
    )
    expected = textwrap.dedent(
        text="""\
        {
            nullptr,
            nullptr,
        }""",
    )
    assert result.code == expected


def test_yaml_set_inline_in_sequence() -> None:
    """A !!set nested in a sequence is formatted inline using set
    delimiters.
    """
    result = literalize(
        source="- !!set\n  ? a\n  ? b\n",
        input_format=InputFormat.YAML,
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=False,
        variable_form=None,
    )
    assert result.code == '{"a", "b"},'


def test_yaml_set_inline_with_format_set_entry() -> None:
    """A !!set nested in a list uses format_set_entry when provided."""
    result = literalize(
        source="- !!set\n  ? a\n",
        input_format=InputFormat.YAML,
        language=GO,
        pre_indent_level=0,
        include_delimiters=False,
        variable_form=None,
    )
    assert result.code == 'map[string]struct{}{"a": struct{}{}},'


def test_yaml_empty_set_inline() -> None:
    """An empty !!set nested in a list uses empty_set override."""
    result = literalize(
        source="- !!set {}\n",
        input_format=InputFormat.YAML,
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=False,
        variable_form=None,
    )
    assert result.code == "set(),"


def test_ordered_map_nested_in_sequence() -> None:
    """An ordered map nested inside a sequence exercises _format_value's
    ordered-map
    branch.
    """
    yaml_string = textwrap.dedent(
        text="""\
        ---
        - !!omap
          - name: Alice
          - age: 30
        """,
    )
    result = literalize(
        source=yaml_string,
        input_format=InputFormat.YAML,
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=None,
    )
    expected = textwrap.dedent(
        text="""\
        (
            OrderedDict([("name", "Alice"), ("age", 30)]),
        )""",
    )
    assert result.code == expected


def test_heterogeneous_bytes_in_collection_raises() -> None:
    """Bytes in a heterogeneous collection raise for Mojo."""
    yaml_string = textwrap.dedent(
        text="""\
        key1: !!binary |
          SGVsbG8=
        key2: 42
    """,
    )
    with pytest.raises(expected_exception=HeterogeneousCollectionError):
        literalize(
            source=yaml_string,
            input_format=InputFormat.YAML,
            language=MOJO,
            pre_indent_level=0,
            include_delimiters=True,
            variable_form=None,
        )


def test_heterogeneous_date_in_collection_raises() -> None:
    """Dates in a heterogeneous collection raise for Mojo."""
    yaml_string = textwrap.dedent(
        text="""\
        - 2024-01-15
        - 42
    """,
    )
    with pytest.raises(expected_exception=HeterogeneousCollectionError):
        literalize(
            source=yaml_string,
            input_format=InputFormat.YAML,
            language=MOJO,
            pre_indent_level=0,
            include_delimiters=True,
            variable_form=None,
        )


def test_heterogeneous_datetime_in_collection_raises() -> None:
    """Datetimes in a heterogeneous collection raise for Mojo."""
    yaml_string = textwrap.dedent(
        text="""\
        - 2024-01-15T12:30:00
        - 42
    """,
    )
    with pytest.raises(expected_exception=HeterogeneousCollectionError):
        literalize(
            source=yaml_string,
            input_format=InputFormat.YAML,
            language=MOJO,
            pre_indent_level=0,
            include_delimiters=True,
            variable_form=None,
        )


def test_homogeneous_ordered_map_no_raise() -> None:
    """Homogeneous ordereddict values do not raise."""
    yaml_string = textwrap.dedent(
        text="""\
        --- !!omap
          - name: Alice
          - city: Paris
    """,
    )
    result = literalize(
        source=yaml_string,
        input_format=InputFormat.YAML,
        language=MOJO,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=None,
    )
    expected = textwrap.dedent(
        text="""\
        [
            Tuple("name", "Alice"),
            Tuple("city", "Paris"),
        ]"""
    )
    assert result.code == expected


def test_mixed_dict_values_none_with_list_raises() -> None:
    """Dicts with None alongside a list raise for Mojo."""
    yaml_string = textwrap.dedent(
        text="""\
        tags:
          - admin
        extra:
    """,
    )
    with pytest.raises(expected_exception=HeterogeneousCollectionError):
        literalize(
            source=yaml_string,
            input_format=InputFormat.YAML,
            language=MOJO,
            pre_indent_level=0,
            include_delimiters=True,
            variable_form=None,
        )


def test_mixed_dict_values_set_with_string_raises() -> None:
    """Dicts with a set alongside a string raise for Mojo."""
    yaml_string = textwrap.dedent(
        text="""\
        name: Alice
        roles: !!set
          ? admin
    """,
    )
    with pytest.raises(expected_exception=HeterogeneousCollectionError):
        literalize(
            source=yaml_string,
            input_format=InputFormat.YAML,
            language=MOJO,
            pre_indent_level=0,
            include_delimiters=True,
            variable_form=None,
        )


def test_mixed_dict_values_with_list_raises() -> None:
    """Dicts with string and list values raise for Mojo."""
    yaml_string = textwrap.dedent(
        text="""\
        name: Bob
        tags:
          - admin
          - user
    """,
    )
    with pytest.raises(expected_exception=HeterogeneousCollectionError):
        literalize(
            source=yaml_string,
            input_format=InputFormat.YAML,
            language=MOJO,
            pre_indent_level=0,
            include_delimiters=True,
            variable_form=None,
        )


def test_mixed_ordered_map_values_raises() -> None:
    """Ordered maps with mixed value types raise for Mojo."""
    yaml_string = textwrap.dedent(
        text="""\
        --- !!omap
          - name: Alice
          - score: 42
          - tags:
            - admin
    """,
    )
    with pytest.raises(expected_exception=HeterogeneousCollectionError):
        literalize(
            source=yaml_string,
            input_format=InputFormat.YAML,
            language=MOJO,
            pre_indent_level=0,
            include_delimiters=True,
            variable_form=None,
        )


def test_r_empty_dict_key_positional() -> None:
    """R with POSITIONAL empty_dict_key emits unnamed list elements."""
    spec = R(
        date_format=R.date_formats.R,
        datetime_format=R.datetime_formats.R,
        empty_dict_key=R.empty_dict_keys.POSITIONAL,
        bytes_format=R.bytes_formats.HEX,
        sequence_format=R.sequence_formats.LIST,
    )
    yaml_string = '{"": "value"}\n'
    result = literalize(
        source=yaml_string,
        input_format=InputFormat.YAML,
        language=spec,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=None,
    )
    expected = textwrap.dedent(
        text="""\
        list(
            "value"
        )"""
    )
    assert result.code == expected


def test_r_empty_dict_key_error() -> None:
    """R with ERROR empty_dict_key raises InvalidDictKeyError."""
    spec = R(
        date_format=R.date_formats.R,
        datetime_format=R.datetime_formats.R,
        empty_dict_key=R.empty_dict_keys.ERROR,
        bytes_format=R.bytes_formats.HEX,
        sequence_format=R.sequence_formats.LIST,
    )
    yaml_string = '{"": "value"}\n'
    expected_msg = re.escape(
        pattern='R does not support the dict key "". '
        "Use empty_dict_key=R.EmptyDictKey.POSITIONAL to emit them "
        "as unnamed list elements instead."
    )
    with pytest.raises(
        expected_exception=InvalidDictKeyError,
        match=f"^{expected_msg}$",
    ):
        literalize(
            source=yaml_string,
            input_format=InputFormat.YAML,
            language=spec,
            pre_indent_level=0,
            include_delimiters=True,
            variable_form=None,
        )


def test_r_empty_dict_key_error_non_empty_key_ok() -> None:
    """R with ERROR empty_dict_key does not raise for non-empty keys."""
    spec = R(
        date_format=R.date_formats.R,
        datetime_format=R.datetime_formats.R,
        empty_dict_key=R.empty_dict_keys.ERROR,
        bytes_format=R.bytes_formats.HEX,
        sequence_format=R.sequence_formats.LIST,
    )
    yaml_string = '{"key": "value"}\n'
    result = literalize(
        source=yaml_string,
        input_format=InputFormat.YAML,
        language=spec,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=None,
    )
    expected = textwrap.dedent(
        text="""\
        list(
            "key" = "value"
        )"""
    )
    assert result.code == expected


def test_raises_for_heterogeneous_ordered_map() -> None:
    """Raises for heterogeneous ordered-map values."""
    yaml_string = textwrap.dedent(
        text="""\
        --- !!omap
          - name: Alice
          - age: 30
    """,
    )
    with pytest.raises(expected_exception=HeterogeneousCollectionError):
        literalize(
            source=yaml_string,
            input_format=InputFormat.YAML,
            language=MOJO,
            pre_indent_level=0,
            include_delimiters=True,
            variable_form=None,
        )


def test_raises_for_heterogeneous_set() -> None:
    """Raises for heterogeneous sets."""
    yaml_string = textwrap.dedent(
        text="""\
        --- !!set
        ? 1
        ? "hello"
    """,
    )
    with pytest.raises(expected_exception=HeterogeneousCollectionError):
        literalize(
            source=yaml_string,
            input_format=InputFormat.YAML,
            language=MOJO,
            pre_indent_level=0,
            include_delimiters=True,
            variable_form=None,
        )


def test_no_raise_for_homogeneous_ordered_map() -> None:
    """Does not raise for homogeneous ordered-map values."""
    yaml_string = textwrap.dedent(
        text="""\
        --- !!omap
          - name: Alice
          - city: Paris
    """,
    )
    result = literalize(
        source=yaml_string,
        input_format=InputFormat.YAML,
        language=MOJO,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=None,
    )
    expected = textwrap.dedent(
        text="""\
        [
            Tuple("name", "Alice"),
            Tuple("city", "Paris"),
        ]"""
    )
    assert result.code == expected


def test_no_raise_for_homogeneous_set() -> None:
    """Does not raise for homogeneous sets."""
    yaml_string = textwrap.dedent(
        text="""\
        --- !!set
        ? 1
        ? 2
    """,
    )
    result = literalize(
        source=yaml_string,
        input_format=InputFormat.YAML,
        language=MOJO,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=None,
    )
    expected = textwrap.dedent(
        text="""\
        Set[Int](
            1,
            2,
        )"""
    )
    assert result.code == expected


def test_dhall_empty_dict_key_error() -> None:
    """Dhall raises InvalidDictKeyError for empty-string dict keys."""
    yaml_string = '{"": "value"}\n'
    expected_msg = re.escape(
        pattern='Dhall does not support the dict key "". '
        "Backtick-quoted labels must be non-empty and contain only "
        "printable ASCII (no backticks or control characters)."
    )
    with pytest.raises(
        expected_exception=InvalidDictKeyError,
        match=f"^{expected_msg}$",
    ):
        literalize(
            source=yaml_string,
            input_format=InputFormat.YAML,
            language=Dhall(),
            pre_indent_level=0,
            include_delimiters=True,
            variable_form=None,
        )


def test_dhall_control_char_in_string() -> None:
    """Dhall escapes control characters using braced unicode escapes."""
    yaml_string = '"\\x01"\n'
    result = literalize(
        source=yaml_string,
        input_format=InputFormat.YAML,
        language=Dhall(),
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=NewVariable(name="my_data"),
    )
    expected = 'let my_data = "\\u{0001}" in my_data'
    assert result.code == expected


def test_dhall_control_char_key_error() -> None:
    """Dhall rejects control characters in dict keys."""
    yaml_string = '{"\\x01": "value"}\n'
    expected_msg = re.escape(
        pattern='Dhall does not support the dict key "\\u{0001}". '
        "Backtick-quoted labels must be non-empty and contain only "
        "printable ASCII (no backticks or control characters)."
    )
    with pytest.raises(
        expected_exception=InvalidDictKeyError,
        match=f"^{expected_msg}$",
    ):
        literalize(
            source=yaml_string,
            input_format=InputFormat.YAML,
            language=Dhall(),
            pre_indent_level=0,
            include_delimiters=True,
            variable_form=None,
        )


def test_nix_control_char_key_error() -> None:
    """Nix rejects control characters in dict keys."""
    yaml_string = '{"\\x01": "value"}\n'
    expected_msg = re.escape(
        pattern='Nix does not support the dict key "\x01". '
        "Attribute names must be non-empty and must not contain "
        "control characters."
    )
    with pytest.raises(
        expected_exception=InvalidDictKeyError,
        match=f"^{expected_msg}$",
    ):
        literalize(
            source=yaml_string,
            input_format=InputFormat.YAML,
            language=Nix(),
            pre_indent_level=0,
            include_delimiters=True,
            variable_form=None,
        )


def test_dhall_backtick_label_unescaping() -> None:
    """Dhall backtick labels contain raw content, not escape sequences."""
    yaml_string = '{"$ref": "value"}\n'
    result = literalize(
        source=yaml_string,
        input_format=InputFormat.YAML,
        language=Dhall(),
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=NewVariable(name="my_data"),
    )
    expected = textwrap.dedent(
        text="""\
        let my_data = {
          `$ref` = "value",
        } in my_data"""
    )
    assert result.code == expected


def test_apply_collection_comments_to_elements_multiline_render() -> None:
    """Comments attach to the correct element when a render is multi-line.

    ``apply_collection_comments_to_elements`` operates at element
    granularity, so a rendered element that spans multiple lines does
    not shift later comments to the wrong element.
    """
    rendered_elements = [
        "first_line_of_element_0\nsecond_line_of_element_0",
        "element_1",
        "element_2_no_inline",
    ]
    collection_comments = CollectionComments(
        elements=(
            ElementComments(before=("before element 0",), inline="inline 0"),
            ElementComments(before=("before element 1",), inline="inline 1"),
            ElementComments(before=(), inline=""),
        ),
        trailing=("trailing",),
    )
    result = apply_collection_comments_to_elements(
        rendered_elements=rendered_elements,
        collection_comments=collection_comments,
        comment_prefix="#",
        comment_suffix="",
    )
    assert result == (
        "# before element 0\n"
        "first_line_of_element_0\n"
        "second_line_of_element_0  # inline 0\n"
        "# before element 1\n"
        "element_1  # inline 1\n"
        "element_2_no_inline\n"
        "# trailing"
    )
