"""Unit tests for comment configuration that cannot be integration
cases.
"""

import pytest

from literalizer import (
    InputFormat,
    Language,
    literalize,
)
from literalizer.languages import (
    Go,
    JavaScript,
    Python,
    Ruby,
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
PYTHON = Python(
    date_format=Python.date_formats.PYTHON,
    datetime_format=Python.datetime_formats.PYTHON,
    bytes_format=Python.bytes_formats.HEX,
    sequence_format=Python.sequence_formats.TUPLE,
    set_format=Python.set_formats.SET,
    variable_type_hints=Python.variable_type_hints_formats.AUTO,
)
RUBY = Ruby(
    date_format=Ruby.date_formats.RUBY,
    datetime_format=Ruby.datetime_formats.RUBY,
    bytes_format=Ruby.bytes_formats.HEX,
    sequence_format=Ruby.sequence_formats.ARRAY,
)


def test_yaml_comment_scalar_only_comments() -> None:
    """Scalar YAML with only markers and comments, no value line."""
    yaml_string = "---\n# just a comment\n...\n"
    result = literalize(
        source=yaml_string,
        input_format=InputFormat.YAML,
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = "# just a comment\nNone"
    assert result.code == expected


def test_yaml_comment_no_include_delimiters() -> None:
    """Comments work with include_delimiters=False."""
    yaml_string = "# comment\n- a\n- b\n"
    result = literalize(
        source=yaml_string,
        input_format=InputFormat.YAML,
        language=PYTHON,
        pre_indent_level=1,
        include_delimiters=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = '    # comment\n    "a",\n    "b",'
    assert result.code == expected


@pytest.mark.parametrize(
    argnames=("language", "expected"),
    argvalues=[
        (PYTHON, "#"),
        (RUBY, "#"),
        (JAVASCRIPT, "//"),
        (GO, "//"),
    ],
)
def test_comment_prefix(language: Language, expected: str) -> None:
    """Each language has the expected comment prefix."""
    assert language.comment_config.prefix == expected


@pytest.mark.parametrize(
    argnames="language",
    argvalues=[
        PYTHON,
        RUBY,
        JAVASCRIPT,
        GO,
    ],
)
def test_comment_suffix(language: Language) -> None:
    """Each language has an empty comment suffix."""
    assert language.comment_config.suffix == ""
