"""Set values are never silently rendered as sequence values."""

import pytest

import literalizer
from literalizer._language import LanguageCls
from literalizer.exceptions import UnrepresentableInputError
from literalizer.languages import Cpp, D, Haxe, Nim, Raku

_SEQUENCE_SURROGATE_LANGUAGES: tuple[LanguageCls, ...] = (
    Cpp,
    D,
    Haxe,
    Nim,
    Raku,
)


@pytest.mark.parametrize(
    argnames="language_cls",
    argvalues=_SEQUENCE_SURROGATE_LANGUAGES,
    ids=[language.__name__ for language in _SEQUENCE_SURROGATE_LANGUAGES],
)
def test_set_sequence_surrogate_is_rejected(language_cls: LanguageCls) -> None:
    """A set format backed by a sequence rejects the tagged YAML value."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="cannot preserve native set semantics",
    ):
        literalizer.literalize(
            source="s: !!set\n  ? a\n  ? b\n",
            input_format=literalizer.InputFormat.YAML,
            language=language_cls(),
        )
