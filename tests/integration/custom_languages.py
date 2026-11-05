"""Custom language implementations exercised by compiling golden
variants.
"""

import dataclasses
import datetime as dt
from collections.abc import Callable
from functools import cache, cached_property
from typing import ClassVar, override

from beartype import beartype

import literalizer
from literalizer import DictFormatConfig
from literalizer._formatters.collection_openers import typed_collection_open
from literalizer._formatters.format_integers import (
    format_integer_hex,
    make_negative_nondecimal_i64_formatter,
)
from literalizer._formatters.type_inference import DictType, ListType
from literalizer._types import Scalar, Value
from literalizer.languages import Cpp, Ruby, Zig

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


@cache
@beartype
def existing_suffix_cpp(*, base_suffix: str) -> literalizer.LanguageCls:
    """Compose a real C++ literal with a suffix already supplied by its
    base.
    """

    def format_integer(_self: Cpp) -> Callable[[int], str]:
        """Keep the factory's actual expression in the native program."""

        def base(value: int) -> str:
            """Supply the caller-owned suffix before composition."""
            return format_integer_hex(value=value) + base_suffix

        return make_negative_nondecimal_i64_formatter(
            base=base, suffix="LL", base_suffix=base_suffix
        )

    return literalizer.LanguageCls.__new__(
        mcs=type(Cpp),
        name=f"ExistingSuffix{base_suffix}Cpp",
        bases=(Cpp,),
        namespace={"format_integer": cached_property(func=format_integer)},
    )


class DatetimeDateRuby(Ruby):
    """Exercise the date interface with the original datetime
    arguments.
    """

    @cached_property
    @override
    def format_datetime(self) -> Callable[[dt.datetime], str]:
        """Pass the datetime itself through the selected date enum
        member.
        """
        return self.date_format


@beartype
def _formatter_contract_variants(*, axis_key: str) -> list[Variant]:
    """Build native consumers of the former direct formatter contracts."""
    match axis_key:
        case "existing_integer_suffix":
            return [
                compact_variant(
                    name=f"Cpp_existing_integer_suffix_{suffix.lower()}",
                    spec=make_spec(
                        lang_cls=existing_suffix_cpp(base_suffix=suffix),
                        language_version=version,
                        variable_type_hints=Cpp.variable_type_hints_formats.NEVER,
                    ),
                    lang_cls=Cpp,
                )
                for suffix in ("LL", "L")
                for version in Cpp.VersionFormats
            ]
        case "date_formatter_datetime_view":
            return [
                compact_variant(
                    name=f"Ruby_date_formatter_datetime_{member.name.lower()}",
                    spec=make_spec(
                        lang_cls=DatetimeDateRuby,
                        language_version=version,
                        date_format=member,
                    ),
                    lang_cls=Ruby,
                )
                for member in Ruby.DateFormats
                if member.value.type_produced is dt.date
                for version in Ruby.VersionFormats
            ]
        case _:
            return []


@beartype
def variants_for_custom_language_axis(*, axis_key: str) -> list[Variant]:
    """Build the custom language variants for an axis, if it has any."""
    formatter_contracts = _formatter_contract_variants(axis_key=axis_key)
    if len(formatter_contracts) > 0:
        return formatter_contracts
    match axis_key:
        case "copied_json_to_native":
            return [
                compact_variant(
                    name=f"Zig_{axis_key}",
                    spec=dataclasses.replace(
                        Zig(
                            language_version=version,
                            json_type=Zig.JsonTypes["STD_JSON_VALUE"],
                        ),
                        json_type=None,
                    ),
                    lang_cls=Zig,
                )
                for version in Zig.VersionFormats
            ]
        case "copied_native_to_record" | "copied_native_to_json":
            return [
                compact_variant(
                    name=f"Zig_{axis_key}",
                    spec=dataclasses.replace(
                        Zig(language_version=version),
                        heterogeneous_strategy=Zig.HeterogeneousStrategies[
                            "RECORD"
                        ],
                    )
                    if axis_key == "copied_native_to_record"
                    else dataclasses.replace(
                        Zig(language_version=version),
                        json_type=Zig.JsonTypes["STD_JSON_VALUE"],
                    ),
                    lang_cls=Zig,
                )
                for version in Zig.VersionFormats
            ]
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
