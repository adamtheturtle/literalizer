"""Input-file discovery shared by integration golden harnesses."""

import dataclasses
from pathlib import Path

from beartype import beartype

import literalizer

_INPUT_FORMATS = {
    "input.json": literalizer.InputFormat.JSON,
    "input.json5": literalizer.InputFormat.JSON5,
    "input.toml": literalizer.InputFormat.TOML,
    "input.yaml": literalizer.InputFormat.YAML,
}


@dataclasses.dataclass(frozen=True, kw_only=True)
class CaseInput:
    """The input file backing a golden-file case."""

    path: Path
    input_format: literalizer.InputFormat


@beartype
def infer_case_input(
    *, case_dir: Path, input_name: str | None = None
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
        return CaseInput(path=path, input_format=_INPUT_FORMATS[input_name])

    candidates = [
        CaseInput(path=case_dir / name, input_format=input_format)
        for name, input_format in _INPUT_FORMATS.items()
        if (case_dir / name).is_file()
    ]
    if len(candidates) != 1:
        names = [candidate.path.name for candidate in candidates]
        msg = f"expected exactly one inferable input file, found {names}"
        raise ValueError(msg)
    return candidates[0]


@beartype
def case_input(*, case_dir: Path) -> CaseInput:
    """Return the input declared by the case-local manifest."""
    # Local import avoids a module cycle: manifests use ``CaseInput`` while
    # every harness continues to use this small compatibility entry point.
    from .case_manifests import load_case_manifest  # noqa: PLC0415

    return load_case_manifest(case_dir=case_dir).input
