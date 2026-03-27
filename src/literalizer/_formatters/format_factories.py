"""Factory functions for building format configurations."""

from collections.abc import Callable

from beartype import beartype

from literalizer._formatters.collection_openers import (
    fixed_dict_open,
    fixed_set_open,
)
from literalizer._language import (
    DictFormatConfig,
    OrderedMapFormatConfig,
    SetFormatConfig,
)
from literalizer._types import Value


@beartype
def set_format_factory(
    *,
    open_template: str,
    close: str,
    empty_template: str | None,
    preamble_lines: tuple[str, ...],
    set_opener_template: str,
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
        )
        config = factory("Any")
    """

    @beartype
    def _build(default_type: str) -> SetFormatConfig:
        """Build a ``SetFormatConfig`` with the given default type."""
        open_str = open_template.format(type=default_type)
        return SetFormatConfig(
            set_open=fixed_set_open(open_str=open_str),
            close=close.format(type=default_type),
            empty_set=(
                empty_template.format(type=default_type)
                if empty_template is not None
                else None
            ),
            preamble_lines=preamble_lines,
            set_opener_template=set_opener_template,
        )

    return _build


@beartype
def dict_format_factory(
    *,
    open_template: str,
    close: str,
    format_entry: Callable[[str, Value, str], str],
    empty_template: str | None,
    preamble_lines: tuple[str, ...],
    narrowed_open: str | None,
) -> Callable[[str], DictFormatConfig]:
    """Return a callable that builds a ``DictFormatConfig`` for a given
    type.

    Templates use ``{type}`` as the placeholder for the default type name.
    The ``open_template`` is wrapped in ``fixed_dict_open``.
    """

    @beartype
    def _build(default_type: str) -> DictFormatConfig:
        """Build a ``DictFormatConfig`` with the given default type."""
        return DictFormatConfig(
            open_fn=fixed_dict_open(
                open_str=open_template.format(type=default_type),
            ),
            close=close,
            format_entry=format_entry,
            empty_dict=(
                empty_template.format(type=default_type)
                if empty_template is not None
                else None
            ),
            preamble_lines=preamble_lines,
            narrowed_open=narrowed_open,
        )

    return _build


@beartype
def ordered_map_format_factory(
    *,
    open_template: str,
    close: str,
    preamble_lines: tuple[str, ...],
) -> Callable[[str], OrderedMapFormatConfig]:
    """Return a callable that builds an ``OrderedMapFormatConfig``.

    Templates use ``{type}`` as the placeholder for the default type name.
    """

    @beartype
    def _build(default_type: str) -> OrderedMapFormatConfig:
        """Build an ``OrderedMapFormatConfig`` with the given default type."""
        return OrderedMapFormatConfig(
            open_str=open_template.format(type=default_type),
            close=close,
            preamble_lines=preamble_lines,
        )

    return _build
