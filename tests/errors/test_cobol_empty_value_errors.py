"""COBOL errors for values that collapse to placeholder spaces."""

import pytest

from literalizer import InputFormat, literalize
from literalizer.exceptions import (
    UnrepresentableEmptyDictError,
    UnrepresentableInputError,
    UnrepresentableStringError,
)
from literalizer.languages import Cobol


def test_cobol_rejects_empty_string_literal() -> None:
    """Plain COBOL never emits an illegal zero-length literal."""
    with pytest.raises(expected_exception=UnrepresentableStringError):
        literalize(
            source='{"e": ""}',
            input_format=InputFormat.JSON,
            language=Cobol(),
        )


@pytest.mark.parametrize(
    argnames=("source", "expected"),
    argvalues=[
        ("null", UnrepresentableInputError),
        ("{}", UnrepresentableEmptyDictError),
        ("[]", UnrepresentableInputError),
    ],
)
def test_cobol_rejects_collapsed_placeholders(
    source: str,
    expected: type[Exception],
) -> None:
    """Null and empty containers never silently become spaces."""
    with pytest.raises(expected_exception=expected):
        literalize(
            source=source,
            input_format=InputFormat.JSON,
            language=Cobol(),
        )
