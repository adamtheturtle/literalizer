"""Checks for the shared JSON-native document fast path."""

from literalizer import CollectionLayout
from literalizer._json_native_document import format_json_native_document_fast
from literalizer._types import OrderedMap
from literalizer.languages import Bash


def test_nested_ordered_map_requires_shared_renderer() -> None:
    """An ordered child makes the fast path return to shared rendering."""
    result = format_json_native_document_fast(
        language=Bash(),
        data={"nested": OrderedMap({"first": 1})},
        line_prefix="",
        include_delimiters=True,
        collection_layout=CollectionLayout.COMPACT,
    )

    assert result is None
