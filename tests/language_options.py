"""The formatter options a language-selecting test may name.

Both the golden suite's variant axes and the error suite's rejection
manifests select languages and build specs by naming an option -- a
constructor parameter whose values are enum members -- rather than
importing the language class and spelling the member itself.  The
registry below is the one place a name becomes an accessor, so an
unknown option fails when the registry loads rather than when a case
runs.

Every option reads the value the constructor took, not the derived
formatter the language built from it: a JSON value type overrides
``format_bytes``, and Haskell, OCaml and SML build a closure from their
date and datetime members rather than returning the member, so a
derived accessor never compares equal to the default.
"""

import dataclasses
import enum
from collections.abc import Callable, Mapping
from typing import Protocol, runtime_checkable

from beartype import beartype

import literalizer
from tests.integration.language_metadata import language_metadata


@runtime_checkable
class _HasBoolFormat(Protocol):
    """A spec exposing a configurable boolean literal spelling."""

    bool_format: enum.Enum
    bool_formats: type[enum.Enum]


@runtime_checkable
class _HasEmptyDictKey(Protocol):
    """A spec exposing a configurable empty-dict key policy."""

    empty_dict_key: enum.Enum
    empty_dict_keys: type[enum.Enum]


@runtime_checkable
class _HasAnnotationEvaluation(Protocol):
    """A spec exposing configurable annotation evaluation."""

    annotation_evaluation: enum.Enum
    annotation_evaluations: type[enum.Enum]


@runtime_checkable
class _HasUnionFormat(Protocol):
    """A spec exposing configurable union annotation syntax."""

    union_format: enum.Enum
    union_formats: type[enum.Enum]


@runtime_checkable
class _HasJsonType(Protocol):
    """A spec exposing a JSON value-type representation.

    Languages without one omit the ``json_type`` constructor field
    entirely, so a ``spec_field_present`` gate selects the languages
    this reads from.
    """

    json_type: enum.Enum | None
    json_types: type[enum.Enum]


@runtime_checkable
class _HasJsonRendering(Protocol):
    """A spec exposing a rendering choice for its JSON value type.

    Only languages whose JSON library has both a structural literal
    form and a parser expose the ``json_rendering`` constructor field,
    so a ``spec_field_present`` gate selects the languages this reads
    from.
    """

    json_rendering: enum.Enum | None
    json_renderings: type[enum.Enum]


@runtime_checkable
class _HasRecordMapValueTyping(Protocol):
    """A spec exposing a widened record-map value-type choice.

    Only languages whose ``RECORD`` strategy spells that map's value
    type explicitly expose the ``record_map_value_typing`` constructor
    field, so a ``spec_field_present`` gate selects the languages this
    reads from.
    """

    record_map_value_typing: enum.Enum
    record_map_value_typings: type[enum.Enum]


@runtime_checkable
class _HasBytesFormat(Protocol):
    """A spec exposing the configured bytes format."""

    bytes_format: enum.Enum
    bytes_formats: type[enum.Enum]


@beartype
def _bool_format(spec: literalizer.Language) -> object:
    """Return the configured boolean literal spelling."""
    assert isinstance(spec, _HasBoolFormat)  # noqa: S101
    return spec.bool_format


@beartype
def _bool_formats(spec: literalizer.Language) -> type[enum.Enum]:
    """Return the boolean literal spellings a language offers."""
    assert isinstance(spec, _HasBoolFormat)  # noqa: S101
    return spec.bool_formats


@beartype
def _empty_dict_key(spec: literalizer.Language) -> object:
    """Return the configured empty-dict key policy."""
    assert isinstance(spec, _HasEmptyDictKey)  # noqa: S101
    return spec.empty_dict_key


@beartype
def _empty_dict_keys(spec: literalizer.Language) -> type[enum.Enum]:
    """Return the empty-dict key policies a language offers."""
    assert isinstance(spec, _HasEmptyDictKey)  # noqa: S101
    return spec.empty_dict_keys


@beartype
def _annotation_evaluation(spec: literalizer.Language) -> object:
    """Return the configured annotation-evaluation mode."""
    assert isinstance(spec, _HasAnnotationEvaluation)  # noqa: S101
    return spec.annotation_evaluation


@beartype
def _annotation_evaluations(spec: literalizer.Language) -> type[enum.Enum]:
    """Return the annotation-evaluation modes a language offers."""
    assert isinstance(spec, _HasAnnotationEvaluation)  # noqa: S101
    return spec.annotation_evaluations


@beartype
def _union_format(spec: literalizer.Language) -> object:
    """Return the configured union annotation syntax."""
    assert isinstance(spec, _HasUnionFormat)  # noqa: S101
    return spec.union_format


@beartype
def _union_formats(spec: literalizer.Language) -> type[enum.Enum]:
    """Return the union annotation forms a language offers."""
    assert isinstance(spec, _HasUnionFormat)  # noqa: S101
    return spec.union_formats


@beartype
def _json_type(spec: literalizer.Language) -> object:
    """Return the configured JSON value type, if any."""
    assert isinstance(spec, _HasJsonType)  # noqa: S101
    return spec.json_type


@beartype
def _json_types(spec: literalizer.Language) -> type[enum.Enum]:
    """Return the JSON value types a language offers."""
    assert isinstance(spec, _HasJsonType)  # noqa: S101
    return spec.json_types


@beartype
def _json_rendering(spec: literalizer.Language) -> object:
    """Return the configured JSON rendering, if any."""
    assert isinstance(spec, _HasJsonRendering)  # noqa: S101
    return spec.json_rendering


@beartype
def _json_renderings(spec: literalizer.Language) -> type[enum.Enum]:
    """Return the JSON renderings a language offers."""
    assert isinstance(spec, _HasJsonRendering)  # noqa: S101
    return spec.json_renderings


@beartype
def _record_map_value_typing(spec: literalizer.Language) -> object:
    """Return the configured widened record-map value typing."""
    assert isinstance(spec, _HasRecordMapValueTyping)  # noqa: S101
    return spec.record_map_value_typing


@beartype
def _record_map_value_typings(
    spec: literalizer.Language,
) -> type[enum.Enum]:
    """Return the widened record-map value types a language offers."""
    assert isinstance(spec, _HasRecordMapValueTyping)  # noqa: S101
    return spec.record_map_value_typings


@beartype
def _bytes_format(spec: literalizer.Language) -> object:
    """Return the configured bytes format, despite JSON overrides."""
    assert isinstance(spec, _HasBytesFormat)  # noqa: S101
    return spec.bytes_format


@beartype
def _bytes_formats(spec: literalizer.Language) -> type[enum.Enum]:
    """Return the bytes formats a language offers."""
    assert isinstance(spec, _HasBytesFormat)  # noqa: S101
    return spec.bytes_formats


_LINE_SEPARATOR = "\u2028"
_PARAGRAPH_SEPARATOR = "\u2029"


@beartype
def _escapes_unicode_line_separators(
    lang_cls: literalizer.LanguageCls,
) -> bool:
    """Return whether string literals escape U+2028 and U+2029.

    A language that emits either separator raw renders the bytes the
    input held, so a case covering the escape has nothing to observe
    there.  The answer comes from the default string formatter rather
    than a declared flag, so a language that gains or loses the escape
    joins or leaves that case on its own.
    """
    formatted = lang_cls().format_string(
        f"a{_LINE_SEPARATOR}b{_PARAGRAPH_SEPARATOR}c"
    )
    return (
        _LINE_SEPARATOR not in formatted
        and _PARAGRAPH_SEPARATOR not in formatted
    )


@dataclasses.dataclass(frozen=True, kw_only=True)
class Option:
    """One configurable formatter option a plan can select values from.

    ``kwarg`` is the language-class constructor parameter name; each
    accessor reads the configured value or the member enum from a built
    spec.
    """

    kwarg: str
    get_default: Callable[[literalizer.Language], object]
    get_members: Callable[[literalizer.Language], type[enum.Enum]]


OPTIONS: Mapping[str, Option] = {
    "annotation_evaluation": Option(
        kwarg="annotation_evaluation",
        get_default=_annotation_evaluation,
        get_members=_annotation_evaluations,
    ),
    "bool_format": Option(
        kwarg="bool_format",
        get_default=_bool_format,
        get_members=_bool_formats,
    ),
    # Each option reads the value the constructor took, not the derived
    # formatter the language built from it: a JSON value type overrides
    # ``format_bytes``, and Haskell, OCaml and SML build a closure from
    # their date and datetime members rather than returning the member,
    # so a derived accessor never compares equal to the default and
    # expands the language default under a non-default name.
    "bytes_format": Option(
        kwarg="bytes_format",
        get_default=_bytes_format,
        get_members=_bytes_formats,
    ),
    "comment_format": Option(
        kwarg="comment_format",
        get_default=lambda spec: spec.comment_format,
        get_members=lambda spec: spec.comment_formats,
    ),
    "date_format": Option(
        kwarg="date_format",
        get_default=lambda spec: spec.date_format,
        get_members=lambda spec: spec.date_formats,
    ),
    "datetime_format": Option(
        kwarg="datetime_format",
        get_default=lambda spec: spec.datetime_format,
        get_members=lambda spec: spec.datetime_formats,
    ),
    "declaration_style": Option(
        kwarg="declaration_style",
        get_default=lambda spec: spec.declaration_style,
        get_members=lambda spec: spec.declaration_styles,
    ),
    "dict_entry_style": Option(
        kwarg="dict_entry_style",
        get_default=lambda spec: spec.dict_entry_style,
        get_members=lambda spec: spec.dict_entry_styles,
    ),
    "dict_format": Option(
        kwarg="dict_format",
        get_default=lambda spec: spec.dict_format,
        get_members=lambda spec: spec.dict_formats,
    ),
    "empty_dict_key": Option(
        kwarg="empty_dict_key",
        get_default=_empty_dict_key,
        get_members=_empty_dict_keys,
    ),
    "float_format": Option(
        kwarg="float_format",
        get_default=lambda spec: spec.float_format,
        get_members=lambda spec: spec.float_formats,
    ),
    "heterogeneous_strategy": Option(
        kwarg="heterogeneous_strategy",
        get_default=lambda spec: spec.heterogeneous_strategy,
        get_members=lambda spec: spec.heterogeneous_strategies,
    ),
    "integer_format": Option(
        kwarg="integer_format",
        get_default=lambda spec: spec.integer_format,
        get_members=lambda spec: spec.integer_formats,
    ),
    "integer_width_strategy": Option(
        kwarg="integer_width_strategy",
        get_default=lambda spec: spec.integer_width_strategy,
        get_members=lambda spec: spec.integer_width_strategies,
    ),
    "json_rendering": Option(
        kwarg="json_rendering",
        get_default=_json_rendering,
        get_members=_json_renderings,
    ),
    "json_type": Option(
        kwarg="json_type",
        get_default=_json_type,
        get_members=_json_types,
    ),
    "language_version": Option(
        kwarg="language_version",
        get_default=lambda spec: spec.language_version,
        get_members=lambda spec: spec.version_formats,
    ),
    "numeric_literal_suffix": Option(
        kwarg="numeric_literal_suffix",
        get_default=lambda spec: spec.numeric_literal_suffix,
        get_members=lambda spec: spec.numeric_literal_suffixes,
    ),
    "numeric_separator": Option(
        kwarg="numeric_separator",
        get_default=lambda spec: spec.numeric_separator,
        get_members=lambda spec: spec.numeric_separators,
    ),
    "numeric_style": Option(
        kwarg="numeric_style",
        get_default=lambda spec: spec.numeric_style,
        get_members=lambda spec: spec.numeric_styles,
    ),
    "record_map_value_typing": Option(
        kwarg="record_map_value_typing",
        get_default=_record_map_value_typing,
        get_members=_record_map_value_typings,
    ),
    "sequence_format": Option(
        kwarg="sequence_format",
        get_default=lambda spec: spec.sequence_format,
        get_members=lambda spec: spec.sequence_formats,
    ),
    "set_format": Option(
        kwarg="set_format",
        get_default=lambda spec: spec.set_format,
        get_members=lambda spec: spec.set_formats,
    ),
    "statement_terminator_style": Option(
        kwarg="statement_terminator_style",
        get_default=lambda spec: spec.statement_terminator_style,
        get_members=lambda spec: spec.statement_terminator_styles,
    ),
    "string_format": Option(
        kwarg="string_format",
        get_default=lambda spec: spec.string_format,
        get_members=lambda spec: spec.string_formats,
    ),
    "trailing_comma": Option(
        kwarg="trailing_comma",
        get_default=lambda spec: spec.trailing_comma,
        get_members=lambda spec: spec.trailing_commas,
    ),
    "union_format": Option(
        kwarg="union_format",
        get_default=_union_format,
        get_members=_union_formats,
    ),
    "variable_type_hints": Option(
        kwarg="variable_type_hints",
        get_default=lambda spec: spec.variable_type_hints,
        get_members=lambda spec: spec.variable_type_hints_formats,
    ),
}

CAPABILITY_FLAGS: Mapping[str, Callable[[literalizer.LanguageCls], bool]] = {
    "declares_call_styles": lambda lang_cls: len(lang_cls.CallStyles) > 0,
    "supports_json_call_result_binding": (
        lambda lang_cls: lang_cls.supports_json_call_result_binding
    ),
    "rejects_heterogeneous_dict_values": (
        lambda lang_cls: not lang_cls.dict_supports_heterogeneous_values
    ),
    "rejects_non_string_dict_keys": (
        lambda lang_cls: not lang_cls.supports_non_string_dict_keys
    ),
    "supports_special_float_dict_keys": (
        lambda lang_cls: (
            lang_cls.supports_non_string_dict_keys
            and lang_cls.supports_special_floats
            and language_metadata(
                language_id=lang_cls.language_id
            ).variants.supports_special_float_dict_keys
        )
    ),
    "supports_module_name": lambda lang_cls: lang_cls.supports_module_name,
    "supports_variable_names": (
        lambda lang_cls: lang_cls.supports_variable_names
    ),
    "supports_widened_integer_formatter": (
        lambda lang_cls: lang_cls().format_integer_widened is not None
    ),
    "supports_multiline_string_literals": (
        lambda lang_cls: lang_cls.supports_multiline_string_literals
    ),
    "supports_record_shape_names": (
        lambda lang_cls: lang_cls.supports_record_shape_names
    ),
    "supports_record_struct_name_prefix": (
        lambda lang_cls: lang_cls.supports_record_struct_name_prefix
    ),
    "supports_ref_elements_in_tuple_strategy": (
        lambda lang_cls: (
            lang_cls.variant_metadata.supports_ref_elements_in_tuple_strategy
        )
    ),
    "supports_standalone_comments_in_wrapped_calls": (
        lambda lang_cls: lang_cls.supports_standalone_comments_in_wrapped_calls
    ),
    "string_literals_escape_null_byte": (
        lambda lang_cls: (
            lang_cls.variant_metadata.string_literals_escape_null_byte
        )
    ),
    "string_literals_escape_unicode_line_separators": (
        _escapes_unicode_line_separators
    ),
    # Only the languages that name dotted-call helpers after path
    # segments declare this flag, and the production check reads it
    # through a protocol that tolerates its absence, so a missing
    # value means False here too.
    "dotted_call_stub_requires_unique_parts": (
        lambda lang_cls: bool(
            vars(lang_cls).get("dotted_call_stub_requires_unique_parts", False)
        )
    ),
}
