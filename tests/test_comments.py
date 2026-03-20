"""Tests for YAML comment handling in literalizer converter."""

import textwrap

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
    date_format=Go.DateFormat.ISO,
    datetime_format=Go.DatetimeFormat.ISO,
    bytes_format=Go.BytesFormat.HEX,
    sequence_format=Go.SequenceFormat.SLICE,
)
JAVASCRIPT = JavaScript(
    date_format=JavaScript.DateFormat.ISO,
    datetime_format=JavaScript.DatetimeFormat.ISO,
    bytes_format=JavaScript.BytesFormat.HEX,
    sequence_format=JavaScript.SequenceFormat.ARRAY,
)
PYTHON = Python(
    date_format=Python.DateFormat.ISO,
    datetime_format=Python.DatetimeFormat.ISO,
    bytes_format=Python.BytesFormat.HEX,
    sequence_format=Python.SequenceFormat.TUPLE,
    set_format=Python.SetFormat.SET,
    variable_type_hints=Python.VariableTypeHints.NONE,
)
RUBY = Ruby(
    date_format=Ruby.DateFormat.ISO,
    datetime_format=Ruby.DatetimeFormat.ISO,
    bytes_format=Ruby.BytesFormat.HEX,
    sequence_format=Ruby.SequenceFormat.ARRAY,
)


def test_yaml_comment_sequence_before() -> None:
    """Full-line comments before sequence items are preserved."""
    yaml_string = "# first\n- a\n# second\n- b\n"
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
            # first
            "a",
            # second
            "b",
        )"""
    )
    assert result == expected


def test_yaml_comment_sequence_inline() -> None:
    """Inline comments on sequence items are preserved."""
    yaml_string = "- a  # note a\n- b  # note b\n"
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
            "a",  # note a
            "b",  # note b
        )"""
    )
    assert result == expected


def test_yaml_comment_mapping() -> None:
    """Comments in mappings are preserved."""
    yaml_string = "# comment for a\na: 1  # inline a\n# comment for b\nb: 2\n"
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
        {
            # comment for a
            "a": 1,  # inline a
            # comment for b
            "b": 2,
        }"""
    )
    assert result == expected


def test_yaml_comment_javascript_prefix() -> None:
    """Comments use the target language's comment prefix."""
    yaml_string = "# comment\n- a\n"
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=JAVASCRIPT,
        line_prefix="",
        indent="    ",
        wrap=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        [
            // comment
            "a",
        ]"""
    )
    assert result == expected


def test_yaml_comment_trailing() -> None:
    """Trailing comments after the last element are preserved."""
    yaml_string = "- a\n# trailing\n"
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
            "a",
            # trailing
        )"""
    )
    assert result == expected


def test_yaml_comment_no_wrap() -> None:
    """Comments work with wrap=False."""
    yaml_string = "# comment\n- a\n- b\n"
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
    expected = '    # comment\n    "a",\n    "b",'
    assert result == expected


def test_yaml_comment_scalar() -> None:
    """Comments on scalar YAML values are preserved."""
    yaml_string = "# note\n42\n"
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
    expected = "# note\n42"
    assert result == expected


def test_yaml_comment_scalar_inline() -> None:
    """Inline comments on scalar YAML values are preserved."""
    yaml_string = "42  # note\n"
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
    expected = "42  # note"
    assert result == expected


def test_yaml_no_comments_unchanged() -> None:
    """YAML without comments produces the same output as before."""
    yaml_string = "- a\n- b\n"
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
            "a",
            "b",
        )"""
    )
    assert result == expected


def test_yaml_comment_multiple_before_lines() -> None:
    """Multiple comment lines before an element are all preserved."""
    yaml_string = "# line 1\n# line 2\n- a\n"
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
            # line 1
            # line 2
            "a",
        )"""
    )
    assert result == expected


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
    assert language.comment_prefix == expected


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
    assert language.comment_suffix == ""


def test_yaml_comment_escaped_quote_in_value() -> None:
    """Escaped quotes do not end the quoted context."""
    yaml_string = 'key: "value \\" # not a comment" # real\n'
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
        {
            "key": "value \\" # not a comment",  # real
        }"""
    )
    assert result == expected


def test_yaml_comment_scalar_quoted_with_hash() -> None:
    """Inline comment after a quoted scalar containing ``#``."""
    yaml_string = '"hello # world"  # note\n'
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
    expected = '"hello # world"  # note'
    assert result == expected


def test_yaml_comment_double_hash() -> None:
    """Double-hash comments preserve the extra ``#``."""
    yaml_string = "## section\n- a\n"
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
            # # section
            "a",
        )"""
    )
    assert result == expected


def test_yaml_comment_block_scalar_not_extracted() -> None:
    """Text inside a block scalar is not mistaken for a comment."""
    yaml_string = "description: |\n  # not a comment\nname: foo\n"
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
        {
            "description": "# not a comment\\n",
            "name": "foo",
        }"""
    )
    assert result == expected


def test_yaml_comment_scalar_with_document_markers() -> None:
    """Document markers ``---`` and ``...`` are ignored in scalars."""
    yaml_string = "---\n# note\n42\n...\n"
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
    expected = "# note\n42"
    assert result == expected


def test_yaml_comment_empty_comment_line() -> None:
    """A bare ``#`` with no text produces a prefix-only comment."""
    yaml_string = "- a\n#\n- b\n"
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
            "a",
            #
            "b",
        )"""
    )
    assert result == expected


def test_yaml_comment_more_body_lines_than_comments() -> None:
    """Body lines beyond the number of comments are emitted plain."""
    yaml_string = "- a\n- b\n- c\n"
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
            "a",
            "b",
            "c",
        )"""
    )
    assert result == expected


def test_yaml_comment_scalar_only_comments() -> None:
    """Scalar YAML with only markers and comments, no value line."""
    yaml_string = "---\n# just a comment\n...\n"
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
    expected = "# just a comment\nNone"
    assert result == expected


def test_yaml_comment_mapping_nested_value_none_token() -> None:
    """Mapping key with nested comment has None at token index 2."""
    yaml_string = "a:\n  # indented\n  x: 1\nb: 2\n"
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
        {
            "a": {"x": 1},
            "b": 2,
        }"""
    )
    assert result == expected
