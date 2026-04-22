"""Cross-language tests for the default heterogeneous-strategy error
contract.

Languages with an opt-in wrapping strategy (e.g. Rust's ``TAGGED_ENUM``)
must still raise on heterogeneous input under the default ``ERROR``
strategy.  The integration framework catches
``HeterogeneousCollectionError`` and silently skips, so the error
contract has no golden-file surface and needs unit coverage.
"""

import pytest

from literalizer import InputFormat, literalize
from literalizer.exceptions import (
    HeterogeneousScalarCollectionError,
    HeterogeneousSiblingListsError,
)
from literalizer.languages import Rust


def test_default_strategy_is_error() -> None:
    """Default Rust spec still raises on heterogeneous scalars."""
    with pytest.raises(expected_exception=HeterogeneousScalarCollectionError):
        literalize(
            source='{"a": 1, "b": "x"}',
            input_format=InputFormat.JSON,
            language=Rust(),
        )


def test_sibling_lists_still_error_without_opt_in() -> None:
    """Default Rust spec raises ``HeterogeneousSiblingListsError`` for
    sibling-list heterogeneity.
    """
    with pytest.raises(expected_exception=HeterogeneousSiblingListsError):
        literalize(
            source='[[1, 2], ["a", "b"]]',
            input_format=InputFormat.JSON,
            language=Rust(),
        )
