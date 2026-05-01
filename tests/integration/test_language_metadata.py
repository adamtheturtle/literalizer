"""Language-wide metadata and protocol checks."""

import dataclasses
import enum
from collections.abc import Callable
from typing import Any, cast

import pytest
from pygments.lexers import find_lexer_class_by_name

import literalizer.languages
from literalizer._language import LanguageCls
from literalizer.exceptions import (
    UnsupportedDefaultDictKeyTypeError,
    UnsupportedDefaultDictValueTypeError,
    UnsupportedDefaultOrderedMapValueTypeError,
    UnsupportedDefaultSequenceElementTypeError,
    UnsupportedDefaultSetElementTypeError,
    UnsupportedLanguageOptionError,
    WrapCombinedInFileNotSupportedError,
)

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


@dataclasses.dataclass(frozen=True)
class _DefaultTypeOptionCase:
    """Constructor option metadata for default collection element
    types.
    """

    option_name: str
    is_supported: Callable[[LanguageCls], bool]
    exception_type: type[UnsupportedLanguageOptionError]


_DEFAULT_TYPE_OPTION_CASES: tuple[_DefaultTypeOptionCase, ...] = (
    _DefaultTypeOptionCase(
        option_name="default_set_element_type",
        is_supported=lambda language_cls: (
            language_cls.supports_default_set_element_type
        ),
        exception_type=UnsupportedDefaultSetElementTypeError,
    ),
    _DefaultTypeOptionCase(
        option_name="default_sequence_element_type",
        is_supported=lambda language_cls: (
            language_cls.supports_default_sequence_element_type
        ),
        exception_type=UnsupportedDefaultSequenceElementTypeError,
    ),
    _DefaultTypeOptionCase(
        option_name="default_dict_value_type",
        is_supported=lambda language_cls: (
            language_cls.supports_default_dict_value_type
        ),
        exception_type=UnsupportedDefaultDictValueTypeError,
    ),
    _DefaultTypeOptionCase(
        option_name="default_dict_key_type",
        is_supported=lambda language_cls: (
            language_cls.supports_default_dict_key_type
        ),
        exception_type=UnsupportedDefaultDictKeyTypeError,
    ),
    _DefaultTypeOptionCase(
        option_name="default_ordered_map_value_type",
        is_supported=lambda language_cls: (
            language_cls.supports_default_ordered_map_value_type
        ),
        exception_type=UnsupportedDefaultOrderedMapValueTypeError,
    ),
)

_UNSUPPORTED_LANGUAGE_OPTIONS: list[
    tuple[LanguageCls, _DefaultTypeOptionCase]
] = [
    (language_cls, option_case)
    for language_cls in _SORTED_LANGUAGES
    for option_case in _DEFAULT_TYPE_OPTION_CASES
    if not option_case.is_supported(language_cls)
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
    assert callable(spec.format_variable_declaration)
    assert callable(spec.format_variable_assignment)
    assert callable(spec.type_hint_collection_preamble_lines)
    assert isinstance(spec.scalar_body_preamble, dict)
    assert isinstance(spec.supports_standalone_comments_in_wrapped_calls, bool)
    assert isinstance(spec.supports_commented_dict_call_args, bool)


@pytest.mark.parametrize(
    argnames=("language_cls", "option_case"),
    argvalues=[
        (language_cls, option_case)
        for language_cls in _SORTED_LANGUAGES
        for option_case in _DEFAULT_TYPE_OPTION_CASES
    ],
    ids=[
        f"{language_cls.__name__}-{option_case.option_name}"
        for language_cls in _SORTED_LANGUAGES
        for option_case in _DEFAULT_TYPE_OPTION_CASES
    ],
)
def test_default_type_support_metadata_matches_constructor_fields(
    *,
    language_cls: LanguageCls,
    option_case: _DefaultTypeOptionCase,
) -> None:
    """Default-type support flags match dataclass constructor fields."""
    field_names = {
        field.name
        for field in dataclasses.fields(
            class_or_instance=cast("Any", language_cls),
        )
    }
    assert option_case.is_supported(language_cls) is (
        option_case.option_name in field_names
    )


@pytest.mark.parametrize(
    argnames=("language_cls", "option_case"),
    argvalues=_UNSUPPORTED_LANGUAGE_OPTIONS,
    ids=[
        f"{language_cls.__name__}-{option_case.option_name}"
        for language_cls, option_case in _UNSUPPORTED_LANGUAGE_OPTIONS
    ],
)
def test_unsupported_language_option_raises(
    *,
    language_cls: LanguageCls,
    option_case: _DefaultTypeOptionCase,
) -> None:
    """Unsupported default-type constructor options raise typed errors."""
    with pytest.raises(
        expected_exception=option_case.exception_type,
        match=(
            rf"^{language_cls.__name__} does not support option "
            rf"{option_case.option_name!r}$"
        ),
    ):
        language_cls(**{option_case.option_name: "String"})


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
