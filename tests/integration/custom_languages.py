"""Custom language implementations exercised by compiling golden
variants.
"""

import dataclasses
from collections.abc import Callable
from functools import cached_property
from typing import ClassVar, override

from beartype import beartype

from literalizer import DictFormatConfig
from literalizer._formatters.collection_openers import typed_collection_open
from literalizer._formatters.type_inference import DictType, ListType
from literalizer._types import Scalar, Value
from literalizer.languages import Go, Zig

from .variant_types import Variant, compact_variant


@dataclasses.dataclass(frozen=True, kw_only=True)
class CallbackGo(Go):
    """Use ordinary callbacks through the language extension
    contract.
    """

    plain_callbacks: bool

    @cached_property
    @override
    def sequence_open(self) -> Callable[[list[Value]], str]:
        """Expose an ordinary sequence callback."""
        native = Go(language_version=self.language_version)
        if self.plain_callbacks:
            return lambda items: str(object=native.sequence_open(items))

        def _type_open(_element_type: type | ListType | DictType) -> str:
            """Provide the extension's integer collection opener."""
            return "[]int{"

        return typed_collection_open(
            type_to_opener=_type_open, fallback="[]any{"
        )

    @cached_property
    @override
    def dict_format_config(self) -> DictFormatConfig:
        """Expose an ordinary mapping callback."""
        native = Go(language_version=self.language_version)

        def _open(items: dict[Scalar, Value], /) -> str:
            """Keep the callback result as plain source text."""
            return str(object=native.dict_format_config.dict_open(items))

        return dataclasses.replace(native.dict_format_config, dict_open=_open)


class SkipNullZig(Zig):
    """A caller-defined Zig policy that omits null mapping fields."""

    skip_null_dict_values: ClassVar[bool] = True


@beartype
def variants_for_custom_language_axis(*, axis_key: str) -> list[Variant]:
    """Build the custom language variants for an axis, if it has any."""
    match axis_key:
        case "custom_zig_null_policy":
            return [
                compact_variant(
                    name=f"Zig_{axis_key}",
                    spec=SkipNullZig(
                        language_version=version,
                        json_type=Zig.JsonTypes["STD_JSON_VALUE"],
                    ),
                    lang_cls=Zig,
                )
                for version in Zig.VersionFormats
            ]
        case "plain_collection_callbacks":
            plain_callbacks = True
        case "typed_collection_callback":
            plain_callbacks = False
        case _:
            return []
    return [
        compact_variant(
            name=f"Go_{axis_key}",
            spec=CallbackGo(
                language_version=version,
                plain_callbacks=plain_callbacks,
            ),
            lang_cls=Go,
        )
        for version in Go.VersionFormats
    ]
