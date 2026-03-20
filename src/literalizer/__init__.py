"""Convert data structures to native language literal syntax."""

from literalizer._core import (
    literalize_json,
    literalize_yaml,
)
from literalizer._formatters import fixed_dict_open, fixed_sequence_open
from literalizer._language import Language, LanguageSpec
from literalizer.exceptions import HeterogeneousCoercionError

__all__ = [
    "HeterogeneousCoercionError",
    "Language",
    "LanguageSpec",
    "fixed_dict_open",
    "fixed_sequence_open",
    "literalize_json",
    "literalize_yaml",
]
