"""Discover golden-file cases under ``tests/integration/cases``.

Houses the dataclasses and discovery functions for every parameterized
golden-file test except :func:`literalize_call`.  ``test_no_dead_golden_files``
imports from this module to enumerate every expected golden filename.
"""

import dataclasses
import datetime
import enum
import functools
import json
import math
import re
import tomllib
from pathlib import Path
from typing import Any, assert_never

import json5
from beartype import beartype
from ruamel.yaml import YAML
from ruamel.yaml.comments import TaggedScalar
from typing_extensions import TypeIs

import literalizer
from literalizer._language import NewVariableNameSyntax
from literalizer._parsing import escape_json5_line_separators
from literalizer.exceptions import (
    InvalidDictKeyError,
    UnrepresentableStringError,
)
from literalizer.languages import Matlab

from .case_inputs import CaseInput
from .case_manifests import (
    INDENT_ROLE,
    NO_VARIABLE_FORM_ROLE,
    PRE_INDENT_COMMENT_SCALAR_ROLE,
    PRE_INDENT_CONTAINER_ROLE,
    STATEMENT_TERMINATOR_ROLE,
    CaseManifest,
    case_dir_name_for_role,
    case_dir_names_for_role,
    case_input,
    heterogeneous_strategy_role,
    load_case_manifests,
    manifest_admits_language,
)
from .language_metadata import language_metadata
from .language_specs import (
    find_redefinition_styles,
    make_spec,
    sorted_languages,
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
        if manifest_admits_language(manifest=manifest, lang_cls=lang_cls)
    ]


@beartype
def kebab_new_variable_languages() -> tuple[literalizer.LanguageCls, ...]:
    """Return languages whose declaration syntax admits hyphens."""
    return tuple(
        lang_cls
        for lang_cls in sorted_languages()
        if lang_cls.new_variable_name_syntax
        in {
            NewVariableNameSyntax.ASCII_KEBAB,
            NewVariableNameSyntax.ASCII_KEBAB_LETTER_BOUNDED,
        }
    )


@beartype
def primed_new_variable_languages() -> tuple[literalizer.LanguageCls, ...]:
    """Return languages whose declaration syntax admits prime suffixes."""
    return tuple(
        lang_cls
        for lang_cls in sorted_languages()
        if lang_cls.new_variable_name_syntax
        in {
            NewVariableNameSyntax.LOWER_ASCII_PRIME_SUFFIX,
            NewVariableNameSyntax.LOWER_LETTER_ASCII_PRIME_SUFFIX,
        }
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
        literalizer.literalize(
            source='{"key\\u0001": 2}',
            input_format=literalizer.InputFormat.JSON,
            language=lang_cls(),
        )
    except (InvalidDictKeyError, UnrepresentableStringError):
        return True
    return False


# Every scalar a parser can yield: JSON/JSON5 -> str/int/float/bool/
# None; TOML adds date/datetime/time; YAML via ruamel adds those plus
# bytes (``!!binary``).  Mirrors ``literalizer._types.Scalar`` but is
# spelled out so strict pyright keeps it fully known (the ruamel
# library ships no type stubs).
type _CaseScalar = (
    str
    | int
    | float
    | bool
    | datetime.date
    | datetime.datetime
    | datetime.time
    | bytes
    | None
)
# Parsed case data.  ``load_case_data`` parses YAML with the ``safe``
# loader (and JSON/JSON5/TOML natively), so containers are plain
# ``dict``/``list``/``set`` rather than the ruamel comment-tracking
# subclasses; a precise model keeps ``@beartype`` accurate and strict
# pyright/ty fully resolved.
type CaseData = (
    _CaseScalar
    # A YAML ``!!pairs`` node resolves to a list of two-tuples.
    | tuple[object, CaseData]
    | list[CaseData]
    | dict[object, CaseData]
    | set[_CaseScalar]
    | frozenset[_CaseScalar]
)

_MATLAB_FIELD_NAME = re.compile(pattern=r"^[A-Za-z][A-Za-z0-9_]*$")


def _is_object_dict(value: object, /) -> TypeIs[dict[object, object]]:
    """Narrow a dynamically typed mapping for strict type checkers."""
    return isinstance(value, dict)


def _is_object_list(value: object, /) -> TypeIs[list[object]]:
    """Narrow a dynamically typed sequence for strict type checkers."""
    return isinstance(value, list)


def _demote_yaml_tags(*, value: object) -> object:
    """Demote round-trip-only tagged scalar wrappers for discovery."""
    if isinstance(value, TaggedScalar):
        return vars(value)["value"]
    if _is_object_dict(value):
        return {
            _demote_yaml_tags(value=key): _demote_yaml_tags(value=item)
            for key, item in value.items()
        }
    if _is_object_list(value):
        return [_demote_yaml_tags(value=item) for item in value]
    return value


@beartype
def load_case_data(*, input_info: CaseInput) -> CaseData:
    """Parse a case input file according to its declared format.

    Dispatches on :attr:`_CaseInput.input_format` so discovery code can
    inspect any case's data without knowing which serialization backs
    it.  ``tomllib``/``json``/``json5`` yield plain containers and
    ``ruamel`` yields its comment-tracking mappings; both are walked
    structurally by the ``has_*`` predicates.
    """
    source = input_info.path.read_text(encoding="utf-8")
    parsed: CaseData
    match input_info.input_format:
        case literalizer.InputFormat.JSON:
            parsed = json.loads(s=source)
        case literalizer.InputFormat.JSON5:
            # The library escapes a raw U+2028 or U+2029 inside a
            # string before handing the source to ``json5``, which
            # refuses one; parse the same way so a case may hold
            # what the library accepts (issue #4518).
            parsed = json5.loads(
                s=escape_json5_line_separators(source=source),
                allow_duplicate_keys=False,
            )
        case literalizer.InputFormat.YAML:
            # ``safe`` (not round-trip): yields plain ``dict``/``list``/
            # ``set`` instead of the ruamel comment-tracking subclasses,
            # so the result matches ``CaseData`` exactly.  Comments are
            # irrelevant to the key/float predicates.
            # Plain ``=`` is a legacy value tag in the safe loader, while
            # Literalizer deliberately routes it through the round-trip
            # loader. Mirror that choice so discovery can inspect the same
            # valid fixtures as the public API.
            yaml = YAML() if "=" in source else YAML(typ="safe")
            yaml_parsed: Any = _demote_yaml_tags(
                value=yaml.load(  # pyright: ignore[reportUnknownMemberType]
                    stream=source,
                )
            )
            parsed = yaml_parsed
        case literalizer.InputFormat.TOML:
            # Unlike the other parsers (which return ``Any``),
            # ``tomllib.loads`` is typed ``dict[str, Any]``.  ``dict``
            # keys are invariant, so route it through an ``Any`` so it
            # widens to ``CaseData`` like the rest.
            toml_parsed: Any = tomllib.loads(source)
            parsed = toml_parsed
        case _ as unreachable:
            assert_never(unreachable)
    return parsed


def has_non_printable_ascii_dict_keys(data: CaseData) -> bool:
    """Return whether a nonempty dict key is outside printable ASCII."""
    match data:
        case dict():
            for key in data:
                if isinstance(key, str) and (
                    key and (not key.isprintable() or not key.isascii())
                ):
                    return True
            return any(
                has_non_printable_ascii_dict_keys(data=v)
                for v in data.values()
            )
        case list():
            return any(
                has_non_printable_ascii_dict_keys(data=item) for item in data
            )
        case _:
            return False


def has_invalid_matlab_struct_keys(data: CaseData) -> bool:
    """Return whether *data* contains a key invalid for a MATLAB
    struct.
    """
    match data:
        case dict():
            return any(
                isinstance(key, str)
                and _MATLAB_FIELD_NAME.fullmatch(string=key) is None
                for key in data
            ) or any(
                has_invalid_matlab_struct_keys(data=value)
                for value in data.values()
            )
        case list():
            return any(
                has_invalid_matlab_struct_keys(data=item) for item in data
            )
        case _:
            return False


@functools.cache
@beartype
def cases_with_invalid_matlab_struct_keys(
    cases_dir: Path,
) -> frozenset[str]:
    """Return case names MATLAB's default struct format cannot render."""
    return frozenset(
        case_dir.name
        for case_dir in cases_dir.iterdir()
        if has_invalid_matlab_struct_keys(
            data=load_case_data(input_info=case_input(case_dir=case_dir))
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


def has_special_floats(data: CaseData) -> bool:
    """Return ``True`` if *data* contains a non-finite float (``inf``,
    ``-inf``, or ``nan``).
    """
    match data:
        case float():
            return not math.isfinite(data)
        case dict():
            return any(has_special_floats(data=v) for v in data.values())
        case list():
            return any(has_special_floats(data=item) for item in data)
        case _:
            return False


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
    cases_dir: Path,
) -> list[tuple[str, literalizer.LanguageCls]]:
    """Return ``(case_name, lang_cls)`` tuples."""
    non_trivial_key_cases = cases_with_non_trivial_dict_keys(
        cases_dir=cases_dir,
    )
    special_float_cases = cases_with_special_floats(cases_dir=cases_dir)
    invalid_matlab_cases = cases_with_invalid_matlab_struct_keys(
        cases_dir=cases_dir
    )
    cases: list[tuple[str, literalizer.LanguageCls]] = []
    for manifest in load_case_manifests(cases_dir=cases_dir):
        if "base" not in manifest.suites:
            continue
        case_dir = manifest.case_dir
        non_trivial = case_dir.name in non_trivial_key_cases
        special_float = case_dir.name in special_float_cases
        for lang_cls in _selected_languages(manifest=manifest):
            if lang_cls is Matlab and case_dir.name in invalid_matlab_cases:
                continue
            if non_trivial and _lang_raises_for_non_printable_ascii_dict_keys(
                lang_cls=lang_cls
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
def discover_combined_cases(
    cases_dir: Path,
) -> list[CombinedCase]:
    """Return combined test cases for all redefinition-supporting
    styles.
    """
    non_trivial_key_cases = cases_with_non_trivial_dict_keys(
        cases_dir=cases_dir,
    )
    special_float_cases = cases_with_special_floats(cases_dir=cases_dir)
    invalid_matlab_cases = cases_with_invalid_matlab_struct_keys(
        cases_dir=cases_dir
    )
    cases: list[CombinedCase] = []
    for manifest in load_case_manifests(cases_dir=cases_dir):
        if "combined" not in manifest.suites:
            continue
        case_dir = manifest.case_dir
        non_trivial = case_dir.name in non_trivial_key_cases
        special_float = case_dir.name in special_float_cases
        for lang_cls in _selected_languages(manifest=manifest):
            lang_name = lang_cls.__name__
            if lang_cls is Matlab and case_dir.name in invalid_matlab_cases:
                continue
            if non_trivial and _lang_raises_for_non_printable_ascii_dict_keys(
                lang_cls=lang_cls
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
        if not find_redefinition_styles(spec=spec):
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
    """Build one ``no_variable_form`` case per opt-in language.

    The fixture declaring the role is a bare integer, because that is
    the minimum input that exercises the bare-value-at-file-scope shape
    and matches every opt-in language's value vocabulary.
    """
    case_dir_name = case_dir_name_for_role(
        cases_dir=_CASES_DIR,
        role=NO_VARIABLE_FORM_ROLE,
    )
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
