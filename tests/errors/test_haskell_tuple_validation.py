"""Resolved public paths must respect Haskell's tuple/Val boundary."""

import pytest

from literalizer import (
    InputFormat,
    NewVariable,
    ValueInput,
    literalize,
    literalize_call,
)
from literalizer.exceptions import IncompatibleFormatsError
from literalizer.languages import Haskell


@pytest.mark.parametrize(
    argnames="source",
    argvalues=["[[[1, 2]]]", "[null, [[1, 2]]]", '[[{"items": [1, 2]}]]'],
)
def test_tuple_call_arguments_are_rejected(source: str) -> None:
    """A generated Val parameter cannot accept a tuple argument."""
    with pytest.raises(
        expected_exception=IncompatibleFormatsError, match="tuple-valued call"
    ):
        _ = literalize_call(
            source=source,
            input_format=InputFormat.JSON,
            language=Haskell(sequence_format=Haskell.sequence_formats.TUPLE),
            target_function="process",
            parameter_names=["value"],
            per_element=True,
            wrap_in_file=True,
        )


@pytest.mark.parametrize(argnames="bound", argvalues=[True, False])
def test_nested_tuple_references_are_rejected(*, bound: bool) -> None:
    """Resolving a reference cannot bypass the inline tuple
    restriction.
    """
    values: dict[str, ValueInput] = {"shared": [1, "x"]}
    with pytest.raises(
        expected_exception=IncompatibleFormatsError,
        match="tuple nested inside",
    ):
        _ = literalize(
            source='[{"$ref":"shared"},{"$ref":"shared"}]',
            input_format=InputFormat.JSON,
            language=Haskell(sequence_format=Haskell.sequence_formats.TUPLE),
            ref_key="$ref",
            bound_refs=values if bound else None,
            ref_values=None if bound else values,
            variable_form=NewVariable(name="my_data", modifiers=frozenset()),
            wrap_in_file=True,
        )


@pytest.mark.parametrize(argnames="per_element", argvalues=[False, True])
def test_tuple_bound_call_arguments_are_rejected(*, per_element: bool) -> None:
    """Resolved bound arguments obey the same Val restriction as
    literals.
    """
    source = '{"$ref":"items"}'
    if per_element:
        source = f"[[{source}]]"
    with pytest.raises(
        expected_exception=IncompatibleFormatsError, match="tuple-valued call"
    ):
        _ = literalize_call(
            source=source,
            input_format=InputFormat.JSON,
            language=Haskell(sequence_format=Haskell.sequence_formats.TUPLE),
            target_function="process",
            parameter_names=["value"],
            per_element=per_element,
            ref_key="$ref",
            bound_refs={"items": [1, 2]},
            wrap_in_file=True,
        )
