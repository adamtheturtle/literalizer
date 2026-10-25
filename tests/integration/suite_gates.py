"""The language facts a declared golden case or variant axis gates on.

:mod:`tests.language_gates` owns the gates that read a language class
or the spec it builds, which the error suite shares.  The rest are the
golden suite's own: they read the test-owned language metadata, a
spec's nested format configuration, or a rendering behavior of the
strategy a spec selects.  Both halves make one union here, so a case
manifest and an axis plan gate on the same vocabulary and every name
either of them uses is checked against the same registry.

A gate names a property rather than a language, so a selection that
follows from a property stays right when a language gains or loses it.
"""

from collections.abc import Callable, Mapping, Sequence
from typing import Annotated, Literal, assert_never

from beartype import beartype
from pydantic import BaseModel, Field

import literalizer
from literalizer._language import (
    IntegerCallStubResult,
    NullableObjectCallStubResult,
)
from literalizer._statements import (
    CallLiteralSyntax,
    CharacterAndHashRawLiterals,
    PrefixedIdentifierSyntax,
)
from tests.language_gates import (
    CapabilityFlagGate,
    EnumMemberPresentGate,
    ModifierPresentGate,
    SpecFieldPresentGate,
    language_gate_admits,
)
from tests.language_options import CAPABILITY_FLAGS, OPTIONS

from .language_metadata import LanguageMetadata, RecordVariantName


class SuiteGateError(ValueError):
    """A declared gate names something no registry answers to."""


@beartype
def _widens_nested_maps_by_wrapping_scalars(
    spec: literalizer.Language,
) -> bool:
    """Return whether the strategy wraps sibling maps' scalar leaves."""
    behavior = spec.heterogeneous_behavior
    return behavior.widens_nested_maps_by_wrapping_scalars


@beartype
def _widens_unrecordizable_nested_sibling_maps(
    spec: literalizer.Language,
) -> bool:
    """Return whether the strategy widens nested maps no record fits."""
    behavior = spec.heterogeneous_behavior
    return behavior.widens_unrecordizable_nested_sibling_maps


@beartype
def _empty_container_type_hint_strategy(
    metadata: LanguageMetadata,
) -> str | None:
    """Return the strategy the empty-container hints are declared
    under.
    """
    settings = metadata.variants.empty_container_type_hint
    if settings is None:
        return None
    return settings.heterogeneous_strategy


METADATA_FIELDS: Mapping[str, Callable[[LanguageMetadata], str | None]] = {
    "language_id": lambda metadata: metadata.language_id,
    "empty_container_type_hint_heterogeneous_strategy": (
        _empty_container_type_hint_strategy
    ),
    "heterogeneous_value_variant_name_language_version": (
        lambda metadata: (
            metadata.variants.heterogeneous_value_variant_name_language_version
        )
    ),
    "heterogeneous_value_variant_name_strategy": (
        lambda metadata: (
            metadata.variants.heterogeneous_value_variant_name_strategy
        )
    ),
    "nested_map_widening": (
        lambda metadata: metadata.variants.nested_map_widening
    ),
    "nested_list_widening": (
        lambda metadata: metadata.variants.nested_list_widening
    ),
}

# Rendering behaviors a strategy either has or has not.  A gate reads
# one from the spec the caller supplies, and an axis override picks the
# option member whose spec has it; the flag is named here once so
# neither spells it itself.
BEHAVIOR_FLAGS: Mapping[str, Callable[[literalizer.Language], bool]] = {
    "sequence_supports_heterogeneity": (
        lambda spec: spec.sequence_format_config.supports_heterogeneity
    ),
    "widens_nested_maps_by_wrapping_scalars": (
        _widens_nested_maps_by_wrapping_scalars
    ),
    "widens_unrecordizable_nested_sibling_maps": (
        _widens_unrecordizable_nested_sibling_maps
    ),
}

# Optional fields on a spec's nested format configuration, which a
# language either declares a value for or leaves unset.
SPEC_CONFIG_FIELDS: Mapping[str, Callable[[literalizer.Language], object]] = {
    "dict_format_config.narrowed_empty_form": (
        lambda spec: spec.dict_format_config.narrowed_empty_form
    ),
}

# Optional spec fields a gate may test for.  A language that cannot
# configure the option omits the constructor field entirely, so field
# presence is the capability test.
SPEC_FIELDS = frozenset(
    {
        "array_inference_policy",
        "annotation_evaluation",
        "bool_format",
        "empty_dict_key",
        "json_rendering",
        "json_type",
        "record_map_value_typing",
        "union_format",
    }
)


class RecordVariantGate(
    BaseModel,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """Admit languages that opt into a focused record variant."""

    kind: Literal["record_variant"]
    variant: RecordVariantName


class NonDefaultKwargGate(
    BaseModel,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """Admit languages that declare a sample constructor value."""

    kind: Literal["non_default_kwarg"]
    kwarg: Annotated[str, Field(min_length=1)]


class MetadataFieldGate(
    BaseModel,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """Admit languages whose metadata field holds a given value."""

    kind: Literal["metadata_field"]
    field: Annotated[str, Field(min_length=1)]
    value: Annotated[str, Field(min_length=1)]


class SpecConfigFieldPresentGate(
    BaseModel,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """Admit languages whose spec configuration sets an optional
    field.
    """

    kind: Literal["spec_config_field_present"]
    field: Annotated[str, Field(min_length=1)]


class BehaviorFlagGate(
    BaseModel,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """Admit languages whose selected strategy sets a behavior flag.

    Unlike every other gate, this one reads a spec the caller builds
    rather than one the language alone decides: an axis passes the spec
    its overrides select, and a case, which selects languages rather
    than specs, passes the language default.
    """

    kind: Literal["behavior_flag"]
    flag: Annotated[str, Field(min_length=1)]


class CallLiteralFlagGate(BaseModel, extra="forbid", frozen=True, strict=True):
    """Require a literal grammar handled by the actual comment scanner."""

    kind: Literal["call_literal_flag"]
    flag: Literal["regex_literals", "verbatim_strings"]


class CallRawStringPrefixGate(
    BaseModel, extra="forbid", frozen=True, strict=True
):
    """Require a raw-string prefix recognized by the call scanner."""

    kind: Literal["call_raw_string_prefix"]
    prefix: Annotated[str, Field(min_length=1)]


class CallInterpolationGate(
    BaseModel, extra="forbid", frozen=True, strict=True
):
    """Require the scanner's interpolation opener and participating quotes."""

    kind: Literal["call_interpolation"]
    opener: Annotated[str, Field(min_length=1)]
    quotes: Annotated[str, Field(min_length=1)]


class CallCharacterQuoteGate(
    BaseModel, extra="forbid", frozen=True, strict=True
):
    """Require the character quote used by the token scanner."""

    kind: Literal["call_character_quote"]
    quote: Annotated[str, Field(min_length=1)]


class CallHashRawPrefixGate(
    BaseModel, extra="forbid", frozen=True, strict=True
):
    """Require a raw prefix and the actual hash delimiter grammar."""

    kind: Literal["call_hash_raw_prefix"]
    prefix: Annotated[str, Field(min_length=1)]
    marker: Annotated[str, Field(min_length=1)]


class IntegerCallStubGate(BaseModel, extra="forbid", frozen=True, strict=True):
    """Require the native producer's integer-returning value stub."""

    kind: Literal["integer_call_stub"]


class NullableObjectCallStubGate(
    BaseModel, extra="forbid", frozen=True, strict=True
):
    """Require a typed nullable result and native conditional grammar."""

    kind: Literal["nullable_object_call_stub"]


class CallIdentifierPrefixGate(
    BaseModel, extra="forbid", frozen=True, strict=True
):
    """Require a prefixed identifier handled by the production scanner."""

    kind: Literal["call_identifier_prefix"]
    prefix: Annotated[str, Field(min_length=1)]


type CallLiteralGate = (
    CallLiteralFlagGate
    | CallRawStringPrefixGate
    | CallInterpolationGate
    | CallCharacterQuoteGate
    | CallHashRawPrefixGate
    | CallIdentifierPrefixGate
)


@beartype
def call_literal_gate_admits(
    *, gate: CallLiteralGate, syntax: CallLiteralSyntax | None
) -> bool:
    """Read scanner grammar directly without constructing a language
    spec.
    """
    if syntax is None:
        return False
    match gate:
        case CallLiteralFlagGate():
            admitted = (
                syntax.regex_literals
                if gate.flag == "regex_literals"
                else syntax.verbatim_strings
            )
        case CallRawStringPrefixGate():
            span = syntax.literal_span_end
            admitted = gate.prefix in syntax.raw_string_prefixes or (
                isinstance(span, CharacterAndHashRawLiterals)
                and gate.prefix in span.raw_string_prefixes
            )
        case CallInterpolationGate():
            admitted = syntax.interpolation_syntax == (
                gate.opener,
                gate.quotes,
            )
        case CallCharacterQuoteGate():
            span = syntax.literal_span_end
            admitted = (
                isinstance(span, CharacterAndHashRawLiterals)
                and span.character_quote == gate.quote
            )
        case CallHashRawPrefixGate():
            span = syntax.literal_span_end
            admitted = (
                isinstance(span, CharacterAndHashRawLiterals)
                and span.hash_marker == gate.marker
                and gate.prefix in span.raw_string_prefixes
            )
        case CallIdentifierPrefixGate():
            span = syntax.literal_span_end
            admitted = (
                isinstance(span, PrefixedIdentifierSyntax)
                and span.prefix == gate.prefix
            )
        case _ as unreachable:
            assert_never(unreachable)
    return admitted


type SuiteGate = Annotated[
    CapabilityFlagGate
    | RecordVariantGate
    | NonDefaultKwargGate
    | SpecFieldPresentGate
    | EnumMemberPresentGate
    | ModifierPresentGate
    | MetadataFieldGate
    | SpecConfigFieldPresentGate
    | BehaviorFlagGate
    | CallLiteralFlagGate
    | CallRawStringPrefixGate
    | CallInterpolationGate
    | CallCharacterQuoteGate
    | CallHashRawPrefixGate
    | CallIdentifierPrefixGate
    | IntegerCallStubGate
    | NullableObjectCallStubGate,
    Field(discriminator="kind"),
]


@beartype
def no_gates() -> list[SuiteGate]:
    """Return a typed empty gate list for the declaring models."""
    return []


@beartype
def validate_gate_names(
    *,
    subject: str,
    gates: Sequence[SuiteGate],
) -> None:
    """Check every name the gates of *subject* declare.

    An unknown name fails when the declaration loads rather than when
    the languages it selects are rendered, so a stale gate names itself
    instead of quietly selecting nothing.
    """
    for gate in gates:
        match gate:
            case CapabilityFlagGate() if gate.flag not in CAPABILITY_FLAGS:
                msg = f"{subject}: unknown capability flag {gate.flag!r}"
                raise SuiteGateError(msg)
            case SpecFieldPresentGate() if gate.field not in SPEC_FIELDS:
                msg = f"{subject}: unknown spec field {gate.field!r}"
                raise SuiteGateError(msg)
            case EnumMemberPresentGate() if gate.option not in OPTIONS:
                msg = f"{subject}: unknown option {gate.option!r}"
                raise SuiteGateError(msg)
            case MetadataFieldGate() if gate.field not in METADATA_FIELDS:
                msg = f"{subject}: unknown metadata field {gate.field!r}"
                raise SuiteGateError(msg)
            case SpecConfigFieldPresentGate() if (
                gate.field not in SPEC_CONFIG_FIELDS
            ):
                msg = f"{subject}: unknown spec config field {gate.field!r}"
                raise SuiteGateError(msg)
            case BehaviorFlagGate() if gate.flag not in BEHAVIOR_FLAGS:
                msg = f"{subject}: unknown behavior flag {gate.flag!r}"
                raise SuiteGateError(msg)
            case _:
                continue


@beartype
def gate_admits(
    *,
    gate: SuiteGate,
    lang_cls: literalizer.LanguageCls,
    metadata: LanguageMetadata,
    spec: literalizer.Language,
) -> bool:
    """Return whether *gate* admits a language.

    *spec* is the language default for every gate but
    :class:`BehaviorFlagGate`, which reads the spec its caller builds.
    """
    match gate:
        case (
            CapabilityFlagGate()
            | SpecFieldPresentGate()
            | EnumMemberPresentGate()
            | ModifierPresentGate()
        ):
            admits = language_gate_admits(
                gate=gate,
                lang_cls=lang_cls,
                spec=spec,
            )
        case IntegerCallStubGate():
            admits = isinstance(
                lang_cls.call_stub_result, IntegerCallStubResult
            )
        case NullableObjectCallStubGate():
            result = lang_cls.call_stub_result
            admits = (
                isinstance(result, NullableObjectCallStubResult)
                and result.conditional_template is not None
            )
        case RecordVariantGate():
            admits = gate.variant in metadata.record_variants
        case NonDefaultKwargGate():
            admits = gate.kwarg in metadata.non_default_kwargs
        case MetadataFieldGate():
            admits = METADATA_FIELDS[gate.field](metadata) == gate.value
        case SpecConfigFieldPresentGate():
            admits = SPEC_CONFIG_FIELDS[gate.field](spec) is not None
        case BehaviorFlagGate():
            admits = BEHAVIOR_FLAGS[gate.flag](spec)
        case (
            CallLiteralFlagGate()
            | CallRawStringPrefixGate()
            | CallInterpolationGate()
            | CallCharacterQuoteGate()
            | CallHashRawPrefixGate()
            | CallIdentifierPrefixGate()
        ):
            admits = call_literal_gate_admits(
                gate=gate, syntax=lang_cls.call_literal_syntax
            )
        case _ as unreachable:
            assert_never(unreachable)
    return admits


@beartype
def gates_admit(
    *,
    gates: Sequence[SuiteGate],
    lang_cls: literalizer.LanguageCls,
    metadata: LanguageMetadata,
    spec: literalizer.Language,
) -> bool:
    """Return whether every gate in *gates* admits a language."""
    return all(
        gate_admits(
            gate=gate,
            lang_cls=lang_cls,
            metadata=metadata,
            spec=spec,
        )
        for gate in gates
    )
