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
def _selected_languages(
    *,
    manifest: RejectionManifest,
) -> tuple[literalizer.LanguageCls, ...]:
    """Return every language the manifest's gates or list select."""
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
                    name=kwarg.member,
                )
            }
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
def _cases_for_languages(
    *,
    manifest: RejectionManifest,
    lang_classes: Sequence[literalizer.LanguageCls],
) -> tuple[RejectionCase, ...]:
    """Return every case *lang_classes* contribute to *manifest*."""
    values: tuple[str | None, ...] = manifest.values or (None,)
    cases: list[RejectionCase] = []
    for lang_cls in lang_classes:
        for member in _option_members(manifest=manifest, lang_cls=lang_cls):
            for value in values:
                suffixes = [
                    part.name if isinstance(part, enum.Enum) else part
                    for part in (member, value)
                    if part is not None
                ]
                case_id = "".join(
                    [lang_cls.__name__, *(f"[{part}]" for part in suffixes)]
                )
                cases.append(
                    RejectionCase(
                        case_id=case_id,
                        lang_cls=lang_cls,
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
        for lang_cls in _selected_languages(manifest=manifest)
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
