"""Manifest-owned consumers of genuine native invocation syntax."""

import dataclasses
import enum
from pathlib import Path

import literalizer
from literalizer.languages import ALL_LANGUAGES

from .case_manifests import (
    CaseManifest,
    load_case_manifests,
)
from .language_specs import make_golden_path


@dataclasses.dataclass(frozen=True, kw_only=True)
class NativeInvocationCase:
    """A manifest and language version with its native consumer
    fixture.
    """

    manifest: CaseManifest
    lang_cls: literalizer.LanguageCls
    version: enum.Enum
    golden_path: Path

    @property
    def test_id(self) -> str:
        """Identify the input, language, and version in pytest output."""
        return (
            f"{self.manifest.case_dir.name}/"
            f"{self.lang_cls.__name__}/{self.version.name}"
        )


def native_invocation_cases(*, cases_dir: Path) -> list[NativeInvocationCase]:
    """Discover every manifest/version that declares native support."""
    return [
        NativeInvocationCase(
            manifest=manifest,
            lang_cls=language,
            version=version,
            golden_path=make_golden_path(
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
