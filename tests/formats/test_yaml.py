"""YAML-format-specific behavior.

YAML carries native tagged types (``!!binary``, ``!!omap``, ``!!set``)
and native ``date``/``datetime`` scalars that other input formats
either cannot express or express only as strings.  Heterogeneous-type
checks involving those tags therefore stay in this module; pure
collection-shape checks that work across every format live in
:mod:`tests.errors.test_coercion_errors`.
"""

import textwrap

import pytest

from literalizer import InputFormat, literalize
from literalizer.exceptions import (
    HeterogeneousCollectionError,
    ParseError,
    YAMLParseError,
)
from literalizer.languages import Mojo, Python

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
    variable_type_hints=Python.variable_type_hints_formats.NEVER,
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
    """``!!binary`` bytes in a heterogeneous collection raise for Mojo."""
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
    """YAML-native dates in a heterogeneous collection raise for Mojo."""
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
    """YAML-native datetimes in a heterogeneous collection raise."""
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


def test_mixed_dict_values_set_with_string_raises() -> None:
    """Dicts with a ``!!set`` alongside a string raise for Mojo."""
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


def test_mixed_ordered_map_values_raises() -> None:
    """``!!omap`` with mixed value types raises for Mojo."""
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


def test_raises_for_heterogeneous_ordered_map() -> None:
    """Raises for heterogeneous ``!!omap`` values."""
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
    """Raises for heterogeneous ``!!set`` members."""
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
