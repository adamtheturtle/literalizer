"""Build format-variant golden-file cases.

Each :class:`Variant` pairs a language class with a specific
non-default formatter spec; each :class:`VariantCase` pairs a variant
with one of the input case directories under ``tests/integration/cases``.
"""

import dataclasses
import enum
import functools
from collections.abc import Callable, Iterable
from pathlib import Path

from beartype import beartype

import literalizer
from literalizer.languages import (
    C,
    Cobol,
    Crystal,
    CSharp,
    Dart,
    Dhall,
    Elm,
    Fortran,
    FSharp,
    Gleam,
    Go,
    Haskell,
    Kotlin,
    Mojo,
    Nim,
    OCaml,
    Odin,
    PureScript,
    Python,
    Roc,
    Rust,
    Swift,
    VisualBasic,
)

from .case_discovery import cases_with_special_floats, discover_cases
from .language_specs import make_spec, sorted_languages

_CASES_DIR = Path(__file__).parent / "cases"


@beartype
def _wrap_variable_name(lang_cls: literalizer.LanguageCls) -> str | None:
    """Return the wrap variable name for a language class."""
    return "my_data" if lang_cls.supports_variable_names else None


@beartype
def wrap_variable_form(
    lang_cls: literalizer.LanguageCls,
) -> literalizer.NewVariable | None:
    """Return a :class:`NewVariable` form for a language class, or
    None.
    """
    name = _wrap_variable_name(lang_cls=lang_cls)
    if name is None:
        return None
    return literalizer.NewVariable(name=name)


# ---------------------------------------------------------------------------
# Test-only data keyed by language class.
#
# Keeping the language-specific test values here — keyed by the language
# class itself, not by ``__name__`` — lets the parameterized variant
# builders below iterate uniformly over ``ALL_LANGUAGES`` without any
# ``if lang_cls.__name__ == "..."`` branches.  Genuine language facts
# live on the language class; only arbitrary test fixtures (alternative
# type names, fictional constructor prefixes, chosen field names, etc.)
# belong in this block.
# ---------------------------------------------------------------------------

# Alternative type names passed to the various ``default_*_type`` kwargs.
# Each value must differ from the language's own default *and* be a valid
# type name for that language's linter / compiler.  ``"String"`` is used
# as the fallback for any supported language not listed explicitly.
DEFAULT_TYPE_OVERRIDE_FALLBACK = "String"

DEFAULT_SET_ELEMENT_TYPE_OVERRIDES: dict[literalizer.LanguageCls, str] = {
    Crystal: "Int32",
    Go: "string",
    CSharp: "string",
    Mojo: "Int",
    Odin: "int",
    Python: "int",
    Rust: "i32",
}

DEFAULT_SEQUENCE_ELEMENT_TYPE_OVERRIDES: dict[literalizer.LanguageCls, str] = {
    Go: "interface{}",
    CSharp: "string",
    Mojo: "Int",
    Python: "int",
}

DEFAULT_DICT_VALUE_TYPE_OVERRIDES: dict[literalizer.LanguageCls, str] = {
    Crystal: "Int32",
    Go: "interface{}",
    CSharp: "object?",
    Dart: "Object?",
    Kotlin: "Comparable<*>?",
    Mojo: "Int",
    Python: "int",
    Rust: "i32",
}

DEFAULT_DICT_KEY_TYPE_OVERRIDES: dict[literalizer.LanguageCls, str] = {
    Crystal: "Int32",
    Go: "any",
    CSharp: "object",
    Dart: "Object",
    Kotlin: "Any",
    Python: "int",
    Rust: "&str",
    Swift: "AnyHashable",
    VisualBasic: "Object",
}


@beartype
def _enum_member_by_name(
    *,
    enum_cls: type[enum.Enum],
    name: str,
) -> enum.Enum:
    """Return the enum member in *enum_cls* whose ``.name`` matches."""
    for member in enum_cls:
        if member.name == name:
            return member
    msg = f"{enum_cls.__name__} has no member named {name!r}"
    raise ValueError(msg)


DEFAULT_ORDERED_MAP_VALUE_TYPE_OVERRIDES: dict[
    literalizer.LanguageCls, str
] = {Go: "interface{}"}

# Languages that expose ``type_name`` / ``constructor_prefix`` kwargs for
# the ADT they emit; the value is the test override to apply.
TYPE_NAME_OVERRIDES: dict[literalizer.LanguageCls, str] = {
    Elm: "JsonVal",
    FSharp: "JsonVal",
    Gleam: "JsonVal",
    Haskell: "JsonVal",
    OCaml: "json_t",
    PureScript: "JsonVal",
    Roc: "JsonVal",
}

CONSTRUCTOR_PREFIX_OVERRIDES: dict[literalizer.LanguageCls, str] = {
    Elm: "J",
    FSharp: "J",
    Gleam: "J",
    Haskell: "J",
    OCaml: "J",
    PureScript: "J",
    Roc: "J",
}

# Languages whose heterogeneous-value enum name is configurable (Rust's
# ``TAGGED_ENUM`` strategy); the value is the test override to apply.
HETEROGENEOUS_VALUE_ENUM_NAME_OVERRIDES: dict[literalizer.LanguageCls, str] = {
    Rust: "JsonValue"
}

# Languages whose heterogeneous-value union name is configurable
# (Dhall's ``UNION_TYPE`` strategy); the value is the test override
# to apply.
HETEROGENEOUS_VALUE_UNION_NAME_OVERRIDES: dict[
    literalizer.LanguageCls, str
] = {Dhall: "JsonValue"}

# Languages whose heterogeneous-value variant name is configurable
# (the Nim ``OBJECT_VARIANT`` strategy and the Mojo ``VARIANT``
# strategy); the value is the test override to apply.
HETEROGENEOUS_VALUE_VARIANT_NAME_OVERRIDES: dict[
    literalizer.LanguageCls, str
] = {Nim: "JsonValue", Mojo: "JsonValue"}

# Languages that accept constructor-name kwargs (Fortran) or field-name
# kwargs (C); the inner dict is the kwargs to pass to the constructor.
CONSTRUCTOR_NAME_OVERRIDES: dict[literalizer.LanguageCls, dict[str, str]] = {
    Fortran: {
        "null_name": "jnull",
        "bool_name": "jbool",
        "int_name": "jint",
        "real_name": "jreal",
        "str_name": "jstr",
        "list_name": "jlist",
        "map_name": "jmap",
        "set_name": "jset",
        "entry_name": "jentry",
    },
}

FIELD_NAME_OVERRIDES: dict[literalizer.LanguageCls, dict[str, str]] = {
    C: {
        "bool_field": "bl",
        "int_field": "integer",
        "uint_field": "uinteger",
        "float_field": "fp",
        "string_field": "str",
        "array_field": "arr",
        "map_field": "dict",
        "key_field": "key",
        "value_field": "val",
    },
}

# Declaration-style → alternative-sequence-format overrides, by enum name.
# Rust CONST and STATIC raise ``IncompatibleFormatsError`` with the default
# ``Vec`` sequence format, so the test falls back to ``Array``.
DECLARATION_STYLE_SEQUENCE_FORMAT_OVERRIDES: dict[
    literalizer.LanguageCls, dict[str, str]
] = {Rust: {"CONST": "ARRAY", "STATIC": "ARRAY"}}


@dataclasses.dataclass(frozen=True)
class Variant:
    """A formatting variant for a language (date, sequence, set, etc.)."""

    name: str
    spec: literalizer.Language
    lang_cls: literalizer.LanguageCls
    collection_layout: literalizer.CollectionLayout = (
        literalizer.CollectionLayout.COMPACT
    )


@dataclasses.dataclass(frozen=True)
class VariantCase:
    """A format-variant golden-file test case."""

    variant_name: str
    variant: Variant
    case_dir_name: str
    variable_form: literalizer.NewVariable | None


@beartype
def build_non_default_variants(
    *,
    category: str,
    get_default: Callable[[literalizer.Language], object],
    get_formats: Callable[[literalizer.Language], type[enum.Enum]],
    make_variant_spec: Callable[
        [literalizer.LanguageCls, enum.Enum],
        literalizer.Language,
    ],
) -> list[Variant]:
    """Build variants for every non-default value of a format enum.

    This is the generic version of the many per-format builder functions
    that all follow the same pattern: iterate all languages, find the
    non-default members of a format enum, and create a ``Variant`` for
    each one.
    """
    variants: list[Variant] = []
    for lang_cls in sorted_languages():
        lang_name = lang_cls.__name__
        spec = make_spec(lang_cls=lang_cls)
        default_format = get_default(spec)
        for fmt in get_formats(spec):
            if fmt is default_format:
                continue
            variants.append(
                Variant(
                    name=f"{lang_name}_{category}_{fmt.name.lower()}",
                    spec=make_variant_spec(lang_cls, fmt),
                    lang_cls=lang_cls,
                )
            )
    return variants


@beartype
def build_default_set_element_type_variants() -> Iterable[Variant]:
    """Build default-set-type variants for languages that support it."""
    variants: list[Variant] = []
    for lang_cls in sorted_languages():
        if not lang_cls.supports_default_set_element_type:
            continue
        type_name = DEFAULT_SET_ELEMENT_TYPE_OVERRIDES.get(
            lang_cls,
            DEFAULT_TYPE_OVERRIDE_FALLBACK,
        )
        variants.append(
            Variant(
                name=f"{lang_cls.__name__}_default_set_element_type_string",
                spec=make_spec(
                    lang_cls=lang_cls, default_set_element_type=type_name
                ),
                lang_cls=lang_cls,
            )
        )
    return variants


@beartype
def build_default_sequence_element_type_variants() -> Iterable[Variant]:
    """Build default-sequence-type variants for languages that support
    it.
    """
    variants: list[Variant] = []
    for lang_cls in sorted_languages():
        if not lang_cls.supports_default_sequence_element_type:
            continue
        type_name = DEFAULT_SEQUENCE_ELEMENT_TYPE_OVERRIDES.get(
            lang_cls,
            DEFAULT_TYPE_OVERRIDE_FALLBACK,
        )
        variants.append(
            Variant(
                name=(
                    f"{lang_cls.__name__}_default_sequence_element_type_string"
                ),
                spec=make_spec(
                    lang_cls=lang_cls, default_sequence_element_type=type_name
                ),
                lang_cls=lang_cls,
            )
        )
    return variants


@beartype
def build_default_dict_value_type_variants() -> Iterable[Variant]:
    """Build default-dict-value-type variants for languages that support
    it.
    """
    variants: list[Variant] = []
    for lang_cls in sorted_languages():
        if not lang_cls.supports_default_dict_value_type:
            continue
        type_name = DEFAULT_DICT_VALUE_TYPE_OVERRIDES.get(
            lang_cls,
            DEFAULT_TYPE_OVERRIDE_FALLBACK,
        )
        variants.append(
            Variant(
                name=f"{lang_cls.__name__}_default_dict_value_type_string",
                spec=make_spec(
                    lang_cls=lang_cls, default_dict_value_type=type_name
                ),
                lang_cls=lang_cls,
            )
        )
    return variants


@beartype
def build_default_dict_key_type_variants() -> Iterable[Variant]:
    """Build default-dict-key-type variants for languages that support
    it.
    """
    variants: list[Variant] = []
    for lang_cls in sorted_languages():
        if not lang_cls.supports_default_dict_key_type:
            continue
        type_name = DEFAULT_DICT_KEY_TYPE_OVERRIDES.get(
            lang_cls,
            DEFAULT_TYPE_OVERRIDE_FALLBACK,
        )
        variants.append(
            Variant(
                name=f"{lang_cls.__name__}_default_dict_key_type",
                spec=make_spec(
                    lang_cls=lang_cls, default_dict_key_type=type_name
                ),
                lang_cls=lang_cls,
            )
        )
    return variants


@beartype
def build_default_ordered_map_value_type_variants() -> Iterable[Variant]:
    """Build default-ordered-map-value-type variants for every language
    that supports the option.
    """
    variants: list[Variant] = []
    for lang_cls in sorted_languages():
        if not lang_cls.supports_default_ordered_map_value_type:
            continue
        type_name = DEFAULT_ORDERED_MAP_VALUE_TYPE_OVERRIDES.get(
            lang_cls,
            DEFAULT_TYPE_OVERRIDE_FALLBACK,
        )
        variants.append(
            Variant(
                name=f"{lang_cls.__name__}_default_ordered_map_value_type",
                spec=make_spec(
                    lang_cls=lang_cls, default_ordered_map_value_type=type_name
                ),
                lang_cls=lang_cls,
            )
        )
    return variants


@beartype
def build_statement_terminator_style_decl_variants() -> Iterable[Variant]:
    """Build statement-terminator + declaration-style cross-option
    variants.

    For each language with multiple statement terminators *and* multiple
    declaration styles, create a variant for every non-default
    statement terminator paired with every non-default declaration style.
    """
    variants: list[Variant] = []
    for lang_cls in sorted_languages():
        lang_name = lang_cls.__name__
        spec = make_spec(lang_cls=lang_cls)
        default_statement_terminator_style = spec.statement_terminator_style
        default_declaration_style = spec.declaration_style
        non_default_statement_terminator_styles = [
            statement_terminator_style
            for statement_terminator_style in spec.statement_terminator_styles
            if statement_terminator_style
            is not default_statement_terminator_style
        ]
        non_default_declaration_styles = [
            declaration_style
            for declaration_style in spec.declaration_styles
            if declaration_style is not default_declaration_style
        ]
        variants.extend(
            Variant(
                name=(
                    f"{lang_name}_statement_terminator_style_{statement_terminator_style.name.lower()}"
                    f"_decl_{declaration_style.name.lower()}"
                ),
                spec=make_spec(
                    lang_cls=lang_cls,
                    statement_terminator_style=statement_terminator_style,
                    declaration_style=declaration_style,
                ),
                lang_cls=lang_cls,
            )
            for statement_terminator_style in (
                non_default_statement_terminator_styles
            )
            for declaration_style in non_default_declaration_styles
        )
    return variants


@beartype
def build_collection_layout_variants() -> Iterable[Variant]:
    """Build variants for every collection-layout option."""
    variants: list[Variant] = []
    for lang_cls in sorted_languages():
        name_prefix = (
            f"{lang_cls.__name__}_layout"
            if lang_cls is Cobol
            else f"{lang_cls.__name__}_collection_layout"
        )
        variants.extend(
            Variant(
                name=f"{name_prefix}_{layout.value}",
                spec=make_spec(lang_cls=lang_cls),
                lang_cls=lang_cls,
                collection_layout=layout,
            )
            for layout in literalizer.CollectionLayout
        )
    return variants


@beartype
def build_sequence_decl_variants() -> Iterable[Variant]:
    """Build sequence format + declaration style cross-option variants.

    For each language with multiple sequence formats *and* multiple
    declaration styles, create a variant for every non-default
    sequence format paired with every non-default declaration style.
    """
    variants: list[Variant] = []
    for lang_cls in sorted_languages():
        lang_name = lang_cls.__name__
        spec = make_spec(lang_cls=lang_cls)
        default_sequence_format = spec.sequence_format
        default_declaration_style = spec.declaration_style
        non_default_sequence_formats = [
            sequence_format
            for sequence_format in spec.sequence_formats
            if sequence_format is not default_sequence_format
        ]
        non_default_declaration_styles = [
            declaration_style
            for declaration_style in spec.declaration_styles
            if declaration_style is not default_declaration_style
        ]
        variants.extend(
            Variant(
                name=(
                    f"{lang_name}_sequence_{sequence_format.name.lower()}"
                    f"_decl_{declaration_style.name.lower()}"
                ),
                spec=make_spec(
                    lang_cls=lang_cls,
                    sequence_format=sequence_format,
                    declaration_style=declaration_style,
                ),
                lang_cls=lang_cls,
            )
            for sequence_format in non_default_sequence_formats
            for declaration_style in non_default_declaration_styles
        )
    return variants


@beartype
def build_constructor_name_variants() -> Iterable[Variant]:
    """Build constructor-name variants for languages listed in
    :data:`CONSTRUCTOR_NAME_OVERRIDES` (e.g. Fortran).
    """
    variants: list[Variant] = []
    for lang_cls in sorted_languages():
        kwargs = CONSTRUCTOR_NAME_OVERRIDES.get(lang_cls)
        if kwargs is None:
            continue
        variants.append(
            Variant(
                name=f"{lang_cls.__name__}_constructor_names_j",
                spec=make_spec(lang_cls=lang_cls, **kwargs),
                lang_cls=lang_cls,
            )
        )
    return variants


@beartype
def build_type_name_variants() -> Iterable[Variant]:
    """Build type-name variants for languages that generate a named type.

    These languages emit a custom algebraic data type in their body
    preamble (e.g. ``data Val = …`` in Haskell).  The ``type_name``
    constructor parameter lets users customize that name.
    """
    variants: list[Variant] = []
    for lang_cls in sorted_languages():
        custom_name = TYPE_NAME_OVERRIDES.get(lang_cls)
        if custom_name is None:
            continue
        variants.append(
            Variant(
                name=f"{lang_cls.__name__}_type_name_{custom_name}",
                spec=make_spec(lang_cls=lang_cls, type_name=custom_name),
                lang_cls=lang_cls,
            )
        )
    return variants


@beartype
def build_constructor_prefix_variants() -> Iterable[Variant]:
    """Build constructor-prefix variants for languages with custom
    ADTs.
    """
    variants: list[Variant] = []
    for lang_cls in sorted_languages():
        custom_prefix = CONSTRUCTOR_PREFIX_OVERRIDES.get(lang_cls)
        if custom_prefix is None:
            continue
        variants.append(
            Variant(
                name=f"{lang_cls.__name__}_prefix_{custom_prefix}",
                spec=make_spec(
                    lang_cls=lang_cls, constructor_prefix=custom_prefix
                ),
                lang_cls=lang_cls,
            )
        )
    return variants


@beartype
def build_heterogeneous_value_name_variants() -> Iterable[Variant]:
    """Build heterogeneous-value-enum-name variants for languages that
    generate a named type for their heterogeneous strategy (e.g. Rust's
    ``TAGGED_ENUM``).  The ``heterogeneous_value_enum_name`` constructor
    parameter lets users customize that name.
    """
    variants: list[Variant] = []
    for lang_cls in sorted_languages():
        custom_name = HETEROGENEOUS_VALUE_ENUM_NAME_OVERRIDES.get(lang_cls)
        if custom_name is None:
            continue
        default_spec = make_spec(lang_cls=lang_cls)
        tagged_enum = next(
            strategy
            for strategy in default_spec.heterogeneous_strategies
            if strategy.name == "TAGGED_ENUM"
        )
        spec = make_spec(
            lang_cls=lang_cls,
            heterogeneous_strategy=tagged_enum,
            heterogeneous_value_enum_name=custom_name,
        )
        variants.append(
            Variant(
                name=(
                    f"{lang_cls.__name__}"
                    f"_heterogeneous_value_enum_name_{custom_name}"
                ),
                spec=spec,
                lang_cls=lang_cls,
            )
        )
    return variants


@beartype
def build_c_field_name_variants() -> Iterable[Variant]:
    """Build field-name variants for languages listed in
    :data:`FIELD_NAME_OVERRIDES` (e.g. C).
    """
    variants: list[Variant] = []
    for lang_cls in sorted_languages():
        kwargs = FIELD_NAME_OVERRIDES.get(lang_cls)
        if kwargs is None:
            continue
        variants.append(
            Variant(
                name=f"{lang_cls.__name__}_field_names_custom",
                spec=make_spec(lang_cls=lang_cls, **kwargs),
                lang_cls=lang_cls,
            )
        )
    return variants


@beartype
def build_language_version_variants() -> Iterable[Variant]:
    """Build version variants for all languages with multiple versions.

    Any language whose ``VersionFormats`` enum has more than one member is
    included automatically; no per-language registration is needed here.
    """
    variants: list[Variant] = []
    for lang_cls in sorted_languages():
        versions_cls = lang_cls.version_formats
        if len(versions_cls) <= 1:
            continue
        spec = make_spec(lang_cls=lang_cls)
        default_version: enum.Enum = spec.language_version
        for version in versions_cls:
            if version is default_version:
                continue
            variants.append(
                Variant(
                    name=f"{lang_cls.__name__}_version_{version.name.lower()}",
                    spec=make_spec(
                        lang_cls=lang_cls, language_version=version
                    ),
                    lang_cls=lang_cls,
                )
            )
    return variants


@beartype
def build_language_version_cross_dict_type_variants() -> Iterable[Variant]:
    """Build cross-product variants: PY38 x non-Any dict value type.

    Exercises the False branch of the ``_any_types`` intersection check
    in the PY38 type-hint preamble builder, where the dict value type is
    not ``Any`` so ``from typing import Any`` is not emitted.
    """
    return [
        Variant(
            name="Python_version_py38_default_dict_value_type_int",
            spec=make_spec(
                lang_cls=Python,
                language_version=_enum_member_by_name(
                    enum_cls=Python.version_formats,
                    name="PY38",
                ),
                default_dict_value_type=DEFAULT_DICT_VALUE_TYPE_OVERRIDES[
                    Python
                ],
            ),
            lang_cls=Python,
        )
    ]


@beartype
def build_heterogeneous_value_union_name_variants() -> Iterable[Variant]:
    """Build heterogeneous-value-union-name variants for languages that
    generate a named union type for their heterogeneous strategy (e.g.
    Dhall's ``UNION_TYPE``).  The ``heterogeneous_value_union_name``
    constructor parameter lets users customize that name.
    """
    variants: list[Variant] = []
    for lang_cls in sorted_languages():
        custom_name = HETEROGENEOUS_VALUE_UNION_NAME_OVERRIDES.get(lang_cls)
        if custom_name is None:
            continue
        default_spec = make_spec(lang_cls=lang_cls)
        union_type = next(
            strategy
            for strategy in default_spec.heterogeneous_strategies
            if strategy.name == "UNION_TYPE"
        )
        spec = make_spec(
            lang_cls=lang_cls,
            heterogeneous_strategy=union_type,
            heterogeneous_value_union_name=custom_name,
        )
        variants.append(
            Variant(
                name=(
                    f"{lang_cls.__name__}"
                    f"_heterogeneous_value_union_name_{custom_name}"
                ),
                spec=spec,
                lang_cls=lang_cls,
            )
        )
    return variants


@beartype
def build_heterogeneous_value_variant_name_variants() -> Iterable[Variant]:
    """Build heterogeneous-value-variant-name variants for languages
    that generate a named variant type for their heterogeneous strategy
    (the Nim ``OBJECT_VARIANT`` and Mojo ``VARIANT``).  The
    ``heterogeneous_value_variant_name`` constructor parameter lets
    users customize that name.
    """
    wrapping_strategy_names = {"OBJECT_VARIANT", "VARIANT"}
    variants: list[Variant] = []
    for lang_cls in sorted_languages():
        custom_name = HETEROGENEOUS_VALUE_VARIANT_NAME_OVERRIDES.get(lang_cls)
        if custom_name is None:
            continue
        default_spec = make_spec(lang_cls=lang_cls)
        wrapping_strategy = next(
            strategy
            for strategy in default_spec.heterogeneous_strategies
            if strategy.name in wrapping_strategy_names
        )
        spec = make_spec(
            lang_cls=lang_cls,
            heterogeneous_strategy=wrapping_strategy,
            heterogeneous_value_variant_name=custom_name,
        )
        variants.append(
            Variant(
                name=(
                    f"{lang_cls.__name__}"
                    f"_heterogeneous_value_variant_name_{custom_name}"
                ),
                spec=spec,
                lang_cls=lang_cls,
            )
        )
    return variants


@beartype
def build_string_format_cross_variants(
    *,
    other_kwarg: str,
    other_tag: str,
    get_other_default: Callable[[literalizer.Language], object],
    get_other_formats: Callable[[literalizer.Language], type[enum.Enum]],
) -> list[Variant]:
    """Build cross-product variants of ``string_format`` and another axis.

    For every language, pair every non-default ``string_format`` with
    every non-default value of the other axis.  Covers code paths where
    the chosen ``string_format`` interacts with another formatter axis
    (e.g. the plain-ISO date/datetime fallback that only fires when both
    ``string_format`` and the date/datetime format are non-default).
    """
    variants: list[Variant] = []
    for lang_cls in sorted_languages():
        spec = make_spec(lang_cls=lang_cls)
        default_string = spec.string_format
        default_other = get_other_default(spec)
        lang_name = lang_cls.__name__
        for sf in spec.string_formats:
            if sf is default_string:
                continue
            for of in get_other_formats(spec):
                if of is default_other:
                    continue
                variants.append(
                    Variant(
                        name=(
                            f"{lang_name}"
                            f"_string_{sf.name.lower()}"
                            f"_{other_tag}_{of.name.lower()}"
                        ),
                        spec=make_spec(
                            lang_cls=lang_cls,
                            string_format=sf,
                            **{other_kwarg: of},
                        ),
                        lang_cls=lang_cls,
                    )
                )
    return variants


@beartype
def build_type_hints_cross_variants() -> list[Variant]:
    """Build cross-product variants: each non-default type-hint format
    combined with each non-default value of another format axis.

    These cover code paths where the type annotation depends on the
    chosen sequence / date / datetime / dict / set format.
    """
    axes: list[
        tuple[
            str,
            Callable[[literalizer.Language], object],
            Callable[[literalizer.Language], type[enum.Enum]],
            str,
        ]
    ] = [
        (
            "seq",
            lambda s: s.sequence_format,
            lambda s: s.sequence_formats,
            "sequence_format",
        ),
        (
            "date",
            lambda s: s.format_date,
            lambda s: s.date_formats,
            "date_format",
        ),
        (
            "dt",
            lambda s: s.format_datetime,
            lambda s: s.datetime_formats,
            "datetime_format",
        ),
        (
            "dict",
            lambda s: s.dict_format,
            lambda s: s.dict_formats,
            "dict_format",
        ),
        (
            "set",
            lambda s: s.set_format,
            lambda s: s.set_formats,
            "set_format",
        ),
        (
            "nls",
            lambda s: s.numeric_literal_suffix,
            lambda s: s.numeric_literal_suffixes,
            "numeric_literal_suffix",
        ),
    ]
    variants: list[Variant] = []
    for lang_cls in sorted_languages():
        spec = make_spec(lang_cls=lang_cls)
        default_th = spec.variable_type_hints
        lang_name = lang_cls.__name__
        for th_fmt in spec.variable_type_hints_formats:
            if th_fmt is default_th:
                continue
            th_tag = th_fmt.name.lower()
            for axis_name, get_default, get_formats, kwarg in axes:
                default = get_default(spec)
                for fmt in get_formats(spec):
                    if fmt is default:
                        continue
                    variants.append(
                        Variant(
                            name=(
                                f"{lang_name}"
                                f"_type_hints_{th_tag}"
                                f"_{axis_name}"
                                f"_{fmt.name.lower()}"
                            ),
                            spec=make_spec(
                                lang_cls=lang_cls,
                                variable_type_hints=th_fmt,
                                **{kwarg: fmt},
                            ),
                            lang_cls=lang_cls,
                        ),
                    )
    return variants


@beartype
def build_modifier_variant_cases() -> list[VariantCase]:
    """Build variants exercising per-language modifier rendering.

    For every language with a non-empty ``modifiers`` enum, emit one
    singleton-modifier variant per member plus one variant per entry
    in ``lang_cls.modifier_combinations``.  Each variant runs against
    inputs covering scalar / dict / set / date / datetime values so
    each branch of typed-declaration inference is exercised;
    combinations the language rejects at literalize time are skipped
    by the test itself.
    """
    cases: list[VariantCase] = []
    case_dirs = (
        "scalar_int",
        "simple_dict",
        "set",
        "empty_set",
        "scalar_date",
        "scalar_datetime",
    )
    for lang_cls in sorted_languages():
        spec = make_spec(lang_cls=lang_cls)
        if len(spec.modifiers) == 0:
            continue
        entries: list[tuple[str, frozenset[enum.Enum]]] = [
            (member.name.lower(), frozenset({member}))
            for member in spec.modifiers
        ]
        entries.extend(
            (combo.name, combo.modifiers)
            for combo in lang_cls.modifier_combinations
        )
        for mod_name, modifiers in entries:
            variant = Variant(
                name=f"{lang_cls.__name__}_modifiers_{mod_name}",
                spec=make_spec(lang_cls=lang_cls),
                lang_cls=lang_cls,
            )
            cases.extend(
                VariantCase(
                    variant_name=variant.name,
                    variant=variant,
                    case_dir_name=case_dir_name,
                    variable_form=literalizer.NewVariable(
                        name="my_data",
                        modifiers=modifiers,
                    ),
                )
                for case_dir_name in case_dirs
            )

    # C#'s default sequence format is a tuple, but a typed declaration
    # forces an array type — mixing the two yields invalid C#.  Force
    # ARRAY for sequence cases so the inferred ``object[]`` matches the
    # generated initializer.
    csharp_readonly_mixed = Variant(
        name="CSharp_modifiers_readonly_mixed_numbers",
        spec=make_spec(
            lang_cls=CSharp,
            sequence_format=CSharp.sequence_formats.ARRAY,
        ),
        lang_cls=CSharp,
    )
    cases.append(
        VariantCase(
            variant_name=csharp_readonly_mixed.name,
            variant=csharp_readonly_mixed,
            case_dir_name="mixed_number_list",
            variable_form=literalizer.NewVariable(
                name="my_data",
                modifiers=frozenset({CSharp.modifiers.READONLY}),
            ),
        )
    )
    csharp_readonly_array = Variant(
        name="CSharp_modifiers_readonly_array",
        spec=make_spec(
            lang_cls=CSharp,
            sequence_format=CSharp.sequence_formats.ARRAY,
        ),
        lang_cls=CSharp,
    )
    cases.append(
        VariantCase(
            variant_name=csharp_readonly_array.name,
            variant=csharp_readonly_array,
            case_dir_name="simple_sequence",
            variable_form=literalizer.NewVariable(
                name="my_data",
                modifiers=frozenset({CSharp.modifiers.READONLY}),
            ),
        )
    )
    return cases


@dataclasses.dataclass(frozen=True, kw_only=True)
class CaseInput:
    """An input case directory plus a variant-name suffix."""

    case_dir_name: str
    suffix: str = ""


@dataclasses.dataclass(frozen=True, kw_only=True)
class _SimpleAxis:
    """A format axis whose variants come from
    :func:`build_non_default_variants`.

    ``kwarg`` is the language-class constructor parameter name; the
    accessor functions read the default value and the formats enum from
    a built spec (which sometimes diverge from ``kwarg``, e.g.
    ``bytes_format`` reads from ``format_bytes``).
    """

    category: str
    kwarg: str
    get_default: Callable[[literalizer.Language], object]
    get_formats: Callable[[literalizer.Language], type[enum.Enum]]


_SIMPLE_AXES: dict[str, _SimpleAxis] = {
    "date": _SimpleAxis(
        category="date",
        kwarg="date_format",
        get_default=lambda s: s.format_date,
        get_formats=lambda s: s.date_formats,
    ),
    "datetime": _SimpleAxis(
        category="datetime",
        kwarg="datetime_format",
        get_default=lambda s: s.format_datetime,
        get_formats=lambda s: s.datetime_formats,
    ),
    "sequence": _SimpleAxis(
        category="sequence",
        kwarg="sequence_format",
        get_default=lambda s: s.sequence_format,
        get_formats=lambda s: s.sequence_formats,
    ),
    "set": _SimpleAxis(
        category="set",
        kwarg="set_format",
        get_default=lambda s: s.set_format,
        get_formats=lambda s: s.set_formats,
    ),
    "comment": _SimpleAxis(
        category="comment",
        kwarg="comment_format",
        get_default=lambda s: s.comment_format,
        get_formats=lambda s: s.comment_formats,
    ),
    "type_hints": _SimpleAxis(
        category="type_hints",
        kwarg="variable_type_hints",
        get_default=lambda s: s.variable_type_hints,
        get_formats=lambda s: s.variable_type_hints_formats,
    ),
    "dict_format": _SimpleAxis(
        category="dict_format",
        kwarg="dict_format",
        get_default=lambda s: s.dict_format,
        get_formats=lambda s: s.dict_formats,
    ),
    "dict_entry_style": _SimpleAxis(
        category="dict_entry_style",
        kwarg="dict_entry_style",
        get_default=lambda s: s.dict_entry_style,
        get_formats=lambda s: s.dict_entry_styles,
    ),
    "integer_format": _SimpleAxis(
        category="integer_format",
        kwarg="integer_format",
        get_default=lambda s: s.integer_format,
        get_formats=lambda s: s.integer_formats,
    ),
    "numeric_literal_suffix": _SimpleAxis(
        category="numeric_literal_suffix",
        kwarg="numeric_literal_suffix",
        get_default=lambda s: s.numeric_literal_suffix,
        get_formats=lambda s: s.numeric_literal_suffixes,
    ),
    "numeric_separator": _SimpleAxis(
        category="numeric_separator",
        kwarg="numeric_separator",
        get_default=lambda s: s.numeric_separator,
        get_formats=lambda s: s.numeric_separators,
    ),
    "float_format": _SimpleAxis(
        category="float_format",
        kwarg="float_format",
        get_default=lambda s: s.float_format,
        get_formats=lambda s: s.float_formats,
    ),
    "numeric_style": _SimpleAxis(
        category="numeric_style",
        kwarg="numeric_style",
        get_default=lambda s: s.numeric_style,
        get_formats=lambda s: s.numeric_styles,
    ),
    "string_format": _SimpleAxis(
        category="string_format",
        kwarg="string_format",
        get_default=lambda s: s.string_format,
        get_formats=lambda s: s.string_formats,
    ),
    "bytes_format": _SimpleAxis(
        category="bytes_format",
        kwarg="bytes_format",
        get_default=lambda s: s.format_bytes,
        get_formats=lambda s: s.bytes_formats,
    ),
    "trailing_comma": _SimpleAxis(
        category="trailing_comma",
        kwarg="trailing_comma",
        get_default=lambda s: s.trailing_comma,
        get_formats=lambda s: s.trailing_commas,
    ),
    "statement_terminator_style": _SimpleAxis(
        category="statement_terminator_style",
        kwarg="statement_terminator_style",
        get_default=lambda s: s.statement_terminator_style,
        get_formats=lambda s: s.statement_terminator_styles,
    ),
    "heterogeneous_strategy": _SimpleAxis(
        category="heterogeneous_strategy",
        kwarg="heterogeneous_strategy",
        get_default=lambda s: s.heterogeneous_strategy,
        get_formats=lambda s: s.heterogeneous_strategies,
    ),
}


@beartype
def _build_simple_axis(*, axis: _SimpleAxis) -> list[Variant]:
    """Build variants for a simple format axis."""
    return build_non_default_variants(
        category=axis.category,
        get_default=axis.get_default,
        get_formats=axis.get_formats,
        make_variant_spec=lambda cls, fmt: make_spec(
            lang_cls=cls, **{axis.kwarg: fmt}
        ),
    )


@beartype
def _build_declaration_style_variants() -> list[Variant]:
    """Build declaration-style variants, applying per-language sequence-
    format overrides where the default sequence format is incompatible
    (e.g. Rust ``CONST`` / ``STATIC`` with ``VEC``).
    """

    def make_spec_for(
        cls: literalizer.LanguageCls,
        fmt: enum.Enum,
    ) -> literalizer.Language:
        """Build a spec for *fmt*, applying any sequence-format
        override.
        """
        overrides = DECLARATION_STYLE_SEQUENCE_FORMAT_OVERRIDES.get(cls, {})
        seq_format_name = overrides.get(fmt.name)
        if seq_format_name is None:
            return make_spec(lang_cls=cls, declaration_style=fmt)
        spec = make_spec(lang_cls=cls)
        seq_fmt = next(
            f for f in spec.sequence_formats if f.name == seq_format_name
        )
        return make_spec(
            lang_cls=cls, declaration_style=fmt, sequence_format=seq_fmt
        )

    return build_non_default_variants(
        category="declaration_style",
        get_default=lambda s: s.declaration_style,
        get_formats=lambda s: s.declaration_styles,
        make_variant_spec=make_spec_for,
    )


_COMPLEX_BUILDERS: dict[str, Callable[[], Iterable[Variant]]] = {
    "collection_layout": build_collection_layout_variants,
    "declaration_style": _build_declaration_style_variants,
    "default_set_element_type": build_default_set_element_type_variants,
    "default_sequence_element_type": (
        build_default_sequence_element_type_variants
    ),
    "default_dict_value_type": build_default_dict_value_type_variants,
    "default_dict_key_type": build_default_dict_key_type_variants,
    "default_ordered_map_value_type": (
        build_default_ordered_map_value_type_variants
    ),
    "statement_terminator_style_decl": (
        build_statement_terminator_style_decl_variants
    ),
    "sequence_decl": build_sequence_decl_variants,
    "type_hints_cross": build_type_hints_cross_variants,
    "string_format_date_cross": lambda: build_string_format_cross_variants(
        other_kwarg="date_format",
        other_tag="date",
        get_other_default=lambda s: s.date_format,
        get_other_formats=lambda s: s.date_formats,
    ),
    "string_format_datetime_cross": lambda: build_string_format_cross_variants(
        other_kwarg="datetime_format",
        other_tag="dt",
        get_other_default=lambda s: s.datetime_format,
        get_other_formats=lambda s: s.datetime_formats,
    ),
    "type_name": build_type_name_variants,
    "constructor_prefix": build_constructor_prefix_variants,
    "constructor_name": build_constructor_name_variants,
    "c_field_name": build_c_field_name_variants,
    "heterogeneous_value_enum_name": build_heterogeneous_value_name_variants,
    "heterogeneous_value_union_name": (
        build_heterogeneous_value_union_name_variants
    ),
    "heterogeneous_value_variant_name": (
        build_heterogeneous_value_variant_name_variants
    ),
    "language_version": build_language_version_variants,
    "language_version_cross_dict_type": (
        build_language_version_cross_dict_type_variants
    ),
}


@beartype
def _ci(*, case_dir_name: str, suffix: str = "") -> CaseInput:
    """Shorthand for :class:`CaseInput` to keep the table compact."""
    return CaseInput(case_dir_name=case_dir_name, suffix=suffix)


INT_INPUTS: tuple[CaseInput, ...] = (
    _ci(case_dir_name="int_list"),
    _ci(case_dir_name="int_list_large", suffix="_large"),
    _ci(case_dir_name="int_list_with_zero", suffix="_zero"),
    _ci(case_dir_name="scalar_int"),
    _ci(case_dir_name="scalar_int_large"),
)

FLOAT_INPUTS: tuple[CaseInput, ...] = (
    _ci(case_dir_name="float_list"),
    _ci(case_dir_name="float_scientific_notation", suffix="_s"),
    _ci(case_dir_name="float_special_values", suffix="_v"),
    _ci(case_dir_name="nested_float_list", suffix="_n"),
    _ci(case_dir_name="scalar_float"),
)

BASIC_COLLECTIONS: tuple[CaseInput, ...] = (
    _ci(case_dir_name="simple_sequence"),
    _ci(case_dir_name="simple_dict", suffix="_dict"),
    _ci(case_dir_name="set", suffix="_set"),
)

ADT_INPUTS: tuple[CaseInput, ...] = (
    _ci(case_dir_name="simple_dict"),
    _ci(case_dir_name="float_special_values", suffix="_v"),
    _ci(case_dir_name="float_list", suffix="_float"),
    _ci(case_dir_name="binary", suffix="_binary"),
    _ci(case_dir_name="scalar_date", suffix="_date"),
    _ci(case_dir_name="scalar_datetime", suffix="_datetime"),
)

HETEROGENEOUS_INPUTS: tuple[CaseInput, ...] = tuple(
    _ci(case_dir_name=d, suffix=s)
    for d, s in (
        ("dict_mixed_scalars", ""),
        ("mixed_type_dicts_in_sequence", ""),
        ("nested_mixed_types", "_sibling"),
        ("nested_mixed_inner", "_inner"),
        ("nested_mixed_dict", ""),
        ("dict_all_scalar_types", ""),
        ("nested_sequences", ""),
        ("dict_mixed_int_widths", ""),
        ("ordered_map", ""),
    )
)

DICT_FORMAT_INPUTS: tuple[CaseInput, ...] = (
    _ci(case_dir_name="simple_dict"),
    _ci(case_dir_name="dict_with_list_value", suffix="_list_val"),
)

DEFAULT_DICT_INPUTS: tuple[CaseInput, ...] = (
    _ci(case_dir_name="empty_dict"),
    _ci(case_dir_name="simple_dict"),
)

_NUMERIC_INPUTS: tuple[CaseInput, ...] = (
    _ci(case_dir_name="int_list"),
    _ci(case_dir_name="int_list_large", suffix="_large"),
    _ci(case_dir_name="int_list_with_zero", suffix="_zero"),
    _ci(case_dir_name="scalar_int"),
    _ci(case_dir_name="scalar_int_large"),
    _ci(case_dir_name="float_list", suffix="_float"),
    _ci(case_dir_name="float_scientific_notation", suffix="_float_s"),
    _ci(case_dir_name="float_special_values", suffix="_float_v"),
    _ci(case_dir_name="nested_float_list", suffix="_float_n"),
    _ci(case_dir_name="scalar_float", suffix="_float_scalar"),
)


# Per-axis input table.  Each axis names the input case directories it
# should run against; coverage is added or removed by editing this table
# alone.  The cross product of every axis's variants with its inputs
# yields the full set of golden-file test cases.
AXIS_INPUTS: dict[str, tuple[CaseInput, ...]] = {
    "date": (
        _ci(case_dir_name="scalar_date"),
        _ci(case_dir_name="date_list"),
        _ci(case_dir_name="date_set"),
    ),
    "datetime": (
        _ci(case_dir_name="scalar_datetime"),
        _ci(case_dir_name="scalar_datetime_naive", suffix="_naive"),
        _ci(case_dir_name="scalar_datetime_non_utc", suffix="_non_utc"),
        _ci(case_dir_name="datetime_list"),
    ),
    "sequence": (
        _ci(case_dir_name="simple_sequence"),
        _ci(case_dir_name="pair_sequence", suffix="_pair"),
        _ci(case_dir_name="triple_sequence", suffix="_triple"),
        _ci(case_dir_name="simple_sequence", suffix="_varname"),
        _ci(case_dir_name="float_list", suffix="_float"),
        _ci(case_dir_name="null_list", suffix="_null"),
        _ci(case_dir_name="binary_list", suffix="_binary"),
    ),
    "set": (
        _ci(case_dir_name="set"),
        _ci(case_dir_name="int_set"),
        _ci(case_dir_name="mixed_set"),
        _ci(case_dir_name="empty_set"),
    ),
    "default_set_element_type": (
        _ci(case_dir_name="empty_set"),
        _ci(case_dir_name="set"),
    ),
    "default_sequence_element_type": (
        _ci(case_dir_name="empty_sequence"),
        _ci(case_dir_name="simple_sequence"),
    ),
    "default_dict_value_type": DEFAULT_DICT_INPUTS,
    "default_dict_key_type": DEFAULT_DICT_INPUTS,
    "default_ordered_map_value_type": (_ci(case_dir_name="ordered_map"),),
    "comment": (_ci(case_dir_name="comments"),),
    "type_hints": tuple(
        _ci(case_dir_name=d)
        for d in (
            "type_hints",
            "scalar_date",
            "scalar_datetime",
            "binary",
            "mixed_type_dicts_in_sequence",
            "empty_dicts_in_sequence",
            "float_list",
            "int_list",
            "empty_list",
            "int_set",
            "mixed_set",
            "empty_set",
            "mixed_number_list",
            "nested_sequence",
            "dict_with_list_value",
            "ordered_map_in_sequence",
        )
    ),
    "type_hints_cross": tuple(
        _ci(case_dir_name=d)
        for d in (
            "int_list",
            "int_list_large",
            "pair_sequence",
            "empty_list",
            "scalar_date",
            "scalar_datetime",
            "simple_dict",
            "int_set",
            "bool_list",
            "float_list",
        )
    ),
    "declaration_style": tuple(
        _ci(case_dir_name=d)
        for d in (
            "simple_sequence",
            "simple_dict",
            "empty_list",
            "empty_dict",
            "int_list",
            "int_key_dict",
            "scalar_int",
            "scalar_int_large",
            "scalar_float",
            "scalar_bool",
            "scalar_string",
            "scalar_null",
            "scalar_date",
            "scalar_datetime",
            "binary",
        )
    ),
    "dict_format": DICT_FORMAT_INPUTS,
    "dict_entry_style": DICT_FORMAT_INPUTS,
    "float_format": FLOAT_INPUTS,
    "integer_format": INT_INPUTS,
    "numeric_literal_suffix": _NUMERIC_INPUTS,
    "numeric_separator": _NUMERIC_INPUTS,
    "string_format": (
        _ci(case_dir_name="string_list"),
        _ci(case_dir_name="string_with_backslash"),
        _ci(case_dir_name="simple_dict", suffix="_dict"),
        _ci(case_dir_name="binary", suffix="_binary"),
        _ci(case_dir_name="scalar_string"),
    ),
    "string_format_date_cross": (_ci(case_dir_name="scalar_date"),),
    "string_format_datetime_cross": (
        _ci(case_dir_name="scalar_datetime", suffix="_dt"),
    ),
    "bytes_format": (_ci(case_dir_name="binary"),),
    "trailing_comma": BASIC_COLLECTIONS,
    "statement_terminator_style": BASIC_COLLECTIONS,
    "collection_layout": (_ci(case_dir_name="dict_with_list_value"),),
    "statement_terminator_style_decl": (_ci(case_dir_name="simple_sequence"),),
    "sequence_decl": (_ci(case_dir_name="int_list"),),
    "type_name": ADT_INPUTS,
    "constructor_prefix": ADT_INPUTS,
    "numeric_style": (
        _ci(case_dir_name="int_list"),
        _ci(case_dir_name="int_list_large", suffix="_large"),
        _ci(case_dir_name="int_list_with_zero", suffix="_zero"),
        _ci(case_dir_name="float_list"),
        _ci(case_dir_name="float_special_values"),
        _ci(case_dir_name="mixed_number_list"),
        _ci(case_dir_name="scalars"),
    ),
    "c_field_name": (
        _ci(case_dir_name="simple_dict"),
        _ci(case_dir_name="simple_sequence"),
    ),
    "constructor_name": (_ci(case_dir_name="simple_dict"),),
    "heterogeneous_strategy": HETEROGENEOUS_INPUTS,
    "heterogeneous_value_enum_name": HETEROGENEOUS_INPUTS,
    "heterogeneous_value_union_name": HETEROGENEOUS_INPUTS,
    "heterogeneous_value_variant_name": HETEROGENEOUS_INPUTS,
    "language_version": tuple(
        _ci(case_dir_name=case_dir_name)
        for case_dir_name in dict.fromkeys(
            case_dir_name
            for case_dir_name, _ in discover_cases(cases_dir=_CASES_DIR)
        )
    ),
    "language_version_cross_dict_type": (_ci(case_dir_name="empty_dict"),),
}


@beartype
def _variants_for_axis(axis_key: str) -> list[Variant]:
    """Return the variants for an axis key, dispatching to the simple
    or complex builder.
    """
    if axis_key in _SIMPLE_AXES:
        return _build_simple_axis(axis=_SIMPLE_AXES[axis_key])
    return list(_COMPLEX_BUILDERS[axis_key]())


@functools.cache
@beartype
def build_variant_cases() -> list[VariantCase]:
    """Collect all format-variant golden-file test cases.

    The full set is the cross product of every axis's variants with its
    declared inputs in :data:`AXIS_INPUTS`, plus the bespoke modifier
    cases from :func:`build_modifier_variant_cases`.
    """
    special_float_cases = cases_with_special_floats(cases_dir=_CASES_DIR)
    cases: list[VariantCase] = []
    for axis_key, inputs in AXIS_INPUTS.items():
        variants = _variants_for_axis(axis_key=axis_key)
        for variant in variants:
            cases.extend(
                VariantCase(
                    variant_name=f"{variant.name}{ci.suffix}",
                    variant=variant,
                    case_dir_name=ci.case_dir_name,
                    variable_form=wrap_variable_form(
                        lang_cls=variant.lang_cls
                    ),
                )
                for ci in inputs
                if not (
                    ci.case_dir_name in special_float_cases
                    and not variant.lang_cls.supports_special_floats
                )
            )
    cases.extend(build_modifier_variant_cases())
    return cases


@functools.cache
@beartype
def group_variant_cases_by_language() -> dict[
    literalizer.LanguageCls,
    list[VariantCase],
]:
    """Return variant cases grouped by language class.

    The test takes the language as its only pytest axis and iterates
    that language's cases inside the test body with ``subtests``.
    Folding ~2000 cases into ~30 cuts collection and per-test overhead
    on slower CI runners (notably Windows).
    """
    groups: dict[literalizer.LanguageCls, list[VariantCase]] = {}
    for case in build_variant_cases():
        groups.setdefault(case.variant.lang_cls, []).append(case)
    return groups


@functools.cache
@beartype
def variant_languages() -> list[literalizer.LanguageCls]:
    """Return languages that have at least one format-variant case."""
    groups = group_variant_cases_by_language()
    return [cls for cls in sorted_languages() if cls in groups]
