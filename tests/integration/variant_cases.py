"""Build format-variant golden-file cases.

Each :class:`Variant` pairs a language class with a specific
non-default formatter spec; each :class:`VariantCase` pairs a variant
with one of the input case directories under ``tests/integration/cases``.

Axes declare their expansion in ``axes.toml`` and are built by the
typed plans in :mod:`variant_plans`, bar the one registered as an
escape-hatch builder in :mod:`variant_escape_hatches`.  What remains
here is the assembly of variants and manifest inputs into cases.
"""

import dataclasses
import enum
import functools
from pathlib import Path
from typing import Protocol, assert_never, runtime_checkable

from beartype import beartype

import literalizer

from .case_discovery import cases_with_special_floats
from .case_manifests import (
    CaseManifestError,
    ManifestVariant,
    VariantCapabilityName,
    load_case_manifests,
    variable_form_for_context,
)
from .language_metadata import language_metadata
from .language_specs import (
    find_redefinition_styles,
    make_spec,
    sorted_languages,
)
from .variant_axis_names import SPECIAL_VARIANT_AXES
from .variant_escape_hatches import (
    ESCAPE_HATCH_VARIANT_AXES,
    escape_hatch_variants,
)
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
    wrap_variable_form,
)

__all__ = ("Variant", "wrap_variable_form")

_CASES_DIR = Path(__file__).parent / "cases"

_SPECIAL_FLOAT_CAPABILITIES: frozenset[VariantCapabilityName] = frozenset(
    {"special_floats"},
)
"""The requirement carried by an input containing a non-finite float."""


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
        if json_variant.lang_cls.language_id == "cpp":
            name = f"{json_variant.name}_variable_multiline"
            cases.append(
                VariantCase(
                    variant_name=name,
                    variant=dataclasses.replace(
                        json_variant,
                        name=name,
                        collection_layout=(
                            literalizer.CollectionLayout.MULTILINE
                        ),
                    ),
                    case_dir_name=case_dir_name,
                    variable_form=wrap_variable_form(),
                    pre_indent_level=0,
                )
            )
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
        for declaration_style in redef_styles:
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
def check_axis_coverage(
    *,
    declared: frozenset[str],
    escape_hatch: frozenset[str],
    special: frozenset[str],
) -> None:
    """Fail when an axis resolves to more than one expansion.

    Every axis name the case manifests may use comes from exactly one of
    the three registries, so an axis registered twice would silently
    expand through whichever one :func:`variants_for_axis` consults
    first.
    """
    both = sorted(declared & escape_hatch)
    if both:
        msg = (
            "variant axes are both declared in axes.toml and registered as "
            f"escape-hatch builders: {both}"
        )
        raise CaseManifestError(msg)
    contextual = sorted(special & (declared | escape_hatch))
    if contextual:
        msg = (
            "variant axes are declared as special axes in axes.toml and also "
            f"expand as ordinary ones: {contextual}"
        )
        raise CaseManifestError(msg)


check_axis_coverage(
    declared=declared_axis_names(),
    escape_hatch=ESCAPE_HATCH_VARIANT_AXES,
    special=SPECIAL_VARIANT_AXES,
)


@beartype
def variants_for_axis(*, axis_key: str) -> list[Variant]:
    """Return the variants for an axis key.

    Most axes name a typed plan in ``axes.toml``; the irregular tail
    dispatches to its registered escape-hatch builder.  A declared plan
    that narrows another axis resolves its base through here too, so a
    narrowing may sit over either kind of expansion.
    """
    if axis_key in ESCAPE_HATCH_VARIANT_AXES:
        return escape_hatch_variants(axis_key=axis_key)
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
def language_supports_capability(
    *,
    lang_cls: literalizer.LanguageCls,
    capability: VariantCapabilityName,
) -> bool:
    """Return whether *lang_cls* provides the named capability."""
    match capability:
        case "collection_comments":
            return make_spec(lang_cls=lang_cls).supports_collection_comments
        case "empty_sibling_sequence_type_hints":
            return lang_cls.supports_empty_sibling_sequence_type_hints
        case "special_floats":
            return lang_cls.supports_special_floats
        case _ as unreachable:
            assert_never(unreachable)


@beartype
def required_capabilities(
    *,
    case_dir_name: str,
    manifest_variant: ManifestVariant,
    special_float_cases: frozenset[str],
) -> frozenset[VariantCapabilityName]:
    """Return the capabilities one manifest variant entry needs.

    A case declares what its input requires, bar special floats, which
    are read out of the input itself so the requirement cannot go stale
    as the fixture changes.
    """
    declared = frozenset(manifest_variant.requires)
    if case_dir_name in special_float_cases:
        return declared | _SPECIAL_FLOAT_CAPABILITIES
    return declared


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
    manifests = load_case_manifests(cases_dir=_CASES_DIR)
    selection_by_case = {
        manifest.case_dir.name: manifest.selection for manifest in manifests
    }
    entries = [
        (manifest.case_dir.name, manifest_variant)
        for manifest in manifests
        for manifest_variant in manifest.variants
    ]
    cases: list[VariantCase] = []
    for case_dir_name, manifest_variant in entries:
        selection = selection_by_case[case_dir_name]
        if manifest_variant.axis in SPECIAL_VARIANT_AXES:
            continue
        variants = variants_for_axis(axis_key=manifest_variant.axis)
        required = required_capabilities(
            case_dir_name=case_dir_name,
            manifest_variant=manifest_variant,
            special_float_cases=special_float_cases,
        )
        cases.extend(
            _case_for_manifest_variant(
                case_dir_name=case_dir_name,
                manifest_variant=manifest_variant,
                variant=variant,
            )
            for variant in variants
            if selection.admits_language(lang_cls=variant.lang_cls)
            if all(
                language_supports_capability(
                    lang_cls=variant.lang_cls,
                    capability=capability,
                )
                for capability in required
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
