"""Rejection of same-key-set sibling dicts whose field types conflict
under the shared ``RECORD`` strategy, for every language that opts into
the field-type split in issue #2961.

Two dicts with the same key set share one generated declaration, but
when a field's scalar value type differs between them one declaration
cannot describe both: it would take the field types of the first dict
and the literal for the other dict would not compile.  The shared record
strategy now splits such dicts into distinct record shapes (issue #2888,
extended to these languages by issue #2961), so sibling lists spanning
them fail the mixed-record-shape gate with
:class:`~literalizer.exceptions.HeterogeneousSiblingListsError` rather
than silently emitting mismatched field types.  A ``record_shape_names``
entry whose key set splits this way cannot identify one declaration, so
it raises :class:`~literalizer.exceptions.UnrepresentableInputError`;
only the languages that expose custom record names can exercise that
contract.  Rust, Go, and Java carry their own equivalents of these
tests, so they are covered separately.
"""

import textwrap

import pytest

from literalizer import InputFormat, Language, LanguageCls, literalize
from literalizer.exceptions import (
    HeterogeneousSiblingListsError,
    UnrepresentableInputError,
)
from literalizer.languages import (
    C,
    Cpp,
    Crystal,
    D,
    Kotlin,
    Nim,
    Odin,
    Scala,
    Swift,
    V,
    Zig,
)

_SCALAR_TYPE_CONFLICT_YAML = textwrap.dedent(
    text="""\
    - a: 1
    - a: hello
    """,
)

_CUSTOM_NAME_SPLIT_YAML = textwrap.dedent(
    text="""\
    first:
      a: 1
    second:
      a: hello
    """,
)

_FIELD_TYPE_SPLIT_LANGUAGES: tuple[LanguageCls, ...] = (
    C,
    Cpp,
    Crystal,
    D,
    Kotlin,
    Nim,
    Odin,
    Scala,
    Swift,
    V,
    Zig,
)

# The languages whose ``RECORD`` strategy also accepts
# ``record_shape_names`` custom declaration names; only these can
# exercise the split-key-set rejection.
_CUSTOM_NAME_LANGUAGES: tuple[LanguageCls, ...] = (Kotlin, Scala)


def _record_strategy_for(language_cls: LanguageCls) -> object:
    """Return *language_cls*'s ``RECORD`` heterogeneous strategy."""
    return next(
        strategy
        for strategy in language_cls().heterogeneous_strategies
        if strategy.name == "RECORD"
    )


@pytest.mark.parametrize(
    argnames="language_cls",
    argvalues=_FIELD_TYPE_SPLIT_LANGUAGES,
    ids=[
        language_cls.__name__ for language_cls in _FIELD_TYPE_SPLIT_LANGUAGES
    ],
)
def test_sibling_records_with_conflicting_scalar_field_types_raise(
    language_cls: LanguageCls,
) -> None:
    """Sibling dicts with equal key sets but conflicting scalar types
    resolve to distinct record shapes, so the sibling list is rejected
    rather than emitting one declaration with a mismatched field type.
    """
    language: Language = language_cls(
        heterogeneous_strategy=_record_strategy_for(language_cls=language_cls),
    )
    with pytest.raises(expected_exception=HeterogeneousSiblingListsError):
        literalize(
            source=_SCALAR_TYPE_CONFLICT_YAML,
            input_format=InputFormat.YAML,
            language=language,
        )


@pytest.mark.parametrize(
    argnames="language_cls",
    argvalues=_CUSTOM_NAME_LANGUAGES,
    ids=[language_cls.__name__ for language_cls in _CUSTOM_NAME_LANGUAGES],
)
def test_custom_name_for_split_key_set_raises(
    language_cls: LanguageCls,
) -> None:
    """A ``record_shape_names`` entry cannot identify one declaration
    when its key set splits into conflicting field-type shapes, so the
    input is rejected rather than emitting duplicate declarations under
    the custom name.
    """
    language: Language = language_cls(
        heterogeneous_strategy=_record_strategy_for(language_cls=language_cls),
        record_shape_names={frozenset({"a"}): "Payload"},
    )
    with pytest.raises(expected_exception=UnrepresentableInputError):
        literalize(
            source=_CUSTOM_NAME_SPLIT_YAML,
            input_format=InputFormat.YAML,
            language=language,
        )
