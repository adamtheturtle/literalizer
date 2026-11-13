"""Discover input cases and language contexts for ``literalize`` fixtures.

Input parsing and value predicates live in :mod:`case_data`.
This module selects languages and collects the contexts used by
:mod:`golden_scenarios`.
"""

import dataclasses
import enum
import functools
from collections.abc import Mapping
from pathlib import Path
from typing import Literal

from beartype import beartype

import literalizer
from literalizer._language import NewVariableNameSyntax
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
    STATEMENT_TERMINATOR_ROLE,
    CaseManifest,
    load_case_manifests,
)
from .language_specs import (
    find_redefinition_styles,
    make_spec,
    sorted_languages,
)
from .manifest_queries import (
    case_dir_name_for_role,
    case_dir_names_for_role,
    heterogeneous_strategy_role,
)

_CASES_DIR = Path(__file__).parent / "cases"


@beartype
def _selected_languages(
    *, manifest: CaseManifest
) -> list[literalizer.LanguageCls]:
    """Return the languages selected by one case manifest."""
    return [
        lang_cls
        for lang_cls in sorted_languages()
        if manifest.selection.admits_language(lang_cls=lang_cls)
    ]


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
def cases_with_invalid_dict_keys(
    *, cases_dir: Path, key_syntax: NewVariableNameSyntax | None
) -> frozenset[str]:
    """Return inputs rejected by the declared dictionary key syntax."""
    if key_syntax is None:
        return frozenset[str]()
    return frozenset(
        name
        for name, data in _case_data_by_name(cases_dir=cases_dir).items()
        if has_invalid_dict_keys(data=data, key_syntax=key_syntax)
    )


@functools.cache
@beartype
def cases_with_non_trivial_dict_keys(
    cases_dir: Path,
) -> frozenset[str]:
    """Return case directory names whose input has non-printable-ASCII
    dict keys that some languages cannot represent.

    Every case is parsed by its declared format, so a JSON/JSON5/TOML
    case carrying such keys is detected the same as a YAML one.
    """
    return frozenset(
        name
        for name, data in _case_data_by_name(cases_dir=cases_dir).items()
        if has_non_printable_ascii_dict_keys(data=data)
    )


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
) -> list[tuple[str, literalizer.LanguageCls]]:
    """Select representable suite inputs before expanding render
    options.
    """
    non_trivial_key_cases = cases_with_non_trivial_dict_keys(
        cases_dir=cases_dir,
    )
    special_float_cases = cases_with_special_floats(cases_dir=cases_dir)
    cases: list[tuple[str, literalizer.LanguageCls]] = []
    for manifest in load_case_manifests(cases_dir=cases_dir):
        if suite not in manifest.suites:
            continue
        name = manifest.case_dir.name
        for lang_cls in _selected_languages(manifest=manifest):
            if name in cases_with_invalid_dict_keys(
                cases_dir=cases_dir,
                key_syntax=make_spec(
                    lang_cls=lang_cls
                ).dict_format_config.key_syntax,
            ):
                continue
            if name in non_trivial_key_cases and (
                _lang_raises_for_non_printable_ascii_dict_keys(
                    lang_cls=lang_cls
                )
            ):
                continue
            if (
                name in special_float_cases
                and not lang_cls.supports_special_floats
            ):
                continue
            cases.append((name, lang_cls))
    return cases


@functools.cache
@beartype
def group_cases_by_language(
    cases_dir: Path,
) -> dict[
    literalizer.LanguageCls,
    list[str],
]:
    """Return case names grouped by language class.

    The test takes the language as its only pytest axis and iterates
    that language's case names inside the test body with ``subtests``.
    Folding thousands of cases into ~30 cuts collection and per-test
    overhead on slower CI runners (notably Windows).
    """
    groups: dict[literalizer.LanguageCls, list[str]] = {}
    for case_name, lang_cls in discover_cases(
        cases_dir=cases_dir, suite="base"
    ):
        groups.setdefault(lang_cls, []).append(case_name)
    return groups


@dataclasses.dataclass(frozen=True)
class CombinedCase:
    """A combined-variable-forms test case for a specific redefinition
    style.
    """

    case_name: str
    lang_cls: literalizer.LanguageCls
    declaration_style: enum.Enum
    golden_name: str


@functools.cache
@beartype
def discover_combined_cases(
    cases_dir: Path,
) -> list[CombinedCase]:
    """Return combined test cases for all redefinition-supporting
    styles.
    """
    cases: list[CombinedCase] = []
    for case_name, lang_cls in discover_cases(
        cases_dir=cases_dir, suite="combined"
    ):
        lang_name = lang_cls.__name__
        spec = make_spec(lang_cls=lang_cls)
        redef_styles = find_redefinition_styles(spec=spec)
        for style in redef_styles:
            if style is redef_styles[0]:
                golden_name = f"{lang_name}_combined"
            else:
                style_suffix = style.name.lower()
                golden_name = (
                    f"{lang_name}_combined_declaration_style_{style_suffix}"
                )
            cases.append(
                CombinedCase(
                    case_name=case_name,
                    lang_cls=lang_cls,
                    declaration_style=style,
                    golden_name=golden_name,
                )
            )
    return cases


@functools.cache
@beartype
def group_combined_cases_by_language(
    cases_dir: Path,
) -> dict[
    literalizer.LanguageCls,
    list[CombinedCase],
]:
    """Return combined cases grouped by language class.

    The test takes the language as its only pytest axis and iterates
    that language's combined cases inside the test body with
    ``subtests``.  Folding thousands of cases into ~30 cuts collection
    and per-test overhead on slower CI runners (notably Windows).
    """
    groups: dict[literalizer.LanguageCls, list[CombinedCase]] = {}
    for case in discover_combined_cases(cases_dir=cases_dir):
        groups.setdefault(case.lang_cls, []).append(case)
    return groups


@dataclasses.dataclass(frozen=True)
class StatementTerminatorCombinedCase:
    """A combined-variable-forms test case with a non-default line
    ending.
    """

    name: str
    lang_cls: literalizer.LanguageCls
    statement_terminator_style: enum.Enum
    case_dir_name: str


@functools.cache
@beartype
def build_statement_terminator_combined_cases() -> list[
    StatementTerminatorCombinedCase
]:
    """Collect combined (declaration + assignment) test cases for
    non-default statement terminators.

    The inputs are the cases declaring the statement-terminator role: a
    sequence and a dict, so a terminator that only shows up after one
    kind of multi-line value is still covered.
    """
    case_dir_names = case_dir_names_for_role(
        cases_dir=_CASES_DIR,
        role=STATEMENT_TERMINATOR_ROLE,
    )
    cases: list[StatementTerminatorCombinedCase] = []
    for lang_cls in sorted_languages():
        lang_name = lang_cls.__name__
        spec = make_spec(lang_cls=lang_cls)
        if len(find_redefinition_styles(spec=spec)) == 0:
            continue
        default_statement_terminator_style = spec.statement_terminator_style
        for statement_terminator_style in spec.statement_terminator_styles:
            if (
                statement_terminator_style
                is default_statement_terminator_style
            ):
                continue
            for case_dir_name in case_dir_names:
                name = (
                    f"{lang_name}_statement_terminator_style"
                    f"_{statement_terminator_style.name.lower()}_{case_dir_name}"
                )
                cases.append(
                    StatementTerminatorCombinedCase(
                        name=name,
                        lang_cls=lang_cls,
                        statement_terminator_style=statement_terminator_style,
                        case_dir_name=case_dir_name,
                    )
                )
    return cases


@dataclasses.dataclass(frozen=True)
class HeterogeneousStrategyCombinedCase:
    """A combined-variable-forms test case with a non-default
    heterogeneous-scalar strategy.
    """

    name: str
    lang_cls: literalizer.LanguageCls
    heterogeneous_strategy: enum.Enum
    case_dir_name: str


@functools.cache
@beartype
def build_heterogeneous_strategy_combined_cases() -> list[
    HeterogeneousStrategyCombinedCase
]:
    """Collect combined (declaration + assignment) test cases for
    non-default heterogeneous-scalar strategies.
    """
    cases: list[HeterogeneousStrategyCombinedCase] = []
    for lang_cls in sorted_languages():
        lang_name = lang_cls.__name__
        spec = make_spec(lang_cls=lang_cls)
        if len(find_redefinition_styles(spec=spec)) == 0:
            continue
        default_strategy = spec.heterogeneous_strategy
        for strategy in spec.heterogeneous_strategies:
            if strategy is default_strategy:
                continue
            name = (
                f"{lang_name}_heterogeneous_strategy"
                f"_{strategy.name.lower()}_combined"
            )
            case_dir_name = case_dir_name_for_role(
                cases_dir=_CASES_DIR,
                role=heterogeneous_strategy_role(
                    strategy_name=strategy.name,
                ),
            )
            cases.append(
                HeterogeneousStrategyCombinedCase(
                    name=name,
                    lang_cls=lang_cls,
                    heterogeneous_strategy=strategy,
                    case_dir_name=case_dir_name,
                )
            )
    return cases
