"""Input-file discovery shared by integration golden harnesses."""

import dataclasses
from pathlib import Path

from beartype import beartype
from pydantic import BaseModel, Field

import literalizer

_INPUT_FORMATS = {
    "input.json": literalizer.InputFormat.JSON,
    "input.jsonc": literalizer.InputFormat.JSONC,
    "input.json5": literalizer.InputFormat.JSON5,
    "input.toml": literalizer.InputFormat.TOML,
    "input.yaml": literalizer.InputFormat.YAML,
}


class ReusedAnchorWarningSpec(
    BaseModel, extra="forbid", frozen=True, strict=True
):
    """The anchor and warning count a YAML fixture deliberately
    produces.
    """

    anchor: str = Field(min_length=1)
    count: int = Field(gt=0)


@dataclasses.dataclass(frozen=True, kw_only=True)
class CaseInput:
    """The input file backing a golden-file case."""

    path: Path
    input_format: literalizer.InputFormat
    expected_reused_anchor_warning: ReusedAnchorWarningSpec | None


@beartype
def infer_case_input(
    *,
    case_dir: Path,
    input_name: str | None,
    expected_reused_anchor_warning: ReusedAnchorWarningSpec | None,
) -> CaseInput:
    """Resolve a manifest's explicit input or infer its sole input
    file.
    """
    if input_name is not None:
        if input_name not in _INPUT_FORMATS:
            msg = (
                f"input must name one of {sorted(_INPUT_FORMATS)}, "
                f"got {input_name!r}"
            )
            raise ValueError(msg)
        path = case_dir / input_name
        if not path.is_file():
            msg = f"declared input does not exist: {path}"
            raise ValueError(msg)
        return CaseInput(
            path=path,
            input_format=_INPUT_FORMATS[input_name],
            expected_reused_anchor_warning=expected_reused_anchor_warning,
        )

    candidates = [
        CaseInput(
            path=case_dir / name,
            input_format=input_format,
            expected_reused_anchor_warning=expected_reused_anchor_warning,
        )
        for name, input_format in _INPUT_FORMATS.items()
        if (case_dir / name).is_file()
    ]
    if len(candidates) != 1:
        names = [candidate.path.name for candidate in candidates]
        msg = f"expected exactly one inferable input file, found {names}"
        raise ValueError(msg)
    return candidates[0]
