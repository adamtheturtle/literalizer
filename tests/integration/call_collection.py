"""Collect call cases and versioned rendering records."""

import dataclasses
import functools
from pathlib import Path

from beartype import beartype

import literalizer
from literalizer._enums import enum_payload
from literalizer.exceptions import ExistingVariableNotSelfContainedError

from .call_expectations import (
    call_style_spec,
    expected_call_shape_exception,
    fixture_rejection,
    wrapped_call_needs_prior_binding,
    wrapper_capability_exclusion,
)
from .call_receivers import uses_integer_receiver
from .case_manifests import CallCaseSpec, WrappedCallFixture, call_case_specs
from .golden_artifacts import GoldenArtifact
from .golden_outcomes import SUCCESS, GoldenOutcome, Rejection
from .language_specs import (
    make_golden_artifact,
    make_spec,
    sorted_languages,
    unique_effective_specs,
)
from .scenario_participation import scenario_exclusion

CASES_DIR = Path(__file__).parent / "cases"


@dataclasses.dataclass(frozen=True, kw_only=True)
class CallRendering:
    """One call configuration, effective spec and expected outcome."""

    config: CallCaseSpec
    lang_cls: literalizer.LanguageCls
    spec: literalizer.Language
    golden_name: str
    expected_exception: type[Exception] | None

    @functools.cached_property
    def observable(self) -> bool:
        """Select the fixture's native consumer once for this spec."""
        return uses_integer_receiver(config=self.config, spec=self.spec)

    @property
    def outcome(self) -> GoldenOutcome | None:
        """Share the resolved result with discovery and execution."""
        return self._resolved_outcome

    @functools.cached_property
    def _resolved_outcome(self) -> GoldenOutcome | None:
        """Report documented errors and exclusions before rendering.

        A missing outcome leaves the call in the legacy runner until its
        representation constraints have been migrated.
        """
        if not self.observable:
            exclusion = scenario_exclusion(
                case_id=f"{self.config.coverage_id}/{self.golden_name}",
                spec=self.spec,
                requirements=(),
                fixture_reason=wrapper_capability_exclusion(
                    config=self.config, lang_cls=self.lang_cls, spec=self.spec
                ),
            )
            if exclusion is not None:
                return exclusion
        if self.expected_exception is not None:
            return Rejection(
                error=fixture_rejection(
                    config=self.config,
                    spec=self.spec,
                    predicted=self.expected_exception,
                ),
                match=None,
            )
        if wrapped_call_needs_prior_binding(
            config=self.config, spec=self.spec
        ):
            return Rejection(
                error=ExistingVariableNotSelfContainedError,
                match="the assignment has no prior declaration",
            )
        if isinstance(self.config.fixture, WrappedCallFixture) and isinstance(
            self.config.variable_form, literalizer.ExistingVariable
        ):
            return SUCCESS
        return None

    def artifact(self, *, cases_dir: Path) -> GoldenArtifact:
        """Return the fixture used for comparison and stale-file
        cleanup.
        """
        return make_golden_artifact(
            parent=cases_dir / self.config.case_dir_name,
            name=self.config.golden_name(name=self.golden_name),
            lang_cls=self.lang_cls,
            version=self.spec.language_version,
        )


def resolve_call_rendering(
    *,
    config: CallCaseSpec,
    lang_cls: literalizer.LanguageCls,
    spec: literalizer.Language,
    golden_name: str,
) -> CallRendering:
    """Predict the API outcome from the same spec execution receives."""
    return CallRendering(
        config=config,
        lang_cls=lang_cls,
        spec=spec,
        golden_name=golden_name,
        expected_exception=expected_call_shape_exception(
            lang_cls=lang_cls, config=config, spec=spec
        ),
    )


@dataclasses.dataclass(frozen=True)
class CallCase:
    """A parameterized call-style golden-file test case."""

    config: CallCaseSpec
    lang_cls: literalizer.LanguageCls

    @property
    def test_id(self) -> str:
        """Return the manifest and language identity of this case."""
        return f"{self.config.coverage_id}/{self.lang_cls.__name__}"

    @functools.cached_property
    def renderings(self) -> tuple[CallRendering, ...]:
        """Exercise the default call once per supported language
        version.
        """
        specs = unique_effective_specs(
            specs=(
                call_style_spec(
                    config=self.config,
                    lang_cls=self.lang_cls,
                    spec=make_spec(
                        lang_cls=self.lang_cls, language_version=version
                    ),
                )
                for version in self.lang_cls.VersionFormats
            ),
        )
        return tuple(
            resolve_call_rendering(
                config=self.config,
                lang_cls=self.lang_cls,
                spec=spec,
                golden_name=f"{self.lang_cls.__name__}_call",
            )
            for spec in specs
        )


@functools.cache
@beartype
def default_call_case_specs() -> tuple[CallCaseSpec, ...]:
    """Return every call case driven by the default per-language
    matrix.
    """
    return tuple(
        spec
        for spec in call_case_specs(cases_dir=CASES_DIR)
        if not spec.variant_only
    )


@functools.cache
@beartype
def discover_call_cases() -> list[CallCase]:
    """Return call test cases for all languages."""
    cases: list[CallCase] = []
    for config in default_call_case_specs():
        for lang_cls in sorted_languages():
            if not config.admits_language(lang_cls=lang_cls):
                continue
            if len(lang_cls.CallStyles) == 0:
                continue
            if (
                config.requires_heterogeneous_dict_values
                and not lang_cls.dict_supports_heterogeneous_values
            ):
                continue
            if config.call_style_type is not None:
                # Only include languages that have this as a
                # non-default style.
                styles = iter(lang_cls.CallStyles)
                if isinstance(
                    enum_payload(member=next(styles), payload_type=object),
                    config.call_style_type,
                ) or not any(
                    isinstance(
                        enum_payload(member=style, payload_type=object),
                        config.call_style_type,
                    )
                    for style in styles
                ):
                    continue
            cases.append(CallCase(config=config, lang_cls=lang_cls))
    return cases
