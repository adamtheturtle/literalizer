"""Language-wide metadata and protocol checks."""

import dataclasses
import inspect
from collections.abc import Mapping
from types import new_class
from typing import Protocol, runtime_checkable

import pytest
from pygments.lexers import find_lexer_class_by_name
from typing_extensions import get_protocol_members

import literalizer.languages
from literalizer import Language, LanguageCls
from literalizer._language import (
    language_string_option,
    require_record_shape_names,
)
from literalizer.exceptions import UnsupportedOptionError
from literalizer.languages import Python


def _language_class_name(language_cls: LanguageCls, /) -> str:
    """Return the language class name."""
    return language_cls.__name__


_SORTED_LANGUAGES: list[LanguageCls] = sorted(
    literalizer.languages.ALL_LANGUAGES,
    key=_language_class_name,
)


def test_all_languages_support_non_ascii_string_literals() -> None:
    """Every backend now represents non-ASCII text in string literals."""
    assert all(
        cls.supports_non_ascii_string_literals for cls in _SORTED_LANGUAGES
    )


_LANGUAGE_OWNED_METADATA = frozenset(
    {
        "supports_variable_names",
        "language_id",
        "dotted_call_stub_indexes_colliding_helpers",
        "json_type_variant_name_suffix",
        "declares_type_name_call_target",
        "record_shape_names_emit_declarations",
        "supports_zero_parameter_calls",
        "supports_empty_sibling_sequence_type_hints",
        "supports_multiline_string_literals",
        "supports_non_ascii_string_literals",
        "supports_nullable_object_fallbacks",
        "supports_typed_dict_open",
        "supports_variadic_calls",
        "supports_stateful_receiver_result_checks",
        "supports_stateful_free_call_consumers",
        "supports_local_binding_documents",
        "reserved_variable_identifiers",
        "supports_key_value_assignment_documents",
        "reserved_variable_identifiers_case_sensitive",
        "supports_json_object_documents",
        "supports_bare_mapping_documents",
        "variant_metadata",
        "wraps_data_dependent_preamble_in_body",
        "uses_data_keyword_for_algebraic_constructors",
    }
)


@pytest.mark.parametrize(
    argnames="language_cls",
    argvalues=_SORTED_LANGUAGES,
    ids=_language_class_name,
)
def test_language_metadata_is_declared_by_each_language(
    *,
    language_cls: LanguageCls,
) -> None:
    """Every language owns its metadata instead of inheriting defaults."""
    missing = _LANGUAGE_OWNED_METADATA - vars(language_cls).keys()
    assert len(missing) == 0


def test_language_metadata_has_no_metaclass_defaults() -> None:
    """The meta-class contract must not conceal missing declarations."""
    inherited_defaults = _LANGUAGE_OWNED_METADATA & vars(LanguageCls).keys()
    assert len(inherited_defaults) == 0


def test_language_ids_are_unique_lower_snake_identifiers() -> None:
    """Every language owns a distinct, stable, neutral identifier."""
    language_ids = [cls.language_id for cls in _SORTED_LANGUAGES]
    assert len(set(language_ids)) == len(language_ids)
    malformed = [
        language_id
        for language_id in language_ids
        if not (language_id.isidentifier() and language_id.islower())
    ]
    assert malformed == []


def test_variant_metadata_fields_have_no_defaults() -> None:
    """Every metadata choice must be supplied by the language class."""
    signature = inspect.signature(obj=type(Python.variant_metadata))
    assert len(signature.parameters) > 0
    defaulted = signature.bind_partial()
    defaulted.apply_defaults()
    assert len(defaulted.arguments) == 0


@pytest.mark.parametrize(
    argnames="language_cls",
    argvalues=_SORTED_LANGUAGES,
    ids=_language_class_name,
)
def test_pygments_name_is_valid(
    *,
    language_cls: LanguageCls,
) -> None:
    """Every language's ``pygments_name`` is recognized by Pygments."""
    if language_cls.pygments_name is None:
        return
    _ = find_lexer_class_by_name(_alias=language_cls.pygments_name)


def test_language_protocol_members_are_not_class_level_none() -> None:
    """Built-in languages never store Protocol members as literal ``None``.

    The runtime Protocol checker treats class-level ``None`` as the
    PEP 544 "attribute is not implemented" marker.  That prevents ABC cache
    warming and makes repeated ``isinstance(_, Language)`` checks traverse the
    whole protocol.  Reported upstream as
    https://github.com/python/cpython/issues/156413.
    """
    missing = object()
    protocol_members = get_protocol_members(Language)
    violations: dict[str, tuple[str, ...]] = {}

    for language_cls in _SORTED_LANGUAGES:
        class_level_none = [
            member
            for member in protocol_members
            if vars(language_cls).get(member, missing) is None
        ]
        violations[language_cls.__name__] = tuple(sorted(class_level_none))

    assert not any(violations.values()), violations


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
    ids=_language_class_name,
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
    ids=_language_class_name,
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


@pytest.mark.parametrize(
    argnames="language_cls",
    argvalues=_SORTED_LANGUAGES,
    ids=_language_class_name,
)
def test_identifier_cases_are_supported_ref_cases(
    *,
    language_cls: LanguageCls,
) -> None:
    """Every preferred identifier case must be valid for refs."""
    preferred_cases = frozenset(language_cls.identifier_cases)
    assert preferred_cases <= language_cls.supported_ref_cases


def test_string_option_rejects_non_string_fields() -> None:
    """A language option declared as a string must hold a string."""
    with pytest.raises(expected_exception=TypeError, match="must be a string"):
        _ = language_string_option(
            language=Python(), name="heterogeneous_strategy"
        )


def test_record_shape_names_reject_invalid_keys() -> None:
    """A record name table must use sets of field names as keys."""
    with pytest.raises(expected_exception=TypeError, match="field-name sets"):
        _ = require_record_shape_names(value={"field": "RecordName"})


@pytest.mark.parametrize(argnames="language_cls", argvalues=[Python])
def test_custom_language_options_are_registered_at_class_creation(
    language_cls: LanguageCls,
) -> None:
    """A custom option is recognized before the defining language is
    used.
    """

    @dataclasses.dataclass(frozen=True, kw_only=True)
    class CustomPython(Python):
        """A custom language with a caller-defined option."""

        custom_dialect: str

    with pytest.raises(
        expected_exception=UnsupportedOptionError, match="custom_dialect"
    ):
        _ = language_cls(custom_dialect="example")
    custom = CustomPython(custom_dialect="example")
    assert isinstance(custom, CustomPython)
    assert custom.custom_dialect == "example"


def test_language_class_registry_requires_a_language_class() -> None:
    """The registry rejects constructors that return ordinary
    instances.
    """
    ordinary_class: type[object] = new_class(
        name="OrdinaryClass", kwds={"metaclass": type(LanguageCls)}
    )
    with pytest.raises(
        expected_exception=TypeError, match="must create a language class"
    ):
        _ = ordinary_class()
