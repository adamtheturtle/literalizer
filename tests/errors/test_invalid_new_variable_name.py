"""Declaration-name checks driven by each language's own reserved set.

The fixed-name rejections are declared in ``tests/errors/rejections``
and run by ``test_rejections.py``.  What is left here is the pair a
manifest cannot express -- a manifest applies one name to every
language it selects, and these read the name out of the language
itself -- together with the acceptances that show where each
restriction stops.
"""

import re

import pytest
from beartype import beartype

from literalizer import (
    InputFormat,
    LanguageCls,
    NewVariable,
    literalize,
    literalize_call,
)
from literalizer.exceptions import ReservedVariableNameError
from literalizer.languages import (
    ALL_LANGUAGES,
    Erlang,
    Fortran,
    JavaScript,
    Swift,
    TypeScript,
)


def test_fortran_accepts_variable_name_at_standard_limit() -> None:
    """The 63-character Fortran name boundary remains valid."""
    literalize(
        source="1",
        input_format=InputFormat.JSON,
        language=Fortran(),
        variable_form=NewVariable(
            name="v" * 63,
            modifiers=frozenset(),
        ),
    )


@pytest.mark.parametrize(
    argnames="language_cls",
    argvalues=[JavaScript, TypeScript],
    ids=lambda language_cls: language_cls.__name__,
)
def test_ecmascript_reserved_property_call_remains_valid(
    language_cls: LanguageCls,
) -> None:
    """Reserved variable names do not block valid property calls."""
    result = literalize_call(
        source="[1]",
        input_format=InputFormat.JSON,
        language=language_cls(),
        target_function="foo.class",
        parameter_names=["value"],
    )

    assert result.code == "foo.class({ value: 1 });"


def test_erlang_lowercase_keyword_is_valid_variable_name() -> None:
    """Erlang variables capitalize names, so lowercase keywords are
    valid.
    """
    result = literalize(
        source="1",
        input_format=InputFormat.JSON,
        language=Erlang(),
        variable_form=NewVariable(name="if", modifiers=frozenset()),
        wrap_in_file=True,
    )

    assert result.code == (
        "-module(module).\n-export([x/0]).\nx() ->\n    If = 1,\n    If."
    )


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


# Jsonnet declares reserved identifiers for its call parameter and
# call target names while naming no variable at all, so a
# ``NewVariable`` there is refused for a different reason (issue
# #4549).
_LANGUAGES_WITH_RESERVED_NEW_VARIABLE_NAMES = tuple(
    language_cls
    for language_cls in sorted(ALL_LANGUAGES, key=lambda cls: cls.__name__)
    if language_cls.reserved_variable_identifiers
    and language_cls.supports_variable_names
)


@pytest.mark.parametrize(
    argnames="language_cls",
    argvalues=_LANGUAGES_WITH_RESERVED_NEW_VARIABLE_NAMES,
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
                literalize(
                    source="1",
                    input_format=InputFormat.JSON,
                    language=language_cls(),
                    variable_form=NewVariable(
                        name=spelling,
                        modifiers=frozenset(),
                    ),
                    wrap_in_file=True,
                )


_RECORD_PREFIX_LANGUAGES = tuple(
    language_cls
    for language_cls in sorted(ALL_LANGUAGES, key=lambda cls: cls.__name__)
    if language_cls.supports_record_struct_name_prefix
)


@pytest.mark.parametrize(
    argnames="language_cls",
    argvalues=_RECORD_PREFIX_LANGUAGES,
    ids=lambda language_cls: language_cls.__name__,
)
def test_generated_record_name_is_reserved_for_record_strategy(
    language_cls: LanguageCls,
) -> None:
    """A declaration cannot shadow an auto-generated record type."""
    prefix = language_cls.__dataclass_fields__[
        "record_struct_name_prefix"
    ].default
    record_strategy = next(
        strategy
        for strategy in language_cls.HeterogeneousStrategies
        if strategy.name == "RECORD"
    )
    language = language_cls(heterogeneous_strategy=record_strategy)

    with pytest.raises(expected_exception=ReservedVariableNameError):
        literalize(
            source='[{"id": 1}]',
            input_format=InputFormat.JSON,
            language=language,
            variable_form=NewVariable(
                name=f"{prefix}0",
                modifiers=frozenset(),
            ),
            wrap_in_file=True,
        )


def test_generated_record_name_is_valid_without_record_strategy() -> None:
    """The generated-name reservation is specific to RECORD output."""
    result = literalize(
        source="1",
        input_format=InputFormat.JSON,
        language=Swift(),
        variable_form=NewVariable(
            name="Record0",
            modifiers=frozenset(),
        ),
        wrap_in_file=True,
    )

    assert "let Record0 = 1" in result.code
