"""Core conversion logic: formatting values and entry points."""

import dataclasses
import datetime
import enum
from collections.abc import Callable, Iterator, Mapping, Sequence
from typing import Final, assert_never

from beartype import BeartypeConf, beartype
from ruamel.yaml.comments import CommentedMap, CommentedSeq, CommentedSet
from ruamel.yaml.compat import ordereddict
from typing_extensions import TypeIs

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
    WideInt,
    infer_element_type,
    record_shape_for_dict,
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
from literalizer._parsing import (
    InputFormat,
    ParsedInput,
    ParsedToml,
    ParsedYaml,
    parse_input,
)
from literalizer._preamble import (
    compute_preamble,
    deduplicate_preamble_entries,
)
from literalizer._types import Scalar, Value, ValueInput
from literalizer.exceptions import (
    CallsNotSupportedByLanguageError,
    CallsNotSupportedByToolError,
    DottedCallTargetNotSupportedError,
    ParameterCountMismatchError,
    PerElementNotListError,
    UnrepresentableInputError,
    UnsupportedCallShapeError,
    UnsupportedIdentifierCaseError,
    VariableNameNotSupportedError,
    WrapInFileWithoutVariableNotSupportedError,
    ZipValuesLengthMismatchError,
    ZipValuesWithoutCallTransformError,
)

_DISABLED_REF_KEY = ""


@dataclasses.dataclass(frozen=True)
class CallContext:
    """Per-row context passed to a :func:`literalize_call`
    ``call_transform``.

    A ``call_transform`` is invoked once per generated call as
    ``call_transform(context)`` and returns the transformed call
    string.  The context carries the call's positional identity so a
    transform can pair it with data from a parallel sequence (see
    :func:`literalize_call`'s ``zip_values``).
    """

    call: str
    """The rendered language-native call expression
    (e.g. ``catalog.lookup("Dune", 1965)``).
    """

    index: int
    """Zero-based position of this call among the generated calls."""

    row: Sequence[Value]
    """The input values for this row, in source order.  For
    ``per_element=True`` this is the i-th top-level element's argument
    values; for ``per_element=False`` it is the whole parsed value
    wrapped in a single-element sequence.
    """

    zipped: str | None
    """The ``zip_values`` entry paired with this call, rendered as a
    language-native literal, or ``None`` when no ``zip_values`` were
    supplied.
    """


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

    contains_standalone_comments: bool = False
    """Whether the rendered source carried standalone comments (lines
    whose only content is a comment, distinct from inline trailing
    comments).  Set when ``literalize_call`` parses YAML input that
    contains top-level before-element or trailing comments.  Callers
    that wrap the result via :meth:`Language.wrap_calls_with_declarations`
    can consult this together with
    :attr:`Language.supports_standalone_comments_in_wrapped_calls`
    to decide whether wrapping is safe.
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
def _format_scalar(
    *,
    value: Scalar,
    spec: Language,
    int_formatter: Callable[[int], str] | None = None,
) -> str:
    """Format a scalar JSON value as a native language literal.

    *int_formatter* overrides ``spec.format_integer`` when given; the
    collection formatter passes a widened formatter (e.g. one that
    always appends an ``L`` suffix) when the surrounding collection's
    inferred element type required widening for some other element.
    """
    match value:
        case None:
            result = spec.null_literal
        case bool():
            result = spec.true_literal if value else spec.false_literal
        case int():
            format_int = (
                int_formatter
                if int_formatter is not None
                else spec.format_integer
            )
            result = format_int(value)
        case float():
            result = spec.format_float(value)
        case str():
            result = spec.format_string(value)
        case bytes():
            result = spec.format_bytes(value)
        case datetime.datetime():
            result = spec.format_datetime(value)
        case datetime.time():
            result = spec.format_time(value)
        case _:
            result = spec.format_date(value)
    return result


@beartype
def _widened_int_formatter(
    *,
    items: list[Value],
    spec: Language,
) -> Callable[[int], str] | None:
    """Return a widened integer formatter for *items* or ``None``.

    Returns ``None`` when *items* do not require widening (no
    out-of-i32 integer present) or when the language does not expose a
    ``format_integer_widened`` override.
    """
    if infer_element_type(items=items) is not WideInt:
        return None
    return getattr(spec, "format_integer_widened", None)


_SCALAR_TYPES: Final = (
    str,
    int,
    float,
    bool,
    type(None),
    datetime.date,
    datetime.datetime,
    datetime.time,
    bytes,
)


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

    Routes scalar children through
    :attr:`~literalizer._language.HeterogeneousBehavior.wrap_scalar`
    and non-scalar children (ref markers, containers) through
    :attr:`~literalizer._language.HeterogeneousBehavior.wrap_non_scalar`.
    """
    behavior = spec.heterogeneous_behavior
    if isinstance(raw_value, _SCALAR_TYPES):
        wrap_scalar = behavior.wrap_scalar
        if wrap_scalar is None or parent_id not in wrap_ids:
            return formatted_value
        return wrap_scalar(raw_value, formatted_value)
    wrap_non_scalar = behavior.wrap_non_scalar
    if wrap_non_scalar is None or parent_id not in wrap_ids:
        return formatted_value
    return wrap_non_scalar(raw_value, formatted_value)


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
    int_formatter = _widened_int_formatter(items=items_as_values, spec=spec)
    formatted = [
        _format_scalar(value=v, spec=spec, int_formatter=int_formatter)
        for v in sorted_items
    ]
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
def _guard_dict_keys_supported(
    *,
    value: Mapping[Scalar, Value],
    spec: Language,
) -> None:
    """Reject non-string dict keys for languages that cannot represent
    them.
    """
    if spec.supports_non_string_dict_keys:
        return
    for key in value:
        if not isinstance(key, str):
            msg = (
                f"{type(spec).__name__} cannot represent dict key of "
                f"type {type(key).__name__}"
            )
            raise UnrepresentableInputError(msg)


@beartype
def _format_ordered_map_value(
    *,
    value: ordereddict,
    spec: Language,
    wrap_ids: frozenset[int],
    ref_case: IdentifierCase | None,
    ref_values: Mapping[str, Value] | None,
    expand_refs: bool,
    ref_key: str,
    collection_layout: CollectionLayout,
    multiline_prefix: str,
) -> str:
    """Format an ordered map as a native language literal."""
    _guard_dict_keys_supported(value=value, spec=spec)
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
                ref_values=ref_values,
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
                    ref_values=ref_values,
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
def _maybe_format_record_literal(
    *,
    value: dict[Scalar, Value],
    spec: Language,
    wrap_ids: frozenset[int],
    ref_case: IdentifierCase | None,
    ref_values: Mapping[str, Value] | None,
    expand_refs: bool,
    ref_key: str,
    collection_layout: CollectionLayout,
    multiline_prefix: str,
) -> str | None:
    """Render *value* as a record-struct literal if eligible.

    Returns ``None`` when the language's heterogeneous behavior is not
    RECORD-enabled or when *value* is not record-shaped (empty,
    non-string keys, or a ruamel ordered map).
    """
    behavior = spec.heterogeneous_behavior
    render_record_literal = behavior.render_record_literal
    if render_record_literal is None:
        return None
    if record_shape_for_dict(value=value) is None:  # pragma: no cover
        return None
    is_multiline = collection_layout is CollectionLayout.MULTILINE
    body_prefix = multiline_prefix + spec.indent if is_multiline else ""
    field_multiline_prefix = body_prefix if is_multiline else multiline_prefix
    # Iterate over *value*'s own keys; missing-from-this-dict keys are
    # filled in by the strategy's render callable using whatever
    # unified shape it has cached.
    str_keys: list[str] = []
    for key in value:
        if not isinstance(key, str):  # pragma: no cover
            return None
        str_keys.append(key)
    formatted_fields: dict[str, str] = {
        key: _format_value(
            value=value[key],
            spec=spec,
            dict_open_override=None,
            wrap_ids=wrap_ids,
            sequence_open_override=None,
            ref_case=ref_case,
            ref_values=ref_values,
            expand_refs=expand_refs,
            ref_key=ref_key,
            collection_layout=collection_layout,
            multiline_prefix=field_multiline_prefix,
        )
        for key in str_keys
    }
    rendered = render_record_literal(value, formatted_fields)
    if not is_multiline:
        return rendered
    return _expand_record_literal_multiline(
        rendered=rendered,
        body_prefix=body_prefix,
        close_prefix=multiline_prefix,
    )


@beartype
def _expand_record_literal_multiline(
    *,
    rendered: str,
    body_prefix: str,
    close_prefix: str,
) -> str:
    """Expand a single-line record literal into multiline form.

    Splits ``Name { f1: v1, f2: v2 }`` (brace-delimited, e.g. Rust and
    Go) or ``Name(f1 = v1, f2 = v2)`` (paren-delimited, e.g. Kotlin,
    Scala, Java) into one entry per line indented under *body_prefix*
    with the closing delimiter on its own line under *close_prefix*.
    The opening delimiter is whichever of ``{`` or ``(`` appears first;
    its matching closer is the literal's final character.  The literal
    always has at least one field because ``render_record_literal`` is
    only called for record-eligible (non-empty) dicts.
    """
    open_idx = min(
        index for index, char in enumerate(iterable=rendered) if char in "{("
    )
    closer = {"{": "}", "(": ")"}[rendered[open_idx]]
    head = rendered[: open_idx + 1]
    body = rendered[open_idx + 1 : -1].strip()
    entries = _split_record_entries(body=body)
    indented = [f"{body_prefix}{entry.strip()}," for entry in entries]
    return f"{head}\n" + "\n".join(indented) + f"\n{close_prefix}{closer}"


@dataclasses.dataclass(frozen=True)
class _StringScanStep:
    r"""One step of scanning inside a string literal.

    *in_string* is the currently-open quote character (or ``None`` if
    the literal just closed).  *skip_next* is ``True`` when the next
    char must be skipped because it is the second half of a ``\X``
    escape sequence.
    """

    in_string: str | None
    skip_next: bool


@beartype
def _split_record_entries(*, body: str) -> list[str]:
    """Split a record-literal body on commas that are not inside
    brackets or quotes.

    *body* is the inner text of ``Name { ... }`` for a record with at
    least one field, so the loop always produces a non-empty trailing
    entry after the last comma (or the whole body when there are no
    top-level commas).
    """
    entries: list[str] = []
    last = 0
    for index in _depth_zero_comma_indices(body=body):
        entries.append(body[last:index])
        last = index + 1
    entries.append(body[last:].strip().rstrip(","))
    return [e for e in entries if e.strip()]


@beartype
def _depth_zero_comma_indices(*, body: str) -> Iterator[int]:
    r"""Yield indices of commas in *body* that are at bracket depth zero
    and outside any string literal.

    Treats ``\\`` inside a string literal as an escape so embedded
    escaped quotes do not prematurely close string tracking.
    """
    depth = 0
    in_string: str | None = None
    skip_next = False
    for index, char in enumerate(iterable=body):
        if skip_next:
            skip_next = False
        elif in_string is not None:
            step = _advance_string_state(char=char, quote=in_string)
            in_string = step.in_string
            skip_next = step.skip_next
        elif char in {'"', "'"}:
            in_string = char
        elif char in {"(", "[", "{"}:
            depth += 1
        elif char in {")", "]", "}"}:
            depth -= 1
        elif char == "," and depth == 0:
            yield index


@beartype
def _advance_string_state(
    *,
    char: str,
    quote: str,
) -> _StringScanStep:
    """Return the next ``(in_string, skip_next)`` state inside a string
    literal, given the current quote and next char.
    """
    if char == "\\":
        return _StringScanStep(in_string=quote, skip_next=True)
    if char == quote:
        return _StringScanStep(in_string=None, skip_next=False)
    return _StringScanStep(in_string=quote, skip_next=False)


@beartype
def _format_dict_value(
    *,
    value: dict[Scalar, Value],
    spec: Language,
    open_override: str | None,
    wrap_ids: frozenset[int],
    ref_case: IdentifierCase | None,
    ref_values: Mapping[str, Value] | None,
    expand_refs: bool,
    ref_key: str,
    collection_layout: CollectionLayout,
    multiline_prefix: str,
) -> str:
    """Format a dict as a native language literal."""
    _guard_dict_keys_supported(value=value, spec=spec)
    dict_cfg = spec.dict_format_config

    dict_items: dict[Scalar, Value] = {
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
                ref_values=ref_values,
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
                    ref_values=ref_values,
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
    elif not ref_key:
        opener = dict_cfg.dict_open(dict_items)
    else:
        open_items = dict_items
        if any(
            isinstance(v, dict)
            and _extract_call_arg_ref_name(value=v, ref_key=ref_key)
            is not None
            for v in dict_items.values()
        ):
            open_items = {
                k: v
                for k, v in dict_items.items()
                if not isinstance(v, dict)
                or _extract_call_arg_ref_name(value=v, ref_key=ref_key) is None
            }
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
    ref_values: Mapping[str, Value] | None,
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
            ref_values=ref_values,
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
        ref_values=ref_values,
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
    dicts: list[dict[Scalar, Value]] = [
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
    combined: dict[Scalar, Value] = {}
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
def _compute_call_slot_scalar_wrap_ids(
    *,
    elements: list[Value],
    spec: Language,
    ref_key: str,
) -> frozenset[int]:
    """Compute ids of top-level scalar call arguments to wrap.

    For each positional argument slot, gather the values across sibling
    calls and ask the language's
    :class:`~literalizer._language.HeterogeneousBehavior` whether any
    of those values need wrapping due to cross-call type divergence.
    The default behavior returns an empty set for every slot; the Mojo
    language under the ``VARIANT`` strategy returns the value ids of
    divergent top-level scalars so they render wrapped as ``Value(...)``.
    """
    slots = _gather_call_slot_values(elements=elements, ref_key=ref_key)
    return frozenset[int]().union(
        *(
            spec.heterogeneous_behavior.compute_call_slot_wrap_ids(slot_values)
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
    ref_values: Mapping[str, Value] | None,
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
        ref_values=ref_values,
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
    ref_values: Mapping[str, Value] | None,
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
            ref_values=ref_values,
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
                    ref_values=ref_values,
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
    elif not ref_key:
        opener = spec.sequence_open(value)
    else:
        open_value = [
            v
            for v in value
            if not isinstance(v, dict)
            or _extract_call_arg_ref_name(value=v, ref_key=ref_key) is None
        ]
        opener = spec.sequence_open(open_value or value)
    return f"{opener}{joined}{sequence_cfg.close}"


@beartype
def _format_value(  # pylint: disable=too-complex
    *,
    value: Value,
    spec: Language,
    dict_open_override: str | None,
    wrap_ids: frozenset[int],
    sequence_open_override: str | None,
    ref_case: IdentifierCase | None,
    ref_values: Mapping[str, Value] | None,
    expand_refs: bool,
    ref_key: str,
    collection_layout: CollectionLayout,
    multiline_prefix: str,
    int_formatter: Callable[[int], str] | None = None,
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

    ``{"$ref": "name"}`` markers anywhere in the value tree are rendered
    as bare identifiers.  ``literalize`` uses
    :attr:`~literalizer._language.Language.format_call_ref_identifier`;
    ``literalize_call`` sets *expand_refs* so nested argument refs use
    :attr:`~literalizer._language.Language.format_call_arg_ref_identifier`.
    When *ref_case* is set the identifier name is converted to that case
    first.
    """
    if ref_key and isinstance(value, dict):
        raw_ref_name = _extract_call_arg_ref_name(value=value, ref_key=ref_key)
        if raw_ref_name is not None:
            ref_name = (
                ref_case.convert(name=raw_ref_name)
                if ref_case is not None
                else raw_ref_name
            )
            ref_value = (
                ref_values.get(raw_ref_name)
                if ref_values is not None
                else None
            )
            return (
                spec.format_call_arg_ref_identifier(ref_name, ref_value)
                if expand_refs
                else spec.format_call_ref_identifier(ref_name, ref_value)
            )
    if isinstance(value, dict) and not isinstance(value, ordereddict):
        record_literal = _maybe_format_record_literal(
            value=value,
            spec=spec,
            wrap_ids=wrap_ids,
            ref_case=ref_case,
            ref_values=ref_values,
            expand_refs=expand_refs,
            ref_key=ref_key,
            collection_layout=collection_layout,
            multiline_prefix=multiline_prefix,
        )
        if record_literal is not None:
            return record_literal
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
            ref_values=ref_values,
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
                ref_values=ref_values,
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
                ref_values=ref_values,
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
        case list():
            result = _format_list_value(
                value=value,
                spec=spec,
                wrap_ids=wrap_ids,
                sequence_open_override=sequence_open_override,
                child_sequence_open_overrides=(),
                ref_case=ref_case,
                ref_values=ref_values,
                expand_refs=expand_refs,
                ref_key=ref_key,
                collection_layout=collection_layout,
                multiline_prefix=multiline_prefix,
            )
        case _:
            result = _format_scalar(
                value=value, spec=spec, int_formatter=int_formatter
            )
    return result


@beartype
def _wrap_body(
    *,
    body: str,
    is_ordered_map: bool,
    data: list[Value] | dict[Scalar, Value] | set[Scalar],
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
    data: dict[Scalar, Value] | set[Scalar] | list[Value],
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
    del expand_refs
    match data:
        case dict() if is_ordered_map:
            opener = spec.ordered_map_format_config.ordered_map_open(data)
        case dict() if dict_open_override is not None:
            opener = dict_open_override
        case dict() if not ref_key:
            opener = spec.dict_format_config.dict_open(data)
        case dict():
            dict_open_items = {
                k: v
                for k, v in data.items()
                if not isinstance(v, dict)
                or _extract_call_arg_ref_name(value=v, ref_key=ref_key) is None
            }
            opener = spec.dict_format_config.dict_open(dict_open_items or data)
        case set():
            sorted_set: list[Value] = sorted(
                data,
                key=lambda v: (type(v).__name__, repr(v)),
            )
            opener = spec.set_format_config.set_open(sorted_set)
        case _ if sequence_open_override is not None:
            opener = sequence_open_override
        case _ if not ref_key:
            opener = spec.sequence_open(data)
        case _:
            sequence_open_items = [
                v
                for v in data
                if not isinstance(v, dict)
                or _extract_call_arg_ref_name(value=v, ref_key=ref_key) is None
            ]
            opener = spec.sequence_open(sequence_open_items or data)
    return opener


@beartype
def _format_multiline_collection_value(
    *,
    value: dict[Scalar, Value] | set[Scalar] | list[Value],
    spec: Language,
    line_prefix: str,
    wrap_ids: frozenset[int],
    ref_case: IdentifierCase | None,
    ref_values: Mapping[str, Value] | None,
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
        ref_values=ref_values,
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
    data: dict[Scalar, Value] | set[Scalar] | list[Value],
    spec: Language,
    body_prefix: str,
    trailing_comma: bool,
    is_ordered_map: bool,
    wrap_ids: frozenset[int],
    ref_case: IdentifierCase | None,
    ref_values: Mapping[str, Value] | None,
    expand_refs: bool,
    ref_key: str,
    collection_layout: CollectionLayout,
) -> list[str]:
    """Format collection elements as indented lines."""
    lines: list[str] = []
    parent_id = id(data)
    match data:
        case dict() as dict_data:
            _guard_dict_keys_supported(value=dict_data, spec=spec)
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
                    ref_values=ref_values,
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
                        ref_values=ref_values,
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
            set_int_formatter = _widened_int_formatter(
                items=list(sorted_items),
                spec=spec,
            )
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
                            ref_values=ref_values,
                            expand_refs=expand_refs,
                            ref_key=ref_key,
                            collection_layout=collection_layout,
                            multiline_prefix=body_prefix,
                            int_formatter=set_int_formatter,
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
                            ref_values=ref_values,
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
def _literalize(  # noqa: PLR0911  # pylint: disable=too-many-return-statements
    *,
    data: Value,
    language: Language,
    line_prefix: str,
    include_delimiters: bool,
    ref_case: IdentifierCase | None,
    ref_values: Mapping[str, Value] | None,
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
        ref_case: When set, ref identifiers are converted to this case
            before rendering.
        ref_values: Optional mapping from ref identifier to the value
            declared elsewhere for that ref.  Forwarded to the
            language's ``format_call_ref_identifier`` /
            ``format_call_arg_ref_identifier`` hooks so type-sensitive
            languages can pick the right form.
        ref_key: The key used to identify ref markers in the input.
        collection_layout: Controls layout for collections nested
            inside other collections.
    """
    if ref_key and isinstance(data, dict):
        raw_ref_name = _extract_call_arg_ref_name(value=data, ref_key=ref_key)
        if raw_ref_name is not None:
            ref_name = (
                ref_case.convert(name=raw_ref_name)
                if ref_case is not None
                else raw_ref_name
            )
            ref_value = (
                ref_values.get(raw_ref_name)
                if ref_values is not None
                else None
            )
            identifier = language.format_call_ref_identifier(
                ref_name, ref_value
            )
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
        datetime.time,
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
            ref_values=ref_values,
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
        empty_value: ordereddict | dict[Scalar, Value] = (
            ordereddict() if is_ordered_map else {}
        )
        formatted = _format_value(
            value=empty_value,
            spec=language,
            dict_open_override=None,
            wrap_ids=wrap_ids,
            sequence_open_override=None,
            ref_case=ref_case,
            ref_values=ref_values,
            expand_refs=False,
            ref_key=ref_key,
            collection_layout=collection_layout,
            multiline_prefix=line_prefix,
        )
        return f"{line_prefix}{formatted}"

    if (
        include_delimiters
        and isinstance(data, dict)
        and not isinstance(data, ordereddict)
    ):
        record_literal = _maybe_format_record_literal(
            value=data,
            spec=language,
            wrap_ids=wrap_ids,
            ref_case=ref_case,
            ref_values=ref_values,
            expand_refs=False,
            ref_key=ref_key,
            collection_layout=CollectionLayout.MULTILINE,
            multiline_prefix=line_prefix,
        )
        if record_literal is not None:
            return f"{line_prefix}{record_literal}"

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
        ref_values=ref_values,
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
    is_call_binding: bool,
) -> str:
    """Optionally wrap *result* in a variable declaration or
    assignment.

    *result* arrives with *line_prefix* already prepended to every
    line.  When wrapping in a variable form the leading prefix on the
    first line is stripped so the value sits flush against the
    declaration's ``=``, then re-prepended once to the entire wrapped
    output.  This keeps every line uniformly indented instead of
    doubly-indenting continuation lines.

    When *is_call_binding* is ``True`` the right-hand side is a call
    expression, not a literal value.  Languages whose literal-binding
    declaration template injects a value-type-derived tag (Haskell's
    ``x :: Val`` annotation, Elm's ``x : Val``, etc.) can opt in to a
    call-specific declaration formatter via
    ``format_call_variable_declaration``; languages that do not define
    one fall back to ``format_variable_declaration`` unchanged.  The
    assignment template re-binds an existing variable and is bare in
    these languages already, so no call-specific override is needed.
    """
    if variable_form is None:
        return result

    if line_prefix and result.startswith(line_prefix):
        value = result[len(line_prefix) :]
    else:
        value = result

    match variable_form:
        case NewVariable(name=name, modifiers=modifiers):
            declaration_formatter = language.format_variable_declaration
            if is_call_binding:
                declaration_formatter = getattr(
                    language,
                    "format_call_variable_declaration",
                    declaration_formatter,
                )
            wrapped = declaration_formatter(name, value, data, modifiers)
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

    ``data`` is the parsed input with ``$ref`` markers left intact so
    the renderer can emit them as bare identifiers.  ``data_for_preamble``
    is the same tree with each ref marker resolved against the caller's
    ``ref_values`` (or stripped when the value is not supplied), so
    preamble inference sees the types actually flowing through the
    rendered code -- not the marker's ``{str: str}`` shape.
    """

    data: Value
    data_for_preamble: Value
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
    ref_values: Mapping[str, Value] | None,
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
    active_ref_key = _active_literalize_ref_key(
        source=source,
        input_format=input_format,
        data=data,
        ref_key=ref_key,
    )

    language.validate_spec_for_data(data=data)

    result = _literalize(
        data=data,
        language=language,
        line_prefix=line_prefix,
        include_delimiters=include_delimiters,
        ref_case=ref_case,
        ref_values=ref_values,
        ref_key=active_ref_key,
        collection_layout=collection_layout,
    )

    comment_line_prefix = (
        line_prefix + language.indent if include_delimiters else line_prefix
    )

    resolved: ResolvedComments | None = None
    match parsed:
        case ParsedYaml() if parsed.needs_comment_resolve:
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
        case ParsedToml():
            comment_cfg = language.comment_config
            resolved = resolve_toml_comments(
                toml_doc=parsed.toml_doc,
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

    data_for_preamble: Value = data
    if ref_values:
        resolution = _resolve_ref_for_preamble(
            value=data,
            ref_values=ref_values,
            ref_key=active_ref_key,
        )
        data_for_preamble = resolution.value if resolution.include else []

    return _PreFormState(
        data=data,
        data_for_preamble=data_for_preamble,
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
        is_call_binding=False,
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
        data=pre_form.data_for_preamble,
        language=language,
        has_variable_declaration=variable_name is not None and is_declaration,
    )
    preamble = deduplicate_preamble_entries(
        entries=(
            tuple(language.static_preamble)
            + computed.header
            + language.data_dependent_preamble(pre_form.data_for_preamble)
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
            source_data=pre_form.data_for_preamble,
        )

    return LiteralizeResult(
        declaration_code=result,
        preamble=preamble,
        body_preamble=computed.body,
        pre_declaration_comments=pre_decl,
        types_present=computed.types_present,
        source_data=pre_form.data_for_preamble,
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
    ref_values: Mapping[str, Value] | None,
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
        ref_values=ref_values,
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
    ref_values: Mapping[str, ValueInput] | None = None,
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
        ref_case: Optional :class:`IdentifierCase` controlling how ref
            identifiers are cased in the rendered output.
            ``{ref_key: "name"}`` markers anywhere in the data are
            rendered as bare identifiers using the
            language's
            :attr:`~literalizer._language.Language.format_call_ref_identifier`
            hook.  When ``None`` (default), ref names are emitted
            verbatim.  When set, the identifier name is converted to
            *ref_case* first.
        ref_values: Optional mapping from ref identifier to the value
            declared elsewhere for that ref.  Some languages render a
            ref differently depending on the type behind it (V emits
            ``name`` for primitive scalars but ``name.clone()`` for
            arrays and maps); supplying *ref_values* lets those
            languages pick the right form.  When omitted, a ref's type
            is unknown and languages fall back to their type-agnostic
            default.  Keys should match the identifiers used in *source*
            before any *ref_case* conversion.
        ref_key: The dict key used to identify variable-reference
            markers in the input data.  A single-key dict whose key
            equals *ref_key* and whose value is a string is treated as a
            ref marker.  Defaults to ``"$ref"``.
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
            :attr:`~literalizer._language.Language.supported_ref_cases`
            for the target language.
        VariableNameNotSupportedError: If *variable_form* is supplied
            but the target language sets
            :attr:`~literalizer._language.Language.supports_variable_names`
            to ``False``.
        WrapInFileWithoutVariableNotSupportedError: If *wrap_in_file*
            is ``True`` and *variable_form* is ``None`` but the target
            language sets
            :attr:`~literalizer._language.Language.supports_no_variable_wrap_in_file`
            to ``False`` (i.e. it cannot represent a bare value at
            file-statement scope).
    """
    if ref_case is not None and ref_case not in language.supported_ref_cases:
        raise UnsupportedIdentifierCaseError(
            language_name=type(language).__name__,
            case_name=ref_case.name,
        )
    materialized_ref_values: Mapping[str, Value] | None = (
        {
            name: _materialize_value_input(value=value)
            for name, value in ref_values.items()
        }
        if ref_values is not None
        else None
    )
    if variable_form is not None and not language.supports_variable_names:
        raise VariableNameNotSupportedError(
            language_name=type(language).__name__,
            variable_name=variable_form.name,
        )
    if (
        wrap_in_file
        and variable_form is None
        and not language.supports_no_variable_wrap_in_file
    ):
        raise WrapInFileWithoutVariableNotSupportedError(
            language_name=type(language).__name__,
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
            ref_values=materialized_ref_values,
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
        ref_values=materialized_ref_values,
        ref_key=ref_key,
        collection_layout=collection_layout,
    )
    return _literalize_apply_form(
        pre_form=pre_form,
        language=language,
        variable_form=variable_form,
        wrap_in_file=wrap_in_file,
    )


def _active_literalize_ref_key(
    *,
    source: str,
    input_format: InputFormat,
    data: Value,
    ref_key: str,
) -> str:
    """Return *ref_key* when literalize should check for ref markers."""
    if (ref_key == "$ref" and "$" in source) or (
        ref_key != "$ref" and ref_key in source
    ):
        return ref_key
    if (
        input_format is InputFormat.JSON
        and "\\" in source
        and _contains_ref_marker(value=data, ref_key=ref_key)
    ):
        return ref_key
    return _DISABLED_REF_KEY


def _extract_call_arg_ref_name(*, value: Value, ref_key: str) -> str | None:
    """Return the identifier name for a ``{ref_key: "name"}`` marker.

    Returns ``None`` when *value* is not a variable-reference marker.
    In :func:`literalize_call` such markers render as the bare
    identifier instead of being formatted as a literal value.
    """
    if not ref_key or not isinstance(value, dict) or len(value) != 1:
        return None
    ref_value = value.get(ref_key)
    if not isinstance(ref_value, str):
        return None
    return ref_value


def _contains_ref_marker(*, value: Value, ref_key: str) -> bool:
    """Return whether *value* contains a ``{ref_key: "name"}`` marker."""
    if _extract_call_arg_ref_name(value=value, ref_key=ref_key) is not None:
        return True
    match value:
        case dict():
            return any(
                _contains_ref_marker(value=v, ref_key=ref_key)
                for v in value.values()
            )
        case list():
            return any(
                _contains_ref_marker(value=item, ref_key=ref_key)
                for item in value
            )
        case _:
            return False


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


@dataclasses.dataclass(frozen=True)
class _PreambleRefResolution:
    """Ref-marker resolution result for preamble inference."""

    include: bool
    value: Value


@beartype
def _resolve_ref_for_preamble(
    *,
    value: Value,
    ref_values: Mapping[str, Value],
    ref_key: str,
) -> _PreambleRefResolution:
    """Resolve ref markers for preamble inference.

    Returns ``include=False`` when *value* is a ref marker whose source
    value was not supplied.  Callers use that flag to drop the
    marker, preserving the historical "strip refs" behavior for
    unknown ref names.
    """
    ref_name = _extract_call_arg_ref_name(value=value, ref_key=ref_key)
    if ref_name is not None:
        if ref_name not in ref_values:
            return _PreambleRefResolution(include=False, value=None)
        return _PreambleRefResolution(
            include=True,
            value=ref_values[ref_name],
        )
    if isinstance(value, list):
        resolved_list: list[Value] = []
        for item in value:
            resolved = _resolve_ref_for_preamble(
                value=item,
                ref_values=ref_values,
                ref_key=ref_key,
            )
            if resolved.include:
                resolved_list.append(resolved.value)
        return _PreambleRefResolution(include=True, value=resolved_list)
    if isinstance(value, dict):
        resolved_dict: dict[Scalar, Value] = {}
        for key, item in value.items():
            resolved = _resolve_ref_for_preamble(
                value=item,
                ref_values=ref_values,
                ref_key=ref_key,
            )
            if resolved.include:
                resolved_dict[key] = resolved.value
        return _PreambleRefResolution(include=True, value=resolved_dict)
    return _PreambleRefResolution(include=True, value=value)


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
def _compute_call_arg_ref_consume_inhibited_names(
    *,
    elements: list[Value],
    ref_values: Mapping[str, Value],
    ref_key: str,
    language: Language,
) -> frozenset[str]:
    """Return ref identifiers whose underlying value inhibits the
    language's consume form.

    Languages whose consume operator rejects certain value types (notably
    the Mojo ``^`` on register-trivial scalars) expose
    :attr:`~literalizer._language.Language.consumable_ref_value_inhibits_consuming_form`
    so the call site can route those refs through the non-consuming
    formatter instead.  Names are returned in the original (pre-``ref_case``)
    form so they can be compared against the user-supplied
    ``consumable_refs`` set without further conversion.

    Refs whose value is not present in *ref_values* fall through with the
    consume form intact, matching the historical behavior for callers
    that omit ``ref_values``.
    """
    if not ref_values:
        return frozenset[str]()
    inhibits = language.consumable_ref_value_inhibits_consuming_form
    referenced: set[str] = set()
    for element in elements:
        arg_values = element if isinstance(element, list) else [element]
        for value in arg_values:
            ref_name = _extract_call_arg_ref_name(value=value, ref_key=ref_key)
            if ref_name is None:
                continue
            referenced.add(ref_name)
    return frozenset(
        name
        for name in referenced
        if name in ref_values and inhibits(ref_values[name])
    )


@beartype
def _strip_call_arg_refs_for_preamble(
    *,
    data: Value,
    per_element_data: list[Value] | None,
    ref_key: str,
    ref_values: Mapping[str, Value],
) -> Value:
    """Return *data* with call-argument ref markers resolved or removed.

    Ref markers represent a variable declared elsewhere, not real data,
    so they would pollute data-driven preamble inference (e.g. dragging
    in ``Data.Map`` imports for Haskell just because the marker happens
    to be a ``{str: str}`` dict).  Drop refs whose values are unknown
    before computing the preamble while leaving :func:`_format_call_args`
    to render them.

    When *ref_values* supplies the value behind a marker, substitute
    that value into the preamble input so the referenced variable's
    types participate in body-preamble computation.

    When *per_element* is ``True``, *data* is a list of argument lists
    and refs are stripped from each inner list.  Otherwise a
    top-level ref becomes an empty list, standing in for "no data".
    Refs nested inside list or dict argument values are also stripped
    recursively.
    """
    if ref_values:
        resolved = _resolve_ref_for_preamble(
            value=data,
            ref_values=ref_values,
            ref_key=ref_key,
        )
        return resolved.value if resolved.include else []
    if per_element_data is not None:
        result: list[Value] = []
        for element in per_element_data:
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
    scalar_wrap_ids: frozenset[int],
    wrap_arg: Callable[[Value, str], str],
    dict_open_override: str | None,
    ref_case: IdentifierCase | None,
    ref_values: Mapping[str, Value] | None,
    consumable_ref_names: frozenset[str],
    single_use_ref_names: frozenset[str],
    consume_inhibited_ref_names: frozenset[str],
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
    lists.  *consume_inhibited_ref_names* is the set of refs whose
    underlying value type inhibits the language's consume form (e.g.
    the Mojo ``^`` on register-trivial scalars).  All three sets use the
    original (pre-``ref_case``) name.  A ref is rendered via the
    language's ``format_call_arg_ref_identifier_consumable`` hook only
    when it is in *consumable_ref_names* and *single_use_ref_names* and
    not in *consume_inhibited_ref_names*; otherwise it goes through the
    regular ``format_call_arg_ref_identifier`` hook.  This ensures that
    a ref used in more than one call -- or whose value type the
    language's consume operator rejects -- is never consumed, even when
    the caller listed it as consumable.
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
            and raw_ref_name not in consume_inhibited_ref_names
        )
        ref_value = (
            ref_values.get(raw_ref_name) if ref_values is not None else None
        )
        if is_consumable:
            return language.format_call_arg_ref_identifier_consumable(
                ref_name, ref_value
            )
        return language.format_call_arg_ref_identifier(ref_name, ref_value)
    formatted = wrap_arg(
        value,
        _format_value(
            value=value,
            spec=language,
            dict_open_override=dict_open_override,
            wrap_ids=wrap_ids,
            sequence_open_override=None,
            ref_case=ref_case,
            ref_values=ref_values,
            expand_refs=True,
            ref_key=ref_key,
            collection_layout=collection_layout,
            multiline_prefix="",
        ),
    )
    wrap_scalar = language.heterogeneous_behavior.wrap_scalar
    if (
        wrap_scalar is None
        or id(value) not in scalar_wrap_ids
        or not isinstance(value, _SCALAR_TYPES)
    ):
        return formatted
    return wrap_scalar(value, formatted)


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
    scalar_wrap_ids: frozenset[int],
    style: CallStyle,
    dict_open_overrides: Sequence[str | None],
    ref_case: IdentifierCase | None,
    ref_values: Mapping[str, Value] | None,
    consumable_ref_names: frozenset[str],
    single_use_ref_names: frozenset[str],
    consume_inhibited_ref_names: frozenset[str],
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
            scalar_wrap_ids=scalar_wrap_ids,
            wrap_arg=wrap_arg,
            dict_open_override=dict_open_overrides[slot_index],
            ref_case=ref_case,
            ref_values=ref_values,
            consumable_ref_names=consumable_ref_names,
            single_use_ref_names=single_use_ref_names,
            consume_inhibited_ref_names=consume_inhibited_ref_names,
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
def _assemble_bare_call_expr(
    *,
    target_function: str,
    args_str: str,
    style: CallStyle,
) -> str:
    """Build the bare call expression (no transform, no terminator).

    ``call_transform`` is only valid for the substitution call styles
    (:class:`PositionalCallStyle`, :class:`KeywordCallStyle`,
    :class:`ObjectCallStyle`); the prefix/postfix/command styles never
    receive one (:func:`_validate_call_preconditions` rejects it), so
    each style here just renders the language-native call form.
    """
    match style:
        case PostfixCallStyle():
            return (
                f"{args_str} {target_function}"
                if args_str
                else target_function
            )
        case PositionalCallStyle() | KeywordCallStyle() | ObjectCallStyle():
            return f"{target_function}{args_str}"
        case PrefixCallStyle(arg_separator=sep):
            inside = (
                f"{target_function}{sep}{args_str}"
                if args_str
                else target_function
            )
            return f"({inside})"
        case CommandCallStyle(arg_separator=sep):
            return (
                f"{target_function}{sep}{args_str}"
                if args_str
                else target_function
            )
        case _ as unreachable:
            assert_never(unreachable)


@beartype
def _assemble_call(
    *,
    target_function: str,
    args_str: str,
    call_transform: Callable[[CallContext], str] | None,
    statement_terminator: str,
    style: CallStyle,
    index: int,
    row: Sequence[Value],
    zipped: str | None,
) -> str:
    """Build one complete call statement.

    Renders the bare call expression and, when a *call_transform* is
    supplied, threads it through :class:`CallContext` so the transform
    can pair the call with per-row data.  The language's statement
    terminator is appended last.
    """
    call_expr = _assemble_bare_call_expr(
        target_function=target_function,
        args_str=args_str,
        style=style,
    )
    if call_transform is not None:
        call_expr = call_transform(
            CallContext(
                call=call_expr,
                index=index,
                row=row,
                zipped=zipped,
            )
        )
    return f"{call_expr}{statement_terminator}"


@beartype
def _render_call_per_element(
    *,
    data: list[Value],
    language: Language,
    style: CallStyle,
    target_function: str,
    parameter_names: Sequence[str],
    call_transform: Callable[[CallContext], str] | None,
    zip_literals: Sequence[str] | None,
    ref_case: IdentifierCase | None,
    consumable_ref_names: frozenset[str],
    ref_values: Mapping[str, Value],
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
    scalar_wrap_ids = _compute_call_slot_scalar_wrap_ids(
        elements=data,
        spec=language,
        ref_key=ref_key,
    )
    single_use_ref_names = _compute_call_arg_ref_single_use_names(
        elements=data,
        ref_key=ref_key,
    )
    consume_inhibited_ref_names = (
        _compute_call_arg_ref_consume_inhibited_names(
            elements=data,
            ref_values=ref_values,
            ref_key=ref_key,
            language=language,
        )
    )
    rendered_elements: list[str] = []
    for index, element in enumerate(iterable=data):
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
            scalar_wrap_ids=scalar_wrap_ids,
            style=style,
            dict_open_overrides=slot_overrides,
            ref_case=ref_case,
            ref_values=ref_values,
            consumable_ref_names=consumable_ref_names,
            single_use_ref_names=single_use_ref_names,
            consume_inhibited_ref_names=consume_inhibited_ref_names,
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
                    index=index,
                    row=arg_values,
                    zipped=(
                        zip_literals[index]
                        if zip_literals is not None
                        else None
                    ),
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
    call_transform: Callable[[CallContext], str] | None,
    zip_literal: str | None,
    ref_case: IdentifierCase | None,
    consumable_ref_names: frozenset[str],
    ref_values: Mapping[str, Value],
    ref_key: str,
    collection_layout: CollectionLayout,
    variable_form: NewVariable | ExistingVariable | None,
) -> str:
    """Render a single call from the whole parsed value.

    A single top-level ref marker renders as just the identifier; in
    that case shape validation and wrap-id computation are skipped.

    When *variable_form* is supplied, the assembled call expression is
    wrapped via the language's ``format_variable_declaration`` /
    ``format_variable_assignment`` hook (instead of being routed through
    ``format_call_statement`` and the language's statement terminator),
    producing an idiomatic binding such as ``let p2 = Playlist::new();``.
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
        scalar_wrap_ids=frozenset[int](),
        style=style,
        dict_open_overrides=[None],
        ref_case=ref_case,
        ref_values=ref_values,
        consumable_ref_names=consumable_ref_names,
        single_use_ref_names=_compute_call_arg_ref_single_use_names(
            elements=[[data]],
            ref_key=ref_key,
        ),
        consume_inhibited_ref_names=(
            _compute_call_arg_ref_consume_inhibited_names(
                elements=[[data]],
                ref_values=ref_values,
                ref_key=ref_key,
                language=language,
            )
        ),
        ref_key=ref_key,
        collection_layout=collection_layout,
    )
    if variable_form is None:
        return language.format_call_statement(
            _assemble_call(
                target_function=target_function,
                args_str=args_str,
                call_transform=call_transform,
                statement_terminator=language.statement_terminator,
                style=style,
                index=0,
                row=[data],
                zipped=zip_literal,
            )
        )
    call_expr = _assemble_call(
        target_function=target_function,
        args_str=args_str,
        call_transform=call_transform,
        statement_terminator="",
        style=style,
        index=0,
        row=[data],
        zipped=zip_literal,
    )
    return _apply_variable_wrapper(
        result=call_expr,
        language=language,
        data=data,
        variable_form=variable_form,
        line_prefix="",
        is_call_binding=True,
    )


@beartype
def _has_inline_multiline_dict_arg(
    *,
    arg_values: Sequence[Value],
    ref_key: str,
) -> bool:
    """Return ``True`` when *arg_values* contains a dict with two or
    more entries that is not a ``$ref`` marker.
    """
    return any(
        _value_is_multikey_non_ref_dict(value=value, ref_key=ref_key)
        for value in arg_values
    )


@beartype
def _value_is_multikey_non_ref_dict(*, value: Value, ref_key: str) -> bool:
    """Return ``True`` if *value* is a dict with multiple keys that is
    not a single-key ``$ref`` marker.
    """
    if not isinstance(value, dict):
        return False
    if len(value) == 1 and isinstance(value.get(ref_key), str):
        return False
    return len(value) > 1


@beartype
def _yaml_has_standalone_comments(*, parsed: ParsedInput) -> bool:
    """Return ``True`` when the YAML source carries standalone comments.

    Standalone comments are comments that appear on their own line —
    either before a top-level element or after the last element.  Inline
    comments (those that follow a value on the same line) do not count.
    Returns ``False`` for non-YAML input or for YAML that parses to a
    scalar; ``ruamel.yaml`` only attaches collection-comment metadata
    to :class:`CommentedSeq` / :class:`CommentedMap` / :class:`CommentedSet`.
    """
    if not isinstance(parsed, ParsedYaml):
        return False
    if not isinstance(
        parsed.raw_data, CommentedSeq | CommentedMap | CommentedSet
    ):
        return False
    collection_comments = extract_yaml_comments(ruamel_data=parsed.raw_data)
    if collection_comments.trailing:
        return True
    return any(element.before for element in collection_comments.elements)


@beartype
def _validate_wrap_in_file_supports_standalone_comments(
    *,
    language: Language,
    wrap_in_file: bool,
    contains_standalone_comments: bool,
) -> None:
    """Raise when wrapping calls would drop required standalone
    comments.
    """
    if (
        wrap_in_file
        and contains_standalone_comments
        and not language.supports_standalone_comments_in_wrapped_calls
    ):
        raise UnsupportedCallShapeError(
            language_name=type(language).__name__,
            reason=(
                "standalone comments cannot be preserved when wrapping "
                "calls in this language"
            ),
        )


@beartype
def _validate_parameter_count(
    *,
    language: Language,
    parameter_names: Sequence[str],
) -> None:
    """Raise ``UnsupportedCallShapeError`` if the parameter count is out
    of range for ``language``.
    """
    if (
        len(parameter_names) == 0
        and not language.supports_zero_parameter_calls
    ):
        raise UnsupportedCallShapeError(
            language_name=type(language).__name__,
            reason=(
                "zero-parameter calls have no representation in this language"
            ),
        )
    max_params = language.max_call_parameters
    if len(parameter_names) > max_params:
        raise UnsupportedCallShapeError(
            language_name=type(language).__name__,
            reason=(
                f"call exceeds this language's {max_params}-parameter limit"
            ),
        )


@beartype
def _validate_call_variable_form(
    *,
    language: Language,
    variable_form: NewVariable | ExistingVariable,
    per_element: bool,
) -> None:
    """Raise typed errors for unsupported ``variable_form``
    combinations.

    ``BothVariableForms`` is rejected upstream by ``literalize_call``
    itself, so the ``variable_form`` parameter here is narrower.
    """
    if per_element:
        raise UnsupportedCallShapeError(
            language_name=type(language).__name__,
            reason=(
                "variable_form is incompatible with per_element=True; "
                "the API does not provide a name per element"
            ),
        )
    if not language.supports_variable_names:
        raise VariableNameNotSupportedError(
            language_name=type(language).__name__,
            variable_name=variable_form.name,
        )
    if not language.call_returns_expression:
        raise UnsupportedCallShapeError(
            language_name=type(language).__name__,
            reason=(
                "calls in this language are statements, not expressions, "
                "so the call result cannot be bound to a variable"
            ),
        )
    if not language.supports_call_variable_binding:
        raise UnsupportedCallShapeError(
            language_name=type(language).__name__,
            reason=(
                "this language's variable-declaration template wraps or "
                "transforms the right-hand side in a way that is only "
                "valid for literal values, not call expressions"
            ),
        )


@beartype
def _validate_call_preconditions(
    *,
    language: Language,
    target_function: str,
    target_function_parts: tuple[str, ...],
    parameter_names: Sequence[str],
    arg_values: Sequence[Value],
    ref_key: str,
    ref_case: IdentifierCase | None,
    call_transform: Callable[[CallContext], str] | None,
    style: CallStyle,
    variable_form: NewVariable | ExistingVariable | None,
    per_element: bool,
) -> None:
    """Raise typed errors for unsupported ``literalize_call`` inputs."""
    _validate_parameter_count(
        language=language, parameter_names=parameter_names
    )
    if variable_form is not None:
        _validate_call_variable_form(
            language=language,
            variable_form=variable_form,
            per_element=per_element,
        )
    if (
        not language.supports_inline_multiline_dict_args
        and _has_inline_multiline_dict_arg(
            arg_values=arg_values, ref_key=ref_key
        )
    ):
        raise UnsupportedCallShapeError(
            language_name=type(language).__name__,
            reason=(
                "multi-key dict call arguments have no inline multiline "
                "representation in this language"
            ),
        )
    if call_transform is not None and not language.call_returns_expression:
        raise UnsupportedCallShapeError(
            language_name=type(language).__name__,
            reason=(
                "calls in this language are statements, not expressions, "
                "so a call_transform cannot consume the call as a value"
            ),
        )
    if call_transform is not None and not isinstance(
        style, PositionalCallStyle | KeywordCallStyle | ObjectCallStyle
    ):
        raise UnsupportedCallShapeError(
            language_name=type(language).__name__,
            reason=(
                "call_transform is only supported for languages whose "
                "call form is an expression that can be wrapped "
                "(positional, keyword, or object call style); this "
                "language uses a prefix, postfix, or command call "
                "style whose language-native wrapper cannot be built "
                "from a context-aware transform"
            ),
        )
    if target_function_parts[-1] in language.reserved_identifiers:
        raise UnsupportedCallShapeError(
            language_name=type(language).__name__,
            reason=(
                f"target_function {target_function!r} ends in a reserved "
                f"identifier of this language"
            ),
        )
    if len(target_function_parts) > 1 and not language.supports_dotted_calls:
        raise DottedCallTargetNotSupportedError(
            language_name=type(language).__name__,
            target_function=target_function,
        )
    if ref_case is not None and ref_case not in language.supported_ref_cases:
        raise UnsupportedIdentifierCaseError(
            language_name=type(language).__name__,
            case_name=ref_case.name,
        )


def _is_value_mapping(
    value: ValueInput, /
) -> TypeIs[Mapping[Scalar, ValueInput]]:
    """Narrow ``value`` to the ``Mapping`` arm of ``ValueInput``."""
    return isinstance(value, Mapping)


def _is_value_sequence(value: ValueInput, /) -> TypeIs[Sequence[ValueInput]]:
    """Narrow ``value`` to the ``Sequence`` arm of ``ValueInput``,
    excluding the ``str``/``bytes`` scalars that are also sequences.
    """
    return isinstance(value, Sequence) and not isinstance(value, str | bytes)


@beartype
def _wrap_call_in_file(
    *,
    language: Language,
    result: str,
    variable_form: NewVariable | ExistingVariable | None,
    target_function_parts: tuple[str, ...],
    parameter_names: Sequence[str],
    arg_values: Sequence[Value],
    call_transform: Callable[[CallContext], str] | None,
    preamble: tuple[str, ...],
    computed_body: tuple[str, ...],
) -> str:
    """Wrap a rendered ``literalize_call`` result in a complete file.

    Emits a no-op stub for the target function so the wrapped file
    compiles on its own.  ``StubReturn.VALUE`` is used whenever the
    call's return value is consumed -- either by a ``call_transform``
    or by binding it to a ``variable_form``; otherwise the call result
    is discarded and a void stub suffices.
    """
    stub_return = (
        StubReturn.VALUE
        if call_transform is not None or variable_form is not None
        else StubReturn.VOID
    )
    body_stubs = language.format_call_stub(
        target_function_parts, parameter_names, stub_return, arg_values
    )
    preamble_stubs = language.format_call_preamble_stub(
        target_function_parts, parameter_names, stub_return, arg_values
    )
    wrap_variable_name = (
        variable_form.name if variable_form is not None else ""
    )
    wrapped = language.wrap_in_file(
        content=result,
        variable_name=wrap_variable_name,
        body_preamble=body_stubs + computed_body,
    )
    call_binding_pragmas: tuple[str, ...] = ()
    if variable_form is not None:
        pragma_hook = getattr(
            language, "format_call_binding_file_pragmas", None
        )
        if pragma_hook is not None:
            call_binding_pragmas = pragma_hook()
    # Stubs follow the language's static preamble (e.g. Go's
    # ``package main`` must come first).
    full_preamble = preamble + call_binding_pragmas + preamble_stubs
    if full_preamble:
        wrapped = "\n".join(full_preamble) + "\n" + wrapped
    return wrapped


def _materialize_value_input(*, value: ValueInput) -> Value:
    """Convert a user-supplied ``ValueInput`` into the internal ``Value``
    form, replacing any non-``list`` ``Sequence`` and non-``dict``
    ``Mapping`` with concrete ``list`` / ``dict`` instances.
    """
    if _is_value_mapping(value):
        return {
            key: _materialize_value_input(value=item)
            for key, item in value.items()
        }
    if _is_value_sequence(value):
        return [_materialize_value_input(value=item) for item in value]
    return value


@beartype
@dataclasses.dataclass(frozen=True)
class _ZipResolution:
    """Resolved ``zip_values``: rendered literals plus the materialized
    values (the latter feed preamble/body-type inference so languages
    with generated value types declare the zip literal's type).
    """

    literals: list[str]
    values: list[Value]


@beartype
def _preamble_data_with_zip(
    *,
    data_for_preamble: Value,
    zip_resolution: "_ZipResolution | None",
) -> Value:
    """Fold ``zip_values`` into the data used for preamble inference.

    The rendered zip literals reference whatever type machinery the
    language uses for a value (e.g. Haskell's ``data Val`` constructors,
    Gleam's ``pub type GVal``).  Including the materialized zip values
    here makes :func:`compute_preamble` /
    ``call_data_dependent_preamble`` see their types so the generated
    declarations cover them.  The call data is nested as a single
    element so its shape is preserved while the zip values are added
    as siblings; only the *set of types present* matters here, not the
    structure.
    """
    if zip_resolution is None:
        return data_for_preamble
    return [data_for_preamble, *zip_resolution.values]


@beartype
def _resolve_zip_literals(
    *,
    zip_values: Sequence[ValueInput] | None,
    call_transform: Callable[[CallContext], str] | None,
    call_count: int,
    language: Language,
    collection_layout: CollectionLayout,
) -> _ZipResolution | None:
    """Render each ``zip_values`` entry to a language-native literal.

    Returns ``None`` when no ``zip_values`` were supplied.  Otherwise a
    ``call_transform`` is required (the values are only reachable
    through it) and the sequence must hold exactly one entry per
    generated call; violations raise
    :class:`~literalizer.exceptions.ZipValuesWithoutCallTransformError`
    or :class:`~literalizer.exceptions.ZipValuesLengthMismatchError`.
    Each entry is rendered the same way :func:`literalize` renders a
    whole value, so the paired literal matches the target language
    (``True`` in Python, ``true`` in TypeScript, ...).
    """
    if zip_values is None:
        return None
    if call_transform is None:
        raise ZipValuesWithoutCallTransformError
    if len(zip_values) != call_count:
        raise ZipValuesLengthMismatchError(
            call_count=call_count,
            zip_count=len(zip_values),
        )
    literals: list[str] = []
    materialized_values: list[Value] = []
    for value in zip_values:
        materialized = _materialize_value_input(value=value)
        language.validate_spec_for_data(data=materialized)
        materialized_values.append(materialized)
        literals.append(
            _literalize(
                data=materialized,
                language=language,
                line_prefix="",
                include_delimiters=True,
                ref_case=None,
                ref_values=None,
                ref_key=_DISABLED_REF_KEY,
                collection_layout=collection_layout,
            )
        )
    return _ZipResolution(literals=literals, values=materialized_values)


@beartype
def literalize_call(
    *,
    source: str,
    input_format: InputFormat,
    language: Language,
    target_function: str,
    parameter_names: Sequence[str],
    call_transform: Callable[[CallContext], str] | None = None,
    zip_values: Sequence[ValueInput] | None = None,
    per_element: bool = True,
    wrap_in_file: bool = False,
    ref_case: IdentifierCase | None = None,
    consumable_refs: frozenset[str] = frozenset(),
    ref_values: Mapping[str, ValueInput] | None = None,
    ref_key: str = "$ref",
    collection_layout: CollectionLayout = CollectionLayout.COMPACT,
    variable_form: VariableForm | None = None,
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
        call_transform: Optional callable transforming each generated
            call.  Invoked once per call as ``call_transform(context)``
            with a :class:`CallContext` and returns the transformed
            string (e.g. ``lambda ctx: f"print({ctx.call})"``).  The
            context also exposes the call's zero-based ``index``, its
            input ``row``, and the paired ``zipped`` literal, so a
            transform can render data from a parallel sequence beside
            each call.  Only supported for languages whose call form is
            an expression that can be wrapped (positional, keyword, or
            object call style); prefix/postfix/command-style languages
            reject it with
            :class:`~literalizer.exceptions.UnsupportedCallShapeError`.
        zip_values: Optional sequence paired positionally with the
            generated calls.  Each entry is rendered to a
            language-native literal (via the same machinery as
            :func:`literalize`) and exposed on
            :attr:`CallContext.zipped` for the matching call, enabling
            patterns like printing an expected value beside each call's
            actual return value.  Must have exactly one entry per
            generated call (one per top-level element when
            *per_element* is ``True``, otherwise one); a length
            mismatch raises
            :class:`~literalizer.exceptions.ZipValuesLengthMismatchError`.
            Requires *call_transform* (the values are only reachable
            through it); supplying *zip_values* without one raises
            :class:`~literalizer.exceptions.ZipValuesWithoutCallTransformError`.
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
            multiple languages.  When *language*'s ``supported_ref_cases``
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
        ref_values: Optional mapping from ref identifier to the source
            value declared elsewhere.  When supplied, values for refs
            used in *source* are included in data-driven preamble
            inference, so languages with generated body types (for
            example Haskell's ``data Val = ...``) declare constructors
            for types reachable only through refs.  Missing ref names
            keep the historical behavior: their markers are omitted
            from preamble inference.  Keys should match the identifiers
            used in *source* before any *ref_case* conversion.
        ref_key: The dict key used to identify variable-reference
            markers in the input data.  A single-key dict whose key
            equals *ref_key* and whose value is a string is treated as
            a ref marker.  Defaults to ``"$ref"``.
        collection_layout: Controls layout for collections nested
            inside call arguments.  ``CollectionLayout.COMPACT``
            preserves the existing one-line nested rendering, while
            ``CollectionLayout.MULTILINE`` expands non-empty nested
            collections with one element per line.
        variable_form: When supplied, wrap the call expression in a
            variable binding using the language's
            ``format_variable_declaration`` /
            ``format_variable_assignment`` hook (the same machinery
            used by :func:`literalize`).  Pass :class:`NewVariable` for
            an idiomatic declaration (``let p2 = Playlist::new();``,
            ``const p2 = new Playlist();``, ``p2 = Playlist()``) or
            :class:`ExistingVariable` for an assignment to an existing
            name.  :class:`BothVariableForms` is rejected with
            :class:`~literalizer.exceptions.UnsupportedCallShapeError`
            because emitting both a declaration and an assignment
            would invoke the target function twice.  Mutability and
            inference are controlled by the per-language
            ``declaration_style`` and ``Modifiers`` enums on the
            supplied ``Language`` instance, not by extra arguments
            here.  Incompatible with ``per_element=True`` (no
            per-element name vector is provided); incompatible with
            languages whose call form is not an expression
            (``call_returns_expression=False``).

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
    if isinstance(variable_form, BothVariableForms):
        # Rendering both halves would invoke the call twice -- a silent
        # side-effect bug for any non-pure target.  Reject up front so
        # the rest of the function can narrow ``variable_form`` to
        # ``NewVariable | ExistingVariable | None``.
        raise UnsupportedCallShapeError(
            language_name=type(language).__name__,
            reason=(
                "BothVariableForms is not supported for literalize_call: "
                "rendering both a declaration and an assignment would "
                "invoke the target function twice"
            ),
        )
    parsed = parse_input(source=source, input_format=input_format)
    data = parsed.data
    contains_standalone_comments = _yaml_has_standalone_comments(parsed=parsed)
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

    per_element_data: list[Value] | None = None
    if per_element:
        if not isinstance(data, list):
            msg = (
                "per_element=True requires a top-level list, "
                f"got {type(data).__name__}"
            )
            raise PerElementNotListError(msg)
        per_element_data = data
    arg_values: Sequence[Value] = (
        per_element_data if per_element_data is not None else [data]
    )

    target_function_parts = tuple(target_function.split(sep="."))
    _validate_call_preconditions(
        language=language,
        target_function=target_function,
        target_function_parts=target_function_parts,
        parameter_names=parameter_names,
        arg_values=arg_values,
        ref_key=ref_key,
        ref_case=ref_case,
        call_transform=call_transform,
        style=style,
        variable_form=variable_form,
        per_element=per_element,
    )
    zip_resolution = _resolve_zip_literals(
        zip_values=zip_values,
        call_transform=call_transform,
        call_count=len(arg_values),
        language=language,
        collection_layout=collection_layout,
    )
    zip_literals = (
        zip_resolution.literals if zip_resolution is not None else None
    )
    _validate_wrap_in_file_supports_standalone_comments(
        language=language,
        wrap_in_file=wrap_in_file,
        contains_standalone_comments=contains_standalone_comments,
    )
    target_function = language.format_call_target(target_function_parts)

    materialized_ref_values: Mapping[str, Value] = {
        name: _materialize_value_input(value=value)
        for name, value in (ref_values or {}).items()
    }

    data_for_preamble = _strip_call_arg_refs_for_preamble(
        data=data,
        per_element_data=per_element_data,
        ref_key=ref_key,
        ref_values=materialized_ref_values,
    )

    if per_element_data is not None:
        collection_comments: CollectionComments | None = None
        if (
            isinstance(parsed, ParsedYaml)
            and parsed.needs_comment_resolve
            and isinstance(parsed.raw_data, CommentedSeq)
        ):
            collection_comments = extract_yaml_comments(
                ruamel_data=parsed.raw_data,
            )
        result = _render_call_per_element(
            data=per_element_data,
            language=language,
            style=style,
            target_function=target_function,
            parameter_names=parameter_names,
            call_transform=call_transform,
            zip_literals=zip_literals,
            ref_case=ref_case,
            consumable_ref_names=consumable_refs,
            ref_values=materialized_ref_values,
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
            zip_literal=zip_literals[0] if zip_literals is not None else None,
            ref_case=ref_case,
            consumable_ref_names=consumable_refs,
            ref_values=materialized_ref_values,
            ref_key=ref_key,
            collection_layout=collection_layout,
            variable_form=variable_form,
        )
    preamble_data = _preamble_data_with_zip(
        data_for_preamble=data_for_preamble,
        zip_resolution=zip_resolution,
    )
    computed = compute_preamble(
        data=preamble_data,
        language=language,
        has_variable_declaration=isinstance(variable_form, NewVariable),
    )
    preamble = deduplicate_preamble_entries(
        entries=(
            tuple(language.static_preamble)
            + computed.header
            + language.call_data_dependent_preamble(preamble_data)
        )
    )

    if wrap_in_file:
        wrapped = _wrap_call_in_file(
            language=language,
            result=result,
            variable_form=variable_form,
            target_function_parts=target_function_parts,
            parameter_names=parameter_names,
            arg_values=arg_values,
            call_transform=call_transform,
            preamble=preamble,
            computed_body=computed.body,
        )
        return LiteralizeResult(
            declaration_code=wrapped,
            preamble=(),
            body_preamble=(),
            types_present=computed.types_present,
            contains_standalone_comments=contains_standalone_comments,
            source_data=data_for_preamble,
        )

    return LiteralizeResult(
        declaration_code=result,
        preamble=preamble,
        body_preamble=computed.body,
        types_present=computed.types_present,
        contains_standalone_comments=contains_standalone_comments,
        source_data=data_for_preamble,
    )
