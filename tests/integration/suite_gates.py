"""Language predicates that golden case manifests can declare.

:mod:`tests.language_gates` owns the gates shared with the error suite.
Golden case manifests may also select on sample constructor values,
rendering behavior and call syntax.
"""

from collections.abc import Callable, Mapping, Sequence
from typing import Annotated, Literal, assert_never

from beartype import beartype
from pydantic import BaseModel, Field

import literalizer
from literalizer._language import (
    IntegerCallStubResult,
    NullableObjectCallStubResult,
    redefinition_config,
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
    SpecFieldAbsentGate,
    SpecFieldPresentGate,
    language_gate_admits,
)
from tests.language_options import CAPABILITY_FLAGS, OPTIONS

from .language_metadata import LanguageMetadata


class SuiteGateError(ValueError):
    """A declared gate names something no registry answers to."""


# Rendering behaviors a case manifest can require of a strategy.
BEHAVIOR_FLAGS: Mapping[str, Callable[[literalizer.Language], bool]] = {
    "declaration_disallows_redefinition": (
        lambda spec: (
            not redefinition_config(
                spec.declaration_style
            ).supports_redefinition
        )
    ),
    "sequence_supports_heterogeneity": (
        lambda spec: spec.sequence_format_config.supports_heterogeneity
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
        "list_rendering_policy",
        "native_argument_layout",
        "program_name",
        "null_constructor_name",
        "indent_file_body",
        "expand_call_stubs",
        "record_map_value_typing",
        "union_format",
    }
)


class NonDefaultKwargGate(
    BaseModel,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """Admit languages that declare a sample constructor value."""

    kind: Literal["non_default_kwarg"]
    kwarg: Annotated[str, Field(min_length=1)]


class BehaviorFlagGate(
    BaseModel,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """Admit languages whose selected strategy sets a behavior flag.

    Case selection supplies the language's default spec.
    """

    kind: Literal["behavior_flag"]
    flag: Annotated[str, Field(min_length=1)]


class CallLiteralFlagGate(BaseModel, extra="forbid", frozen=True, strict=True):
    """Require a literal grammar handled by the actual comment scanner."""

    kind: Literal["call_literal_flag"]
    flag: Literal["regex_literals", "verbatim_strings", "backtick_strings"]


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
    """Require an object result that can be null and a conditional
    expression.
    """

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
            admitted = {
                "regex_literals": syntax.regex_literals,
                "verbatim_strings": syntax.verbatim_strings,
                "backtick_strings": syntax.backtick_strings,
            }[gate.flag]
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
    | NonDefaultKwargGate
    | SpecFieldAbsentGate
    | SpecFieldPresentGate
    | EnumMemberPresentGate
    | ModifierPresentGate
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
            case SpecFieldPresentGate() | SpecFieldAbsentGate() if (
                gate.field not in SPEC_FIELDS
            ):
                msg = f"{subject}: unknown spec field {gate.field!r}"
                raise SuiteGateError(msg)
            case EnumMemberPresentGate() if gate.option not in OPTIONS:
                msg = f"{subject}: unknown option {gate.option!r}"
                raise SuiteGateError(msg)
            case BehaviorFlagGate() if gate.flag not in BEHAVIOR_FLAGS:
                msg = f"{subject}: unknown behavior flag {gate.flag!r}"
                raise SuiteGateError(msg)
            case _:
                continue


@beartype
def _call_stub_gate_admits(
    *,
    gate: IntegerCallStubGate | NullableObjectCallStubGate,
    lang_cls: literalizer.LanguageCls,
) -> bool:
    """Match result gates against the native producer's return type."""
    result = lang_cls.call_stub_result
    if isinstance(gate, IntegerCallStubGate):
        return isinstance(result, IntegerCallStubResult)
    return (
        isinstance(result, NullableObjectCallStubResult)
        and result.conditional_template is not None
    )


@beartype
def gate_admits(
    *,
    gate: SuiteGate,
    lang_cls: literalizer.LanguageCls,
    metadata: LanguageMetadata,
    spec: literalizer.Language,
) -> bool:
    """Return whether *gate* admits a language using its default spec."""
    match gate:
        case (
            CapabilityFlagGate()
            | SpecFieldAbsentGate()
            | SpecFieldPresentGate()
            | EnumMemberPresentGate()
            | ModifierPresentGate()
        ):
            admits = language_gate_admits(
                gate=gate,
                lang_cls=lang_cls,
                spec=spec,
            )
        case IntegerCallStubGate() | NullableObjectCallStubGate():
            admits = _call_stub_gate_admits(gate=gate, lang_cls=lang_cls)
        case NonDefaultKwargGate():
            admits = gate.kwarg in metadata.non_default_kwargs
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
