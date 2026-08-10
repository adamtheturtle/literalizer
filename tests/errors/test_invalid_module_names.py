"""Module-name identifier validation tests."""

import pytest

from literalizer import LanguageCls
from literalizer.exceptions import InvalidModuleNameError
from literalizer.languages import ALL_LANGUAGES, Java

_MODULE_LANGUAGES = sorted(
    (
        language_cls
        for language_cls in ALL_LANGUAGES
        if language_cls.supports_module_name
    ),
    key=lambda language_cls: language_cls.__name__,
)


@pytest.mark.parametrize(
    argnames="language_cls",
    argvalues=_MODULE_LANGUAGES,
    ids=[language_cls.__name__ for language_cls in _MODULE_LANGUAGES],
)
def test_module_languages_reject_source_injection(
    language_cls: LanguageCls,
) -> None:
    """Every named-scope language rejects a non-identifier module name."""
    with pytest.raises(
        expected_exception=InvalidModuleNameError,
        match="cannot use module_name 'X \\{\\} class Y'",
    ):
        language_cls(module_name="X {} class Y")


def test_java_accepts_identifier_module_name() -> None:
    """A normal module identifier remains accepted."""
    language = Java(module_name="MyModule")

    assert isinstance(language, Java)
