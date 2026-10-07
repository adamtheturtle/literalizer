"""Fallback guards for states not produced by the public renderer.

Built-in formats supply their optional type names, and root collection
inference retains a collection shape. The remaining helper tests cover
absent configuration and scalar inference that public inputs cannot reach.
"""

from typing import TYPE_CHECKING

from literalizer._formatters.fallbacks import (
    collection_or_default,
    value_or_default,
)

if TYPE_CHECKING:
    from tests.integration.parsed_values import ParsedValue


def test_absent_value_uses_default() -> None:
    """An absent optional formatter setting selects its default."""
    assert value_or_default(value=None, default="default") == "default"


def test_scalar_inference_uses_source_collection() -> None:
    """Non-collection inference leaves the source opener data intact."""
    source: list[ParsedValue] = [1]
    assert collection_or_default(value=None, default=source) is source
    assert collection_or_default(value=5, default=source) is source
