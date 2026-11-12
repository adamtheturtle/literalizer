"""Owned complete consumers of shared result-check recipes."""

import dataclasses
import enum
import tomllib
from pathlib import Path

from pydantic import BaseModel

from literalizer.languages import Python

from .case_manifests import load_case_manifests
from .language_specs import make_golden_path


class CheckedRecipe(BaseModel, extra="forbid", frozen=True):
    """Original source rows, paired expected values and caller program."""

    source: str
    zip_source: str
    pre_indent_level: int
    invocation: dict[str, object]
    consumer_template: str


@dataclasses.dataclass(frozen=True)
class SharedCheckedCase:
    """One declared caller program and its Python target version."""

    name: str
    recipe: CheckedRecipe
    version: enum.Enum
    golden_path: Path


def shared_checked_cases(*, cases_dir: Path) -> tuple[SharedCheckedCase, ...]:
    """Discover and own every declared complete checked-call consumer."""
    return tuple(
        SharedCheckedCase(
            name=manifest.case_dir.name,
            recipe=CheckedRecipe.model_validate(
                obj=tomllib.loads(
                    manifest.input.path.read_text(encoding="utf-8")
                )
            ),
            version=version,
            golden_path=make_golden_path(
                parent=manifest.case_dir,
                name="Python_shared_checked",
                lang_cls=Python,
                version=version,
            ),
        )
        for manifest in load_case_manifests(cases_dir=cases_dir)
        if manifest.owner == "shared-invocation"
        and manifest.selection.admits_language(lang_cls=Python)
        for version in Python.VersionFormats
    )
