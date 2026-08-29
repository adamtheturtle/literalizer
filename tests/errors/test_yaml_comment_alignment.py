"""Tests for YAML comment alignment errors.

The input is built by patching what the YAML parser hands back, so
there is no source string a rejection manifest could declare.
"""

import importlib

import pytest

import literalizer
from literalizer._comments import CollectionComments
from literalizer.languages import Java


def _misaligned_comments(
    *,
    ruamel_data: object,
    nested: bool,
    hoist_nested_inline: bool,
) -> CollectionComments:
    """Return deliberately malformed parser metadata for an error test."""
    del ruamel_data, nested, hoist_nested_inline
    return CollectionComments(elements=(), trailing=("trailing",))


def test_literalize_fails_on_yaml_comment_misalignment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The public API fails hard when parser comment slots are
    misaligned.
    """
    literalize_module = importlib.import_module(name="literalizer._literalize")
    monkeypatch.setattr(
        target=literalize_module,
        name="extract_yaml_comments",
        value=_misaligned_comments,
    )

    with pytest.raises(
        expected_exception=ValueError,
        match=r"zip\(\) argument 2 is longer than argument 1",
    ):
        literalizer.literalize(
            source="outer:\n  # nested\n  keep: 1\n  drop: 2\n",
            input_format=literalizer.InputFormat.YAML,
            language=Java(),
            collection_layout=literalizer.CollectionLayout.MULTILINE,
        )
