"""Calls without reference hints retain declaration helpers in composed
files
(#6581).
"""

import pytest

from literalizer import (
    InputFormat,
    Language,
    NewVariable,
    literalize,
    literalize_call,
    literalize_call_with_declarations,
)
from literalizer.languages import Go, Python, Rust


@pytest.mark.parametrize(
    argnames="language",
    argvalues=[
        Python(heterogeneous_strategy=Python.heterogeneous_strategies.RECORD),
        Go(heterogeneous_strategy=Go.heterogeneous_strategies.RECORD),
        Rust(heterogeneous_strategy=Rust.heterogeneous_strategies.RECORD),
    ],
)
def test_unhinted_call_keeps_record_dependencies(
    language: Language,
) -> None:
    """Keep the producer's complete block when no replacement is
    inferred.
    """
    declaration = literalize(
        source='{"a": 1}',
        input_format=InputFormat.JSON,
        language=language,
        variable_form=NewVariable(name="item", modifiers=frozenset()),
    )
    call = literalize_call(
        source='{"$ref": "item"}',
        input_format=InputFormat.JSON,
        language=language,
        target_function="consume",
        parameter_names=("value",),
        per_element=False,
        ref_key="$ref",
    )
    result = literalize_call_with_declarations(
        language=language,
        declarations=[declaration],
        call=call,
        extra_body_preamble=(),
        extra_class_preamble=(),
        extra_preamble=(),
    )
    assert len(declaration.data_dependent_preamble) > 0
    for entry in declaration.data_dependent_preamble:
        assert entry in result.code
