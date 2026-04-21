"""Unit tests for Dhall's union-type heterogeneous-value strategy.

Golden-file coverage for the main rendering paths lives in
``tests/integration/cases/*/Dhall_heterogeneous_strategy_union_type*.dhall``.
These unit tests cover error-raising on the default strategy, which
has no golden-file surface (the integration framework catches and
skips heterogeneous errors).
"""

import pytest

from literalizer import InputFormat, literalize
from literalizer.exceptions import (
    HeterogeneousScalarCollectionError,
    HeterogeneousSiblingListsError,
)
from literalizer.languages import Dhall


def test_default_strategy_is_error() -> None:
    """Default Dhall spec still raises on heterogeneous scalars."""
    with pytest.raises(expected_exception=HeterogeneousScalarCollectionError):
        literalize(
            source='{"a": 1, "b": "x"}',
            input_format=InputFormat.JSON,
            language=Dhall(),
        )


def test_sibling_lists_still_error_without_opt_in() -> None:
    """Default Dhall spec raises ``HeterogeneousSiblingListsError`` for
    sibling-list heterogeneity.
    """
    with pytest.raises(expected_exception=HeterogeneousSiblingListsError):
        literalize(
            source='[[1, 2], ["a", "b"]]',
            input_format=InputFormat.JSON,
            language=Dhall(),
        )
