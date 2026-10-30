"""C++ headers alone cannot replace record declarations (#6584)."""

import enum

import pytest

from literalizer import (
    InputFormat,
    LanguageCls,
    NewVariable,
    literalize,
    literalize_call,
    literalize_call_with_declarations,
)
from literalizer.languages import Cpp


@pytest.mark.parametrize(
    argnames="version", argvalues=list(Cpp.version_formats)
)
@pytest.mark.parametrize(argnames="known_reference", argvalues=[False, True])
def test_cpp_composed_record_dependencies(
    *, version: enum.Enum, known_reference: bool
) -> None:
    """Keep the original record and headers without a canonical
    replacement.
    """
    language_cls: LanguageCls = Cpp
    language = language_cls(
        language_version=version,
        heterogeneous_strategy=Cpp.heterogeneous_strategies.RECORD,
    )
    declaration = literalize(
        source='{"name": "first", "values": [1, 2]}',
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
        ref_values=(
            {"item": {"name": "first", "values": [1, 2]}}
            if known_reference
            else None
        ),
    )
    result = literalize_call_with_declarations(
        language=language,
        declarations=[declaration],
        call=call,
        extra_body_preamble=(),
        extra_class_preamble=(),
        extra_preamble=(),
    )
    for entry in declaration.preamble:
        assert entry in result.code
