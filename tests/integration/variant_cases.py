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
from literalizer.exceptions import IncompatibleFormatsError
from literalizer.languages import ALL_LANGUAGES, Cpp

from .case_discovery import cases_with_special_floats
from .language_specs import (
    find_redefinition_styles,
    make_spec,
    sorted_languages,
)
from .variant_inputs import AXIS_INPUTS
from .variant_metadata_builders import (
    build_collection_layout_variants,
    build_dhall_nested_map_widening_variants,
    build_empty_map_narrowing_variants,
    build_language_version_cross_dict_type_variants,
    build_modifier_variant_cases,
    build_nested_map_widening_variants,
    build_record_field_type_split_variants,
    build_record_keyword_field_variants,
    build_record_nonrecord_dict_field_variants,
    build_record_quoted_field_variants,
    build_record_unify_optional_fields_variants,
)
from .variant_types import (
    Variant,
    VariantCase,
    enum_member_by_name,
    wrap_variable_form,
)

__all__ = ("Variant", "wrap_variable_form")

_CASES_DIR = Path(__file__).parent / "cases"


_enum_member_by_name = enum_member_by_name


def _check_default_type_variants() -> None:
    """Validate language-owned default-type variant metadata."""
    for lang_cls in ALL_LANGUAGES:
        supported_fields = {
            field_name
            for field_name, supported in (
                (
                    "default_set_element_type",
                    lang_cls.supports_default_set_element_type,
                ),
                (
                    "default_sequence_element_type",
                    lang_cls.supports_default_sequence_element_type,
                ),
                (
                    "default_dict_value_type",
                    lang_cls.supports_default_dict_value_type,
                ),
                (
                    "default_dict_key_type",
                    lang_cls.supports_default_dict_key_type,
                ),
                (
                    "default_ordered_map_value_type",
                    lang_cls.supports_default_ordered_map_value_type,
                ),
            )
            if supported
        }
        configured_fields = set(lang_cls.non_default_kwargs) & {
            "default_set_element_type",
            "default_sequence_element_type",
            "default_dict_value_type",
            "default_dict_key_type",
            "default_ordered_map_value_type",
        }
        assert configured_fields == supported_fields  # noqa: S101
        default_spec = make_spec(lang_cls=lang_cls)
        for field_name in configured_fields:
            override = lang_cls.non_default_kwargs[field_name]
            variant_spec = make_spec(
                lang_cls=lang_cls,
                **{field_name: override},
            )
            assert variant_spec != default_spec, (  # noqa: S101
                f"{lang_cls.__name__}.{field_name}={override!r}"
            )


_check_default_type_variants()


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
                    fixture_prefix="",
                    record_null_substitutions=None,
                    collection_layout=literalizer.CollectionLayout.COMPACT,
                )
            )
    return variants


@beartype
def _build_default_type_variants(
    *,
    field_name: str,
    variant_suffix: str,
) -> list[Variant]:
    """Build one configurable collection-default type axis."""
    return [
        Variant(
            name=f"{lang_cls.__name__}_{variant_suffix}",
            spec=make_spec(lang_cls=lang_cls, **{field_name: type_name}),
            lang_cls=lang_cls,
            fixture_prefix="",
            record_null_substitutions=None,
            collection_layout=literalizer.CollectionLayout.COMPACT,
        )
        for lang_cls in sorted_languages()
        if (type_name := lang_cls.non_default_kwargs.get(field_name))
        is not None
    ]


@beartype
def build_default_set_element_type_variants() -> Iterable[Variant]:
    """Build default-set-type variants for languages that support it."""
    return _build_default_type_variants(
        field_name="default_set_element_type",
        variant_suffix="default_set_element_type_string",
    )


@beartype
def build_default_sequence_element_type_variants() -> Iterable[Variant]:
    """Build default-sequence-type variants for supported languages."""
    return _build_default_type_variants(
        field_name="default_sequence_element_type",
        variant_suffix="default_sequence_element_type_string",
    )


@runtime_checkable
class _HasJsonType(Protocol):
    """Structural type for languages whose spec exposes a ``json_type``
    value field, alongside the ``json_types`` enum that configures it.

    Languages without a JSON value-type representation omit the
    ``json_type`` constructor field entirely (their ``json_types`` enum
    is empty), so the ``isinstance`` check skips them without reflection.
    """

    json_type: enum.Enum | None
    json_types: type[enum.Enum]


@runtime_checkable
class _HasBytesFormat(Protocol):
    """Structural type for specs exposing a configured bytes format."""

    bytes_format: enum.Enum


@beartype
def _configured_bytes_format(spec: literalizer.Language) -> enum.Enum:
    """Return the configured enum despite JSON formatter overrides."""
    assert isinstance(spec, _HasBytesFormat)  # noqa: S101
    return spec.bytes_format


@beartype
def build_json_type_variants() -> Iterable[Variant]:
    """Build JSON value-type variants for every language whose spec
    exposes a ``json_type`` field.

    For each such language, emit a variant for every ``json_type``
        setting other than its default.  The available settings are ``None``
    (the narrow, no-JSON-type rendering) together with each member of the
    language's ``json_types`` enum.  Every current language offers a
    single non-default setting: the JSON-capable languages default to
    ``None`` and gain one JSON value type, while D defaults to its only
    JSON value type and narrows back to ``None``.
    """
    variants: list[Variant] = []
    for lang_cls in sorted_languages():
        spec = make_spec(lang_cls=lang_cls)
        if not isinstance(spec, _HasJsonType):
            continue
        default_json_type = spec.json_type
        json_type_options: list[enum.Enum | None] = [None, *spec.json_types]
        for json_type in json_type_options:
            if json_type is default_json_type:
                continue
            suffix = (
                "narrow"
                if json_type is None
                else (
                    lang_cls.json_type_variant_name_suffix
                    or json_type.name.lower()
                )
            )
            variants.append(
                Variant(
                    name=f"{lang_cls.__name__}_json_type_{suffix}",
                    spec=make_spec(lang_cls=lang_cls, json_type=json_type),
                    lang_cls=lang_cls,
                    fixture_prefix="",
                    record_null_substitutions=None,
                    collection_layout=literalizer.CollectionLayout.COMPACT,
                )
            )
    return variants


def _check_json_type_variants() -> None:
    """Validate JSON value-type variant coverage at import time.

    :func:`build_json_type_variants` must emit a variant for exactly the
    languages whose spec exposes a ``json_type`` field, so a future
    JSON-capable language cannot land without coverage.  Every entry in
    A language-owned filename suffix must belong to such a language and
    actually differ from the member name it renames; either kind of drift
    would silently break variant coverage or leave a dead override.
    """
    supported = {
        lang_cls
        for lang_cls in ALL_LANGUAGES
        if isinstance(make_spec(lang_cls=lang_cls), _HasJsonType)
    }
    covered = {variant.lang_cls for variant in build_json_type_variants()}
    assert covered == supported  # noqa: S101
    suffix_overrides = {
        lang_cls: lang_cls.json_type_variant_name_suffix
        for lang_cls in ALL_LANGUAGES
        if lang_cls.json_type_variant_name_suffix is not None
    }
    assert set(suffix_overrides) <= supported  # noqa: S101
    for lang_cls, suffix in suffix_overrides.items():
        spec = make_spec(lang_cls=lang_cls)
        assert isinstance(spec, _HasJsonType)  # noqa: S101
        member_suffixes = {
            member.name.lower()
            for member in spec.json_types
            if member is not spec.json_type
        }
        assert suffix not in member_suffixes, lang_cls.__name__  # noqa: S101


_check_json_type_variants()


@beartype
def build_json_type_cross_variants(
    *,
    category: str,
    kwarg: str,
    get_default: Callable[[literalizer.Language], object],
    get_formats: Callable[[literalizer.Language], type[enum.Enum]],
) -> list[Variant]:
    """Cross every non-default JSON type with another format axis.

    Starting from :func:`build_json_type_variants` keeps discovery tied to
    the language capability.  A newly added JSON type or format therefore
    receives the cross-option coverage without another language allow-list.
    """
    variants: list[Variant] = []
    for json_variant in build_json_type_variants():
        spec = json_variant.spec
        assert isinstance(spec, _HasJsonType)  # noqa: S101
        default = get_default(spec)
        for fmt in get_formats(spec):
            if fmt is default:
                continue
            variants.append(
                Variant(
                    name=(
                        f"{json_variant.name}_{category}_{fmt.name.lower()}"
                    ),
                    spec=make_spec(
                        lang_cls=json_variant.lang_cls,
                        json_type=spec.json_type,
                        **{kwarg: fmt},
                    ),
                    lang_cls=json_variant.lang_cls,
                    fixture_prefix="",
                    record_null_substitutions=None,
                    collection_layout=literalizer.CollectionLayout.COMPACT,
                )
            )
    return variants


@beartype
def build_json_type_datetime_cross_variants() -> list[Variant]:
    """Build every non-default ``json_type`` + datetime-format cross."""
    return build_json_type_cross_variants(
        category="datetime",
        kwarg="datetime_format",
        get_default=lambda spec: spec.datetime_format,
        get_formats=lambda spec: spec.datetime_formats,
    )


@beartype
def build_json_type_bytes_cross_variants() -> list[Variant]:
    """Build every non-default ``json_type`` + bytes-format cross."""
    return build_json_type_cross_variants(
        category="bytes",
        kwarg="bytes_format",
        get_default=_configured_bytes_format,
        get_formats=lambda spec: spec.bytes_formats,
    )


@beartype
def build_json_type_language_version_cross_variants() -> list[Variant]:
    """Build every non-default JSON type + language-version cross."""
    return build_json_type_cross_variants(
        category="version",
        kwarg="language_version",
        get_default=lambda spec: spec.language_version,
        get_formats=lambda spec: spec.version_formats,
    )


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
                    fixture_prefix="",
                    record_null_substitutions=None,
                    collection_layout=literalizer.CollectionLayout.COMPACT,
                )
            )
    return variants


@beartype
def build_default_dict_value_type_variants() -> Iterable[Variant]:
    """Build default-dict-value-type variants for supported languages."""
    return _build_default_type_variants(
        field_name="default_dict_value_type",
        variant_suffix="default_dict_value_type_string",
    )


@beartype
def build_default_dict_key_type_variants() -> Iterable[Variant]:
    """Build default-dict-key-type variants for supported languages."""
    return _build_default_type_variants(
        field_name="default_dict_key_type",
        variant_suffix="default_dict_key_type",
    )


@beartype
def build_default_ordered_map_value_type_variants() -> Iterable[Variant]:
    """Build default-ordered-map-value-type variants for every language
    that supports the option.
    """
    return _build_default_type_variants(
        field_name="default_ordered_map_value_type",
        variant_suffix="default_ordered_map_value_type",
    )


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
                fixture_prefix="",
                record_null_substitutions=None,
                collection_layout=literalizer.CollectionLayout.COMPACT,
            )
            for statement_terminator_style in (
                non_default_statement_terminator_styles
            )
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
                spec=make_spec(
                    lang_cls=lang_cls,
                    sequence_format=sequence_format,
                    declaration_style=declaration_style,
                ),
                lang_cls=lang_cls,
                fixture_prefix="",
                record_null_substitutions=None,
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
    seq_format_name = lang_cls.declaration_style_sequence_format_overrides.get(
        declaration_style.name
    )
    if seq_format_name is None:
        return None
    spec = make_spec(lang_cls=lang_cls)
    return next(f for f in spec.sequence_formats if f.name == seq_format_name)


@beartype
def build_json_type_declaration_cross_variants() -> list[Variant]:
    """Build every non-default ``json_type`` + declaration-style cross."""
    variants: list[Variant] = []
    for json_variant in build_json_type_variants():
        spec = json_variant.spec
        assert isinstance(spec, _HasJsonType)  # noqa: S101
        for declaration_style in spec.declaration_styles:
            if declaration_style is spec.declaration_style:
                continue
            kwargs: dict[str, object] = {
                "json_type": spec.json_type,
                "declaration_style": declaration_style,
            }
            seq_override = _resolve_sequence_format_override(
                lang_cls=json_variant.lang_cls,
                declaration_style=declaration_style,
            )
            if seq_override is not None:
                kwargs["sequence_format"] = seq_override
            try:
                variant_spec = make_spec(
                    lang_cls=json_variant.lang_cls,
                    **kwargs,
                )
            except IncompatibleFormatsError:
                continue
            variants.append(
                Variant(
                    name=(
                        f"{json_variant.name}"
                        f"_declaration_style_{declaration_style.name.lower()}"
                    ),
                    spec=variant_spec,
                    lang_cls=json_variant.lang_cls,
                    fixture_prefix="",
                    record_null_substitutions=None,
                    collection_layout=literalizer.CollectionLayout.COMPACT,
                )
            )
    return variants


@beartype
def build_json_type_variable_form_cases() -> list[VariantCase]:
    """Build JSON-type cases selected by redefinition capability.

    Redefinition-supporting declaration styles exercise a declaration and
    assignment together.  Languages without such a style instead exercise
    their existing-variable form once.
    """
    cases: list[VariantCase] = []
    for json_variant in build_json_type_variants():
        spec = json_variant.spec
        assert isinstance(spec, _HasJsonType)  # noqa: S101
        redef_styles = find_redefinition_styles(spec=spec)
        if not redef_styles:
            name = f"{json_variant.name}_existing"
            cases.append(
                VariantCase(
                    variant_name=name,
                    variant=Variant(
                        name=name,
                        spec=spec,
                        lang_cls=json_variant.lang_cls,
                        fixture_prefix="",
                        record_null_substitutions=None,
                        collection_layout=literalizer.CollectionLayout.COMPACT,
                    ),
                    case_dir_name="dict_with_list_value",
                    variable_form=literalizer.ExistingVariable(name="my_data"),
                )
            )
            continue
        for index, declaration_style in enumerate(iterable=redef_styles):
            kwargs: dict[str, object] = {
                "json_type": spec.json_type,
                "declaration_style": declaration_style,
            }
            seq_override = _resolve_sequence_format_override(
                lang_cls=json_variant.lang_cls,
                declaration_style=declaration_style,
            )
            # No current JSON-capable redefinition style needs an override
            # or has a sibling style; these paths activate from metadata when
            # such a language is added.
            if seq_override is not None:
                kwargs["sequence_format"] = seq_override  # pragma: no cover
            name = f"{json_variant.name}_combined"
            if index > 0:
                name = (  # pragma: no cover
                    f"{name}_declaration_style_"
                    f"{declaration_style.name.lower()}"
                )
            variant = Variant(
                name=name,
                spec=make_spec(lang_cls=json_variant.lang_cls, **kwargs),
                lang_cls=json_variant.lang_cls,
                fixture_prefix="",
                record_null_substitutions=None,
                collection_layout=literalizer.CollectionLayout.COMPACT,
            )
            cases.append(
                VariantCase(
                    variant_name=name,
                    variant=variant,
                    case_dir_name="dict_with_list_value",
                    variable_form=literalizer.BothVariableForms(
                        name="my_data",
                        modifiers=frozenset(),
                    ),
                )
            )
    return cases


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
                        fixture_prefix="",
                        record_null_substitutions=None,
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
                        fixture_prefix="",
                        record_null_substitutions=None,
                        collection_layout=literalizer.CollectionLayout.COMPACT,
                    )
                )
    return variants


@beartype
def build_constructor_name_variants() -> Iterable[Variant]:
    """Build language-owned constructor-name variants."""
    variants: list[Variant] = []
    for lang_cls in sorted_languages():
        kwargs = lang_cls.non_default_kwargs
        if "null_name" not in kwargs:
            continue
        variants.append(
            Variant(
                name=f"{lang_cls.__name__}_constructor_names_j",
                spec=make_spec(lang_cls=lang_cls, **kwargs),
                lang_cls=lang_cls,
                fixture_prefix="",
                record_null_substitutions=None,
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
        custom_name = lang_cls.non_default_kwargs.get("type_name")
        if custom_name is None:
            continue
        variants.append(
            Variant(
                name=f"{lang_cls.__name__}_type_name_{custom_name}",
                spec=make_spec(lang_cls=lang_cls, type_name=custom_name),
                lang_cls=lang_cls,
                fixture_prefix="",
                record_null_substitutions=None,
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
        custom_prefix = lang_cls.non_default_kwargs.get("constructor_prefix")
        if custom_prefix is None:
            continue
        variants.append(
            Variant(
                name=f"{lang_cls.__name__}_prefix_{custom_prefix}",
                spec=make_spec(
                    lang_cls=lang_cls, constructor_prefix=custom_prefix
                ),
                lang_cls=lang_cls,
                fixture_prefix="",
                record_null_substitutions=None,
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
    shape_keys = frozenset({"id", "label", "enabled", "related_ids"})
    custom_name = "NamedType"
    for lang_cls in sorted_languages():
        default_spec = make_spec(lang_cls=lang_cls)
        if not lang_cls.supports_record_shape_names:
            continue
        metadata = lang_cls.variant_metadata
        assert isinstance(default_spec, _HasRecordShapeNames)  # noqa: S101
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
        if metadata.record_variant_version is not None:
            spec_kwargs["language_version"] = enum_member_by_name(
                enum_cls=lang_cls.VersionFormats,
                name=metadata.record_variant_version,
            )
        fixture_prefix = metadata.external_record_shape_fixture_prefix
        if lang_cls.record_shape_names_emit_declarations:
            assert fixture_prefix is None  # noqa: S101
            fixture_prefix = ""
        else:
            assert fixture_prefix is not None  # noqa: S101
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
                fixture_prefix=fixture_prefix,
                record_null_substitutions=None,
                collection_layout=literalizer.CollectionLayout.COMPACT,
            )
        )
    return variants


@beartype
def build_cpp14_error_record_shape_names_variants() -> Iterable[Variant]:
    """Build the C++14 ``ERROR`` external-map-alias regression variant."""
    yield Variant(
        name="Cpp_error_record_shape_names_Expense",
        spec=Cpp(
            language_version=Cpp.version_formats.CPP14,
            heterogeneous_strategy=Cpp.heterogeneous_strategies.ERROR,
            module_name="main",
            record_shape_names={
                frozenset({"expense_id", "trip_id", "amount_usd"}): "Expense",
            },
        ),
        lang_cls=Cpp,
        fixture_prefix=('#include "../../cpp_support/include/expense.hpp"\n'),
        record_null_substitutions=None,
        collection_layout=literalizer.CollectionLayout.COMPACT,
    )


@beartype
def build_record_null_substitutions_record_variants() -> Iterable[Variant]:
    """Build a ``RECORD`` variant for every language that names generated
    record structs.

    This cross-language golden verifies that null replacements participate
    in record-field type inference instead of merely checking one rendered
    C++ expression.
    """
    variants: list[Variant] = []
    for lang_cls in sorted_languages():
        if not lang_cls.supports_record_struct_name_prefix:
            continue
        default_spec = make_spec(lang_cls=lang_cls)
        metadata = lang_cls.variant_metadata
        record_strategy = next(
            strategy
            for strategy in default_spec.heterogeneous_strategies
            if strategy.name == "RECORD"
        )
        spec_kwargs: dict[str, object] = {
            "heterogeneous_strategy": record_strategy,
        }
        if metadata.record_variant_version is not None:
            spec_kwargs["language_version"] = enum_member_by_name(
                enum_cls=lang_cls.VersionFormats,
                name=metadata.record_variant_version,
            )
        variants.append(
            Variant(
                name=f"{lang_cls.__name__}_record_null_substitutions_record",
                spec=make_spec(lang_cls=lang_cls, **spec_kwargs),
                lang_cls=lang_cls,
                fixture_prefix="",
                record_null_substitutions={
                    "due_date": -1,
                    "parent_id": -1,
                    "assignee": "",
                },
                collection_layout=literalizer.CollectionLayout.COMPACT,
            )
        )
    return variants


@beartype
def build_string_embedded_nul_variants() -> Iterable[Variant]:
    r"""Build embedded-null-byte variants for the languages that escape it.

    The ``string_embedded_nul`` input carries a bare null byte and a
    null byte immediately followed by a digit.  Each golden file pins the
    escape a language emits and its distinctness before a following digit
    (issue #3006).  Participation is driven by
    ``variant_metadata.string_literals_escape_null_byte``: languages that
    reject the value (R, COBOL) or still emit a raw null byte are
    excluded.  A language with more than one string format (Python, whose
    raw and single-quoted formats carry their own null-byte handling)
    contributes one variant per format. JSON type variants that can
    represent null bytes opt in through their
    ``string_literals_escape_null_byte`` property.
    """
    variants: list[Variant] = []
    for lang_cls in sorted_languages():
        if lang_cls.variant_metadata.string_literals_escape_null_byte:
            string_formats = list(
                make_spec(lang_cls=lang_cls).string_formats,
            )
            for string_format in string_formats:
                suffix = (
                    ""
                    if len(string_formats) == 1
                    else f"_{string_format.name.lower()}"
                )
                variants.append(
                    Variant(
                        name=(
                            f"{lang_cls.__name__}_string_embedded_nul{suffix}"
                        ),
                        spec=make_spec(
                            lang_cls=lang_cls,
                            string_format=string_format,
                        ),
                        lang_cls=lang_cls,
                        fixture_prefix="",
                        record_null_substitutions=None,
                        collection_layout=literalizer.CollectionLayout.COMPACT,
                    )
                )
        for json_type in lang_cls.JsonTypes:
            if not json_type.string_literals_escape_null_byte:
                continue
            suffix = (
                lang_cls.json_type_variant_name_suffix
                or json_type.name.lower()
            )
            variants.append(
                Variant(
                    name=(f"{lang_cls.__name__}_string_embedded_nul_{suffix}"),
                    spec=make_spec(
                        lang_cls=lang_cls,
                        json_type=json_type,
                    ),
                    lang_cls=lang_cls,
                    fixture_prefix="",
                    record_null_substitutions=None,
                    collection_layout=literalizer.CollectionLayout.COMPACT,
                )
            )
    return variants


@beartype
def build_record_nested_map_fallback_variants() -> Iterable[Variant]:
    """Build nested-map fallback variants for capable ``RECORD``
    strategies.

    A list of records whose top-level keys are uniform but whose nested
    map under one key differs in shape (divergent or disjoint key sets)
    cannot render that nested field as a record: giving the two nested
    maps distinct record shapes forces the enclosing records to split,
    so the ``RECORD`` strategy would reject the sibling list.  The shared
    widening pass drops such families from the shape mapping, so the
    outer record survives.  Rust widens the field to ``HashMap<&'static
    str, Value>`` and wraps the leaves in its value enum (issue #2910).
    Go, Java, C#, Kotlin, Scala, and Swift use their universal top types
    (issues #2911 through #2916). Crystal, Nim, V, D, Odin, Zig, C, and
    C++ use language-specific value carriers (issues #2917 and #2919
    through #2924). The remaining ``RECORD`` languages gain their own
    widening in later sub-issues of #2909, so this stays out of
    all-languages base
    discovery. Every effective language version is covered because the
    widened carrier and aggregate syntax can vary by target standard.
    Both layouts are covered because their widened-map paths render
    compact and multiline literals separately.
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
        if record_strategy is None:
            continue
        default_spec = make_spec(
            lang_cls=lang_cls,
            heterogeneous_strategy=record_strategy,
        )
        behavior = default_spec.heterogeneous_behavior
        if not behavior.widens_unrecordizable_nested_sibling_maps:
            continue
        specs_by_version: dict[enum.Enum, literalizer.Language] = {}
        for version in lang_cls.VersionFormats:
            version_spec = make_spec(
                lang_cls=lang_cls,
                heterogeneous_strategy=record_strategy,
                language_version=version,
            )
            specs_by_version[version_spec.language_version] = version_spec
        for spec in specs_by_version.values():
            for suffix, layout in (
                ("", literalizer.CollectionLayout.COMPACT),
                ("_multiline", literalizer.CollectionLayout.MULTILINE),
            ):
                variants.append(
                    Variant(
                        name=(
                            f"{lang_cls.__name__}_record_nested_map_fallback"
                            f"{suffix}"
                        ),
                        spec=spec,
                        lang_cls=lang_cls,
                        fixture_prefix="",
                        record_null_substitutions=None,
                        collection_layout=layout,
                    )
                )
    return variants


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
                fixture_prefix="",
                record_null_substitutions=None,
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
                        fixture_prefix="",
                        record_null_substitutions=None,
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
        custom_name = lang_cls.non_default_kwargs.get(
            "heterogeneous_value_enum_name"
        )
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
                fixture_prefix="",
                record_null_substitutions=None,
                collection_layout=literalizer.CollectionLayout.COMPACT,
            )
        )
    return variants


@beartype
def build_tagged_enum_empty_container_variants() -> Iterable[Variant]:
    """Build the ``tagged_enum_empty_container`` variants.

    A scalar beside an empty list/map (``[1, []]`` / ``[1, {}]``) has no
    single element type, so a ``TAGGED_ENUM`` strategy wraps the scalar
    in its value enum and the empty container in a ``List`` / ``Map``
    variant of that enum (issue #3028).  Only languages that expose a
    ``TAGGED_ENUM`` strategy participate, so the case directories stay
    out of the all-languages base discovery (other statically typed
    languages reject or diverge on this shape).
    """
    variants: list[Variant] = []
    for lang_cls in sorted_languages():
        default_spec = make_spec(lang_cls=lang_cls)
        tagged_enum = next(
            (
                strategy
                for strategy in default_spec.heterogeneous_strategies
                if strategy.name == "TAGGED_ENUM"
            ),
            None,
        )
        if tagged_enum is None:
            continue
        spec = make_spec(
            lang_cls=lang_cls,
            heterogeneous_strategy=tagged_enum,
        )
        variants.append(
            Variant(
                name=f"{lang_cls.__name__}_tagged_enum_empty_container",
                spec=spec,
                lang_cls=lang_cls,
                fixture_prefix="",
                record_null_substitutions=None,
                collection_layout=literalizer.CollectionLayout.COMPACT,
            )
        )
    return variants


@beartype
def build_empty_container_type_hint_variants() -> Iterable[Variant]:
    """Build variants for languages declaring empty-container hint support."""
    variants: list[Variant] = []
    for lang_cls in sorted_languages():
        kwargs = lang_cls.empty_container_type_hint_variant_kwargs
        if kwargs is None:
            continue
        variants.append(
            Variant(
                name=f"{lang_cls.__name__}_empty_container_type_hint",
                spec=lang_cls(**kwargs),
                lang_cls=lang_cls,
                fixture_prefix="",
                record_null_substitutions=None,
                collection_layout=literalizer.CollectionLayout.COMPACT,
            )
        )
    return variants


@beartype
def build_c_field_name_variants() -> Iterable[Variant]:
    """Build language-owned field-name variants."""
    variants: list[Variant] = []
    for lang_cls in sorted_languages():
        kwargs = lang_cls.non_default_kwargs
        if "bool_field" not in kwargs:
            continue
        variants.append(
            Variant(
                name=f"{lang_cls.__name__}_field_names_custom",
                spec=make_spec(lang_cls=lang_cls, **kwargs),
                lang_cls=lang_cls,
                fixture_prefix="",
                record_null_substitutions=None,
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
                    fixture_prefix="",
                    record_null_substitutions=None,
                    collection_layout=literalizer.CollectionLayout.COMPACT,
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
        custom_name = lang_cls.non_default_kwargs.get(
            "heterogeneous_value_union_name"
        )
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
                fixture_prefix="",
                record_null_substitutions=None,
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
    variants: list[Variant] = []
    for lang_cls in sorted_languages():
        custom_name = lang_cls.non_default_kwargs.get(
            "heterogeneous_value_variant_name"
        )
        metadata = lang_cls.variant_metadata
        strategy_name = metadata.heterogeneous_value_variant_name_strategy
        version_name = metadata.heterogeneous_value_variant_name_version
        if custom_name is None:
            assert strategy_name is None  # noqa: S101
            assert version_name is None  # noqa: S101
            continue
        assert strategy_name is not None  # noqa: S101
        default_spec = make_spec(lang_cls=lang_cls)
        wrapping_strategy = _enum_member_by_name(
            enum_cls=default_spec.heterogeneous_strategies,
            name=strategy_name,
        )
        kwargs: dict[str, object] = {
            "heterogeneous_strategy": wrapping_strategy,
            "heterogeneous_value_variant_name": custom_name,
        }
        if version_name is not None:
            kwargs["language_version"] = _enum_member_by_name(
                enum_cls=default_spec.version_formats,
                name=version_name,
            )
        spec = make_spec(lang_cls=lang_cls, **kwargs)
        variants.append(
            Variant(
                name=(
                    f"{lang_cls.__name__}"
                    f"_heterogeneous_value_variant_name_{custom_name}"
                ),
                spec=spec,
                lang_cls=lang_cls,
                fixture_prefix="",
                record_null_substitutions=None,
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
                        fixture_prefix="",
                        record_null_substitutions=None,
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
                        fixture_prefix="",
                        record_null_substitutions=None,
                        collection_layout=literalizer.CollectionLayout.COMPACT,
                    )
                )
    return variants


@beartype
def build_object_variant_container_variants() -> list[Variant]:
    """Build focused variants for languages with ``OBJECT_VARIANT``.

    The input shapes target Nim today, the only built-in language with
    this strategy.  Discovering it from :data:`ALL_LANGUAGES` keeps the
    regression matrix extensible when another language opts into the
    same recursive object-variant representation.
    """
    variants: list[Variant] = []
    for lang_cls in sorted(ALL_LANGUAGES, key=lambda cls: cls.__name__):
        strategy = next(
            (
                strategy_option
                for strategy_option in lang_cls.HeterogeneousStrategies
                if strategy_option.name == "OBJECT_VARIANT"
            ),
            None,
        )
        if strategy is None:
            continue
        variants.append(
            Variant(
                name=f"{lang_cls.__name__}_object_variant_containers",
                spec=make_spec(
                    lang_cls=lang_cls,
                    heterogeneous_strategy=strategy,
                ),
                lang_cls=lang_cls,
                fixture_prefix="",
                record_null_substitutions=None,
                collection_layout=literalizer.CollectionLayout.COMPACT,
            )
        )
    return variants


@beartype
def build_nested_tuple_strategy_variants() -> list[Variant]:
    """Build tuple-strategy regressions for every supporting language."""
    variants: list[Variant] = []
    for lang_cls in sorted_languages():
        tuple_strategy = next(
            (
                strategy
                for strategy in lang_cls.HeterogeneousStrategies
                if strategy.name == "TUPLE"
            ),
            None,
        )
        if tuple_strategy is None:
            continue
        variants.extend(
            Variant(
                name=(
                    f"{lang_cls.__name__}_heterogeneous_strategy_tuple_nested"
                ),
                spec=make_spec(
                    lang_cls=lang_cls,
                    heterogeneous_strategy=tuple_strategy,
                    language_version=version,
                ),
                lang_cls=lang_cls,
                fixture_prefix="",
                record_null_substitutions=None,
                collection_layout=literalizer.CollectionLayout.COMPACT,
            )
            for version in lang_cls.VersionFormats
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
                            fixture_prefix="",
                            record_null_substitutions=None,
                            collection_layout=literalizer.CollectionLayout.COMPACT,
                        ),
                    )
    return variants


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
        seq_format_name = cls.declaration_style_sequence_format_overrides.get(
            fmt.name
        )
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
                    fixture_prefix="",
                    record_null_substitutions=None,
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
    "json_type_bytes_cross": build_json_type_bytes_cross_variants,
    "json_type_language_version_cross": (
        build_json_type_language_version_cross_variants
    ),
    "json_type_datetime_cross": build_json_type_datetime_cross_variants,
    "json_type_declaration_cross": (
        build_json_type_declaration_cross_variants
    ),
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
    "object_variant_containers": (build_object_variant_container_variants),
    "nested_tuple_strategy": build_nested_tuple_strategy_variants,
    "type_name": build_type_name_variants,
    "constructor_prefix": build_constructor_prefix_variants,
    "constructor_name": build_constructor_name_variants,
    "c_field_name": build_c_field_name_variants,
    "heterogeneous_value_enum_name": build_heterogeneous_value_name_variants,
    "record_shape_names": build_record_shape_names_variants,
    "cpp14_error_record_shape_names": (
        build_cpp14_error_record_shape_names_variants
    ),
    "record_null_substitutions_record": (
        build_record_null_substitutions_record_variants
    ),
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
    "record_keyword_field": build_record_keyword_field_variants,
    "record_quoted_field": build_record_quoted_field_variants,
    "record_field_type_split": build_record_field_type_split_variants,
    "record_nested_map_fallback": build_record_nested_map_fallback_variants,
    "string_embedded_nul": build_string_embedded_nul_variants,
    "nested_map_widening": build_nested_map_widening_variants,
    "dhall_nested_map_widening": build_dhall_nested_map_widening_variants,
    "empty_map_narrowing": build_empty_map_narrowing_variants,
    "tagged_enum_empty_container": build_tagged_enum_empty_container_variants,
    "empty_container_type_hint": build_empty_container_type_hint_variants,
    "record_epoch_i32_overflow": build_record_epoch_i32_overflow_variants,
    "record_numeric_cross": build_record_numeric_cross_variants,
    "language_version": build_language_version_variants,
    "language_version_cross_dict_type": (
        build_language_version_cross_dict_type_variants
    ),
    "bool_format": build_bool_format_variants,
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
    declared inputs in :data:`AXIS_INPUTS`, plus capability-generated
    capability-generated JSON variable forms and the focused modifier
    regressions.
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
    cases.extend(build_json_type_variable_form_cases())
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
