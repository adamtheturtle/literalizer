"""Load and validate case-local golden coverage manifests."""

from __future__ import annotations

import dataclasses
import functools
import tomllib
from collections.abc import Mapping  # noqa: TC003
from pathlib import Path  # noqa: TC003
from typing import Annotated, Literal

from beartype import beartype
from pydantic import BaseModel, Field, ValidationError

import literalizer
from literalizer._types import ValueInput  # noqa: TC001

from .case_inputs import CaseInput, infer_case_input
from .variant_axis_names import KNOWN_VARIANT_AXES

MANIFEST_NAME = "case.toml"

type VariableFormName = Literal["new", "existing", "both"]
type CollectionLayoutName = Literal["compact", "multiline"]
type SuiteName = Literal["base", "combined"]
type OwnerName = Literal[
    "literalize-call",
    "literalize-ref",
    "literalize-ref-default",
    "new-variable-kebab",
    "new-variable-prime",
    "variant",
]


def _empty_suites() -> list[SuiteName]:
    """Return a typed empty suite list for the validation model."""
    return []


_VARIABLE_FORMS_BY_NAME: Mapping[
    VariableFormName, literalizer.VariableForm
] = {
    "new": literalizer.NewVariable(name="my_data", modifiers=frozenset()),
    "existing": literalizer.ExistingVariable(name="my_data"),
    "both": literalizer.BothVariableForms(
        name="my_data",
        modifiers=frozenset(),
    ),
}


class CaseManifestError(ValueError):
    """A case manifest is invalid or internally inconsistent."""


class RenderContext(
    BaseModel,
    arbitrary_types_allowed=True,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """Simple render arguments declared by a case rather than a runner."""

    variable_form: VariableFormName = "new"
    collection_layout: CollectionLayoutName | None = None
    pre_indent_level: Annotated[int, Field(ge=0)] = 0
    record_null_substitutions: Mapping[str, ValueInput] | None = None


class ManifestVariant(
    BaseModel,
    arbitrary_types_allowed=True,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """One input's participation in a named, typed variant axis."""

    axis: Annotated[str, Field(min_length=1)]
    suffix: str = ""
    context: RenderContext = Field(default_factory=RenderContext)


def _empty_variants() -> list[ManifestVariant]:
    """Return a typed empty variant list for the validation model."""
    return []


class _CaseManifestData(
    BaseModel,
    arbitrary_types_allowed=True,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """Strict representation of the data read directly from TOML."""

    schema_version: Literal[1]
    input: str | None = None
    suites: list[SuiteName] = Field(default_factory=_empty_suites)
    owner: OwnerName | None = None
    base_context: RenderContext = Field(default_factory=RenderContext)
    variants: list[ManifestVariant] = Field(default_factory=_empty_variants)

    def validate_consistency(self) -> None:
        """Validate relationships that span manifest fields."""
        if len(self.suites) != len(set(self.suites)):
            msg = "suites contains a duplicate entry"
            raise ValueError(msg)
        if self.suites and self.owner is not None:
            msg = "suites and owner are mutually exclusive"
            raise ValueError(msg)
        if not self.suites and self.owner is None:
            msg = "declare suites or a specialized owner"
            raise ValueError(msg)
        if (
            "base_context" in self.model_fields_set
            and "base" not in self.suites
        ):
            msg = "base_context requires participation in the base suite"
            raise ValueError(msg)

        logical_cases = [(entry.axis, entry.suffix) for entry in self.variants]
        if len(logical_cases) != len(set(logical_cases)):
            msg = "duplicate logical variant case"
            raise ValueError(msg)
        for entry in self.variants:
            if entry.axis not in KNOWN_VARIANT_AXES:
                msg = f"unknown variant axis {entry.axis!r}"
                raise ValueError(msg)


@dataclasses.dataclass(frozen=True, kw_only=True)
class CaseManifest:
    """Validated coverage and input metadata for one case directory."""

    path: Path
    case_dir: Path
    schema_version: Literal[1]
    input: CaseInput
    suites: frozenset[SuiteName]
    owner: OwnerName | None
    base_context: RenderContext
    variants: tuple[ManifestVariant, ...]


@beartype
def variable_form_for_context(
    *, context: RenderContext
) -> literalizer.VariableForm:
    """Translate a validated manifest variable-form name to the API
    type.
    """
    return _VARIABLE_FORMS_BY_NAME[context.variable_form]


def _fail(*, path: Path, message: str) -> CaseManifestError:
    """Build a manifest error containing its source path."""
    return CaseManifestError(f"{path}: {message}")


def _load_manifest_data(*, path: Path) -> _CaseManifestData:
    """Parse and structurally validate one manifest file."""
    try:
        raw = tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        raise _fail(path=path, message=f"invalid TOML: {exc}") from exc

    try:
        data = _CaseManifestData.model_validate(obj=raw)
        data.validate_consistency()
    except (ValidationError, ValueError) as exc:
        raise _fail(path=path, message=str(object=exc)) from exc
    return data


@functools.cache
@beartype
def load_case_manifest(case_dir: Path) -> CaseManifest:
    """Return one fully validated ``case.toml`` manifest."""
    path = case_dir / MANIFEST_NAME
    if not path.is_file():
        raise _fail(path=path, message="manifest is missing")
    data = _load_manifest_data(path=path)
    try:
        input_info = infer_case_input(
            case_dir=case_dir,
            input_name=data.input,
        )
    except ValueError as exc:
        raise _fail(path=path, message=str(object=exc)) from exc

    return CaseManifest(
        path=path,
        case_dir=case_dir,
        schema_version=data.schema_version,
        input=input_info,
        suites=frozenset(data.suites),
        owner=data.owner,
        base_context=data.base_context,
        variants=tuple(data.variants),
    )


@beartype
def case_input(*, case_dir: Path) -> CaseInput:
    """Return the input declared by the case-local manifest."""
    return load_case_manifest(case_dir=case_dir).input


@functools.cache
@beartype
def load_case_manifests(cases_dir: Path) -> tuple[CaseManifest, ...]:
    """Load every case manifest in stable directory-name order."""
    case_dirs = sorted(path for path in cases_dir.iterdir() if path.is_dir())
    return tuple(
        load_case_manifest(case_dir=case_dir) for case_dir in case_dirs
    )


@functools.cache
@beartype
def case_manifests_by_name(cases_dir: Path) -> Mapping[str, CaseManifest]:
    """Return the shared manifest inventory keyed by case directory
    name.
    """
    return {
        manifest.case_dir.name: manifest
        for manifest in load_case_manifests(cases_dir=cases_dir)
    }
