"""Nested-shape scope tests for Rust tuple-with-Vec rendering."""

import literalizer
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


def test_tuple_inside_tuple_is_collected_independently() -> None:
    """A nested mixed-shape tuple is valid in its outer tuple slot."""
    assert '("x", (1, (2, vec![3])))' in _render(source='{"x": [1, [2, [3]]]}')
