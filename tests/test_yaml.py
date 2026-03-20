"""Tests for YAML-related literalizer functionality."""

import textwrap

import pytest
from beartype import beartype

from literalizer import (
    Language,
    LanguageSpec,
    literalize_yaml,
)
from literalizer._formatters import (
    dict_entry_with_separator,
    fixed_dict_open,
    fixed_sequence_open,
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    format_string_backslash,
    passthrough_sequence_entry,
    passthrough_set_entry,
)
from literalizer.exceptions import (
    EmptyDictKeyError,
    HeterogeneousCoercionError,
    ParseError,
    YAMLParseError,
)
from literalizer.languages import (
    Go,
    Java,
    JavaScript,
    Mojo,
    Python,
    R,
    Ruby,
)

GO = Go(
    date_format=Go.DateFormat.ISO,
    datetime_format=Go.DatetimeFormat.ISO,
    sequence_format=Go.SequenceFormat.SLICE,
)
JAVASCRIPT = JavaScript(
    date_format=JavaScript.DateFormat.ISO,
    datetime_format=JavaScript.DatetimeFormat.ISO,
    sequence_format=JavaScript.SequenceFormat.ARRAY,
)
MOJO = Mojo(
    sequence_format=Mojo.SequenceFormat.LIST,
)
PYTHON = Python(
    date_format=Python.DateFormat.ISO,
    datetime_format=Python.DatetimeFormat.ISO,
    bytes_format=Python.BytesFormat.HEX,
    sequence_format=Python.SequenceFormat.TUPLE,
    set_format=Python.SetFormat.SET,
    variable_type_hints=Python.VariableTypeHints.NONE,
)


@beartype
def _format_test_omap_entry(key: str, value: str) -> str:
    """Format an omap entry for use in custom Language test
    fixtures.
    """
    return f"{key}: {value}"


def test_literalize_yaml_empty_sequence() -> None:
    """An empty YAML sequence produces an empty string."""
    result = literalize_yaml(
        yaml_string="[]\n",
        language=PYTHON,
        line_prefix="",
        indent="    ",
        wrap=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result == ""


def test_literalize_yaml_sequence() -> None:
    """``literalize_yaml`` parses a YAML sequence string."""
    yaml_string = "- [user_1, 1000.0]\n- [user_2, 2000.0]\n"
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=PYTHON,
        line_prefix="    ",
        indent="    ",
        wrap=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = '    ("user_1", 1000.0),\n    ("user_2", 2000.0),'
    assert result == expected


def test_literalize_yaml_mapping() -> None:
    """``literalize_yaml`` parses a YAML mapping string."""
    yaml_string = "a: 1\nb: true\n"
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=PYTHON,
        line_prefix="",
        indent="    ",
        wrap=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = '{\n    "a": 1,\n    "b": True,\n}'
    assert result == expected


def test_literalize_yaml_invalid() -> None:
    """``literalize_yaml`` raises on invalid YAML."""
    with pytest.raises(expected_exception=YAMLParseError):
        literalize_yaml(
            yaml_string=":\n  :\n    - ][",
            language=PYTHON,
            line_prefix="",
            indent="    ",
            wrap=False,
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
            line_prefix="",
            indent="    ",
            wrap=False,
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
        line_prefix="",
        indent="    ",
        wrap=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result == expected


def test_literalize_yaml_date() -> None:
    """``literalize_yaml`` formats date values as ISO string literals."""
    yaml_string = "- 2024-01-15\n"
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=PYTHON,
        line_prefix="",
        indent="    ",
        wrap=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result == '"2024-01-15",'


def test_literalize_yaml_datetime() -> None:
    """``literalize_yaml`` formats datetime values as ISO string
    literals.
    """
    yaml_string = "- 2024-01-15T12:30:00\n"
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=PYTHON,
        line_prefix="",
        indent="    ",
        wrap=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result == '"2024-01-15T12:30:00",'


def test_literalize_yaml_binary() -> None:
    """``literalize_yaml`` formats !!binary values as hex strings."""
    yaml_string = "- !!binary |\n    SGVsbG8=\n"
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=PYTHON,
        line_prefix="",
        indent="    ",
        wrap=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result == '"48656c6c6f",'


def test_yaml_set_inline_in_sequence() -> None:
    """A !!set nested in a sequence is formatted inline using set
    delimiters.
    """
    result = literalize_yaml(
        yaml_string="- !!set\n  ? a\n  ? b\n",
        language=PYTHON,
        line_prefix="",
        indent="    ",
        wrap=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result == '{"a", "b"},'


def test_yaml_set_inline_with_format_set_entry() -> None:
    """A !!set nested in a list uses format_set_entry when provided."""
    result = literalize_yaml(
        yaml_string="- !!set\n  ? a\n",
        language=GO,
        line_prefix="",
        indent="    ",
        wrap=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result == 'map[any]struct{}{"a": struct{}{}},'


def test_yaml_empty_set_inline() -> None:
    """An empty !!set nested in a list uses empty_set override."""
    result = literalize_yaml(
        yaml_string="- !!set {}\n",
        language=PYTHON,
        line_prefix="",
        indent="    ",
        wrap=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result == "set(),"


def test_omap_nested_in_sequence() -> None:
    """An omap nested inside a sequence exercises _format_value's omap
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
        line_prefix="",
        indent="    ",
        wrap=True,
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
    assert result == expected


def test_omap_custom_language_spec() -> None:
    """An omap with a custom Language calls format_omap_entry."""
    yaml_string = textwrap.dedent(
        text="""\
        !!omap
        - name: Alice
        - age: 30
        """,
    )
    custom = LanguageSpec(
        null_literal="null",
        true_literal="true",
        false_literal="false",
        sequence_open=fixed_sequence_open(open_str="["),
        sequence_close="]",
        dict_open=fixed_dict_open(open_str="{"),
        dict_close="}",
        format_dict_entry=dict_entry_with_separator(separator=": "),
        multiline_trailing_comma=True,
        single_element_trailing_comma=False,
        format_string=format_string_backslash,
        format_bytes=format_bytes_hex,
        format_date=format_date_iso,
        format_datetime=format_datetime_iso,
        empty_sequence=None,
        empty_dict=None,
        set_open="[",
        set_close="]",
        empty_set=None,
        format_sequence_entry=passthrough_sequence_entry,
        format_set_entry=passthrough_set_entry,
        comment_prefix="//",
        comment_suffix="",
        omap_open="{",
        omap_close="}",
        format_omap_entry=_format_test_omap_entry,
        multiline_close_indent="",
        element_separator=", ",
        skip_null_dict_values=False,
        coerce_heterogeneous_to_strings=False,
        supports_collection_comments=True,
        format_variable_declaration=PYTHON.format_variable_declaration,
        format_variable_assignment=PYTHON.format_variable_assignment,
        sequence_format=Python.SequenceFormat.TUPLE,
    )
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=custom,
        line_prefix="",
        indent="    ",
        wrap=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        {
            "name": "Alice",
            "age": 30,
        }""",
    )
    assert result == expected


def test_custom_format_date() -> None:
    """A custom format_date callable is used for date values."""
    spec = Python(
        date_format=Python.DateFormat.PYTHON,
        datetime_format=Python.DatetimeFormat.ISO,
        bytes_format=Python.BytesFormat.HEX,
        sequence_format=Python.SequenceFormat.TUPLE,
        set_format=Python.SetFormat.SET,
        variable_type_hints=Python.VariableTypeHints.NONE,
    )
    result = literalize_yaml(
        yaml_string="- 2024-01-15\n",
        language=spec,
        line_prefix="",
        indent="    ",
        wrap=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result == "datetime.date(year=2024, month=1, day=15),"


def test_custom_format_datetime() -> None:
    """A custom format_datetime callable is used for datetime values."""
    spec = Python(
        date_format=Python.DateFormat.ISO,
        datetime_format=Python.DatetimeFormat.PYTHON,
        bytes_format=Python.BytesFormat.HEX,
        sequence_format=Python.SequenceFormat.TUPLE,
        set_format=Python.SetFormat.SET,
        variable_type_hints=Python.VariableTypeHints.NONE,
    )
    result = literalize_yaml(
        yaml_string="- 2024-01-15T12:30:00\n",
        language=spec,
        line_prefix="",
        indent="    ",
        wrap=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = (
        "datetime.datetime("
        "year=2024, month=1, day=15, "
        "hour=12, minute=30, second=0),"
    )
    assert result == expected


def test_java_native_dates() -> None:
    """Java language spec with native date formatting."""
    spec = Java(
        date_format=Java.DateFormat.JAVA,
        datetime_format=Java.DatetimeFormat.INSTANT,
        sequence_format=Java.SequenceFormat.ARRAY,
    )
    result = literalize_yaml(
        yaml_string="- 2024-01-15\n- 2024-01-15T12:30:00\n",
        language=spec,
        line_prefix="",
        indent="    ",
        wrap=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    lines = result.split(sep="\n")
    assert lines[0] == "LocalDate.of(2024, 1, 15),"
    assert lines[1] == 'Instant.parse("2024-01-15T12:30:00")'


def test_ruby_native_dates() -> None:
    """Ruby language spec with native date formatting."""
    spec = Ruby(
        date_format=Ruby.DateFormat.RUBY,
        datetime_format=Ruby.DatetimeFormat.RUBY,
        sequence_format=Ruby.SequenceFormat.ARRAY,
    )
    result = literalize_yaml(
        yaml_string="- 2024-01-15T12:30:00\n",
        language=spec,
        line_prefix="",
        indent="    ",
        wrap=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result == "Time.new(2024, 1, 15, 12, 30, 0),"


def test_custom_format_bytes() -> None:
    """A custom format_bytes callable is used for bytes values."""
    spec = Python(
        date_format=Python.DateFormat.ISO,
        datetime_format=Python.DatetimeFormat.ISO,
        bytes_format=Python.BytesFormat.PYTHON,
        sequence_format=Python.SequenceFormat.TUPLE,
        set_format=Python.SetFormat.SET,
        variable_type_hints=Python.VariableTypeHints.NONE,
    )
    result = literalize_yaml(
        yaml_string="- !!binary |\n    SGVsbG8=\n",
        language=spec,
        line_prefix="",
        indent="    ",
        wrap=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result == "b'Hello',"


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
        line_prefix="",
        indent="    ",
        wrap=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = '{\n    "key1": "48656c6c6f",\n    "key2": "42",\n}'
    assert result == expected


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
        line_prefix="",
        indent="    ",
        wrap=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = '[\n    "1",\n    "hello",\n]'
    assert result == expected


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
        line_prefix="",
        indent="    ",
        wrap=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = '[\n    "2024-01-15",\n    "42",\n]'
    assert result == expected


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
        line_prefix="",
        indent="    ",
        wrap=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = '[\n    "2024-01-15T12:30:00",\n    "42",\n]'
    assert result == expected


def test_coerce_homogeneous_omap_no_coercion() -> None:
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
        line_prefix="",
        indent="    ",
        wrap=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = '[\n    ("name", "Alice"),\n    ("city", "Paris"),\n]'
    assert result == expected


def test_r_empty_dict_key_positional() -> None:
    """R with POSITIONAL empty_dict_key emits unnamed list elements."""
    spec = R(
        date_format=R.DateFormat.ISO,
        datetime_format=R.DatetimeFormat.ISO,
        empty_dict_key=R.EmptyDictKey.POSITIONAL,
        sequence_format=R.SequenceFormat.LIST,
    )
    yaml_string = '{"": "value"}\n'
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=spec,
        line_prefix="",
        indent="    ",
        wrap=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result == 'list(\n    "value"\n)'


def test_r_empty_dict_key_positional_is_default() -> None:
    """R defaults to POSITIONAL for empty_dict_key."""
    spec = R(
        date_format=R.DateFormat.ISO,
        datetime_format=R.DatetimeFormat.ISO,
        empty_dict_key=R.EmptyDictKey.POSITIONAL,
        sequence_format=R.SequenceFormat.LIST,
    )
    yaml_string = '{"": "value"}\n'
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=spec,
        line_prefix="",
        indent="    ",
        wrap=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result == 'list(\n    "value"\n)'


def test_r_empty_dict_key_error() -> None:
    """R with ERROR empty_dict_key raises EmptyDictKeyError."""
    spec = R(
        date_format=R.DateFormat.ISO,
        datetime_format=R.DatetimeFormat.ISO,
        empty_dict_key=R.EmptyDictKey.ERROR,
        sequence_format=R.SequenceFormat.LIST,
    )
    yaml_string = '{"": "value"}\n'
    with pytest.raises(expected_exception=EmptyDictKeyError):
        literalize_yaml(
            yaml_string=yaml_string,
            language=spec,
            line_prefix="",
            indent="    ",
            wrap=True,
            variable_name=None,
            new_variable=True,
            error_on_coercion=False,
        )


def test_r_empty_dict_key_error_non_empty_key_ok() -> None:
    """R with ERROR empty_dict_key does not raise for non-empty keys."""
    spec = R(
        date_format=R.DateFormat.ISO,
        datetime_format=R.DatetimeFormat.ISO,
        empty_dict_key=R.EmptyDictKey.ERROR,
        sequence_format=R.SequenceFormat.LIST,
    )
    yaml_string = '{"key": "value"}\n'
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=spec,
        line_prefix="",
        indent="    ",
        wrap=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result == 'list(\n    "key" = "value"\n)'


def test_error_on_coercion_raises_for_heterogeneous_list() -> None:
    """Error_on_coercion raises when a list has mixed scalar types."""
    yaml_string = "- 1\n- 2.5\n- 3\n"
    with pytest.raises(expected_exception=HeterogeneousCoercionError):
        literalize_yaml(
            yaml_string=yaml_string,
            language=MOJO,
            line_prefix="",
            indent="    ",
            wrap=True,
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
            line_prefix="",
            indent="    ",
            wrap=True,
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
        line_prefix="",
        indent="    ",
        wrap=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=True,
    )
    assert result == "[\n    1,\n    2,\n    3,\n]"


def test_error_on_coercion_no_effect_without_coerce_flag() -> None:
    """Error_on_coercion has no effect when language doesn't coerce."""
    yaml_string = "- 1\n- 2.5\n- 3\n"
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=PYTHON,
        line_prefix="",
        indent="    ",
        wrap=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=True,
    )
    assert result == "(\n    1,\n    2.5,\n    3,\n)"


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
            line_prefix="",
            indent="    ",
            wrap=True,
            variable_name=None,
            new_variable=True,
            error_on_coercion=True,
        )


def test_error_on_coercion_raises_for_heterogeneous_omap() -> None:
    """Error_on_coercion raises for heterogeneous omap values."""
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
            line_prefix="",
            indent="    ",
            wrap=True,
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
            line_prefix="",
            indent="    ",
            wrap=True,
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
        line_prefix="",
        indent="    ",
        wrap=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=True,
    )
    assert result == '{\n    "a": 1,\n    "b": 2,\n}'


def test_error_on_coercion_no_raise_for_homogeneous_omap() -> None:
    """Error_on_coercion does not raise for homogeneous omap values."""
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
        line_prefix="",
        indent="    ",
        wrap=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=True,
    )
    assert result == '[\n    ("name", "Alice"),\n    ("city", "Paris"),\n]'


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
        line_prefix="",
        indent="    ",
        wrap=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=True,
    )
    assert result == "[\n    1,\n    2,\n]"
