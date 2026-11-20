"""Typed definitions for the golden suite's variant axes."""

import enum
import functools
from collections.abc import Mapping
from typing import Protocol, runtime_checkable

import literalizer
from literalizer._enums import enum_payload
from tests.enum_members import enum_member_by_name
from tests.language_options import CAPABILITY_FLAGS, OPTIONS

from .axis_builders import (
    BOTH_LAYOUTS,
    COMPACT,
    MULTILINE,
    Axis,
    AxisTarget,
    Choice,
    Name,
    Options,
    cross,
    declaration_sequence,
    expand,
    filtered,
    fixed_options,
    has_member,
    has_option,
    has_sample,
    member,
    member_with_behavior,
    members,
    metadata_member,
    named,
    named_choice,
    pin,
    sample,
    sample_value,
    single_choice,
    values,
)
from .language_metadata import LanguageMetadata
from .language_specs import make_spec

_ANNOTATION_EVALUATION = OPTIONS["annotation_evaluation"]
_ARRAY_INFERENCE_POLICY = OPTIONS["array_inference_policy"]
_BOOL_FORMAT = OPTIONS["bool_format"]
_BYTES_FORMAT = OPTIONS["bytes_format"]
_COMMENT_FORMAT = OPTIONS["comment_format"]
_DATETIME_FORMAT = OPTIONS["datetime_format"]
_DATE_FORMAT = OPTIONS["date_format"]
_DECLARATION_STYLE = OPTIONS["declaration_style"]
_DICT_ENTRY_STYLE = OPTIONS["dict_entry_style"]
_DICT_FORMAT = OPTIONS["dict_format"]
_EMPTY_DICT_KEY = OPTIONS["empty_dict_key"]
_FLOAT_FORMAT = OPTIONS["float_format"]
_HETEROGENEOUS_STRATEGY = OPTIONS["heterogeneous_strategy"]
_INTEGER_FORMAT = OPTIONS["integer_format"]
_INTEGER_WIDTH_STRATEGY = OPTIONS["integer_width_strategy"]
_JSON_RENDERING = OPTIONS["json_rendering"]
_JSON_TYPE = OPTIONS["json_type"]
_LANGUAGE_VERSION = OPTIONS["language_version"]
_LIST_RENDERING_POLICY = OPTIONS["list_rendering_policy"]
_NUMERIC_LITERAL_SUFFIX = OPTIONS["numeric_literal_suffix"]
_NUMERIC_SEPARATOR = OPTIONS["numeric_separator"]
_NUMERIC_STYLE = OPTIONS["numeric_style"]
_RECORD_MAP_VALUE_TYPING = OPTIONS["record_map_value_typing"]
_SEQUENCE_FORMAT = OPTIONS["sequence_format"]
_SET_FORMAT = OPTIONS["set_format"]
_STATEMENT_TERMINATOR_STYLE = OPTIONS["statement_terminator_style"]
_STRING_FORMAT = OPTIONS["string_format"]
_TRAILING_COMMA = OPTIONS["trailing_comma"]
_UNION_FORMAT = OPTIONS["union_format"]
_VARIABLE_TYPE_HINTS = OPTIONS["variable_type_hints"]


_default_allows_empty_ordered_map_keys = CAPABILITY_FLAGS[
    "default_allows_empty_ordered_map_keys"
]
_supports_special_float_dict_keys = CAPABILITY_FLAGS[
    "supports_special_float_dict_keys"
]
_supports_widened_integer_formatter = CAPABILITY_FLAGS[
    "supports_widened_integer_formatter"
]

_NAMED_RECORD = "NamedType"
_EXTERNAL_RECORD = "ExternalRecordShape"
_MOVE_ONLY_RECORD = "UserRecord"


@runtime_checkable
class _EscapesNullByte(Protocol):
    """An enum member describing how it renders an embedded null byte."""

    string_literals_escape_null_byte: bool


def _comment_suffix(selected: enum.Enum) -> bool:
    """Return whether a comment format closes with a terminator."""
    return bool(
        enum_payload(
            member=selected, payload_type=literalizer.CommentConfig
        ).suffix
    )


def _escapes_null_byte(selected: enum.Enum) -> bool:
    """Return whether this member's formatter escapes an embedded null."""
    if not isinstance(selected, _EscapesNullByte):
        raise NotImplementedError
    return selected.string_literals_escape_null_byte


def _json_type_label(target: AxisTarget, selected: enum.Enum) -> str:
    """Prefer the language's name for its JSON representation."""
    declared = target.lang_cls.json_type_variant_name_suffix
    return selected.name.lower() if declared is None else declared


def _empty_container_hints(target: AxisTarget) -> Options | None:
    """Select languages with explicit empty-container hints and apply them."""
    settings = target.metadata.variants.empty_container_type_hint
    if settings is None:
        return None
    return {
        "empty_container_type_hints": {
            tuple(entry.path): entry.hint for entry in settings.type_hints
        }
    }


def _empty_container_strategy(metadata: LanguageMetadata) -> str | None:
    """Return the heterogeneous strategy paired with the declared
    hints.
    """
    settings = metadata.variants.empty_container_type_hint
    return None if settings is None else settings.heterogeneous_strategy


def _external_cpp_type_preamble(
    target: AxisTarget,
    *,
    name: str,
    source: str,
    strategy: str,
) -> tuple[str, ...]:
    """Generate a separate declaration for an externally named C++
    type.
    """
    if target.lang_cls.record_shape_names_emit_declarations:
        return ()
    if target.default_spec.language_id != "cpp":
        raise NotImplementedError
    cpp = make_spec(
        lang_cls=target.lang_cls,
        heterogeneous_strategy=enum_member_by_name(
            enum_cls=target.default_spec.heterogeneous_strategies,
            name=strategy,
        ),
        language_version=enum_member_by_name(
            enum_cls=target.lang_cls.VersionFormats, name="CPP14"
        ),
        record_struct_name_prefix="FixtureRecord",
    )
    example = literalizer.literalize(
        language=cpp,
        source=source,
        input_format=literalizer.InputFormat.JSON,
    )
    return (
        *example.preamble,
        *example.body_preamble,
        f"using {name} = decltype({example.declaration_code});",
    )


def _named_sample(*, suffix: str, option: str) -> Name:
    """Include the declared sample value in the variant name."""
    return lambda target, _label: (
        f"{target.name}_{suffix}_{sample_value(target=target, kwarg=option)}"
    )


def _multiline_delimiter_choices(target: AxisTarget) -> tuple[Choice, ...]:
    """Exercise native custom, punctuation and exhausted delimiters."""
    kwarg = "multiline_raw_string_delimiter_base"
    return (
        Choice(
            label="custom",
            kwargs={kwarg: sample_value(target=target, kwarg=kwarg)},
        ),
        Choice(label="punctuation", kwargs={kwarg: "_{}[]#<>%:;.?*"}),
        Choice(label="exhausted", kwargs={kwarg: "abcdefghijklmnop"}),
    )


def _registry(**axes: Axis) -> Mapping[str, Axis]:
    """Index builders by their unique Python keyword names."""
    return axes


_record_version = metadata_member(
    option=_LANGUAGE_VERSION,
    read=lambda metadata: metadata.variants.record_language_version,
    optional=True,
)


_array_inference_policy_choices = members(
    option=_ARRAY_INFERENCE_POLICY, include_default=True
)
_json_type_choices = members(
    option=_JSON_TYPE, unset="narrow", label=_json_type_label
)
_list_rendering_policy_choices = members(
    option=_LIST_RENDERING_POLICY, include_default=True
)
_sequence_choices = members(option=_SEQUENCE_FORMAT)


_ANONYMOUS_RECORD_OPTIONS = (
    member(option=_DICT_FORMAT, name="ANONYMOUS_RECORD"),
)
_CSHARP_OBJECT_CARRIER_OPTIONS = (
    member(option=_SEQUENCE_FORMAT, name="ARRAY"),
)
_ERROR_RECORD_SHAPE_NAMES_OPTIONS = (
    member(option=_HETEROGENEOUS_STRATEGY, name="ERROR"),
    fixed_options(
        record_shape_names={frozenset(("first", "last")): _EXTERNAL_RECORD}
    ),
)
_NESTED_MAP_WIDENING_SCALAR_WRAPPING_OPTIONS = (
    member_with_behavior(
        option=_HETEROGENEOUS_STRATEGY,
        admits=lambda spec: (
            spec.heterogeneous_behavior.widens_nested_maps_by_wrapping_scalars
        ),
    ),
)
_RECORD_EAGER_FIELD_ANNOTATIONS_OPTIONS = (
    member(option=_ANNOTATION_EVALUATION, name="EAGER"),
    member(option=_HETEROGENEOUS_STRATEGY, name="RECORD"),
)


# Unlike the ordinary ``comment`` axis, this keeps a language's default
# format: the terminator is the subject, so a default comment that
# closes with one belongs here.  A line-comment member has an empty
# suffix and drops out.
_comment_terminator_axis = expand(
    name=named_choice(suffix="comment_terminator"),
    choices=members(
        option=_COMMENT_FORMAT, include_default=True, accepts=_comment_suffix
    ),
)
# The settings a language may take are ``None`` -- the narrow rendering
# with no JSON value type -- together with each member of its
# ``JsonTypes`` enum.  The JSON-capable languages default to ``None``
# and gain their value type here, while D defaults to its only value
# type and narrows back.  A language whose value type is better known by
# its representation than by its member name declares that name itself.
_json_type_axis = expand(
    name=named_choice(suffix="json_type"),
    choices=_json_type_choices,
    requires=(has_option(option="json_type"),),
)


AXES: Mapping[str, Axis] = _registry(
    # Anonymous records use the same epoch scalar option as named records.
    anonymous_record_epoch=expand(
        name=named(suffix="anonymous_record_epoch"),
        overrides=(
            pin(option=_DICT_FORMAT, name="ANONYMOUS_RECORD"),
            pin(option=_DATETIME_FORMAT, name="EPOCH"),
        ),
        layouts=BOTH_LAYOUTS,
    ),
    annotation_evaluation=expand(
        name=named_choice(suffix="annotation_evaluation"),
        choices=members(option=_ANNOTATION_EVALUATION),
        requires=(has_option(option="annotation_evaluation"),),
    ),
    array_inference_policy=expand(
        name=named_choice(suffix="array_inference"),
        choices=_array_inference_policy_choices,
        requires=(has_option(option="array_inference_policy"),),
        layouts=BOTH_LAYOUTS,
    ),
    array_inference_policy_mutable=expand(
        name=lambda target, label: (
            f"{target.name}_array_inference_{label}_mutable"
        ),
        choices=_array_inference_policy_choices,
        requires=(has_option(option="array_inference_policy"),),
        overrides=(member(option=_DECLARATION_STYLE, name="VAR"),),
    ),
    array_inference_policy_tuple=expand(
        name=lambda target, label: (
            f"{target.name}_array_inference_{label}_tuple"
        ),
        choices=_array_inference_policy_choices,
        requires=(has_option(option="array_inference_policy"),),
        overrides=(member(option=_SEQUENCE_FORMAT, name="TUPLE"),),
    ),
    array_inference_type_hints=expand(
        name=named(suffix="array_type_hints_always"),
        requires=(has_option(option="array_inference_policy"),),
        overrides=(member(option=_VARIABLE_TYPE_HINTS, name="ALWAYS"),),
        layouts=BOTH_LAYOUTS,
    ),
    bool_format=expand(
        name=named_choice(suffix="bool_format"),
        choices=members(option=_BOOL_FORMAT),
        requires=(has_option(option="bool_format"),),
    ),
    bytes_format=expand(
        name=named_choice(suffix="bytes_format"),
        choices=members(option=_BYTES_FORMAT),
    ),
    # These caller contracts exercise C# reference annotations for null values.
    csharp_object_carrier=expand(
        name=named(suffix="object_carrier"),
        requires=(
            lambda target: target.lang_cls.supports_nullable_object_fallbacks,
        ),
        overrides=_CSHARP_OBJECT_CARRIER_OPTIONS,
        layouts=BOTH_LAYOUTS,
    ),
    csharp_object_carrier_records=expand(
        name=named(suffix="object_carrier_records"),
        requires=(
            lambda target: target.lang_cls.supports_nullable_object_fallbacks,
        ),
        overrides=(
            *_CSHARP_OBJECT_CARRIER_OPTIONS,
            member(option=_HETEROGENEOUS_STRATEGY, name="RECORD"),
        ),
        layouts=BOTH_LAYOUTS,
    ),
    csharp_object_array_fallback=expand(
        name=named_choice(suffix="object_array_fallback"),
        choices=values(
            kwarg="default_sequence_element_type",
            qualified_nullable="System.Object?",
            non_nullable="object",
            dynamic="dynamic",
        ),
        requires=(
            lambda target: target.lang_cls.supports_nullable_object_fallbacks,
        ),
        overrides=(member(option=_SEQUENCE_FORMAT, name="ARRAY"),),
    ),
    custom_value_field_names=expand(
        name=named(suffix="field_names_custom"),
        requires=(has_sample(kwarg="bool_field"),),
        overrides=(
            sample(kwarg="bool_field"),
            sample(kwarg="int_field"),
            sample(kwarg="uint_field"),
            sample(kwarg="float_field"),
            sample(kwarg="string_field"),
            sample(kwarg="array_field"),
            sample(kwarg="map_field"),
            sample(kwarg="key_field"),
            sample(kwarg="value_field"),
        ),
    ),
    # Every language renders the shared input under both layouts.  The
    # middle name segment is language metadata, because the COBOL fixtures
    # call it ``layout`` rather than ``collection_layout``.
    collection_layout=expand(
        name=lambda target, _label: (
            f"{target.name}_{target.metadata.golden.collection_layout_category}"
        ),
        layouts=((COMPACT, "_compact"), (MULTILINE, "_multiline")),
    ),
    comment=expand(
        name=named_choice(suffix="comment"),
        choices=members(option=_COMMENT_FORMAT),
    ),
    comment_terminator=_comment_terminator_axis,
    comment_terminator_call=filtered(
        base=_comment_terminator_axis,
        requires=(
            lambda variant: bool(variant.lang_cls.CallStyles),
            lambda variant: (
                variant.lang_cls.supports_standalone_comments_in_wrapped_calls
            ),
        ),
    ),
    constructor_name=expand(
        name=named(suffix="constructor_names_j"),
        requires=(has_sample(kwarg="null_name"),),
        overrides=(
            sample(kwarg="null_name"),
            sample(kwarg="bool_name"),
            sample(kwarg="int_name"),
            sample(kwarg="real_name"),
            sample(kwarg="str_name"),
            sample(kwarg="list_name"),
            sample(kwarg="map_name"),
            sample(kwarg="set_name"),
            sample(kwarg="entry_name"),
        ),
    ),
    constructor_prefix=expand(
        name=_named_sample(suffix="prefix", option="constructor_prefix"),
        requires=(has_sample(kwarg="constructor_prefix"),),
        overrides=(sample(kwarg="constructor_prefix"),),
    ),
    date=expand(
        name=named_choice(suffix="date"), choices=members(option=_DATE_FORMAT)
    ),
    datetime=expand(
        name=named_choice(suffix="datetime"),
        choices=members(option=_DATETIME_FORMAT),
    ),
    datetime_epoch=expand(
        name=named(suffix="datetime_epoch"),
        overrides=(pin(option=_DATETIME_FORMAT, name="EPOCH"),),
    ),
    datetime_python=expand(
        name=named(suffix="datetime_python"),
        overrides=(pin(option=_DATETIME_FORMAT, name="PYTHON"),),
    ),
    datetime_javascript=expand(
        name=named(suffix="datetime_javascript"),
        overrides=(pin(option=_DATETIME_FORMAT, name="JS"),),
    ),
    datetime_php=expand(
        name=named(suffix="datetime_php"),
        overrides=(pin(option=_DATETIME_FORMAT, name="PHP"),),
    ),
    datetime_swift=expand(
        name=named(suffix="datetime_swift"),
        overrides=(pin(option=_DATETIME_FORMAT, name="SWIFT"),),
    ),
    declaration_style=expand(
        name=named_choice(suffix="declaration_style"),
        choices=members(
            option=_DECLARATION_STYLE, extra_options=declaration_sequence
        ),
    ),
    # Static declarations infer a datetime type for these values.
    static_datetime_declaration=expand(
        name=named(suffix="declaration_style_static"),
        overrides=(
            pin(option=_DECLARATION_STYLE, name="STATIC"),
            pin(option=_SEQUENCE_FORMAT, name="ARRAY"),
        ),
    ),
    default_dict_key_type=expand(
        name=named(suffix="default_dict_key_type"),
        requires=(has_sample(kwarg="default_dict_key_type"),),
        overrides=(sample(kwarg="default_dict_key_type"),),
    ),
    default_dict_value_type=expand(
        name=named(suffix="default_dict_value_type_string"),
        requires=(has_sample(kwarg="default_dict_value_type"),),
        overrides=(sample(kwarg="default_dict_value_type"),),
    ),
    default_ordered_map_value_type=expand(
        name=named(suffix="default_ordered_map_value_type"),
        requires=(has_sample(kwarg="default_ordered_map_value_type"),),
        overrides=(sample(kwarg="default_ordered_map_value_type"),),
    ),
    default_sequence_element_type=expand(
        name=named(suffix="default_sequence_element_type_string"),
        requires=(has_sample(kwarg="default_sequence_element_type"),),
        overrides=(sample(kwarg="default_sequence_element_type"),),
    ),
    default_set_element_type=expand(
        name=named(suffix="default_set_element_type_string"),
        requires=(has_sample(kwarg="default_set_element_type"),),
        overrides=(sample(kwarg="default_set_element_type"),),
    ),
    # Mirrors ``nested_map_widening`` for Dhall's ``UNION_TYPE`` strategy,
    # against a dedicated input.  Dhall renders dicts as records whose type
    # is fixed by their field set, so the shared input (whose sibling inner
    # maps also differ in *which* keys they carry) can never type-check as a
    # Dhall list regardless of widening.  This input keeps every sibling
    # inner map at the same key set while diverging its scalar value types,
    # so the widening fix is exactly what makes the list type-check (#2897).
    # Both axes reuse the same strategy predicate.
    nested_map_widening_uniform_keys=expand(
        name=named(suffix="nested_map_widening"),
        requires=(
            lambda target: (
                target.metadata.variants.nested_map_widening == "uniform_keys"
            ),
        ),
        overrides=_NESTED_MAP_WIDENING_SCALAR_WRAPPING_OPTIONS,
        layouts=BOTH_LAYOUTS,
    ),
    dict_decl=expand(
        name=named_choice(suffix="dict"),
        choices=cross(
            primary=members(option=_DICT_FORMAT),
            decl=members(
                option=_DECLARATION_STYLE, extra_options=declaration_sequence
            ),
        ),
    ),
    dict_entry_style=expand(
        name=named_choice(suffix="dict_entry_style"),
        choices=members(option=_DICT_ENTRY_STYLE),
    ),
    dict_format=expand(
        name=named_choice(suffix="dict_format"),
        choices=members(option=_DICT_FORMAT),
    ),
    # The hints themselves are fixture data: which value in the input gets
    # an explicit type, and what that type is spelled as, are choices the
    # language's own manifest makes alongside the strategy they hold under.
    # The table override comes first because it is what admits a language:
    # one declaring no hints does not participate, so the strategy those
    # hints are held under is never read for it.
    empty_container_type_hint=expand(
        name=named(suffix="empty_container_type_hint"),
        overrides=(
            _empty_container_hints,
            metadata_member(
                option=_HETEROGENEOUS_STRATEGY, read=_empty_container_strategy
            ),
        ),
    ),
    empty_dict_key=expand(
        name=named_choice(suffix="empty_dict_key"),
        choices=members(option=_EMPTY_DICT_KEY),
        requires=(has_option(option="empty_dict_key"),),
    ),
    # An empty map beside a non-empty map sibling must borrow the sibling's
    # concrete key/value types, or the fallback type of the empty literal
    # disagrees with the sibling and the list fails to compile (V issue
    # #3015: ``[map[string]IVal{}, {'x': 1}]`` is rejected because the
    # ``int`` value cannot coerce to the ``IVal`` interface; Rust issue
    # #3013: ``HashMap::<String, String>::from([])`` disagrees with the
    # sibling ``HashMap<&str, i32>``).  Only languages whose
    # ``dict_format_config`` declares a ``narrowed_empty_form`` narrow the
    # empty map this way; the others have their own, still-divergent
    # handling of this shape.
    empty_map_narrowing=expand(
        name=named(suffix="empty_map_narrowing"),
        requires=(
            lambda target: (
                target.default_spec.dict_format_config.narrowed_empty_form
                is not None
            ),
        ),
        layouts=BOTH_LAYOUTS,
    ),
    error_record_shape_names=expand(
        name=lambda target, _label: (
            f"{target.name}_error_record_shape_names_{_EXTERNAL_RECORD}"
        ),
        requires=(lambda target: target.lang_cls.supports_record_shape_names,),
        overrides=_ERROR_RECORD_SHAPE_NAMES_OPTIONS,
        fixture_options=_record_version,
        preamble=functools.partial(
            _external_cpp_type_preamble,
            name=_EXTERNAL_RECORD,
            source='{"first": "", "last": ""}',
            strategy="ERROR",
        ),
    ),
    float_format=expand(
        name=named_choice(suffix="float_format"),
        choices=members(option=_FLOAT_FORMAT),
    ),
    scientific_float_precision=expand(
        name=named(suffix="float_format_scientific_precision"),
        overrides=(pin(option=_FLOAT_FORMAT, name="SCIENTIFIC"),),
    ),
    heterogeneous_strategy=expand(
        name=named_choice(suffix="heterogeneous_strategy"),
        choices=members(option=_HETEROGENEOUS_STRATEGY),
    ),
    heterogeneous_strategy_record=expand(
        name=named(suffix="heterogeneous_strategy_record"),
        overrides=(pin(option=_HETEROGENEOUS_STRATEGY, name="RECORD"),),
    ),
    heterogeneous_strategy_datetime_cross=expand(
        name=named_choice(suffix="heterogeneous_strategy"),
        choices=cross(
            primary=members(option=_HETEROGENEOUS_STRATEGY),
            datetime=members(option=_DATETIME_FORMAT),
        ),
    ),
    heterogeneous_strategy_tagged_enum=expand(
        name=named(suffix="heterogeneous_strategy_tagged_enum"),
        overrides=(pin(option=_HETEROGENEOUS_STRATEGY, name="TAGGED_ENUM"),),
    ),
    heterogeneous_strategy_tuple_ref_elements=expand(
        name=named(suffix="heterogeneous_strategy_tuple"),
        requires=(
            lambda target: (
                target.lang_cls.variant_metadata.supports_ref_elements_in_tuple_strategy
            ),
        ),
        overrides=(pin(option=_HETEROGENEOUS_STRATEGY, name="TUPLE"),),
    ),
    cpp14_heterogeneous_strategy_tuple=expand(
        name=named(suffix="cpp14_heterogeneous_strategy_tuple"),
        overrides=(
            pin(option=_LANGUAGE_VERSION, name="CPP14"),
            pin(option=_HETEROGENEOUS_STRATEGY, name="TUPLE"),
        ),
    ),
    heterogeneous_value_enum_name=expand(
        name=_named_sample(
            suffix="heterogeneous_value_enum_name",
            option="heterogeneous_value_enum_name",
        ),
        requires=(has_sample(kwarg="heterogeneous_value_enum_name"),),
        overrides=(
            member(option=_HETEROGENEOUS_STRATEGY, name="TAGGED_ENUM"),
            sample(kwarg="heterogeneous_value_enum_name"),
        ),
    ),
    heterogeneous_value_union_name=expand(
        name=_named_sample(
            suffix="heterogeneous_value_union_name",
            option="heterogeneous_value_union_name",
        ),
        requires=(has_sample(kwarg="heterogeneous_value_union_name"),),
        overrides=(
            member(option=_HETEROGENEOUS_STRATEGY, name="UNION_TYPE"),
            sample(kwarg="heterogeneous_value_union_name"),
        ),
    ),
    heterogeneous_value_variant_name=expand(
        name=_named_sample(
            suffix="heterogeneous_value_variant_name",
            option="heterogeneous_value_variant_name",
        ),
        requires=(has_sample(kwarg="heterogeneous_value_variant_name"),),
        overrides=(
            metadata_member(
                option=_HETEROGENEOUS_STRATEGY,
                read=lambda metadata: (
                    metadata.variants.heterogeneous_value_variant_name_strategy
                ),
            ),
            sample(kwarg="heterogeneous_value_variant_name"),
        ),
    ),
    integer_format=expand(
        name=named_choice(suffix="integer_format"),
        choices=members(option=_INTEGER_FORMAT),
    ),
    integer_width_strategy=expand(
        name=named_choice(suffix="integer_width_strategy"),
        choices=members(option=_INTEGER_WIDTH_STRATEGY),
    ),
    # An opt-in rendering choice for languages whose JSON library has both
    # a structural literal form and a parser (today only C++).  Every
    # variant pins the JSON value type non-default, because the option is
    # rejected without one.
    json_rendering=expand(
        name=named_choice(suffix="json_rendering"),
        choices=members(option=_JSON_RENDERING),
        requires=(has_option(option="json_rendering"),),
        overrides=(member(option=_JSON_TYPE, name="NLOHMANN_JSON"),),
    ),
    json_type=_json_type_axis,
    json_type_bytes_cross=expand(
        name=named_choice(suffix="json_type"),
        choices=cross(
            primary=_json_type_choices, bytes=members(option=_BYTES_FORMAT)
        ),
        requires=(has_option(option="json_type"),),
    ),
    # Preserve the C++ variable-form layout regression from issue #3595.
    json_type_variable_multiline=expand(
        name=lambda target, label: (
            f"{target.name}_json_type_{label}_variable_multiline"
        ),
        choices=_json_type_choices,
        requires=(has_option(option="json_type"),),
        layouts=((MULTILINE, ""),),
    ),
    json_type_call_result=filtered(
        base=_json_type_axis,
        requires=(
            lambda variant: variant.lang_cls.supports_json_call_result_binding,
        ),
    ),
    json_type_datetime_cross=expand(
        name=named_choice(suffix="json_type"),
        choices=cross(
            primary=_json_type_choices,
            datetime=members(option=_DATETIME_FORMAT),
        ),
        requires=(has_option(option="json_type"),),
    ),
    # A declaration style a JSON value type cannot be declared under is
    # skipped: the pairing is rejected upfront rather than rendered.
    json_type_declaration_cross=expand(
        name=named_choice(suffix="json_type"),
        choices=cross(
            primary=_json_type_choices,
            declaration_style=members(
                option=_DECLARATION_STYLE, extra_options=declaration_sequence
            ),
        ),
        requires=(has_option(option="json_type"),),
        skip_incompatible=True,
    ),
    json_type_language_version_cross=expand(
        name=named_choice(suffix="json_type"),
        choices=cross(
            primary=_json_type_choices,
            version=members(option=_LANGUAGE_VERSION),
        ),
        requires=(has_option(option="json_type"),),
    ),
    # The shape keys, the shape name and the strategy that puts them to work
    # are the ones ``error_record_shape_names`` declares; this pairs them
    # with each JSON value type.  Unlike that axis, the fixture hosts no
    # external shape declaration: the JSON inputs render the shape inline.
    json_type_record_shape_names_cross=expand(
        name=lambda target, label: (
            f"{target.name}_json_type_{label}_record_shape_names_{_EXTERNAL_RECORD}"
        ),
        choices=_json_type_choices,
        requires=(
            has_option(option="json_type"),
            lambda target: target.lang_cls.supports_record_shape_names,
        ),
        overrides=_ERROR_RECORD_SHAPE_NAMES_OPTIONS,
        fixture_options=_record_version,
    ),
    language_version=expand(
        name=named_choice(suffix="version"),
        choices=members(option=_LANGUAGE_VERSION),
    ),
    # Exercises the False branch of the ``_any_types`` intersection check in
    # the PY38 type-hint preamble builder: the dict value type is not
    # ``Any``, so ``from typing import Any`` is not emitted.
    language_version_cross_dict_type=expand(
        name=_named_sample(
            suffix="version_py38_default_dict_value_type",
            option="default_dict_value_type",
        ),
        requires=(has_sample(kwarg="default_dict_value_type"),),
        overrides=(
            pin(option=_LANGUAGE_VERSION, name="PY38"),
            sample(kwarg="default_dict_value_type"),
        ),
    ),
    # A dict annotation can include a non-empty collection in its value union
    # solely because a different value needs annotation.  Exercise the
    # eager Python 3.8 imports for every collection named by that union.
    python_eager_dict_value_union=expand(
        name=named(suffix="eager_dict_value_union"),
        overrides=(
            pin(option=_LANGUAGE_VERSION, name="PY38"),
            pin(option=_ANNOTATION_EVALUATION, name="EAGER"),
            pin(option=_VARIABLE_TYPE_HINTS, name="ALWAYS"),
        ),
    ),
    # Evaluate native record container annotations using each declared
    # compatible eager collection and union aliases for each Python version.
    python_record_eager_annotations=expand(
        name=named(suffix="record_eager_annotations"),
        requires=(has_member(option=_LANGUAGE_VERSION, name="PY38"),),
        overrides=(
            pin(option=_ANNOTATION_EVALUATION, name="EAGER"),
            pin(option=_HETEROGENEOUS_STRATEGY, name="RECORD"),
            member(option=_VARIABLE_TYPE_HINTS, name="ALWAYS"),
        ),
    ),
    # Record fields are annotated even for assignments without a root hint.
    record_eager_field_annotations=expand(
        name=named(suffix="record_eager_field_annotations"),
        requires=(
            has_member(option=_LANGUAGE_VERSION, name="PY38"),
            has_member(option=_ANNOTATION_EVALUATION, name="EAGER"),
            has_member(option=_HETEROGENEOUS_STRATEGY, name="RECORD"),
        ),
        overrides=_RECORD_EAGER_FIELD_ANNOTATIONS_OPTIONS,
    ),
    # Exercise the other native sequence/set aliases in eager record fields.
    record_eager_collection_aliases=expand(
        name=named(suffix="record_eager_collection_aliases"),
        requires=(
            has_member(option=_LANGUAGE_VERSION, name="PY38"),
            has_member(option=_ANNOTATION_EVALUATION, name="EAGER"),
            has_member(option=_HETEROGENEOUS_STRATEGY, name="RECORD"),
            has_member(option=_SEQUENCE_FORMAT, name="LIST"),
            has_member(option=_SET_FORMAT, name="FROZENSET"),
        ),
        overrides=(
            *_RECORD_EAGER_FIELD_ANNOTATIONS_OPTIONS,
            member(option=_SEQUENCE_FORMAT, name="LIST"),
            member(option=_SET_FORMAT, name="FROZENSET"),
        ),
    ),
    # ALWAYS annotates a declaration whatever its shape, so the annotation
    # names every collection in the data rather than only the ones an
    # emptiness rule forces.  Exercise the eager Python 3.8 imports for a
    # document that holds no empty collection at all.
    python_eager_always_imports=expand(
        name=named(suffix="eager_always_imports"),
        overrides=(
            pin(option=_LANGUAGE_VERSION, name="PY38"),
            pin(option=_ANNOTATION_EVALUATION, name="EAGER"),
            pin(option=_VARIABLE_TYPE_HINTS, name="ALWAYS"),
        ),
    ),
    # tomlkit exposes one body entry per dotted-key statement even when
    # several statements collapse into one rendered top-level mapping key.
    python_toml_dotted_key_comments=expand(
        name=named(suffix="toml_dotted_key_comments"),
        overrides=(pin(option=_LANGUAGE_VERSION, name="PY38"),),
    ),
    # YAML set comments follow the order of unwrapped scalar values.
    # The wrapper class names from ruamel do not determine that order.
    python_yaml_wrapped_set_comments=expand(
        name=named(suffix="yaml_wrapped_set_comments"),
        overrides=(pin(option=_LANGUAGE_VERSION, name="PY38"),),
    ),
    # A preserved first-line comment must not be parsed as Python's source
    # encoding declaration and change the decoding of the generated file.
    python_yaml_encoding_cookie_comment=expand(
        name=named(suffix="yaml_encoding_cookie_comment"),
        overrides=(pin(option=_LANGUAGE_VERSION, name="PY38"),),
    ),
    # Raw-string delimiter bases: one the language's own manifest names, and
    # two every participating language shares.  The punctuation base pins
    # the characters a delimiter may hold, and the exhausted base is long
    # enough that the renderer runs out of candidates and has to fall back.
    multiline_raw_string_delimiter=expand(
        name=named_choice(suffix="multiline_raw_string_delimiter"),
        choices=_multiline_delimiter_choices,
        requires=(has_sample(kwarg="multiline_raw_string_delimiter_base"),),
        overrides=(member(option=_STRING_FORMAT, name="MULTILINE"),),
    ),
    multiline_string=expand(
        name=named(suffix="string_format_multiline"),
        requires=(
            lambda target: target.lang_cls.supports_multiline_string_literals,
        ),
        overrides=(member(option=_STRING_FORMAT, name="MULTILINE"),),
    ),
    # Preserve multiline whitespace through an explicit list representation as
    # well as each language's default sequence representation.
    multiline_string_list=expand(
        name=named(suffix="string_format_multiline_list"),
        requires=(
            lambda target: target.lang_cls.supports_multiline_string_literals,
        ),
        overrides=(
            pin(option=_SEQUENCE_FORMAT, name="LIST"),
            member(option=_STRING_FORMAT, name="MULTILINE"),
        ),
    ),
    # Native record fields keep their scalar representation when alternate
    # datetime, date, or bytes options are selected. Membership in the option
    # enums discovers the languages that can render each combination.
    native_record=expand(
        name=named(suffix="native_record"),
        overrides=(pin(option=_DICT_FORMAT, name="RECORD"),),
    ),
    anonymous_record=expand(
        name=named(suffix="anonymous_record"),
        requires=(has_member(option=_DICT_FORMAT, name="ANONYMOUS_RECORD"),),
        overrides=_ANONYMOUS_RECORD_OPTIONS,
    ),
    anonymous_record_mutable=expand(
        name=named(suffix="anonymous_record_mutable"),
        requires=(
            has_member(option=_DICT_FORMAT, name="ANONYMOUS_RECORD"),
            has_member(option=_DECLARATION_STYLE, name="LET_MUTABLE"),
        ),
        overrides=(
            *_ANONYMOUS_RECORD_OPTIONS,
            member(option=_DECLARATION_STYLE, name="LET_MUTABLE"),
        ),
    ),
    native_record_indent=expand(
        name=named_choice(suffix="native_record_indent"),
        choices=values(kwarg="indent", two_spaces="  "),
        overrides=(pin(option=_DICT_FORMAT, name="RECORD"),),
        layouts=((MULTILINE, ""),),
    ),
    native_record_bytes=expand(
        name=named_choice(suffix="native_record_bytes"),
        choices=members(option=_BYTES_FORMAT, include_default=True),
        overrides=(pin(option=_DICT_FORMAT, name="RECORD"),),
        layouts=BOTH_LAYOUTS,
    ),
    native_record_epoch=expand(
        name=named(suffix="native_record_epoch"),
        overrides=(
            pin(option=_DICT_FORMAT, name="RECORD"),
            pin(option=_DATETIME_FORMAT, name="EPOCH"),
        ),
        layouts=BOTH_LAYOUTS,
    ),
    native_record_iso_temporal=expand(
        name=named(suffix="native_record_iso_temporal"),
        overrides=(
            pin(option=_DICT_FORMAT, name="RECORD"),
            pin(option=_DATE_FORMAT, name="ISO"),
            pin(option=_DATETIME_FORMAT, name="ISO"),
        ),
        layouts=BOTH_LAYOUTS,
    ),
    # Sibling dict values that are themselves maps share one declared value
    # type in the enclosing container, but each inner map otherwise renders
    # with its own narrowed opener, so a map narrower than the widened slot
    # type does not compile (issue #2878; the dict-value analogue of the
    # sibling widening #1471/#1472 applied to call arguments and sequence
    # elements).  Go widens every such inner map to ``map[string]any``
    # (#2878) and Kotlin widens the element maps to
    # ``mapOf<String, Map<String, Any?>>`` (#2890) so each literal matches
    # its declared type.  Only languages that declare this opt-in
    # participate today, so the input stays out of all-languages base
    # discovery; both layouts are covered because the compact and multiline
    # paths render the widened literals separately.
    nested_map_widening=expand(
        name=named(suffix="nested_map_widening"),
        requires=(
            lambda target: (
                target.metadata.variants.nested_map_widening == "default"
            ),
        ),
        layouts=BOTH_LAYOUTS,
    ),
    # The same input, for the languages that widen it by wrapping every
    # sibling map's scalar leaves in a shared value carrier rather than by
    # widening the declared slot type: Rust's ``TAGGED_ENUM`` value enum
    # (#2879), ``OBJECT_VARIANT`` in Nim (#2898), ``VARIANT`` in Mojo
    # (#2895), ``INTERFACE`` in V (#2896), the value union in Zig,
    # and ``RECORD`` with ``std::variant`` in C++
    # alias (#2917).  The strategy is the one whose rendering behavior says
    # so, rather than one named per language.
    nested_map_widening_scalar_wrapping=expand(
        name=named(suffix="nested_map_widening"),
        requires=(
            lambda target: (
                target.metadata.variants.nested_map_widening == "none"
            ),
        ),
        overrides=_NESTED_MAP_WIDENING_SCALAR_WRAPPING_OPTIONS,
        layouts=BOTH_LAYOUTS,
    ),
    nested_tuple_strategy=expand(
        name=named(suffix="heterogeneous_strategy_tuple_nested"),
        overrides=(pin(option=_HETEROGENEOUS_STRATEGY, name="TUPLE"),),
    ),
    numeric_literal_suffix=expand(
        name=named_choice(suffix="numeric_literal_suffix"),
        choices=members(option=_NUMERIC_LITERAL_SUFFIX),
    ),
    numeric_separator=expand(
        name=named_choice(suffix="numeric_separator"),
        choices=members(option=_NUMERIC_SEPARATOR),
    ),
    numeric_style=expand(
        name=named_choice(suffix="numeric_style"),
        choices=members(option=_NUMERIC_STYLE),
    ),
    # Covers formatters whose datetime rendering depends on the selected
    # numeric style, such as Haskell's explicit ``HInt`` constructor around
    # epoch seconds.
    numeric_style_datetime_cross=expand(
        name=named_choice(suffix="numeric_style"),
        choices=cross(
            primary=members(option=_NUMERIC_STYLE),
            datetime=members(option=_DATETIME_FORMAT),
        ),
    ),
    object_variant_containers=expand(
        name=named(suffix="object_variant_containers"),
        overrides=(
            pin(option=_HETEROGENEOUS_STRATEGY, name="OBJECT_VARIANT"),
        ),
    ),
    # ISO dates need no JSON import under OBJECT_VARIANT, while native
    # datetimes still do. Both inputs use this exact option combination.
    object_variant_iso_date=expand(
        name=named(suffix="object_variant_iso_date"),
        overrides=(
            pin(option=_HETEROGENEOUS_STRATEGY, name="OBJECT_VARIANT"),
            pin(option=_DATE_FORMAT, name="ISO"),
        ),
    ),
    record_epoch_i32_overflow=expand(
        name=named(suffix="record_epoch_i32_overflow"),
        overrides=(
            pin(option=_HETEROGENEOUS_STRATEGY, name="RECORD"),
            pin(option=_DATETIME_FORMAT, name="EPOCH"),
        ),
    ),
    record_field_type_split=expand(
        name=named(suffix="record_field_type_split"),
        requires=(
            lambda target: (
                "field_type_split" in target.metadata.record_variants
            ),
        ),
        overrides=(member(option=_HETEROGENEOUS_STRATEGY, name="RECORD"),),
    ),
    record_empty_dict_field=expand(
        name=named(suffix="record_empty_dict_field"),
        requires=(
            lambda target: (
                "empty_dict_field" in target.metadata.record_variants
            ),
        ),
        overrides=(member(option=_HETEROGENEOUS_STRATEGY, name="RECORD"),),
    ),
    record_list_field_type_split=expand(
        name=named(suffix="record_list_field_type_split"),
        requires=(
            lambda target: (
                "list_field_type_split" in target.metadata.record_variants
            ),
        ),
        overrides=(member(option=_HETEROGENEOUS_STRATEGY, name="RECORD"),),
    ),
    record_keyword_field=expand(
        name=named(suffix="record_keyword_field"),
        requires=(
            lambda target: "keyword_field" in target.metadata.record_variants,
        ),
        overrides=(member(option=_HETEROGENEOUS_STRATEGY, name="RECORD"),),
    ),
    native_record_keyword_fields=expand(
        name=named(suffix="record_keyword_fields"),
        requires=(
            lambda target: "keyword_field" in target.metadata.record_variants,
        ),
        overrides=(member(option=_HETEROGENEOUS_STRATEGY, name="RECORD"),),
        fixture_options=_record_version,
    ),
    # The value type of a widened fallback map (see
    # ``record_nested_map_fallback`` below) is data-derived by default, so
    # two inputs sharing one record shape can declare one field two ways.
    # ``WIDE`` pins the strategy's value carrier instead, and only the
    # languages that spell that type into an invariant container expose the
    # option (issue #3748).  Run against the homogeneous fallback input,
    # whose scalars all share one type, these lock in the carrier surviving
    # the very uniformity the default narrows on.  Every effective language
    # version and both layouts are covered for the same reasons as the
    # fallback axis itself.
    record_map_value_typing=expand(
        name=named_choice(suffix="record_map_value_typing"),
        choices=members(option=_RECORD_MAP_VALUE_TYPING),
        requires=(has_option(option="record_map_value_typing"),),
        overrides=(member(option=_HETEROGENEOUS_STRATEGY, name="RECORD"),),
        layouts=BOTH_LAYOUTS,
    ),
    # A list of records whose top-level keys are uniform but whose nested
    # map under one key differs in shape (divergent or disjoint key sets)
    # cannot render that nested field as a record: giving the two nested
    # maps distinct record shapes forces the enclosing records to split, so
    # the ``RECORD`` strategy would reject the sibling list.  The shared
    # widening pass drops such families from the shape mapping, so the outer
    # record survives.  Rust widens the field to
    # ``HashMap<&'static str, Value>`` and wraps the leaves in its value
    # enum (issue #2910).  Go, Java, C#, Kotlin, Scala, and Swift use their
    # universal top types (issues #2911 through #2916).  Crystal, Nim, V, D,
    # Odin, Zig, C, and C++ use language-specific value carriers (issues
    # #2917 and #2919 through #2924).  The remaining ``RECORD`` languages
    # gain their own widening in later sub-issues of #2909, which is what
    # the capability predicate selects on. Every effective version is
    # covered because the
    # widened carrier and aggregate syntax can vary by target standard, and
    # both layouts because their widened-map paths render compact and
    # multiline literals separately.
    record_nested_map_fallback=expand(
        name=named(suffix="record_nested_map_fallback"),
        overrides=(pin(option=_HETEROGENEOUS_STRATEGY, name="RECORD"),),
        requires_configured=lambda spec: (
            spec.heterogeneous_behavior.widens_unrecordizable_nested_sibling_maps
        ),
        layouts=BOTH_LAYOUTS,
    ),
    # Explicit annotations must retain the native record names in root
    # collections as well as in individual record fields.
    record_type_hints_always=expand(
        name=named(suffix="record_type_hints_always"),
        overrides=(
            pin(option=_HETEROGENEOUS_STRATEGY, name="RECORD"),
            pin(option=_VARIABLE_TYPE_HINTS, name="ALWAYS"),
        ),
        layouts=BOTH_LAYOUTS,
    ),
    record_nested_in_ordered_map=expand(
        name=named(suffix="record_nested_in_ordered_map"),
        overrides=(
            pin(option=_HETEROGENEOUS_STRATEGY, name="RECORD"),
            pin(option=_SEQUENCE_FORMAT, name="ARRAY"),
        ),
    ),
    record_nonrecord_dict_field=expand(
        name=named(suffix="record_nonrecord_dict_field"),
        requires=(
            lambda target: (
                "nonrecord_dict_field" in target.metadata.record_variants
            ),
        ),
        overrides=(member(option=_HETEROGENEOUS_STRATEGY, name="RECORD"),),
    ),
    record_null_substitutions_record=expand(
        name=named(suffix="record_null_substitutions_record"),
        requires=(
            lambda target: target.lang_cls.supports_record_struct_name_prefix,
        ),
        overrides=(member(option=_HETEROGENEOUS_STRATEGY, name="RECORD"),),
        fixture_options=_record_version,
    ),
    # Run against the ``record_wide_int`` input, these lock in that a
    # record's declared field type follows the value, not the formatted
    # literal (issue #2306, follow-up to #2297; extended to
    # Kotlin/Java/Scala by #2376): an integer field keeps its value-derived
    # type however the literal is written, and an integer beyond the signed
    # 64-bit range is typed to match its wide-integer overflow-fallback
    # literal instead of the type a formatted-string inspection would infer.
    record_numeric_cross=expand(
        name=named_choice(suffix="heterogeneous_strategy_record"),
        choices=cross(
            primary=single_choice,
            integer=members(option=_INTEGER_FORMAT),
            separator=members(option=_NUMERIC_SEPARATOR),
            suffix=members(option=_NUMERIC_LITERAL_SUFFIX),
        ),
        overrides=(pin(option=_HETEROGENEOUS_STRATEGY, name="RECORD"),),
    ),
    record_quoted_field=expand(
        name=named(suffix="record_quoted_field"),
        requires=(
            lambda target: "quoted_field" in target.metadata.record_variants,
        ),
        overrides=(member(option=_HETEROGENEOUS_STRATEGY, name="RECORD"),),
    ),
    qualified_import_call=expand(
        name=lambda target, _label: f"{target.name}_qualified_import",
        requires=(has_option(option="qualified_imports"),),
        overrides=(
            member(option=_DICT_FORMAT, name="RECORD"),
            fixed_options(qualified_imports=(("Prelude", "Numbers"),)),
        ),
    ),
    record_shape_names=expand(
        name=lambda target, _label: (
            f"{target.name}_record_shape_names_{_NAMED_RECORD}"
        ),
        requires=(lambda target: target.lang_cls.supports_record_shape_names,),
        overrides=(
            member(option=_HETEROGENEOUS_STRATEGY, name="RECORD"),
            fixed_options(
                record_shape_names={
                    frozenset(
                        ("id", "label", "enabled", "related_ids")
                    ): _NAMED_RECORD
                }
            ),
        ),
        fixture_options=_record_version,
        preamble=functools.partial(
            _external_cpp_type_preamble,
            name=_NAMED_RECORD,
            source=(
                '{"id": 1, "label": "x", "enabled": true, "related_ids": [0]}'
            ),
            strategy="RECORD",
        ),
    ),
    record_unify_optional_fields=expand(
        name=named(suffix="record_unify_optional_fields"),
        requires=(
            lambda target: (
                "unify_optional_fields" in target.metadata.record_variants
            ),
        ),
        overrides=(
            member(option=_HETEROGENEOUS_STRATEGY, name="RECORD"),
            fixed_options(record_unify_optional_fields=True),
        ),
    ),
    record_sequence_format=expand(
        name=named_choice(suffix="record_sequence"),
        choices=_sequence_choices,
        overrides=(pin(option=_HETEROGENEOUS_STRATEGY, name="RECORD"),),
    ),
    record_array_sequence=expand(
        name=named(suffix="record_array_sequence"),
        overrides=(
            pin(option=_HETEROGENEOUS_STRATEGY, name="RECORD"),
            pin(option=_SEQUENCE_FORMAT, name="ARRAY"),
        ),
    ),
    # Scalar leaves are valid even when nested tuple records are rejected.
    record_tuple_sequence=expand(
        name=named(suffix="record_tuple_sequence"),
        overrides=(
            pin(option=_HETEROGENEOUS_STRATEGY, name="RECORD"),
            pin(option=_SEQUENCE_FORMAT, name="TUPLE"),
        ),
    ),
    sequence=expand(
        name=named_choice(suffix="sequence"), choices=_sequence_choices
    ),
    # An interface carrier can represent a sequence containing only nulls.
    interface_null_sequence=expand(
        name=named(suffix="heterogeneous_strategy_interface"),
        overrides=(pin(option=_HETEROGENEOUS_STRATEGY, name="INTERFACE"),),
    ),
    # Nested tuple openers need the TUPLE member to represent recursive
    # tuple structure.
    sequence_tuple_nested=expand(
        name=named(suffix="sequence_tuple"),
        overrides=(pin(option=_SEQUENCE_FORMAT, name="TUPLE"),),
    ),
    sequence_tuple_nested_vec=expand(
        name=named(suffix="sequence_tuple_nested_vec"),
        overrides=(pin(option=_SEQUENCE_FORMAT, name="TUPLE_NESTED_VEC"),),
    ),
    sequence_decl=expand(
        name=named_choice(suffix="sequence"),
        choices=cross(
            primary=members(option=_SEQUENCE_FORMAT),
            decl=members(option=_DECLARATION_STYLE),
        ),
        skip_incompatible=True,
    ),
    set=expand(
        name=named_choice(suffix="set"), choices=members(option=_SET_FORMAT)
    ),
    set_decl=expand(
        name=named_choice(suffix="set"),
        choices=cross(
            primary=members(option=_SET_FORMAT),
            decl=members(
                option=_DECLARATION_STYLE, extra_options=declaration_sequence
            ),
        ),
    ),
    statement_terminator_style=expand(
        name=named_choice(suffix="statement_terminator_style"),
        choices=members(option=_STATEMENT_TERMINATOR_STYLE),
    ),
    statement_terminator_style_decl=expand(
        name=named_choice(suffix="statement_terminator_style"),
        choices=cross(
            primary=members(option=_STATEMENT_TERMINATOR_STYLE),
            decl=members(option=_DECLARATION_STYLE),
        ),
    ),
    # The ``string_embedded_nul`` input carries a bare null byte and a null
    # byte immediately before a digit, and each golden pins the escape a
    # language emits for both (issue #3006).  A language participates when
    # its default string formatter escapes them faithfully; one that rejects
    # the value, emits a raw null byte, or emits a digit-greedy escape stays
    # out.  Naming the format says nothing for a language offering one, so
    # those fixtures keep the bare name.
    string_embedded_nul=expand(
        name=named_choice(suffix="string_embedded_nul"),
        choices=members(option=_STRING_FORMAT, include_default=True),
        requires=(
            lambda target: (
                target.lang_cls.variant_metadata.string_literals_escape_null_byte
            ),
        ),
        sole_choice_name=named(suffix="string_embedded_nul"),
    ),
    # A JSON value type escapes null bytes on its own account, whatever the
    # language's default string formatter does, so it opts in per member
    # rather than through the language's own capability.
    string_embedded_nul_json_type=expand(
        name=named_choice(suffix="string_embedded_nul"),
        choices=members(
            option=_JSON_TYPE,
            include_default=True,
            accepts=_escapes_null_byte,
            label=_json_type_label,
        ),
        requires=(has_option(option="json_type"),),
    ),
    scalar_string_embedded_nul=expand(
        name=named(suffix="scalar_string_embedded_nul"),
        requires=(
            lambda target: (
                target.lang_cls.variant_metadata.string_literals_escape_null_byte
            ),
        ),
    ),
    string_format=expand(
        name=named_choice(suffix="string_format"),
        choices=members(
            option=_STRING_FORMAT,
            accepts=lambda selected: selected.name != "MULTILINE",
        ),
    ),
    erlang_noncharacter_string=expand(
        name=named(suffix="noncharacter_string"),
        overrides=(pin(option=_LANGUAGE_VERSION, name="OTP_25"),),
    ),
    erlang_otp_json_noncharacter_string=expand(
        name=named(suffix="otp_json_noncharacter_string"),
        overrides=(
            pin(option=_LANGUAGE_VERSION, name="OTP_25"),
            pin(option=_JSON_TYPE, name="OTP_JSON"),
        ),
    ),
    epoch_datetime_list=expand(
        name=named(suffix="epoch_datetime_list"),
        overrides=(pin(option=_DATETIME_FORMAT, name="EPOCH"),),
    ),
    del_string=expand(
        name=named_choice(suffix="del"),
        choices=members(option=_STRING_FORMAT, include_default=True),
    ),
    toml_basic_string=expand(
        name=named(suffix="basic_string"),
        overrides=(pin(option=_DATE_FORMAT, name="TOML"),),
    ),
    # Cover code paths where the chosen string format interacts with the
    # date or datetime format, such as the plain-ISO fallback that only
    # fires when both are non-default.
    string_format_date_cross=expand(
        name=named_choice(suffix="string"),
        choices=cross(
            primary=members(
                option=_STRING_FORMAT,
                accepts=lambda selected: selected.name != "MULTILINE",
            ),
            date=members(option=_DATE_FORMAT),
        ),
    ),
    string_format_datetime_cross=expand(
        name=named_choice(suffix="string"),
        choices=cross(
            primary=members(
                option=_STRING_FORMAT,
                accepts=lambda selected: selected.name != "MULTILINE",
            ),
            dt=members(option=_DATETIME_FORMAT),
        ),
    ),
    tagged_enum_empty_container=expand(
        name=named(suffix="tagged_enum_empty_container"),
        overrides=(pin(option=_HETEROGENEOUS_STRATEGY, name="TAGGED_ENUM"),),
    ),
    trailing_comma=expand(
        name=named_choice(suffix="trailing_comma"),
        choices=members(option=_TRAILING_COMMA),
    ),
    type_hints=expand(
        name=named_choice(suffix="type_hints"),
        choices=members(option=_VARIABLE_TYPE_HINTS),
    ),
    # Cover code paths where the type annotation depends on the chosen
    # sequence / date / datetime / dict / set / suffix format.
    type_hints_cross=expand(
        name=named_choice(suffix="type_hints"),
        choices=cross(
            primary=members(option=_VARIABLE_TYPE_HINTS),
            seq=members(option=_SEQUENCE_FORMAT),
            date=members(option=_DATE_FORMAT),
            dt=members(option=_DATETIME_FORMAT),
            dict=members(option=_DICT_FORMAT),
            set=members(option=_SET_FORMAT),
            nls=members(option=_NUMERIC_LITERAL_SUFFIX),
        ),
    ),
    typed_dict_null_filtering=expand(
        name=named(suffix="skip_null_dict_values"),
        requires=(lambda target: target.lang_cls.supports_typed_dict_open,),
        overrides=(fixed_options(skip_null_dict_values=True),),
    ),
    type_name=expand(
        name=_named_sample(suffix="type_name", option="type_name"),
        requires=(has_sample(kwarg="type_name"),),
        overrides=(sample(kwarg="type_name"),),
    ),
    union_format=expand(
        name=named_choice(suffix="union_format"),
        choices=members(option=_UNION_FORMAT),
        requires=(has_option(option="union_format"),),
        overrides=(member(option=_HETEROGENEOUS_STRATEGY, name="RECORD"),),
    ),
    nested_empty_map_cousins=expand(
        name=named(suffix="nested_empty_map_cousins"),
        requires=(
            lambda target: (
                target.default_spec.dict_format_config.narrowed_empty_form
                is not None
            ),
        ),
    ),
    nested_list_integer_widening=expand(
        name=named(suffix="nested_list_integer_widening"),
        requires=(
            lambda target: (
                target.metadata.variants.nested_list_widening
                == "integer_width"
            ),
        ),
        overrides=(pin(option=_HETEROGENEOUS_STRATEGY, name="RECORD"),),
    ),
    kotlin_widened_i64_min=expand(
        name=named(suffix="widened_i64_min"),
        requires=(
            lambda target: _supports_widened_integer_formatter(
                target.lang_cls
            ),
        ),
        overrides=(pin(option=_LANGUAGE_VERSION, name="V2_4"),),
    ),
    i64_min_integer_format=expand(
        name=named_choice(suffix="i64_min_integer_format"),
        choices=members(option=_INTEGER_FORMAT),
    ),
    i64_min_record_integer_format=expand(
        name=named_choice(suffix="i64_min_record_integer_format"),
        choices=cross(
            primary=single_choice, integer=members(option=_INTEGER_FORMAT)
        ),
        overrides=(pin(option=_HETEROGENEOUS_STRATEGY, name="RECORD"),),
    ),
    special_float_dict_key=expand(
        name=named(suffix="special_float_dict_key"),
        requires=(
            lambda target: _supports_special_float_dict_keys(target.lang_cls),
        ),
    ),
    datetime_epoch_far_future=expand(
        name=named(suffix="datetime_epoch_far_future"),
        requires=(has_member(option=_LANGUAGE_VERSION, name="PY39"),),
        overrides=(pin(option=_DATETIME_FORMAT, name="EPOCH"),),
    ),
    nested_map_mixed_int_widths=expand(
        name=named(suffix="nested_map_mixed_int_widths"),
        requires=(
            lambda target: _supports_widened_integer_formatter(
                target.lang_cls
            ),
        ),
    ),
    union_format_type_hints=expand(
        name=lambda target, label: (
            f"{target.name}_union_format_{label}_type_hints_always"
        ),
        choices=members(option=_UNION_FORMAT),
        requires=(has_option(option="union_format"),),
        overrides=(member(option=_VARIABLE_TYPE_HINTS, name="ALWAYS"),),
    ),
    zig_v0_12_record=expand(
        name=named(suffix="v0_12_record"),
        overrides=(
            pin(option=_LANGUAGE_VERSION, name="V0_12"),
            pin(option=_HETEROGENEOUS_STRATEGY, name="RECORD"),
        ),
    ),
    yaml_v1_2_control_strings=expand(
        name=named(suffix="v1_2_control_strings"),
        overrides=(pin(option=_LANGUAGE_VERSION, name="V1_2"),),
    ),
    symbol_non_identifier_keys=expand(
        name=named(suffix="symbol_non_identifier_keys"),
        overrides=(pin(option=_DICT_ENTRY_STYLE, name="SYMBOL"),),
    ),
    # The round-trip YAML loader retains explicit scalar tags in
    # ``TaggedScalar`` wrappers that must be demoted before rendering.
    yaml_tagged_scalars=expand(name=named(suffix="yaml_tagged_scalars")),
    # Record inference with an explicitly selected list sequence format.
    record_list_sequence=expand(
        name=named(suffix="record_list_sequence"),
        overrides=(
            pin(option=_HETEROGENEOUS_STRATEGY, name="RECORD"),
            pin(option=_SEQUENCE_FORMAT, name="LIST"),
        ),
    ),
    call_result_var_type_hints_always=expand(
        name=named(suffix="call_result_var_type_hints_always"),
        overrides=(
            pin(option=_DECLARATION_STYLE, name="VAR"),
            pin(option=_VARIABLE_TYPE_HINTS, name="ALWAYS"),
        ),
    ),
    cpp14_heterogeneous_strategy_record=expand(
        name=named(suffix="cpp14_heterogeneous_strategy_record"),
        overrides=(
            pin(option=_LANGUAGE_VERSION, name="CPP14"),
            pin(option=_HETEROGENEOUS_STRATEGY, name="RECORD"),
        ),
    ),
    cpp14_tuple_carrier_name=expand(
        name=_named_sample(
            suffix="cpp14_tuple_carrier",
            option="heterogeneous_value_variant_name",
        ),
        requires=(has_sample(kwarg="heterogeneous_value_variant_name"),),
        overrides=(
            pin(option=_LANGUAGE_VERSION, name="CPP14"),
            pin(option=_HETEROGENEOUS_STRATEGY, name="TUPLE"),
            sample(kwarg="heterogeneous_value_variant_name"),
        ),
    ),
    cpp_tuple_versions=expand(
        name=named(suffix="tuple"),
        requires=(has_member(option=_LANGUAGE_VERSION, name="CPP14"),),
        overrides=(pin(option=_HETEROGENEOUS_STRATEGY, name="TUPLE"),),
    ),
    heterogeneous_tuple_versions=expand(
        name=named(suffix="tuple"),
        overrides=(pin(option=_HETEROGENEOUS_STRATEGY, name="TUPLE"),),
    ),
    epoch_hash_set_boundaries=expand(
        name=named(suffix="epoch_hash_set_boundaries"),
        overrides=(
            pin(option=_DATETIME_FORMAT, name="EPOCH"),
            pin(option=_SET_FORMAT, name="HASH_SET"),
        ),
    ),
    epoch_sorted_set_boundaries=expand(
        name=named(suffix="epoch_sorted_set_boundaries"),
        overrides=(
            pin(option=_DATETIME_FORMAT, name="EPOCH"),
            pin(option=_SET_FORMAT, name="SORTED_SET"),
        ),
    ),
    sequence_array_epoch=expand(
        name=named(suffix="sequence_array_epoch"),
        overrides=(
            pin(option=_SEQUENCE_FORMAT, name="ARRAY"),
            pin(option=_DATETIME_FORMAT, name="EPOCH"),
        ),
    ),
    default_empty_dict_key=expand(
        name=named(suffix="default_empty_dict_key"),
        requires=(
            lambda target: _default_allows_empty_ordered_map_keys(
                target.lang_cls
            ),
        ),
    ),
    list_rendering_policy=expand(
        name=named_choice(suffix="list_rendering"),
        choices=_list_rendering_policy_choices,
        requires=(has_option(option="list_rendering_policy"),),
        layouts=BOTH_LAYOUTS,
    ),
    list_rendering_policy_prefix=expand(
        name=lambda target, label: (
            f"{target.name}_list_rendering_{label}_prefix"
        ),
        choices=_list_rendering_policy_choices,
        requires=(has_option(option="list_rendering_policy"),),
        overrides=(sample(kwarg="constructor_prefix"),),
    ),
    list_rendering_policy_json=expand(
        name=lambda target, label: (
            f"{target.name}_list_rendering_{label}_json"
        ),
        choices=_list_rendering_policy_choices,
        requires=(has_option(option="list_rendering_policy"),),
        overrides=(member(option=_JSON_TYPE, name="JSON_ENCODE_VALUE"),),
    ),
    list_rendering_policy_record=expand(
        name=lambda target, label: (
            f"{target.name}_list_rendering_{label}_record"
        ),
        choices=_list_rendering_policy_choices,
        requires=(has_option(option="list_rendering_policy"),),
        overrides=(member(option=_DICT_FORMAT, name="RECORD"),),
    ),
    # Render an external C++ binding with a move-only record field.
    cpp_external_record_move=expand(
        name=lambda target, _label: (
            f"{target.name}_external_record_move_{_MOVE_ONLY_RECORD}"
        ),
        requires=(
            has_member(option=_SEQUENCE_FORMAT, name="INITIALIZER_LIST"),
        ),
        overrides=(
            member(option=_HETEROGENEOUS_STRATEGY, name="RECORD"),
            fixed_options(
                record_shape_names={
                    frozenset(("move_guard",)): _MOVE_ONLY_RECORD
                },
                move_only_record_names=frozenset({_MOVE_ONLY_RECORD}),
            ),
        ),
    ),
    # Erlang module identifiers are atoms: the accepted boundary is 255
    # characters, while the 256-character rejection stays in the error corpus.
    erlang_module_name_atom_limit=expand(
        name=named_choice(suffix="module_name_atom_limit"),
        choices=values(kwarg="module_name", **{"255_characters": "a" * 255}),
        requires=(has_member(option=_LANGUAGE_VERSION, name="OTP_25"),),
    ),
    program_name=expand(
        name=named_choice(suffix="program_name"),
        choices=values(
            kwarg="program_name", hyphen="my-program", mixed_case="Playlist"
        ),
        requires=(has_option(option="program_name"),),
    ),
    null_constructor_name=expand(
        name=named_choice(suffix="null_constructor"),
        choices=values(
            kwarg="null_constructor_name", empty="Empty", playlist="Playlist"
        ),
        requires=(has_option(option="null_constructor_name"),),
    ),
    dict_entry_spaced_multiline=expand(
        name=named(suffix="dict_entry_spaced_multiline"),
        overrides=(pin(option=_DICT_ENTRY_STYLE, name="SPACED"),),
        layouts=((MULTILINE, ""),),
    ),
    indent_file_body=expand(
        name=named(suffix="indent_file_body_enabled"),
        requires=(has_option(option="indent_file_body"),),
        overrides=(fixed_options(indent_file_body=True),),
    ),
    expand_call_stubs=expand(
        name=named(suffix="expand_call_stubs_enabled"),
        requires=(has_option(option="expand_call_stubs"),),
        overrides=(fixed_options(expand_call_stubs=True),),
    ),
    expanded_call_file=expand(
        name=named_choice(suffix="expanded_call_file"),
        choices=values(kwarg="indent", two_spaces="  ", four_spaces="    "),
        requires=(
            has_option(option="indent_file_body"),
            has_option(option="expand_call_stubs"),
        ),
        overrides=(
            fixed_options(indent_file_body=True),
            fixed_options(expand_call_stubs=True),
        ),
    ),
)
