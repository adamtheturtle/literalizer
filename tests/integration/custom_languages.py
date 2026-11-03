"""Custom language implementations exercised by compiling golden
variants.
"""

import dataclasses
from collections.abc import Callable
from functools import cache, cached_property
from typing import ClassVar

from beartype import beartype

import literalizer
from literalizer import DictFormatConfig
from literalizer._formatters.collection_openers import typed_collection_open
from literalizer._formatters.type_inference import DictType, ListType
from literalizer._types import Scalar, Value
from literalizer.languages import Zig

from .language_specs import make_spec, sorted_languages
from .variant_types import Variant, compact_variant


@cache
@beartype
def callback_language(
    *, lang_cls: literalizer.LanguageCls, plain_callbacks: bool
) -> literalizer.LanguageCls:
    """Extend each native spec through the same collection hook contract.

    Inheriting the native dataclass keeps its constructor and per-fixture
    module configuration intact. Only the two public callbacks change;
    the native implementation supplies valid language delimiters.
    """

    def native_spec(spec: literalizer.Language) -> literalizer.Language:
        """Rebuild the caller's complete native configuration."""
        return lang_cls(
            **{
                field.name: vars(spec)[field.name]
                for field in dataclasses.fields(class_or_instance=spec)
                if field.init
            }
        )

    def sequence_open(
        self: literalizer.Language,
    ) -> Callable[[list[Value]], str]:
        """Expose an ordinary sequence callback."""
        native = native_spec(spec=self)
        if plain_callbacks:
            return lambda items: str(object=native.sequence_open(items))

        def _type_open(_element_type: type | ListType | DictType) -> str:
            """Provide the extension's integer collection opener."""
            return str(object=native.sequence_open([1]))

        return typed_collection_open(
            type_to_opener=_type_open,
            fallback=str(object=native.sequence_open([])),
        )

    def dict_format_config(self: literalizer.Language) -> DictFormatConfig:
        """Expose an ordinary mapping callback."""
        native = native_spec(spec=self)

        def _open(items: dict[Scalar, Value], /) -> str:
            """Keep the callback result as plain source text."""
            return str(object=native.dict_format_config.dict_open(items))

        return dataclasses.replace(native.dict_format_config, dict_open=_open)

    return literalizer.LanguageCls.__new__(
        mcs=type(lang_cls),
        name=f"Callback{lang_cls.__name__}",
        bases=(lang_cls,),
        namespace={
            "sequence_open": cached_property(func=sequence_open),
            "dict_format_config": cached_property(func=dict_format_config),
        },
    )


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
            name=f"{lang_cls.__name__}_{axis_key}",
            spec=make_spec(
                lang_cls=callback_language(
                    lang_cls=lang_cls, plain_callbacks=plain_callbacks
                ),
                language_version=version,
            ),
            lang_cls=lang_cls,
        )
        for lang_cls in sorted_languages()
        for version in lang_cls.VersionFormats
    ]
