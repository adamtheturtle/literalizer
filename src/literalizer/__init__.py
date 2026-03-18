"""Convert data structures to native language literal syntax."""

from literalizer._core import (
    literalize_json,
    literalize_yaml,
)
from literalizer._language import Language, LanguageSpec

__all__ = [
    "Language",
    "LanguageSpec",
    "literalize_json",
    "literalize_yaml",
]
