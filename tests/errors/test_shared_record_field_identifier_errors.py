"""Lexical field-identifier checks in the shared ``RECORD`` renderer."""

import pytest

from literalizer import InputFormat, Language, LanguageCls, literalize
from literalizer.exceptions import UnrepresentableInputError
from literalizer.languages import (
    C,
    Cpp,
    Crystal,
    D,
    Go,
    Java,
    Kotlin,
    Odin,
    Python,
    Scala,
    Swift,
    V,
)

# Zig safely renders this key as a quoted identifier, so it is covered by its
# existing identifier-escaping tests.  The remaining affected languages use a
# shared renderer but have no syntax for this key in a generated record field.
_UNESCAPABLE_FIELD_LANGUAGES: tuple[LanguageCls, ...] = (
    C,
    Cpp,
    Crystal,
    D,
    Java,
    Kotlin,
    Odin,
    Python,
    Scala,
    Swift,
    V,
)


def _record_strategy_for(language_cls: LanguageCls) -> object:
    """Return *language_cls*'s ``RECORD`` heterogeneous strategy."""
    return next(
        strategy
        for strategy in language_cls().heterogeneous_strategies
        if strategy.name == "RECORD"
    )


@pytest.mark.parametrize(
    argnames="language_cls",
    argvalues=_UNESCAPABLE_FIELD_LANGUAGES,
    ids=[
        language_cls.__name__ for language_cls in _UNESCAPABLE_FIELD_LANGUAGES
    ],
)
def test_record_strategy_rejects_hyphenated_field_key(
    language_cls: LanguageCls,
) -> None:
    """A hyphenated key fails before a target language returns invalid
    source.
    """
    language: Language = language_cls(
        heterogeneous_strategy=_record_strategy_for(language_cls=language_cls),
    )
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="lexical field identifier",
    ):
        literalize(
            source='[{"a-b": 1}]',
            input_format=InputFormat.JSON,
            language=language,
        )


def test_record_strategy_rejects_colliding_transformed_field_keys() -> None:
    """Keys that map to one Go field name fail before source is
    returned.
    """
    language = Go(
        heterogeneous_strategy=Go.heterogeneous_strategies.RECORD,
    )
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="collides with another key",
    ):
        literalize(
            source='[{"a-b": 1, "a_b": 2}]',
            input_format=InputFormat.JSON,
            language=language,
        )
