"""Tests for literalizer TOML conversion."""

import textwrap

import pytest

from literalizer import (
    Language,
    literalize_toml,
)
from literalizer.exceptions import (
    HeterogeneousCoercionError,
    ParseError,
    TOMLParseError,
)
from literalizer.languages import (
    Go,
    JavaScript,
    Mojo,
    Python,
)

PYTHON = Python(
    date_format=Python.date_formats.PYTHON,
    datetime_format=Python.datetime_formats.PYTHON,
    bytes_format=Python.bytes_formats.HEX,
    sequence_format=Python.sequence_formats.TUPLE,
    set_format=Python.set_formats.SET,
    variable_type_hints=Python.variable_type_hints_formats.AUTO,
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


def test_dict_python() -> None:
    """Python dict renders key-value pairs from TOML."""
    toml_string = 'user_1 = "team_alpha"\nuser_2 = "team_alpha"\n'
    result = literalize_toml(
        toml_string=toml_string,
        language=PYTHON,
        pre_indent_level=1,
        include_delimiters=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = '    "user_1": "team_alpha",\n    "user_2": "team_alpha",'
    assert result.code == expected


def test_dict_include_delimiters() -> None:
    """Wrapping a dict adds braces and indentation."""
    toml_string = "a = 1\nb = 2\n"
    result = literalize_toml(
        toml_string=toml_string,
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
            "b": 2,
        }"""
    )
    assert result.code == expected


def test_empty_table() -> None:
    """An empty TOML string produces an empty dict."""
    result = literalize_toml(
        toml_string="",
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result.code == "{}"


def test_integers() -> None:
    """Integer values in a TOML array are rendered literally."""
    toml_string = "values = [42, 0, -7]\n"
    result = literalize_toml(
        toml_string=toml_string,
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
            "values": (42, 0, -7),
        }"""
    )
    assert result.code == expected


def test_floats() -> None:
    """Float values are rendered literally."""
    toml_string = "values = [1000.0, 3.14]\n"
    result = literalize_toml(
        toml_string=toml_string,
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
            "values": (1000.0, 3.14),
        }"""
    )
    assert result.code == expected


def test_booleans() -> None:
    """Boolean values are formatted per language."""
    toml_string = "enabled = true\nverbose = false\n"
    result = literalize_toml(
        toml_string=toml_string,
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
            "enabled": True,
            "verbose": False,
        }"""
    )
    assert result.code == expected


def test_nested_table() -> None:
    """Nested TOML tables are rendered as nested dicts."""
    toml_string = '[server]\nname = "test"\nport = 8080\n'
    result = literalize_toml(
        toml_string=toml_string,
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
            "server": {"name": "test", "port": 8080},
        }"""
    )
    assert result.code == expected


def test_array_of_tables() -> None:
    """TOML array-of-tables produces a list of dicts."""
    toml_string = '[[items]]\nname = "a"\n\n[[items]]\nname = "b"\n'
    result = literalize_toml(
        toml_string=toml_string,
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
            "items": ({"name": "a"}, {"name": "b"}),
        }"""
    )
    assert result.code == expected


def test_date_python() -> None:
    """TOML date values are converted to Python date literals."""
    toml_string = "created = 2024-01-15\n"
    result = literalize_toml(
        toml_string=toml_string,
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
            "created": datetime.date(year=2024, month=1, day=15),
        }"""
    )
    assert result.code == expected


def test_datetime_python() -> None:
    """TOML datetime values are converted to Python datetime literals."""
    toml_string = "updated = 2024-01-15T10:30:00\n"
    result = literalize_toml(
        toml_string=toml_string,
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert '"updated": datetime.datetime(' in result.code
    assert "year=2024" in result.code
    assert "minute=30" in result.code


def test_time_coerced_to_string() -> None:
    """TOML time values are coerced to ISO-format strings."""
    toml_string = "start = 10:30:00\n"
    result = literalize_toml(
        toml_string=toml_string,
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
            "start": "10:30:00",
        }"""
    )
    assert result.code == expected


def test_invalid_toml() -> None:
    """``literalize_toml`` raises on invalid TOML."""
    with pytest.raises(expected_exception=TOMLParseError):
        literalize_toml(
            toml_string="not = [valid toml",
            language=PYTHON,
            pre_indent_level=0,
            include_delimiters=False,
            variable_name=None,
            new_variable=True,
            error_on_coercion=False,
        )


def test_invalid_toml_is_parse_error() -> None:
    """``TOMLParseError`` is a subclass of ``ParseError``."""
    with pytest.raises(expected_exception=ParseError):
        literalize_toml(
            toml_string="not = [valid toml",
            language=PYTHON,
            pre_indent_level=0,
            include_delimiters=False,
            variable_name=None,
            new_variable=True,
            error_on_coercion=False,
        )


def test_variable_declaration() -> None:
    """Variable name wraps the output in a declaration."""
    toml_string = 'name = "alice"\n'
    result = literalize_toml(
        toml_string=toml_string,
        language=JAVASCRIPT,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name="config",
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        const config = {
            "name": "alice",
        };"""
    )
    assert result.code == expected


def test_variable_assignment() -> None:
    """``new_variable=False`` uses assignment syntax."""
    toml_string = 'name = "alice"\n'
    result = literalize_toml(
        toml_string=toml_string,
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name="config",
        new_variable=False,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        config = {
            "name": "alice",
        }"""
    )
    assert result.code == expected


def test_go_output() -> None:
    """TOML input renders correctly for Go."""
    toml_string = 'name = "test"\ncount = 42\n'
    result = literalize_toml(
        toml_string=toml_string,
        language=GO,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = 'map[string]any{\n\t"name": "test",\n\t"count": 42,\n}'
    assert result.code == expected


MOJO = Mojo(
    date_format=Mojo.date_formats.ISO,
    datetime_format=Mojo.datetime_formats.ISO,
    bytes_format=Mojo.bytes_formats.HEX,
    sequence_format=Mojo.sequence_formats.LIST,
)


def test_error_on_coercion_raises() -> None:
    """Error_on_coercion raises for heterogeneous TOML arrays."""
    toml_string = "values = [1, 2.5, 3]\n"
    with pytest.raises(expected_exception=HeterogeneousCoercionError):
        literalize_toml(
            toml_string=toml_string,
            language=MOJO,
            pre_indent_level=0,
            include_delimiters=True,
            variable_name=None,
            new_variable=True,
            error_on_coercion=True,
        )


def test_error_on_coercion_no_raise_homogeneous() -> None:
    """Error_on_coercion does not raise for homogeneous TOML arrays."""
    toml_string = "values = [1, 2, 3]\n"
    result = literalize_toml(
        toml_string=toml_string,
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=True,
    )
    expected = textwrap.dedent(
        text="""\
        {
            "values": (1, 2, 3),
        }"""
    )
    assert result.code == expected


@pytest.mark.parametrize(
    argnames=("toml_string", "language", "expected"),
    argvalues=[
        ("v = 42\n", PYTHON, '{\n    "v": 42,\n}'),
        ("v = 3.14\n", PYTHON, '{\n    "v": 3.14,\n}'),
        ('v = "hello"\n', PYTHON, '{\n    "v": "hello",\n}'),
        ("v = true\n", PYTHON, '{\n    "v": True,\n}'),
        ("v = false\n", PYTHON, '{\n    "v": False,\n}'),
    ],
)
def test_scalar_types(
    *, toml_string: str, language: Language, expected: str
) -> None:
    """Various TOML scalar types render correctly."""
    result = literalize_toml(
        toml_string=toml_string,
        language=language,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result.code == expected
