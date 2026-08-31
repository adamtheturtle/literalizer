"""Swift tuple-record validation branch coverage."""

import pytest

from literalizer import InputFormat, literalize
from literalizer._language import Language
from literalizer.exceptions import UnrepresentableInputError
from literalizer.languages import Swift


def _tuple_record_swift() -> Language:
    """Return Swift configured for the affected option combination."""
    return Swift(
        heterogeneous_strategy=Swift.heterogeneous_strategies.RECORD,
        sequence_format=Swift.sequence_formats.TUPLE,
    )


def test_ordered_map_nested_tuple_record_is_rejected() -> None:
    """Ordered-map traversal finds a record below two tuple levels."""
    with pytest.raises(expected_exception=UnrepresentableInputError):
        literalize(
            source="!!omap\n- groups:\n  - - id: 1\n",
            input_format=InputFormat.YAML,
            language=_tuple_record_swift(),
        )


def test_scalar_has_no_nested_tuple_record() -> None:
    """The recursive validation accepts a scalar leaf."""
    literalize(
        source="1",
        input_format=InputFormat.JSON,
        language=_tuple_record_swift(),
    )
