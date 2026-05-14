"""Parameterized checks across all input formats.

These tests verify that ``literalize`` raises precise exceptions when
input data cannot be represented in the target language's collection
formats (e.g. heterogeneous scalar types in Mojo, non-uniform record
shapes in Dhall).  Format-specific tests for ordered maps and sets
remain in :mod:`tests.formats.test_yaml`.
"""

import json
import re
from io import StringIO
from typing import TYPE_CHECKING, assert_never

import pytest
import tomlkit
from beartype import beartype
from ruamel.yaml import YAML

from literalizer import InputFormat, literalize
from literalizer.exceptions import (
    HeterogeneousScalarCollectionError,
    HeterogeneousSiblingListsError,
    MixedDictShapesError,
    MixedDictValuesError,
    MixedListValuesError,
)
from literalizer.languages import Dhall, Mojo, Python

if TYPE_CHECKING:
    from collections.abc import Mapping

type _SourceData = (
    dict[str, _SourceData]
    | list[_SourceData]
    | str
    | int
    | float
    | bool
    | None
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
    variable_type_hints=Python.variable_type_hints_formats.NEVER,
)

ALL_FORMATS = list(InputFormat)

# Formats that support None/null values (TOML has no null type).
FORMATS_WITH_NULL = [f for f in ALL_FORMATS if f != InputFormat.TOML]


@beartype
def _to_source(
    data: _SourceData,
    input_format: InputFormat,
) -> str:
    """Serialize *data* into a source string for *input_format*.

    For TOML, non-dict data is wrapped in ``{"_": data}`` because TOML
    requires a top-level table.  The checks walk the whole data tree,
    so the wrapping does not affect whether an error is raised.
    """
    match input_format:
        case InputFormat.JSON:
            return json.dumps(obj=data)
        case InputFormat.JSON5:
            # Valid JSON is valid JSON5.
            return json.dumps(obj=data)
        case InputFormat.YAML:
            yaml = YAML()
            stream = StringIO()
            yaml.dump(data=data, stream=stream)  # pyright: ignore[reportUnknownMemberType]
            return stream.getvalue()
        case InputFormat.TOML:
            toml_data: Mapping[str, _SourceData] = (
                data if isinstance(data, dict) else {"_": data}
            )
            return tomlkit.dumps(data=toml_data)
        case _ as unreachable:
            assert_never(unreachable)


# --- Tests that should raise ---


@pytest.mark.parametrize(argnames="input_format", argvalues=ALL_FORMATS)
def test_raises_heterogeneous_array(input_format: InputFormat) -> None:
    """Heterogeneous scalar array raises across all formats."""
    expected_msg = re.escape(
        pattern="Collection contains heterogeneous scalar types that "
        "cannot be represented in the target language "
        "(found types: float, int)",
    )
    with pytest.raises(
        expected_exception=HeterogeneousScalarCollectionError,
        match=f"^{expected_msg}$",
    ):
        literalize(
            source=_to_source(data=[1, 2.5, 3], input_format=input_format),
            input_format=input_format,
            language=MOJO,
            pre_indent_level=0,
            include_delimiters=True,
        )


@pytest.mark.parametrize(argnames="input_format", argvalues=ALL_FORMATS)
def test_raises_heterogeneous_dict(input_format: InputFormat) -> None:
    """Dict with mixed-type scalar values raises across all formats."""
    with pytest.raises(expected_exception=HeterogeneousScalarCollectionError):
        literalize(
            source=_to_source(
                data={"a": 1, "b": 2.5},
                input_format=input_format,
            ),
            input_format=input_format,
            language=MOJO,
            pre_indent_level=0,
            include_delimiters=True,
        )


@pytest.mark.parametrize(argnames="input_format", argvalues=ALL_FORMATS)
def test_raises_nested_heterogeneous(input_format: InputFormat) -> None:
    """Heterogeneous data nested in a list raises across all formats."""
    with pytest.raises(expected_exception=HeterogeneousScalarCollectionError):
        literalize(
            source=_to_source(
                data=[[1, "hello"]],
                input_format=input_format,
            ),
            input_format=input_format,
            language=MOJO,
            pre_indent_level=0,
            include_delimiters=True,
        )


@pytest.mark.parametrize(argnames="input_format", argvalues=ALL_FORMATS)
def test_raises_sibling_lists(input_format: InputFormat) -> None:
    """Heterogeneous sibling sub-lists raise across all formats."""
    expected_msg = re.escape(
        pattern="Sibling lists contain heterogeneous scalar types that "
        "cannot be represented in the target language "
        "(found types: int, str)",
    )
    with pytest.raises(
        expected_exception=HeterogeneousSiblingListsError,
        match=f"^{expected_msg}$",
    ):
        literalize(
            source=_to_source(
                data=[[1, 2], ["a", "b"]],
                input_format=input_format,
            ),
            input_format=input_format,
            language=MOJO,
            pre_indent_level=0,
            include_delimiters=True,
        )


@pytest.mark.parametrize(argnames="input_format", argvalues=ALL_FORMATS)
def test_raises_nested_sibling_lists(input_format: InputFormat) -> None:
    """Nested heterogeneous sibling sub-lists raise across all formats."""
    expected_msg = re.escape(
        pattern="Sibling lists contain heterogeneous scalar types that "
        "cannot be represented in the target language "
        "(found types: int, str)",
    )
    with pytest.raises(
        expected_exception=HeterogeneousSiblingListsError,
        match=f"^{expected_msg}$",
    ):
        literalize(
            source=_to_source(
                data=[[[1, 2], ["a", "b"]]],
                input_format=input_format,
            ),
            input_format=input_format,
            language=MOJO,
            pre_indent_level=0,
            include_delimiters=True,
        )


@pytest.mark.parametrize(argnames="input_format", argvalues=ALL_FORMATS)
def test_raises_mixed_dict_values(input_format: InputFormat) -> None:
    """Dict with string and list values raises across all formats."""
    expected_msg = re.escape(
        pattern="Dict contains values of mixed types that cannot be "
        "represented in the target language "
        "(found types: list, str)",
    )
    with pytest.raises(
        expected_exception=MixedDictValuesError,
        match=f"^{expected_msg}$",
    ):
        literalize(
            source=_to_source(
                data={"name": "Bob", "tags": ["admin", "user"]},
                input_format=input_format,
            ),
            input_format=input_format,
            language=MOJO,
            pre_indent_level=0,
            include_delimiters=True,
        )


@pytest.mark.parametrize(argnames="input_format", argvalues=ALL_FORMATS)
def test_raises_nested_mixed_dict_values(input_format: InputFormat) -> None:
    """Nested dict with mixed types raises across all formats.

    The first child (a homogeneous dict) does not have mixed types, so
    the search must skip past it before finding the mixed one.
    """
    expected_msg = re.escape(
        pattern="Dict contains values of mixed types that cannot be "
        "represented in the target language "
        "(found types: list, str)",
    )
    with pytest.raises(
        expected_exception=MixedDictValuesError,
        match=f"^{expected_msg}$",
    ):
        literalize(
            source=_to_source(
                data={
                    "a": {"x": 1},
                    "b": {"x": "hello", "y": [1]},
                },
                input_format=input_format,
            ),
            input_format=input_format,
            language=MOJO,
            pre_indent_level=0,
            include_delimiters=True,
        )


@pytest.mark.parametrize(argnames="input_format", argvalues=ALL_FORMATS)
def test_raises_nested_mixed_list_values(input_format: InputFormat) -> None:
    """Nested list with mixed types raises across all formats.

    The first element is a homogeneous list, so the search must skip
    past it before finding the mixed second element.
    """
    expected_msg = re.escape(
        pattern="List contains elements of mixed types that cannot be "
        "represented in the target language "
        "(found types: list, str)",
    )
    with pytest.raises(
        expected_exception=MixedListValuesError,
        match=f"^{expected_msg}$",
    ):
        literalize(
            source=_to_source(
                data=[[1, 2], ["hello", ["nested"]]],
                input_format=input_format,
            ),
            input_format=input_format,
            language=MOJO,
            pre_indent_level=0,
            include_delimiters=True,
        )


@pytest.mark.parametrize(argnames="input_format", argvalues=ALL_FORMATS)
def test_raises_mixed_list_values(input_format: InputFormat) -> None:
    """List with string and nested list raises across all formats."""
    expected_msg = re.escape(
        pattern="List contains elements of mixed types that cannot be "
        "represented in the target language "
        "(found types: list, str)",
    )
    with pytest.raises(
        expected_exception=MixedListValuesError,
        match=f"^{expected_msg}$",
    ):
        literalize(
            source=_to_source(
                data=["hello", ["nested"]],
                input_format=input_format,
            ),
            input_format=input_format,
            language=MOJO,
            pre_indent_level=0,
            include_delimiters=True,
        )


@pytest.mark.parametrize(argnames="input_format", argvalues=ALL_FORMATS)
def test_raises_mixed_dict_inside_mixed_list(
    input_format: InputFormat,
) -> None:
    """Error message reports dict type families when a mixed dict is
    nested inside a mixed list.
    """
    expected_msg = re.escape(
        pattern="Dict contains values of mixed types that cannot be "
        "represented in the target language "
        "(found types: list, str)",
    )
    with pytest.raises(
        expected_exception=MixedDictValuesError,
        match=f"^{expected_msg}$",
    ):
        literalize(
            source=_to_source(
                data={"wrapper": [{"a": "x", "b": [1]}, "text"]},
                input_format=input_format,
            ),
            input_format=input_format,
            language=MOJO,
            pre_indent_level=0,
            include_delimiters=True,
        )


@pytest.mark.parametrize(argnames="input_format", argvalues=ALL_FORMATS)
def test_raises_mixed_dict_shapes(input_format: InputFormat) -> None:
    """Dicts with different key sets raise across all formats (Dhall)."""
    data: _SourceData = {
        "items": [
            {"type": "create", "draft": True},
            {"type": "update"},
        ],
    }
    expected_msg = re.escape(
        pattern="List contains dicts with different key sets that "
        "cannot be represented in the target language",
    )
    with pytest.raises(
        expected_exception=MixedDictShapesError,
        match=f"^{expected_msg}$",
    ):
        literalize(
            source=_to_source(data=data, input_format=input_format),
            input_format=input_format,
            language=Dhall(),
            pre_indent_level=0,
            include_delimiters=True,
        )


@pytest.mark.parametrize(argnames="input_format", argvalues=FORMATS_WITH_NULL)
def test_raises_mixed_dict_none_list(input_format: InputFormat) -> None:
    """Dict with None alongside a list raises (formats with null)."""
    expected_msg = re.escape(
        pattern="Dict contains values of mixed types that cannot be "
        "represented in the target language "
        "(found types: list, none)",
    )
    with pytest.raises(
        expected_exception=MixedDictValuesError,
        match=f"^{expected_msg}$",
    ):
        literalize(
            source=_to_source(
                data={"tags": ["admin"], "extra": None},
                input_format=input_format,
            ),
            input_format=input_format,
            language=MOJO,
            pre_indent_level=0,
            include_delimiters=True,
        )


# --- Tests that should NOT raise ---


@pytest.mark.parametrize(argnames="input_format", argvalues=ALL_FORMATS)
def test_no_raise_homogeneous_array(input_format: InputFormat) -> None:
    """Homogeneous array does not raise across all formats."""
    literalize(
        source=_to_source(data=[1, 2, 3], input_format=input_format),
        input_format=input_format,
        language=MOJO,
        pre_indent_level=0,
        include_delimiters=True,
    )


@pytest.mark.parametrize(argnames="input_format", argvalues=ALL_FORMATS)
def test_no_raise_homogeneous_dict(input_format: InputFormat) -> None:
    """Homogeneous dict values do not raise across all formats."""
    literalize(
        source=_to_source(
            data={"a": 1, "b": 2},
            input_format=input_format,
        ),
        input_format=input_format,
        language=MOJO,
        pre_indent_level=0,
        include_delimiters=True,
    )


@pytest.mark.parametrize(argnames="input_format", argvalues=ALL_FORMATS)
def test_no_raise_heterogeneous_for_language_supporting_it(
    input_format: InputFormat,
) -> None:
    """Heterogeneous data does not raise for languages that support it."""
    literalize(
        source=_to_source(data=[1, 2.5, 3], input_format=input_format),
        input_format=input_format,
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=True,
    )


@pytest.mark.parametrize(argnames="input_format", argvalues=ALL_FORMATS)
def test_no_raise_uniform_dict_shapes(input_format: InputFormat) -> None:
    """Uniform dict shapes do not raise across all formats (Dhall)."""
    data: _SourceData = [
        {"type": "create", "name": "a"},
        {"type": "update", "name": "b"},
    ]
    literalize(
        source=_to_source(data=data, input_format=input_format),
        input_format=input_format,
        language=Dhall(),
        pre_indent_level=0,
        include_delimiters=True,
    )
