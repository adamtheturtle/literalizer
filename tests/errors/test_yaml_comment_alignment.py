"""Tests for YAML comment alignment errors."""

import pytest

from literalizer._comments import CollectionComments
from literalizer._literalize import (
    _filter_collection_comments,  # pyright: ignore[reportPrivateUsage]
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
