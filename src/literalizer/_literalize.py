"""Core conversion logic: formatting values and entry points."""

import dataclasses
import datetime
import enum
from collections.abc import Callable, Sequence
from typing import assert_never

from beartype import BeartypeConf, beartype
from ruamel.yaml.comments import CommentedSeq
from ruamel.yaml.compat import ordereddict

from literalizer._checks import check_data
from literalizer._comments import (
    CollectionComments,
    apply_collection_comments_to_elements,
    extract_yaml_comments,
    prepend_collection_comments,
)
from literalizer._comments_resolve import (
    ResolvedComments,
    resolve_toml_comments,
    resolve_yaml_comments,
)
from literalizer._formatters.type_inference import (
    DictType,
    infer_element_type,
)
from literalizer._language import (
    CallStyle,
    CallSupport,
    CollectionLayout,
    CommandCallStyle,
    IdentifierCase,
    KeywordCallStyle,
    Language,
    ObjectCallStyle,
    PositionalCallStyle,
    PostfixCallStyle,
    PrefixCallStyle,
    StubReturn,
)
from literalizer._parsing import InputFormat, parse_input
from literalizer._preamble import (
    compute_preamble,
    deduplicate_preamble_entries,
)
from literalizer._types import Scalar, Value
from literalizer.exceptions import (
    CallsNotSupportedByLanguageError,
    CallsNotSupportedByToolError,
    DottedCallsNotSupportedError,
    ParameterCountMismatchError,
    PerElementNotListError,
    UnsupportedIdentifierCaseError,
    VariableNamesNotSupportedError,
)


@dataclasses.dataclass(frozen=True)
class LiteralizeResult:
    """Result of converting data to a native language literal."""

    declaration_code: str
    """The variable declaration or assignment text, without any
    :attr:`body_preamble` or :attr:`pre_declaration_comments` lines.

    Use :attr:`code` for the full formatted text including all prefix
    lines.
    """

    preamble: tuple[str, ...]
    """Lines (imports, package declarations, etc.) that must precede
    the generated code.  Empty when none are needed.
    """

    body_preamble: tuple[str, ...]
    """Type-definition lines (e.g. F#'s ``type Val = …``, Haskell's
    ``data Val = …`` and typeclass instances) that are prepended to
    :attr:`code`.  Empty when none are needed.

    Use :attr:`bare_code` to obtain the literal text *without* these
    lines.
    """

    pre_declaration_comments: tuple[str, ...] = ()
    """Already-formatted comment lines that appear between
    :attr:`body_preamble` and the variable declaration/assignment in
    :attr:`code`.  These come from scalar before-comments when the
    language does not support them inline.

    Included in :attr:`bare_code` but excluded from
    :attr:`declaration_code`.
    """

    types_present: frozenset[type] = frozenset()
    """The set of Python types observed in the source data (e.g.
    ``int``, ``str``, ``list``, ``dict``).  Callers that combine
    multiple ``literalize`` results (for example, a test harness that
    pairs ``$ref`` declarations with a downstream call) can union
    these and re-invoke :attr:`Language.compute_body_preamble` to
    derive a single body preamble that covers every type referenced
    across the combined output.
    """

    source_data: Value = None
    """The parsed source value the literal was rendered from.  Most
    callers do not need it.  Callers that combine multiple
    ``literalize`` results and re-invoke
    :attr:`Language.compute_body_preamble` to derive a single body
    preamble surface this so the recomputation can inspect actual
    values (e.g. datetime microsecond precision) rather than passing
    a placeholder.
    """

    @property
    def code(self) -> str:
        """The formatted literal text.

        When a language defines ``scalar_body_preamble`` entries (e.g.
        Haskell typeclass instances), those lines are prepended to the
        code so they appear in the correct structural position.
        """
        all_prefix_lines = (
            *self.body_preamble,
            *self.pre_declaration_comments,
        )
        if not all_prefix_lines:
            return self.declaration_code
        return "\n".join(all_prefix_lines) + "\n" + self.declaration_code

    @property
    def bare_code(self) -> str:
        """The literal text without :attr:`body_preamble` prepended.

        Identical to :attr:`code` when :attr:`body_preamble` is empty.
        :attr:`pre_declaration_comments` are preserved.
        """
        if not self.pre_declaration_comments:
            return self.declaration_code
        return (
            "\n".join(self.pre_declaration_comments)
            + "\n"
            + self.declaration_code
        )


@dataclasses.dataclass(frozen=True)
class NewVariable:
    """Wrap output in a new variable declaration."""

    name: str
    modifiers: frozenset[enum.Enum] = frozenset()
    """Declaration modifiers to apply.  Each language exposes its own
    modifier enum as ``Language.Modifiers`` (e.g. ``Java.Modifiers.FINAL``,
    ``CSharp.Modifiers.READONLY``, ``Cpp.Modifiers.STATIC``).  Values
    that are not members of the target language's ``Modifiers`` enum
    are silently ignored.
    """


@dataclasses.dataclass(frozen=True)
class ExistingVariable:
    """Wrap output in an assignment to an existing variable."""

    name: str


@dataclasses.dataclass(frozen=True)
class BothVariableForms:
    """Produce both a declaration and an assignment, combined.

    Requires ``wrap_in_file=True`` on :func:`literalize`.
    """

    name: str
    modifiers: frozenset[enum.Enum] = frozenset()
    """Declaration modifiers applied to the declaration half.  See
    :attr:`NewVariable.modifiers`.
    """


VariableForm = NewVariable | ExistingVariable | BothVariableForms


@beartype
def _format_scalar(*, value: Scalar, spec: Language) -> str:
    """Format a scalar JSON value as a native language literal."""
    match value:
        case None:
            result = spec.null_literal
        case bool():
            result = spec.true_literal if value else spec.false_literal
        case int():
            result = spec.format_integer(value)
        case float():
            result = spec.format_float(value)
        case str():
            result = spec.format_string(value)
        case bytes():
            result = spec.format_bytes(value)
        case datetime.datetime():
            result = spec.format_datetime(value)
        case _:
            result = spec.format_date(value)
    return result


@beartype
def _maybe_wrap_child(
    *,
    parent_id: int,
    wrap_ids: frozenset[int],
    raw_value: Value,
    formatted_value: str,
    spec: Language,
) -> str:
    """Wrap *formatted_value* when *parent_id* is in *wrap_ids*.

    Delegates to
    :attr:`~literalizer._language.HeterogeneousBehavior.wrap_scalar`
    on the spec's
    :attr:`~literalizer._language.Language.heterogeneous_behavior`.
    """
    if parent_id not in wrap_ids:
        return formatted_value
    return spec.heterogeneous_behavior.wrap_scalar(
        raw_value,
        formatted_value,
    )


@beartype
def _compute_wrap_ids(*, data: Value, spec: Language) -> frozenset[int]:
    """Return container ids whose scalar children should be wrapped.

    Delegates to the language spec's
    :attr:`~literalizer._language.HeterogeneousBehavior.compute_wrap_ids`.
    """
    return spec.heterogeneous_behavior.compute_wrap_ids(data)


@beartype
def _build_dict_entry(
    *, key_str: str, raw_value: Value, formatted_value: str, spec: Language
) -> str:
    """Format a single dict key-value entry using the language spec."""
    return spec.dict_format_config.format_entry(
        key_str,
        raw_value,
        formatted_value,
    )


@beartype
def _format_set_value(
    *,
    value: set[Scalar],
    spec: Language,
    wrap_ids: frozenset[int],
) -> str:
    """Format a set value as a native language literal."""
    set_cfg = spec.set_format_config

    if not value and set_cfg.empty_set is not None:
        return set_cfg.empty_set
    sorted_items = sorted(value, key=lambda v: (type(v).__name__, repr(v)))
    items_as_values: list[Value] = list(sorted_items)
    parent_id = id(value)
    formatted = [_format_scalar(value=v, spec=spec) for v in sorted_items]
    entries = [
        spec.format_set_entry(
            v,
            _maybe_wrap_child(
                parent_id=parent_id,
                wrap_ids=wrap_ids,
                raw_value=v,
                formatted_value=item,
                spec=spec,
            ),
        )
        for v, item in zip(sorted_items, formatted, strict=True)
    ]
    joined = spec.element_separator.join(entries)
    return set_cfg.set_open(items_as_values) + joined + set_cfg.close


@beartype
def _format_ordered_map_value(
    *,
    value: ordereddict,
    spec: Language,
    wrap_ids: frozenset[int],
    ref_case: IdentifierCase | None,
    expand_refs: bool,
    ref_key: str,
    collection_layout: CollectionLayout,
    multiline_prefix: str,
) -> str:
    """Format an ordered map as a native language literal."""
    ordered_map_cfg = spec.ordered_map_format_config

    ordered_map_items: list[tuple[str, Value]] = [
        (k, v)
        for k, v in value.items()  # pyright: ignore[reportUnknownVariableType,reportUnknownMemberType]
        if not (spec.skip_null_dict_values and v is None)
    ]
    if (
        not ordered_map_items
        and spec.dict_format_config.empty_dict is not None
    ):
        return spec.dict_format_config.empty_dict
    parent_id = id(value)
    sibling_list_values: list[list[Value]] = [
        v for _, v in ordered_map_items if isinstance(v, list)
    ]
    outer_sequence_override = _compute_sequence_open_override(
        items=sibling_list_values,
        spec=spec,
    )
    position_overrides = _compute_sibling_list_position_overrides(
        list_values=sibling_list_values,
        spec=spec,
    )
    pairs = [
        spec.format_ordered_map_entry(
            _format_value(
                value=k,
                spec=spec,
                dict_open_override=None,
                wrap_ids=wrap_ids,
                sequence_open_override=None,
                ref_case=ref_case,
                expand_refs=expand_refs,
                ref_key=ref_key,
                collection_layout=CollectionLayout.COMPACT,
                multiline_prefix=multiline_prefix,
            ),
            v,
            _maybe_wrap_child(
                parent_id=parent_id,
                wrap_ids=wrap_ids,
                raw_value=v,
                formatted_value=_format_dict_entry_value(
                    value=v,
                    spec=spec,
                    wrap_ids=wrap_ids,
                    outer_sequence_override=outer_sequence_override,
                    position_overrides=position_overrides,
                    ref_case=ref_case,
                    expand_refs=expand_refs,
                    ref_key=ref_key,
                    collection_layout=collection_layout,
                    multiline_prefix=multiline_prefix,
                ),
                spec=spec,
            ),
        )
        for k, v in ordered_map_items
    ]
    joined = spec.element_separator.join(pairs)
    opening = ordered_map_cfg.ordered_map_open(value)
    return opening + joined + ordered_map_cfg.close


@beartype
def _format_dict_value(
    *,
    value: dict[str, Value],
    spec: Language,
    open_override: str | None,
    wrap_ids: frozenset[int],
    ref_case: IdentifierCase | None,
    expand_refs: bool,
    ref_key: str,
    collection_layout: CollectionLayout,
    multiline_prefix: str,
) -> str:
    """Format a dict as a native language literal."""
    dict_cfg = spec.dict_format_config

    dict_items: dict[str, Value] = {
        k: v
        for k, v in value.items()
        if not (spec.skip_null_dict_values and v is None)
    }
    if not dict_items and dict_cfg.empty_dict is not None:
        return dict_cfg.empty_dict
    parent_id = id(value)
    # Widen nested sequences that occupy matching positions across
    # sibling list-valued dict entries, so consumers iterating these
    # values (e.g. tuple-style) see a consistent element type at each
    # position instead of one branch narrowed to a concrete type and
    # another collapsed to the fallback.
    sibling_list_values: list[list[Value]] = [
        v for v in dict_items.values() if isinstance(v, list)
    ]
    outer_sequence_override = _compute_sequence_open_override(
        items=sibling_list_values,
        spec=spec,
    )
    position_overrides = _compute_sibling_list_position_overrides(
        list_values=sibling_list_values,
        spec=spec,
    )
    pairs = [
        _build_dict_entry(
            key_str=_format_value(
                value=k,
                spec=spec,
                dict_open_override=None,
                wrap_ids=wrap_ids,
                sequence_open_override=None,
                ref_case=ref_case,
                expand_refs=expand_refs,
                ref_key=ref_key,
                collection_layout=CollectionLayout.COMPACT,
                multiline_prefix=multiline_prefix,
            ),
            raw_value=v,
            formatted_value=_maybe_wrap_child(
                parent_id=parent_id,
                wrap_ids=wrap_ids,
                raw_value=v,
                formatted_value=_format_dict_entry_value(
                    value=v,
                    spec=spec,
                    wrap_ids=wrap_ids,
                    outer_sequence_override=outer_sequence_override,
                    position_overrides=position_overrides,
                    ref_case=ref_case,
                    expand_refs=expand_refs,
                    ref_key=ref_key,
                    collection_layout=collection_layout,
                    multiline_prefix=multiline_prefix,
                ),
                spec=spec,
            ),
            spec=spec,
        )
        for k, v in dict_items.items()
    ]
    joined = spec.element_separator.join(pairs)
    if open_override is not None:
        opener = open_override
    else:
        open_items = (
            {
                k: v
                for k, v in dict_items.items()
                if _extract_call_arg_ref_name(value=v, ref_key=ref_key) is None
            }
            if expand_refs
            else dict_items
        )
        opener = dict_cfg.dict_open(open_items or dict_items)
    return opener + joined + dict_cfg.close


@beartype
def _format_dict_entry_value(
    *,
    value: Value,
    spec: Language,
    wrap_ids: frozenset[int],
    outer_sequence_override: str | None,
    position_overrides: Sequence[str | None],
    ref_case: IdentifierCase | None,
    expand_refs: bool,
    ref_key: str,
    collection_layout: CollectionLayout,
    multiline_prefix: str,
) -> str:
    """Format a dict entry's value, threading sequence-opener overrides
    into list-typed values so the outer and inner sequences render with
    types that are consistent across sibling dict entries.

    *outer_sequence_override* is the widened opener for the list itself
    (so sibling list-valued entries share one outer type).
    *position_overrides* supplies per-position openers for the list's
    immediate child lists (so nested sequences at matching positions
    across sibling entries share a widened type).
    """
    if isinstance(value, list):
        return _format_list_value(
            value=value,
            spec=spec,
            wrap_ids=wrap_ids,
            sequence_open_override=outer_sequence_override,
            child_sequence_open_overrides=position_overrides,
            ref_case=ref_case,
            expand_refs=expand_refs,
            ref_key=ref_key,
            collection_layout=collection_layout,
            multiline_prefix=multiline_prefix,
        )
    return _format_value(
        value=value,
        spec=spec,
        dict_open_override=None,
        wrap_ids=wrap_ids,
        sequence_open_override=None,
        ref_case=ref_case,
        expand_refs=expand_refs,
        ref_key=ref_key,
        collection_layout=collection_layout,
        multiline_prefix=multiline_prefix,
    )


@beartype
def _compute_dict_open_override(
    *,
    items: list[Value],
    spec: Language,
) -> str | None:
    """Return a widened dict opener when dicts in a list infer
    different value types, or ``None`` when no widening is needed.
    """
    dict_open = spec.dict_format_config.dict_open
    dicts: list[dict[str, Value]] = [
        item
        for item in items
        if isinstance(item, dict) and not isinstance(item, ordereddict)
    ]
    # Widening compares openers across dicts, so we need at least two
    # to have anything to compare.
    min_dicts_for_widening = 2
    if len(dicts) < min_dicts_for_widening:
        return None

    filtered_dicts = [
        {
            k: v
            for k, v in d.items()
            if not (spec.skip_null_dict_values and v is None)
        }
        for d in dicts
    ]

    openers = {dict_open(d) for d in filtered_dicts}
    if len(openers) <= 1:
        return None

    # Types differ: combine all values to infer the widened type.
    # Use the unfiltered dicts so that ``None`` values contribute
    # "unknown type" to the widening — otherwise a dict that filters
    # to ``{}`` would narrow the widened type to the other dicts'
    # concrete value type, losing the null slot's uncertainty.
    combined: dict[str, Value] = {}
    idx = 0
    for d in dicts:
        for v in d.values():
            combined[f"_k{idx}"] = v
            idx += 1
    return dict_open(combined)


@beartype
def _gather_call_slot_values(
    *,
    elements: list[Value],
    ref_key: str,
) -> list[list[Value]]:
    """Group non-ref argument values by positional slot across calls.

    Ref markers are filtered out: the marker isn't rendered as a real
    value at the call site, so its shape must not influence
    sibling-aware widening.
    """
    slots: list[list[Value]] = []
    for element in elements:
        arg_values = element if isinstance(element, list) else [element]
        for slot_index, arg_value in enumerate(iterable=arg_values):
            if slot_index >= len(slots):
                slots.append([])
            is_ref = _extract_call_arg_ref_name(
                value=arg_value, ref_key=ref_key
            )
            if is_ref is None:
                slots[slot_index].append(arg_value)
    return slots


@beartype
def _compute_call_slot_overrides(
    *,
    elements: list[Value],
    spec: Language,
    ref_key: str,
) -> list[str | None]:
    """Compute per-slot dict-open overrides across sibling calls.

    For each positional argument slot in per-element calls, gather the
    values at that slot across all elements and compute a widened
    dict opener so that dict arguments at the same slot share a
    common type.  Sibling calls render as independent statements with
    no enclosing sequence, so ``narrowed_open`` does not apply here —
    each dict still needs its own full opener, just widened when
    sibling dicts differ in inferred value type.
    """
    slots = _gather_call_slot_values(elements=elements, ref_key=ref_key)
    return [
        _compute_dict_open_override(items=slot_values, spec=spec)
        for slot_values in slots
    ]


@beartype
def _compute_call_per_element_wrap_ids(
    *,
    elements: list[Value],
    spec: Language,
    ref_key: str,
) -> frozenset[int]:
    """Compute wrap_ids spanning sibling per-element calls.

    For each positional argument slot, compute wrap_ids on the slot's
    values as if they were siblings inside a single list, then union
    the results.  This mirrors the dict-opener widening done by
    :func:`_compute_call_slot_overrides` so that render-time wrapping
    strategies (e.g. Rust's ``TAGGED_ENUM``) stay consistent across
    sibling calls: a slot whose combined values are heterogeneous
    triggers wrapping in every sibling at that slot, not just the
    ones whose own argument is locally mixed.
    """
    slots = _gather_call_slot_values(elements=elements, ref_key=ref_key)
    return frozenset[int]().union(
        *(
            _compute_wrap_ids(data=slot_values, spec=spec)
            for slot_values in slots
        )
    )


@beartype
def _compute_sequence_dict_override(
    *,
    items: list[Value],
    spec: Language,
) -> str | None:
    """Determine the dict opener override for dicts in a sequence.

    When all items are uniform dicts and the language defines a
    ``narrowed_open``, returns that anonymous opener so the
    sequence type carries the map type instead of each dict.
    Otherwise falls back to the widening logic of
    :func:`_compute_dict_open_override`.
    """
    narrowed_open = spec.dict_format_config.narrowed_open
    if narrowed_open is not None:
        element_type = infer_element_type(items=items)
        if isinstance(element_type, DictType):
            return narrowed_open
    return _compute_dict_open_override(items=items, spec=spec)


@beartype
def _compute_sequence_open_override(
    *,
    items: Sequence[Value],
    spec: Language,
) -> str | None:
    """Return a widened sequence opener when lists in *items* infer
    different element types, or ``None`` when no widening is needed.

    Analogous to :func:`_compute_dict_open_override` but operates on
    nested sequences.  ``items`` are the sibling values at a matching
    position across several sibling containers; only list-typed items
    participate in the widening.  When the element types diverge the
    override widens to the language's fallback opener — the opener
    returned for an empty sequence — so every sibling renders with the
    "accepts anything" type instead of narrowing one branch to its
    concrete element type.

    Languages that use variant-based typing (e.g. C++'s
    ``std::variant``) expose an element-specific opener for every
    shape — their empty-sequence opener is not a true fallback, so
    applying this widening would cascade type mismatches into the
    containing declaration.  Detect that case by comparing the
    empty-sequence opener with the opener for a mixed list; if they
    differ the language has no stable fallback and no widening is
    applied.
    """
    lists: list[list[Value]] = [
        item for item in items if isinstance(item, list)
    ]
    # Widening compares openers across lists, so we need at least two
    # to have anything to compare.
    min_lists_for_widening = 2
    if len(lists) < min_lists_for_widening:
        return None

    openers = {spec.sequence_open(lst) for lst in lists}
    if len(openers) <= 1:
        return None

    fallback = spec.sequence_open([])
    if fallback != spec.sequence_open(_FALLBACK_PROBE):
        return None
    return fallback


# Two scalars of incompatible types, used to probe whether a language's
# sequence opener collapses to a stable "any"-like fallback for mixed
# content.  When the opener for this probe equals the opener for an
# empty sequence the language has a true fallback; otherwise it builds
# a content-specific type (variant, union, etc.) that we must leave
# alone to avoid cascading type mismatches.
_FALLBACK_PROBE: list[Value] = [1, "probe"]


@beartype
def _compute_sibling_list_position_overrides(
    *,
    list_values: list[list[Value]],
    spec: Language,
) -> list[str | None]:
    """Compute per-position sequence-open overrides across sibling lists.

    For each position ``i`` across the given sibling lists, gather the
    items at that position and compute a widened sequence opener so
    that sub-lists sharing the same positional slot across siblings
    render with a common element type.  ``None`` at a given position
    means no widening is needed there.

    Returns an empty list when fewer than two sibling lists are
    provided, since widening requires siblings to compare against.
    """
    min_lists_for_widening = 2
    if len(list_values) < min_lists_for_widening:
        return []
    max_len = max(len(lst) for lst in list_values)
    slots: list[list[Value]] = [[] for _ in range(max_len)]
    for lst in list_values:
        for position, item in enumerate(iterable=lst):
            slots[position].append(item)
    return [
        _compute_sequence_open_override(items=slot_values, spec=spec)
        for slot_values in slots
    ]


@beartype
def _empty_child_sibling_opener(
    *,
    value: list[Value],
    position: int,
    spec: Language,
) -> str | None:
    """Opener to use for an empty inner-list child at *position*.

    Empty inner lists have no contents to infer a type from, so the
    default per-list opener falls back to the language's generic
    "any"-typed sequence (e.g. ``new Object[]{``, ``[]any{``,
    ``Vec::<String>::new()``).  When that empty list sits beside
    non-empty homogeneous list siblings, the rendered literal then
    mixes the narrow sibling type with the generic empty type and is
    rejected by the static type checkers used for Java, Rust, Go, etc.

    Pull a typed opener from a non-empty list sibling when all such
    siblings produce the same opener, so the empty list renders with
    a matching type.  Returns ``None`` when no homogeneous sibling
    opener exists and the default fallback should stand.
    """
    item = value[position]
    if not (isinstance(item, list) and not item):
        return None
    non_empty_siblings = [
        other for other in value if isinstance(other, list) and other
    ]
    if not non_empty_siblings:
        return None
    sibling_openers = {spec.sequence_open(o) for o in non_empty_siblings}
    if len(sibling_openers) != 1:
        return None
    return next(iter(sibling_openers))


@beartype
def _format_sequence_child(
    *,
    value: list[Value],
    position: int,
    child: Value,
    spec: Language,
    wrap_ids: frozenset[int],
    dict_open_override: str | None,
    child_sequence_open_overrides: Sequence[str | None],
    ref_case: IdentifierCase | None,
    expand_refs: bool,
    ref_key: str,
    collection_layout: CollectionLayout,
    multiline_prefix: str,
) -> str:
    """Format a single sequence child with sibling-aware typed empty.

    Empty inner-list children sit beside non-empty homogeneous siblings
    in cases like ``[[1, 2], [], [3, 4]]``.  When the language has a
    bespoke narrowed-empty form (e.g. ``List[Int]()`` for Mojo,
    ``[] of Int32`` for Crystal, ``[] : List Natural`` for Dhall),
    short-circuit to it so the rendered literal type-checks.  Otherwise
    fall through to the regular recursive formatter, which uses
    sibling-derived ``sequence_open_override`` to make the empty list
    render as ``opener + close`` for languages where that is valid
    (Java, Go, Rust, ...).
    """
    parent_override = (
        child_sequence_open_overrides[position]
        if (
            position < len(child_sequence_open_overrides)
            and child_sequence_open_overrides[position] is not None
        )
        else None
    )
    sibling_open = (
        None
        if parent_override is not None
        else _empty_child_sibling_opener(
            value=value,
            position=position,
            spec=spec,
        )
    )
    if (
        parent_override is None
        and isinstance(child, list)
        and not child
        and sibling_open is not None
    ):
        narrowed_empty_form = spec.sequence_format_config.narrowed_empty_form
        if narrowed_empty_form is not None:
            non_empty_siblings = [
                other for other in value if isinstance(other, list) and other
            ]
            return narrowed_empty_form(non_empty_siblings)
    return _format_value(
        value=child,
        spec=spec,
        dict_open_override=dict_open_override,
        wrap_ids=wrap_ids,
        sequence_open_override=(
            parent_override if parent_override is not None else sibling_open
        ),
        ref_case=ref_case,
        expand_refs=expand_refs,
        ref_key=ref_key,
        collection_layout=collection_layout,
        multiline_prefix=multiline_prefix,
    )


@beartype
def _format_list_value(
    *,
    value: list[Value],
    spec: Language,
    wrap_ids: frozenset[int],
    sequence_open_override: str | None,
    child_sequence_open_overrides: Sequence[str | None],
    ref_case: IdentifierCase | None,
    expand_refs: bool,
    ref_key: str,
    collection_layout: CollectionLayout,
    multiline_prefix: str,
) -> str:
    """Format a list as a native language literal.

    *sequence_open_override* overrides the opener for this list itself
    (used when a parent has widened nested sequence types across
    sibling positions).

    *child_sequence_open_overrides* supplies per-position sequence
    openers for child lists, so nested sequences at matching positions
    across sibling containers can share a widened type.
    """
    sequence_cfg = spec.sequence_format_config

    # When a parent has widened this position's opener, skip the
    # default ``empty_sequence`` literal so the empty list still
    # renders with the widened opener and stays type-consistent with
    # its non-empty siblings.  However, if this list is in wrap_ids,
    # it must use the typed empty literal (e.g. ``[]TYPE{}``) regardless
    # of any sibling opener, so that the element type is preserved.
    if (
        not value
        and sequence_cfg.empty_sequence is not None
        and (sequence_open_override is None or id(value) in wrap_ids)
    ):
        return sequence_cfg.empty_sequence
    if collection_layout is CollectionLayout.MULTILINE and value:
        return _format_multiline_collection_value(
            value=value,
            spec=spec,
            line_prefix=multiline_prefix,
            wrap_ids=wrap_ids,
            ref_case=ref_case,
            expand_refs=expand_refs,
            ref_key=ref_key,
            sequence_open_override=sequence_open_override,
        )
    dict_open_override = _compute_sequence_dict_override(
        items=value,
        spec=spec,
    )
    parent_id = id(value)
    items = [
        spec.format_sequence_entry(
            v,
            _maybe_wrap_child(
                parent_id=parent_id,
                wrap_ids=wrap_ids,
                raw_value=v,
                formatted_value=_format_sequence_child(
                    value=value,
                    position=position,
                    child=v,
                    spec=spec,
                    wrap_ids=wrap_ids,
                    dict_open_override=dict_open_override,
                    child_sequence_open_overrides=(
                        child_sequence_open_overrides
                    ),
                    ref_case=ref_case,
                    expand_refs=expand_refs,
                    ref_key=ref_key,
                    collection_layout=collection_layout,
                    multiline_prefix=multiline_prefix,
                ),
                spec=spec,
            ),
        )
        for position, v in enumerate(iterable=value)
    ]
    # Drop items that render to the empty string before joining, so a
    # nested empty sub-list inside a non-empty list (possible in
    # languages like Forth whose empty-sequence opener and close are
    # both empty) does not leave a dangling separator in the output.
    non_empty_items = [item for item in items if item]
    joined = spec.element_separator.join(non_empty_items)
    # Some languages (e.g. Python) require a trailing comma on
    # single-element sequences to avoid syntactic ambiguity.  The
    # decision uses the original element count so filtered-away empty
    # sub-lists do not flip a multi-element list into the trailing-
    # comma branch.
    if len(items) == 1 and sequence_cfg.single_element_trailing_comma:
        joined += spec.element_separator.strip()
    if sequence_open_override is not None:
        opener = sequence_open_override
    else:
        open_value = (
            [
                v
                for v in value
                if _extract_call_arg_ref_name(value=v, ref_key=ref_key) is None
            ]
            if expand_refs
            else value
        )
        opener = spec.sequence_open(open_value or value)
    return f"{opener}{joined}{sequence_cfg.close}"


@beartype
def _format_value(
    *,
    value: Value,
    spec: Language,
    dict_open_override: str | None,
    wrap_ids: frozenset[int],
    sequence_open_override: str | None,
    ref_case: IdentifierCase | None,
    expand_refs: bool,
    ref_key: str,
    collection_layout: CollectionLayout,
    multiline_prefix: str,
) -> str:
    """Format any JSON value as a native language literal.

    Handles scalars, lists (recursively), dicts, and sets.

    When *dict_open_override* is set, dict values use it as the opening
    delimiter instead of inferring the type from their own values.
    This is used to widen map value types when dicts with differing
    inferred types appear in the same sequence.

    When *sequence_open_override* is set, list values use it as the
    opening delimiter instead of inferring their element type.  This
    widens nested sequence types at matching positions across sibling
    containers.

    *wrap_ids* is the set of container ids whose scalar children should
    be wrapped by the spec's
    :attr:`~literalizer._language.HeterogeneousBehavior.wrap_scalar`
    hook.

    When *ref_case* is set or *expand_refs* is ``True``,
    ``{"$ref": "name"}`` markers anywhere in the value tree are rendered
    as bare identifiers via
    :attr:`~literalizer._language.Language.format_call_ref_identifier`.
    When *ref_case* is set the identifier name is converted to that case
    first.  When both are absent, ref dicts are
    formatted as ordinary literal dicts.
    """
    if ref_case is not None or expand_refs:
        ref_name = _extract_call_arg_ref_name(value=value, ref_key=ref_key)
        if ref_name is not None:
            if ref_case is not None:
                ref_name = ref_case.convert(name=ref_name)
            return (
                spec.format_call_arg_ref_identifier(ref_name)
                if expand_refs
                else spec.format_call_ref_identifier(ref_name)
            )
    if (
        collection_layout is CollectionLayout.MULTILINE
        and isinstance(value, (dict, list, set, ordereddict))
        and value
    ):
        return _format_multiline_collection_value(
            value=value,
            spec=spec,
            line_prefix=multiline_prefix,
            wrap_ids=wrap_ids,
            ref_case=ref_case,
            expand_refs=expand_refs,
            ref_key=ref_key,
            dict_open_override=dict_open_override,
            sequence_open_override=sequence_open_override,
        )
    match value:
        case ordereddict():
            result = _format_ordered_map_value(
                value=value,
                spec=spec,
                wrap_ids=wrap_ids,
                ref_case=ref_case,
                expand_refs=expand_refs,
                ref_key=ref_key,
                collection_layout=collection_layout,
                multiline_prefix=multiline_prefix,
            )
        case dict():
            result = _format_dict_value(
                value=value,
                spec=spec,
                open_override=dict_open_override,
                wrap_ids=wrap_ids,
                ref_case=ref_case,
                expand_refs=expand_refs,
                ref_key=ref_key,
                collection_layout=collection_layout,
                multiline_prefix=multiline_prefix,
            )
        case set():
            result = _format_set_value(
                value=value,
                spec=spec,
                wrap_ids=wrap_ids,
            )
        case list():  # pragma: no branch
            result = _format_list_value(
                value=value,
                spec=spec,
                wrap_ids=wrap_ids,
                sequence_open_override=sequence_open_override,
                child_sequence_open_overrides=(),
                ref_case=ref_case,
                expand_refs=expand_refs,
                ref_key=ref_key,
                collection_layout=collection_layout,
                multiline_prefix=multiline_prefix,
            )
        case _:
            result = _format_scalar(value=value, spec=spec)
    return result


@beartype
def _wrap_body(
    *,
    body: str,
    is_ordered_map: bool,
    data: list[Value] | dict[str, Value] | set[Scalar],
    spec: Language,
    line_prefix: str,
) -> str:
    """Wrap ``body`` in the language's open/close delimiters."""
    ci = spec.indent if spec.indent_closing_delimiter else ""
    close_prefix = f"{line_prefix}{ci}"
    match data:
        case dict() if is_ordered_map:
            ordered_map_cfg = spec.ordered_map_format_config
            open_str = ordered_map_cfg.ordered_map_open(data)
            opening = f"{line_prefix}{open_str}"
            closing = f"{close_prefix}{ordered_map_cfg.close}"
        case dict():
            dict_cfg = spec.dict_format_config
            opening = f"{line_prefix}{dict_cfg.dict_open(data)}"
            closing = f"{close_prefix}{dict_cfg.close}"
        case set():
            sorted_set: list[Value] = sorted(
                data,
                key=lambda v: (type(v).__name__, repr(v)),
            )
            set_cfg = spec.set_format_config
            opening = f"{line_prefix}{set_cfg.set_open(sorted_set)}"
            closing = f"{close_prefix}{set_cfg.close}"
        case _:
            opening = f"{line_prefix}{spec.sequence_open(data)}"
            closing = f"{close_prefix}{spec.sequence_format_config.close}"
    return f"{opening.rstrip()}\n{body}\n{closing}"


@beartype
def _collection_open_for_multiline_value(
    *,
    data: dict[str, Value] | set[Scalar] | list[Value],
    spec: Language,
    is_ordered_map: bool,
    dict_open_override: str | None,
    sequence_open_override: str | None,
    expand_refs: bool,
    ref_key: str,
) -> str:
    """Return an opener without a leading prefix.

    Used for a nested multiline collection.
    """
    if isinstance(data, dict):
        if is_ordered_map:
            return spec.ordered_map_format_config.ordered_map_open(data)
        if dict_open_override is not None:
            return dict_open_override
        dict_open_items = (
            {
                k: v
                for k, v in data.items()
                if _extract_call_arg_ref_name(value=v, ref_key=ref_key) is None
            }
            if expand_refs
            else data
        )
        return spec.dict_format_config.dict_open(dict_open_items or data)
    if isinstance(data, set):
        sorted_set: list[Value] = sorted(
            data,
            key=lambda v: (type(v).__name__, repr(v)),
        )
        return spec.set_format_config.set_open(sorted_set)
    if sequence_open_override is not None:
        return sequence_open_override
    sequence_open_items = (
        [
            v
            for v in data
            if _extract_call_arg_ref_name(value=v, ref_key=ref_key) is None
        ]
        if expand_refs
        else data
    )
    return spec.sequence_open(sequence_open_items or data)


@beartype
def _format_multiline_collection_value(
    *,
    value: dict[str, Value] | set[Scalar] | list[Value],
    spec: Language,
    line_prefix: str,
    wrap_ids: frozenset[int],
    ref_case: IdentifierCase | None,
    expand_refs: bool,
    ref_key: str,
    dict_open_override: str | None = None,
    sequence_open_override: str | None = None,
) -> str:
    """Format a nested collection whose first delimiter has no leading
    prefix.

    The caller adds its own entry prefix to the first line. Continuation
    lines and the closing delimiter are prefixed here so nested layouts align
    under that entry.
    """
    is_ordered_map = isinstance(value, ordereddict)
    trailing_comma = spec.trailing_comma_config.multiline_trailing_comma
    body_prefix = line_prefix + spec.indent
    lines = _format_collection_lines(
        data=value,
        spec=spec,
        body_prefix=body_prefix,
        trailing_comma=trailing_comma,
        is_ordered_map=is_ordered_map,
        wrap_ids=wrap_ids,
        ref_case=ref_case,
        expand_refs=expand_refs,
        ref_key=ref_key,
        collection_layout=CollectionLayout.MULTILINE,
    )
    body = "\n".join(lines)
    opening = _collection_open_for_multiline_value(
        data=value,
        spec=spec,
        is_ordered_map=is_ordered_map,
        dict_open_override=dict_open_override,
        sequence_open_override=sequence_open_override,
        expand_refs=expand_refs,
        ref_key=ref_key,
    ).rstrip()
    closing_indent = spec.indent if spec.indent_closing_delimiter else ""
    close_prefix = line_prefix + closing_indent
    match value:
        case dict() if is_ordered_map:
            close = spec.ordered_map_format_config.close
        case dict():
            close = spec.dict_format_config.close
        case set():
            close = spec.set_format_config.close
        case _:
            close = spec.sequence_format_config.close
    return f"{opening}\n{body}\n{close_prefix}{close}"


@beartype
def _rstrip_lines(text: str) -> str:
    """Remove trailing whitespace from each line."""
    return "\n".join(line.rstrip() for line in text.split(sep="\n"))


@beartype
def _append_entries(
    *,
    formatted_entries: Sequence[str],
    lines: list[str],
    body_prefix: str,
    trailing_comma: bool,
    spec: Language,
) -> None:
    """Append formatted entries with separators to *lines*."""
    last_idx = len(formatted_entries) - 1
    for i, entry in enumerate(iterable=formatted_entries):
        add_sep = i < last_idx or trailing_comma
        sep = spec.element_separator.strip() if add_sep else ""
        lines.append(f"{body_prefix}{_rstrip_lines(text=entry)}{sep}")


@beartype
def _format_collection_lines(
    *,
    data: dict[str, Value] | set[Scalar] | list[Value],
    spec: Language,
    body_prefix: str,
    trailing_comma: bool,
    is_ordered_map: bool,
    wrap_ids: frozenset[int],
    ref_case: IdentifierCase | None,
    expand_refs: bool,
    ref_key: str,
    collection_layout: CollectionLayout,
) -> list[str]:
    """Format collection elements as indented lines."""
    lines: list[str] = []
    parent_id = id(data)
    match data:
        case dict() as dict_data:
            entries = [
                (k, v)
                for k, v in dict_data.items()
                if not (spec.skip_null_dict_values and v is None)
            ]
            sibling_list_values: list[list[Value]] = [
                v for _, v in entries if isinstance(v, list)
            ]
            outer_sequence_override = _compute_sequence_open_override(
                items=sibling_list_values,
                spec=spec,
            )
            position_overrides = _compute_sibling_list_position_overrides(
                list_values=sibling_list_values,
                spec=spec,
            )
            formatted_entries: list[str] = []
            for k, v in entries:
                formatted_key: str = _format_value(
                    value=k,
                    spec=spec,
                    dict_open_override=None,
                    wrap_ids=wrap_ids,
                    sequence_open_override=None,
                    ref_case=ref_case,
                    expand_refs=False,
                    ref_key=ref_key,
                    collection_layout=CollectionLayout.COMPACT,
                    multiline_prefix=body_prefix,
                )
                formatted_val = _maybe_wrap_child(
                    parent_id=parent_id,
                    wrap_ids=wrap_ids,
                    raw_value=v,
                    formatted_value=_format_dict_entry_value(
                        value=v,
                        spec=spec,
                        wrap_ids=wrap_ids,
                        outer_sequence_override=outer_sequence_override,
                        position_overrides=position_overrides,
                        ref_case=ref_case,
                        expand_refs=expand_refs,
                        ref_key=ref_key,
                        collection_layout=collection_layout,
                        multiline_prefix=body_prefix,
                    ),
                    spec=spec,
                )
                entry = (
                    spec.format_ordered_map_entry(
                        formatted_key, v, formatted_val
                    )
                    if is_ordered_map
                    else _build_dict_entry(
                        key_str=formatted_key,
                        raw_value=v,
                        formatted_value=formatted_val,
                        spec=spec,
                    )
                )
                formatted_entries.append(entry)
            dict_trailing = (
                trailing_comma
                and spec.dict_format_config.supports_trailing_comma
            )
            _append_entries(
                formatted_entries=formatted_entries,
                lines=lines,
                body_prefix=body_prefix,
                trailing_comma=dict_trailing,
                spec=spec,
            )
        case set() as set_data:
            sorted_items = sorted(
                set_data,
                key=lambda v: (type(v).__name__, repr(v)),
            )
            set_parent_id = id(set_data)
            formatted_entries = [
                spec.format_set_entry(
                    item,
                    _maybe_wrap_child(
                        parent_id=set_parent_id,
                        wrap_ids=wrap_ids,
                        raw_value=item,
                        formatted_value=_format_value(
                            value=item,
                            spec=spec,
                            dict_open_override=None,
                            wrap_ids=wrap_ids,
                            sequence_open_override=None,
                            ref_case=ref_case,
                            expand_refs=expand_refs,
                            ref_key=ref_key,
                            collection_layout=collection_layout,
                            multiline_prefix=body_prefix,
                        ),
                        spec=spec,
                    ),
                )
                for item in sorted_items
            ]
            set_trailing = (
                trailing_comma
                and spec.set_format_config.supports_trailing_comma
            )
            _append_entries(
                formatted_entries=formatted_entries,
                lines=lines,
                body_prefix=body_prefix,
                trailing_comma=set_trailing,
                spec=spec,
            )
        case list() as list_data:
            seq_trailing = (
                trailing_comma
                and spec.sequence_format_config.supports_trailing_comma
            )
            dict_open_override = _compute_sequence_dict_override(
                items=list_data,
                spec=spec,
            )
            formatted_entries = [
                spec.format_sequence_entry(
                    element,
                    _maybe_wrap_child(
                        parent_id=parent_id,
                        wrap_ids=wrap_ids,
                        raw_value=element,
                        formatted_value=_format_sequence_child(
                            value=list_data,
                            position=position,
                            child=element,
                            spec=spec,
                            wrap_ids=wrap_ids,
                            dict_open_override=dict_open_override,
                            child_sequence_open_overrides=(),
                            ref_case=ref_case,
                            expand_refs=expand_refs,
                            ref_key=ref_key,
                            collection_layout=collection_layout,
                            multiline_prefix=body_prefix,
                        ),
                        spec=spec,
                    ),
                )
                for position, element in enumerate(iterable=list_data)
            ]
            # Drop entries that render to the empty string so a nested
            # empty sub-list (possible in languages like Forth whose
            # empty-sequence opener and close are both empty) does not
            # leave a dangling indented blank line in the output.
            formatted_entries = [e for e in formatted_entries if e]
            _append_entries(
                formatted_entries=formatted_entries,
                lines=lines,
                body_prefix=body_prefix,
                trailing_comma=seq_trailing,
                spec=spec,
            )
        case _ as unreachable:
            assert_never(unreachable)
    return lines


@beartype(conf=BeartypeConf(is_pep484_tower=True))
def _literalize(
    *,
    data: Value,
    language: Language,
    line_prefix: str,
    include_delimiters: bool,
    ref_case: IdentifierCase | None,
    ref_key: str,
    collection_layout: CollectionLayout,
) -> str:
    r"""Convert data to native language literal text.

    Each element (or key-value pair) is formatted as a native literal
    for the given language with a trailing comma and the language's
    indent.

    Args:
        data: A scalar, sequence, or mapping.  Scalars (strings,
            numbers, booleans, ``None``, :class:`datetime.date`,
            :class:`datetime.datetime`) are formatted as a single
            literal value.  Sequences may contain scalars, sequences,
            or mappings with nesting to arbitrary depth.  Mappings are
            formatted as one key-value pair per line using the
            language's dict separator.
        language: A :class:`Language` instance describing how to format
            literals.  Use one of the built-in constants
            (e.g. :data:`PYTHON`, :data:`GO`) or provide your own.
        line_prefix: String to prepend to every output line
            (e.g. ``"        "`` for 8-space margin, or ``"\t\t"``
            for 2-tab margin).  Positions the generated block at
            the right column in surrounding source code.
        include_delimiters: If True, include the collection delimiters
            (``[`` … ``]`` for arrays, ``{`` … ``}`` for dicts).
            Ignored for scalar values.
        ref_case: When set, any ref mapping is rendered as a bare
            identifier instead of a literal dict.
        ref_key: The key used to identify ref markers in the input.
        collection_layout: Controls layout for collections nested
            inside other collections.
    """
    if ref_case is not None:
        ref_name = _extract_call_arg_ref_name(value=data, ref_key=ref_key)
        if ref_name is not None:
            ref_name = ref_case.convert(name=ref_name)
            identifier = language.format_call_ref_identifier(ref_name)
            return f"{line_prefix}{identifier}"

    check_data(data=data, spec=language)

    wrap_ids = _compute_wrap_ids(data=data, spec=language)

    # Handle scalars (check ``str`` before Sequence since ``str`` is a
    # Sequence, and datetime before date since datetime subclasses
    # date).
    scalar_types = (
        str,
        bytes,
        int,
        float,
        bool,
        datetime.datetime,
        datetime.date,
    )
    if isinstance(data, scalar_types) or data is None:
        return f"{line_prefix}{_format_scalar(value=data, spec=language)}"

    # Empty collections have no elements to lay out line-by-line, so
    # delegate to _format_value which already returns the correct
    # compact representation (e.g. ``{}``, ``[]``).
    if not data and include_delimiters:
        formatted: str = _format_value(
            value=data,
            spec=language,
            dict_open_override=None,
            wrap_ids=wrap_ids,
            sequence_open_override=None,
            ref_case=ref_case,
            expand_refs=False,
            ref_key=ref_key,
            collection_layout=collection_layout,
            multiline_prefix=line_prefix,
        )
        return f"{line_prefix}{formatted}"

    # When all dict values are null and the spec skips nulls, the dict
    # collapses to an empty-collection literal.
    if (
        isinstance(data, dict)
        and include_delimiters
        and language.skip_null_dict_values
        and all(v is None for v in data.values())
    ):
        is_ordered_map = isinstance(data, ordereddict)
        empty_value: ordereddict | dict[str, Value] = (
            ordereddict() if is_ordered_map else {}
        )
        formatted = _format_value(
            value=empty_value,
            spec=language,
            dict_open_override=None,
            wrap_ids=wrap_ids,
            sequence_open_override=None,
            ref_case=ref_case,
            expand_refs=False,
            ref_key=ref_key,
            collection_layout=collection_layout,
            multiline_prefix=line_prefix,
        )
        return f"{line_prefix}{formatted}"

    body_prefix = (
        line_prefix + language.indent if include_delimiters else line_prefix
    )

    is_ordered_map = isinstance(data, ordereddict)
    trailing_comma = language.trailing_comma_config.multiline_trailing_comma
    lines: list[str] = _format_collection_lines(
        data=data,
        spec=language,
        body_prefix=body_prefix,
        trailing_comma=trailing_comma,
        is_ordered_map=is_ordered_map,
        wrap_ids=wrap_ids,
        ref_case=ref_case,
        expand_refs=False,
        ref_key=ref_key,
        collection_layout=collection_layout,
    )

    body = "\n".join(lines)

    if not include_delimiters or not body:
        return body

    return _wrap_body(
        body=body,
        is_ordered_map=is_ordered_map,
        data=data,
        spec=language,
        line_prefix=line_prefix,
    )


@beartype
def _apply_variable_wrapper(
    *,
    result: str,
    language: Language,
    data: Value,
    variable_form: NewVariable | ExistingVariable | None,
    line_prefix: str,
) -> str:
    """Optionally wrap *result* in a variable declaration or
    assignment.

    *result* arrives with *line_prefix* already prepended to every
    line.  When wrapping in a variable form the leading prefix on the
    first line is stripped so the value sits flush against the
    declaration's ``=``, then re-prepended once to the entire wrapped
    output.  This keeps every line uniformly indented instead of
    doubly-indenting continuation lines.
    """
    if variable_form is None:
        return result

    if line_prefix and result.startswith(line_prefix):
        value = result[len(line_prefix) :]
    else:
        value = result

    match variable_form:
        case NewVariable(name=name, modifiers=modifiers):
            wrapped = language.format_variable_declaration(
                name,
                value,
                data,
                modifiers,
            )
        case _:
            wrapped = language.format_variable_assignment(
                variable_form.name,
                value,
                data,
            )

    return line_prefix + wrapped


@dataclasses.dataclass(frozen=True)
class _PreFormState:
    """Variable-form-independent results of
    :func:`_literalize_pre_form`.
    """

    data: Value
    result: str
    resolved: ResolvedComments | None
    line_prefix: str


@beartype
def _literalize_pre_form(
    *,
    source: str,
    input_format: InputFormat,
    language: Language,
    pre_indent_level: int,
    include_delimiters: bool,
    ref_case: IdentifierCase | None,
    ref_key: str,
    collection_layout: CollectionLayout,
) -> _PreFormState:
    """Run the variable-form-independent phase of :func:`literalize`.

    Parses the source, formats the literal, and resolves YAML/TOML
    comments.
    """
    line_prefix = language.indent * pre_indent_level
    parsed = parse_input(source=source, input_format=input_format)
    data = parsed.data

    language.validate_spec_for_data(data=data)

    result = _literalize(
        data=data,
        language=language,
        line_prefix=line_prefix,
        include_delimiters=include_delimiters,
        ref_case=ref_case,
        ref_key=ref_key,
        collection_layout=collection_layout,
    )

    comment_line_prefix = (
        line_prefix + language.indent if include_delimiters else line_prefix
    )

    resolved: ResolvedComments | None = None
    match input_format:
        case InputFormat.YAML if parsed.yaml_needs_comment_resolve:
            comment_cfg = language.comment_config
            cp = comment_cfg.prefix
            cs = comment_cfg.suffix
            resolved = resolve_yaml_comments(
                yaml_string=source,
                raw_data=parsed.raw_data,
                base=result,
                language=language,
                comment_prefix=cp,
                comment_suffix=cs,
                comment_line_prefix=comment_line_prefix,
                line_prefix=line_prefix,
                include_delimiters=include_delimiters,
            )
            result = resolved.result
        case InputFormat.TOML:
            comment_cfg = language.comment_config
            resolved = resolve_toml_comments(
                toml_doc=parsed.raw_data,
                base=result,
                language=language,
                comment_prefix=comment_cfg.prefix,
                comment_suffix=comment_cfg.suffix,
                comment_line_prefix=comment_line_prefix,
                include_delimiters=include_delimiters,
            )
            result = resolved.result
        case _:
            pass

    return _PreFormState(
        data=data,
        result=result,
        resolved=resolved,
        line_prefix=line_prefix,
    )


@beartype
def _literalize_apply_form(
    *,
    pre_form: _PreFormState,
    language: Language,
    variable_form: NewVariable | ExistingVariable | None,
    wrap_in_file: bool,
) -> LiteralizeResult:
    """Apply variable-form-specific wrapping on top of a pre-form pass.

    Performs variable wrapping, handles any pending collection
    comments, computes the preamble, and optionally wraps the output
    in a complete file.
    """
    result = _apply_variable_wrapper(
        result=pre_form.result,
        language=language,
        data=pre_form.data,
        variable_form=variable_form,
        line_prefix=pre_form.line_prefix,
    )

    resolved = pre_form.resolved
    if resolved is not None and resolved.pending is not None:
        comment_cfg = language.comment_config
        result = prepend_collection_comments(
            collection_comments=resolved.pending,
            base=result,
            comment_prefix=comment_cfg.prefix,
            comment_suffix=comment_cfg.suffix,
            line_prefix=pre_form.line_prefix,
        )

    variable_name = variable_form.name if variable_form is not None else None
    is_declaration = isinstance(variable_form, NewVariable)
    computed = compute_preamble(
        data=pre_form.data,
        language=language,
        has_variable_declaration=variable_name is not None and is_declaration,
    )
    preamble = deduplicate_preamble_entries(
        entries=(
            tuple(language.static_preamble)
            + computed.header
            + language.data_dependent_preamble(pre_form.data)
        )
    )

    pre_decl = resolved.pending_scalar_before if resolved is not None else ()

    if wrap_in_file:
        content = result
        if pre_decl:
            content = "\n".join(pre_decl) + "\n" + content
        wrapped = language.wrap_in_file(
            content=content,
            variable_name=variable_name or "",
            body_preamble=computed.body,
        )
        if preamble:
            wrapped = "\n".join(preamble) + "\n" + wrapped
        return LiteralizeResult(
            declaration_code=wrapped,
            preamble=(),
            body_preamble=(),
            types_present=computed.types_present,
            source_data=pre_form.data,
        )

    return LiteralizeResult(
        declaration_code=result,
        preamble=preamble,
        body_preamble=computed.body,
        pre_declaration_comments=pre_decl,
        types_present=computed.types_present,
        source_data=pre_form.data,
    )


@beartype
def _literalize_both_forms(
    *,
    source: str,
    input_format: InputFormat,
    language: Language,
    pre_indent_level: int,
    include_delimiters: bool,
    variable_form: BothVariableForms,
    ref_case: IdentifierCase | None,
    ref_key: str,
    collection_layout: CollectionLayout,
) -> LiteralizeResult:
    """Produce combined declaration + assignment output."""
    pre_form = _literalize_pre_form(
        source=source,
        input_format=input_format,
        language=language,
        pre_indent_level=pre_indent_level,
        include_delimiters=include_delimiters,
        ref_case=ref_case,
        ref_key=ref_key,
        collection_layout=collection_layout,
    )
    declaration = _literalize_apply_form(
        pre_form=pre_form,
        language=language,
        variable_form=NewVariable(
            name=variable_form.name,
            modifiers=variable_form.modifiers,
        ),
        wrap_in_file=False,
    )
    assignment = _literalize_apply_form(
        pre_form=pre_form,
        language=language,
        variable_form=ExistingVariable(name=variable_form.name),
        wrap_in_file=False,
    )
    decl_preamble = (
        *declaration.body_preamble,
        *declaration.pre_declaration_comments,
    )
    wrapped = language.wrap_combined_in_file(
        declaration=declaration.declaration_code,
        assignment=assignment.bare_code,
        variable_name=variable_form.name,
        body_preamble=decl_preamble,
    )
    if declaration.preamble:
        wrapped = "\n".join(declaration.preamble) + "\n" + wrapped
    return LiteralizeResult(
        declaration_code=wrapped,
        preamble=(),
        body_preamble=(),
        types_present=declaration.types_present,
        source_data=declaration.source_data,
    )


@beartype
def literalize(
    *,
    source: str,
    input_format: InputFormat,
    language: Language,
    pre_indent_level: int = 0,
    include_delimiters: bool = True,
    variable_form: VariableForm | None = None,
    wrap_in_file: bool = False,
    ref_case: IdentifierCase | None = None,
    ref_key: str = "$ref",
    collection_layout: CollectionLayout = CollectionLayout.COMPACT,
) -> LiteralizeResult:
    r"""Convert a JSON, JSON5, YAML, or TOML string to a native
    language literal.

    YAML and TOML comments are preserved in the output using the
    target language's comment syntax.

    Args:
        source: The input string to convert.
        input_format: The serialization format of *source*.
        language: A :class:`Language` instance describing how to format
            literals.  Use one of the built-in constants
            (e.g. :data:`PYTHON`, :data:`GO`) or provide your own.
            Languages whose ``wrap_in_file`` introduces a named scope
            (the wrapping class in Java, the ``program`` in Fortran,
            the ``-module`` in Erlang) carry that name as a constructor
            argument (``Java(module_name="Foo")``); languages whose
            wrappers do not introduce a named scope take no such
            argument.
        pre_indent_level: Number of ``indent`` steps to prepend to
            every output line.  For example, ``2`` with a 4-space
            indent produces an 8-space margin.  Defaults to ``0``.
        include_delimiters: If True, include the collection delimiters
            (``[`` … ``]`` for arrays, ``{`` … ``}`` for dicts).
        variable_form: Controls how the output is wrapped in a variable.
            Pass :class:`NewVariable` to use
            ``format_variable_declaration`` (e.g. ``const x =`` in
            JavaScript), :class:`ExistingVariable` to use
            ``format_variable_assignment`` (e.g. ``x =``),
            or :class:`BothVariableForms` to produce both a declaration
            and an assignment combined in one output (requires
            *wrap_in_file*).  ``None`` (default) means no variable
            wrapping.
        wrap_in_file: If ``True``, assemble :attr:`code` as a
            complete, valid source file using the language's
            ``wrap_in_file`` method and prepend :attr:`preamble`.
            When set, :attr:`preamble` and :attr:`body_preamble`
            on the result are empty tuples (their content has been
            folded into :attr:`code`).
        ref_case: When set, ``{ref_key: "name"}`` markers anywhere in
            the data are rendered as bare identifiers using the
            language's
            :attr:`~literalizer._language.Language.format_call_ref_identifier`
            hook, with the identifier name first converted to
            *ref_case*.  When ``None`` (default), such dicts are treated
            as ordinary literal dicts with no special handling.
        ref_key: The dict key used to identify variable-reference
            markers in the input data.  A single-key dict whose key
            equals *ref_key* and whose value is a string is treated as a
            ref marker when *ref_case* is set.  Defaults to ``"$ref"``.
        collection_layout: Controls layout for collections nested
            inside other collections.  ``CollectionLayout.COMPACT``
            preserves the existing one-line nested rendering, while
            ``CollectionLayout.MULTILINE`` expands non-empty nested
            collections with one element per line.

    Raises:
        JSONParseError: If *input_format* is ``JSON`` and *source* is
            not valid JSON.
        JSON5ParseError: If *input_format* is ``JSON5`` and *source*
            is not valid JSON5.
        YAMLParseError: If *input_format* is ``YAML`` and *source* is
            not valid YAML.
        TOMLParseError: If *input_format* is ``TOML`` and *source* is
            not valid TOML.
        HeterogeneousCollectionError: If the data contains collections
            whose shape cannot be represented in the target language
            (e.g. heterogeneous scalar types in a language that requires
            homogeneous collections).
        ValueError: If *variable_form* is :class:`BothVariableForms`
            and *wrap_in_file* is ``False``, or if the language's
            ``declaration_style`` does not support redefinition.
        UnsupportedIdentifierCaseError: If *ref_case* is not in
            :attr:`~literalizer._language.Language.identifier_cases`
            for the target language.
        VariableNamesNotSupportedError: If *variable_form* is supplied
            for a language that does not support variable names.
    """
    if variable_form is not None and not language.supports_variable_names:
        raise VariableNamesNotSupportedError(
            language_name=type(language).__name__,
        )
    if ref_case is not None and ref_case not in language.identifier_cases:
        raise UnsupportedIdentifierCaseError(
            language_name=type(language).__name__,
            case_name=ref_case.name,
        )
    if isinstance(variable_form, BothVariableForms):
        if not wrap_in_file:
            msg = "BothVariableForms requires wrap_in_file=True"
            raise ValueError(msg)
        if not language.declaration_style.value.supports_redefinition:
            msg = (
                "BothVariableForms requires a declaration_style that "
                "supports redefinition; "
                f"{language.declaration_style.name!r} does not."
            )
            raise ValueError(msg)
        return _literalize_both_forms(
            source=source,
            input_format=input_format,
            language=language,
            pre_indent_level=pre_indent_level,
            include_delimiters=include_delimiters,
            variable_form=variable_form,
            ref_case=ref_case,
            ref_key=ref_key,
            collection_layout=collection_layout,
        )

    pre_form = _literalize_pre_form(
        source=source,
        input_format=input_format,
        language=language,
        pre_indent_level=pre_indent_level,
        include_delimiters=include_delimiters,
        ref_case=ref_case,
        ref_key=ref_key,
        collection_layout=collection_layout,
    )
    return _literalize_apply_form(
        pre_form=pre_form,
        language=language,
        variable_form=variable_form,
        wrap_in_file=wrap_in_file,
    )


@beartype
def _extract_call_arg_ref_name(*, value: Value, ref_key: str) -> str | None:
    """Return the identifier name for a ``{ref_key: "name"}`` marker.

    Returns ``None`` when *value* is not a variable-reference marker.
    In :func:`literalize_call` such markers render as the bare
    identifier instead of being formatted as a literal value.
    """
    if not isinstance(value, dict) or len(value) != 1:
        return None
    ref_value = value.get(ref_key)
    if not isinstance(ref_value, str):
        return None
    return ref_value


@beartype
def _strip_refs_from_value(*, value: Value, ref_key: str) -> Value:
    """Return *value* with ``{"$ref": "name"}`` markers removed at any
    depth.

    Used to produce ref-free data for preamble inference, validation,
    and wrap-id computation so that the ``{str: str}`` shape of a ref
    marker never influences type-dependent logic.
    """
    if isinstance(value, list):
        return [
            _strip_refs_from_value(value=item, ref_key=ref_key)
            for item in value
            if _extract_call_arg_ref_name(value=item, ref_key=ref_key) is None
        ]
    if (
        isinstance(value, dict)
        and _extract_call_arg_ref_name(value=value, ref_key=ref_key) is None
    ):
        return {
            k: _strip_refs_from_value(value=v, ref_key=ref_key)
            for k, v in value.items()
            if _extract_call_arg_ref_name(value=v, ref_key=ref_key) is None
        }
    return value


@beartype
def _compute_call_arg_ref_single_use_names(
    *,
    elements: list[Value],
    ref_key: str,
) -> frozenset[str]:
    """Return ref identifiers that appear exactly once across the calls.

    Names are returned in the original (pre-``ref_case``) form supplied
    by the caller, so they can be compared against the user-supplied
    ``consumable_refs`` set on
    :func:`~literalizer.literalize_call` without further conversion.

    Refs not in this set are unsafe to consume: they appear in more than
    one per-element call (or more than once inside a single call's
    argument list), so a language that moves consumable refs (notably
    C++ ``std::move``) would render a use-after-move on the second
    occurrence.
    """
    counts: dict[str, int] = {}
    for element in elements:
        arg_values = element if isinstance(element, list) else [element]
        for value in arg_values:
            ref_name = _extract_call_arg_ref_name(value=value, ref_key=ref_key)
            if ref_name is None:
                continue
            counts[ref_name] = counts.get(ref_name, 0) + 1
    return frozenset(name for name, count in counts.items() if count == 1)


@beartype
def _strip_call_arg_refs_for_preamble(
    *,
    data: Value,
    per_element: bool,
    ref_key: str,
) -> Value:
    """Return *data* with call-argument ref markers removed.

    Ref markers represent a variable declared elsewhere, not real data,
    so they would pollute data-driven preamble inference (e.g. dragging
    in ``Data.Map`` imports for Haskell just because the marker happens
    to be a ``{str: str}`` dict).  Drop them before computing the
    preamble while leaving :func:`_format_call_args` to render them.

    When *per_element* is ``True``, *data* is a list of argument lists
    and refs are stripped from each inner list.  Otherwise a
    top-level ref becomes an empty list, standing in for "no data".
    Refs nested inside list or dict argument values are also stripped
    recursively.
    """
    if per_element:
        if not isinstance(data, list):
            return data
        result: list[Value] = []
        for element in data:
            if isinstance(element, list):
                result.append(
                    [
                        _strip_refs_from_value(value=v, ref_key=ref_key)
                        for v in element
                        if _extract_call_arg_ref_name(value=v, ref_key=ref_key)
                        is None
                    ]
                )
            elif (
                _extract_call_arg_ref_name(value=element, ref_key=ref_key)
                is None
            ):
                result.append(
                    _strip_refs_from_value(value=element, ref_key=ref_key)
                )
        return result
    if _extract_call_arg_ref_name(value=data, ref_key=ref_key) is not None:
        return []
    return _strip_refs_from_value(value=data, ref_key=ref_key)


@beartype
def _format_single_call_arg(
    *,
    value: Value,
    language: Language,
    wrap_ids: frozenset[int],
    wrap_arg: Callable[[Value, str], str],
    dict_open_override: str | None,
    ref_case: IdentifierCase | None,
    consumable_ref_names: frozenset[str],
    single_use_ref_names: frozenset[str],
    ref_key: str,
    collection_layout: CollectionLayout,
) -> str:
    """Format one argument value for a function call.

    A ref marker renders as the bare identifier; the ``format_call_arg``
    hook is skipped for refs because the referenced variable already has
    the call's parameter type.  When *ref_case* is not ``None``, the ref
    name is converted to that case before being emitted.

    *consumable_ref_names* is the caller's declaration of which refs
    this call owns and may move from.  *single_use_ref_names* is the
    set of refs that appear exactly once across this call's argument
    lists.  Both sets use the original (pre-``ref_case``) name.  A ref
    is rendered via the language's
    ``format_call_arg_ref_identifier_consumable`` hook only when it is
    in both sets; otherwise it goes through the regular
    ``format_call_arg_ref_identifier`` hook.  This ensures that a ref
    used in more than one call (or more than once in a single call's
    arguments) is never consumed, even when the caller listed it as
    consumable.
    """
    raw_ref_name = _extract_call_arg_ref_name(value=value, ref_key=ref_key)
    if raw_ref_name is not None:
        ref_name = (
            ref_case.convert(name=raw_ref_name)
            if ref_case is not None
            else raw_ref_name
        )
        is_consumable = (
            raw_ref_name in consumable_ref_names
            and raw_ref_name in single_use_ref_names
        )
        if is_consumable:
            return language.format_call_arg_ref_identifier_consumable(ref_name)
        return language.format_call_arg_ref_identifier(ref_name)
    return wrap_arg(
        value,
        _format_value(
            value=value,
            spec=language,
            dict_open_override=dict_open_override,
            wrap_ids=wrap_ids,
            sequence_open_override=None,
            ref_case=ref_case,
            expand_refs=True,
            ref_key=ref_key,
            collection_layout=collection_layout,
            multiline_prefix="",
        ),
    )


@beartype
def _format_prefix_call_args(
    *,
    formatted: list[str],
    params: Sequence[str],
    sep: str,
    kw_prefix: str,
) -> str:
    """Format values for :class:`PrefixCallStyle`.

    When *kw_prefix* is empty the call is positional (values only).
    Otherwise each value is emitted as ``{kw_prefix}{name}{sep}{value}``.
    """
    if not kw_prefix:
        return sep.join(formatted)
    if len(params) != len(formatted):
        raise ParameterCountMismatchError(
            expected=len(params), got=len(formatted)
        )
    return sep.join(
        f"{kw_prefix}{name}{sep}{val}"
        for name, val in zip(params, formatted, strict=True)
    )


@beartype
def _format_call_args(
    *,
    values: Sequence[Value],
    params: Sequence[str],
    language: Language,
    wrap_ids: frozenset[int],
    style: CallStyle,
    dict_open_overrides: Sequence[str | None],
    ref_case: IdentifierCase | None,
    consumable_ref_names: frozenset[str],
    single_use_ref_names: frozenset[str],
    ref_key: str,
    collection_layout: CollectionLayout,
) -> str:
    """Format argument values for a single function call.

    For infix styles returns the parenthesized argument list
    ``(arg1, arg2)``.  For :class:`PostfixCallStyle` returns the
    unwrapped, space-separated argument list so the caller can
    assemble ``args target`` directly.

    A value shaped like ``{"$ref": "name"}`` renders as the bare
    identifier ``name`` instead of being formatted as a literal, so
    callers can refer to a variable declared elsewhere (e.g. via
    :class:`NewVariable`).

    *dict_open_overrides* supplies a per-positional dict opener so that
    dict arguments at the same slot across sibling calls share a
    widened type.  ``None`` at a given position means "no override".

    *ref_case*, when not ``None``, converts each ``{"$ref": "name"}``
    identifier to that :class:`IdentifierCase` before emitting it.
    """
    wrap_arg = language.format_call_arg
    formatted = [
        _format_single_call_arg(
            value=arg_value,
            language=language,
            wrap_ids=wrap_ids,
            wrap_arg=wrap_arg,
            dict_open_override=dict_open_overrides[slot_index],
            ref_case=ref_case,
            consumable_ref_names=consumable_ref_names,
            single_use_ref_names=single_use_ref_names,
            ref_key=ref_key,
            collection_layout=collection_layout,
        )
        for slot_index, arg_value in enumerate(iterable=values)
    ]

    if not formatted and not language.allows_empty_call_parens:
        return ""

    match style:
        case PositionalCallStyle():
            return f"({', '.join(formatted)})"
        case KeywordCallStyle(separator=kw_sep):
            if len(params) != len(formatted):
                raise ParameterCountMismatchError(
                    expected=len(params), got=len(formatted)
                )
            inner = ", ".join(
                f"{name}{kw_sep}{val}"
                for name, val in zip(params, formatted, strict=True)
            )
            return f"({inner})"
        case ObjectCallStyle(separator=kw_sep):
            if len(params) != len(formatted):
                raise ParameterCountMismatchError(
                    expected=len(params), got=len(formatted)
                )
            named = ", ".join(
                f"{name}{kw_sep}{val}"
                for name, val in zip(params, formatted, strict=True)
            )
            return f"({{ {named} }})"
        case (
            PostfixCallStyle(arg_separator=sep)
            | CommandCallStyle(arg_separator=sep)
        ):
            return sep.join(formatted)
        case PrefixCallStyle(arg_separator=sep, keyword_prefix=kw_prefix):
            return _format_prefix_call_args(
                formatted=formatted,
                params=params,
                sep=sep,
                kw_prefix=kw_prefix,
            )
        case _ as unreachable:
            assert_never(unreachable)


@beartype
def _extract_call_transform_wrapper(
    *,
    call_transform: Callable[[str], str],
) -> str:
    """Extract the wrapper word from a Python-style *call_transform*.

    Used by call styles that build the call expression by adding the
    wrapper before or after the inner call rather than substituting
    it into the transform's parenthesized template.  Probes
    *call_transform* with a sentinel and returns the prefix preceding
    the sentinel, stripped of the trailing ``(`` and any whitespace
    (e.g. ``lambda c: f"emit({c})"`` yields ``"emit"``).
    """
    sentinel = "\x00"
    wrapped = call_transform(sentinel)
    idx = wrapped.index(sentinel)
    return wrapped[:idx].rstrip("(").strip()


@beartype
def _assemble_postfix_call(
    *,
    target_function: str,
    args_str: str,
    call_transform: Callable[[str], str] | None,
) -> str:
    """Build ``args target`` for :class:`PostfixCallStyle`.

    With a wrapper transform the wrapper word is appended postfix,
    so the result is e.g. ``args target emit``.
    """
    call_expr = (
        f"{args_str} {target_function}" if args_str else target_function
    )
    if call_transform is not None:
        wrapper = _extract_call_transform_wrapper(
            call_transform=call_transform,
        )
        if wrapper:
            call_expr = f"{call_expr} {wrapper}"
    return call_expr


@beartype
def _assemble_prefix_call(
    *,
    target_function: str,
    args_str: str,
    call_transform: Callable[[str], str] | None,
    arg_separator: str,
) -> str:
    """Build ``(target args)`` for :class:`PrefixCallStyle`.

    With a wrapper transform the result is e.g.
    ``(emit (target args))``.
    """
    inside = (
        f"{target_function}{arg_separator}{args_str}"
        if args_str
        else target_function
    )
    call_expr = f"({inside})"
    if call_transform is not None:
        wrapper = _extract_call_transform_wrapper(
            call_transform=call_transform,
        )
        if wrapper:
            call_expr = f"({wrapper}{arg_separator}{call_expr})"
    return call_expr


@beartype
def _assemble_command_call(
    *,
    target_function: str,
    args_str: str,
    call_transform: Callable[[str], str] | None,
    arg_separator: str,
    wrapped_call_template: str,
) -> str:
    """Build ``target arg1 arg2`` for :class:`CommandCallStyle`.

    With a wrapper transform the inner call is formatted using
    *wrapped_call_template* (e.g. ``emit "$(target arg1 arg2)"`` for
    Bash or ``emit [target arg1 arg2]`` for Tcl).
    """
    call_expr = (
        f"{target_function}{arg_separator}{args_str}"
        if args_str
        else target_function
    )
    if call_transform is not None:
        wrapper = _extract_call_transform_wrapper(
            call_transform=call_transform,
        )
        if wrapper:
            call_expr = wrapped_call_template.format(
                wrapper=wrapper,
                inner=call_expr,
            )
    return call_expr


@beartype
def _assemble_call(
    *,
    target_function: str,
    args_str: str,
    call_transform: Callable[[str], str] | None,
    statement_terminator: str,
    style: CallStyle,
) -> str:
    """Build one complete call statement.

    Dispatches to a per-style helper and appends the language's
    statement terminator.
    """
    match style:
        case PostfixCallStyle():
            call_expr = _assemble_postfix_call(
                target_function=target_function,
                args_str=args_str,
                call_transform=call_transform,
            )
        case PositionalCallStyle() | KeywordCallStyle() | ObjectCallStyle():
            call_expr = f"{target_function}{args_str}"
            if call_transform is not None:
                call_expr = call_transform(call_expr)
        case PrefixCallStyle(arg_separator=sep):
            call_expr = _assemble_prefix_call(
                target_function=target_function,
                args_str=args_str,
                call_transform=call_transform,
                arg_separator=sep,
            )
        case CommandCallStyle(
            arg_separator=sep,
            wrapped_call_template=wrapped_call_template,
        ):
            call_expr = _assemble_command_call(
                target_function=target_function,
                args_str=args_str,
                call_transform=call_transform,
                arg_separator=sep,
                wrapped_call_template=wrapped_call_template,
            )
        case _ as unreachable:
            assert_never(unreachable)
    return f"{call_expr}{statement_terminator}"


@beartype
def _render_call_per_element(
    *,
    data: list[Value],
    language: Language,
    style: CallStyle,
    target_function: str,
    parameter_names: Sequence[str],
    call_transform: Callable[[str], str] | None,
    ref_case: IdentifierCase | None,
    consumable_ref_names: frozenset[str],
    ref_key: str,
    collection_comments: CollectionComments | None = None,
    collection_layout: CollectionLayout = CollectionLayout.COMPACT,
) -> str:
    """Render one call per top-level list element.

    Variable-reference markers (``{"$ref": "name"}``) are syntactic
    pointers rather than real data, so they are skipped during
    data-shape validation and wrap-id computation while still
    appearing as identifiers in the rendered call.
    :func:`_compute_call_slot_overrides` and
    :func:`_compute_call_per_element_wrap_ids` similarly filter them
    out so the marker's ``{str: str}`` shape does not influence
    per-slot widening.
    """
    slot_overrides = _compute_call_slot_overrides(
        elements=data,
        spec=language,
        ref_key=ref_key,
    )
    slot_wrap_ids = _compute_call_per_element_wrap_ids(
        elements=data,
        spec=language,
        ref_key=ref_key,
    )
    single_use_ref_names = _compute_call_arg_ref_single_use_names(
        elements=data,
        ref_key=ref_key,
    )
    rendered_elements: list[str] = []
    for element in data:
        arg_values = element if isinstance(element, list) else [element]
        non_ref_args = [
            v
            for v in arg_values
            if _extract_call_arg_ref_name(value=v, ref_key=ref_key) is None
        ]
        for value in non_ref_args:
            stripped_value = _strip_refs_from_value(
                value=value, ref_key=ref_key
            )
            check_data(data=stripped_value, spec=language)
            language.validate_call_arg(stripped_value)
        call_wrap_ids = (
            _compute_wrap_ids(data=non_ref_args, spec=language) | slot_wrap_ids
        )
        args_str = _format_call_args(
            values=arg_values,
            params=parameter_names,
            language=language,
            wrap_ids=call_wrap_ids,
            style=style,
            dict_open_overrides=slot_overrides,
            ref_case=ref_case,
            consumable_ref_names=consumable_ref_names,
            single_use_ref_names=single_use_ref_names,
            ref_key=ref_key,
            collection_layout=collection_layout,
        )
        rendered_elements.append(
            language.format_call_statement(
                _assemble_call(
                    target_function=target_function,
                    args_str=args_str,
                    call_transform=call_transform,
                    statement_terminator=language.statement_terminator,
                    style=style,
                )
            )
        )
    if collection_comments is not None:
        comment_cfg = language.comment_config
        return apply_collection_comments_to_elements(
            rendered_elements=rendered_elements,
            collection_comments=collection_comments,
            comment_prefix=comment_cfg.prefix,
            comment_suffix=comment_cfg.suffix,
        )
    return "\n".join(rendered_elements)


@beartype
def _render_call_whole(
    *,
    data: Value,
    language: Language,
    style: CallStyle,
    target_function: str,
    parameter_names: Sequence[str],
    call_transform: Callable[[str], str] | None,
    ref_case: IdentifierCase | None,
    consumable_ref_names: frozenset[str],
    ref_key: str,
    collection_layout: CollectionLayout,
) -> str:
    """Render a single call from the whole parsed value.

    A single top-level ref marker renders as just the identifier; in
    that case shape validation and wrap-id computation are skipped.
    """
    if _extract_call_arg_ref_name(value=data, ref_key=ref_key) is None:
        stripped_data = _strip_refs_from_value(value=data, ref_key=ref_key)
        check_data(data=stripped_data, spec=language)
        language.validate_call_arg(stripped_data)
        call_wrap_ids = _compute_wrap_ids(data=[data], spec=language)
    else:
        call_wrap_ids = frozenset[int]()
    args_str = _format_call_args(
        values=[data],
        params=parameter_names,
        language=language,
        wrap_ids=call_wrap_ids,
        style=style,
        dict_open_overrides=[None],
        ref_case=ref_case,
        consumable_ref_names=consumable_ref_names,
        single_use_ref_names=_compute_call_arg_ref_single_use_names(
            elements=[[data]],
            ref_key=ref_key,
        ),
        ref_key=ref_key,
        collection_layout=collection_layout,
    )
    return language.format_call_statement(
        _assemble_call(
            target_function=target_function,
            args_str=args_str,
            call_transform=call_transform,
            statement_terminator=language.statement_terminator,
            style=style,
        )
    )


@beartype
def literalize_call(
    *,
    source: str,
    input_format: InputFormat,
    language: Language,
    target_function: str,
    parameter_names: Sequence[str],
    call_transform: Callable[[str], str] | None = None,
    per_element: bool = True,
    wrap_in_file: bool = False,
    ref_case: IdentifierCase | None = None,
    consumable_refs: frozenset[str] = frozenset(),
    ref_key: str = "$ref",
    collection_layout: CollectionLayout = CollectionLayout.COMPACT,
) -> LiteralizeResult:
    r"""Convert data to function call expressions in the target language.

    Each top-level list element (when *per_element* is ``True``) becomes
    a separate function call with arguments formatted according to the
    language's :attr:`~Language.call_style_config`.

    Args:
        source: The input string to convert.
        input_format: The serialization format of *source*.
        language: A :class:`Language` instance describing how to format
            literals.
        target_function: The function expression to call
            (e.g. ``"throttler.should_send_notification"``).
        parameter_names: Parameter names, positionally mapped to each
            element in each row.  For :class:`PositionalCallStyle`
            languages these are unused in the output but still
            determine how many values to expect per row.
        call_transform: Optional callable transforming each call expression.
            Receives the bare call string and returns the transformed
            version (e.g. ``lambda c: f"print({c})"``).
        per_element: If ``True`` (default), each top-level list element
            becomes a separate call.  If ``False``, the whole
            literalized value is passed as a single argument.
        wrap_in_file: If ``True``, assemble :attr:`code` as a
            complete, self-contained source file using the language's
            ``wrap_in_file`` method and prepend :attr:`preamble`.  A
            no-op stub for *target_function* is also injected so the
            generated file does not reference an undefined name; when
            a *call_transform* is supplied the wrapper name it
            introduces is not stubbed — callers that transform calls
            are responsible for providing that definition themselves.
            When set, :attr:`preamble` and :attr:`body_preamble`
            on the result are empty tuples (their content has been
            folded into :attr:`code`).
        ref_case: Optional :class:`IdentifierCase` controlling how ref
            identifiers are cased in the rendered output.  When
            ``None`` (default) ref names are emitted verbatim.  When
            set, each ref identifier is normalized to ``snake_case``
            and then converted to the requested case via ``pyhumps``,
            so the same source can drive idiomatic identifiers across
            multiple languages.  When *language*'s ``identifier_cases``
            does not expose the requested case,
            :class:`~literalizer.exceptions.UnsupportedIdentifierCaseError`
            is raised.
        consumable_refs: Names of ref identifiers this call owns and
            may move from.  Refs in this set may be rendered with a
            consuming form (e.g. C++ ``std::move``) when they appear in
            exactly one call argument; refs used by more than one call
            -- or omitted from this set -- are emitted as the bare
            identifier so subsequent uses of the variable remain valid.
            Names should match the identifiers used in *source* before
            any *ref_case* conversion.  Defaults to an empty set (no
            refs are consumed).
        ref_key: The dict key used to identify variable-reference
            markers in the input data.  A single-key dict whose key
            equals *ref_key* and whose value is a string is treated as
            a ref marker.  Defaults to ``"$ref"``.
        collection_layout: Controls layout for collections nested
            inside call arguments.  ``CollectionLayout.COMPACT``
            preserves the existing one-line nested rendering, while
            ``CollectionLayout.MULTILINE`` expands non-empty nested
            collections with one element per line.

    .. note::

        When composing the output of this function with
        :func:`literalize` — for example, declaring a variable with
        :func:`literalize` and then referencing it via a ref marker in
        the call — the two halves each
        compute :attr:`~LiteralizeResult.preamble` and
        :attr:`~LiteralizeResult.body_preamble` independently from the
        data they see.  Concatenating the results into a single file
        can produce duplicate import lines or duplicate type
        declarations, which strict compilers (Haskell, D, …) reject
        and a linter (``ruff``, ``pylint``, …) flags.  Remove the
        duplicate preamble entries (preserving first-seen order) before
        emitting the file.  The "Composing declarations and calls"
        section of :doc:`/function-call-use-case` shows a worked example.
    """
    parsed = parse_input(source=source, input_format=input_format)
    data = parsed.data
    match language.call_style_config:
        case CallSupport.NOT_IN_LANGUAGE:
            raise CallsNotSupportedByLanguageError(
                language_name=type(language).__name__,
            )
        case CallSupport.NOT_IMPLEMENTED_BY_TOOL:
            raise CallsNotSupportedByToolError(
                language_name=type(language).__name__,
            )
        case _ as style:
            pass

    target_function_parts = tuple(target_function.split(sep="."))
    if len(target_function_parts) > 1 and not language.supports_dotted_calls:
        raise DottedCallsNotSupportedError(
            language_name=type(language).__name__,
            target_function=target_function,
        )
    if ref_case is not None and ref_case not in language.identifier_cases:
        raise UnsupportedIdentifierCaseError(
            language_name=type(language).__name__,
            case_name=ref_case.name,
        )
    target_function = language.format_call_target(target_function_parts)

    data_for_preamble = _strip_call_arg_refs_for_preamble(
        data=data,
        per_element=per_element,
        ref_key=ref_key,
    )

    if per_element:
        if not isinstance(data, list):
            msg = (
                "per_element=True requires a top-level list, "
                f"got {type(data).__name__}"
            )
            raise PerElementNotListError(msg)
        collection_comments: CollectionComments | None = None
        if (
            input_format is InputFormat.YAML
            and parsed.yaml_needs_comment_resolve
            and isinstance(parsed.raw_data, CommentedSeq)
        ):
            collection_comments = extract_yaml_comments(
                ruamel_data=parsed.raw_data,
            )
        result = _render_call_per_element(
            data=data,
            language=language,
            style=style,
            target_function=target_function,
            parameter_names=parameter_names,
            call_transform=call_transform,
            ref_case=ref_case,
            consumable_ref_names=consumable_refs,
            ref_key=ref_key,
            collection_comments=collection_comments,
            collection_layout=collection_layout,
        )
    else:
        result = _render_call_whole(
            data=data,
            language=language,
            style=style,
            target_function=target_function,
            parameter_names=parameter_names,
            call_transform=call_transform,
            ref_case=ref_case,
            consumable_ref_names=consumable_refs,
            ref_key=ref_key,
            collection_layout=collection_layout,
        )
    computed = compute_preamble(
        data=data_for_preamble,
        language=language,
        has_variable_declaration=False,
    )
    preamble = deduplicate_preamble_entries(
        entries=(
            tuple(language.static_preamble)
            + computed.header
            + language.call_data_dependent_preamble(data_for_preamble)
        )
    )

    if wrap_in_file:
        # Emit a no-op stub for ``target_function`` so the wrapped file
        # compiles on its own.  ``StubReturn.VALUE`` is used whenever a
        # ``call_transform`` consumes the call's return value; otherwise
        # the call result is discarded and a void stub suffices.
        stub_return = (
            StubReturn.VALUE if call_transform is not None else StubReturn.VOID
        )
        body_stubs = language.format_call_stub(
            target_function_parts, parameter_names, stub_return
        )
        preamble_stubs = language.format_call_preamble_stub(
            target_function_parts, parameter_names, stub_return
        )
        wrapped = language.wrap_in_file(
            content=result,
            variable_name="",
            body_preamble=body_stubs + computed.body,
        )
        # Stubs follow the language's static preamble (e.g. Go's
        # ``package main`` must come first).
        full_preamble = preamble + preamble_stubs
        if full_preamble:
            wrapped = "\n".join(full_preamble) + "\n" + wrapped
        return LiteralizeResult(
            declaration_code=wrapped,
            preamble=(),
            body_preamble=(),
            types_present=computed.types_present,
            source_data=data_for_preamble,
        )

    return LiteralizeResult(
        declaration_code=result,
        preamble=preamble,
        body_preamble=computed.body,
        types_present=computed.types_present,
        source_data=data_for_preamble,
    )
