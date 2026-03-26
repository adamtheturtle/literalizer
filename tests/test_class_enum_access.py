"""Test class-level format Enum access via the LanguageCls meta-class."""

import pytest

from literalizer import LanguageCls
from literalizer.languages import ALL_LANGUAGES


@pytest.mark.parametrize(
    argnames="language_cls",
    argvalues=sorted(ALL_LANGUAGES, key=lambda c: c.__name__),
    ids=lambda c: c.__name__,
)
def test_format_enums_populated(*, language_cls: LanguageCls) -> None:
    """Every language exposes at least one member in each format Enum."""
    assert len(language_cls.SequenceFormats) >= 1
    assert len(language_cls.SetFormats) >= 1
    assert len(language_cls.BytesFormats) >= 1
    assert len(language_cls.DateFormats) >= 1
    assert len(language_cls.DatetimeFormats) >= 1
    assert len(language_cls.VariableTypeHints) >= 1
    assert len(language_cls.DeclarationStyles) >= 1
    assert len(language_cls.DictFormats) >= 1
    assert len(language_cls.IntegerFormats) >= 1
    assert len(language_cls.NumericSeparators) >= 1
    assert len(language_cls.StringFormats) >= 1
    assert len(language_cls.TrailingCommas) >= 1
