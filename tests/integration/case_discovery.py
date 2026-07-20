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
import tomllib
from pathlib import Path
from typing import Any, assert_never

import pyjson5
from beartype import beartype
from ruamel.yaml import YAML

import literalizer
from literalizer._language import NewVariableNameSyntax
from literalizer.exceptions import InvalidDictKeyError

from .call_cases import CALL_CASE_CONFIGS
from .language_specs import (
    find_redefinition_styles,
    make_spec,
    sorted_languages,
)

# Case directories consumed only by a dedicated variant axis, never by
# the all-languages base / combined / language-version discovery.  Like
# the call and ``$ref`` case directories, a specialized test owns these.
#
# ``record_wide_int`` carries an integer beyond the signed 64-bit range
# to exercise Go's and Rust's value-derived ``RECORD`` field typing
# (issue #2306) via the ``record_numeric_cross`` axis.  Other languages'
# default heterogeneous representations cannot hold a >2^63 integer in a
# container -- a separate latent issue, not #2306 -- so base-discovering
# it for every language would emit golden files that fail to compile.
#
# The ``tuple_pair_*`` / ``tuple_triple_*`` directories carry
# two-element and three-element mixed scalar arrays solely to exercise
# the ``TUPLE`` heterogeneous strategy (issue #2331; Kotlin
# ``Pair``/``Triple``).  Only the ``heterogeneous_strategy`` axis is
# meaningful for them, so they stay out of the all-languages base
# discovery.
#
# ``record_list_of_records`` carries a record field whose value is a
# list of record-shaped dicts, exercising the ``RECORD`` strategy's
# ``element_record_name`` field typing (issue #2420; C++
# ``std::vector<RecordN>``).  Only the ``heterogeneous_strategy`` axis
# is meaningful for it -- under the default strategy it is just another
# heterogeneous dict already covered elsewhere -- so it stays out of
# the all-languages base discovery.
# ``record_nonrecord_dict_field`` carries a record-shaped dict whose
# ``meta`` field is an empty (non-record) dict.  Its dedicated variant
# builder exercises the widened C# ``object`` field and the documented
# Nim rejection path (the cross-language decision in #2317).  The case
# stays out of all-languages base discovery because only ``RECORD``
# behavior is relevant; other ports do not yet all emit valid code for it.
#
# ``heterogeneous_time_string`` carries ``[09:30:00, "hello"]`` solely
# to drive the ``case datetime.time():`` arm of each language's
# heterogeneous-variant signature builder under the
# ``heterogeneous_strategy`` axis (replacing the
# ``test_datetime_time_heterogeneous_variant_renders`` shim, issue
# #2518).  Under the default per-language strategy it is just another
# heterogeneous list already covered elsewhere, so it stays out of the
# all-languages base discovery; only the ``heterogeneous_strategy``
# axis consumes it.
#
# ``dict_wide_int_key`` carries a single ``{>2^53: "tag"}`` entry to
# pin the dict-key arm of the Perl ``MATH_BIG_INT`` preamble check
# (#2588 follow-up): a wide integer that appears only as a key still
# drives the ``Math::BigInt`` wrapper, so the ``use Math::BigInt;``
# preamble must follow.  Other languages cannot represent the key in a
# base golden, so it stays out of the all-languages base discovery.
VARIANT_ONLY_CASE_DIRS = frozenset(
    {
        "record_wide_int",
        "record_list_of_records",
        "record_nonrecord_dict_field",
        "tuple_pair_record_field",
        "tuple_pair_top_level",
        "tuple_triple_record_field",
        "tuple_triple_top_level",
        "heterogeneous_time_string",
        "dict_wide_int_key",
        "object_variant_mixed_scalar_empty_list",
        "object_variant_integer_widening_tiers",
        "object_variant_null_only_map",
        "object_variant_nested_tables_mixed_int_widths",
        "object_variant_empty_and_nonempty_maps",
        "object_variant_null_only_list",
        "object_variant_scalar_empty_map",
        "object_variant_nested_empty_list_table",
        "object_variant_all_wrapped_children",
        # ``record_keyword_field`` carries dict keys that collide with
        # Rust keywords (``type``, ``match``) and Zig keywords
        # (``error``, ``switch``) to exercise the field-name escaping in
        # each RECORD language: Rust raw identifiers (``r#type``, issue
        # #2880) and Zig quoted identifiers (``@"error"``, issue #2963).
        # Every key that is not one language's keyword renders verbatim
        # there, so both golden files compile.  Only languages that
        # escape keyword field names opt in, so base-discovering it for
        # every language would emit golden files that may fail to compile.
        "record_keyword_field",
        # ``record_quoted_field`` covers quoted identifiers in Zig for keys
        # such as ``a-b``.  Only Zig opts into this capability, so the case
        # remains outside all-languages base discovery.
        "record_quoted_field",
        # ``record_field_type_split`` carries same-key-set dicts whose
        # field types conflict (a nested record with different fields,
        # differing scalar types) in positions that never share a
        # sibling list, so a field-type-splitting RECORD strategy
        # resolves each group to its own struct (Rust issue #2881, Go
        # issue #2888, the remaining RECORD languages issue #2961).  Only
        # the RECORD strategies that split shapes by field type consume
        # the ``record_field_type_split`` variant; the non-RECORD
        # languages would key nothing by field type, so base-discovering
        # it for every language would emit golden files that fail to
        # compile.
        "record_field_type_split",
        # ``record_nested_map_fallback`` carries a list of records whose
        # uniform top-level keys hold nested sibling maps of divergent /
        # disjoint shape, which the ``RECORD`` strategy cannot render as
        # a record (issue #2910).  The shared widening pass drops those
        # maps from the shape mapping so the outer record survives.  Rust,
        # Go, Java, C#, Kotlin, Scala, and Swift are top-type consumers;
        # Rust, Crystal, Nim, V, D, Odin, Zig, C, and C++ use
        # language-specific value carriers (issues #2910 through #2917
        # and #2919 through #2924). Remaining RECORD languages widen in
        # later sub-issues of #2909, so this case stays out of
        # all-languages base discovery.
        "record_nested_map_fallback",
        # ``nested_map_widening`` carries sibling dict values that are
        # maps whose value types diverge (issue #2878).  Each inner map
        # otherwise renders at its own narrower value type while the
        # enclosing container declares the widened type, so only
        # languages that can widen render it as code that compiles: Go
        # and Kotlin widen the opener (issues #2878/#2890) while Rust,
        # Nim, Mojo, V, and C++ wrap the scalar leaves in their
        # ``TAGGED_ENUM`` / ``OBJECT_VARIANT`` / ``VARIANT`` /
        # ``INTERFACE`` / RECORD-map value carriers (issues
        # #2879/#2898/#2895/#2896/#2917).  The Go, Kotlin, Rust, Nim,
        # Mojo, V, and C++ ``nested_map_widening`` variants are the sole
        # consumers, so it stays out of the all-languages base discovery.
        "nested_map_widening",
        # ``empty_map_narrowing`` carries an empty map beside a non-empty
        # map sibling (``[{}, {"x": 1}]``).  Only languages whose
        # ``dict_format_config`` declares a ``narrowed_empty_form`` type
        # the empty literal from the sibling's key/value types so the list
        # compiles (V issue #3015, Rust issue #3013); other statically
        # typed languages still render this shape in different ways, so it
        # stays out of the all-languages base discovery.
        "empty_map_narrowing",
        # ``tagged_enum_empty_list`` / ``tagged_enum_empty_map`` carry a
        # scalar beside an empty list / map (``[1, []]`` / ``[1, {}]``),
        # which has no single element type.  Only a ``TAGGED_ENUM``
        # strategy renders this shape as code that compiles, wrapping the
        # scalar in its value enum and the empty container in a ``List`` /
        # ``Map`` variant (issue #3028); other statically typed languages
        # reject or diverge on it, so both directories stay out of the
        # all-languages base discovery.
        "tagged_enum_empty_list",
        "tagged_enum_empty_map",
        # ``dhall_nested_map_widening`` is the Dhall counterpart of
        # ``nested_map_widening`` (issue #2897).  Dhall renders dicts as
        # records typed by their field set, so it needs a dedicated input
        # whose sibling inner maps share one key set while diverging their
        # scalar value types; the ``UNION_TYPE`` strategy then wraps every
        # sibling map's leaves in ``Value`` so the list type-checks.  The
        # Dhall ``dhall_nested_map_widening`` variants are the sole
        # consumers, so it stays out of the all-languages base discovery.
        "dhall_nested_map_widening",
        # A string mixing an embedded quote, a control character, and a
        # multi-byte character exercises string escaping for every JSON value
        # back end.  It stays variant-only because the ``json_type`` axis is
        # its sole consumer.
        "json_string_escaping",
        # ``string_embedded_nul`` carries a bare embedded null byte and a
        # null byte immediately followed by a digit, to pin the escape
        # each language emits (and its distinctness before a following
        # digit) for the languages whose ``variant_metadata`` sets
        # ``string_literals_escape_null_byte`` (issue #3006), plus COBOL's
        # ``json_type=CJSON`` byte-splicing build.  Languages that reject
        # the value, emit a raw null byte, or emit a digit-greedy escape
        # do not participate, so only the ``string_embedded_nul`` axis
        # consumes it and it stays out of the all-languages base discovery.
        "string_embedded_nul",
    }
)


KEBAB_NEW_VARIABLE_CASE_DIR = "new_variable_kebab_name"
"""Golden case that verifies a hyphenated ``NewVariable`` binding."""

PRIMED_NEW_VARIABLE_CASE_DIR = "new_variable_prime_suffix"
"""Golden case that verifies a primed ``NewVariable`` binding."""


@beartype
def kebab_new_variable_languages() -> tuple[literalizer.LanguageCls, ...]:
    """Return languages whose declaration syntax admits hyphens."""
    return tuple(
        lang_cls
        for lang_cls in sorted_languages()
        if lang_cls.new_variable_name_syntax
        is NewVariableNameSyntax.ASCII_KEBAB
    )


@beartype
def primed_new_variable_languages() -> tuple[literalizer.LanguageCls, ...]:
    """Return languages whose declaration syntax admits prime suffixes."""
    return tuple(
        lang_cls
        for lang_cls in sorted_languages()
        if lang_cls.new_variable_name_syntax
        is NewVariableNameSyntax.LOWER_ASCII_PRIME_SUFFIX
    )


@functools.cache
@beartype
def _specialized_case_dirs() -> frozenset[str]:
    """Case directories a specialized test owns, so they are excluded
    from the all-languages base / combined / language-version
    discovery: the call, ``$ref`` and default-``$ref`` case
    directories plus :data:`VARIANT_ONLY_CASE_DIRS`.
    """
    return (
        frozenset(cfg.case_dir_name for cfg in CALL_CASE_CONFIGS)
        | frozenset(cfg.case_dir_name for cfg in LITERALIZE_REF_CASE_CONFIGS)
        | frozenset(
            cfg.case_dir_name for cfg in LITERALIZE_DEFAULT_REF_CASE_CONFIGS
        )
        | frozenset(
            (KEBAB_NEW_VARIABLE_CASE_DIR, PRIMED_NEW_VARIABLE_CASE_DIR),
        )
        | VARIANT_ONLY_CASE_DIRS
    )


@dataclasses.dataclass(frozen=True)
class LiteralizeRefCaseConfig:
    """Configuration for a ``literalize`` ``$ref`` golden-file test
    case.

    When *ref_value_sources* is supplied, each entry maps a
    ``{ref_key: name}`` marker in ``input.yaml`` to a JSON source whose
    value seeds ``ref_values`` on the :func:`literalize` call and the
    matching ref stub.  Without it the harness keeps its historical
    behavior: refs render with no value-type knowledge and stubs are
    dict shaped.

    When *ref_case_override* is set, the case forces that identifier
    case for the ``ref_case`` argument of :func:`literalize` instead of
    using the language's default (``identifier_cases[0]``).  Discovery
    skips any language whose ``supported_ref_cases`` does not include
    the override.
    """

    case_dir_name: str
    ref_key: str
    ref_value_sources: tuple[tuple[str, str], ...]
    ref_case_override: literalizer.IdentifierCase | None


LITERALIZE_REF_CASE_CONFIGS: list[LiteralizeRefCaseConfig] = [
    LiteralizeRefCaseConfig(
        case_dir_name="literalize_ref_whole",
        ref_key="$ref",
        ref_value_sources=(),
        ref_case_override=None,
    ),
    LiteralizeRefCaseConfig(
        case_dir_name="literalize_ref_in_dict",
        ref_key="$ref",
        ref_value_sources=(),
        ref_case_override=None,
    ),
    LiteralizeRefCaseConfig(
        case_dir_name="literalize_ref_in_list",
        ref_key="$ref",
        ref_value_sources=(),
        ref_case_override=None,
    ),
    LiteralizeRefCaseConfig(
        case_dir_name="literalize_ref_heterogeneous",
        ref_key="$ref",
        ref_value_sources=(),
        ref_case_override=None,
    ),
    LiteralizeRefCaseConfig(
        case_dir_name="literalize_ref_in_mixed_list",
        ref_key="$ref",
        ref_value_sources=(),
        ref_case_override=None,
    ),
    LiteralizeRefCaseConfig(
        case_dir_name="literalize_ref_camel_name",
        ref_key="$ref",
        ref_value_sources=(),
        ref_case_override=None,
    ),
    LiteralizeRefCaseConfig(
        case_dir_name="literalize_ref_forced_camel_name",
        ref_key="$ref",
        ref_value_sources=(),
        ref_case_override=literalizer.IdentifierCase.CAMEL,
    ),
    LiteralizeRefCaseConfig(
        case_dir_name="literalize_ref_deep_nesting",
        ref_key="$ref",
        ref_value_sources=(),
        ref_case_override=None,
    ),
    LiteralizeRefCaseConfig(
        case_dir_name="literalize_ref_scalar",
        ref_key="$ref",
        ref_value_sources=(("my_int", "42"),),
        ref_case_override=None,
    ),
    LiteralizeRefCaseConfig(
        case_dir_name="literalize_ref_kebab_name",
        ref_key="$ref",
        ref_value_sources=(),
        ref_case_override=literalizer.IdentifierCase.KEBAB,
    ),
    LiteralizeRefCaseConfig(
        case_dir_name="literalize_ref_json_escaped_key",
        ref_key="$ref",
        ref_value_sources=(),
        ref_case_override=None,
    ),
    LiteralizeRefCaseConfig(
        case_dir_name="literalize_ref_toml_table",
        ref_key="$ref",
        ref_value_sources=(),
        ref_case_override=None,
    ),
    LiteralizeRefCaseConfig(
        case_dir_name="literalize_ref_json5_unquoted_key",
        ref_key="$ref",
        ref_value_sources=(),
        ref_case_override=None,
    ),
]

LITERALIZE_DEFAULT_REF_CASE_CONFIGS: list[LiteralizeRefCaseConfig] = [
    LiteralizeRefCaseConfig(
        case_dir_name="literalize_ref_default_nested",
        ref_key="$ref",
        ref_value_sources=(),
        ref_case_override=None,
    ),
    LiteralizeRefCaseConfig(
        case_dir_name="literalize_ref_default_whole",
        ref_key="$ref",
        ref_value_sources=(),
        ref_case_override=None,
    ),
]


@dataclasses.dataclass(frozen=True, kw_only=True)
class _CaseInput:
    """The input file backing a golden-file case."""

    path: Path
    input_format: literalizer.InputFormat


@beartype
def case_input(*, case_dir: Path) -> _CaseInput:
    """Return the input file path and its :class:`InputFormat` for a case.

    Cases use ``input.yaml`` by default.  Cases whose behavior depends on
    format-specific parsing (e.g. JSON unicode escapes) or whose input
    contains a value the YAML 1.2 spec cannot natively express (currently
    ``datetime.time``) use ``input.json``, ``input.json5``, or
    ``input.toml`` instead.  A case must carry exactly one input file:
    ``test_no_dead_golden_files`` flags a case that carries more than one
    because the unused file becomes orphaned.
    """
    json_path = case_dir / "input.json"
    if json_path.exists():
        return _CaseInput(
            path=json_path,
            input_format=literalizer.InputFormat.JSON,
        )
    json5_path = case_dir / "input.json5"
    if json5_path.exists():
        return _CaseInput(
            path=json5_path,
            input_format=literalizer.InputFormat.JSON5,
        )
    toml_path = case_dir / "input.toml"
    if toml_path.exists():
        return _CaseInput(
            path=toml_path,
            input_format=literalizer.InputFormat.TOML,
        )
    return _CaseInput(
        path=case_dir / "input.yaml",
        input_format=literalizer.InputFormat.YAML,
    )


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
    | None
    | datetime.date
    | datetime.datetime
    | datetime.time
    | bytes
)
# Parsed case data.  ``load_case_data`` parses YAML with the ``safe``
# loader (and JSON/JSON5/TOML natively), so containers are plain
# ``dict``/``list``/``set`` rather than the ruamel comment-tracking
# subclasses; a precise model keeps ``@beartype`` accurate and strict
# pyright/ty fully resolved.
type CaseData = (
    _CaseScalar
    | list[CaseData]
    | dict[object, CaseData]
    | set[_CaseScalar]
    | frozenset[_CaseScalar]
)


@beartype
def load_case_data(*, input_info: _CaseInput) -> CaseData:
    """Parse a case input file according to its declared format.

    Dispatches on :attr:`_CaseInput.input_format` so discovery code can
    inspect any case's data without knowing which serialization backs
    it.  ``tomllib``/``json``/``pyjson5`` yield plain containers and
    ``ruamel`` yields its comment-tracking mappings; both are walked
    structurally by the ``has_*`` predicates.
    """
    source = input_info.path.read_text(encoding="utf-8")
    parsed: CaseData
    match input_info.input_format:
        case literalizer.InputFormat.JSON:
            parsed = json.loads(s=source)
        case literalizer.InputFormat.JSON5:
            parsed = pyjson5.decode(data=source)  # pylint: disable=no-member
        case literalizer.InputFormat.YAML:
            # ``safe`` (not round-trip): yields plain ``dict``/``list``/
            # ``set`` instead of the ruamel comment-tracking subclasses,
            # so the result matches ``CaseData`` exactly.  Comments are
            # irrelevant to the key/float predicates.
            parsed = YAML(typ="safe").load(  # pyright: ignore[reportUnknownMemberType]
                stream=source,
            )
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
    """Return ``True`` if *data* contains a dict key that is empty or
    has characters outside printable ASCII.
    """
    match data:
        case dict():
            for key in data:
                if isinstance(key, str) and (
                    not key or not key.isprintable() or not key.isascii()
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


@functools.cache
@beartype
def cases_with_non_trivial_dict_keys(
    cases_dir: Path,
) -> frozenset[str]:
    """Return case directory names whose input has dict keys that some
    languages cannot represent (empty or non-printable-ASCII).

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


def has_non_ascii_strings(data: CaseData) -> bool:
    """Return ``True`` if *data* contains a string with a non-ASCII
    character.
    """
    match data:
        case str():
            return not data.isascii()
        case dict():
            return any(
                (isinstance(k, str) and not k.isascii())
                or has_non_ascii_strings(data=v)
                for k, v in data.items()
            )
        case list():
            return any(has_non_ascii_strings(data=item) for item in data)
        case set() | frozenset():
            return any(has_non_ascii_strings(data=item) for item in data)
        case _:
            return False


@functools.cache
@beartype
def cases_with_non_ascii_strings(
    cases_dir: Path,
) -> frozenset[str]:
    """Return case directory names whose input contains a non-ASCII
    string value that some languages cannot represent in a portable
    string literal.
    """
    result: set[str] = set()
    for case_dir in cases_dir.iterdir():
        input_info = case_input(case_dir=case_dir)
        loaded = load_case_data(input_info=input_info)
        if has_non_ascii_strings(data=loaded):
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
    specialized_case_dirs = _specialized_case_dirs()
    non_trivial_key_cases = cases_with_non_trivial_dict_keys(
        cases_dir=cases_dir,
    )
    special_float_cases = cases_with_special_floats(cases_dir=cases_dir)
    non_ascii_string_cases = cases_with_non_ascii_strings(cases_dir=cases_dir)
    cases: list[tuple[str, literalizer.LanguageCls]] = []
    for case_dir in sorted(cases_dir.iterdir()):
        if case_dir.name in specialized_case_dirs:
            continue
        non_trivial = case_dir.name in non_trivial_key_cases
        special_float = case_dir.name in special_float_cases
        non_ascii_string = case_dir.name in non_ascii_string_cases
        for lang_cls in sorted_languages():
            if non_trivial and _lang_raises_for_non_printable_ascii_dict_keys(
                lang_cls=lang_cls
            ):
                continue
            if special_float and not lang_cls.supports_special_floats:
                continue
            if (
                non_ascii_string
                and not lang_cls.supports_non_ascii_string_literals
            ):
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
    specialized_case_dirs = _specialized_case_dirs()
    non_trivial_key_cases = cases_with_non_trivial_dict_keys(
        cases_dir=cases_dir,
    )
    special_float_cases = cases_with_special_floats(cases_dir=cases_dir)
    non_ascii_string_cases = cases_with_non_ascii_strings(cases_dir=cases_dir)
    cases: list[CombinedCase] = []
    for case_dir in sorted(cases_dir.iterdir()):
        if case_dir.name in specialized_case_dirs:
            continue
        non_trivial = case_dir.name in non_trivial_key_cases
        special_float = case_dir.name in special_float_cases
        non_ascii_string = case_dir.name in non_ascii_string_cases
        for lang_cls in sorted_languages():
            lang_name = lang_cls.__name__
            if non_trivial and _lang_raises_for_non_printable_ascii_dict_keys(
                lang_cls=lang_cls
            ):
                continue
            if special_float and not lang_cls.supports_special_floats:
                continue
            if (
                non_ascii_string
                and not lang_cls.supports_non_ascii_string_literals
            ):
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
    # Most strategies exercise the mixed-scalar dict; the TUPLE strategy
    # needs an input that actually carries a tuple-eligible
    # heterogeneous scalar array, so it is paired with the canonical
    # record-field fixture (which also exercises RECORD/TUPLE
    # composition) instead.
    default_case_dir_name = "dict_mixed_scalars"
    strategy_case_dir_names = {"TUPLE": "tuple_record_field"}
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
            case_dir_name = strategy_case_dir_names.get(
                strategy.name,
                default_case_dir_name,
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

    ``simple_dict`` exercises a multi-line container value at indent
    across every language with class-field modifiers.  Languages may
    additionally opt into a focused ``comment_scalar_before_and_inline``
    case through their variant metadata.  It exercises a scalar whose
    formatted value is preceded by comment lines carrying the same
    ``line_prefix`` indent.
    """
    cases: list[PreIndentCase] = []
    for lang_cls in sorted_languages():
        cases.extend(
            PreIndentCase(
                name=f"{lang_cls.__name__}_pre_indent_1_{combo.name}",
                lang_cls=lang_cls,
                case_dir_name="simple_dict",
                pre_indent_level=1,
                modifiers=combo.modifiers,
            )
            for combo in lang_cls.modifier_combinations
        )
    for lang_cls in sorted_languages():
        if not lang_cls.variant_metadata.pre_indent_comment_scalar_variant:
            continue
        cases.extend(
            PreIndentCase(
                name=(
                    f"{lang_cls.__name__}_pre_indent_1_{combo.name}"
                    "_comment_scalar_before_and_inline"
                ),
                lang_cls=lang_cls,
                case_dir_name="comment_scalar_before_and_inline",
                pre_indent_level=1,
                modifiers=combo.modifiers,
            )
            for combo in lang_cls.modifier_combinations
        )
    return cases
