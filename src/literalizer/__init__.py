"""Convert data structures to native language literal syntax."""

from literalizer._core import (
    LiteralizeResult,
    literalize_json,
    literalize_yaml,
)
from literalizer._formatters import (
    fixed_dict_open,
    fixed_sequence_open,
    fixed_set_open,
)
from literalizer._language import (
    CommentConfig,
    DateFormatConfig,
    DatetimeFormatConfig,
    DictFormatConfig,
    Language,
    LanguageCls,
    OrderedMapFormatConfig,
    SequenceFormatConfig,
    SetFormatConfig,
    TrailingCommaConfig,
)

__all__ = [
    "CommentConfig",
    "DateFormatConfig",
    "DatetimeFormatConfig",
    "DictFormatConfig",
    "Language",
    "LanguageCls",
    "LiteralizeResult",
    "OrderedMapFormatConfig",
    "SequenceFormatConfig",
    "SetFormatConfig",
    "TrailingCommaConfig",
    "fixed_dict_open",
    "fixed_sequence_open",
    "fixed_set_open",
    "literalize_json",
    "literalize_yaml",
]
