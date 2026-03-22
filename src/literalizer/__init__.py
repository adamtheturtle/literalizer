"""Convert data structures to native language literal syntax."""

from literalizer._core import (
    LiteralizeResult,
    literalize_json,
    literalize_yaml,
)
from literalizer._formatters import fixed_dict_open, fixed_sequence_open
from literalizer._language import (
    CommentConfig,
    DictFormatConfig,
    Language,
    LanguageCls,
    OrderedMapFormatConfig,
    SequenceFormatConfig,
    SetFormatConfig,
)

__all__ = [
    "CommentConfig",
    "DictFormatConfig",
    "Language",
    "LanguageCls",
    "LiteralizeResult",
    "OrderedMapFormatConfig",
    "SequenceFormatConfig",
    "SetFormatConfig",
    "fixed_dict_open",
    "fixed_sequence_open",
    "literalize_json",
    "literalize_yaml",
]
