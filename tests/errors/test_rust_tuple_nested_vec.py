"""Safety checks for Rust's tuple-with-nested-Vec sequence format."""

import pytest

import literalizer
from literalizer.exceptions import MixedListValuesError
from literalizer.languages import Rust


@pytest.mark.parametrize(
    argnames="source",
    argvalues=[
        "[[1, [2]], [3, 4]]",
        "[[1, []], [2, [3, [4]]]]",
        '[[1, []], [2, [3]], [4, ["x"]]]',
    ],
)
def test_nested_vec_tuple_rejects_nonuniform_siblings(source: str) -> None:
    """A tuple cannot share a Vec slot with a differently typed
    sibling.
    """
    with pytest.raises(expected_exception=MixedListValuesError):
        literalizer.literalize(
            source=source,
            input_format=literalizer.InputFormat.JSON,
            language=Rust(
                sequence_format=Rust.sequence_formats.TUPLE_NESTED_VEC
            ),
        )
