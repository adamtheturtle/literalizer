"""Discover input cases and language contexts for ``literalize`` fixtures.

Input parsing and value predicates live in :mod:`case_data`.
This module selects languages and collects the contexts used by
:mod:`golden_scenarios`.
"""

import functools
from collections.abc import Mapping
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
from .case_manifests import (
    load_case_manifests,
)
from .language_specs import (
    make_spec,
    sorted_languages,
)


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
def _lang_raises_for_non_printable_ascii_dict_keys(
    lang_cls: literalizer.LanguageCls,
) -> bool:
    """Return whether a language rejects a non-printable ASCII dict key.

    Used to skip golden-file cases whose input contains such keys for
    languages whose contract is to reject those inputs rather than
    produce rendered output.
    """
    try:
        _ = literalizer.literalize(
            source='{"key\\u0001": 2}',
            input_format=literalizer.InputFormat.JSON,
            language=lang_cls(),
        )
    except (InvalidDictKeyError, UnrepresentableStringError):
        return True
    return False


@functools.cache
@beartype
def _case_data_by_name(*, cases_dir: Path) -> Mapping[str, CaseData]:
    """Parse the shared manifest inventory once for discovery
    predicates.
    """
    return {
        manifest.case_dir.name: load_case_data(input_info=manifest.input)
        for manifest in load_case_manifests(cases_dir=cases_dir)
    }


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
        name
        for name, data in _case_data_by_name(cases_dir=cases_dir).items()
        if has_special_floats(data=data)
    )


@functools.cache
@beartype
def discover_cases(
    *, cases_dir: Path, suite: Literal["base", "combined"]
) -> dict[literalizer.LanguageCls, list[str]]:
    """Group representable suite inputs by their selected language.

    Inspect each input directly instead of joining separate indexes of
    invalid keys, non-ASCII keys and special floats by directory name.
    Both the base and combined scenarios consume the same selection.
    """
    data_by_name = _case_data_by_name(cases_dir=cases_dir)
    groups: dict[literalizer.LanguageCls, list[str]] = {}
    for manifest in load_case_manifests(cases_dir=cases_dir):
        if suite not in manifest.suites:
            continue
        name = manifest.case_dir.name
        data = data_by_name[name]
        non_trivial_keys = has_non_printable_ascii_dict_keys(data=data)
        special_floats = has_special_floats(data=data)
        for lang_cls in sorted_languages():
            if not manifest.selection.admits_language(lang_cls=lang_cls):
                continue
            key_syntax = make_spec(
                lang_cls=lang_cls
            ).dict_format_config.key_syntax
            if key_syntax is not None and has_invalid_dict_keys(
                data=data, key_syntax=key_syntax
            ):
                continue
            if non_trivial_keys and (
                _lang_raises_for_non_printable_ascii_dict_keys(
                    lang_cls=lang_cls
                )
            ):
                continue
            if special_floats and not lang_cls.supports_special_floats:
                continue
            groups.setdefault(lang_cls, []).append(name)
    return groups
