"""Build format-variant golden-file cases.

Each :class:`Variant` pairs a language class with a specific
non-default formatter spec; each :class:`VariantCase` pairs a variant
with one of the input case directories under ``tests/integration/cases``.

Most axes declare their expansion in ``axes.toml`` and are built by the
typed plans in :mod:`variant_plans`.  What remains here is the
irregular tail registered in :data:`ESCAPE_HATCH_VARIANT_AXES`, plus
the assembly of variants and manifest inputs into cases.
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
from literalizer.languages import ALL_LANGUAGES

from .case_discovery import (
    EMPTY_SIBLING_SEQUENCE_TYPE_HINT_CASE_DIR,
    cases_with_special_floats,
)
from .case_manifests import (
    CaseManifestError,
    ManifestVariant,
    load_case_manifests,
    variable_form_for_context,
)
from .language_metadata import language_metadata
from .language_specs import (
    find_redefinition_styles,
    make_spec,
    sorted_languages,
)
from .variant_axis_names import KNOWN_VARIANT_AXES, SPECIAL_VARIANT_AXES
from .variant_metadata_builders import (
    build_collection_layout_variants,
    build_dhall_nested_map_widening_variants,
    build_empty_map_narrowing_variants,
    build_modifier_variant_cases,
    build_nested_map_widening_variants,
)
from .variant_plans import declared_axis_names, variants_for_declared_axis
from .variant_types import (
    Variant,
    VariantCase,
    compact_variant,
    enum_member_by_name,
    find_enum_member,
    wrap_variable_form,
)

__all__ = ("Variant", "wrap_variable_form")

_CASES_DIR = Path(__file__).parent / "cases"


_enum_member_by_name = enum_member_by_name


@beartype
def build_comment_terminator_variants() -> list[Variant]:
    """Build every suffix-delimited comment-format variant.

    Unlike the ordinary ``comment`` axis, this includes a language's
    default format when that format has a suffix. The explicit
    ``CommentFormats`` enum on each language class is the capability
    source; line-comment members have an empty suffix and do not
    participate.
    """
    variants: list[Variant] = []
    for lang_cls in sorted_languages():
        default_spec = make_spec(lang_cls=lang_cls)
        for comment_format in default_spec.comment_formats:
            config = comment_format.value
            assert isinstance(config, literalizer.CommentConfig)  # noqa: S101
            if not config.suffix:
                continue
            variants.append(
                compact_variant(
                    name=(
                        f"{lang_cls.__name__}_comment_terminator"
                        f"_{comment_format.name.lower()}"
                    ),
                    spec=make_spec(
                        lang_cls=lang_cls,
                        comment_format=comment_format,
                    ),
                    lang_cls=lang_cls,
                )
            )
    return variants


@beartype
def build_typed_dict_null_filtering_variants() -> Iterable[Variant]:
    """Build null-filtering variants for typed-dict languages."""
    variants: list[Variant] = []
    for lang_cls in sorted_languages():
        if not lang_cls.supports_typed_dict_open:
            continue
        variant_cls = type(
            f"_{lang_cls.__name__}SkipNullDictValues",
            (lang_cls,),
            {"skip_null_dict_values": True},
        )
        assert isinstance(variant_cls, literalizer.LanguageCls)  # noqa: S101
        variants.append(
            compact_variant(
                name=f"{lang_cls.__name__}_skip_null_dict_values",
                spec=make_spec(lang_cls=variant_cls),
                lang_cls=lang_cls,
            )
        )
    return variants


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
                compact_variant(
                    name=f"{lang_cls.__name__}_json_type_{suffix}",
                    spec=make_spec(lang_cls=lang_cls, json_type=json_type),
                    lang_cls=lang_cls,
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
                compact_variant(
                    name=(
                        f"{json_variant.name}_{category}_{fmt.name.lower()}"
                    ),
                    spec=make_spec(
                        lang_cls=json_variant.lang_cls,
                        json_type=spec.json_type,
                        **{kwarg: fmt},
                    ),
                    lang_cls=json_variant.lang_cls,
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
    metadata = language_metadata(language_id=lang_cls.language_id)
    overrides = metadata.declaration_style_sequence_format_overrides
    seq_format_name = overrides.get(declaration_style.name)
    if seq_format_name is None:
        return None
    spec = make_spec(lang_cls=lang_cls)
    return enum_member_by_name(
        enum_cls=spec.sequence_formats,
        name=seq_format_name,
    )


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
                compact_variant(
                    name=(
                        f"{json_variant.name}"
                        f"_declaration_style_{declaration_style.name.lower()}"
                    ),
                    spec=variant_spec,
                    lang_cls=json_variant.lang_cls,
                )
            )
    return variants


@beartype
def build_json_type_variable_form_cases(
    *, case_dir_name: str
) -> list[VariantCase]:
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
                    variant=compact_variant(
                        name=name,
                        spec=spec,
                        lang_cls=json_variant.lang_cls,
                    ),
                    case_dir_name=case_dir_name,
                    pre_indent_level=0,
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
            variant = compact_variant(
                name=name,
                spec=make_spec(lang_cls=json_variant.lang_cls, **kwargs),
                lang_cls=json_variant.lang_cls,
            )
            cases.append(
                VariantCase(
                    variant_name=name,
                    variant=variant,
                    case_dir_name=case_dir_name,
                    variable_form=literalizer.BothVariableForms(
                        name="my_data",
                        modifiers=frozenset(),
                    ),
                    pre_indent_level=0,
                )
            )
    return cases


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
def build_json_type_record_shape_names_cross_variants() -> Iterable[Variant]:
    """Cross JSON value types with shape names for supporting
    languages.
    """
    shape_keys = frozenset({"first", "last"})
    custom_name = "ExternalRecordShape"
    for json_variant in build_json_type_variants():
        lang_cls = json_variant.lang_cls
        if not lang_cls.supports_record_shape_names:
            continue
        spec = json_variant.spec
        metadata = language_metadata(language_id=lang_cls.language_id)
        assert isinstance(spec, _HasJsonType)  # noqa: S101
        assert isinstance(spec, _HasRecordShapeNames)  # noqa: S101
        spec_kwargs: dict[str, object] = {
            "heterogeneous_strategy": enum_member_by_name(
                enum_cls=lang_cls.HeterogeneousStrategies,
                name="ERROR",
            ),
            "json_type": spec.json_type,
            "record_shape_names": {shape_keys: custom_name},
        }
        record_language_version = metadata.variants.record_language_version
        if record_language_version is not None:
            spec_kwargs["language_version"] = enum_member_by_name(
                enum_cls=lang_cls.VersionFormats,
                name=record_language_version,
            )
        if lang_cls.supports_module_name:
            spec_kwargs["module_name"] = lang_cls.module_name_case.convert(
                name="main",
            )
        yield compact_variant(
            name=f"{json_variant.name}_record_shape_names_{custom_name}",
            spec=lang_cls(**spec_kwargs),
            lang_cls=lang_cls,
        )


@beartype
def build_string_embedded_nul_variants() -> Iterable[Variant]:
    r"""Build embedded-null-byte variants for the languages that escape it.

    The ``string_embedded_nul`` input carries a bare null byte and a
    null byte immediately followed by a digit.  Each golden file pins the
    escape a language emits and its distinctness before a following digit
    (issue #3006).  Participation is driven by
    ``variant_metadata.string_literals_escape_null_byte``: languages that
    reject the value (R, COBOL) or still emit a raw null byte are
    excluded.  A language with more than one string format contributes
    one variant per format. JSON type variants that can
    represent null bytes opt in through their
    ``string_literals_escape_null_byte`` property.
    """
    variants: list[Variant] = []
    for lang_cls in sorted_languages():
        if lang_cls.variant_metadata.string_literals_escape_null_byte:
            string_formats = [
                string_format
                for string_format in make_spec(
                    lang_cls=lang_cls
                ).string_formats
                if string_format.name != "MULTILINE"
            ]
            for string_format in string_formats:
                suffix = (
                    ""
                    if len(string_formats) == 1
                    else f"_{string_format.name.lower()}"
                )
                variants.append(
                    compact_variant(
                        name=(
                            f"{lang_cls.__name__}_string_embedded_nul{suffix}"
                        ),
                        spec=make_spec(
                            lang_cls=lang_cls,
                            string_format=string_format,
                        ),
                        lang_cls=lang_cls,
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
                compact_variant(
                    name=(f"{lang_cls.__name__}_string_embedded_nul_{suffix}"),
                    spec=make_spec(
                        lang_cls=lang_cls,
                        json_type=json_type,
                    ),
                    lang_cls=lang_cls,
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
        record_strategy = find_enum_member(
            enum_cls=default_spec.heterogeneous_strategies,
            name="RECORD",
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
                        collection_layout=layout,
                        fixture_prefix="",
                        record_null_substitutions=None,
                    )
                )
    return variants


@beartype
def build_empty_container_type_hint_variants() -> Iterable[Variant]:
    """Build variants for languages declaring empty-container hint support."""
    variants: list[Variant] = []
    for lang_cls in sorted_languages():
        metadata = language_metadata(language_id=lang_cls.language_id)
        settings = metadata.variants.empty_container_type_hint
        if settings is None:
            continue
        kwargs: dict[str, object] = {
            "heterogeneous_strategy": enum_member_by_name(
                enum_cls=lang_cls.HeterogeneousStrategies,
                name=settings.heterogeneous_strategy,
            ),
            "empty_container_type_hints": {
                tuple(entry.path): entry.hint for entry in settings.type_hints
            },
        }
        variants.append(
            compact_variant(
                name=f"{lang_cls.__name__}_empty_container_type_hint",
                spec=lang_cls(**kwargs),
                lang_cls=lang_cls,
            )
        )
    return variants


@beartype
def build_multiline_string_context_cases(
    *,
    combined_case_dir_name: str,
    combined_suffix: str,
    combined_variable_form: literalizer.VariableForm,
    pre_indent_case_dir_name: str,
    pre_indent_level: int,
) -> list[VariantCase]:
    """Build assignment and nonzero-indentation multiline contexts.

    The ordinary multiline axis already renders every input with a
    :class:`~literalizer.NewVariable`.  Add a combined declaration and
    assignment for each language whose declaration metadata says that
    redefinition is supported.  Languages with class-field modifier
    combinations also exercise the public ``pre_indent_level`` path in the
    same valid class-scope context used by the dedicated pre-indent suite.
    """
    cases: list[VariantCase] = []
    for base_variant in variants_for_declared_axis(
        axis_key="multiline_string",
        resolve_axis=variants_for_axis,
    ):
        spec = base_variant.spec
        redefinition_styles = find_redefinition_styles(spec=spec)
        if redefinition_styles:
            declaration_style = (
                spec.declaration_style
                if spec.declaration_style in redefinition_styles
                else redefinition_styles[0]
            )
            name = f"{base_variant.name}{combined_suffix}"
            cases.append(
                VariantCase(
                    variant_name=name,
                    variant=dataclasses.replace(
                        base_variant,
                        name=name,
                        spec=make_spec(
                            lang_cls=base_variant.lang_cls,
                            string_format=spec.string_format,
                            declaration_style=declaration_style,
                        ),
                    ),
                    case_dir_name=combined_case_dir_name,
                    variable_form=combined_variable_form,
                    pre_indent_level=0,
                )
            )

        for combination in base_variant.lang_cls.modifier_combinations:
            name = (
                f"{base_variant.name}_pre_indent_{pre_indent_level}_"
                f"{combination.name}"
            )
            cases.append(
                VariantCase(
                    variant_name=name,
                    variant=dataclasses.replace(base_variant, name=name),
                    case_dir_name=pre_indent_case_dir_name,
                    variable_form=literalizer.NewVariable(
                        name="my_data",
                        modifiers=combination.modifiers,
                    ),
                    pre_indent_level=pre_indent_level,
                )
            )
    return cases


@beartype
def build_multiline_raw_string_delimiter_variants() -> list[Variant]:
    """Build custom, punctuation, and exhausted raw-delimiter variants."""
    variants: list[Variant] = []
    for lang_cls in sorted_languages():
        metadata = language_metadata(language_id=lang_cls.language_id)
        custom_base = metadata.non_default_kwargs.get(
            "multiline_raw_string_delimiter_base"
        )
        if custom_base is None:
            continue
        multiline = _enum_member_by_name(
            enum_cls=lang_cls.StringFormats,
            name="MULTILINE",
        )
        for name, delimiter_base in (
            ("custom", custom_base),
            ("punctuation", "_{}[]#<>%:;.?*"),
            ("exhausted", "abcdefghijklmnop"),
        ):
            variants.append(
                compact_variant(
                    name=(
                        f"{lang_cls.__name__}_multiline_raw_string_delimiter"
                        f"_{name}"
                    ),
                    spec=make_spec(
                        lang_cls=lang_cls,
                        string_format=multiline,
                        multiline_raw_string_delimiter_base=delimiter_base,
                    ),
                    lang_cls=lang_cls,
                )
            )
    return variants


# Axes whose expansion is genuinely irregular, and so is written as a
# typed Python builder instead of a declared plan in ``axes.toml``:
# the ``json_type`` family (which starts from another axis's variants
# rather than from a language, and whose declaration-style cross
# filters on :exc:`~literalizer.exceptions.IncompatibleFormatsError`),
# the widening and narrowing cases (which pair a compact and a
# multiline layout and select a spec by rendering behavior), and a
# handful of one-off shapes.  A meta-test holds this set to its current
# membership: new axes belong in ``axes.toml``.
_ESCAPE_HATCH_BUILDERS: dict[str, Callable[[], Iterable[Variant]]] = {
    "collection_layout": build_collection_layout_variants,
    "comment_terminator": build_comment_terminator_variants,
    "dhall_nested_map_widening": build_dhall_nested_map_widening_variants,
    "empty_container_type_hint": build_empty_container_type_hint_variants,
    "empty_map_narrowing": build_empty_map_narrowing_variants,
    "json_type": build_json_type_variants,
    "json_type_bytes_cross": build_json_type_bytes_cross_variants,
    "json_type_datetime_cross": build_json_type_datetime_cross_variants,
    "json_type_declaration_cross": (
        build_json_type_declaration_cross_variants
    ),
    "json_type_language_version_cross": (
        build_json_type_language_version_cross_variants
    ),
    "json_type_record_shape_names_cross": (
        build_json_type_record_shape_names_cross_variants
    ),
    "multiline_raw_string_delimiter": (
        build_multiline_raw_string_delimiter_variants
    ),
    "nested_map_widening": build_nested_map_widening_variants,
    "record_nested_map_fallback": build_record_nested_map_fallback_variants,
    "string_embedded_nul": build_string_embedded_nul_variants,
    "typed_dict_null_filtering": build_typed_dict_null_filtering_variants,
}

ESCAPE_HATCH_VARIANT_AXES = frozenset(_ESCAPE_HATCH_BUILDERS)


@beartype
def check_axis_coverage(
    *,
    expandable: frozenset[str],
    declared: frozenset[str],
    escape_hatch: frozenset[str],
) -> None:
    """Fail when an axis resolves to other than one expansion.

    Every axis the case manifests may name has to reach exactly one
    declared plan or one registered escape-hatch builder.
    """
    both = sorted(declared & escape_hatch)
    if both:
        msg = (
            "variant axes are both declared in axes.toml and registered as "
            f"escape-hatch builders: {both}"
        )
        raise CaseManifestError(msg)
    unexpanded = sorted(expandable - declared - escape_hatch)
    if unexpanded:
        msg = (
            f"variant axes {unexpanded} have no expansion; declare a plan "
            "in axes.toml or register an escape-hatch builder"
        )
        raise CaseManifestError(msg)
    unknown = sorted((declared | escape_hatch) - expandable)
    if unknown:
        msg = (
            f"variant axes {unknown} expand but are not in KNOWN_VARIANT_AXES"
        )
        raise CaseManifestError(msg)


check_axis_coverage(
    expandable=KNOWN_VARIANT_AXES - SPECIAL_VARIANT_AXES,
    declared=declared_axis_names(),
    escape_hatch=ESCAPE_HATCH_VARIANT_AXES,
)


@beartype
def variants_for_axis(*, axis_key: str) -> list[Variant]:
    """Return the variants for an axis key.

    Most axes name a typed plan in ``axes.toml``; the irregular tail
    dispatches to its registered escape-hatch builder.  A declared plan
    that narrows another axis resolves its base through here too, so a
    narrowing may sit over either kind of expansion.
    """
    if axis_key in _ESCAPE_HATCH_BUILDERS:
        return list(_ESCAPE_HATCH_BUILDERS[axis_key]())
    return variants_for_declared_axis(
        axis_key=axis_key,
        resolve_axis=variants_for_axis,
    )


@beartype
def _case_for_manifest_variant(
    *,
    case_dir_name: str,
    manifest_variant: ManifestVariant,
    variant: Variant,
) -> VariantCase:
    """Combine typed language expansion with case-local render context."""
    context = manifest_variant.context
    if context.collection_layout is not None:
        variant = dataclasses.replace(
            variant,
            collection_layout=literalizer.CollectionLayout(
                value=context.collection_layout
            ),
        )
    if context.record_null_substitutions is not None:
        variant = dataclasses.replace(
            variant,
            record_null_substitutions=context.record_null_substitutions,
        )
    return VariantCase(
        variant_name=f"{variant.name}{manifest_variant.suffix}",
        variant=variant,
        case_dir_name=case_dir_name,
        variable_form=variable_form_for_context(context=context),
        pre_indent_level=context.pre_indent_level,
    )


def _one_special_input(
    *, entries: list[tuple[str, ManifestVariant]], axis: str
) -> tuple[str, ManifestVariant]:
    """Return the sole manifest entry registered for a special axis."""
    matches = [entry for entry in entries if entry[1].axis == axis]
    if len(matches) != 1:
        msg = f"variant axis {axis!r} requires exactly one manifest input"
        raise CaseManifestError(msg)
    return matches[0]


@beartype
def validate_unique_variant_targets(cases: list[VariantCase]) -> None:
    """Fail when two inventory entries resolve to one golden path."""
    targets: dict[tuple[str, str, str, object], VariantCase] = {}
    for case in cases:
        target = (
            case.case_dir_name,
            case.variant_name,
            case.variant.spec.extension,
            case.variant.spec.language_version,
        )
        previous = targets.get(target)
        if previous is not None:
            msg = (
                "duplicate golden target from manifest inventory: "
                f"{case.case_dir_name}/{case.variant_name}"
                f"@{case.variant.spec.language_version.name}"
                f".{case.variant.spec.extension}"
            )
            raise CaseManifestError(msg)
        targets[target] = case


@functools.cache
@beartype
def build_variant_cases() -> list[VariantCase]:
    """Collect all format-variant golden-file test cases.

    The full set is the cross product of typed language variants with the
    case-local manifest entries, plus the manifest-selected contextual
    expansions for variable forms, modifiers, and pre-indent coverage.
    """
    special_float_cases = cases_with_special_floats(cases_dir=_CASES_DIR)
    entries = [
        (manifest.case_dir.name, manifest_variant)
        for manifest in load_case_manifests(cases_dir=_CASES_DIR)
        for manifest_variant in manifest.variants
    ]
    cases: list[VariantCase] = []
    for case_dir_name, manifest_variant in entries:
        if manifest_variant.axis in SPECIAL_VARIANT_AXES:
            continue
        variants = variants_for_axis(axis_key=manifest_variant.axis)
        cases.extend(
            _case_for_manifest_variant(
                case_dir_name=case_dir_name,
                manifest_variant=manifest_variant,
                variant=variant,
            )
            for variant in variants
            if not (
                case_dir_name in special_float_cases
                and not variant.lang_cls.supports_special_floats
            )
            and not (
                case_dir_name == EMPTY_SIBLING_SEQUENCE_TYPE_HINT_CASE_DIR
                and not (
                    variant.lang_cls.supports_empty_sibling_sequence_type_hints
                )
            )
        )

    modifier_inputs = tuple(
        case_dir_name
        for case_dir_name, entry in entries
        if entry.axis == "modifiers"
    )
    modifier_sequence_inputs = {
        entry.suffix.removeprefix("_"): case_dir_name
        for case_dir_name, entry in entries
        if entry.axis == "modifier_sequence_format"
    }
    cases.extend(
        build_modifier_variant_cases(
            case_dir_names=modifier_inputs,
            sequence_case_dirs=modifier_sequence_inputs,
        )
    )

    json_case_dir_name, _ = _one_special_input(
        entries=entries,
        axis="json_type_variable_form",
    )
    cases.extend(
        build_json_type_variable_form_cases(case_dir_name=json_case_dir_name)
    )

    combined_case_dir_name, combined_entry = _one_special_input(
        entries=entries,
        axis="multiline_string_combined",
    )
    pre_indent_case_dir_name, pre_indent_entry = _one_special_input(
        entries=entries,
        axis="multiline_string_pre_indent",
    )
    cases.extend(
        build_multiline_string_context_cases(
            combined_case_dir_name=combined_case_dir_name,
            combined_suffix=combined_entry.suffix,
            combined_variable_form=variable_form_for_context(
                context=combined_entry.context
            ),
            pre_indent_case_dir_name=pre_indent_case_dir_name,
            pre_indent_level=pre_indent_entry.context.pre_indent_level,
        )
    )

    validate_unique_variant_targets(cases=cases)
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
