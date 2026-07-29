"""Tests for configurable Python union annotations."""

import pytest

from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import Python


@pytest.mark.parametrize(
    argnames=("union_format", "union_syntax", "union_import"),
    argvalues=[
        pytest.param(
            Python.union_formats.TYPING,
            "Union[",
            "from typing import Union",
            id="typing",
        ),
        pytest.param(Python.union_formats.PIPE, " | ", "", id="pipe"),
    ],
)
def test_record_union_format(
    union_format: Python.UnionFormats,
    union_syntax: str,
    union_import: str,
) -> None:
    """Record fields and their imports follow the configured format."""
    language = Python(
        heterogeneous_strategy=Python.heterogeneous_strategies.RECORD,
        union_format=union_format,
    )

    result = literalize(
        source='vals = [09:30:00, "hello"]\n',
        input_format=InputFormat.TOML,
        language=language,
        variable_form=NewVariable(name="my_data", modifiers=frozenset()),
        wrap_in_file=True,
    )

    assert union_syntax in result.code
    if union_import:
        assert union_import in result.code
    else:
        assert "from typing import Union" not in result.code
