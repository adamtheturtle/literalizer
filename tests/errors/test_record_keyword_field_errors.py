"""Errors for record fields that cannot escape reserved identifiers."""

import pytest

from literalizer import InputFormat, Language, literalize
from literalizer.exceptions import UnrepresentableInputError
from literalizer.languages import Cpp, Crystal, Java


@pytest.mark.parametrize(
    argnames=("language", "keyword"),
    argvalues=[
        (
            Java(heterogeneous_strategy=Java.heterogeneous_strategies.RECORD),
            "class",
        ),
        (
            Cpp(heterogeneous_strategy=Cpp.heterogeneous_strategies.RECORD),
            "template",
        ),
        (
            Crystal(
                heterogeneous_strategy=Crystal.heterogeneous_strategies.RECORD
            ),
            "initialize",
        ),
    ],
)
def test_unescapable_record_keyword_is_rejected(
    language: Language, keyword: str
) -> None:
    """Reject names reserved for generated record fields."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match=rf"record field name '{keyword}' is reserved",
    ):
        literalize(
            source=f'[{{"{keyword}": 1}}]',
            input_format=InputFormat.JSON,
            language=language,
        )
