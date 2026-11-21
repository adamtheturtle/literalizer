"""Collect reference cases and their effective language options."""

import dataclasses
import functools
from pathlib import Path

from beartype import beartype

import literalizer
from literalizer.exceptions import (
    CallArgNotSupportedError,
    ExistingVariableNotSelfContainedError,
    UnrepresentableInputError,
    UnrepresentableNullError,
)
from tests.enum_members import enum_member_by_name

from .call_ref_contracts import (
    authored_call_ref_outcome,
    unsupported_reference_marker,
)
from .case_manifests import (
    REF_DEFAULT_OWNER,
    REF_OWNER,
    ExternalRefContext,
    OwnerName,
    RefCaseSpec,
    RefExpressionContext,
    ref_case_specs,
)
from .golden_artifacts import GoldenArtifact
from .golden_outcomes import SUCCESS, Exclusion, GoldenOutcome, Rejection
from .language_metadata import language_metadata
from .language_specs import (
    find_redefinition_styles,
    make_golden_artifact,
    make_spec,
    reference_case_for_declaration_style,
    sorted_languages,
    unique_effective_specs,
)
from .rejection_contracts import rejected_examples
from .scenario_participation import Requirement, scenario_exclusion
from .variant_cases import Variant, variants_for_axis
from .variant_context import config_with_variant_layout

CASES_DIR = Path(__file__).parent / "cases"


@functools.cache
def _rejects_reference_before_assignment() -> frozenset[
    literalizer.LanguageCls
]:
    """Read the root-reference and null constraints that take
    precedence.
    """
    return frozenset(
        case.lang_cls
        for contract, error in (
            (
                "existing_variable_ref_in_typed_wrapper",
                CallArgNotSupportedError,
            ),
            (
                "null_indistinguishable_from_empty_text",
                UnrepresentableNullError,
            ),
            (
                "null_indistinguishable_from_empty_text",
                UnrepresentableInputError,
            ),
        )
        for case in rejected_examples(contract=contract, error=error)
    )


def _reference_outcome(
    *,
    config: RefCaseSpec,
    lang_cls: literalizer.LanguageCls,
    spec: literalizer.Language,
    golden_name: str,
    ref_case: literalizer.IdentifierCase | None,
) -> GoldenOutcome:
    """Resolve fixture prerequisites and documented reference errors."""
    exclusion = _reference_exclusion(
        config=config, spec=spec, ref_case=ref_case, golden_name=golden_name
    )
    if exclusion is not None:
        return exclusion
    if (
        config.case_dir_name == "literalize_ref_known_null_assignment"
        and lang_cls not in _rejects_reference_before_assignment()
        and not spec.reference_assignment_declares_binding(None)
    ):
        return Rejection(
            error=ExistingVariableNotSelfContainedError,
            match="the assignment has no prior declaration",
        )
    outcome = authored_call_ref_outcome(
        config=config, spec=spec, lang_cls=lang_cls
    )
    if outcome is None:
        outcome = unsupported_reference_marker(
            config=config, lang_cls=lang_cls, cases_dir=CASES_DIR
        )
    if outcome is not None:
        return outcome
    if (
        isinstance(config.context, ExternalRefContext)
        and config.variable_form == "existing"
        and "my_data" in config.context.declarations
        and len(find_redefinition_styles(spec=spec)) == 0
    ):
        return Exclusion(
            reason="the external destination needs a reassignable declaration"
        )
    return SUCCESS


def _reference_exclusion(
    *,
    config: RefCaseSpec,
    spec: literalizer.Language,
    ref_case: literalizer.IdentifierCase | None,
    golden_name: str,
) -> Exclusion | None:
    """Check the requested spelling, binding and native consumer."""
    requirements: list[Requirement] = []
    if config.variable_form == "both":
        requirements.append(Requirement.REDEFINITION)
    if isinstance(config.context, (ExternalRefContext, RefExpressionContext)):
        requirements.append(Requirement.CALL_SYNTAX)
    return scenario_exclusion(
        case_id=f"{config.coverage_id}/{golden_name}",
        spec=spec,
        requirements=requirements,
        fixture_reason=(
            f"unsupported reference spelling {ref_case.name}"
            if ref_case is not None
            and ref_case not in spec.supported_ref_cases
            else None
        ),
    )


@dataclasses.dataclass(frozen=True, kw_only=True)
class RefRendering:
    """A reference configuration, target spec and owned fixture."""

    config: RefCaseSpec
    lang_cls: literalizer.LanguageCls
    spec: literalizer.Language
    golden_name: str
    ref_case: literalizer.IdentifierCase | None

    outcome: GoldenOutcome

    def artifact(self, *, cases_dir: Path) -> GoldenArtifact:
        """Locate the fixture used by execution and inventory checks."""
        return make_golden_artifact(
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

    @functools.cached_property
    def renderings(self) -> tuple[RefRendering, ...]:
        """Exercise each selected version under the owner's ref policy."""
        default = self.owner == REF_DEFAULT_OWNER
        ref_case = (
            None
            if default
            else self.config.ref_case_for(lang_cls=self.lang_cls)
        )
        suffix = "ref_default" if default else "ref"
        return tuple(
            RefRendering(
                config=self.config,
                lang_cls=self.lang_cls,
                spec=spec,
                outcome=_reference_outcome(
                    config=self.config,
                    lang_cls=self.lang_cls,
                    spec=spec,
                    ref_case=ref_case,
                    golden_name=f"{self.lang_cls.__name__}_{suffix}",
                ),
                golden_name=f"{self.lang_cls.__name__}_{suffix}",
                ref_case=(
                    None
                    if default
                    else spec.identifier_cases[0]
                    if ref_case is None
                    else ref_case
                ),
            )
            for spec in ref_language_specs(
                config=self.config, lang_cls=self.lang_cls
            )
        )


@functools.cache
@beartype
def discover_literalize_ref_cases(
    *, owner: OwnerName
) -> list[LiteralizeRefCase]:
    """Return reference cases for the selected API owner.

    Backend gates run here. Each rendering checks its own spelling,
    declaration style and native consumer once it has an effective spec.
    """
    return [
        LiteralizeRefCase(config=config, lang_cls=lang_cls, owner=owner)
        for config in ref_case_specs(cases_dir=CASES_DIR, owner=owner)
        if not config.variant_only
        for lang_cls in sorted_languages()
        if config.admits_language(lang_cls=lang_cls)
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

    @functools.cached_property
    def renderings(self) -> tuple[RefRendering, ...]:
        """Retain the exact spec and ref spelling selected by the axis."""
        return (
            RefRendering(
                config=self.config,
                lang_cls=self.lang_cls,
                spec=self.variant.spec,
                outcome=_reference_outcome(
                    config=self.config,
                    lang_cls=self.lang_cls,
                    spec=self.variant.spec,
                    ref_case=self.ref_case,
                    golden_name=self.golden_name,
                ),
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
    spec = ref_language_options(
        config=config, lang_cls=lang_cls, spec=variant.spec
    )
    # A selected declaration variant is an explicit choice. The base
    # suite's automatic mutable-style fallback must not relabel it.
    names = language_metadata(
        language_id=lang_cls.language_id
    ).variants.declaration_style_variable_names
    reference_case = ref_case
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
    kwargs: dict[str, object] = {}
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
            kwargs[name] = enum_member_by_name(enum_cls=enum_cls, name=choice)
    if config.default_sequence_element_type is not None:
        kwargs["default_sequence_element_type"] = (
            config.default_sequence_element_type
        )
    return dataclasses.replace(spec, **kwargs) if len(kwargs) > 0 else spec


@beartype
def ref_language_specs(
    *, config: RefCaseSpec, lang_cls: literalizer.LanguageCls
) -> tuple[literalizer.Language, ...]:
    """Resolve options once and retain one spec per effective version."""
    specs = (
        ref_language_options(
            config=config,
            lang_cls=lang_cls,
            spec=make_spec(lang_cls=lang_cls, language_version=version),
        )
        for version in lang_cls.VersionFormats
    )
    return unique_effective_specs(
        specs=(
            _with_redefinition_style(config=config, spec=spec)
            for spec in specs
        ),
    )


def _with_redefinition_style(
    *, config: RefCaseSpec, spec: literalizer.Language
) -> literalizer.Language:
    """Resolve the mutable-style fallback before checking
    applicability.
    """
    if (
        config.variable_form == "both"
        and config.declaration_style is None
        and not Requirement.REDEFINITION.satisfied_by(spec=spec)
    ):
        styles = find_redefinition_styles(spec=spec)
        if len(styles) > 0:
            return dataclasses.replace(spec, declaration_style=styles[0])
    return spec


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
