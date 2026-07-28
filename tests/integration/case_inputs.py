"""Input-file discovery shared by integration golden harnesses."""

import dataclasses
from pathlib import Path

from beartype import beartype

import literalizer


@dataclasses.dataclass(frozen=True, kw_only=True)
class CaseInput:
    """The input file backing a golden-file case."""

    path: Path
    input_format: literalizer.InputFormat


@beartype
def case_input(*, case_dir: Path) -> CaseInput:
    """Return the sole input file and serialization format for a case.

    Cases use ``input.yaml`` by default.  Format-specific cases may use
    ``input.json``, ``input.json5``, or ``input.toml`` instead.
    """
    json_path = case_dir / "input.json"
    if json_path.exists():
        return CaseInput(
            path=json_path,
            input_format=literalizer.InputFormat.JSON,
        )
    json5_path = case_dir / "input.json5"
    if json5_path.exists():
        return CaseInput(
            path=json5_path,
            input_format=literalizer.InputFormat.JSON5,
        )
    toml_path = case_dir / "input.toml"
    if toml_path.exists():
        return CaseInput(
            path=toml_path,
            input_format=literalizer.InputFormat.TOML,
        )
    return CaseInput(
        path=case_dir / "input.yaml",
        input_format=literalizer.InputFormat.YAML,
    )
