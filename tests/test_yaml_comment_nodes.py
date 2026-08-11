"""Focused tests for YAML comment-node identity collection."""

from ruamel.yaml.comments import CommentedMap, CommentedSeq, CommentedSet

from literalizer._literalize import (
    _collect_yaml_comment_nodes,  # pyright: ignore[reportPrivateUsage]
)
from literalizer._types import Scalar, Value


def test_yaml_comment_nodes_ignore_transformed_missing_keys() -> None:
    """Transformed mappings may contain keys absent from the raw node."""

    def make_value() -> Value:
        """Return a value with contextual recursive typing."""
        result: dict[Scalar, Value] = {}
        result["missing"] = 1
        return result

    value = make_value()
    raw_value = CommentedMap({"present": 1})
    out: dict[int, CommentedSeq | CommentedMap | CommentedSet] = {}

    _collect_yaml_comment_nodes(value=value, raw_value=raw_value, out=out)

    assert out == {id(value): raw_value}
