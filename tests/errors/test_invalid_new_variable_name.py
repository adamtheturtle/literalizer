"""Declaration-name checks driven by each language's own reserved set.

The fixed-name rejections are declared in ``tests/errors/rejections``
and run by ``test_rejections.py``. The remaining tests read reserved
names from the language itself, rather than applying one manifest name
to every selected language. Acceptance boundaries use shared golden files.
"""

import re

import pytest
from beartype import beartype

from literalizer import (
    InputFormat,
    LanguageCls,
    NewVariable,
    literalize,
)
from literalizer.exceptions import ReservedVariableNameError
from literalizer.languages import ALL_LANGUAGES


def _language_class_name(language_cls: LanguageCls, /) -> str:
    """Return the language class name."""
    return language_cls.__name__


@beartype
def _spellings(*, name: str, language_cls: LanguageCls) -> tuple[str, ...]:
    """Return the spellings of *name* the language must refuse.

    A case-sensitive language reserves the one spelling it declares.
    A case-insensitive one reads every casing of it as the same word,
    so an upper-cased and a capitalized spelling have to be refused
    too.
    """
    if language_cls.reserved_variable_identifiers_case_sensitive:
        return (name,)
    spellings = (name, name.upper(), name.capitalize())
    return tuple(dict.fromkeys(spellings))


# A target can reserve call names without supporting named variables.
# Select declaration-name cases only where those declarations apply (#4549).


@pytest.mark.parametrize(
    argnames="language_cls",
    argvalues=tuple(
        language_cls
        for language_cls in sorted(ALL_LANGUAGES, key=_language_class_name)
        if len(language_cls.reserved_variable_identifiers) > 0
        and language_cls.supports_variable_names
    ),
    ids=lambda language_cls: language_cls.__name__,
)
def test_all_declared_reserved_names_raise(
    language_cls: LanguageCls,
) -> None:
    """Every language-specific reserved declaration name is rejected.

    The message is asserted here rather than in a manifest because it
    names the identifier, which differs for every language.  A language
    whose reserved set is case-insensitive is fed each name in other
    spellings too, so that dropping the fold would fail here rather
    than let a differently-cased keyword through.
    """
    for reserved_name in sorted(language_cls.reserved_variable_identifiers):
        for spelling in _spellings(
            name=reserved_name,
            language_cls=language_cls,
        ):
            expected_message = (
                f"{language_cls.__name__} cannot use NewVariable name "
                f"{spelling!r}: it is a reserved identifier"
            )
            with pytest.raises(
                expected_exception=ReservedVariableNameError,
                match=f"^{re.escape(pattern=expected_message)}$",
            ):
                _ = literalize(
                    source="1",
                    input_format=InputFormat.JSON,
                    language=language_cls(),
                    variable_form=NewVariable(
                        name=spelling,
                        modifiers=frozenset(),
                    ),
                    wrap_in_file=True,
                )
