"""Composition metadata describes every emitted native operand."""

from literalizer import InputFormat, literalize_native_calls
from literalizer.languages import ObjectiveC


def test_native_batch_metadata_covers_emitted_values_only() -> None:
    """Later rows contribute types without leaking unused source
    values.
    """
    result = literalize_native_calls(
        source='[["first", true], [42, false]]',
        input_format=InputFormat.JSON,
        language=ObjectiveC(),
        invocation={
            "function": "consume",
            "parameter-types": ["id"],
            "return-type": "void",
            "arguments": [{"input": 0}],
        },
    )
    assert result.source_data == [["first"], [42]]
    assert {str, int}.issubset(result.types_present)
    assert bool not in result.types_present
    assert result.is_call_statement
    assert not result.uses_existing_variable
