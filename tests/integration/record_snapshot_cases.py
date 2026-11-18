"""Declared consumers of caller-owned record-name snapshots."""

import enum
import tomllib
from collections.abc import Iterator
from pathlib import Path

from pydantic import BaseModel, TypeAdapter

from literalizer.languages import Rust

from .golden_artifacts import GoldenArtifact
from .golden_renderings import GoldenRendering
from .golden_scenarios import scenario_renderings
from .language_specs import make_golden_artifact


class RecordSnapshotCase(BaseModel, extra="forbid", frozen=True):
    """A named record seed, caller mutations and native consumer."""

    name: str
    case_name: str
    seed_golden_name: str
    golden_name: str
    parent_fields: frozenset[str]
    parent_name: str
    child_name: str
    consumer_template: str

    def artifact(
        self, *, cases_dir: Path, version: enum.Enum
    ) -> GoldenArtifact:
        """Locate the native fixture for one target version."""
        return make_golden_artifact(
            parent=cases_dir / self.case_name,
            name=self.golden_name,
            lang_cls=Rust,
            version=version,
        )


RECORD_SNAPSHOT_CASES: tuple[RecordSnapshotCase, ...] = TypeAdapter(
    type=tuple[RecordSnapshotCase, ...]
).validate_python(
    tomllib.loads(
        Path(__file__).with_suffix(suffix=".toml").read_text(encoding="utf-8")
    )["cases"]
)


def snapshot_rendering(*, case: RecordSnapshotCase) -> GoldenRendering:
    """Reuse the exact named-record seed from the original runtime
    test.
    """
    return next(
        rendering
        for rendering in scenario_renderings()["format_variant", Rust]
        if rendering.case_dir_name == case.case_name
        and rendering.golden_name == case.seed_golden_name
    )


def record_snapshot_artifacts(*, cases_dir: Path) -> Iterator[GoldenArtifact]:
    """Own every native program produced from the declared snapshot
    cases.
    """
    return (
        case.artifact(cases_dir=cases_dir, version=spec.language_version)
        for case in RECORD_SNAPSHOT_CASES
        for spec in snapshot_rendering(case=case).specs
    )
