"""Discover golden-file cases under ``tests/integration/cases``.

Houses the dataclasses and discovery functions for every parameterized
golden-file test except :func:`literalize_call`.  ``test_no_dead_golden_files``
imports from this module to enumerate every expected golden filename.
"""

import dataclasses
import enum
import functools
import math
from pathlib import Path

from beartype import beartype
from ruamel.yaml import YAML

import literalizer
from literalizer.exceptions import InvalidDictKeyError

from .call_cases import CALL_CASE_CONFIGS
from .language_specs import (
    find_redefinition_styles,
    make_spec,
    sorted_languages,
)


@dataclasses.dataclass(frozen=True)
class LiteralizeRefCaseConfig:
    """Configuration for a ``literalize`` ``$ref`` golden-file test
    case.
    """

    case_dir_name: str
    ref_key: str


LITERALIZE_REF_CASE_CONFIGS: list[LiteralizeRefCaseConfig] = [
    LiteralizeRefCaseConfig(
        case_dir_name="literalize_ref_whole",
        ref_key="$ref",
    ),
    LiteralizeRefCaseConfig(
        case_dir_name="literalize_ref_in_dict",
        ref_key="$ref",
    ),
    LiteralizeRefCaseConfig(
        case_dir_name="literalize_ref_in_list",
        ref_key="$ref",
    ),
    LiteralizeRefCaseConfig(
        case_dir_name="literalize_ref_heterogeneous",
        ref_key="$ref",
    ),
    LiteralizeRefCaseConfig(
        case_dir_name="literalize_ref_in_mixed_list",
        ref_key="$ref",
    ),
    LiteralizeRefCaseConfig(
        case_dir_name="literalize_ref_camel_name",
        ref_key="$ref",
    ),
    LiteralizeRefCaseConfig(
        case_dir_name="literalize_ref_deep_nesting",
        ref_key="$ref",
    ),
]

LITERALIZE_DEFAULT_REF_CASE_CONFIGS: list[LiteralizeRefCaseConfig] = [
    LiteralizeRefCaseConfig(
        case_dir_name="literalize_ref_default_nested",
        ref_key="$ref",
    ),
    LiteralizeRefCaseConfig(
        case_dir_name="literalize_ref_default_whole",
        ref_key="$ref",
    ),
]


@functools.cache
def _lang_raises_for_non_printable_ascii_dict_keys(
    lang_cls: literalizer.LanguageCls,
) -> bool:
    """Return ``True`` if the language raises :exc:`InvalidDictKeyError`
    for a dict key containing a non-printable ASCII character.

    Used to skip golden-file cases whose input contains such keys for
    languages whose contract is to raise :exc:`InvalidDictKeyError` for
    those inputs rather than produce rendered output.
    """
    try:
        literalizer.literalize(
            source='{"key\\u0001": 1}',
            input_format=literalizer.InputFormat.JSON,
            language=lang_cls(),
        )
    except InvalidDictKeyError:
        return True
    return False


@beartype
def has_non_printable_ascii_dict_keys(data: object) -> bool:
    """Return ``True`` if *data* contains a dict key that is empty or
    has characters outside printable ASCII.
    """
    match data:
        case dict():
            for key in data:  # pyright: ignore[reportUnknownVariableType]
                if isinstance(key, str) and (
                    not key or not key.isprintable() or not key.isascii()
                ):
                    return True
            return any(
                has_non_printable_ascii_dict_keys(data=v)  # pyright: ignore[reportUnknownArgumentType]
                for v in data.values()  # pyright: ignore[reportUnknownVariableType]
            )
        case list():
            return any(
                has_non_printable_ascii_dict_keys(data=item)  # pyright: ignore[reportUnknownArgumentType]
                for item in data  # pyright: ignore[reportUnknownVariableType]
            )
        case _:
            return False


@functools.cache
@beartype
def cases_with_non_trivial_dict_keys(
    cases_dir: Path,
) -> frozenset[str]:
    """Return case directory names whose input YAML has dict keys that
    some languages cannot represent (empty or non-printable-ASCII).
    """
    yaml = YAML()
    result: set[str] = set()
    for case_dir in cases_dir.iterdir():
        loaded: object = yaml.load(  # pyright: ignore[reportUnknownMemberType]
            stream=(case_dir / "input.yaml").read_text(),
        )
        if has_non_printable_ascii_dict_keys(data=loaded):
            result.add(case_dir.name)
    return frozenset(result)


@beartype
def has_special_floats(data: object) -> bool:
    """Return ``True`` if *data* contains a non-finite float (``inf``,
    ``-inf``, or ``nan``).
    """
    match data:
        case float():
            return not math.isfinite(data)
        case dict():
            return any(
                has_special_floats(data=v)  # pyright: ignore[reportUnknownArgumentType]
                for v in data.values()  # pyright: ignore[reportUnknownVariableType]
            )
        case list():
            return any(
                has_special_floats(data=item)  # pyright: ignore[reportUnknownArgumentType]
                for item in data  # pyright: ignore[reportUnknownVariableType]
            )
        case _:
            return False


@functools.cache
@beartype
def cases_with_special_floats(
    cases_dir: Path,
) -> frozenset[str]:
    """Return case directory names whose input YAML contains a
    non-finite float that some languages cannot produce at runtime.
    """
    yaml = YAML()
    result: set[str] = set()
    for case_dir in cases_dir.iterdir():
        loaded: object = yaml.load(  # pyright: ignore[reportUnknownMemberType]
            stream=(case_dir / "input.yaml").read_text(),
        )
        if has_special_floats(data=loaded):
            result.add(case_dir.name)
    return frozenset(result)


@functools.cache
@beartype
def discover_cases(
    cases_dir: Path,
) -> list[tuple[str, literalizer.LanguageCls]]:
    """Return ``(case_name, lang_cls)`` tuples."""
    call_case_dirs = frozenset(cfg.case_dir_name for cfg in CALL_CASE_CONFIGS)
    ref_case_dirs = frozenset(
        cfg.case_dir_name for cfg in LITERALIZE_REF_CASE_CONFIGS
    )
    default_ref_case_dirs = frozenset(
        cfg.case_dir_name for cfg in LITERALIZE_DEFAULT_REF_CASE_CONFIGS
    )
    non_trivial_key_cases = cases_with_non_trivial_dict_keys(
        cases_dir=cases_dir,
    )
    special_float_cases = cases_with_special_floats(cases_dir=cases_dir)
    cases: list[tuple[str, literalizer.LanguageCls]] = []
    for case_dir in sorted(cases_dir.iterdir()):
        if case_dir.name in call_case_dirs:
            continue
        if case_dir.name in ref_case_dirs:
            continue
        if case_dir.name in default_ref_case_dirs:
            continue
        non_trivial = case_dir.name in non_trivial_key_cases
        special_float = case_dir.name in special_float_cases
        for lang_cls in sorted_languages():
            if non_trivial and _lang_raises_for_non_printable_ascii_dict_keys(
                lang_cls
            ):
                continue
            if special_float and not lang_cls.supports_special_floats:
                continue
            cases.append((case_dir.name, lang_cls))
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
    for case_name, lang_cls in discover_cases(cases_dir=cases_dir):
        groups.setdefault(lang_cls, []).append(case_name)
    return groups


@dataclasses.dataclass(frozen=True)
class CombinedCase:
    """A combined-variable-forms test case for a specific redefinition
    style.
    """

    case_name: str
    lang_name: str
    lang_cls: literalizer.LanguageCls
    declaration_style: enum.Enum
    golden_file_name: str


@functools.cache
@beartype
def discover_combined_cases(cases_dir: Path) -> list[CombinedCase]:
    """Return combined test cases for all redefinition-supporting
    styles.
    """
    call_case_dirs = frozenset(cfg.case_dir_name for cfg in CALL_CASE_CONFIGS)
    ref_case_dirs = frozenset(
        cfg.case_dir_name for cfg in LITERALIZE_REF_CASE_CONFIGS
    )
    default_ref_case_dirs = frozenset(
        cfg.case_dir_name for cfg in LITERALIZE_DEFAULT_REF_CASE_CONFIGS
    )
    non_trivial_key_cases = cases_with_non_trivial_dict_keys(
        cases_dir=cases_dir,
    )
    special_float_cases = cases_with_special_floats(cases_dir=cases_dir)
    cases: list[CombinedCase] = []
    for case_dir in sorted(cases_dir.iterdir()):
        if case_dir.name in call_case_dirs:
            continue
        if case_dir.name in ref_case_dirs:
            continue
        if case_dir.name in default_ref_case_dirs:
            continue
        non_trivial = case_dir.name in non_trivial_key_cases
        special_float = case_dir.name in special_float_cases
        for lang_cls in sorted_languages():
            lang_name = lang_cls.__name__
            if non_trivial and _lang_raises_for_non_printable_ascii_dict_keys(
                lang_cls
            ):
                continue
            if special_float and not lang_cls.supports_special_floats:
                continue
            spec = make_spec(lang_cls=lang_cls)
            redef_styles = find_redefinition_styles(spec=spec)
            for style in redef_styles:
                if style is redef_styles[0]:
                    golden_name = f"{lang_name}_combined"
                else:
                    style_suffix = style.name.lower()
                    golden_name = (
                        f"{lang_name}_combined"
                        f"_declaration_style_{style_suffix}"
                    )
                cases.append(
                    CombinedCase(
                        case_name=case_dir.name,
                        lang_name=lang_name,
                        lang_cls=lang_cls,
                        declaration_style=style,
                        golden_file_name=golden_name,
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
    """
    cases: list[StatementTerminatorCombinedCase] = []
    for lang_cls in sorted_languages():
        lang_name = lang_cls.__name__
        spec = make_spec(lang_cls=lang_cls)
        if not find_redefinition_styles(spec=spec):
            continue
        default_statement_terminator_style = spec.statement_terminator_style
        for statement_terminator_style in spec.statement_terminator_styles:
            if (
                statement_terminator_style
                is default_statement_terminator_style
            ):
                continue
            for case_dir_name in ("simple_sequence", "simple_dict"):
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
    case_dir_name = "dict_mixed_scalars"
    for lang_cls in sorted_languages():
        lang_name = lang_cls.__name__
        spec = make_spec(lang_cls=lang_cls)
        if not find_redefinition_styles(spec=spec):
            continue
        default_strategy = spec.heterogeneous_strategy
        for strategy in spec.heterogeneous_strategies:
            if strategy is default_strategy:
                continue
            name = (
                f"{lang_name}_heterogeneous_strategy"
                f"_{strategy.name.lower()}_combined"
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
    """Build one ``no_variable_form`` case per opt-in language.

    Uses the ``scalar_int`` fixture (``42``) because it is the
    minimum input that exercises the bare-value-at-file-scope shape
    and matches every opt-in language's value vocabulary.
    """
    case_dir_name = "scalar_int"
    return [
        NoVariableFormCase(
            name=f"{lang_cls.__name__}_no_variable_form",
            lang_cls=lang_cls,
            case_dir_name=case_dir_name,
        )
        for lang_cls in sorted_languages()
        if lang_cls.supports_no_variable_wrap_in_file
    ]


@functools.cache
@beartype
def build_indent_cases() -> list[IndentCase]:
    r"""Build one non-default-indent case per language.

    The chosen indent (``"   "``) is three spaces, which is distinct
    from every language's default (``"    "``, ``"  "``, or ``"\t"``)
    so the golden file is guaranteed to diverge from the default-indent
    ``bool_list`` rendering unless ``self.indent`` is being ignored.
    """
    case_dir_name = "bool_list"
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
    """
    cases: list[PreIndentCase] = []
    case_dir_name = "simple_dict"
    for lang_cls in sorted_languages():
        cases.extend(
            PreIndentCase(
                name=f"{lang_cls.__name__}_pre_indent_1_{combo.name}",
                lang_cls=lang_cls,
                case_dir_name=case_dir_name,
                pre_indent_level=1,
                modifiers=combo.modifiers,
            )
            for combo in lang_cls.modifier_combinations
        )
    return cases
