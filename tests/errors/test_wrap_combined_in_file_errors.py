"""Error contracts for languages that cannot wrap combined variable
forms.
"""

import pytest

from literalizer import LanguageCls
from literalizer.exceptions import WrapCombinedInFileNotSupportedError
from literalizer.languages import ALL_LANGUAGES


def _language_class_name(language_cls: LanguageCls, /) -> str:
    """Return the language class name."""
    return language_cls.__name__


_SORTED_LANGUAGES: list[LanguageCls] = sorted(
    ALL_LANGUAGES,
    key=_language_class_name,
)

_UNSUPPORTED_COMBINED_LANGUAGES: list[LanguageCls] = [
    cls
    for cls in _SORTED_LANGUAGES
    if not any(
        style.value.supports_redefinition for style in cls.DeclarationStyles
    )
]


@pytest.mark.parametrize(
    argnames="language_cls",
    argvalues=_UNSUPPORTED_COMBINED_LANGUAGES,
    ids=_language_class_name,
)
def test_wrap_combined_in_file_unsupported_raises(
    *,
    language_cls: LanguageCls,
) -> None:
    """Check wrap_combined_in_file raises when redefinition is unsupported."""
    with pytest.raises(expected_exception=WrapCombinedInFileNotSupportedError):
        _ = language_cls().wrap_combined_in_file(
            declaration="x = 1",
            assignment="x = 2",
            variable_name="x",
            body_preamble=(),
        )
