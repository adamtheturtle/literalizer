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
    DictFormatConfig,
    Language,
    SequenceFormatConfig,
    no_compute_wrap_ids,
    no_empty_container_literal_overrides,
)
from literalizer._literalize import guard_dict_keys_supported, rstrip_lines
from literalizer._types import OrderedMap, Scalar, Value


class _SharedRendererRequiredError(Exception):
    """Signal a value outside the JSON-native fast path."""


@beartype
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


def _configuration_requires_shared_renderer(
    *,
    language: Language,
    dict_config: DictFormatConfig,
    sequence_config: SequenceFormatConfig,
    dict_head: str,
    sequence_head: str,
) -> bool:
    """Return whether configuration semantics need the shared renderer."""
    if (
        not _inference_is_inert(language=language)
        or language.skip_null_dict_values
        or sequence_config.single_element_trailing_comma
        or dict_config.narrowed_open is not None
    ):
        return True
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
    if (
        dict_config.narrowed_empty_form is not None
        or sequence_config.narrowed_empty_form is not None
        or dict_config.close == ""
        or sequence_config.close == ""
    ):
        return True
    return dict_config.empty_dict not in (
        None,
        dict_head + dict_config.close,
    ) or sequence_config.empty_sequence not in (
        None,
        sequence_head + sequence_config.close,
    )


class _JsonNativeRenderer:
    """Render one tree after the public fast-path boundary validates
    it.

    Keeping the recursive operations without decorators as implementation
    methods preserves the single Beartype check at the registered
    document boundary; checking every child would undo the fast path's
    purpose.
    """

    def __init__(
        self,
        *,
        language: Language,
        dict_config: DictFormatConfig,
        sequence_config: SequenceFormatConfig,
        dict_head: str,
        sequence_head: str,
    ) -> None:
        """Bind language hooks and collection strategies once per document."""
        self.language = language
        self.dict_config = dict_config
        self.sequence_config = sequence_config
        self.format_string = language.format_string
        self.format_integer = language.format_integer
        self.format_float = language.format_float
        self.null_literal = language.null_literal
        self.true_literal = language.true_literal
        self.false_literal = language.false_literal
        self.format_dict_entry = dict_config.format_entry
        self.format_sequence_entry = language.format_sequence_entry
        self.separator = language.element_separator
        self.dict_head = dict_head
        self.dict_close = dict_config.close
        self.sequence_head = sequence_head
        self.sequence_close = sequence_config.close
        self.int_range = _renderable_int_range(language=language)

        # Select each entry strategy once per document rather than
        # branching or calling a no-op language hook for every node.
        if (
            isinstance(self.format_dict_entry, DictEntryWithSeparator)
            and self.format_dict_entry.format_value
            is passthrough_sequence_entry
        ):
            self.entry_separator = self.format_dict_entry.separator
            self.dict_entries = self._direct_dict_entries
        else:
            self.entry_separator = ""
            self.dict_entries = self._hook_dict_entries
        if self.format_sequence_entry is passthrough_sequence_entry:
            self.sequence_entries = self._direct_sequence_entries
        else:
            self.sequence_entries = self._hook_sequence_entries

    def scalar(self, value: Value, /) -> str:
        """Format one JSON-native scalar."""
        match value:
            case None:
                return self.null_literal
            case bool():
                if value:
                    return self.true_literal
                return self.false_literal
            case int():
                if (
                    not self.int_range.minimum
                    <= value
                    <= self.int_range.maximum
                ):
                    raise _SharedRendererRequiredError
                return self.format_integer(value)
            case float():
                return self.format_float(value)
            case str():
                return self.format_string(value)
            case _:
                raise _SharedRendererRequiredError

    def compact(self, value: Value, /) -> str:
        """Format one value with compact nested collections."""
        match value:
            case dict():
                entries = self.dict_entries(value)
                return (
                    self.dict_head
                    + self.separator.join(entries)
                    + self.dict_close
                )
            case list():
                items = self.sequence_entries(value)
                return (
                    self.sequence_head
                    + self.separator.join(items)
                    + self.sequence_close
                )
            case _:
                return self.scalar(value)

    def _direct_dict_entries(self, value: dict[Scalar, Value], /) -> list[str]:
        """Join each formatted key and value with the separator."""
        guard_dict_keys_supported(value=value, spec=self.language)
        return [
            self.scalar(key) + self.entry_separator + self.compact(child)
            for key, child in value.items()
        ]

    def _hook_dict_entries(self, value: dict[Scalar, Value], /) -> list[str]:
        """Build each dict entry through the language's hook."""
        guard_dict_keys_supported(value=value, spec=self.language)
        return [
            self.format_dict_entry(
                self.scalar(key), child, self.compact(child)
            )
            for key, child in value.items()
        ]

    def _direct_sequence_entries(self, value: list[Value], /) -> list[str]:
        """Format each element with no per-entry wrapping."""
        return [self.compact(child) for child in value]

    def _hook_sequence_entries(self, value: list[Value], /) -> list[str]:
        """Build each element through the language's entry hook."""
        return [
            self.format_sequence_entry(child, self.compact(child))
            for child in value
        ]

    def root(
        self, value: dict[Scalar, Value] | list[Value], /, *, line_prefix: str
    ) -> str:
        """Format the root collection over multiple lines."""
        is_dict = isinstance(value, dict)
        config_supports_trailing_comma = (
            self.dict_config.supports_trailing_comma
            if is_dict
            else self.sequence_config.supports_trailing_comma
        )
        trailing_comma = (
            self.language.trailing_comma_config.multiline_trailing_comma
            and config_supports_trailing_comma
        )
        head = self.dict_head if is_dict else self.sequence_head
        closer = self.dict_close if is_dict else self.sequence_close
        entries = (
            self.dict_entries(value)
            if isinstance(value, dict)
            else self.sequence_entries(value)
        )
        body_prefix = line_prefix + self.language.indent
        separator_text = self.separator.strip()
        last_index = len(entries) - 1
        # Trim per line, not just at the end of the entry: that is what
        # the shared renderer does, and a scalar formatter that emits a
        # multi-line literal would otherwise diverge from it.
        collected_lines: list[str] = []
        for entry_index, entry_entry in enumerate(iterable=entries):
            effective_separator_text = ""
            if entry_index < last_index or trailing_comma:
                effective_separator_text = separator_text
            collected_lines.append(
                f"{body_prefix}{rstrip_lines(text=entry_entry)}{effective_separator_text}"
            )
        closing_indent = ""
        if self.language.indent_closing_delimiter:
            closing_indent = self.language.indent
        opening = (line_prefix + head).rstrip()
        return (
            f"{opening}\n{'\n'.join(collected_lines)}\n"
            f"{line_prefix}{closing_indent}{closer}"
        )


@beartype
def format_json_native_document_fast(
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
    if (
        not include_delimiters
        or collection_layout is not CollectionLayout.COMPACT
        or not isinstance(dict_open, FixedOpen)
        or not isinstance(sequence_open, FixedOpen)
        or _configuration_requires_shared_renderer(
            language=language,
            dict_config=dict_config,
            sequence_config=sequence_config,
            dict_head=dict_open.open_str,
            sequence_head=sequence_open.open_str,
        )
    ):
        return None

    renderer = _JsonNativeRenderer(
        language=language,
        dict_config=dict_config,
        sequence_config=sequence_config,
        dict_head=dict_open.open_str,
        sequence_head=sequence_open.open_str,
    )
    try:
        # The shared renderer always lays out the root collection over
        # multiple lines; ``collection_layout`` controls nested values.
        if len(data) == 0:
            return line_prefix + renderer.compact(data)
        return renderer.root(data, line_prefix=line_prefix)
    except _SharedRendererRequiredError:
        return None


@beartype
def register_json_native_document_fast(*, language_cls: type) -> None:
    """Opt *language_cls* into the shared JSON-native fast path.

    Call this from a language module once the language's ``json_type``
    modes are known to render as a plain dynamic-node tree.  Instances
    that turn out not to qualify still fall back automatically.
    """
    _ = format_document_fast.register(
        cls=language_cls,
        func=format_json_native_document_fast,
    )
