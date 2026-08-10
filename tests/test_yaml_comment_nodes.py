"""Focused tests for YAML comment-node identity collection."""

from typing import TYPE_CHECKING

from ruamel.yaml.comments import CommentedMap, CommentedSeq, CommentedSet

from literalizer._literalize import (
    _collect_yaml_comment_nodes,  # pyright: ignore[reportPrivateUsage]
)

if TYPE_CHECKING:
    from literalizer._types import Value


def test_yaml_comment_nodes_ignore_transformed_missing_keys() -> None:
    """Transformed mappings may contain keys absent from the raw node."""
    value: Value = {"missing": 1}
    raw_value = CommentedMap({"present": 1})
    out: dict[int, CommentedSeq | CommentedMap | CommentedSet] = {}

    _collect_yaml_comment_nodes(value=value, raw_value=raw_value, out=out)

    assert out == {id(value): raw_value}
