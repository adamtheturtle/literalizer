"""Discover input cases and language contexts for ``literalize`` fixtures.

Input parsing and value predicates live in :mod:`case_data`.
This module selects languages and collects the contexts used by
:mod:`golden_scenarios`.
"""

import dataclasses
import enum
import functools
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
    has_invalid_dict_keys,
    has_non_printable_ascii_dict_keys,
    has_special_floats,
    load_case_data,
)
from .case_manifests import (
    INDENT_ROLE,
    NO_VARIABLE_FORM_ROLE,
    PRE_INDENT_COMMENT_SCALAR_ROLE,
    PRE_INDENT_CONTAINER_ROLE,
    STATEMENT_TERMINATOR_ROLE,
    CaseManifest,
    case_input,
    load_case_manifests,
)
from .language_metadata import language_metadata
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
def cases_with_invalid_dict_keys(
    *, cases_dir: Path, key_syntax: NewVariableNameSyntax | None
) -> frozenset[str]:
    """Return inputs rejected by the declared dictionary key syntax."""
    if key_syntax is None:
        return frozenset[str]()
    return frozenset(
        case_dir.name
        for case_dir in cases_dir.iterdir()
        if has_invalid_dict_keys(
            data=load_case_data(input_info=case_input(case_dir=case_dir)),
            key_syntax=key_syntax,
        )
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
    result: set[str] = set()
    for case_dir in cases_dir.iterdir():
        input_info = case_input(case_dir=case_dir)
        loaded = load_case_data(input_info=input_info)
        if has_non_printable_ascii_dict_keys(data=loaded):
            result.add(case_dir.name)
    return frozenset(result)


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
    result: set[str] = set()
    for case_dir in cases_dir.iterdir():
        input_info = case_input(case_dir=case_dir)
        loaded = load_case_data(input_info=input_info)
        if has_special_floats(data=loaded):
            result.add(case_dir.name)
    return frozenset(result)


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


@dataclasses.dataclass(frozen=True)
class PreIndentCase:
    """A ``pre_indent_level`` golden-file test case.

    Exercises the interaction between ``pre_indent_level > 0`` and a
    ``NewVariable`` form with a class-field modifier combination —
    the scenario that previously placed the indent between ``=`` and a
    multi-line value and doubly indented continuation lines.
    """

    name: str
    lang_cls: literalizer.LanguageCls
    case_dir_name: str
    pre_indent_level: int
    modifiers: frozenset[enum.Enum]


@dataclasses.dataclass(frozen=True)
class IndentCase:
    """A non-default ``indent`` golden-file test case.

    Re-renders the ``bool_list`` fixture for every language with a
    three-space ``indent`` (a value no language defaults to) to lock
    in the fix from issue #2084: every spec's ``indent`` field must
    actually flow through ``wrap_in_file`` and the core literalizer.
    """

    name: str
    lang_cls: literalizer.LanguageCls
    case_dir_name: str
    indent: str


@dataclasses.dataclass(frozen=True)
class NoVariableFormCase:
    """A ``wrap_in_file=True, variable_form=None`` golden-file case.

    Exercises the shape on every language whose
    :attr:`~literalizer._language.Language.supports_no_variable_wrap_in_file`
    is ``True`` (i.e. the language can represent a bare value at
    file-statement scope).  Languages that opt out are covered by a
    separate error-raising test.
    """

    name: str
    lang_cls: literalizer.LanguageCls
    case_dir_name: str


@functools.cache
@beartype
def build_no_variable_form_cases() -> list[NoVariableFormCase]:
    """Build every declared ``no_variable_form`` case.

    Each role-owning fixture selects the languages that can represent
    its input at file-statement scope.  The historical scalar fixture
    retains its original golden names; additional shapes include their
    case name so several fixtures can share the role.
    """
    manifests = {
        manifest.case_dir.name: manifest
        for manifest in load_case_manifests(cases_dir=_CASES_DIR)
    }
    collected_entries: list[NoVariableFormCase] = []
    for entry_case_dir_name in case_dir_names_for_role(
        cases_dir=_CASES_DIR, role=NO_VARIABLE_FORM_ROLE
    ):
        selection = manifests[entry_case_dir_name].selection
        for entry_lang_cls in sorted_languages():
            if (
                entry_lang_cls.supports_no_variable_wrap_in_file
                and selection.admits_language(lang_cls=entry_lang_cls)
            ):
                if entry_case_dir_name == "scalar_int":
                    effective_name = (
                        f"{entry_lang_cls.__name__}_no_variable_form"
                    )
                else:
                    effective_name = (
                        f"{entry_lang_cls.__name__}_no_variable_form_"
                        f"{entry_case_dir_name}"
                    )
                collected_entries.append(
                    NoVariableFormCase(
                        name=effective_name,
                        lang_cls=entry_lang_cls,
                        case_dir_name=entry_case_dir_name,
                    )
                )
    return collected_entries


@functools.cache
@beartype
def build_indent_cases() -> list[IndentCase]:
    r"""Build one non-default-indent case per language.

    The chosen indent (``"   "``) is three spaces, which is distinct
    from every language's default (``"    "``, ``"  "``, or ``"\t"``)
    so the golden file is guaranteed to diverge from the default-indent
    rendering of the role's fixture unless ``self.indent`` is being
    ignored.
    """
    case_dir_name = case_dir_name_for_role(
        cases_dir=_CASES_DIR,
        role=INDENT_ROLE,
    )
    indent = "   "
    return [
        IndentCase(
            name=f"{lang_cls.__name__}_indent_three_space",
            lang_cls=lang_cls,
            case_dir_name=case_dir_name,
            indent=indent,
        )
        for lang_cls in sorted_languages()
    ]


@functools.cache
@beartype
def build_pre_indent_cases() -> list[PreIndentCase]:
    """Build ``pre_indent_level`` cases keyed off
    ``modifier_combinations``.

    Languages whose ``wrap_in_file`` recognizes class-field modifiers
    (``Java``, ``CSharp``, ``Cpp``) place the declaration directly at
    class scope, so a non-zero ``pre_indent_level`` produces output
    that is both syntactically valid and visually demonstrates the
    fix: the declaration line carries the indent, the value sits flush
    against ``=``, and continuation lines keep their relative offsets.

    The case declaring the container role exercises a multi-line
    container value at indent across every language with class-field
    modifiers.  Languages may additionally opt into the comment-scalar
    role's case through their test metadata.  It exercises a scalar
    whose formatted value is preceded by comment lines carrying the same
    ``line_prefix`` indent.
    """
    container_case_dir_name = case_dir_name_for_role(
        cases_dir=_CASES_DIR,
        role=PRE_INDENT_CONTAINER_ROLE,
    )
    comment_scalar_case_dir_name = case_dir_name_for_role(
        cases_dir=_CASES_DIR,
        role=PRE_INDENT_COMMENT_SCALAR_ROLE,
    )
    cases: list[PreIndentCase] = []
    for lang_cls in sorted_languages():
        cases.extend(
            PreIndentCase(
                name=f"{lang_cls.__name__}_pre_indent_1_{combo.name}",
                lang_cls=lang_cls,
                case_dir_name=container_case_dir_name,
                pre_indent_level=1,
                modifiers=combo.modifiers,
            )
            for combo in lang_cls.modifier_combinations
        )
    for lang_cls in sorted_languages():
        metadata = language_metadata(language_id=lang_cls.language_id)
        if not metadata.variants.pre_indent_comment_scalar:
            continue
        cases.extend(
            PreIndentCase(
                name=(
                    f"{lang_cls.__name__}_pre_indent_1_{combo.name}"
                    f"_{comment_scalar_case_dir_name}"
                ),
                lang_cls=lang_cls,
                case_dir_name=comment_scalar_case_dir_name,
                pre_indent_level=1,
                modifiers=combo.modifiers,
            )
            for combo in lang_cls.modifier_combinations
        )
    return cases
