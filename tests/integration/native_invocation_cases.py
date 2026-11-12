"""Manifest-owned consumers of genuine native invocation syntax."""

import enum
from pathlib import Path

import literalizer
from literalizer.languages import ALL_LANGUAGES

from .case_manifests import (
    CaseManifest,
    load_case_manifests,
)
from .language_specs import make_golden_path


def native_invocation_cases(
    *, cases_dir: Path
) -> list[tuple[CaseManifest, literalizer.LanguageCls, enum.Enum, Path]]:
    """Discover every manifest/version that declares native support."""
    return [
        (
            manifest,
            language,
            version,
            make_golden_path(
                parent=manifest.case_dir,
                name=f"{language.__name__}_native_invocations",
                lang_cls=language,
                version=version,
            ),
        )
        for manifest in load_case_manifests(cases_dir=cases_dir)
        if manifest.native_invocation is not None
        for language in ALL_LANGUAGES
        if language.supports_native_invocations
        and manifest.selection.admits_language(lang_cls=language)
        for version in language.VersionFormats
    ]
