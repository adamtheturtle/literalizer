"""Tests for YAML-related literalizer functionality."""

import re
import textwrap

import pytest

from literalizer import (
    InputFormat,
    literalize,
)
from literalizer.exceptions import (
    HeterogeneousCollectionError,
    InvalidDictKeyError,
    ParseError,
    YAMLParseError,
)
from literalizer.languages import (
    Dhall,
    Mojo,
    Nix,
    Python,
    R,
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


def test_parse_yaml_invalid_roundtrip_path_raises() -> None:
    """Invalid YAML still raises on the round-trip parsing path."""
    with pytest.raises(expected_exception=YAMLParseError):
        literalize(
            source="value: [1\n# force roundtrip path\n",
            input_format=InputFormat.YAML,
            language=PYTHON,
        )


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
