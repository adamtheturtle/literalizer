"""Language-wide metadata and protocol checks."""

import enum
from collections.abc import Mapping
from typing import Protocol, runtime_checkable

import pytest
from pygments.lexers import find_lexer_class_by_name

import literalizer.languages
from literalizer import LanguageCls
from literalizer.exceptions import WrapCombinedInFileNotSupportedError
from literalizer.languages import Python, Raku

_SORTED_LANGUAGES: list[LanguageCls] = sorted(
    literalizer.languages.ALL_LANGUAGES,
    key=lambda c: c.__name__,
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
    argvalues=_SORTED_LANGUAGES,
    ids=[c.__name__ for c in _SORTED_LANGUAGES],
)
def test_language_version_is_non_empty_string(
    *,
    language_cls: LanguageCls,
) -> None:
    """Every language's default ``language_version`` is an enum member."""
    spec = language_cls()
    assert isinstance(spec.language_version, enum.Enum)


@pytest.mark.parametrize(
    argnames="language_cls",
    argvalues=_SORTED_LANGUAGES,
    ids=[c.__name__ for c in _SORTED_LANGUAGES],
)
def test_pygments_name_is_valid(
    *,
    language_cls: LanguageCls,
) -> None:
    """Every language's ``pygments_name`` is recognized by Pygments."""
    if language_cls.pygments_name is None:
        return
    find_lexer_class_by_name(_alias=language_cls.pygments_name)


@pytest.mark.parametrize(
    argnames="language_cls",
    argvalues=_SORTED_LANGUAGES,
    ids=[c.__name__ for c in _SORTED_LANGUAGES],
)
def test_protocol_properties_accessible(
    *,
    language_cls: LanguageCls,
) -> None:
    """Every Language exposes its Protocol attributes for any language."""
    spec = language_cls()
    assert callable(spec.validate_call_arg)
    assert callable(spec.format_call_statement)
    assert callable(spec.call_data_dependent_preamble)
    assert callable(spec.format_call_stub)
    assert callable(spec.format_call_preamble_stub)
    assert callable(spec.format_call_target)
    assert callable(spec.format_call_ref_identifier)
    assert callable(spec.format_call_arg_ref_identifier)
    assert callable(spec.format_call_arg_ref_identifier_consumable)
    assert callable(spec.consumable_ref_value_inhibits_consuming_form)
    assert callable(spec.format_variable_declaration)
    assert callable(spec.format_variable_assignment)
    assert callable(spec.type_hint_collection_preamble_lines)
    assert isinstance(spec.scalar_body_preamble, dict)
    assert isinstance(spec.supports_standalone_comments_in_wrapped_calls, bool)
    assert isinstance(spec.supports_multi_param_call_wrapper_stub, bool)
    assert isinstance(spec.supports_dict_literal_as_free_expression, bool)


@pytest.mark.parametrize(
    argnames="language_cls",
    argvalues=_SORTED_LANGUAGES,
    ids=[c.__name__ for c in _SORTED_LANGUAGES],
)
def test_format_enumeration_properties(
    language_cls: LanguageCls,
) -> None:
    """Every language exposes iterable format-enumeration properties."""
    spec = language_cls()
    assert issubclass(spec.bytes_formats, enum.Enum)
    assert len(spec.bytes_formats) >= 1
    assert issubclass(spec.sequence_formats, enum.Enum)
    assert len(spec.sequence_formats) >= 1
    assert issubclass(spec.set_formats, enum.Enum)
    assert len(spec.set_formats) >= 1
    assert issubclass(spec.date_formats, enum.Enum)
    assert len(spec.date_formats) >= 1
    assert issubclass(spec.datetime_formats, enum.Enum)
    assert len(spec.datetime_formats) >= 1
    assert issubclass(spec.comment_formats, enum.Enum)
    assert len(spec.comment_formats) >= 1
    assert issubclass(spec.declaration_styles, enum.Enum)
    assert len(spec.declaration_styles) >= 1
    assert issubclass(spec.dict_formats, enum.Enum)
    assert len(spec.dict_formats) >= 1
    assert issubclass(spec.float_formats, enum.Enum)
    assert len(spec.float_formats) >= 1
    assert issubclass(spec.integer_formats, enum.Enum)
    assert len(spec.integer_formats) >= 1
    assert issubclass(spec.numeric_separators, enum.Enum)
    assert len(spec.numeric_separators) >= 1
    assert issubclass(spec.numeric_styles, enum.Enum)
    assert len(spec.numeric_styles) >= 1
    assert issubclass(spec.string_formats, enum.Enum)
    assert len(spec.string_formats) >= 1
    assert issubclass(spec.trailing_commas, enum.Enum)
    assert len(spec.trailing_commas) >= 1
    assert issubclass(spec.statement_terminator_styles, enum.Enum)
    assert len(spec.statement_terminator_styles) >= 1
    assert issubclass(spec.call_styles, enum.Enum)
    assert issubclass(spec.version_formats, enum.Enum)
    assert len(spec.version_formats) >= 1


@pytest.mark.parametrize(
    argnames="language_cls",
    argvalues=_UNSUPPORTED_COMBINED_LANGUAGES,
    ids=[c.__name__ for c in _UNSUPPORTED_COMBINED_LANGUAGES],
)
def test_wrap_combined_in_file_unsupported_raises(
    *,
    language_cls: LanguageCls,
) -> None:
    """Check wrap_combined_in_file raises when redefinition is unsupported."""
    with pytest.raises(expected_exception=WrapCombinedInFileNotSupportedError):
        language_cls().wrap_combined_in_file(
            declaration="x = 1",
            assignment="x = 2",
            variable_name="x",
            body_preamble=(),
        )


@runtime_checkable
class _HasRecordStructNamePrefix(Protocol):
    """Structural type for languages that expose a
    ``record_struct_name_prefix`` constructor field.

    Used to narrow a generic :class:`literalizer.Language` to one with
    the field without introspecting ``__dataclass_fields__`` or casting
    to ``Any``.
    """

    record_struct_name_prefix: str


@pytest.mark.parametrize(
    argnames="language_cls",
    argvalues=_SORTED_LANGUAGES,
    ids=[c.__name__ for c in _SORTED_LANGUAGES],
)
def test_supports_record_struct_name_prefix_matches_constructor(
    *,
    language_cls: LanguageCls,
) -> None:
    """The flag is ``True`` exactly when the constructor accepts
    ``record_struct_name_prefix``.

    Runtime-dispatched callers rely on this flag instead of inspecting
    dataclass fields, so it must stay in lock-step with the actual
    constructor keyword arguments.
    """
    spec = language_cls()
    accepts_kwarg = isinstance(spec, _HasRecordStructNamePrefix)
    assert language_cls.supports_record_struct_name_prefix == accepts_kwarg


@runtime_checkable
class _HasRecordShapeNames(Protocol):
    """Structural type for languages that expose a
    ``record_shape_names`` constructor field.

    Used to narrow a generic :class:`literalizer.Language` to one with
    the field without introspecting ``__dataclass_fields__`` or casting
    to ``Any``.
    """

    record_shape_names: Mapping[frozenset[str], str]


@pytest.mark.parametrize(
    argnames="language_cls",
    argvalues=_SORTED_LANGUAGES,
    ids=[c.__name__ for c in _SORTED_LANGUAGES],
)
def test_supports_record_shape_names_matches_constructor(
    *,
    language_cls: LanguageCls,
) -> None:
    """The flag is ``True`` exactly when the constructor accepts
    ``record_shape_names``.

    Runtime-dispatched callers rely on this flag instead of inspecting
    dataclass fields, so it must stay in lock-step with the actual
    constructor keyword arguments.
    """
    spec = language_cls()
    accepts_kwarg = isinstance(spec, _HasRecordShapeNames)
    assert language_cls.supports_record_shape_names == accepts_kwarg


def test_supported_ref_cases_independent_of_identifier_cases() -> None:
    """``supported_ref_cases`` is not derived from ``identifier_cases``.

    The two attributes answer different questions -- syntactic validity
    vs. stylistic preference -- and one is not a function of the other.
    """
    python = Python()
    assert frozenset(python.identifier_cases) != python.supported_ref_cases
    assert frozenset(python.identifier_cases) <= python.supported_ref_cases

    raku = Raku()
    assert frozenset(raku.identifier_cases) != raku.supported_ref_cases
    assert frozenset(raku.identifier_cases) <= raku.supported_ref_cases


@pytest.mark.parametrize(
    argnames="language_cls",
    argvalues=_SORTED_LANGUAGES,
    ids=[c.__name__ for c in _SORTED_LANGUAGES],
)
def test_identifier_cases_are_supported_ref_cases(
    *,
    language_cls: LanguageCls,
) -> None:
    """Every preferred identifier case must be valid for refs."""
    preferred_cases = frozenset(language_cls.identifier_cases)
    assert preferred_cases <= language_cls.supported_ref_cases
