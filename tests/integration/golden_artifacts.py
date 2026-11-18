"""Generated fixture metadata shared by corpus tools."""

import dataclasses
import enum
from pathlib import Path

from literalizer import LanguageCls


@dataclasses.dataclass(frozen=True, kw_only=True)
class GoldenArtifact:
    """One generated fixture, its owning case and its effective target."""

    path: Path
    case_name: str
    language: LanguageCls
    version: enum.Enum
