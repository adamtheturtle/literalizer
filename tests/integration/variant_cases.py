"""Build format-variant golden-file cases.

Each :class:`Variant` pairs a language class with a specific
non-default formatter spec; each :class:`VariantCase` pairs a variant
with one of the input case directories under ``tests/integration/cases``.
"""

import dataclasses
import enum
import functools
from collections.abc import Callable, Iterable

from beartype import beartype

import literalizer
from literalizer.languages import (
    C,
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
    Rust,
    Swift,
    VisualBasic,
)

from .language_specs import make_spec, sorted_languages


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
}

CONSTRUCTOR_PREFIX_OVERRIDES: dict[literalizer.LanguageCls, str] = {
    Elm: "J",
    FSharp: "J",
    Gleam: "J",
    Haskell: "J",
    OCaml: "J",
    PureScript: "J",
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
                spec=lang_cls(default_set_element_type=type_name),
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
                spec=lang_cls(default_sequence_element_type=type_name),
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
                spec=lang_cls(default_dict_value_type=type_name),
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
                spec=lang_cls(default_dict_key_type=type_name),
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
                spec=lang_cls(default_ordered_map_value_type=type_name),
                lang_cls=lang_cls,
            )
        )
    return variants


@beartype
def build_line_ending_decl_variants() -> Iterable[Variant]:
    """Build line-ending + declaration-style cross-option variants.

    For each language with multiple line endings *and* multiple
    declaration styles, create a variant for every non-default
    line ending paired with every non-default declaration style.
    """
    variants: list[Variant] = []
    for lang_cls in sorted_languages():
        lang_name = lang_cls.__name__
        spec = make_spec(lang_cls=lang_cls)
        default_line_ending = spec.line_ending
        default_declaration_style = spec.declaration_style
        non_default_line_endings = [
            line_ending
            for line_ending in spec.line_endings
            if line_ending is not default_line_ending
        ]
        non_default_declaration_styles = [
            declaration_style
            for declaration_style in spec.declaration_styles
            if declaration_style is not default_declaration_style
        ]
        variants.extend(
            Variant(
                name=(
                    f"{lang_name}_line_ending_{line_ending.name.lower()}"
                    f"_decl_{declaration_style.name.lower()}"
                ),
                spec=lang_cls(
                    line_ending=line_ending,
                    declaration_style=declaration_style,
                ),
                lang_cls=lang_cls,
            )
            for line_ending in non_default_line_endings
            for declaration_style in non_default_declaration_styles
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
                spec=lang_cls(
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
                spec=lang_cls(**kwargs),
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
                spec=lang_cls(type_name=custom_name),
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
                spec=lang_cls(constructor_prefix=custom_prefix),
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
        spec = lang_cls(
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
                spec=lang_cls(**kwargs),
                lang_cls=lang_cls,
            )
        )
    return variants


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
        spec = lang_cls(
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
        spec = lang_cls(
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
                        spec=lang_cls(
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
                            spec=lang_cls(
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


@functools.cache
@beartype
def build_variant_cases() -> list[VariantCase]:
    """Collect all format-variant golden-file test cases."""
    nv = build_non_default_variants
    date = nv(
        category="date",
        get_default=lambda s: s.format_date,
        get_formats=lambda s: s.date_formats,
        make_variant_spec=lambda cls, fmt: cls(date_format=fmt),
    )
    datetime_ = nv(
        category="datetime",
        get_default=lambda s: s.format_datetime,
        get_formats=lambda s: s.datetime_formats,
        make_variant_spec=lambda cls, fmt: cls(datetime_format=fmt),
    )
    sequence = nv(
        category="sequence",
        get_default=lambda s: s.sequence_format,
        get_formats=lambda s: s.sequence_formats,
        make_variant_spec=lambda cls, fmt: cls(sequence_format=fmt),
    )
    set_ = nv(
        category="set",
        get_default=lambda s: s.set_format,
        get_formats=lambda s: s.set_formats,
        make_variant_spec=lambda cls, fmt: cls(set_format=fmt),
    )
    comment = nv(
        category="comment",
        get_default=lambda s: s.comment_format,
        get_formats=lambda s: s.comment_formats,
        make_variant_spec=lambda cls, fmt: cls(comment_format=fmt),
    )
    type_hints = nv(
        category="type_hints",
        get_default=lambda s: s.variable_type_hints,
        get_formats=lambda s: s.variable_type_hints_formats,
        make_variant_spec=lambda cls, fmt: cls(variable_type_hints=fmt),
    )

    def declaration_style_make_spec(
        cls: literalizer.LanguageCls,
        fmt: enum.Enum,
    ) -> literalizer.Language:
        """Build a spec for *fmt*, applying any per-language sequence-
        format
        override listed in
        :data:`DECLARATION_STYLE_SEQUENCE_FORMAT_OVERRIDES`.

        Some declaration styles are incompatible with the default sequence
        format (e.g. Rust CONST/STATIC raise ``IncompatibleFormatsError``
        when combined with ``VEC``).
        """
        overrides = DECLARATION_STYLE_SEQUENCE_FORMAT_OVERRIDES.get(cls, {})
        seq_format_name = overrides.get(fmt.name)
        if seq_format_name is None:
            return cls(declaration_style=fmt)
        spec = cls()
        seq_fmt = next(
            f for f in spec.sequence_formats if f.name == seq_format_name
        )
        return cls(declaration_style=fmt, sequence_format=seq_fmt)

    declaration_style = nv(
        category="declaration_style",
        get_default=lambda s: s.declaration_style,
        get_formats=lambda s: s.declaration_styles,
        make_variant_spec=declaration_style_make_spec,
    )
    dict_format = nv(
        category="dict_format",
        get_default=lambda s: s.dict_format,
        get_formats=lambda s: s.dict_formats,
        make_variant_spec=lambda cls, fmt: cls(dict_format=fmt),
    )
    dict_entry_style = nv(
        category="dict_entry_style",
        get_default=lambda s: s.dict_entry_style,
        get_formats=lambda s: s.dict_entry_styles,
        make_variant_spec=lambda cls, fmt: cls(dict_entry_style=fmt),
    )
    integer_format = nv(
        category="integer_format",
        get_default=lambda s: s.integer_format,
        get_formats=lambda s: s.integer_formats,
        make_variant_spec=lambda cls, fmt: cls(integer_format=fmt),
    )
    numeric_literal_suffix = nv(
        category="numeric_literal_suffix",
        get_default=lambda s: s.numeric_literal_suffix,
        get_formats=lambda s: s.numeric_literal_suffixes,
        make_variant_spec=lambda cls, fmt: cls(numeric_literal_suffix=fmt),
    )
    numeric_separator = nv(
        category="numeric_separator",
        get_default=lambda s: s.numeric_separator,
        get_formats=lambda s: s.numeric_separators,
        make_variant_spec=lambda cls, fmt: cls(numeric_separator=fmt),
    )
    float_format = nv(
        category="float_format",
        get_default=lambda s: s.float_format,
        get_formats=lambda s: s.float_formats,
        make_variant_spec=lambda cls, fmt: cls(float_format=fmt),
    )
    numeric_style = nv(
        category="numeric_style",
        get_default=lambda s: s.numeric_style,
        get_formats=lambda s: s.numeric_styles,
        make_variant_spec=lambda cls, fmt: cls(numeric_style=fmt),
    )
    string_format = nv(
        category="string_format",
        get_default=lambda s: s.string_format,
        get_formats=lambda s: s.string_formats,
        make_variant_spec=lambda cls, fmt: cls(string_format=fmt),
    )
    bytes_format = nv(
        category="bytes_format",
        get_default=lambda s: s.format_bytes,
        get_formats=lambda s: s.bytes_formats,
        make_variant_spec=lambda cls, fmt: cls(bytes_format=fmt),
    )
    trailing_comma = nv(
        category="trailing_comma",
        get_default=lambda s: s.trailing_comma,
        get_formats=lambda s: s.trailing_commas,
        make_variant_spec=lambda cls, fmt: cls(trailing_comma=fmt),
    )
    line_ending = nv(
        category="line_ending",
        get_default=lambda s: s.line_ending,
        get_formats=lambda s: s.line_endings,
        make_variant_spec=lambda cls, fmt: cls(line_ending=fmt),
    )
    heterogeneous_strategy = nv(
        category="heterogeneous_strategy",
        get_default=lambda s: s.heterogeneous_strategy,
        get_formats=lambda s: s.heterogeneous_strategies,
        make_variant_spec=lambda cls, fmt: cls(heterogeneous_strategy=fmt),
    )

    type_hints_cross = build_type_hints_cross_variants()
    string_format_date_cross = build_string_format_cross_variants(
        other_kwarg="date_format",
        other_tag="date",
        get_other_default=lambda s: s.date_format,
        get_other_formats=lambda s: s.date_formats,
    )
    string_format_datetime_cross = build_string_format_cross_variants(
        other_kwarg="datetime_format",
        other_tag="dt",
        get_other_default=lambda s: s.datetime_format,
        get_other_formats=lambda s: s.datetime_formats,
    )

    cases: list[VariantCase] = []
    variant_sources: list[tuple[Iterable[Variant], str, str]] = [
        (date, "scalar_date", ""),
        (date, "date_list", ""),
        (date, "date_set", ""),
        (datetime_, "scalar_datetime", ""),
        (datetime_, "scalar_datetime_naive", "_naive"),
        (datetime_, "scalar_datetime_non_utc", "_non_utc"),
        (sequence, "simple_sequence", ""),
        (sequence, "pair_sequence", "_pair"),
        (sequence, "triple_sequence", "_triple"),
        (sequence, "simple_sequence", "_varname"),
        (set_, "set", ""),
        (build_default_set_element_type_variants(), "empty_set", ""),
        (build_default_set_element_type_variants(), "set", ""),
        (
            build_default_sequence_element_type_variants(),
            "empty_sequence",
            "",
        ),
        (
            build_default_sequence_element_type_variants(),
            "simple_sequence",
            "",
        ),
        (build_default_dict_value_type_variants(), "empty_dict", ""),
        (build_default_dict_value_type_variants(), "simple_dict", ""),
        (build_default_dict_key_type_variants(), "empty_dict", ""),
        (build_default_dict_key_type_variants(), "simple_dict", ""),
        (
            build_default_ordered_map_value_type_variants(),
            "ordered_map",
            "",
        ),
        (comment, "comments", ""),
        (type_hints, "type_hints", ""),
        (type_hints, "scalar_date", ""),
        (type_hints, "scalar_datetime", ""),
        (type_hints, "binary", ""),
        (type_hints, "mixed_type_dicts_in_sequence", ""),
        (type_hints, "empty_dicts_in_sequence", ""),
        (type_hints, "float_list", ""),
        (type_hints, "int_list", ""),
        (type_hints, "empty_list", ""),
        (type_hints, "int_set", ""),
        (type_hints, "empty_set", ""),
        (type_hints, "mixed_number_list", ""),
        (type_hints, "nested_sequence", ""),
        (type_hints, "dict_with_list_value", ""),
        (type_hints, "ordered_map_in_sequence", ""),
        (type_hints_cross, "int_list", ""),
        (type_hints_cross, "int_list_large", ""),
        (type_hints_cross, "pair_sequence", ""),
        (type_hints_cross, "empty_list", ""),
        (type_hints_cross, "scalar_date", ""),
        (type_hints_cross, "scalar_datetime", ""),
        (type_hints_cross, "simple_dict", ""),
        (type_hints_cross, "int_set", ""),
        (declaration_style, "simple_sequence", ""),
        (declaration_style, "simple_dict", ""),
        (declaration_style, "empty_list", ""),
        (declaration_style, "empty_dict", ""),
        (declaration_style, "int_list", ""),
        (declaration_style, "int_key_dict", ""),
        (declaration_style, "scalar_int", ""),
        (declaration_style, "scalar_int_large", ""),
        (declaration_style, "scalar_float", ""),
        (declaration_style, "scalar_bool", ""),
        (declaration_style, "scalar_string", ""),
        (declaration_style, "scalar_null", ""),
        (declaration_style, "scalar_date", ""),
        (declaration_style, "scalar_datetime", ""),
        (declaration_style, "binary", ""),
        (dict_format, "simple_dict", ""),
        (dict_format, "dict_with_list_value", "_list_val"),
        (dict_entry_style, "simple_dict", ""),
        (
            dict_entry_style,
            "dict_with_list_value",
            "_list_val",
        ),
        (sequence, "float_list", "_float"),
        (float_format, "float_list", ""),
        (float_format, "float_scientific_notation", "_s"),
        (float_format, "float_special_values", "_v"),
        (float_format, "nested_float_list", "_n"),
        (integer_format, "int_list", ""),
        (integer_format, "int_list_large", "_large"),
        (integer_format, "int_list_with_zero", "_zero"),
        (numeric_literal_suffix, "int_list", ""),
        (numeric_literal_suffix, "int_list_large", "_large"),
        (
            numeric_literal_suffix,
            "int_list_with_zero",
            "_zero",
        ),
        (numeric_separator, "int_list", ""),
        (numeric_separator, "int_list_large", "_large"),
        (numeric_separator, "int_list_with_zero", "_zero"),
        (string_format, "string_list", ""),
        (string_format, "string_with_backslash", ""),
        (string_format, "simple_dict", "_dict"),
        (string_format, "binary", "_binary"),
        (string_format_date_cross, "scalar_date", ""),
        (string_format_datetime_cross, "scalar_datetime", "_dt"),
        (bytes_format, "binary", ""),
        (trailing_comma, "simple_sequence", ""),
        (line_ending, "simple_sequence", ""),
        (line_ending, "simple_dict", "_dict"),
        (build_line_ending_decl_variants(), "simple_sequence", ""),
        (build_sequence_decl_variants(), "int_list", ""),
        (build_type_name_variants(), "simple_dict", ""),
        (build_constructor_prefix_variants(), "simple_dict", ""),
        (build_constructor_prefix_variants(), "float_special_values", "_v"),
        (build_constructor_prefix_variants(), "float_list", "_float"),
        (build_constructor_prefix_variants(), "binary", "_binary"),
        (build_constructor_prefix_variants(), "scalar_date", "_date"),
        (build_constructor_prefix_variants(), "scalar_datetime", "_datetime"),
        (numeric_style, "int_list", ""),
        (numeric_style, "int_list_with_zero", "_zero"),
        (numeric_style, "float_list", ""),
        (numeric_style, "float_special_values", ""),
        (numeric_style, "mixed_number_list", ""),
        (numeric_style, "scalars", ""),
        (build_c_field_name_variants(), "simple_dict", ""),
        (build_c_field_name_variants(), "simple_sequence", ""),
        (build_constructor_name_variants(), "simple_dict", ""),
        (type_hints_cross, "bool_list", ""),
        (type_hints_cross, "float_list", ""),
        (heterogeneous_strategy, "dict_mixed_scalars", ""),
        (heterogeneous_strategy, "mixed_type_dicts_in_sequence", ""),
        (
            build_heterogeneous_value_name_variants(),
            "dict_mixed_scalars",
            "",
        ),
        (
            build_heterogeneous_value_union_name_variants(),
            "dict_mixed_scalars",
            "",
        ),
        (
            build_heterogeneous_value_variant_name_variants(),
            "dict_mixed_scalars",
            "",
        ),
        (heterogeneous_strategy, "nested_mixed_types", "_sibling"),
        (heterogeneous_strategy, "nested_mixed_inner", "_inner"),
        (heterogeneous_strategy, "nested_mixed_dict", ""),
        (heterogeneous_strategy, "dict_all_scalar_types", ""),
        (heterogeneous_strategy, "nested_sequences", ""),
        (heterogeneous_strategy, "dict_mixed_int_widths", ""),
        (heterogeneous_strategy, "ordered_map", ""),
    ]
    for variants, case_dir_name, suffix in variant_sources:
        cases.extend(
            VariantCase(
                variant_name=f"{variant.name}{suffix}",
                variant=variant,
                case_dir_name=case_dir_name,
                variable_form=wrap_variable_form(lang_cls=variant.lang_cls),
            )
            for variant in variants
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
