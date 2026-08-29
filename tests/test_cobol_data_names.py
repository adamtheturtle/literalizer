"""Tests for COBOL data-name disambiguation.

These drive the name suffixing directly, a thousand collisions deep,
which no document of a size worth keeping would reach through the
public API (issue #4699).
"""

from literalizer.languages.cobol import (
    _NameScope,  # pyright: ignore[reportPrivateUsage]
    _unique_cobol_name,  # pyright: ignore[reportPrivateUsage]
)


def test_cobol_collision_suffix_probe_advances() -> None:
    """Repeated collisions retain the next suffix for their base."""
    scope = _NameScope(level=5, used=set(), next_suffix={})
    collision_count = 1_000

    names = [
        _unique_cobol_name(base="F-A-B", scope=scope)
        for _ in range(collision_count)
    ]

    assert names[:3] == ["F-A-B", "F-A-B-2", "F-A-B-3"]
    assert names[-1] == "F-A-B-1000"
    assert scope.next_suffix["F-A-B"] == collision_count + 1


def test_cobol_collision_suffix_skips_preexisting_name() -> None:
    """A scope without a cursor can still skip an occupied suffix."""
    expected_next_suffix = 4
    scope = _NameScope(
        level=5,
        used={"F-A-B", "F-A-B-2"},
        next_suffix={},
    )

    assert _unique_cobol_name(base="F-A-B", scope=scope) == "F-A-B-3"
    assert scope.next_suffix["F-A-B"] == expected_next_suffix
