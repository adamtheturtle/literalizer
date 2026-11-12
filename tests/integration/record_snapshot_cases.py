"""Declared consumers of caller-owned record-name snapshots."""

import tomllib
from pathlib import Path

from pydantic import BaseModel, TypeAdapter

from literalizer.languages import Rust

from .golden_scenarios import GoldenRendering, golden_groups
from .language_specs import make_golden_path


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


RECORD_SNAPSHOT_CASES = TypeAdapter(
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
        for group in golden_groups()
        if group.scenario_name == "format_variant" and group.lang_cls is Rust
        for rendering in group.renderings
        if rendering.case_dir_name == case.case_name
        and rendering.golden_name == case.seed_golden_name
    )


def record_snapshot_golden_paths(*, cases_dir: Path) -> set[Path]:
    """Own every native program produced from the declared snapshot
    cases.
    """
    return {
        make_golden_path(
            parent=cases_dir / case.case_name,
            name=case.golden_name,
            lang_cls=Rust,
            version=version,
        )
        for case in RECORD_SNAPSHOT_CASES
        for version in snapshot_rendering(case=case).versions
    }
