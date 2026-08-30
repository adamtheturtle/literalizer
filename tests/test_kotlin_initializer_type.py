"""Focused tests for Kotlin initializer type extraction."""

from literalizer.languages.kotlin import (
    _kotlin_explicit_initializer_type,  # pyright: ignore[reportPrivateUsage]
)


def test_compact_nested_initializer_uses_outer_generics() -> None:
    """Nested calls on one line do not extend the declaration type."""
    assert (
        _kotlin_explicit_initializer_type(
            'listOf<Map<String, Int>>(mapOf<String, Int>("b" to 1))'
        )
        == "List<Map<String, Int>>"
    )
