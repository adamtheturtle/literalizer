"""Tests for retaining ruamel nodes used by comment rendering.

The subject is which parser nodes survive a walk, not any rendered
output, so there is nothing for a golden file to hold (issue #4699).
"""

from collections.abc import Mapping
from typing import TYPE_CHECKING

import pytest
from ruamel.yaml.comments import CommentedMap

from literalizer._literalize import (
    _collect_yaml_comment_nodes,  # pyright: ignore[reportPrivateUsage]
    _normalized_mapping_objects,  # pyright: ignore[reportPrivateUsage]
)

if TYPE_CHECKING:
    from literalizer._types import Scalar, Value


def test_yaml_comment_mapping_is_indexed_once(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Collecting children performs one mapping scan, not one per key."""
    calls = 0

    def counting_normalize(
        *, mapping: Mapping[object, object]
    ) -> dict[object, object]:
        """Count complete mapping indexes."""
        nonlocal calls
        calls += 1
        return _normalized_mapping_objects(mapping=mapping)

    monkeypatch.setattr(
        target="literalizer._literalize._normalized_mapping_objects",
        name=counting_normalize,
    )
    size = 1_000
    value: dict[Scalar, Value] = {}
    for index in range(size):
        value[f"key_{index}"] = index
    raw = CommentedMap(value)

    _collect_yaml_comment_nodes(
        value=value,
        raw_value=raw,
        out={},
    )

    assert calls == 1
