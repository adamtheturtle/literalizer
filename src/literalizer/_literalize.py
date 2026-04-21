"""Core conversion logic: formatting values and entry points."""

import dataclasses
import datetime
import enum
from collections.abc import Callable, Sequence
from typing import assert_never, cast

from beartype import BeartypeConf, beartype
from ruamel.yaml.compat import ordereddict

from literalizer._checks import check_data
from literalizer._comments import prepend_collection_comments
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
    KeywordCallStyle,
    Language,
    ObjectCallStyle,
    PositionalCallStyle,
    PostfixCallStyle,
    PrefixCallStyle,
)
from literalizer._parsing import InputFormat, parse_input
from literalizer._preamble import compute_preamble
from literalizer._types import Scalar, Value
from literalizer.exceptions import (
    CallsNotSupportedByLanguageError,
    CallsNotSupportedByToolError,
    ParameterCountMismatchError,
    PerElementNotListError,
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
def _format_set_value(*, value: set[Scalar], spec: Language) -> str:
    """Format a set value as a native language literal."""
    set_cfg = spec.set_format_config

    if not value and set_cfg.empty_set is not None:
        return set_cfg.empty_set
    sorted_items = sorted(value, key=lambda v: (type(v).__name__, repr(v)))
    items_as_values: list[Value] = list(sorted_items)
    formatted = [_format_scalar(value=v, spec=spec) for v in sorted_items]
    entries = [
        spec.format_set_entry(v, item)
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
) -> str:
    """Format an ordered map as a native language literal."""
    ordered_map_cfg = spec.ordered_map_format_config

    ordered_map_items: list[tuple[str, Value]] = [
        (k, v)
        for k, v in value.items()  # pyright: ignore[reportUnknownVariableType,reportUnknownMemberType]
        if not (spec.skip_null_dict_values and v is None)
    ]
    parent_id = id(value)
    pairs = [
        spec.format_ordered_map_entry(
            _format_value(
                value=k,
                spec=spec,
                dict_open_override=None,
                wrap_ids=wrap_ids,
            ),
            v,
            _maybe_wrap_child(
                parent_id=parent_id,
                wrap_ids=wrap_ids,
                raw_value=v,
                formatted_value=_format_value(
                    value=v,
                    spec=spec,
                    dict_open_override=None,
                    wrap_ids=wrap_ids,
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
    pairs = [
        _build_dict_entry(
            key_str=_format_value(
                value=k,
                spec=spec,
                dict_open_override=None,
                wrap_ids=wrap_ids,
            ),
            raw_value=v,
            formatted_value=_maybe_wrap_child(
                parent_id=parent_id,
                wrap_ids=wrap_ids,
                raw_value=v,
                formatted_value=_format_value(
                    value=v,
                    spec=spec,
                    dict_open_override=None,
                    wrap_ids=wrap_ids,
                ),
                spec=spec,
            ),
            spec=spec,
        )
        for k, v in dict_items.items()
    ]
    joined = spec.element_separator.join(pairs)
    opener = (
        open_override
        if open_override is not None
        else dict_cfg.dict_open(dict_items)
    )
    return opener + joined + dict_cfg.close


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
def _format_list_value(
    *,
    value: list[Value],
    spec: Language,
    wrap_ids: frozenset[int],
) -> str:
    """Format a list as a native language literal."""
    sequence_cfg = spec.sequence_format_config

    if not value and sequence_cfg.empty_sequence is not None:
        return sequence_cfg.empty_sequence
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
                formatted_value=_format_value(
                    value=v,
                    spec=spec,
                    dict_open_override=dict_open_override,
                    wrap_ids=wrap_ids,
                ),
                spec=spec,
            ),
        )
        for v in value
    ]
    joined = spec.element_separator.join(items)
    # Some languages (e.g. Python) require a trailing comma on
    # single-element sequences to avoid syntactic ambiguity.
    if len(items) == 1 and sequence_cfg.single_element_trailing_comma:
        joined += spec.element_separator.strip()
    return f"{spec.sequence_open(value)}{joined}{sequence_cfg.close}"


@beartype
def _format_value(
    *,
    value: Value,
    spec: Language,
    dict_open_override: str | None,
    wrap_ids: frozenset[int],
) -> str:
    """Format any JSON value as a native language literal.

    Handles scalars, lists (recursively), dicts, and sets.

    When *dict_open_override* is set, dict values use it as the opening
    delimiter instead of inferring the type from their own values.
    This is used to widen map value types when dicts with differing
    inferred types appear in the same sequence.

    *wrap_ids* is the set of container ids whose scalar children should
    be wrapped by the spec's
    :attr:`~literalizer._language.HeterogeneousBehavior.wrap_scalar`
    hook.
    """
    match value:
        case ordereddict():
            return _format_ordered_map_value(
                value=value,
                spec=spec,
                wrap_ids=wrap_ids,
            )
        case dict():
            return _format_dict_value(
                value=value,
                spec=spec,
                open_override=dict_open_override,
                wrap_ids=wrap_ids,
            )
        case set():
            return _format_set_value(value=value, spec=spec)
        case list():
            return _format_list_value(
                value=value,
                spec=spec,
                wrap_ids=wrap_ids,
            )
        case _:
            return _format_scalar(value=value, spec=spec)


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
        lines.append(f"{body_prefix}{entry}{sep}")


def _format_collection_lines(
    *,
    data: dict[str, Value] | set[Scalar] | list[Value],
    spec: Language,
    body_prefix: str,
    trailing_comma: bool,
    is_ordered_map: bool,
    wrap_ids: frozenset[int],
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
            formatted_entries: list[str] = []
            for k, v in entries:
                formatted_key = _format_value(
                    value=k,
                    spec=spec,
                    dict_open_override=None,
                    wrap_ids=wrap_ids,
                )
                formatted_val = _maybe_wrap_child(
                    parent_id=parent_id,
                    wrap_ids=wrap_ids,
                    raw_value=v,
                    formatted_value=_format_value(
                        value=v,
                        spec=spec,
                        dict_open_override=None,
                        wrap_ids=wrap_ids,
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
            _append_entries(
                formatted_entries=formatted_entries,
                lines=lines,
                body_prefix=body_prefix,
                trailing_comma=trailing_comma,
                spec=spec,
            )
        case set() as set_data:
            sorted_items = sorted(
                set_data,
                key=lambda v: (type(v).__name__, repr(v)),
            )
            formatted_entries = [
                spec.format_set_entry(
                    item,
                    _format_value(
                        value=item,
                        spec=spec,
                        dict_open_override=None,
                        wrap_ids=wrap_ids,
                    ),
                )
                for item in sorted_items
            ]
            _append_entries(
                formatted_entries=formatted_entries,
                lines=lines,
                body_prefix=body_prefix,
                trailing_comma=trailing_comma,
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
                        formatted_value=_format_value(
                            value=element,
                            spec=spec,
                            dict_open_override=dict_open_override,
                            wrap_ids=wrap_ids,
                        ),
                        spec=spec,
                    ),
                )
                for element in list_data
            ]
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
    """
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
        formatted = _format_value(
            value=data,
            spec=language,
            dict_open_override=None,
            wrap_ids=wrap_ids,
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
        )
        return f"{line_prefix}{formatted}"

    body_prefix = (
        line_prefix + language.indent if include_delimiters else line_prefix
    )

    is_ordered_map = isinstance(data, ordereddict)
    trailing_comma = language.trailing_comma_config.multiline_trailing_comma
    lines = _format_collection_lines(
        data=data,
        spec=language,
        body_prefix=body_prefix,
        trailing_comma=trailing_comma,
        is_ordered_map=is_ordered_map,
        wrap_ids=wrap_ids,
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
) -> str:
    """Optionally wrap *result* in a variable declaration or
    assignment.
    """
    match variable_form:
        case None:
            return result
        case NewVariable(name=name, modifiers=modifiers):
            return language.format_variable_declaration(
                name,
                result,
                data,
                modifiers,
            )
        case _:
            return language.format_variable_assignment(
                variable_form.name,
                result,
                data,
            )


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
    )

    resolved: ResolvedComments | None = None
    if input_format is InputFormat.YAML:
        comment_cfg = language.comment_config
        cp = comment_cfg.prefix
        cs = comment_cfg.suffix
        comment_line_prefix = (
            line_prefix + language.indent
            if include_delimiters
            else line_prefix
        )
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
    elif input_format is InputFormat.TOML:
        comment_cfg = language.comment_config
        comment_line_prefix = (
            line_prefix + language.indent
            if include_delimiters
            else line_prefix
        )
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
    preamble = (
        tuple(language.static_preamble)
        + computed.header
        + language.data_dependent_preamble(pre_form.data)
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
        )

    return LiteralizeResult(
        declaration_code=result,
        preamble=preamble,
        body_preamble=computed.body,
        pre_declaration_comments=pre_decl,
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
) -> LiteralizeResult:
    """Produce combined declaration + assignment output."""
    pre_form = _literalize_pre_form(
        source=source,
        input_format=input_format,
        language=language,
        pre_indent_level=pre_indent_level,
        include_delimiters=include_delimiters,
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
    """
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
        )

    pre_form = _literalize_pre_form(
        source=source,
        input_format=input_format,
        language=language,
        pre_indent_level=pre_indent_level,
        include_delimiters=include_delimiters,
    )
    return _literalize_apply_form(
        pre_form=pre_form,
        language=language,
        variable_form=variable_form,
        wrap_in_file=wrap_in_file,
    )


@beartype
def _format_call_args(
    *,
    values: list[Value],
    params: Sequence[str],
    language: Language,
    wrap_ids: frozenset[int],
    style: CallStyle,
) -> str:
    """Format argument values for a single function call.

    For infix styles returns the parenthesized argument list
    ``(arg1, arg2)``.  For :class:`PostfixCallStyle` returns the
    unwrapped, space-separated argument list so the caller can
    assemble ``args target`` directly.
    """
    formatted = [
        _format_value(
            value=v,
            spec=language,
            dict_open_override=None,
            wrap_ids=wrap_ids,
        )
        for v in values
    ]

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
        case PostfixCallStyle(arg_separator=sep):
            return sep.join(formatted)
        case PrefixCallStyle(arg_separator=sep, keyword_prefix=kw_prefix):
            if len(params) != len(formatted):
                raise ParameterCountMismatchError(
                    expected=len(params), got=len(formatted)
                )
            return sep.join(
                f"{kw_prefix}{name}{sep}{val}"
                for name, val in zip(params, formatted, strict=True)
            )
        case _ as unreachable:
            assert_never(unreachable)


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

    Infix styles produce ``target(args)``.  :class:`PostfixCallStyle`
    produces ``args target``; when a *call_transform* like
    ``lambda c: f"emit({c})"`` is provided, the wrapper word is
    extracted via a sentinel and appended postfix, so the result is
    e.g. ``args target emit``.
    """
    match style:
        case PostfixCallStyle():
            call_expr = (
                f"{args_str} {target_function}"
                if args_str
                else target_function
            )
            if call_transform is not None:
                sentinel = "\x00"
                wrapped = call_transform(sentinel)
                idx = wrapped.index(sentinel)
                wrapper = wrapped[:idx].rstrip("(").strip()
                if wrapper:
                    call_expr = f"{call_expr} {wrapper}"
        case PositionalCallStyle() | KeywordCallStyle() | ObjectCallStyle():
            call_expr = f"{target_function}{args_str}"
            if call_transform is not None:
                call_expr = call_transform(call_expr)
        case PrefixCallStyle(arg_separator=sep):
            inside = (
                f"{target_function}{sep}{args_str}"
                if args_str
                else target_function
            )
            call_expr = f"({inside})"
            if call_transform is not None:
                sentinel = "\x00"
                wrapped = call_transform(sentinel)
                idx = wrapped.index(sentinel)
                wrapper = wrapped[:idx].rstrip("(").strip()
                if wrapper:
                    call_expr = f"({wrapper}{sep}{call_expr})"
        case _ as unreachable:
            assert_never(unreachable)
    return f"{call_expr}{statement_terminator}"


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
            complete, valid source file using the language's
            ``wrap_in_file`` method and prepend :attr:`preamble`.
            When set, :attr:`preamble` and :attr:`body_preamble`
            on the result are empty tuples (their content has been
            folded into :attr:`code`).
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

    if per_element:
        if not isinstance(data, list):
            msg = (
                "per_element=True requires a top-level list, "
                f"got {type(data).__name__}"
            )
            raise PerElementNotListError(msg)

        lines: list[str] = []
        for element in data:
            arg_values = element if isinstance(element, list) else [element]
            # Each element produces an independent call; check its
            # argument list on its own rather than the top-level list,
            # which is never rendered as a sequence in per-element mode.
            for value in arg_values:
                check_data(data=value, spec=language)
            call_wrap_ids = _compute_wrap_ids(
                data=cast("list[Value]", arg_values),
                spec=language,
            )
            args_str = _format_call_args(
                values=cast("list[Value]", arg_values),
                params=parameter_names,
                language=language,
                wrap_ids=call_wrap_ids,
                style=style,
            )
            lines.append(
                _assemble_call(
                    target_function=target_function,
                    args_str=args_str,
                    call_transform=call_transform,
                    statement_terminator=language.statement_terminator,
                    style=style,
                )
            )
        result = "\n".join(lines)
    else:
        check_data(data=data, spec=language)
        lit = _literalize(
            data=data,
            language=language,
            line_prefix="",
            include_delimiters=True,
        )
        args_str = lit if isinstance(style, PrefixCallStyle) else f"({lit})"
        result = _assemble_call(
            target_function=target_function,
            args_str=args_str,
            call_transform=call_transform,
            statement_terminator=language.statement_terminator,
            style=style,
        )
    computed = compute_preamble(
        data=data,
        language=language,
        has_variable_declaration=False,
    )
    preamble = (
        tuple(language.static_preamble)
        + computed.header
        + language.data_dependent_preamble(data)
    )

    if wrap_in_file:
        wrapped = language.wrap_in_file(
            content=result,
            variable_name="",
            body_preamble=computed.body,
        )
        if preamble:
            wrapped = "\n".join(preamble) + "\n" + wrapped
        return LiteralizeResult(
            declaration_code=wrapped,
            preamble=(),
            body_preamble=(),
        )

    return LiteralizeResult(
        declaration_code=result,
        preamble=preamble,
        body_preamble=computed.body,
    )
