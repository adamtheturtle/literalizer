"""Tests for YAML comment handling that cannot be integration cases."""

import pytest

from literalizer import (
    Language,
    literalize_yaml,
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
    variable_type_hints=Python.variable_type_hints_formats.NONE,
)
RUBY = Ruby(
    date_format=Ruby.date_formats.RUBY,
    datetime_format=Ruby.datetime_formats.RUBY,
    bytes_format=Ruby.bytes_formats.HEX,
    sequence_format=Ruby.sequence_formats.ARRAY,
)


def test_yaml_comment_no_include_delimiters() -> None:
    """Comments work with include_delimiters=False."""
    yaml_string = "# comment\n- a\n- b\n"
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=PYTHON,
        line_prefix="    ",
        indent="    ",
        include_delimiters=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = '    # comment\n    "a",\n    "b",'
    assert result.code == expected


def test_yaml_comment_scalar() -> None:
    """Comments on scalar YAML values are preserved."""
    yaml_string = "# note\n42\n"
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=PYTHON,
        line_prefix="",
        indent="    ",
        include_delimiters=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = "# note\n42"
    assert result.code == expected


def test_yaml_comment_scalar_inline() -> None:
    """Inline comments on scalar YAML values are preserved."""
    yaml_string = "42  # note\n"
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=PYTHON,
        line_prefix="",
        indent="    ",
        include_delimiters=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = "42  # note"
    assert result.code == expected


def test_yaml_comment_scalar_quoted_with_hash() -> None:
    """Inline comment after a quoted scalar containing ``#``."""
    yaml_string = '"hello # world"  # note\n'
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=PYTHON,
        line_prefix="",
        indent="    ",
        include_delimiters=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = '"hello # world"  # note'
    assert result.code == expected


def test_yaml_comment_scalar_with_document_markers() -> None:
    """Document markers ``---`` and ``...`` are ignored in scalars."""
    yaml_string = "---\n# note\n42\n...\n"
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=PYTHON,
        line_prefix="",
        indent="    ",
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = "# note\n42"
    assert result.code == expected


def test_yaml_comment_scalar_only_comments() -> None:
    """Scalar YAML with only markers and comments, no value line."""
    yaml_string = "---\n# just a comment\n...\n"
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=PYTHON,
        line_prefix="",
        indent="    ",
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = "# just a comment\nNone"
    assert result.code == expected


def test_yaml_comment_block_scalar_not_extracted() -> None:
    """Text inside a block scalar is not mistaken for a comment."""
    yaml_string = "description: |\n  # not a comment\nname: foo\n"
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=PYTHON,
        line_prefix="",
        indent="    ",
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = (
        '{\n    "description": "# not a comment\\n",\n    "name": "foo",\n}'
    )
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
