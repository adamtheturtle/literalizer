"""Lisp-family empty-mapping distinction tests."""

import pytest

from literalizer import InputFormat, literalize
from literalizer._language import Language
from literalizer.exceptions import UnrepresentableEmptyDictError
from literalizer.languages import CommonLisp, Scheme


@pytest.mark.parametrize(
    argnames="language",
    argvalues=[CommonLisp(), Scheme()],
)
def test_lisp_languages_reject_empty_mapping(language: Language) -> None:
    """An empty mapping never silently becomes the empty list."""
    with pytest.raises(expected_exception=UnrepresentableEmptyDictError):
        literalize(
            source='{"a": null, "c": {}, "d": []}',
            input_format=InputFormat.JSON,
            language=language,
        )
