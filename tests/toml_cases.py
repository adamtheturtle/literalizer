"""Load declarative unit-test cases from TOML files."""

import tomllib
from pathlib import Path


def load_toml_cases(*, name: str) -> dict[str, object]:
    """Return the parsed unit-case document named *name*."""
    path = Path(__file__).parent / "unit_cases" / f"{name}.toml"
    return tomllib.loads(path.read_text(encoding="utf-8"))
