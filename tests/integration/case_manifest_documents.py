"""Load the TOML shared by manifest validation and fixture paths."""

import functools
import tomllib
from collections.abc import Mapping
from pathlib import Path

MANIFEST_NAME = "case.toml"


@functools.cache
def read_case_manifest_document(*, path: Path) -> Mapping[str, object]:
    """Read a case manifest once for the lifetime of the process."""
    with path.open(mode="rb") as source:
        return tomllib.load(source)
