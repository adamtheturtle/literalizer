"""Shared discovery and fixture ownership for constructor bindings."""

import dataclasses
import enum
from pathlib import Path

from beartype import beartype

from literalizer import NewVariable

from .case_manifests import (
    CaseManifest,
    CaseManifestError,
    load_case_manifests,
)
from .constructor_variants import (
    ConstructorBindingSpec,
    constructor_binding_specs,
)
from .golden_checks import NO_SKIPS
from .language_specs import make_golden_path, sorted_languages

CASES_DIR = Path(__file__).parent / "cases"


@dataclasses.dataclass(frozen=True, kw_only=True)
class ConstructorBindingCase(ConstructorBindingSpec):
    """A constructor variant owned by a native fixture manifest."""

    manifest: CaseManifest


@beartype
def constructor_golden_path(
    *,
    case: ConstructorBindingCase,
    version: enum.Enum,
) -> Path:
    """Locate the variant's native golden file."""
    return make_golden_path(
        parent=case.manifest.case_dir,
        name=case.name,
        lang_cls=case.lang_cls,
        version=version,
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
            and manifest.constructor.target_template is None
        )
        if len(owners) == 0:
            msg = (
                f"constructor binding {case.name!r} "
                "has no native fixture owner"
            )
            raise CaseManifestError(msg)
        cases.extend(
            ConstructorBindingCase(
                name=case.name,
                lang_cls=case.lang_cls,
                spec_overrides=case.spec_overrides,
                variable_form=case.variable_form,
                skip=case.skip,
                manifest=manifest,
            )
            for manifest in owners
        )
    for manifest in manifests:
        config = manifest.constructor
        if config is not None and config.target_template is not None:
            cases.extend(
                ConstructorBindingCase(
                    name=f"{lang_cls.__name__}_constructor_target",
                    lang_cls=lang_cls,
                    spec_overrides={},
                    variable_form=NewVariable(name="p", modifiers=frozenset()),
                    skip=NO_SKIPS,
                    manifest=manifest,
                )
                for lang_cls in sorted_languages()
                if manifest.selection.admits_language(lang_cls=lang_cls)
            )
    return cases
