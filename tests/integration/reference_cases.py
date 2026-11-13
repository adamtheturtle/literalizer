"""Collect reference cases and their effective language options."""

import dataclasses
import enum
import functools
from pathlib import Path

from beartype import beartype

import literalizer
from tests.enum_members import enum_member_by_name

from .case_manifests import (
    REF_DEFAULT_OWNER,
    REF_OWNER,
    OwnerName,
    RefCaseSpec,
    ref_case_specs,
)
from .language_metadata import language_metadata
from .language_specs import (
    find_redefinition_styles,
    make_golden_path,
    make_spec,
    reference_case_for_declaration_style,
    sorted_languages,
)
from .variant_cases import Variant, variants_for_axis
from .variant_context import config_with_variant_layout

CASES_DIR = Path(__file__).parent / "cases"


@dataclasses.dataclass(frozen=True, kw_only=True)
class RefRendering:
    """A reference configuration, target spec and owned fixture."""

    config: RefCaseSpec
    lang_cls: literalizer.LanguageCls
    spec: literalizer.Language
    golden_name: str
    ref_case: literalizer.IdentifierCase | None

    def golden_path(self, *, cases_dir: Path) -> Path:
        """Locate the fixture used by execution and inventory checks."""
        return make_golden_path(
            parent=cases_dir / self.config.case_dir_name,
            name=self.config.golden_name(name=self.golden_name),
            lang_cls=self.lang_cls,
            version=self.spec.language_version,
        )


@dataclasses.dataclass(frozen=True)
class LiteralizeRefCase:
    """A parameterized literalize-ref golden-file test case."""

    config: RefCaseSpec
    lang_cls: literalizer.LanguageCls
    owner: OwnerName

    @property
    def renderings(self) -> tuple[RefRendering, ...]:
        """Exercise each selected version under the owner's ref policy."""
        rows: list[RefRendering] = []
        for version in ref_language_versions(
            config=self.config, lang_cls=self.lang_cls
        ):
            spec = make_spec(lang_cls=self.lang_cls, language_version=version)
            ref_case = None
            if self.owner != REF_DEFAULT_OWNER:
                ref_case = self.config.ref_case_for(lang_cls=self.lang_cls)
                if ref_case is None:
                    ref_case = spec.identifier_cases[0]
            suffix = (
                "ref_default" if self.owner == REF_DEFAULT_OWNER else "ref"
            )
            rows.append(
                RefRendering(
                    config=self.config,
                    lang_cls=self.lang_cls,
                    spec=spec,
                    golden_name=f"{self.lang_cls.__name__}_{suffix}",
                    ref_case=ref_case,
                )
            )
        return tuple(rows)


@functools.cache
@beartype
def discover_literalize_ref_cases(
    *, owner: OwnerName
) -> list[LiteralizeRefCase]:
    """Return reference cases for the selected API owner.

    Explicit reference cases require a supported reference spelling and,
    for combined forms, a redefinition style. Default cases exercise the
    public defaults without imposing those explicit options.
    """
    return [
        LiteralizeRefCase(config=config, lang_cls=lang_cls, owner=owner)
        for config in ref_case_specs(cases_dir=CASES_DIR, owner=owner)
        if not config.variant_only
        for lang_cls in sorted_languages()
        if config.admits_language(lang_cls=lang_cls)
        if owner == REF_DEFAULT_OWNER
        or config.variable_form != "both"
        or bool(find_redefinition_styles(spec=make_spec(lang_cls=lang_cls)))
        if owner == REF_DEFAULT_OWNER
        or config.ref_case_for(lang_cls=lang_cls) is None
        or config.ref_case_for(lang_cls=lang_cls)
        in lang_cls.supported_ref_cases
    ]


@dataclasses.dataclass(frozen=True)
class LiteralizeRefVariantCase:
    """A reference scenario paired with an effective language variant."""

    config: RefCaseSpec
    variant: Variant
    ref_case: literalizer.IdentifierCase | None

    @property
    def lang_cls(self) -> literalizer.LanguageCls:
        """Expose the target language consistently across reference
        cases.
        """
        return self.variant.lang_cls

    @property
    def golden_name(self) -> str:
        """Retain whether the public API receives an explicit ref case."""
        suffix = "ref_default" if self.ref_case is None else "ref"
        return f"{self.variant.name}_{suffix}"

    @property
    def renderings(self) -> tuple[RefRendering, ...]:
        """Retain the exact spec and ref spelling selected by the axis."""
        return (
            RefRendering(
                config=self.config,
                lang_cls=self.lang_cls,
                spec=self.variant.spec,
                golden_name=self.golden_name,
                ref_case=self.ref_case,
            ),
        )


@beartype
def _reference_variant_case(
    *, config: RefCaseSpec, variant: Variant, owner: OwnerName
) -> LiteralizeRefVariantCase | None:
    """Retain selected options and reject unsupported reference styles."""
    lang_cls = variant.lang_cls
    if not config.admits_language(lang_cls=lang_cls):
        return None
    ref_case = config.ref_case_for(lang_cls=lang_cls)
    if ref_case is not None and ref_case not in lang_cls.supported_ref_cases:
        return None
    spec = ref_language_options(
        config=config, lang_cls=lang_cls, spec=variant.spec
    )
    if (
        config.variable_form == "both"
        and spec.declaration_style not in find_redefinition_styles(spec=spec)
    ):
        return None
    # A selected declaration variant is an explicit choice. The base
    # suite's automatic mutable-style fallback must not relabel it.
    names = language_metadata(
        language_id=lang_cls.language_id
    ).variants.declaration_style_variable_names
    reference_case = config.ref_case_for(lang_cls=lang_cls)
    if owner == REF_DEFAULT_OWNER:
        reference_case = None
    elif reference_case is None:
        reference_case = reference_case_for_declaration_style(
            lang_cls=lang_cls, spec=spec
        )
    selected_config = config_with_variant_layout(
        config=config, layout=variant.collection_layout
    ).model_copy(
        update={
            "declaration_style": spec.declaration_style.name,
            "variable_name": names.get(
                spec.declaration_style.name, config.variable_name
            ),
            "ref_case_override": reference_case,
        }
    )
    return LiteralizeRefVariantCase(
        config=selected_config,
        variant=dataclasses.replace(variant, spec=spec),
        ref_case=reference_case,
    )


@functools.cache
@beartype
def build_literalize_ref_variant_cases() -> list[LiteralizeRefVariantCase]:
    """Discover reference variants through the existing typed axis
    plans.
    """
    return [
        case
        for owner in (REF_OWNER, REF_DEFAULT_OWNER)
        for config in ref_case_specs(cases_dir=CASES_DIR, owner=owner)
        for entry in config.variants
        for variant in variants_for_axis(axis_key=entry.axis)
        if (
            case := _reference_variant_case(
                config=config, variant=variant, owner=owner
            )
        )
        is not None
    ]


@beartype
def ref_language_options(
    *,
    config: RefCaseSpec,
    lang_cls: literalizer.LanguageCls,
    spec: literalizer.Language,
) -> literalizer.Language:
    """Apply the output modes explicitly selected by a reference case."""
    for name, enum_cls, choice in (
        (
            "variable_type_hints",
            lang_cls.VariableTypeHints,
            config.variable_type_hints,
        ),
        (
            "heterogeneous_strategy",
            lang_cls.HeterogeneousStrategies,
            config.heterogeneous_strategy,
        ),
        ("sequence_format", lang_cls.SequenceFormats, config.sequence_format),
        (
            "declaration_style",
            lang_cls.DeclarationStyles,
            config.declaration_style,
        ),
        ("json_type", lang_cls.JsonTypes, config.json_type),
        ("dict_format", lang_cls.DictFormats, config.dict_format),
    ):
        if choice is not None:
            spec = dataclasses.replace(
                spec,
                **{name: enum_member_by_name(enum_cls=enum_cls, name=choice)},
            )
    if config.default_sequence_element_type is not None:
        spec = dataclasses.replace(
            spec,
            default_sequence_element_type=config.default_sequence_element_type,
        )
    return spec


@beartype
def ref_language_versions(
    *, config: RefCaseSpec, lang_cls: literalizer.LanguageCls
) -> tuple[enum.Enum, ...]:
    """Return each effective target version once after applying
    options.
    """
    return tuple(
        dict.fromkeys(
            ref_language_options(
                config=config,
                lang_cls=lang_cls,
                spec=make_spec(lang_cls=lang_cls, language_version=version),
            ).language_version
            for version in lang_cls.VersionFormats
        )
    )


@beartype
def reference_golden_cases() -> tuple[
    LiteralizeRefCase | LiteralizeRefVariantCase, ...
]:
    """Collect explicit, default and variant reference fixture owners."""
    return (
        *discover_literalize_ref_cases(owner=REF_OWNER),
        *discover_literalize_ref_cases(owner=REF_DEFAULT_OWNER),
        *build_literalize_ref_variant_cases(),
    )
