"""Generated fixture metadata shared by corpus tools."""

import dataclasses
import enum
from pathlib import Path

from literalizer import LanguageCls


@dataclasses.dataclass(frozen=True, kw_only=True)
class GoldenArtifact:
    """One generated fixture and the effective target that produced it."""

    path: Path
    language: LanguageCls
    version: enum.Enum
