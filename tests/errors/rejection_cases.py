"""Expand a rejection manifest into the cases the suite runs.

A manifest selects languages by capability and may vary one
option's members and one list of declared values across them.  This
module turns that declaration into a flat, ordered list of cases, each
carrying the language, the constructor arguments its spec is built
from, and the identifier its line in the golden file is keyed by.
"""

import dataclasses
import enum
import functools
import itertools
from collections.abc import Mapping, Sequence
from typing import assert_never

from beartype import beartype

import literalizer
from tests.enum_members import enum_member_by_name, find_enum_member
from tests.language_gates import LanguageGate, language_gate_admits
from tests.language_options import OPTIONS

from .rejection_manifests import (
    LANGUAGE_CLASSES,
    BooleanKwarg,
    CallSpec,
    EmptyContainerTypeHintsKwarg,
    OptionMemberKwarg,
    OptionUnsetKwarg,
    RecordShapeNamesKwarg,
    RejectionKwarg,
    RejectionManifest,
    TextKwarg,
    substituted,
)


@dataclasses.dataclass(frozen=True, kw_only=True)
class RejectionCase:
    """One language's run of one rejection manifest."""

    case_id: str
    lang_cls: literalizer.LanguageCls
    modifier_cls: literalizer.LanguageCls
    kwargs: Mapping[str, object]
    source: str | None
    value: str | None


@beartype
def _admits(
    *,
    gates: Sequence[LanguageGate],
    lang_cls: literalizer.LanguageCls,
) -> bool:
    """Return whether every gate admits a language."""
    spec = lang_cls()
    return all(
        language_gate_admits(gate=gate, lang_cls=lang_cls, spec=spec)
        for gate in gates
    )


@beartype
def selected_languages(
    *,
    manifest: RejectionManifest,
) -> tuple[literalizer.LanguageCls, ...]:
    """Return every language admitted by the scenario's capability gates.

    An omitted gate admits every language. Requested enum members are
    checked separately for each combination of options and values.
    """
    return tuple(
        lang_cls
        for lang_cls in LANGUAGE_CLASSES
        if _admits(gates=manifest.gates, lang_cls=lang_cls)
    )


@beartype
def _kwarg_values(
    *,
    kwarg: RejectionKwarg,
    lang_cls: literalizer.LanguageCls,
    value: str | None,
) -> Mapping[str, object]:
    """Return the constructor arguments one declared argument makes."""
    resolved: Mapping[str, object]
    match kwarg:
        case OptionMemberKwarg():
            option = OPTIONS[kwarg.option]
            resolved = {
                option.kwarg: enum_member_by_name(
                    enum_cls=option.get_members(lang_cls()),
                    name=substituted(template=kwarg.member, value=value),
                )
            }
        case OptionUnsetKwarg():
            resolved = {OPTIONS[kwarg.option].kwarg: None}
        case BooleanKwarg():
            resolved = {kwarg.kwarg: kwarg.value}
        case TextKwarg():
            resolved = {
                kwarg.kwarg: substituted(template=kwarg.value, value=value)
            }
        case RecordShapeNamesKwarg():
            resolved = {
                "record_shape_names": {
                    frozenset(keys): substituted(template=name, value=value)
                    for keys, name in zip(
                        kwarg.key_sets,
                        kwarg.names,
                        strict=True,
                    )
                }
            }
        case EmptyContainerTypeHintsKwarg():
            resolved = {
                "empty_container_type_hints": {
                    hint.path: hint.type_name for hint in kwarg.hints
                }
            }
        case _ as unreachable:
            assert_never(unreachable)
    return resolved


@beartype
def _option_members(
    *,
    manifest: RejectionManifest,
    lang_cls: literalizer.LanguageCls,
) -> tuple[enum.Enum | None, ...]:
    """Return the option members this manifest runs a language under.

    A manifest naming no option runs each language once, which is
    spelled as a single member of ``None``.
    """
    if manifest.option is None:
        return (None,)
    option = OPTIONS[manifest.option]
    spec = lang_cls()
    if option.kwarg not in {
        field.name for field in dataclasses.fields(class_or_instance=spec)
    }:
        return ()
    return tuple(option.get_members(spec))


@beartype
def _case_kwargs(
    *,
    manifest: RejectionManifest,
    lang_cls: literalizer.LanguageCls,
    member: enum.Enum | None,
    value: str | None,
) -> Mapping[str, object]:
    """Return every constructor argument one case is built from."""
    kwargs: dict[str, object] = {}
    for kwarg in manifest.call.kwargs:
        kwargs.update(
            _kwarg_values(kwarg=kwarg, lang_cls=lang_cls, value=value)
        )
    if member is not None:
        option_name = manifest.option
        if option_name is None:
            raise NotImplementedError
        kwargs[OPTIONS[option_name].kwarg] = member
    return kwargs


@beartype
def _case_id(
    *,
    lang_cls: literalizer.LanguageCls,
    parts: tuple[enum.Enum | str | None, ...],
) -> str:
    """Return the identifier one case's golden line is keyed by.

    An option member is named and a declared value is quoted: the two
    read differently in a golden file, and a value that is the empty
    string is still visible.  A part the case does not vary over is
    left out rather than written as an empty bracket.
    """
    collected_suffixes: list[str] = []
    for entry_part in parts:
        if entry_part is not None:
            if isinstance(entry_part, enum.Enum):
                effective_entry_part = entry_part.name
            else:
                effective_entry_part = repr(entry_part)
            collected_suffixes.append(effective_entry_part)
    suffixes = collected_suffixes
    return "".join([lang_cls.__name__, *(f"[{part}]" for part in suffixes)])


@beartype
def _supports_case(
    *,
    manifest: RejectionManifest,
    lang_cls: literalizer.LanguageCls,
    value: str | None,
) -> bool:
    """Require enum members needed to express the call, without probing it."""
    spec = lang_cls()
    fields = {
        field.name for field in dataclasses.fields(class_or_instance=spec)
    }
    for kwarg in manifest.call.kwargs:
        if isinstance(kwarg, OptionMemberKwarg):
            option = OPTIONS[kwarg.option]
            if (
                option.kwarg not in fields
                or find_enum_member(
                    enum_cls=option.get_members(spec),
                    name=substituted(template=kwarg.member, value=value),
                )
                is None
            ):
                return False
    return True


@beartype
def _modifier_classes(
    *,
    call: CallSpec,
    lang_cls: literalizer.LanguageCls,
) -> tuple[literalizer.LanguageCls, ...]:
    """Select owners by their declared modifier members, not their
    names.
    """
    candidates: Sequence[literalizer.LanguageCls] = (lang_cls,)
    if call.modifier_source == "all":
        candidates = tuple(LANGUAGE_CLASSES)
    return tuple(
        candidate
        for candidate in candidates
        if all(
            find_enum_member(enum_cls=candidate.Modifiers, name=name)
            is not None
            for name in call.modifiers
        )
    )


@beartype
def _modifier_case_part(
    *,
    call: CallSpec,
    modifier_cls: literalizer.LanguageCls,
) -> str | None:
    """Label enum ownership only when the scenario expands that
    dimension.
    """
    if call.modifier_source == "all":
        return f"modifiers={modifier_cls.__name__}"
    return None


@beartype
def _cases_for_languages(
    *,
    manifest: RejectionManifest,
    lang_classes: Sequence[literalizer.LanguageCls],
) -> tuple[RejectionCase, ...]:
    """Return every case *lang_classes* contribute to *manifest*."""
    values: tuple[str | None, ...]
    values = (None,)
    if len(manifest.values) > 0:
        values = manifest.values
    sources: tuple[str | None, ...]
    if len(manifest.call.sources) > 0:
        sources = manifest.call.sources
    else:
        sources = (None,)
    cases: list[RejectionCase] = []
    for lang_cls in lang_classes:
        for member, value, modifier_cls in itertools.product(
            _option_members(manifest=manifest, lang_cls=lang_cls),
            values,
            _modifier_classes(call=manifest.call, lang_cls=lang_cls),
        ):
            if not _supports_case(
                manifest=manifest, lang_cls=lang_cls, value=value
            ):
                continue
            for source in sources:
                # A single source is the manifest's whole subject,
                # so naming it in every case identifier would say
                # nothing the manifest does not already say.
                modifier_source = _modifier_case_part(
                    call=manifest.call, modifier_cls=modifier_cls
                )
                named_source = None
                if len(sources) > 1:
                    named_source = source
                cases.append(
                    RejectionCase(
                        case_id=_case_id(
                            lang_cls=lang_cls,
                            parts=(
                                member,
                                value,
                                named_source,
                                modifier_source,
                            ),
                        ),
                        lang_cls=lang_cls,
                        modifier_cls=modifier_cls,
                        source=source,
                        value=value,
                        kwargs=_case_kwargs(
                            manifest=manifest,
                            lang_cls=lang_cls,
                            member=member,
                            value=value,
                        ),
                    )
                )
    return tuple(cases)


@functools.cache
@beartype
def rejection_cases(
    *,
    manifest: RejectionManifest,
) -> tuple[RejectionCase, ...]:
    """Expand a scenario across languages offering its requested
    options.
    """
    return _cases_for_languages(
        manifest=manifest,
        lang_classes=selected_languages(manifest=manifest),
    )
