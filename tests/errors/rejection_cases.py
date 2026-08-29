"""Expand a rejection manifest into the cases the suite runs.

A manifest selects languages -- by gate or by name -- and may vary one
option's members and one list of declared values across them.  This
module turns that declaration into a flat, ordered list of cases, each
carrying the language, the constructor arguments its spec is built
from, and the identifier its line in the golden file is keyed by.
"""

import dataclasses
import enum
import functools
from collections.abc import Mapping, Sequence
from typing import assert_never

from beartype import beartype

import literalizer
from tests.enum_members import enum_member_by_name
from tests.language_gates import LanguageGate, language_gate_admits
from tests.language_options import OPTIONS

from .rejection_manifests import (
    LANGUAGES_BY_NAME,
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
    """Return every language the manifest's gates or list select.

    Both the languages the manifest claims the rejection for and the
    ones it records as accepting the input are drawn from here, so a
    golden file can state the whole population it was built from.
    """
    if manifest.languages:
        return tuple(
            LANGUAGES_BY_NAME[name] for name in sorted(manifest.languages)
        )
    return tuple(
        lang_cls
        for lang_cls in LANGUAGES_BY_NAME.values()
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
    return tuple(option.get_members(lang_cls()))


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
        assert manifest.option is not None  # noqa: S101
        kwargs[OPTIONS[manifest.option].kwarg] = member
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
    suffixes = [
        part.name if isinstance(part, enum.Enum) else repr(part)
        for part in parts
        if part is not None
    ]
    return "".join([lang_cls.__name__, *(f"[{part}]" for part in suffixes)])


@beartype
def _cases_for_languages(
    *,
    manifest: RejectionManifest,
    lang_classes: Sequence[literalizer.LanguageCls],
) -> tuple[RejectionCase, ...]:
    """Return every case *lang_classes* contribute to *manifest*."""
    values: tuple[str | None, ...] = manifest.values or (None,)
    sources: tuple[str | None, ...] = manifest.call.sources or (None,)
    cases: list[RejectionCase] = []
    for lang_cls in lang_classes:
        for member in _option_members(manifest=manifest, lang_cls=lang_cls):
            for value in values:
                for source in sources:
                    # A single source is the manifest's whole subject,
                    # so naming it in every case identifier would say
                    # nothing the manifest does not already say.
                    named_source = source if len(sources) > 1 else None
                    cases.append(
                        RejectionCase(
                            case_id=_case_id(
                                lang_cls=lang_cls,
                                parts=(member, value, named_source),
                            ),
                            lang_cls=lang_cls,
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
    """Return every case whose language must raise the rejection."""
    accepting = frozenset(manifest.accepting_languages)
    selected = [
        lang_cls
        for lang_cls in selected_languages(manifest=manifest)
        if lang_cls.__name__ not in accepting
    ]
    return _cases_for_languages(manifest=manifest, lang_classes=selected)


@functools.cache
@beartype
def accepting_cases(
    *,
    manifest: RejectionManifest,
) -> tuple[RejectionCase, ...]:
    """Return every case whose language is declared not to reject."""
    selected = [
        LANGUAGES_BY_NAME[name] for name in manifest.accepting_languages
    ]
    return _cases_for_languages(manifest=manifest, lang_classes=selected)
