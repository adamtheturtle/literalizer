"""Nested-shape scope tests for Rust tuple-with-Vec rendering."""

import pytest

import literalizer
from literalizer.exceptions import MixedListValuesError
from literalizer.languages import Rust


def _render(*, source: str) -> str:
    """Render *source* with the nested-Vec tuple format."""
    return literalizer.literalize(
        source=source,
        input_format=literalizer.InputFormat.JSON,
        language=Rust(sequence_format=Rust.sequence_formats.TUPLE_NESTED_VEC),
    ).code


def test_empty_vec_is_compatible_with_populated_tuple_sibling() -> None:
    """An empty Vec borrows the populated sibling's element type."""
    rendered = _render(source="[[1, []], [2, [3]]]")
    assert "(1, Vec::<i32>::new())" in rendered
    assert "(2, vec![3])" in rendered


def test_trailing_empty_vec_is_compatible_with_populated_sibling() -> None:
    """Compatibility is symmetric when the empty Vec comes second."""
    rendered = _render(source="[[1, [3]], [2, []]]")
    assert "(1, vec![3])" in rendered
    assert "(2, Vec::<i32>::new())" in rendered


def test_populated_vec_slots_do_not_need_empty_vec_inference() -> None:
    """The tuple scan also handles slots where every Vec is populated."""
    rendered = _render(source="[[1, [2]], [3, [4]]]")
    assert "(1, vec![2])" in rendered
    assert "(3, vec![4])" in rendered


def test_empty_vec_does_not_mask_conflicting_populated_siblings() -> None:
    """An empty Vec is a wildcard, not evidence that all siblings
    agree.
    """
    with pytest.raises(expected_exception=MixedListValuesError):
        _render(source='[[1, []], [2, [3]], [4, ["x"]]]')


def test_tuple_inside_tuple_is_collected_independently() -> None:
    """A nested mixed-shape tuple is valid in its outer tuple slot."""
    assert '("x", (1, (2, vec![3])))' in _render(source='{"x": [1, [2, [3]]]}')
