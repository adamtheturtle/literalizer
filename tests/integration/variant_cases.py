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
from collections.abc import Callable, Iterable
from pathlib import Path
from typing import Protocol, runtime_checkable

from beartype import beartype

import literalizer

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
from .variant_metadata_builders import build_modifier_variant_cases
from .variant_plans import (
    declared_axis_names,
    sequence_format_override,
    variants_for_declared_axis,
)
from .variant_types import (
    Variant,
    VariantCase,
    compact_variant,
    enum_member_by_name,
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
    for json_variant in variants_for_axis(axis_key="json_type"):
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
            lang_cls = json_variant.lang_cls
            kwargs: dict[str, object] = {
                "json_type": spec.json_type,
                "declaration_style": declaration_style,
                # A declaration style that substitutes a sequence format
                # in, as Rust ``CONST`` does, needs the same
                # substitution here; no JSON-capable redefinition style
                # declares one today.
                **sequence_format_override(
                    metadata=language_metadata(
                        language_id=lang_cls.language_id
                    ),
                    default_spec=make_spec(lang_cls=lang_cls),
                    declaration_style=declaration_style,
                ),
            }
            # No current JSON-capable language has a sibling redefinition
            # style; that path activates from metadata when such a
            # language is added.
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
# typed Python builder instead of a declared plan in ``axes.toml``.
# ``comment_terminator`` and ``string_embedded_nul`` gate on the member
# rather than on the language; ``empty_container_type_hint`` and
# ``multiline_raw_string_delimiter`` pass fixture data through as a
# constructor argument; ``typed_dict_null_filtering`` renders through a
# synthesized language subclass.  A meta-test holds this set to its
# current membership: new axes belong in ``axes.toml``.
_ESCAPE_HATCH_BUILDERS: dict[str, Callable[[], Iterable[Variant]]] = {
    "comment_terminator": build_comment_terminator_variants,
    "empty_container_type_hint": build_empty_container_type_hint_variants,
    "multiline_raw_string_delimiter": (
        build_multiline_raw_string_delimiter_variants
    ),
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
