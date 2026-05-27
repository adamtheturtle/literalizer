"""Build format-variant golden-file cases.

Each :class:`Variant` pairs a language class with a specific
non-default formatter spec; each :class:`VariantCase` pairs a variant
with one of the input case directories under ``tests/integration/cases``.
"""

import dataclasses
import enum
import functools
from collections.abc import Callable, Iterable, Mapping
from pathlib import Path
from typing import Protocol, runtime_checkable

from beartype import beartype

import literalizer
from literalizer.languages import (
    ALL_LANGUAGES,
    C,
    Cobol,
    Cpp,
    Crystal,
    CSharp,
    D,
    Dart,
    Dhall,
    Elm,
    Fortran,
    FSharp,
    Gleam,
    Go,
    Groovy,
    Haskell,
    Java,
    Kotlin,
    Mojo,
    Nim,
    OCaml,
    Odin,
    PureScript,
    Python,
    Roc,
    Rust,
    Scala,
    Swift,
    VisualBasic,
    Zig,
)

from .case_discovery import cases_with_special_floats, discover_cases
from .language_specs import make_spec, sorted_languages

_CASES_DIR = Path(__file__).parent / "cases"


@beartype
def wrap_variable_form() -> literalizer.NewVariable:
    """Return the canonical :class:`NewVariable` form used by the
    variable-form integration tests.

    Callers that pass the result to ``literalize`` should treat
    :class:`~literalizer.exceptions.VariableNameNotSupportedError` as
    the signal that the language cannot wrap output in a named
    variable, rather than pre-filtering on ``supports_variable_names``.
    """
    return literalizer.NewVariable(name="my_data")


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
# type name for that language's linter / compiler.  Each mapping enumerates
# every language whose dataclass exposes the corresponding kwargs entry.
DEFAULT_SET_ELEMENT_TYPES: dict[literalizer.LanguageCls, str] = {
    CSharp: "string",
    Crystal: "Int32",
    Dart: "String",
    Go: "string",
    Groovy: "String",
    Kotlin: "String",
    Mojo: "Int",
    Odin: "int",
    Python: "int",
    Rust: "i32",
    Swift: "String",
    VisualBasic: "String",
}

DEFAULT_SEQUENCE_ELEMENT_TYPES: dict[literalizer.LanguageCls, str] = {
    CSharp: "string",
    Go: "interface{}",
    Mojo: "Int",
    Python: "int",
    Rust: "i32",
    Swift: "String",
    VisualBasic: "String",
}

DEFAULT_DICT_VALUE_TYPES: dict[literalizer.LanguageCls, str] = {
    CSharp: "object?",
    Crystal: "Int32",
    Dart: "Object?",
    Go: "interface{}",
    Kotlin: "Comparable<*>?",
    Mojo: "Int",
    Python: "int",
    Rust: "i32",
    Swift: "String",
    VisualBasic: "String",
}

DEFAULT_DICT_KEY_TYPES: dict[literalizer.LanguageCls, str] = {
    CSharp: "object",
    Crystal: "Int32",
    Dart: "Object",
    Go: "any",
    Kotlin: "Any",
    Mojo: "Int",
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


DEFAULT_ORDERED_MAP_VALUE_TYPES: dict[literalizer.LanguageCls, str] = {
    Go: "interface{}",
}


@runtime_checkable
class _HasDefaultSetElementType(Protocol):
    """Structural type for languages with a ``default_set_element_type``
    field.
    """

    default_set_element_type: str


@runtime_checkable
class _HasDefaultSequenceElementType(Protocol):
    """Structural type for languages with a
    ``default_sequence_element_type`` field.
    """

    default_sequence_element_type: str


@runtime_checkable
class _HasDefaultDictValueType(Protocol):
    """Structural type for languages with a ``default_dict_value_type``
    field.
    """

    default_dict_value_type: str


@runtime_checkable
class _HasDefaultDictKeyType(Protocol):
    """Structural type for languages with a ``default_dict_key_type``
    field.
    """

    default_dict_key_type: str


@runtime_checkable
class _HasDefaultOrderedMapValueType(Protocol):
    """Structural type for languages with a
    ``default_ordered_map_value_type`` field.
    """

    default_ordered_map_value_type: str


def _read_default_set_element_type(spec: literalizer.Language) -> str:
    """Read ``default_set_element_type`` from a default-constructed
    spec.
    """
    assert isinstance(spec, _HasDefaultSetElementType)  # noqa: S101
    return spec.default_set_element_type


def _read_default_sequence_element_type(spec: literalizer.Language) -> str:
    """Read ``default_sequence_element_type`` from a default-constructed
    spec.
    """
    assert isinstance(spec, _HasDefaultSequenceElementType)  # noqa: S101
    return spec.default_sequence_element_type


def _read_default_dict_value_type(spec: literalizer.Language) -> str:
    """Read ``default_dict_value_type`` from a default-constructed
    spec.
    """
    assert isinstance(spec, _HasDefaultDictValueType)  # noqa: S101
    return spec.default_dict_value_type


def _read_default_dict_key_type(spec: literalizer.Language) -> str:
    """Read ``default_dict_key_type`` from a default-constructed spec."""
    assert isinstance(spec, _HasDefaultDictKeyType)  # noqa: S101
    return spec.default_dict_key_type


def _read_default_ordered_map_value_type(spec: literalizer.Language) -> str:
    """Read ``default_ordered_map_value_type`` from a default-constructed
    spec.
    """
    assert isinstance(spec, _HasDefaultOrderedMapValueType)  # noqa: S101
    return spec.default_ordered_map_value_type


@dataclasses.dataclass(frozen=True, kw_only=True)
class _DefaultTypeTable:
    """Validation entry for one ``DEFAULT_*_TYPES`` override table."""

    field_name: str
    table: dict[literalizer.LanguageCls, str]
    supports: Callable[[literalizer.LanguageCls], bool]
    read_default: Callable[[literalizer.Language], str]


def _check_default_type_tables() -> None:
    """Validate the ``DEFAULT_*_TYPES`` tables at import time.

    Each table must list exactly the languages whose dataclass exposes
    the corresponding ``default_*_type`` field, and every override
    value must differ from that field's own default; either kind of
    drift would silently break variant coverage.
    """
    tables: tuple[_DefaultTypeTable, ...] = (
        _DefaultTypeTable(
            field_name="default_set_element_type",
            table=DEFAULT_SET_ELEMENT_TYPES,
            supports=lambda cls: cls.supports_default_set_element_type,
            read_default=_read_default_set_element_type,
        ),
        _DefaultTypeTable(
            field_name="default_sequence_element_type",
            table=DEFAULT_SEQUENCE_ELEMENT_TYPES,
            supports=lambda cls: cls.supports_default_sequence_element_type,
            read_default=_read_default_sequence_element_type,
        ),
        _DefaultTypeTable(
            field_name="default_dict_value_type",
            table=DEFAULT_DICT_VALUE_TYPES,
            supports=lambda cls: cls.supports_default_dict_value_type,
            read_default=_read_default_dict_value_type,
        ),
        _DefaultTypeTable(
            field_name="default_dict_key_type",
            table=DEFAULT_DICT_KEY_TYPES,
            supports=lambda cls: cls.supports_default_dict_key_type,
            read_default=_read_default_dict_key_type,
        ),
        _DefaultTypeTable(
            field_name="default_ordered_map_value_type",
            table=DEFAULT_ORDERED_MAP_VALUE_TYPES,
            supports=lambda cls: cls.supports_default_ordered_map_value_type,
            read_default=_read_default_ordered_map_value_type,
        ),
    )
    for entry in tables:
        expected = {cls for cls in ALL_LANGUAGES if entry.supports(cls)}
        assert set(entry.table.keys()) == expected, entry.field_name  # noqa: S101
        for lang_cls, override in entry.table.items():
            default = entry.read_default(make_spec(lang_cls=lang_cls))
            assert override != default, (  # noqa: S101
                f"{lang_cls.__name__}.{entry.field_name}={override!r}"
            )


_check_default_type_tables()

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
    collection_layout: literalizer.CollectionLayout


@dataclasses.dataclass(frozen=True)
class VariantCase:
    """A format-variant golden-file test case."""

    variant_name: str
    variant: Variant
    case_dir_name: str
    variable_form: literalizer.VariableForm


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
                    collection_layout=literalizer.CollectionLayout.COMPACT,
                )
            )
    return variants


@beartype
def build_default_set_element_type_variants() -> Iterable[Variant]:
    """Build default-set-type variants for languages that support it."""
    return [
        Variant(
            name=f"{lang_cls.__name__}_default_set_element_type_string",
            spec=make_spec(
                lang_cls=lang_cls, default_set_element_type=type_name
            ),
            lang_cls=lang_cls,
            collection_layout=literalizer.CollectionLayout.COMPACT,
        )
        for lang_cls, type_name in DEFAULT_SET_ELEMENT_TYPES.items()
    ]


@beartype
def build_default_sequence_element_type_variants() -> Iterable[Variant]:
    """Build default-sequence-type variants for languages that support
    it.
    """
    return [
        Variant(
            name=(f"{lang_cls.__name__}_default_sequence_element_type_string"),
            spec=make_spec(
                lang_cls=lang_cls, default_sequence_element_type=type_name
            ),
            lang_cls=lang_cls,
            collection_layout=literalizer.CollectionLayout.COMPACT,
        )
        for lang_cls, type_name in DEFAULT_SEQUENCE_ELEMENT_TYPES.items()
    ]


@beartype
def build_json_type_variants() -> Iterable[Variant]:
    """Build JSON value type variants for languages that support them."""
    return [
        Variant(
            name="Rust_json_type_serde_json_value",
            spec=make_spec(
                lang_cls=Rust,
                json_type=Rust.json_types.SERDE_JSON_VALUE,
            ),
            lang_cls=Rust,
            collection_layout=literalizer.CollectionLayout.COMPACT,
        ),
        Variant(
            name="Crystal_json_type_json_any",
            spec=make_spec(
                lang_cls=Crystal,
                json_type=Crystal.json_types.JSON_ANY,
            ),
            lang_cls=Crystal,
            collection_layout=literalizer.CollectionLayout.COMPACT,
        ),
        Variant(
            name="Java_json_type_jackson_json_node",
            spec=make_spec(
                lang_cls=Java,
                json_type=Java.json_types.JACKSON_JSON_NODE,
            ),
            lang_cls=Java,
            collection_layout=literalizer.CollectionLayout.COMPACT,
        ),
        Variant(
            name="Scala_json_type_circe",
            spec=make_spec(
                lang_cls=Scala,
                json_type=Scala.json_types.CIRCE,
            ),
            lang_cls=Scala,
            collection_layout=literalizer.CollectionLayout.COMPACT,
        ),
        Variant(
            name="CSharp_json_type_json_node",
            spec=make_spec(
                lang_cls=CSharp,
                json_type=CSharp.json_types.SYSTEM_TEXT_JSON_NODE,
            ),
            lang_cls=CSharp,
            collection_layout=literalizer.CollectionLayout.COMPACT,
        ),
        Variant(
            name="Nim_json_type_json_node",
            spec=make_spec(
                lang_cls=Nim,
                json_type=Nim.json_types.JSON_NODE,
            ),
            lang_cls=Nim,
            collection_layout=literalizer.CollectionLayout.COMPACT,
        ),
        Variant(
            name="Haskell_json_type_aeson_value",
            spec=make_spec(
                lang_cls=Haskell,
                json_type=Haskell.json_types.AESON_VALUE,
            ),
            lang_cls=Haskell,
            collection_layout=literalizer.CollectionLayout.COMPACT,
        ),
        Variant(
            name="Zig_json_type_std_json_value",
            spec=make_spec(
                lang_cls=Zig,
                json_type=Zig.json_types.STD_JSON_VALUE,
            ),
            lang_cls=Zig,
            collection_layout=literalizer.CollectionLayout.COMPACT,
        ),
        Variant(
            name="D_json_type_narrow",
            spec=make_spec(
                lang_cls=D,
                json_type=None,
            ),
            lang_cls=D,
            collection_layout=literalizer.CollectionLayout.COMPACT,
        ),
        Variant(
            name="Kotlin_json_type_kotlinx_json_element",
            spec=make_spec(
                lang_cls=Kotlin,
                json_type=Kotlin.json_types.KOTLINX_JSON_ELEMENT,
            ),
            lang_cls=Kotlin,
            collection_layout=literalizer.CollectionLayout.COMPACT,
        ),
        Variant(
            name="Cpp_json_type_nlohmann_json",
            spec=make_spec(
                lang_cls=Cpp,
                json_type=Cpp.json_types.NLOHMANN_JSON,
            ),
            lang_cls=Cpp,
            collection_layout=literalizer.CollectionLayout.COMPACT,
        ),
        Variant(
            name="Gleam_json_type_gleam_json_json",
            spec=make_spec(
                lang_cls=Gleam,
                json_type=Gleam.json_types.GLEAM_JSON_JSON,
            ),
            lang_cls=Gleam,
            collection_layout=literalizer.CollectionLayout.COMPACT,
        ),
        Variant(
            name="OCaml_json_type_yojson_safe_t",
            spec=make_spec(
                lang_cls=OCaml,
                json_type=OCaml.json_types.YOJSON_SAFE_T,
            ),
            lang_cls=OCaml,
            collection_layout=literalizer.CollectionLayout.COMPACT,
        ),
        Variant(
            name="Elm_json_type_json_encode_value",
            spec=make_spec(
                lang_cls=Elm,
                json_type=Elm.json_types.JSON_ENCODE_VALUE,
            ),
            lang_cls=Elm,
            collection_layout=literalizer.CollectionLayout.COMPACT,
        ),
    ]


@runtime_checkable
class _HasEmptyDictKey(Protocol):
    """Structural type for languages that expose an ``empty_dict_key``
    constructor field.

    Used by :func:`build_empty_dict_key_variants` to narrow a generic
    :class:`literalizer.Language` to one with the field, without
    introspecting ``__dataclass_fields__`` or casting to ``Any``.
    """

    empty_dict_key: enum.Enum
    empty_dict_keys: type[enum.Enum]


@beartype
def build_empty_dict_key_variants() -> Iterable[Variant]:
    """Build empty-dict-key variants for every language whose spec
    exposes the field with more than one policy.

    Languages whose ``EmptyDictKey`` enum has a single member (the common
    case today) produce no variants; languages that don't expose
    ``empty_dict_key`` at all are skipped via the protocol check.
    """
    variants: list[Variant] = []
    for lang_cls in sorted_languages():
        spec = make_spec(lang_cls=lang_cls)
        if not isinstance(spec, _HasEmptyDictKey):
            continue
        default = spec.empty_dict_key
        for fmt in spec.empty_dict_keys:
            if fmt is default:
                continue
            variants.append(
                Variant(
                    name=(
                        f"{lang_cls.__name__}"
                        f"_empty_dict_key_{fmt.name.lower()}"
                    ),
                    spec=make_spec(
                        lang_cls=lang_cls,
                        empty_dict_key=fmt,
                    ),
                    lang_cls=lang_cls,
                    collection_layout=literalizer.CollectionLayout.COMPACT,
                )
            )
    return variants


@beartype
def build_default_dict_value_type_variants() -> Iterable[Variant]:
    """Build default-dict-value-type variants for languages that support
    it.
    """
    return [
        Variant(
            name=f"{lang_cls.__name__}_default_dict_value_type_string",
            spec=make_spec(
                lang_cls=lang_cls, default_dict_value_type=type_name
            ),
            lang_cls=lang_cls,
            collection_layout=literalizer.CollectionLayout.COMPACT,
        )
        for lang_cls, type_name in DEFAULT_DICT_VALUE_TYPES.items()
    ]


@beartype
def build_default_dict_key_type_variants() -> Iterable[Variant]:
    """Build default-dict-key-type variants for languages that support
    it.
    """
    return [
        Variant(
            name=f"{lang_cls.__name__}_default_dict_key_type",
            spec=make_spec(lang_cls=lang_cls, default_dict_key_type=type_name),
            lang_cls=lang_cls,
            collection_layout=literalizer.CollectionLayout.COMPACT,
        )
        for lang_cls, type_name in DEFAULT_DICT_KEY_TYPES.items()
    ]


@beartype
def build_default_ordered_map_value_type_variants() -> Iterable[Variant]:
    """Build default-ordered-map-value-type variants for every language
    that supports the option.
    """
    return [
        Variant(
            name=f"{lang_cls.__name__}_default_ordered_map_value_type",
            spec=make_spec(
                lang_cls=lang_cls, default_ordered_map_value_type=type_name
            ),
            lang_cls=lang_cls,
            collection_layout=literalizer.CollectionLayout.COMPACT,
        )
        for lang_cls, type_name in DEFAULT_ORDERED_MAP_VALUE_TYPES.items()
    ]


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
                collection_layout=literalizer.CollectionLayout.COMPACT,
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
                collection_layout=literalizer.CollectionLayout.COMPACT,
            )
            for sequence_format in non_default_sequence_formats
            for declaration_style in non_default_declaration_styles
        )
    return variants


@beartype
def _resolve_sequence_format_override(
    *,
    lang_cls: literalizer.LanguageCls,
    declaration_style: enum.Enum,
) -> enum.Enum | None:
    """Return the sequence-format override for *declaration_style*, if
    any.

    Rust ``CONST`` and ``STATIC`` reject the default ``VEC`` sequence
    format upfront in ``__post_init__``; any cross-product variant that
    pairs them with a non-default set/dict format still has to apply
    the same sequence-format override the standalone declaration-style
    variants use.
    """
    overrides = DECLARATION_STYLE_SEQUENCE_FORMAT_OVERRIDES.get(lang_cls, {})
    seq_format_name = overrides.get(declaration_style.name)
    if seq_format_name is None:
        return None
    spec = make_spec(lang_cls=lang_cls)
    return next(f for f in spec.sequence_formats if f.name == seq_format_name)


@beartype
def build_set_decl_variants() -> Iterable[Variant]:
    """Build set format + declaration style cross-option variants.

    For each language with multiple set formats *and* multiple
    declaration styles, create a variant for every non-default
    set format paired with every non-default declaration style.
    """
    variants: list[Variant] = []
    for lang_cls in sorted_languages():
        lang_name = lang_cls.__name__
        spec = make_spec(lang_cls=lang_cls)
        default_set_format = spec.set_format
        default_declaration_style = spec.declaration_style
        non_default_set_formats = [
            set_format
            for set_format in spec.set_formats
            if set_format is not default_set_format
        ]
        non_default_declaration_styles = [
            declaration_style
            for declaration_style in spec.declaration_styles
            if declaration_style is not default_declaration_style
        ]
        for set_format in non_default_set_formats:
            for declaration_style in non_default_declaration_styles:
                seq_override = _resolve_sequence_format_override(
                    lang_cls=lang_cls,
                    declaration_style=declaration_style,
                )
                kwargs: dict[str, object] = {
                    "set_format": set_format,
                    "declaration_style": declaration_style,
                }
                if seq_override is not None:
                    kwargs["sequence_format"] = seq_override
                variants.append(
                    Variant(
                        name=(
                            f"{lang_name}_set_{set_format.name.lower()}"
                            f"_decl_{declaration_style.name.lower()}"
                        ),
                        spec=make_spec(lang_cls=lang_cls, **kwargs),
                        lang_cls=lang_cls,
                        collection_layout=literalizer.CollectionLayout.COMPACT,
                    )
                )
    return variants


@beartype
def build_dict_decl_variants() -> Iterable[Variant]:
    """Build dict format + declaration style cross-option variants.

    For each language with multiple dict formats *and* multiple
    declaration styles, create a variant for every non-default
    dict format paired with every non-default declaration style.
    """
    variants: list[Variant] = []
    for lang_cls in sorted_languages():
        lang_name = lang_cls.__name__
        spec = make_spec(lang_cls=lang_cls)
        default_dict_format = spec.dict_format
        default_declaration_style = spec.declaration_style
        non_default_dict_formats = [
            dict_format
            for dict_format in spec.dict_formats
            if dict_format is not default_dict_format
        ]
        non_default_declaration_styles = [
            declaration_style
            for declaration_style in spec.declaration_styles
            if declaration_style is not default_declaration_style
        ]
        for dict_format in non_default_dict_formats:
            for declaration_style in non_default_declaration_styles:
                seq_override = _resolve_sequence_format_override(
                    lang_cls=lang_cls,
                    declaration_style=declaration_style,
                )
                kwargs: dict[str, object] = {
                    "dict_format": dict_format,
                    "declaration_style": declaration_style,
                }
                if seq_override is not None:
                    kwargs["sequence_format"] = seq_override
                variants.append(
                    Variant(
                        name=(
                            f"{lang_name}_dict_{dict_format.name.lower()}"
                            f"_decl_{declaration_style.name.lower()}"
                        ),
                        spec=make_spec(lang_cls=lang_cls, **kwargs),
                        lang_cls=lang_cls,
                        collection_layout=literalizer.CollectionLayout.COMPACT,
                    )
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
                collection_layout=literalizer.CollectionLayout.COMPACT,
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
                collection_layout=literalizer.CollectionLayout.COMPACT,
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
                collection_layout=literalizer.CollectionLayout.COMPACT,
            )
        )
    return variants


@runtime_checkable
class _HasRecordShapeNames(Protocol):
    """Structural type for languages that expose a
    ``record_shape_names`` constructor field.

    Used by :func:`build_record_shape_names_variants` to narrow a
    generic :class:`literalizer.Language` to one with the field, without
    introspecting ``__dataclass_fields__`` or casting to ``Any``.
    """

    record_shape_names: Mapping[frozenset[str], str]


@beartype
def build_record_shape_names_variants() -> Iterable[Variant]:
    """Build ``record_shape_names`` variants for every language whose
    spec exposes a ``record_shape_names`` field and a ``RECORD``
    heterogeneous strategy.

    Bypasses :func:`make_spec` caching because the user-facing
    ``record_shape_names`` parameter is a ``Mapping``, which cannot be
    stored in the cache key's :class:`frozenset` of kwargs.
    """
    variants: list[Variant] = []
    shape_keys = frozenset({"id", "description", "is_done", "blocks"})
    custom_name = "Task"
    for lang_cls in sorted_languages():
        default_spec = make_spec(lang_cls=lang_cls)
        if not isinstance(default_spec, _HasRecordShapeNames):
            continue
        # A spec exposing ``record_shape_names`` always also exposes the
        # RECORD strategy the field configures, so ``next`` cannot miss.
        record_strategy = next(
            strategy
            for strategy in default_spec.heterogeneous_strategies
            if strategy.name == "RECORD"
        )
        spec_kwargs: dict[str, object] = {
            "heterogeneous_strategy": record_strategy,
            "record_shape_names": {shape_keys: custom_name},
        }
        # Mirror :func:`make_spec`'s ``module_name`` default (this
        # builder bypasses it): a language whose ``wrap_in_file``
        # introduces a named scope (e.g. Java's ``class {module_name}``,
        # which its CI lint host loads as ``Main``) needs the same
        # ``"main"`` name that :func:`make_spec` uses.
        if lang_cls.supports_module_name:
            spec_kwargs["module_name"] = lang_cls.module_name_case.convert(
                name="main",
            )
        spec = lang_cls(**spec_kwargs)
        variants.append(
            Variant(
                name=(f"{lang_cls.__name__}_record_shape_names_{custom_name}"),
                spec=spec,
                lang_cls=lang_cls,
                collection_layout=literalizer.CollectionLayout.COMPACT,
            )
        )
    return variants


@beartype
def build_record_unify_optional_fields_variants() -> Iterable[Variant]:
    """Build the Rust ``record_unify_optional_fields`` variant.

    Combines :attr:`Rust.record_unify_optional_fields` with the
    ``RECORD`` heterogeneous strategy so the golden case exercises the
    Option/Some/None rendering.  Only Rust currently has this knob.
    """
    default_spec = make_spec(lang_cls=Rust)
    record_strategy = next(
        strategy
        for strategy in default_spec.heterogeneous_strategies
        if strategy.name == "RECORD"
    )
    spec = make_spec(
        lang_cls=Rust,
        heterogeneous_strategy=record_strategy,
        record_unify_optional_fields=True,
    )
    return [
        Variant(
            name="Rust_record_unify_optional_fields",
            spec=spec,
            lang_cls=Rust,
            collection_layout=literalizer.CollectionLayout.COMPACT,
        )
    ]


@beartype
def build_record_nonrecord_dict_field_variants() -> Iterable[Variant]:
    """Build the Nim ``record_nonrecord_dict_field`` variant.

    Nim is the only port that *rejects* a non-record-dict (here an
    empty dict) record field under ``RECORD`` while still rendering the
    surrounding record (the other ports either reject the whole input
    earlier or widen the field to a map type), so this single-language
    variant locks in that rejection path.  See #2317 for the
    cross-language set / non-record-dict record-field decision.
    """
    default_spec = make_spec(lang_cls=Nim)
    record_strategy = next(
        strategy
        for strategy in default_spec.heterogeneous_strategies
        if strategy.name == "RECORD"
    )
    return [
        Variant(
            name="Nim_record_nonrecord_dict_field",
            spec=make_spec(
                lang_cls=Nim, heterogeneous_strategy=record_strategy
            ),
            lang_cls=Nim,
            collection_layout=literalizer.CollectionLayout.COMPACT,
        )
    ]


@beartype
def build_record_epoch_i32_overflow_variants() -> Iterable[Variant]:
    """Build a ``RECORD`` + ``EPOCH`` variant for every language whose
    spec exposes both a ``RECORD`` heterogeneous strategy and an
    ``EPOCH`` datetime format.

    A post-2038 ``datetime`` rendered as ``EPOCH`` seconds exceeds
    32-bit range, so a language whose record component for an epoch is
    a fixed-width integer must widen it (and suffix the literal) for
    the output to compile.  Driven generically off spec capabilities
    rather than naming a language so the matrix stays
    language-agnostic.
    """
    variants: list[Variant] = []
    for lang_cls in sorted_languages():
        default_spec = make_spec(lang_cls=lang_cls)
        record_strategy = next(
            (
                strategy
                for strategy in default_spec.heterogeneous_strategies
                if strategy.name == "RECORD"
            ),
            None,
        )
        epoch = next(
            (
                fmt
                for fmt in default_spec.datetime_formats
                if fmt.name == "EPOCH"
            ),
            None,
        )
        if record_strategy is None or epoch is None:
            continue
        variants.append(
            Variant(
                name=f"{lang_cls.__name__}_record_epoch_i32_overflow",
                spec=make_spec(
                    lang_cls=lang_cls,
                    heterogeneous_strategy=record_strategy,
                    datetime_format=epoch,
                ),
                lang_cls=lang_cls,
                collection_layout=literalizer.CollectionLayout.COMPACT,
            )
        )
    return variants


@beartype
def build_record_numeric_cross_variants() -> Iterable[Variant]:
    """Build ``RECORD`` x non-default numeric-formatter variants.

    For every language exposing a ``RECORD`` heterogeneous strategy,
    cross ``RECORD`` with every non-default ``integer_format``,
    ``numeric_separator`` and ``numeric_literal_suffix``.  Run against
    the ``record_wide_int`` input these lock in that the declared field
    type follows the value, not the formatted literal (issue #2306,
    follow-up to #2297; extended to Kotlin/Java/Scala by #2376): an
    integer field keeps its value-derived type however the literal is
    written, and an integer beyond the signed 64-bit range is typed to
    match its wide-integer overflow-fallback literal instead of the
    type a formatted-string inspection would infer.
    """
    axes: list[
        tuple[
            str,
            str,
            Callable[[literalizer.Language], object],
            Callable[[literalizer.Language], type[enum.Enum]],
        ]
    ] = [
        (
            "integer",
            "integer_format",
            lambda s: s.integer_format,
            lambda s: s.integer_formats,
        ),
        (
            "separator",
            "numeric_separator",
            lambda s: s.numeric_separator,
            lambda s: s.numeric_separators,
        ),
        (
            "suffix",
            "numeric_literal_suffix",
            lambda s: s.numeric_literal_suffix,
            lambda s: s.numeric_literal_suffixes,
        ),
    ]
    variants: list[Variant] = []
    for lang_cls in sorted_languages():
        spec = make_spec(lang_cls=lang_cls)
        record_strategy = next(
            (
                strategy
                for strategy in spec.heterogeneous_strategies
                if strategy.name == "RECORD"
            ),
            None,
        )
        if record_strategy is None:
            continue
        lang_name = lang_cls.__name__
        for tag, kwarg, get_default, get_formats in axes:
            default = get_default(spec)
            for fmt in get_formats(spec):
                if fmt is default:
                    continue
                variants.append(
                    Variant(
                        name=(
                            f"{lang_name}_heterogeneous_strategy_record"
                            f"_{tag}_{fmt.name.lower()}"
                        ),
                        spec=make_spec(
                            lang_cls=lang_cls,
                            heterogeneous_strategy=record_strategy,
                            **{kwarg: fmt},
                        ),
                        lang_cls=lang_cls,
                        collection_layout=literalizer.CollectionLayout.COMPACT,
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
                collection_layout=literalizer.CollectionLayout.COMPACT,
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
                collection_layout=literalizer.CollectionLayout.COMPACT,
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
        versions_cls = lang_cls.VersionFormats
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
                    collection_layout=literalizer.CollectionLayout.COMPACT,
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
                default_dict_value_type=DEFAULT_DICT_VALUE_TYPES[Python],
            ),
            lang_cls=Python,
            collection_layout=literalizer.CollectionLayout.COMPACT,
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
                collection_layout=literalizer.CollectionLayout.COMPACT,
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
                collection_layout=literalizer.CollectionLayout.COMPACT,
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
                        collection_layout=literalizer.CollectionLayout.COMPACT,
                    )
                )
    return variants


@beartype
def build_heterogeneous_strategy_datetime_cross_variants() -> list[Variant]:
    """Build cross-product variants of ``heterogeneous_strategy`` and
    ``datetime_format``.

    For every language, pair every non-default heterogeneous strategy
    with every non-default datetime format.  Covers code paths where the
    chosen heterogeneous strategy selects a variant based on the rendered
    Python type of a datetime value (e.g. Rust's ``TAGGED_ENUM`` routing
    an ``EPOCH`` datetime through the ``i64`` variant rather than a
    ``DateTime`` variant).
    """
    variants: list[Variant] = []
    for lang_cls in sorted_languages():
        spec = make_spec(lang_cls=lang_cls)
        default_strategy = spec.heterogeneous_strategy
        default_dt = spec.datetime_format
        lang_name = lang_cls.__name__
        for strategy in spec.heterogeneous_strategies:
            if strategy is default_strategy:
                continue
            for dt in spec.datetime_formats:
                if dt is default_dt:
                    continue
                variants.append(
                    Variant(
                        name=(
                            f"{lang_name}"
                            f"_heterogeneous_strategy_{strategy.name.lower()}"
                            f"_datetime_{dt.name.lower()}"
                        ),
                        spec=make_spec(
                            lang_cls=lang_cls,
                            heterogeneous_strategy=strategy,
                            datetime_format=dt,
                        ),
                        lang_cls=lang_cls,
                        collection_layout=literalizer.CollectionLayout.COMPACT,
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
                            collection_layout=literalizer.CollectionLayout.COMPACT,
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
        "scalar_time",
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
                collection_layout=literalizer.CollectionLayout.COMPACT,
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
        collection_layout=literalizer.CollectionLayout.COMPACT,
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
        collection_layout=literalizer.CollectionLayout.COMPACT,
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
    suffix: str


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
    "integer_width_strategy": _SimpleAxis(
        category="integer_width_strategy",
        kwarg="integer_width_strategy",
        get_default=lambda s: s.integer_width_strategy,
        get_formats=lambda s: s.integer_width_strategies,
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


@runtime_checkable
class _HasBoolFormat(Protocol):
    """Structural type for languages that expose a ``bool_format``
    constructor field.

    Used by :func:`build_bool_format_variants` to narrow a generic
    :class:`literalizer.Language` to one with the field, without
    hard-coding the (currently single) language that has it.
    """

    bool_format: enum.Enum


@beartype
def build_bool_format_variants() -> Iterable[Variant]:
    """Build ``bool_format`` variants for every language whose spec
    exposes the field.  Equivalent to a :data:`_SIMPLE_AXES` entry, but
    discovered via the :class:`_HasBoolFormat` protocol so languages
    without the field do not need a stub enum.
    """
    variants: list[Variant] = []
    for lang_cls in sorted_languages():
        default_spec = make_spec(lang_cls=lang_cls)
        if not isinstance(default_spec, _HasBoolFormat):
            continue
        default_format = default_spec.bool_format
        for fmt in type(default_format):
            if fmt is default_format:
                continue
            variants.append(
                Variant(
                    name=(
                        f"{lang_cls.__name__}_bool_format_{fmt.name.lower()}"
                    ),
                    spec=make_spec(lang_cls=lang_cls, bool_format=fmt),
                    lang_cls=lang_cls,
                    collection_layout=literalizer.CollectionLayout.COMPACT,
                )
            )
    return variants


_COMPLEX_BUILDERS: dict[str, Callable[[], Iterable[Variant]]] = {
    "collection_layout": build_collection_layout_variants,
    "declaration_style": _build_declaration_style_variants,
    "default_set_element_type": build_default_set_element_type_variants,
    "default_sequence_element_type": (
        build_default_sequence_element_type_variants
    ),
    "json_type": build_json_type_variants,
    "default_dict_value_type": build_default_dict_value_type_variants,
    "empty_dict_key": build_empty_dict_key_variants,
    "default_dict_key_type": build_default_dict_key_type_variants,
    "default_ordered_map_value_type": (
        build_default_ordered_map_value_type_variants
    ),
    "statement_terminator_style_decl": (
        build_statement_terminator_style_decl_variants
    ),
    "sequence_decl": build_sequence_decl_variants,
    "set_decl": build_set_decl_variants,
    "dict_decl": build_dict_decl_variants,
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
    "heterogeneous_strategy_datetime_cross": (
        build_heterogeneous_strategy_datetime_cross_variants
    ),
    "type_name": build_type_name_variants,
    "constructor_prefix": build_constructor_prefix_variants,
    "constructor_name": build_constructor_name_variants,
    "c_field_name": build_c_field_name_variants,
    "heterogeneous_value_enum_name": build_heterogeneous_value_name_variants,
    "record_shape_names": build_record_shape_names_variants,
    "heterogeneous_value_union_name": (
        build_heterogeneous_value_union_name_variants
    ),
    "heterogeneous_value_variant_name": (
        build_heterogeneous_value_variant_name_variants
    ),
    "record_unify_optional_fields": (
        build_record_unify_optional_fields_variants
    ),
    "record_nonrecord_dict_field": (
        build_record_nonrecord_dict_field_variants
    ),
    "record_epoch_i32_overflow": build_record_epoch_i32_overflow_variants,
    "record_numeric_cross": build_record_numeric_cross_variants,
    "language_version": build_language_version_variants,
    "language_version_cross_dict_type": (
        build_language_version_cross_dict_type_variants
    ),
    "bool_format": build_bool_format_variants,
}


@beartype
def _ci(*, case_dir_name: str, suffix: str) -> CaseInput:
    """Shorthand for :class:`CaseInput` to keep the table compact."""
    return CaseInput(case_dir_name=case_dir_name, suffix=suffix)


INT_INPUTS: tuple[CaseInput, ...] = (
    _ci(case_dir_name="int_list", suffix=""),
    _ci(case_dir_name="int_list_large", suffix="_large"),
    _ci(case_dir_name="int_list_with_zero", suffix="_zero"),
    _ci(case_dir_name="scalar_int", suffix=""),
    _ci(case_dir_name="scalar_int_large", suffix=""),
)

FLOAT_INPUTS: tuple[CaseInput, ...] = (
    _ci(case_dir_name="float_list", suffix=""),
    _ci(case_dir_name="float_scientific_notation", suffix="_s"),
    _ci(case_dir_name="float_special_values", suffix="_v"),
    _ci(case_dir_name="nested_float_list", suffix="_n"),
    _ci(case_dir_name="scalar_float", suffix=""),
)

BASIC_COLLECTIONS: tuple[CaseInput, ...] = (
    _ci(case_dir_name="simple_sequence", suffix=""),
    _ci(case_dir_name="simple_dict", suffix="_dict"),
    _ci(case_dir_name="set", suffix="_set"),
)

ADT_INPUTS: tuple[CaseInput, ...] = (
    _ci(case_dir_name="simple_dict", suffix=""),
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
        ("heterogeneous_list_with_string", ""),
        ("dict_with_list_value", "_list_val"),
        ("multiline_sibling_list_widening", "_sibling_widening"),
        ("record_basic", ""),
        ("record_pure_scalars", ""),
        ("record_nested_container", ""),
        ("record_sequence", ""),
        ("record_two_shapes", ""),
        ("record_nested_record", ""),
        ("record_list_of_records", ""),
        ("tuple_record_field", ""),
        ("tuple_record_seq_sibling", ""),
        ("tuple_int_key_dict_value", ""),
        ("tuple_top_level", ""),
        ("tuple_record_sequence", ""),
        ("tuple_pair_record_field", ""),
        ("tuple_pair_top_level", ""),
        ("tuple_triple_record_field", ""),
        ("tuple_triple_top_level", ""),
    )
)

# The ``heterogeneous_strategy`` axis additionally covers
# ``int_key_dict`` and ``empty_dict`` so the RECORD strategy walks the
# two non-record-eligible dict shapes through ``record_shape_for_dict``:
# ``int_key_dict`` exercises the non-string-key branch and ``empty_dict``
# exercises the empty-dict branch.  Languages that cannot represent
# integer keys raise ``UnrepresentableInputError`` and are skipped; the
# rest render both as plain maps, identical to the default output.
HETEROGENEOUS_STRATEGY_INPUTS: tuple[CaseInput, ...] = (
    *HETEROGENEOUS_INPUTS,
    _ci(case_dir_name="int_key_dict", suffix=""),
    _ci(case_dir_name="empty_dict", suffix=""),
)

DICT_FORMAT_INPUTS: tuple[CaseInput, ...] = (
    _ci(case_dir_name="simple_dict", suffix=""),
    _ci(case_dir_name="dict_with_list_value", suffix="_list_val"),
)

DEFAULT_DICT_INPUTS: tuple[CaseInput, ...] = (
    _ci(case_dir_name="empty_dict", suffix=""),
    _ci(case_dir_name="simple_dict", suffix=""),
)

_NUMERIC_INPUTS: tuple[CaseInput, ...] = (
    _ci(case_dir_name="int_list", suffix=""),
    _ci(case_dir_name="int_list_large", suffix="_large"),
    _ci(case_dir_name="int_list_with_zero", suffix="_zero"),
    _ci(case_dir_name="scalar_int", suffix=""),
    _ci(case_dir_name="scalar_int_large", suffix=""),
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
        _ci(case_dir_name="scalar_date", suffix=""),
        _ci(case_dir_name="date_list", suffix=""),
        _ci(case_dir_name="date_set", suffix=""),
    ),
    "datetime": (
        _ci(case_dir_name="scalar_datetime", suffix=""),
        _ci(case_dir_name="scalar_datetime_naive", suffix="_naive"),
        _ci(case_dir_name="scalar_datetime_non_utc", suffix="_non_utc"),
        _ci(case_dir_name="datetime_list", suffix=""),
    ),
    "sequence": (
        _ci(case_dir_name="simple_sequence", suffix=""),
        _ci(case_dir_name="pair_sequence", suffix="_pair"),
        _ci(case_dir_name="triple_sequence", suffix="_triple"),
        _ci(case_dir_name="simple_sequence", suffix="_varname"),
        _ci(case_dir_name="float_list", suffix="_float"),
        _ci(case_dir_name="null_list", suffix="_null"),
        _ci(case_dir_name="binary_list", suffix="_binary"),
    ),
    "set": (
        _ci(case_dir_name="set", suffix=""),
        _ci(case_dir_name="int_set", suffix=""),
        _ci(case_dir_name="mixed_set", suffix=""),
        _ci(case_dir_name="empty_set", suffix=""),
        _ci(case_dir_name="set_mixed_int_widths", suffix=""),
    ),
    "default_set_element_type": (
        _ci(case_dir_name="empty_set", suffix=""),
        _ci(case_dir_name="set", suffix=""),
    ),
    "default_sequence_element_type": (
        _ci(case_dir_name="empty_sequence", suffix=""),
        _ci(case_dir_name="simple_sequence", suffix=""),
    ),
    "json_type": (
        _ci(case_dir_name="dict_with_list_value", suffix=""),
        _ci(case_dir_name="nested_mixed_inner", suffix="_nested_mixed"),
        _ci(case_dir_name="dates", suffix="_dates"),
        _ci(case_dir_name="dict_with_nulls", suffix="_nulls"),
        _ci(case_dir_name="date_set", suffix="_date_set"),
        _ci(case_dir_name="ordered_map", suffix="_ordered_map"),
        _ci(case_dir_name="scalar_datetime_naive", suffix="_datetime_naive"),
        _ci(case_dir_name="binary", suffix="_binary"),
        _ci(case_dir_name="scalar_float", suffix="_float"),
        _ci(case_dir_name="scalar_time", suffix="_time"),
        _ci(case_dir_name="scalar_int_large", suffix="_long"),
        _ci(case_dir_name="scalar_int_very_large", suffix="_bigint"),
        _ci(case_dir_name="bool_list", suffix="_bool_list"),
    ),
    "default_dict_value_type": DEFAULT_DICT_INPUTS,
    "default_dict_key_type": DEFAULT_DICT_INPUTS,
    "empty_dict_key": (_ci(case_dir_name="simple_dict", suffix=""),),
    "default_ordered_map_value_type": (
        _ci(case_dir_name="ordered_map", suffix=""),
    ),
    "comment": (_ci(case_dir_name="comments", suffix=""),),
    "type_hints": tuple(
        _ci(case_dir_name=d, suffix="")
        for d in (
            "type_hints",
            "scalar_date",
            "scalar_datetime",
            # ``scalar_time`` pins the ``case datetime.time():`` scalar
            # type-hint arm under non-default (``ALWAYS``)
            # ``variable_type_hints``, replacing the
            # ``test_datetime_time_always_type_hint_renders`` shim
            # (issue #2518).  The Python-only ``_structural_type_id``
            # time arm cannot ride this all-languages axis (it would
            # force non-compiling Kotlin nested-time-list output); it
            # keeps a focused pytest test instead.
            "scalar_time",
            "binary",
            "mixed_type_dicts_in_sequence",
            "empty_dicts_in_sequence",
            "float_list",
            "int_list",
            "empty_list",
            "int_set",
            "mixed_set",
            "empty_set",
            "set_mixed_int_widths",
            "mixed_number_list",
            "nested_sequence",
            "dict_with_list_value",
            "ordered_map_in_sequence",
        )
    ),
    "type_hints_cross": tuple(
        _ci(case_dir_name=d, suffix="")
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
        _ci(case_dir_name=d, suffix="")
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
            "time_dict",
            "binary",
            "set_mixed_int_widths",
        )
    ),
    "dict_format": DICT_FORMAT_INPUTS,
    "dict_entry_style": DICT_FORMAT_INPUTS,
    "float_format": FLOAT_INPUTS,
    "integer_format": INT_INPUTS,
    "numeric_literal_suffix": _NUMERIC_INPUTS,
    "numeric_separator": _NUMERIC_INPUTS,
    "string_format": (
        _ci(case_dir_name="string_list", suffix=""),
        _ci(case_dir_name="string_with_backslash", suffix=""),
        _ci(case_dir_name="simple_dict", suffix="_dict"),
        _ci(case_dir_name="binary", suffix="_binary"),
        _ci(case_dir_name="scalar_string", suffix=""),
        _ci(case_dir_name="time_list", suffix="_time"),
        # Pins the non-ASCII branch of each non-default string format:
        # Perl ``DOUBLE_UTF8`` adds ``use utf8;`` and emits literal
        # characters (#2600), and every other multi-format language's
        # alternate quoting style is exercised against the same input.
        _ci(case_dir_name="string_unicode", suffix=""),
    ),
    "string_format_date_cross": (_ci(case_dir_name="scalar_date", suffix=""),),
    "string_format_datetime_cross": (
        _ci(case_dir_name="scalar_datetime", suffix="_dt"),
    ),
    "bytes_format": (_ci(case_dir_name="binary", suffix=""),),
    "trailing_comma": BASIC_COLLECTIONS,
    "statement_terminator_style": BASIC_COLLECTIONS,
    "collection_layout": tuple(
        _ci(case_dir_name=d, suffix="")
        for d in (
            "dict_with_list_value",
            "nested",
            "nested_mixed_set",
            "multiline_sibling_list_widening",
        )
    ),
    "statement_terminator_style_decl": (
        _ci(case_dir_name="simple_sequence", suffix=""),
    ),
    "sequence_decl": (
        _ci(case_dir_name="int_list", suffix=""),
        # A one-element list pins the single-element-tuple trailing
        # comma in both the type annotation and the value (e.g. Rust
        # ``static my_data: (i32,) = (1,);``); a multi-element input
        # cannot exercise that carve-out.
        _ci(case_dir_name="int_list_single", suffix=""),
    ),
    "set_decl": (_ci(case_dir_name="set_mixed_int_widths", suffix=""),),
    "dict_decl": (_ci(case_dir_name="int_key_dict", suffix=""),),
    "type_name": ADT_INPUTS,
    "constructor_prefix": ADT_INPUTS,
    "numeric_style": (
        _ci(case_dir_name="int_list", suffix=""),
        _ci(case_dir_name="int_list_large", suffix="_large"),
        _ci(case_dir_name="int_list_with_zero", suffix="_zero"),
        _ci(case_dir_name="float_list", suffix=""),
        _ci(case_dir_name="float_special_values", suffix=""),
        _ci(case_dir_name="mixed_number_list", suffix=""),
        _ci(case_dir_name="scalars", suffix=""),
    ),
    "c_field_name": (
        _ci(case_dir_name="simple_dict", suffix=""),
        _ci(case_dir_name="simple_sequence", suffix=""),
    ),
    "constructor_name": (_ci(case_dir_name="simple_dict", suffix=""),),
    "heterogeneous_strategy": (
        *HETEROGENEOUS_STRATEGY_INPUTS,
        # ``heterogeneous_time_string`` carries a time and a string in
        # one list to pin the ``datetime.time`` arm of each language's
        # heterogeneous-variant signature builder under its non-default
        # wrap-as-variant strategies (Rust tagged enum, Dhall union
        # type, Nim object variant).  It replaces the
        # ``test_datetime_time_heterogeneous_variant_renders`` shim
        # (issue #2518).
        _ci(case_dir_name="heterogeneous_time_string", suffix=""),
    ),
    "heterogeneous_strategy_datetime_cross": (
        _ci(case_dir_name="dict_all_scalar_types", suffix=""),
    ),
    "heterogeneous_value_enum_name": HETEROGENEOUS_INPUTS,
    "record_shape_names": (
        _ci(case_dir_name="record_named_shape", suffix=""),
        _ci(case_dir_name="record_named_nested_record", suffix=""),
    ),
    "heterogeneous_value_union_name": HETEROGENEOUS_INPUTS,
    "heterogeneous_value_variant_name": HETEROGENEOUS_INPUTS,
    "record_unify_optional_fields": (
        _ci(case_dir_name="record_optional_unify", suffix=""),
    ),
    "record_nonrecord_dict_field": (
        _ci(case_dir_name="record_nonrecord_dict_field", suffix=""),
    ),
    "record_epoch_i32_overflow": (
        _ci(case_dir_name="record_epoch_datetime_i32_overflow", suffix=""),
    ),
    "record_numeric_cross": (_ci(case_dir_name="record_wide_int", suffix=""),),
    "integer_width_strategy": (
        _ci(case_dir_name="record_wide_int", suffix=""),
        _ci(case_dir_name="int_list", suffix=""),
        _ci(case_dir_name="dict_wide_int_key", suffix=""),
    ),
    "language_version": tuple(
        _ci(case_dir_name=case_dir_name, suffix="")
        for case_dir_name in dict.fromkeys(
            case_dir_name
            for case_dir_name, _ in discover_cases(cases_dir=_CASES_DIR)
        )
    ),
    "language_version_cross_dict_type": (
        _ci(case_dir_name="empty_dict", suffix=""),
        _ci(case_dir_name="empty_ordered_map", suffix=""),
    ),
    "bool_format": (
        _ci(case_dir_name="scalar_bool", suffix=""),
        _ci(case_dir_name="bool_list", suffix=""),
        _ci(case_dir_name="nested_bool_list", suffix=""),
    ),
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
                    variable_form=wrap_variable_form(),
                )
                for ci in inputs
                if not (
                    ci.case_dir_name in special_float_cases
                    and not variant.lang_cls.supports_special_floats
                )
            )
    cases.extend(build_modifier_variant_cases())
    cases.extend(
        (
            VariantCase(
                variant_name="Rust_json_type_serde_json_value_combined",
                variant=Variant(
                    name="Rust_json_type_serde_json_value_combined",
                    spec=make_spec(
                        lang_cls=Rust,
                        json_type=Rust.json_types.SERDE_JSON_VALUE,
                        declaration_style=Rust.declaration_styles.LET_MUT,
                    ),
                    lang_cls=Rust,
                    collection_layout=literalizer.CollectionLayout.COMPACT,
                ),
                case_dir_name="dict_with_list_value",
                variable_form=literalizer.BothVariableForms(name="my_data"),
            ),
            VariantCase(
                variant_name="Rust_json_type_serde_json_value_lazy_static",
                variant=Variant(
                    name="Rust_json_type_serde_json_value_lazy_static",
                    spec=make_spec(
                        lang_cls=Rust,
                        json_type=Rust.json_types.SERDE_JSON_VALUE,
                        declaration_style=Rust.declaration_styles.LAZY_STATIC,
                    ),
                    lang_cls=Rust,
                    collection_layout=literalizer.CollectionLayout.COMPACT,
                ),
                case_dir_name="dict_with_list_value",
                variable_form=wrap_variable_form(),
            ),
            VariantCase(
                variant_name="Crystal_json_type_json_any_combined",
                variant=Variant(
                    name="Crystal_json_type_json_any_combined",
                    spec=make_spec(
                        lang_cls=Crystal,
                        json_type=Crystal.json_types.JSON_ANY,
                    ),
                    lang_cls=Crystal,
                    collection_layout=literalizer.CollectionLayout.COMPACT,
                ),
                case_dir_name="dict_with_list_value",
                variable_form=literalizer.BothVariableForms(name="my_data"),
            ),
            VariantCase(
                variant_name="Java_json_type_jackson_json_node_combined",
                variant=Variant(
                    name="Java_json_type_jackson_json_node_combined",
                    spec=make_spec(
                        lang_cls=Java,
                        json_type=Java.json_types.JACKSON_JSON_NODE,
                    ),
                    lang_cls=Java,
                    collection_layout=literalizer.CollectionLayout.COMPACT,
                ),
                case_dir_name="dict_with_list_value",
                variable_form=literalizer.BothVariableForms(name="my_data"),
            ),
            VariantCase(
                variant_name="Scala_json_type_circe_combined",
                variant=Variant(
                    name="Scala_json_type_circe_combined",
                    spec=make_spec(
                        lang_cls=Scala,
                        json_type=Scala.json_types.CIRCE,
                        declaration_style=Scala.declaration_styles.VAR,
                    ),
                    lang_cls=Scala,
                    collection_layout=literalizer.CollectionLayout.COMPACT,
                ),
                case_dir_name="dict_with_list_value",
                variable_form=literalizer.BothVariableForms(name="my_data"),
            ),
            VariantCase(
                variant_name="CSharp_json_type_json_node_combined",
                variant=Variant(
                    name="CSharp_json_type_json_node_combined",
                    spec=make_spec(
                        lang_cls=CSharp,
                        json_type=CSharp.json_types.SYSTEM_TEXT_JSON_NODE,
                    ),
                    lang_cls=CSharp,
                    collection_layout=literalizer.CollectionLayout.COMPACT,
                ),
                case_dir_name="dict_with_list_value",
                variable_form=literalizer.BothVariableForms(name="my_data"),
            ),
            VariantCase(
                variant_name="Nim_json_type_json_node_combined",
                variant=Variant(
                    name="Nim_json_type_json_node_combined",
                    spec=make_spec(
                        lang_cls=Nim,
                        json_type=Nim.json_types.JSON_NODE,
                    ),
                    lang_cls=Nim,
                    collection_layout=literalizer.CollectionLayout.COMPACT,
                ),
                case_dir_name="dict_with_list_value",
                variable_form=literalizer.BothVariableForms(name="my_data"),
            ),
            VariantCase(
                variant_name="Zig_json_type_std_json_value_combined",
                variant=Variant(
                    name="Zig_json_type_std_json_value_combined",
                    spec=make_spec(
                        lang_cls=Zig,
                        json_type=Zig.json_types.STD_JSON_VALUE,
                        declaration_style=Zig.declaration_styles.VAR,
                    ),
                    lang_cls=Zig,
                    collection_layout=literalizer.CollectionLayout.COMPACT,
                ),
                case_dir_name="dict_with_list_value",
                variable_form=literalizer.BothVariableForms(name="my_data"),
            ),
            VariantCase(
                variant_name="Haskell_json_type_aeson_value_existing",
                variant=Variant(
                    name="Haskell_json_type_aeson_value_existing",
                    spec=make_spec(
                        lang_cls=Haskell,
                        json_type=Haskell.json_types.AESON_VALUE,
                    ),
                    lang_cls=Haskell,
                    collection_layout=literalizer.CollectionLayout.COMPACT,
                ),
                case_dir_name="dict_with_list_value",
                variable_form=literalizer.ExistingVariable(name="my_data"),
            ),
            VariantCase(
                variant_name="OCaml_json_type_yojson_safe_t_existing",
                variant=Variant(
                    name="OCaml_json_type_yojson_safe_t_existing",
                    spec=make_spec(
                        lang_cls=OCaml,
                        json_type=OCaml.json_types.YOJSON_SAFE_T,
                    ),
                    lang_cls=OCaml,
                    collection_layout=literalizer.CollectionLayout.COMPACT,
                ),
                case_dir_name="dict_with_list_value",
                variable_form=literalizer.ExistingVariable(name="my_data"),
            ),
            # Covers the ``false_literal`` cached property on OCaml
            # under ``YOJSON_SAFE_T``: none of the shared
            # ``VARIANT_CASES["json_type"]`` inputs contain a ``False``
            # value, so the coverage gate flags the false-literal arm
            # otherwise.
            VariantCase(
                variant_name="OCaml_json_type_yojson_safe_t_bool_list",
                variant=Variant(
                    name="OCaml_json_type_yojson_safe_t_bool_list",
                    spec=make_spec(
                        lang_cls=OCaml,
                        json_type=OCaml.json_types.YOJSON_SAFE_T,
                    ),
                    lang_cls=OCaml,
                    collection_layout=literalizer.CollectionLayout.COMPACT,
                ),
                case_dir_name="bool_list",
                variable_form=literalizer.NewVariable(name="my_data"),
            ),
            VariantCase(
                variant_name="Kotlin_json_type_kotlinx_json_element_combined",
                variant=Variant(
                    name="Kotlin_json_type_kotlinx_json_element_combined",
                    spec=make_spec(
                        lang_cls=Kotlin,
                        json_type=Kotlin.json_types.KOTLINX_JSON_ELEMENT,
                        declaration_style=Kotlin.declaration_styles.VAR,
                    ),
                    lang_cls=Kotlin,
                    collection_layout=literalizer.CollectionLayout.COMPACT,
                ),
                case_dir_name="dict_with_list_value",
                variable_form=literalizer.BothVariableForms(name="my_data"),
            ),
            VariantCase(
                variant_name="Cpp_json_type_nlohmann_json_combined",
                variant=Variant(
                    name="Cpp_json_type_nlohmann_json_combined",
                    spec=make_spec(
                        lang_cls=Cpp,
                        json_type=Cpp.json_types.NLOHMANN_JSON,
                    ),
                    lang_cls=Cpp,
                    collection_layout=literalizer.CollectionLayout.COMPACT,
                ),
                case_dir_name="dict_with_list_value",
                variable_form=literalizer.BothVariableForms(name="my_data"),
            ),
            VariantCase(
                variant_name="Gleam_json_type_gleam_json_json_datetime_epoch",
                variant=Variant(
                    name="Gleam_json_type_gleam_json_json_datetime_epoch",
                    spec=make_spec(
                        lang_cls=Gleam,
                        json_type=Gleam.json_types.GLEAM_JSON_JSON,
                        datetime_format=Gleam.datetime_formats.EPOCH,
                    ),
                    lang_cls=Gleam,
                    collection_layout=literalizer.CollectionLayout.COMPACT,
                ),
                case_dir_name="scalar_datetime_naive",
                variable_form=literalizer.NewVariable(name="my_data"),
            ),
            VariantCase(
                variant_name="Gleam_json_type_gleam_json_json_bytes_base64",
                variant=Variant(
                    name="Gleam_json_type_gleam_json_json_bytes_base64",
                    spec=make_spec(
                        lang_cls=Gleam,
                        json_type=Gleam.json_types.GLEAM_JSON_JSON,
                        bytes_format=Gleam.bytes_formats.BASE64,
                    ),
                    lang_cls=Gleam,
                    collection_layout=literalizer.CollectionLayout.COMPACT,
                ),
                case_dir_name="binary",
                variable_form=literalizer.NewVariable(name="my_data"),
            ),
            VariantCase(
                variant_name="Gleam_json_type_gleam_json_json_combined",
                variant=Variant(
                    name="Gleam_json_type_gleam_json_json_combined",
                    spec=make_spec(
                        lang_cls=Gleam,
                        json_type=Gleam.json_types.GLEAM_JSON_JSON,
                    ),
                    lang_cls=Gleam,
                    collection_layout=literalizer.CollectionLayout.COMPACT,
                ),
                case_dir_name="dict_with_list_value",
                variable_form=literalizer.BothVariableForms(name="my_data"),
            ),
            VariantCase(
                variant_name="Nim_json_type_json_node_let",
                variant=Variant(
                    name="Nim_json_type_json_node_let",
                    spec=make_spec(
                        lang_cls=Nim,
                        json_type=Nim.json_types.JSON_NODE,
                        declaration_style=Nim.declaration_styles.LET,
                    ),
                    lang_cls=Nim,
                    collection_layout=literalizer.CollectionLayout.COMPACT,
                ),
                case_dir_name="dict_with_list_value",
                variable_form=wrap_variable_form(),
            ),
            # Covers the ``false_literal`` cached property on Elm under
            # ``JSON_ENCODE_VALUE``: none of the shared
            # ``VARIANT_CASES["json_type"]`` inputs contain a ``False``
            # value.
            VariantCase(
                variant_name="Elm_json_type_json_encode_value_bool_list",
                variant=Variant(
                    name="Elm_json_type_json_encode_value_bool_list",
                    spec=make_spec(
                        lang_cls=Elm,
                        json_type=Elm.json_types.JSON_ENCODE_VALUE,
                    ),
                    lang_cls=Elm,
                    collection_layout=literalizer.CollectionLayout.COMPACT,
                ),
                case_dir_name="bool_list",
                variable_form=literalizer.NewVariable(name="my_data"),
            ),
            # Covers the negative-numeric paren-wrap arm of
            # ``_format_elm_json_with_ctor`` (positive numerals pass
            # through bare; the shared ``json_type`` inputs only carry
            # positives).
            VariantCase(
                variant_name=("Elm_json_type_json_encode_value_negative_int"),
                variant=Variant(
                    name=("Elm_json_type_json_encode_value_negative_int"),
                    spec=make_spec(
                        lang_cls=Elm,
                        json_type=Elm.json_types.JSON_ENCODE_VALUE,
                    ),
                    lang_cls=Elm,
                    collection_layout=literalizer.CollectionLayout.COMPACT,
                ),
                case_dir_name="scalar_int_negative_large",
                variable_form=literalizer.NewVariable(name="my_data"),
            ),
            # Covers the ``inf``/``nan`` arms of the JSON-mode float
            # formatter on Elm.
            VariantCase(
                variant_name=(
                    "Elm_json_type_json_encode_value_float_specials"
                ),
                variant=Variant(
                    name=("Elm_json_type_json_encode_value_float_specials"),
                    spec=make_spec(
                        lang_cls=Elm,
                        json_type=Elm.json_types.JSON_ENCODE_VALUE,
                    ),
                    lang_cls=Elm,
                    collection_layout=literalizer.CollectionLayout.COMPACT,
                ),
                case_dir_name="float_special_values",
                variable_form=literalizer.NewVariable(name="my_data"),
            ),
            # Covers ``bytes_format=BASE64`` under JSON mode (the
            # default JSON variant uses ``HEX``).
            VariantCase(
                variant_name=("Elm_json_type_json_encode_value_base64"),
                variant=Variant(
                    name=("Elm_json_type_json_encode_value_base64"),
                    spec=make_spec(
                        lang_cls=Elm,
                        json_type=Elm.json_types.JSON_ENCODE_VALUE,
                        bytes_format=Elm.bytes_formats.BASE64,
                    ),
                    lang_cls=Elm,
                    collection_layout=literalizer.CollectionLayout.COMPACT,
                ),
                case_dir_name="binary",
                variable_form=literalizer.NewVariable(name="my_data"),
            ),
            # Covers ``datetime_format=EPOCH`` under JSON mode (datetime
            # rendered as ``Json.Encode.int`` of Unix epoch seconds).
            VariantCase(
                variant_name=("Elm_json_type_json_encode_value_epoch"),
                variant=Variant(
                    name=("Elm_json_type_json_encode_value_epoch"),
                    spec=make_spec(
                        lang_cls=Elm,
                        json_type=Elm.json_types.JSON_ENCODE_VALUE,
                        datetime_format=Elm.datetime_formats.EPOCH,
                    ),
                    lang_cls=Elm,
                    collection_layout=literalizer.CollectionLayout.COMPACT,
                ),
                case_dir_name="scalar_datetime",
                variable_form=literalizer.NewVariable(name="my_data"),
            ),
        )
    )
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
