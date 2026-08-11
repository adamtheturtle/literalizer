"""The language facts a declared test may gate a case on.

A gate answers one question about a language -- does its constructor
take this parameter, does this option offer this member, does the class
declare this capability -- so a file that selects languages says which
fact it selects on rather than listing class names.  The golden suite's
variant axes and the error suite's rejection manifests share this
vocabulary, so a fact is spelled one way across both.

Gates that read a language's *test* metadata rather than the language
itself stay with the suite that owns that metadata.
"""

import dataclasses
from typing import Annotated, Literal, assert_never

from beartype import beartype
from pydantic import BaseModel, Field

import literalizer

from .enum_members import find_enum_member
from .language_options import CAPABILITY_FLAGS, OPTIONS


class CapabilityFlagGate(
    BaseModel,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """Admit languages whose class declares a capability flag."""

    kind: Literal["capability_flag"]
    flag: Annotated[str, Field(min_length=1)]


class SpecFieldPresentGate(
    BaseModel,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """Admit languages whose spec exposes an optional field."""

    kind: Literal["spec_field_present"]
    field: Annotated[str, Field(min_length=1)]


class EnumMemberPresentGate(
    BaseModel,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """Admit languages offering a named member of an option enum."""

    kind: Literal["enum_member_present"]
    option: Annotated[str, Field(min_length=1)]
    member: Annotated[str, Field(min_length=1)]


class ModifierPresentGate(
    BaseModel,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """Admit languages whose declarations take a named modifier."""

    kind: Literal["modifier_present"]
    modifier: Annotated[str, Field(min_length=1)]


type LanguageGate = Annotated[
    CapabilityFlagGate
    | SpecFieldPresentGate
    | EnumMemberPresentGate
    | ModifierPresentGate,
    Field(discriminator="kind"),
]


@beartype
def language_gate_admits(
    *,
    gate: CapabilityFlagGate
    | SpecFieldPresentGate
    | EnumMemberPresentGate
    | ModifierPresentGate,
    lang_cls: literalizer.LanguageCls,
    spec: literalizer.Language,
) -> bool:
    """Return whether *gate* admits a language."""
    match gate:
        case ModifierPresentGate():
            admits = (
                find_enum_member(
                    enum_cls=lang_cls.Modifiers,
                    name=gate.modifier,
                )
                is not None
            )
        case CapabilityFlagGate():
            admits = CAPABILITY_FLAGS[gate.flag](lang_cls)
        case SpecFieldPresentGate():
            fields = dataclasses.fields(class_or_instance=spec)
            admits = gate.field in {spec_field.name for spec_field in fields}
        case EnumMemberPresentGate():
            option = OPTIONS[gate.option]
            admits = (
                find_enum_member(
                    enum_cls=option.get_members(spec),
                    name=gate.member,
                )
                is not None
            )
        case _ as unreachable:
            assert_never(unreachable)
    return admits
