"""Focused tests for YAML nested-comment bookkeeping."""

import pytest
from ruamel.yaml.comments import CommentedMap, CommentedSeq, CommentedSet

from literalizer._comments import CollectionComments, ElementComments
from literalizer._literalize import (
    _collect_yaml_comment_nodes,  # pyright: ignore[reportPrivateUsage]
    _filter_collection_comments,  # pyright: ignore[reportPrivateUsage]
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


def test_filter_collection_comments_tracks_rendered_entries() -> None:
    """Comments for omitted entries are not assigned to later values."""
    first = ElementComments(before=("first",), inline="")
    omitted = ElementComments(before=(), inline="omitted")
    last = ElementComments(before=(), inline="last")
    comments = CollectionComments(
        elements=(first, omitted, last), trailing=("trailing",)
    )

    filtered = _filter_collection_comments(
        collection_comments=comments,
        keep=(True, False, True),
    )

    assert filtered == CollectionComments(
        elements=(first, last), trailing=("trailing",)
    )


def test_filter_collection_comments_fails_on_misalignment() -> None:
    """An internal comment-slot mismatch fails hard."""
    comments = CollectionComments(elements=(), trailing=())

    with pytest.raises(
        expected_exception=ValueError,
        match=r"zip\(\) argument 2 is longer than argument 1",
    ):
        _filter_collection_comments(
            collection_comments=comments,
            keep=(True,),
        )
