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
from literalizer.exceptions import ParseError, YAMLParseError
from literalizer.languages import (
    Go,
    Java,
    JavaScript,
    Mojo,
    Python,
    Ruby,
)

GO = Go()
JAVASCRIPT = JavaScript()
MOJO = Mojo()
PYTHON = Python()


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
        wrap=True,
    )
    assert result == ""


def test_literalize_yaml_sequence() -> None:
    """``literalize_yaml`` parses a YAML sequence string."""
    yaml_string = "- [user_1, 1000.0]\n- [user_2, 2000.0]\n"
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=PYTHON,
        line_prefix="    ",
        wrap=False,
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
        wrap=True,
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
            wrap=False,
        )


def test_literalize_yaml_invalid_is_parse_error() -> None:
    """``YAMLParseError`` is a subclass of ``ParseError``."""
    with pytest.raises(expected_exception=ParseError):
        literalize_yaml(
            yaml_string=":\n  :\n    - ][",
            language=PYTHON,
            line_prefix="",
            wrap=False,
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
        wrap=False,
    )
    assert result == expected


def test_literalize_yaml_date() -> None:
    """``literalize_yaml`` formats date values as ISO string literals."""
    yaml_string = "- 2024-01-15\n"
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=PYTHON,
        line_prefix="",
        wrap=False,
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
        wrap=False,
    )
    assert result == '"2024-01-15T12:30:00",'


def test_literalize_yaml_binary() -> None:
    """``literalize_yaml`` formats !!binary values as hex strings."""
    yaml_string = "- !!binary |\n    SGVsbG8=\n"
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=PYTHON,
        line_prefix="",
        wrap=False,
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
        wrap=False,
    )
    assert result == '{"a", "b"},'


def test_yaml_set_inline_with_format_set_entry() -> None:
    """A !!set nested in a list uses format_set_entry when provided."""
    result = literalize_yaml(
        yaml_string="- !!set\n  ? a\n",
        language=GO,
        line_prefix="",
        wrap=False,
    )
    assert result == 'map[any]struct{}{"a": struct{}{}},'


def test_yaml_empty_set_inline() -> None:
    """An empty !!set nested in a list uses empty_set override."""
    result = literalize_yaml(
        yaml_string="- !!set {}\n",
        language=PYTHON,
        line_prefix="",
        wrap=False,
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
        wrap=True,
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
        format_variable_declaration=PYTHON.format_variable_declaration,
        format_variable_assignment=PYTHON.format_variable_assignment,
    )
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=custom,
        line_prefix="",
        wrap=True,
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
    spec = Python(date_format=Python.DateFormat.PYTHON)
    result = literalize_yaml(
        yaml_string="- 2024-01-15\n",
        language=spec,
        line_prefix="",
        wrap=False,
    )
    assert result == "datetime.date(2024, 1, 15),"


def test_custom_format_datetime() -> None:
    """A custom format_datetime callable is used for datetime values."""
    spec = Python(datetime_format=Python.DatetimeFormat.PYTHON)
    result = literalize_yaml(
        yaml_string="- 2024-01-15T12:30:00\n",
        language=spec,
        line_prefix="",
        wrap=False,
    )
    assert result == "datetime.datetime(2024, 1, 15, 12, 30, 0),"


def test_java_native_dates() -> None:
    """Java language spec with native date formatting."""
    spec = Java(
        date_format=Java.DateFormat.JAVA,
        datetime_format=Java.DatetimeFormat.INSTANT,
    )
    result = literalize_yaml(
        yaml_string="- 2024-01-15\n- 2024-01-15T12:30:00\n",
        language=spec,
        line_prefix="",
        wrap=False,
    )
    lines = result.split(sep="\n")
    assert lines[0] == "LocalDate.of(2024, 1, 15),"
    assert lines[1] == 'Instant.parse("2024-01-15T12:30:00")'


def test_ruby_native_dates() -> None:
    """Ruby language spec with native date formatting."""
    spec = Ruby(
        date_format=Ruby.DateFormat.RUBY,
        datetime_format=Ruby.DatetimeFormat.RUBY,
    )
    result = literalize_yaml(
        yaml_string="- 2024-01-15T12:30:00\n",
        language=spec,
        line_prefix="",
        wrap=False,
    )
    assert result == "Time.new(2024, 1, 15, 12, 30, 0),"


def test_custom_format_bytes() -> None:
    """A custom format_bytes callable is used for bytes values."""
    spec = Python(bytes_format=Python.BytesFormat.PYTHON)
    result = literalize_yaml(
        yaml_string="- !!binary |\n    SGVsbG8=\n",
        language=spec,
        line_prefix="",
        wrap=False,
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
        wrap=True,
    )
    assert '"48656c6c6f"' in result
    assert '"42"' in result


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
        wrap=True,
    )
    assert '"1"' in result
    assert '"hello"' in result


def test_coerce_heterogeneous_set_collision() -> None:
    """Coercion is skipped when it would reduce element count."""
    yaml_string = textwrap.dedent(
        text="""\
        --- !!set
        ? 1
        ? "1"
    """,
    )
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=MOJO,
        wrap=True,
    )
    expected = textwrap.dedent(
        text="""\
        [
            1,
            "1",
        ]""",
    )
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
        wrap=True,
    )
    assert '"Alice"' in result
    assert '"Paris"' in result
