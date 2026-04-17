"""Convert data structures to native language literal syntax."""

from literalizer._core import (
    BothVariableForms,
    ExistingVariable,
    InputFormat,
    LiteralizeResult,
    NewVariable,
    VariableForm,
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

__all__ = [
    "BothVariableForms",
    "CallStyleConfig",
    "CallStyleKind",
    "CommentConfig",
    "DateFormatConfig",
    "DatetimeFormatConfig",
    "DictFormatConfig",
    "ExistingVariable",
    "InputFormat",
    "Language",
    "LanguageCls",
    "LiteralizeResult",
    "NewVariable",
    "OrderedMapFormatConfig",
    "SequenceFormatConfig",
    "SetFormatConfig",
    "TrailingCommaConfig",
    "VariableForm",
    "fixed_dict_open",
    "fixed_sequence_open",
    "fixed_set_open",
    "literalize",
    "literalize_call",
]
