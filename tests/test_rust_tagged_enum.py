"""Unit tests for Rust's tagged-enum heterogeneous-value strategy.

Golden-file coverage for the rendering paths (dict-mixed, sibling-list,
sibling-dict heterogeneity, and integer-width variant selection) lives
in ``tests/integration/cases/*/Rust_heterogeneous_strategy_tagged_enum*.rs``.
These unit tests cover the error contract, which the integration
framework silently skips.
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
