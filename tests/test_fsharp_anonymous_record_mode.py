"""Public API coverage for opt-in F# anonymous records."""

import pytest

from literalizer import (
    InputFormat,
    literalize,
)
from literalizer.exceptions import (
    HeterogeneousScalarCollectionError,
    UnrepresentableInputError,
)
from literalizer.languages import FSharp


@pytest.mark.parametrize(
    argnames=("source", "input_format", "message"),
    argvalues=[
        ('{"not-a-field": 1}', InputFormat.JSON, "field"),
        ('{"let": 1}', InputFormat.JSON, "field"),
        ("1: one\n", InputFormat.YAML, "field"),
        ("{}", InputFormat.JSON, "empty records"),
        ('{"x": null}', InputFormat.JSON, "NoneType"),
        ('[{"x": 1}, {"x": "one"}]', InputFormat.JSON, "uniform"),
        ('[{"x": 1}, {"y": 1}]', InputFormat.JSON, "uniform"),
        ("--- !!omap\n- a: 1\n", InputFormat.YAML, "ordered maps"),
        ("--- !!set\na:\n", InputFormat.YAML, "set"),
    ],
)
def test_anonymous_record_mode_rejects_unsupported_input(
    source: str, input_format: InputFormat, message: str
) -> None:
    """Invalid native shapes fail clearly instead of emitting bad F#."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError, match=message
    ):
        _ = literalize(
            source=source,
            input_format=input_format,
            language=FSharp(dict_format=FSharp.dict_formats.ANONYMOUS_RECORD),
        )


def test_anonymous_record_mode_conflicts_with_json_node() -> None:
    """The two independent representations cannot be selected together."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError, match="json_type"
    ):
        _ = literalize(
            source='{"x": 1}',
            input_format=InputFormat.JSON,
            language=FSharp(
                dict_format=FSharp.dict_formats.ANONYMOUS_RECORD,
                json_type=FSharp.json_types.SYSTEM_TEXT_JSON_NODE,
            ),
        )


def test_anonymous_record_mode_rejects_mixed_scalar_list() -> None:
    """Native F# lists cannot contain unrelated scalar types."""
    with pytest.raises(expected_exception=HeterogeneousScalarCollectionError):
        _ = literalize(
            source='[1, "hello"]',
            input_format=InputFormat.JSON,
            language=FSharp(dict_format=FSharp.dict_formats.ANONYMOUS_RECORD),
        )
