"""Factory functions for building format configurations."""

from collections.abc import Callable
from typing import Protocol, runtime_checkable

from beartype import beartype

from literalizer._formatters.collection_openers import (
    fixed_open,
)
from literalizer._language import (
    DictFormatBuilder,
    DictFormatConfig,
    OrderedMapFormatConfig,
    SequenceFormatConfig,
    SetFormatConfig,
)
from literalizer._types import Value


@runtime_checkable
class _OrderedMapFormatBuilder(Protocol):
    """Protocol for the callable returned by
    ``ordered_map_format_factory``.
    """

    def __call__(
        self,
        default_type: str,
        *,
        default_key_type: str,
    ) -> OrderedMapFormatConfig:
        """Build an ``OrderedMapFormatConfig`` with the given default type."""
        ...


@beartype
def _build_sequence_format_config(
    *,
    default_type: str,
    open_template: str,
    close: str,
    supports_heterogeneity: bool,
    single_element_trailing_comma: bool,
    single_element_template: str | None,
    supports_trailing_comma: bool,
    empty_template: str | None,
    preamble_lines: tuple[str, ...],
    format_entry: Callable[[Value, str], str],
    typed_opener_fallback_template: str | None,
) -> SequenceFormatConfig:
    """Build a ``SequenceFormatConfig`` with the given default type."""
    effective_empty_sequence = None
    if empty_template is not None:
        effective_empty_sequence = empty_template.format(type=default_type)
    effective_typed_opener_fallback = None
    if typed_opener_fallback_template is not None:
        effective_typed_opener_fallback = (
            typed_opener_fallback_template.format(
                type=default_type,
            )
        )
    return SequenceFormatConfig(
        sequence_open=fixed_open(
            open_str=open_template.format(type=default_type),
        ),
        close=close,
        supports_heterogeneity=supports_heterogeneity,
        single_element_trailing_comma=single_element_trailing_comma,
        supports_trailing_comma=supports_trailing_comma,
        empty_sequence=(effective_empty_sequence),
        preamble_lines=preamble_lines,
        format_entry=format_entry,
        typed_opener_fallback=(effective_typed_opener_fallback),
        uses_typed_literal_for_scalars=False,
        requires_uniform_record_shapes=False,
        declared_type=None,
        narrowed_empty_form=None,
        single_element_template=single_element_template,
    )


@beartype
def sequence_format_factory(
    *,
    open_template: str,
    close: str,
    supports_heterogeneity: bool,
    single_element_trailing_comma: bool,
    single_element_template: str | None,
    supports_trailing_comma: bool,
    empty_template: str | None,
    preamble_lines: tuple[str, ...],
    format_entry: Callable[[Value, str], str],
    typed_opener_fallback_template: str | None,
) -> Callable[[str], SequenceFormatConfig]:
    """Return a callable that builds a ``SequenceFormatConfig`` for a
    given type.

    Templates use ``{type}`` as the placeholder for the default type
    name.  The ``open_template`` is wrapped in ``fixed_open``.
    """

    def _build(default_type: str) -> SequenceFormatConfig:
        """Delegate to module-level implementation."""
        return _build_sequence_format_config(
            default_type=default_type,
            open_template=open_template,
            close=close,
            supports_heterogeneity=supports_heterogeneity,
            single_element_trailing_comma=single_element_trailing_comma,
            single_element_template=single_element_template,
            supports_trailing_comma=supports_trailing_comma,
            empty_template=empty_template,
            preamble_lines=preamble_lines,
            format_entry=format_entry,
            typed_opener_fallback_template=typed_opener_fallback_template,
        )

    return _build


@beartype
def _build_set_format_config(
    *,
    default_type: str,
    open_template: str,
    close: str,
    empty_template: str | None,
    preamble_lines: tuple[str, ...],
    set_opener_template: str,
    supports_heterogeneity: bool,
    supports_trailing_comma: bool,
) -> SetFormatConfig:
    """Build a ``SetFormatConfig`` with the given default type."""
    open_str = open_template.format(type=default_type)
    effective_empty_set = None
    if empty_template is not None:
        effective_empty_set = empty_template.format(type=default_type)
    return SetFormatConfig(
        set_open=fixed_open(open_str=open_str),
        close=close.format(type=default_type),
        empty_set=(effective_empty_set),
        preamble_lines=preamble_lines,
        set_opener_template=set_opener_template,
        supports_heterogeneity=supports_heterogeneity,
        supports_trailing_comma=supports_trailing_comma,
    )


@beartype
def set_format_factory(
    *,
    open_template: str,
    close: str,
    empty_template: str | None,
    preamble_lines: tuple[str, ...],
    set_opener_template: str,
    supports_heterogeneity: bool,
    supports_trailing_comma: bool,
) -> Callable[[str], SetFormatConfig]:
    """Return a callable that builds a ``SetFormatConfig`` for a given
    type.

    Templates use ``{type}`` as the placeholder for the default type name.

    Example::

        factory = set_format_factory(
            open_template="Set<{type}>([",
            close="])",
            empty_template="Set<{type}>()",
            preamble_lines=(),
            set_opener_template="",
            supports_trailing_comma=True,
        )
        config = factory("Any")
    """

    def _build(default_type: str) -> SetFormatConfig:
        """Delegate to module-level implementation."""
        return _build_set_format_config(
            default_type=default_type,
            open_template=open_template,
            close=close,
            empty_template=empty_template,
            preamble_lines=preamble_lines,
            set_opener_template=set_opener_template,
            supports_heterogeneity=supports_heterogeneity,
            supports_trailing_comma=supports_trailing_comma,
        )

    return _build


@beartype
def _build_dict_format_config(
    *,
    default_type: str,
    default_key_type: str,
    open_template: str,
    close: str,
    format_entry: Callable[[str, Value, str], str],
    empty_template: str | None,
    preamble_lines: tuple[str, ...],
    narrowed_open: str | None,
    supports_trailing_comma: bool,
) -> DictFormatConfig:
    """Build a ``DictFormatConfig`` with the given default type."""
    fmt_kwargs = {"type": default_type, "key_type": default_key_type}
    effective_empty_dict = None
    if empty_template is not None:
        effective_empty_dict = empty_template.format(**fmt_kwargs)
    return DictFormatConfig(
        dict_open=fixed_open(
            open_str=open_template.format(**fmt_kwargs),
        ),
        close=close,
        format_entry=format_entry,
        empty_dict=(effective_empty_dict),
        preamble_lines=preamble_lines,
        narrowed_open=narrowed_open,
        supports_trailing_comma=supports_trailing_comma,
        narrowed_empty_form=None,
    )


@beartype
def dict_format_factory(
    *,
    open_template: str,
    close: str,
    format_entry: Callable[[str, Value, str], str],
    empty_template: str | None,
    preamble_lines: tuple[str, ...],
    narrowed_open: str | None,
    supports_trailing_comma: bool,
) -> DictFormatBuilder:
    """Return a callable that builds a ``DictFormatConfig`` for a given
    type.

    Templates use ``{type}`` and optionally ``{key_type}`` as
    placeholders for the default value type and key type names.
    The ``open_template`` is wrapped in ``fixed_open``.
    """

    def _build(
        default_type: str,
        *,
        default_key_type: str,
    ) -> DictFormatConfig:
        """Delegate to module-level implementation."""
        return _build_dict_format_config(
            default_type=default_type,
            default_key_type=default_key_type,
            open_template=open_template,
            close=close,
            format_entry=format_entry,
            empty_template=empty_template,
            preamble_lines=preamble_lines,
            narrowed_open=narrowed_open,
            supports_trailing_comma=supports_trailing_comma,
        )

    return _build


@beartype
def _build_ordered_map_format_config(
    *,
    default_type: str,
    default_key_type: str,
    open_template: str,
    close: str,
    preamble_lines: tuple[str, ...],
) -> OrderedMapFormatConfig:
    """Build an ``OrderedMapFormatConfig`` with the given default type."""
    fmt_kwargs = {"type": default_type, "key_type": default_key_type}
    return OrderedMapFormatConfig(
        ordered_map_open=fixed_open(
            open_str=open_template.format(**fmt_kwargs),
        ),
        close=close,
        preamble_lines=preamble_lines,
    )


@beartype
def ordered_map_format_factory(
    *,
    open_template: str,
    close: str,
    preamble_lines: tuple[str, ...],
) -> _OrderedMapFormatBuilder:
    """Return a callable that builds an ``OrderedMapFormatConfig``.

    Templates use ``{type}`` and optionally ``{key_type}`` as
    placeholders for the default value type and key type names.
    """

    def _build(
        default_type: str,
        *,
        default_key_type: str,
    ) -> OrderedMapFormatConfig:
        """Delegate to module-level implementation."""
        return _build_ordered_map_format_config(
            default_type=default_type,
            default_key_type=default_key_type,
            open_template=open_template,
            close=close,
            preamble_lines=preamble_lines,
        )

    return _build
