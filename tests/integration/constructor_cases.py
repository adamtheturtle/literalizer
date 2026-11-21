"""Shared discovery and fixture ownership for constructor bindings."""

import dataclasses
import enum
import functools
from pathlib import Path

from beartype import beartype

from literalizer import Language, NewVariable
from literalizer.exceptions import IncompatibleFormatsError
from literalizer.languages import CSharp

from .case_manifests import (
    CaseManifest,
    CaseManifestError,
    load_case_manifests,
)
from .constructor_variants import (
    ConstructorBindingSpec,
    constructor_binding_specs,
)
from .golden_artifacts import GoldenArtifact
from .golden_outcomes import SUCCESS, Exclusion, GoldenOutcome, Rejection
from .language_specs import make_golden_artifact, sorted_languages
from .scenario_participation import Requirement, scenario_exclusion

CASES_DIR = Path(__file__).parent / "cases"


@dataclasses.dataclass(frozen=True, kw_only=True)
class ConstructorBindingCase(ConstructorBindingSpec):
    """A constructor variant owned by a native fixture manifest."""

    manifest: CaseManifest

    @functools.cached_property
    def consumer_template(self) -> str | None:
        """Resolve the native consumer for a participating backend."""
        config = self.manifest.constructor
        assert config is not None  # noqa: S101
        return config.consumer_for_language(
            language_name=self.lang_cls.__name__
        )

    @functools.cached_property
    def renderings(self) -> tuple["ConstructorRendering", ...]:
        """Expand the versions used by execution and fixture inventory."""
        config = self.manifest.constructor
        assert config is not None  # noqa: S101
        return tuple(
            ConstructorRendering(
                case=self,
                spec=(
                    dataclasses.replace(
                        spec,
                        **{
                            key: value.format(
                                target=spec.format_constructor_target(
                                    config.class_name
                                )
                            )
                            for key, value in config.target_options.items()
                        },
                    )
                    if len(config.target_options) > 0
                    else spec
                ),
            )
            for spec in self.specs
        )


@dataclasses.dataclass(frozen=True, kw_only=True)
class ConstructorRendering:
    """One collected constructor case, version and effective spec."""

    case: ConstructorBindingCase
    spec: Language

    @property
    def version(self) -> enum.Enum:
        """Report the version that owns the fixture."""
        return self.spec.language_version

    @functools.cached_property
    def outcome(self) -> GoldenOutcome:
        """Check constructor applicability before predicting API
        errors.
        """
        config = self.case.manifest.constructor
        assert config is not None  # noqa: S101
        if not config.renders_target:
            exclusion = scenario_exclusion(
                case_id=f"{self.case.manifest.case_dir.name}/{self.case.name}",
                spec=self.spec,
                requirements=(Requirement.CONSTRUCTOR_BINDING,),
                fixture_reason=None,
            )
            if exclusion is not None:
                return exclusion
        form = self.case.variable_form
        if (
            isinstance(self.spec, CSharp)
            and isinstance(form, NewVariable)
            and CSharp.Modifiers["CONST"] in form.modifiers
        ):
            return Rejection(
                error=IncompatibleFormatsError,
                match="const.*cannot bind a runtime call result",
            )
        return SUCCESS

    @property
    def artifact(self) -> GoldenArtifact:
        """Locate the native fixture compared by the constructor
        runner.
        """
        return make_golden_artifact(
            parent=self.case.manifest.case_dir,
            name=self.case.name,
            lang_cls=self.case.lang_cls,
            version=self.spec.language_version,
        )


@beartype
def constructor_binding_cases(
    *, cases_dir: Path
) -> list[ConstructorBindingCase]:
    """Return every declared constructor call-binding variant."""
    manifests = [
        manifest
        for manifest in load_case_manifests(cases_dir=cases_dir)
        if manifest.owner == "constructor-binding"
    ]
    cases: list[ConstructorBindingCase] = []
    for case in constructor_binding_specs():
        owners = tuple(
            manifest
            for manifest in manifests
            if manifest.selection.admits_language(lang_cls=case.lang_cls)
            and manifest.constructor is not None
            and not manifest.constructor.renders_target
        )
        if len(owners) == 0 and any(
            Requirement.CONSTRUCTOR_BINDING.satisfied_by(spec=spec)
            for spec in case.specs
        ):
            msg = (
                f"constructor binding {case.name!r} "
                "has no native fixture owner"
            )
            raise CaseManifestError(msg)
        for manifest in owners:
            owned_case = ConstructorBindingCase(
                name=case.name,
                lang_cls=case.lang_cls,
                spec_overrides=case.spec_overrides,
                variable_form=case.variable_form,
                manifest=manifest,
            )
            if any(
                not isinstance(rendering.outcome, Exclusion)
                for rendering in owned_case.renderings
            ):
                _ = owned_case.consumer_template
                cases.append(owned_case)
    for manifest in manifests:
        config = manifest.constructor
        if config is not None and config.renders_target:
            for lang_cls in sorted_languages():
                if not manifest.selection.admits_language(lang_cls=lang_cls):
                    continue
                cases.append(
                    ConstructorBindingCase(
                        name=f"{lang_cls.__name__}_constructor_target",
                        lang_cls=lang_cls,
                        spec_overrides={},
                        variable_form=NewVariable(
                            name="p", modifiers=frozenset()
                        ),
                        manifest=manifest,
                    )
                )
    return cases
