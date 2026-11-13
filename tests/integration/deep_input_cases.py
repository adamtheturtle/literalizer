"""Manifest-owned source recipes for compiling deep-input consumers."""

import dataclasses
import tomllib
from pathlib import Path

from pydantic import BaseModel, Field

from .case_manifests import (
    CaseManifest,
    load_case_manifests,
)
from .language_specs import make_golden_path
from .manifest_values import (
    CallInputFormat,
    ManifestLanguage,
)


class DeepInputRecipe(
    BaseModel, arbitrary_types_allowed=True, extra="forbid", frozen=True
):
    """Flat metadata avoids the nesting limit during input discovery."""

    language: ManifestLanguage
    input_format: CallInputFormat
    opener: str
    closer: str
    depth: int = Field(gt=0)
    payload: str
    consumer_template: str

    @property
    def source(self) -> str:
        """Build the original source without recursively walking its
        values.
        """
        return (
            self.opener * self.depth + self.payload + self.closer * self.depth
        )


@dataclasses.dataclass(frozen=True)
class DeepInputCase:
    """One owned input recipe and its complete native consumer."""

    manifest: CaseManifest
    recipe: DeepInputRecipe

    @property
    def golden_path(self) -> Path:
        """Own the native file for the original default language
        version.
        """
        language = self.recipe.language
        return make_golden_path(
            parent=self.manifest.case_dir,
            name=f"{language.__name__}_unwrapped_depth",
            lang_cls=language,
            version=language().language_version,
        )


def deep_input_cases(*, cases_dir: Path) -> tuple[DeepInputCase, ...]:
    """Discover every deep-input recipe through its declared owner."""
    return tuple(
        DeepInputCase(
            manifest=manifest,
            recipe=DeepInputRecipe.model_validate(
                obj=tomllib.loads(
                    manifest.input.path.read_text(encoding="utf-8")
                )
            ),
        )
        for manifest in load_case_manifests(cases_dir=cases_dir)
        if manifest.owner == "deep-input"
    )


def deep_input_golden_paths(*, cases_dir: Path) -> set[Path]:
    """Include every declared native program in the orphan inventory."""
    return {case.golden_path for case in deep_input_cases(cases_dir=cases_dir)}
