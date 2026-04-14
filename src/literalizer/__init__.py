"""Convert data structures to native language literal syntax."""

from literalizer._core import (
    InputFormat,
    LiteralizeResult,
    literalize,
    literalize_call,
)
from literalizer._formatters.collection_openers import (
    fixed_dict_open,
    fixed_sequence_open,
    fixed_set_open,
)
from literalizer._language import (
    CallStyleConfig,
    CallStyleKind,
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
from literalizer.exceptions import UnsupportedCallStyleError

__all__ = [
    "CallStyleConfig",
    "CallStyleKind",
    "CommentConfig",
    "DateFormatConfig",
    "DatetimeFormatConfig",
    "DictFormatConfig",
    "InputFormat",
    "Language",
    "LanguageCls",
    "LiteralizeResult",
    "OrderedMapFormatConfig",
    "SequenceFormatConfig",
    "SetFormatConfig",
    "TrailingCommaConfig",
    "UnsupportedCallStyleError",
    "fixed_dict_open",
    "fixed_sequence_open",
    "fixed_set_open",
    "literalize",
    "literalize_call",
]
