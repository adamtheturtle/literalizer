"""Hypothesis roundtrip tests for literalizer converter."""

import ast
import json

from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from literalizer import (
    InputFormat,
    literalize,
)
from literalizer.languages import Python

# Use LIST sequence format so that ast.literal_eval returns plain lists,
# matching the JSON input directly without any conversion step.
PYTHON = Python(
    date_format=Python.date_formats.PYTHON,
    datetime_format=Python.datetime_formats.PYTHON,
    bytes_format=Python.bytes_formats.HEX,
    sequence_format=Python.sequence_formats.LIST,
    set_format=Python.set_formats.SET,
    variable_type_hints=Python.variable_type_hints_formats.NEVER,
)

type _JSONScalar = str | int | float | bool | None

type _JSONValue = _JSONScalar | list[_JSONValue] | dict[str, _JSONValue]


# Characters valid in JSON strings: Unicode letters (L), marks (M), numbers
# (N), punctuation (P), symbols (S), and separators (Z). Control characters
# (category C) are excluded because JSON forbids raw control characters,
# and ``\x00`` is excluded explicitly because json.dumps refuses null bytes.
json_text = st.text(
    alphabet=st.characters(
        categories=("L", "M", "N", "P", "S", "Z"), exclude_characters="\x00"
    ),
    max_size=20,
)
json_scalars: st.SearchStrategy[_JSONValue] = (
    st.none()
    | st.booleans()
    | st.integers()
    # ``nan`` and ``inf`` are excluded because JSON does not support them.
    | st.floats(allow_nan=False, allow_infinity=False)
    | json_text
)


def _json_collection_values(
    children: st.SearchStrategy[_JSONValue],
) -> st.SearchStrategy[_JSONValue]:
    """Return recursive JSON collection strategies."""
    return st.lists(elements=children, max_size=3) | st.dictionaries(
        keys=json_text,
        values=children,
        max_size=3,
    )


json_values: st.SearchStrategy[_JSONValue] = st.recursive(
    base=json_scalars,
    extend=_json_collection_values,
    # ``max_leaves`` caps total nodes generated; the recursive strategy
    # is by far the dominant cost in these tests, so a tight bound here
    # is the biggest single performance lever without losing
    # meaningful coverage.
    max_leaves=15,
)
json_arrays = st.lists(elements=json_values, max_size=5)
json_objects = st.dictionaries(keys=json_text, values=json_values, max_size=5)


@settings(deadline=None)
@given(data=json_arrays)
def test_roundtrip_array(data: list[_JSONValue]) -> None:
    """JSON array -> Python literal -> ast.literal_eval round-trips."""
    result = literalize(
        source=json.dumps(obj=data),
        input_format=InputFormat.JSON,
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=None,
    )
    parsed = ast.literal_eval(node_or_string=result.code)
    assert parsed == data


@settings(deadline=None)
@given(data=json_scalars)
def test_roundtrip_scalar(data: _JSONScalar) -> None:
    """Scalar -> Python literal -> ast.literal_eval round-trips."""
    result = literalize(
        source=json.dumps(obj=data),
        input_format=InputFormat.JSON,
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=False,
        variable_form=None,
    )
    parsed = ast.literal_eval(node_or_string=result.code)
    assert parsed == data


# ``st.dictionaries`` internally filters draws to ensure unique keys, which
# can accumulate enough filtered examples to trigger the ``filter_too_much``
# health check on unlucky seeds.  The filtering is expected behavior here,
# so we suppress the check rather than change the strategy.
@given(data=json_objects)
@settings(deadline=None, suppress_health_check=[HealthCheck.filter_too_much])
def test_roundtrip_dict(data: dict[str, _JSONValue]) -> None:
    """JSON object -> Python literal -> ast.literal_eval round-trips."""
    result = literalize(
        source=json.dumps(obj=data),
        input_format=InputFormat.JSON,
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=None,
    )
    parsed = ast.literal_eval(node_or_string=result.code)
    assert parsed == data
