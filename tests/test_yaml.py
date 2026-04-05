"""Tests for YAML-related literalizer functionality."""

import textwrap

import pytest

from literalizer import (
    Language,
    literalize_yaml,
)
from literalizer.exceptions import (
    HeterogeneousCoercionError,
    InvalidDictKeyError,
    ParseError,
    YAMLParseError,
)
from literalizer.languages import (
    Cpp,
    Dhall,
    Go,
    JavaScript,
    Mojo,
    Python,
    R,
)

GO = Go(
    date_format=Go.date_formats.GO,
    datetime_format=Go.datetime_formats.GO,
    bytes_format=Go.bytes_formats.HEX,
    sequence_format=Go.sequence_formats.SLICE,
)
JAVASCRIPT = JavaScript(
    date_format=JavaScript.date_formats.JS,
    datetime_format=JavaScript.datetime_formats.JS,
    bytes_format=JavaScript.bytes_formats.HEX,
    sequence_format=JavaScript.sequence_formats.ARRAY,
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


def test_literalize_yaml_empty_sequence() -> None:
    """An empty YAML sequence produces the empty-sequence literal."""
    result = literalize_yaml(
        yaml_string="[]\n",
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result.code == "()"


def test_literalize_yaml_sequence() -> None:
    """``literalize_yaml`` parses a YAML sequence string."""
    yaml_string = "- [user_1, 1000.0]\n- [user_2, 2000.0]\n"
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=PYTHON,
        pre_indent_level=1,
        include_delimiters=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = '    ("user_1", 1000.0),\n    ("user_2", 2000.0),'
    assert result.code == expected


def test_literalize_yaml_mapping() -> None:
    """``literalize_yaml`` parses a YAML mapping string."""
    yaml_string = "a: 1\nb: true\n"
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        {
            "a": 1,
            "b": True,
        }"""
    )
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
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=language,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = '{\n\t"a": 1,\n\t"b": True,\n}'
    assert result.code == expected


def test_literalize_yaml_invalid() -> None:
    """``literalize_yaml`` raises on invalid YAML."""
    with pytest.raises(expected_exception=YAMLParseError):
        literalize_yaml(
            yaml_string=":\n  :\n    - ][",
            language=PYTHON,
            pre_indent_level=0,
            include_delimiters=False,
            variable_name=None,
            new_variable=True,
            error_on_coercion=False,
        )


def test_literalize_yaml_invalid_is_parse_error() -> None:
    """``YAMLParseError`` is a subclass of ``ParseError``."""
    with pytest.raises(expected_exception=ParseError):
        literalize_yaml(
            yaml_string=":\n  :\n    - ][",
            language=PYTHON,
            pre_indent_level=0,
            include_delimiters=False,
            variable_name=None,
            new_variable=True,
            error_on_coercion=False,
        )


@pytest.mark.parametrize(
    argnames=("yaml_string", "language", "expected"),
    argvalues=[
        ("42", PYTHON, "42"),
        ("3.14", PYTHON, "3.14"),
        ("hello", PYTHON, '"hello"'),
        ("true", PYTHON, "True"),
        ("false", PYTHON, "False"),
        ("null", PYTHON, "None"),
        ("true", JAVASCRIPT, "true"),
        ("null", GO, "nil"),
    ],
)
def test_literalize_yaml_scalar(
    *,
    yaml_string: str,
    language: Language,
    expected: str,
) -> None:
    """``literalize_yaml`` handles scalar YAML values."""
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=language,
        pre_indent_level=0,
        include_delimiters=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result.code == expected


def test_literalize_yaml_date() -> None:
    """``literalize_yaml`` formats date values using the language
    format.
    """
    yaml_string = "- 2024-01-15\n"
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result.code == "datetime.date(year=2024, month=1, day=15),"


def test_literalize_yaml_datetime() -> None:
    """``literalize_yaml`` formats datetime values using the language
    format.
    """
    yaml_string = "- 2024-01-15T12:30:00\n"
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = (
        "datetime.datetime("
        "year=2024, month=1, day=15, "
        "hour=12, minute=30, second=0),"
    )
    assert result.code == expected


def test_cpp_array_binary_typed() -> None:
    """C++ ARRAY format infers std::array<std::string, N> for binary
    data.
    """
    cpp_array = Cpp(sequence_format=Cpp.sequence_formats.ARRAY)
    yaml_string = "- !!binary |\n    SGVsbG8=\n"
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=cpp_array,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert '"48656c6c6f"' in result.code
    assert "std::array<std::string, 1>" in result.code


def test_cpp_array_null_list_fallback() -> None:
    """C++ ARRAY format falls back when schema type is not directly
    convertible (e.g. all-null list).
    """
    cpp_array = Cpp(sequence_format=Cpp.sequence_formats.ARRAY)
    yaml_string = "- null\n- null\n"
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=cpp_array,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert "nullptr" in result.code
    assert result.code.startswith("{")


def test_literalize_yaml_binary() -> None:
    """``literalize_yaml`` formats !!binary values as hex strings."""
    yaml_string = "- !!binary |\n    SGVsbG8=\n"
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result.code == '"48656c6c6f",'


def test_yaml_set_inline_in_sequence() -> None:
    """A !!set nested in a sequence is formatted inline using set
    delimiters.
    """
    result = literalize_yaml(
        yaml_string="- !!set\n  ? a\n  ? b\n",
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result.code == '{"a", "b"},'


def test_yaml_set_inline_with_format_set_entry() -> None:
    """A !!set nested in a list uses format_set_entry when provided."""
    result = literalize_yaml(
        yaml_string="- !!set\n  ? a\n",
        language=GO,
        pre_indent_level=0,
        include_delimiters=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result.code == 'map[string]struct{}{"a": struct{}{}},'


def test_yaml_empty_set_inline() -> None:
    """An empty !!set nested in a list uses empty_set override."""
    result = literalize_yaml(
        yaml_string="- !!set {}\n",
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
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
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        (
            OrderedDict([("name", "Alice"), ("age", 30)]),
        )""",
    )
    assert result.code == expected


def test_coerce_heterogeneous_bytes_in_collection() -> None:
    """Bytes in a heterogeneous collection are coerced to hex strings."""
    yaml_string = textwrap.dedent(
        text="""\
        key1: !!binary |
          SGVsbG8=
        key2: 42
    """,
    )
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=MOJO,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        {
            "key1": "48656c6c6f",
            "key2": "42",
        }"""
    )
    assert result.code == expected


def test_coerce_heterogeneous_set() -> None:
    """Heterogeneous sets are coerced to all strings."""
    yaml_string = textwrap.dedent(
        text="""\
        --- !!set
        ? 1
        ? "hello"
    """,
    )
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=MOJO,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        Set[String](
            "1",
            "hello",
        )"""
    )
    assert result.code == expected


def test_coerce_heterogeneous_date_in_collection() -> None:
    """Dates in a heterogeneous collection are coerced to ISO strings."""
    yaml_string = textwrap.dedent(
        text="""\
        - 2024-01-15
        - 42
    """,
    )
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=MOJO,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        [
            "2024-01-15",
            "42",
        ]"""
    )
    assert result.code == expected


def test_coerce_heterogeneous_datetime_in_collection() -> None:
    """Datetimes in a heterogeneous collection are coerced to ISO
    strings.
    """
    yaml_string = textwrap.dedent(
        text="""\
        - 2024-01-15T12:30:00
        - 42
    """,
    )
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=MOJO,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        [
            "2024-01-15T12:30:00",
            "42",
        ]"""
    )
    assert result.code == expected


def test_homogeneous_date_list_mojo() -> None:
    """A homogeneous list of dates is formatted via
    date_formats.__call__.
    """
    yaml_string = textwrap.dedent(
        text="""\
        - 2024-01-15
        - 2024-01-16
    """,
    )
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=MOJO,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        [
            "2024-01-15",
            "2024-01-16",
        ]"""
    )
    assert result.code == expected


def test_homogeneous_datetime_list_mojo() -> None:
    """A homogeneous list of datetimes is formatted via
    datetime_formats.__call__.
    """
    yaml_string = textwrap.dedent(
        text="""\
        - 2024-01-15T12:30:00
        - 2024-01-16T08:00:00
    """,
    )
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=MOJO,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        [
            "2024-01-15T12:30:00",
            "2024-01-16T08:00:00",
        ]"""
    )
    assert result.code == expected


def test_coerce_homogeneous_ordered_map_no_coercion() -> None:
    """Homogeneous ordereddict values are not coerced."""
    yaml_string = textwrap.dedent(
        text="""\
        --- !!omap
          - name: Alice
          - city: Paris
    """,
    )
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=MOJO,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        [
            Tuple("name", "Alice"),
            Tuple("city", "Paris"),
        ]"""
    )
    assert result.code == expected


def test_coerce_mixed_dict_values_none_with_list() -> None:
    """Dicts with None alongside a list are coerced to strings."""
    yaml_string = textwrap.dedent(
        text="""\
        tags:
          - admin
        extra:
    """,
    )
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=MOJO,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        {
            "tags": "[\\"admin\\"]",
            "extra": "None",
        }"""
    )
    assert result.code == expected


def test_coerce_mixed_dict_values_set_with_string() -> None:
    """Dicts with a set alongside a string are coerced to strings."""
    yaml_string = textwrap.dedent(
        text="""\
        name: Alice
        roles: !!set
          ? admin
    """,
    )
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=MOJO,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    # Set is converted to a sorted JSON array before string conversion.
    expected = textwrap.dedent(
        text="""\
        {
            "name": "Alice",
            "roles": "[\\"admin\\"]",
        }"""
    )
    assert result.code == expected


def test_coerce_mixed_dict_values_with_list() -> None:
    """Dicts with string and list values are coerced to all strings."""
    yaml_string = textwrap.dedent(
        text="""\
        name: Bob
        tags:
          - admin
          - user
    """,
    )
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=MOJO,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        {
            "name": "Bob",
            "tags": "[\\"admin\\", \\"user\\"]",
        }"""
    )
    assert result.code == expected


def test_coerce_mixed_ordered_map_values() -> None:
    """Ordered maps with mixed value types are coerced to strings."""
    yaml_string = textwrap.dedent(
        text="""\
        --- !!omap
          - name: Alice
          - score: 42
          - tags:
            - admin
    """,
    )
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=MOJO,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        [
            Tuple("name", "Alice"),
            Tuple("score", "42"),
            Tuple("tags", "[\\"admin\\"]"),
        ]"""
    )
    assert result.code == expected


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
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=spec,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        list(
            "value"
        )"""
    )
    assert result.code == expected


def test_r_empty_dict_key_positional_is_default() -> None:
    """R defaults to POSITIONAL for empty_dict_key."""
    spec = R(
        date_format=R.date_formats.R,
        datetime_format=R.datetime_formats.R,
        empty_dict_key=R.empty_dict_keys.POSITIONAL,
        bytes_format=R.bytes_formats.HEX,
        sequence_format=R.sequence_formats.LIST,
    )
    yaml_string = '{"": "value"}\n'
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=spec,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
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
    with pytest.raises(expected_exception=InvalidDictKeyError):
        literalize_yaml(
            yaml_string=yaml_string,
            language=spec,
            pre_indent_level=0,
            include_delimiters=True,
            variable_name=None,
            new_variable=True,
            error_on_coercion=False,
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
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=spec,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        list(
            "key" = "value"
        )"""
    )
    assert result.code == expected


def test_error_on_coercion_raises_for_heterogeneous_list() -> None:
    """Error_on_coercion raises when a list has mixed scalar types."""
    yaml_string = "- 1\n- 2.5\n- 3\n"
    with pytest.raises(expected_exception=HeterogeneousCoercionError):
        literalize_yaml(
            yaml_string=yaml_string,
            language=MOJO,
            pre_indent_level=0,
            include_delimiters=True,
            variable_name=None,
            new_variable=True,
            error_on_coercion=True,
        )


def test_error_on_coercion_raises_for_heterogeneous_dict() -> None:
    """Error_on_coercion raises when dict values have mixed scalar
    types.
    """
    yaml_string = textwrap.dedent(
        text="""\
        a: 1
        b: 2.5
    """,
    )
    with pytest.raises(expected_exception=HeterogeneousCoercionError):
        literalize_yaml(
            yaml_string=yaml_string,
            language=MOJO,
            pre_indent_level=0,
            include_delimiters=True,
            variable_name=None,
            new_variable=True,
            error_on_coercion=True,
        )


def test_error_on_coercion_no_raise_for_homogeneous() -> None:
    """Error_on_coercion does not raise for homogeneous collections."""
    yaml_string = "- 1\n- 2\n- 3\n"
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=MOJO,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=True,
    )
    expected = textwrap.dedent(
        text="""\
        [
            1,
            2,
            3,
        ]"""
    )
    assert result.code == expected


def test_error_on_coercion_no_effect_without_coerce_flag() -> None:
    """Error_on_coercion has no effect when language doesn't coerce."""
    yaml_string = "- 1\n- 2.5\n- 3\n"
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=True,
    )
    expected = textwrap.dedent(
        text="""\
        (
            1,
            2.5,
            3,
        )"""
    )
    assert result.code == expected


def test_error_on_coercion_raises_for_nested_heterogeneous() -> None:
    """Error_on_coercion raises for heterogeneous data nested in a
    list.
    """
    yaml_string = textwrap.dedent(
        text="""\
        - - 1
          - "hello"
    """,
    )
    with pytest.raises(expected_exception=HeterogeneousCoercionError):
        literalize_yaml(
            yaml_string=yaml_string,
            language=MOJO,
            pre_indent_level=0,
            include_delimiters=True,
            variable_name=None,
            new_variable=True,
            error_on_coercion=True,
        )


def test_error_on_coercion_raises_for_heterogeneous_ordered_map() -> None:
    """Error_on_coercion raises for heterogeneous ordered-map values."""
    yaml_string = textwrap.dedent(
        text="""\
        --- !!omap
          - name: Alice
          - age: 30
    """,
    )
    with pytest.raises(expected_exception=HeterogeneousCoercionError):
        literalize_yaml(
            yaml_string=yaml_string,
            language=MOJO,
            pre_indent_level=0,
            include_delimiters=True,
            variable_name=None,
            new_variable=True,
            error_on_coercion=True,
        )


def test_error_on_coercion_raises_for_heterogeneous_set() -> None:
    """Error_on_coercion raises for heterogeneous sets."""
    yaml_string = textwrap.dedent(
        text="""\
        --- !!set
        ? 1
        ? "hello"
    """,
    )
    with pytest.raises(expected_exception=HeterogeneousCoercionError):
        literalize_yaml(
            yaml_string=yaml_string,
            language=MOJO,
            pre_indent_level=0,
            include_delimiters=True,
            variable_name=None,
            new_variable=True,
            error_on_coercion=True,
        )


def test_error_on_coercion_no_raise_for_homogeneous_dict() -> None:
    """Error_on_coercion does not raise for homogeneous dict values."""
    yaml_string = textwrap.dedent(
        text="""\
        a: 1
        b: 2
    """,
    )
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=MOJO,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=True,
    )
    expected = textwrap.dedent(
        text="""\
        {
            "a": 1,
            "b": 2,
        }"""
    )
    assert result.code == expected


def test_error_on_coercion_no_raise_for_homogeneous_ordered_map() -> None:
    """Error_on_coercion does not raise for homogeneous ordered-map values."""
    yaml_string = textwrap.dedent(
        text="""\
        --- !!omap
          - name: Alice
          - city: Paris
    """,
    )
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=MOJO,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=True,
    )
    expected = textwrap.dedent(
        text="""\
        [
            Tuple("name", "Alice"),
            Tuple("city", "Paris"),
        ]"""
    )
    assert result.code == expected


def test_error_on_coercion_no_raise_for_homogeneous_set() -> None:
    """Error_on_coercion does not raise for homogeneous sets."""
    yaml_string = textwrap.dedent(
        text="""\
        --- !!set
        ? 1
        ? 2
    """,
    )
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=MOJO,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=True,
    )
    expected = textwrap.dedent(
        text="""\
        Set[Int](
            1,
            2,
        )"""
    )
    assert result.code == expected


def test_error_on_coercion_raises_for_mixed_dict_values() -> None:
    """Error_on_coercion raises when a dict has values of mixed types."""
    yaml_string = textwrap.dedent(
        text="""\
        name: Bob
        tags:
          - admin
          - user
    """,
    )
    with pytest.raises(expected_exception=HeterogeneousCoercionError):
        literalize_yaml(
            yaml_string=yaml_string,
            language=MOJO,
            pre_indent_level=0,
            include_delimiters=True,
            variable_name=None,
            new_variable=True,
            error_on_coercion=True,
        )


def test_error_on_coercion_raises_for_mixed_list_values() -> None:
    """Error_on_coercion raises when a list has mixed element types."""
    yaml_string = textwrap.dedent(
        text="""\
        - hello
        -
          - nested
    """,
    )
    with pytest.raises(expected_exception=HeterogeneousCoercionError):
        literalize_yaml(
            yaml_string=yaml_string,
            language=MOJO,
            pre_indent_level=0,
            include_delimiters=True,
            variable_name=None,
            new_variable=True,
            error_on_coercion=True,
        )


def test_error_on_coercion_raises_for_mixed_dict_shapes() -> None:
    """Error_on_coercion raises when a list has dicts with different
    keys, including when the list is nested inside a dict.
    """
    yaml_string = textwrap.dedent(
        text="""\
        items:
          - type: create
            draft: true
          - type: update
    """,
    )
    with pytest.raises(expected_exception=HeterogeneousCoercionError):
        literalize_yaml(
            yaml_string=yaml_string,
            language=Dhall(),
            pre_indent_level=0,
            include_delimiters=True,
            variable_name=None,
            new_variable=True,
            error_on_coercion=True,
        )


def test_error_on_coercion_no_raise_for_uniform_dict_shapes() -> None:
    """Error_on_coercion does not raise when all dicts in a list have
    the same keys.
    """
    yaml_string = textwrap.dedent(
        text="""\
        - type: create
          name: a
        - type: update
          name: b
    """,
    )
    literalize_yaml(
        yaml_string=yaml_string,
        language=Dhall(),
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=True,
    )


def test_error_on_coercion_raises_for_mixed_dict_none_list() -> None:
    """Error_on_coercion raises when a dict has None alongside a list."""
    yaml_string = textwrap.dedent(
        text="""\
        tags:
          - admin
        extra:
    """,
    )
    with pytest.raises(expected_exception=HeterogeneousCoercionError):
        literalize_yaml(
            yaml_string=yaml_string,
            language=MOJO,
            pre_indent_level=0,
            include_delimiters=True,
            variable_name=None,
            new_variable=True,
            error_on_coercion=True,
        )


def test_dhall_empty_dict_key_error() -> None:
    """Dhall raises InvalidDictKeyError for empty-string dict keys."""
    yaml_string = '{"": "value"}\n'
    with pytest.raises(expected_exception=InvalidDictKeyError):
        literalize_yaml(
            yaml_string=yaml_string,
            language=Dhall(),
            pre_indent_level=0,
            include_delimiters=True,
            variable_name=None,
            new_variable=True,
            error_on_coercion=False,
        )


def test_dhall_control_char_in_string() -> None:
    """Dhall escapes control characters using braced unicode escapes."""
    yaml_string = '"\\x01"\n'
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=Dhall(),
        pre_indent_level=0,
        include_delimiters=True,
        variable_name="my_data",
        new_variable=True,
        error_on_coercion=False,
    )
    expected = 'let my_data = "\\u{0001}" in my_data'
    assert result.code == expected


def test_dhall_control_char_key_error() -> None:
    """Dhall rejects control characters in dict keys."""
    yaml_string = '{"\\x01": "value"}\n'
    with pytest.raises(expected_exception=InvalidDictKeyError):
        literalize_yaml(
            yaml_string=yaml_string,
            language=Dhall(),
            pre_indent_level=0,
            include_delimiters=True,
            variable_name=None,
            new_variable=True,
            error_on_coercion=False,
        )


def test_dhall_backtick_label_unescaping() -> None:
    """Dhall backtick labels contain raw content, not escape sequences."""
    yaml_string = '{"$ref": "value"}\n'
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=Dhall(),
        pre_indent_level=0,
        include_delimiters=True,
        variable_name="my_data",
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        let my_data = {
          `$ref` = "value",
        } in my_data"""
    )
    assert result.code == expected
