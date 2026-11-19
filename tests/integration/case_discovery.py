"""Discover input cases and language contexts for ``literalize`` fixtures.

Input parsing and value predicates live in :mod:`case_data`.
This module selects languages and collects the contexts used by
:mod:`golden_scenarios`.
"""

import dataclasses
import functools
from pathlib import Path
from typing import Literal

from beartype import beartype

import literalizer
from literalizer.exceptions import (
    InvalidDictKeyError,
    UnrepresentableStringError,
)

from .case_data import (
    CaseData,
    has_invalid_dict_keys,
    has_non_printable_ascii_dict_keys,
    has_special_floats,
    load_case_data,
)
from .case_inputs import CaseInput
from .case_manifests import (
    load_case_manifests,
)
from .golden_outcomes import SUCCESS, Exclusion, Success
from .language_specs import (
    make_spec,
    sorted_languages,
)
from .rejection_contracts import rejected_examples


@beartype
def kebab_new_variable_languages() -> tuple[literalizer.LanguageCls, ...]:
    """Return languages whose declaration syntax admits hyphens."""
    return tuple(
        lang_cls
        for lang_cls in sorted_languages()
        if lang_cls.new_variable_name_syntax.accepts(name="my-data")
    )


@beartype
def primed_new_variable_languages() -> tuple[literalizer.LanguageCls, ...]:
    """Return languages whose declaration syntax admits prime suffixes."""
    return tuple(
        lang_cls
        for lang_cls in sorted_languages()
        if lang_cls.new_variable_name_syntax.accepts(name="my_data'")
    )


@functools.cache
def _control_key_rejecting_languages() -> frozenset[literalizer.LanguageCls]:
    """Read the existing error contract for control-bearing mapping
    keys.
    """
    return frozenset(
        case.lang_cls
        for error in (InvalidDictKeyError, UnrepresentableStringError)
        for case in rejected_examples(
            contract="struct_field_names", error=error
        )
        if case.source == r'{"a\u0001b": "value"}'
    )


@dataclasses.dataclass(frozen=True, kw_only=True)
class CaseAdmission:
    """One admitted manifest and its structural discovery outcome."""

    case_name: str
    outcome: Success | Exclusion


@functools.cache
@beartype
def _case_data(*, input_info: CaseInput) -> CaseData:
    """Parse an admitted input once, shared by discovery consumers."""
    return load_case_data(input_info=input_info)


@functools.cache
@beartype
def cases_with_special_floats(
    cases_dir: Path,
) -> frozenset[str]:
    """Return case directory names whose input contains a non-finite
    float that some languages cannot produce at runtime.

    Every case is parsed by its declared format, so a JSON5/TOML case
    expressing ``inf``/``nan`` is detected the same as a YAML one.
    """
    return frozenset(
        manifest.case_dir.name
        for manifest in load_case_manifests(cases_dir=cases_dir)
        if has_special_floats(data=_case_data(input_info=manifest.input))
    )


@beartype
def _discovery_outcome(
    *, data: CaseData, lang_cls: literalizer.LanguageCls
) -> Success | Exclusion:
    """Decide structural participation from input and target contracts."""
    key_syntax = make_spec(lang_cls=lang_cls).dict_format_config.key_syntax
    if key_syntax is not None and has_invalid_dict_keys(
        data=data, key_syntax=key_syntax
    ):
        return Exclusion(reason="mapping key does not fit the target grammar")
    if has_non_printable_ascii_dict_keys(data=data) and (
        lang_cls in _control_key_rejecting_languages()
    ):
        return Exclusion(
            reason=(
                "non-printable or non-ASCII key on a target with "
                "a documented control-key rejection"
            )
        )
    if has_special_floats(data=data) and not lang_cls.supports_special_floats:
        return Exclusion(
            reason="target does not support non-finite float literals"
        )
    return SUCCESS


@functools.cache
@beartype
def discover_case_admissions(
    *,
    cases_dir: Path,
    suite: Literal["base", "combined"],
    lang_cls: literalizer.LanguageCls,
) -> tuple[CaseAdmission, ...]:
    """List structural outcomes for cases whose manifests select the suite.

    Cases outside the suite or its declared backend selection never need
    their source parsed. Shared inputs are cached by their input identity.
    """
    return tuple(
        CaseAdmission(
            case_name=manifest.case_dir.name,
            outcome=_discovery_outcome(
                data=_case_data(input_info=manifest.input), lang_cls=lang_cls
            ),
        )
        for manifest in load_case_manifests(cases_dir=cases_dir)
        if suite in manifest.suites
        and manifest.selection.admits_language(lang_cls=lang_cls)
    )


@functools.cache
@beartype
def discover_cases(
    *,
    cases_dir: Path,
    suite: Literal["base", "combined"],
    lang_cls: literalizer.LanguageCls,
) -> tuple[str, ...]:
    """Return the selected cases for the ordinary literal runner."""
    return tuple(
        entry.case_name
        for entry in discover_case_admissions(
            cases_dir=cases_dir, suite=suite, lang_cls=lang_cls
        )
        if isinstance(entry.outcome, Success)
    )
