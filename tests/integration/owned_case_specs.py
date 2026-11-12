"""Case and example identity shared by owned manifest tables."""

from collections.abc import Mapping
from typing import Annotated

from pydantic import BaseModel, Field, ValidationInfo, model_validator


class OwnedCaseSpec(
    BaseModel,
    arbitrary_types_allowed=True,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """Base for an owner-scoped manifest table that knows its case.

    The directory name identifies the case on disk rather than being
    manifest data, so :func:`load_case_manifest` supplies it through the
    validation context instead of a second construction step.
    """

    # Supplied by the loader through the validation context rather than
    # by the manifest, so a case's directory name stays a single source
    # of truth on disk.
    case_dir_name: str
    example: Annotated[str, Field(pattern=r"^[a-z][a-z0-9_]*$")] | None

    @property
    def coverage_id(self) -> str:
        """Identify an example without changing its shared input owner."""
        if self.example is None:
            return self.case_dir_name
        return f"{self.case_dir_name}/{self.example}"

    def golden_name(self, *, name: str) -> str:
        """Keep named examples distinct from the shared default golden."""
        if self.example is None:
            return name
        return f"{name}_{self.example}"

    @model_validator(mode="before")
    @classmethod
    def _add_case_dir_name(
        cls,
        data: Mapping[str, object],
        info: ValidationInfo[Mapping[str, str] | None],
    ) -> Mapping[str, object]:
        """Add the owning case directory name from the load context."""
        raw_context = info.context
        context: Mapping[str, str]
        context = dict[str, str]() if raw_context is None else raw_context
        return {
            "example": None,
            **data,
            "case_dir_name": context["case_dir_name"],
        }
