"""Shared whole-document fast path for JSON-native language modes.

A language's ``json_type`` mode renders every value into one dynamic
node tree: fixed collection delimiters, bare nested values, and no
sibling type inference, widening, record shaping or scalar wrapping.
For those modes the shared renderer in
:mod:`literalizer._literalize` does a lot of per-node work that cannot
change the answer.

:func:`format_json_native_document_fast` renders such a document
directly.  It is not a re-implementation of any one language: every
delimiter, separator, entry template and scalar literal still comes
from the same language hooks the shared renderer uses, so the output is
byte-for-byte identical.  What it drops is the generic recursion around
those hooks.

Languages opt in by registering this function with the
:func:`~literalizer._document_formatting.format_document_fast`
dispatch seam.  Registration alone is not a promise that a given
*instance* qualifies: the eligibility gate below re-checks, per call,
that the configured hooks really are the JSON-native shape, and returns
``None`` for anything else so the shared renderer handles it.
"""

import dataclasses

from beartype import beartype

from literalizer._document_formatting import format_document_fast
from literalizer._formatters.collection_openers import FixedOpen
from literalizer._formatters.format_entries import (
    DictEntryWithSeparator,
    passthrough_sequence_entry,
)
from literalizer._formatters.type_inference import (
    I32_MAX,
    I32_MIN,
    I64_MAX,
    I64_MIN,
)
from literalizer._language import (
    CollectionLayout,
    Language,
    no_compute_wrap_ids,
    no_empty_container_literal_overrides,
)
from literalizer._literalize import guard_dict_keys_supported, rstrip_lines
from literalizer._types import OrderedMap, Scalar, Value


class _SharedRendererRequiredError(Exception):
    """Signal a value outside the JSON-native fast path."""


@dataclasses.dataclass(frozen=True)
class _IntRange:
    """The integer range the fast path may render itself.

    Outside it the shared renderer swaps in a widened integer formatter
    for the whole collection (:class:`~literalizer._formatters.
    type_inference.WideInt` / :class:`~literalizer._formatters.
    type_inference.BeyondI64`), which the fast path does not model.  A
    language with no widened formatter at all has nothing to diverge
    from, so its bounds are infinite.
    """

    minimum: int | float
    maximum: int | float


@beartype
def _renderable_int_range(*, language: Language) -> _IntRange:
    """Return the integer bounds the fast path may render for
    *language*.
    """
    if language.format_integer_widened is not None:
        return _IntRange(minimum=I32_MIN, maximum=I32_MAX)
    if language.format_integer_beyond_i64 is not None:
        return _IntRange(minimum=I64_MIN, maximum=I64_MAX)
    return _IntRange(minimum=-float("inf"), maximum=float("inf"))


@beartype
def _inference_is_inert(*, language: Language) -> bool:
    """Return whether *language* renders values without inference.

    The shared renderer pre-walks the data for scalar-wrapping parents,
    empty-container literal replacements, record shapes and tuple-shaped
    lists.  Each of those can rewrite a node, so the fast path only
    applies when the language leaves every one of them at its shared
    no-op.
    """
    behavior = language.heterogeneous_behavior
    return (
        behavior.compute_wrap_ids is no_compute_wrap_ids
        and behavior.empty_container_literal_overrides
        is no_empty_container_literal_overrides
        and behavior.render_record_literal is None
        and behavior.render_tuple_literal is None
    )


@beartype
def format_json_native_document_fast(  # noqa: C901, PLR0915  # pylint: disable=too-complex
    language: Language,
    data: Value,
    *,
    line_prefix: str,
    include_delimiters: bool,
    collection_layout: CollectionLayout,
) -> str | None:
    """Render a JSON-native tree without the generic node recursion.

    Returns ``None`` -- meaning "use the shared renderer" -- whenever
    *language* is not configured as a plain dynamic-node tree, or when
    *data* holds a value the fast path does not model: a non-JSON
    scalar, an integer wide enough to swap the collection's integer
    formatter, an :class:`~literalizer._types.OrderedMap`, or a
    multiline nested layout.
    """
    if not isinstance(data, (dict, list)) or isinstance(data, OrderedMap):
        return None
    dict_config = language.dict_format_config
    sequence_config = language.sequence_format_config
    dict_open = dict_config.dict_open
    sequence_open = sequence_config.sequence_open
    if (  # pylint: disable=too-many-boolean-expressions
        not include_delimiters
        or collection_layout is not CollectionLayout.COMPACT
        or not isinstance(dict_open, FixedOpen)
        or not isinstance(sequence_open, FixedOpen)
        or not _inference_is_inert(language=language)
        or language.skip_null_dict_values
        or sequence_config.single_element_trailing_comma
        or dict_config.narrowed_open is not None
        or dict_config.narrowed_empty_form is not None
        or sequence_config.narrowed_empty_form is not None
        # An empty collection must render as its delimiters with nothing
        # between them, either because the language declares no separate
        # empty literal or because that literal spells the same thing.
        # The shared renderer picks between the two per position -- an
        # empty list beside a non-empty list sibling takes the sibling's
        # opener rather than the empty literal -- and the fast path does
        # not model that choice.  A non-empty closer additionally keeps
        # an empty nested collection from rendering as the empty string,
        # which the shared renderer drops from its parent rather than
        # joining with a separator.
        or not dict_config.close
        or not sequence_config.close
        or dict_config.empty_dict
        not in (None, dict_open.open_str + dict_config.close)
        or sequence_config.empty_sequence
        not in (None, sequence_open.open_str + sequence_config.close)
    ):
        return None

    format_string = language.format_string
    format_integer = language.format_integer
    format_float = language.format_float
    null_literal = language.null_literal
    true_literal = language.true_literal
    false_literal = language.false_literal
    format_dict_entry = dict_config.format_entry
    format_sequence_entry = language.format_sequence_entry
    separator = language.element_separator
    dict_head = dict_open.open_str
    dict_close = dict_config.close
    sequence_head = sequence_open.open_str
    sequence_close = sequence_config.close
    int_range = _renderable_int_range(language=language)

    def scalar(value: Value, /) -> str:
        """Format one JSON-native scalar."""
        match value:
            case None:
                return null_literal
            case bool():
                return true_literal if value else false_literal
            case int():
                if not int_range.minimum <= value <= int_range.maximum:
                    raise _SharedRendererRequiredError
                return format_integer(value)
            case float():
                return format_float(value)
            case str():
                return format_string(value)
            case _:
                raise _SharedRendererRequiredError

    def compact(value: Value, /) -> str:
        """Format one value with compact nested collections."""
        match value:
            case dict():
                entries = dict_entries(value)
                return dict_head + separator.join(entries) + dict_close
            case list():
                items = sequence_entries(value)
                return sequence_head + separator.join(items) + sequence_close
            case _:
                return scalar(value)

    # Bind the per-collection entry builders once.  A language whose
    # entry hooks add nothing to the child literal -- a bare separator
    # between key and value, an untouched sequence element -- would
    # otherwise pay a hook call per node to be handed the string back
    # unchanged.
    if (
        isinstance(format_dict_entry, DictEntryWithSeparator)
        and format_dict_entry.format_value is passthrough_sequence_entry
    ):
        entry_separator = format_dict_entry.separator

        def dict_entries(value: dict[Scalar, Value], /) -> list[str]:
            """Join each formatted key and value with the separator."""
            guard_dict_keys_supported(value=value, spec=language)
            return [
                scalar(key) + entry_separator + compact(child)
                for key, child in value.items()
            ]
    else:

        def dict_entries(value: dict[Scalar, Value], /) -> list[str]:
            """Build each dict entry through the language's hook."""
            guard_dict_keys_supported(value=value, spec=language)
            return [
                format_dict_entry(scalar(key), child, compact(child))
                for key, child in value.items()
            ]

    if format_sequence_entry is passthrough_sequence_entry:

        def sequence_entries(value: list[Value], /) -> list[str]:
            """Format each element with no per-entry wrapping."""
            return [compact(child) for child in value]
    else:

        def sequence_entries(value: list[Value], /) -> list[str]:
            """Build each element through the language's entry hook."""
            return [
                format_sequence_entry(child, compact(child)) for child in value
            ]

    def root(value: dict[Scalar, Value] | list[Value], /) -> str:
        """Format the root collection over multiple lines."""
        is_dict = isinstance(value, dict)
        config_supports_trailing_comma = (
            dict_config.supports_trailing_comma
            if is_dict
            else sequence_config.supports_trailing_comma
        )
        trailing_comma = (
            language.trailing_comma_config.multiline_trailing_comma
            and config_supports_trailing_comma
        )
        head = dict_head if is_dict else sequence_head
        closer = dict_close if is_dict else sequence_close
        entries = (
            dict_entries(value)
            if isinstance(value, dict)
            else sequence_entries(value)
        )
        body_prefix = line_prefix + language.indent
        separator_text = separator.strip()
        last_index = len(entries) - 1
        # Trim per line, not just at the end of the entry: that is what
        # the shared renderer does, and a scalar formatter that emits a
        # multi-line literal would otherwise diverge from it.
        lines = [
            f"{body_prefix}{rstrip_lines(text=entry)}"
            f"{separator_text if index < last_index or trailing_comma else ''}"
            for index, entry in enumerate(iterable=entries)
        ]
        closing_indent = (
            language.indent if language.indent_closing_delimiter else ""
        )
        opening = (line_prefix + head).rstrip()
        return (
            f"{opening}\n{'\n'.join(lines)}\n"
            f"{line_prefix}{closing_indent}{closer}"
        )

    try:
        # The shared renderer always lays out the root collection over
        # multiple lines; ``collection_layout`` controls nested values.
        if not data:
            return line_prefix + compact(data)
        return root(data)
    except _SharedRendererRequiredError:
        return None


@beartype
def register_json_native_document_fast(*, language_cls: type) -> None:
    """Opt *language_cls* into the shared JSON-native fast path.

    Call this from a language module once the language's ``json_type``
    modes are known to render as a plain dynamic-node tree.  Instances
    that turn out not to qualify still fall back automatically.
    """
    format_document_fast.register(
        cls=language_cls,
        func=format_json_native_document_fast,
    )
