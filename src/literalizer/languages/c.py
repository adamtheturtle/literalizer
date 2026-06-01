"""C language specification."""

import collections.abc
import dataclasses
import datetime
import enum
from collections.abc import Callable, Mapping, Sequence
from functools import cached_property
from types import MappingProxyType
from typing import ClassVar, TypeGuard

from beartype import beartype

from literalizer._formatters.collection_openers import (
    fixed_open,
)
from literalizer._formatters.format_dates import (
    format_date_iso,
    format_datetime_epoch,
    format_datetime_iso,
    format_time_iso,
)
from literalizer._formatters.format_entries import (
    braced_dict_entry,
    format_bytes_base64,
    format_bytes_hex,
    passthrough_sequence_entry,
    variable_declaration_formatter,
)
from literalizer._formatters.format_floats import (
    format_float_fixed,
    format_float_repr,
    format_float_scientific,
)
from literalizer._formatters.format_integers import (
    I64_MAX,
    format_integer_hex,
    make_long_suffix_formatter,
    make_overflow_fallback_formatter,
    make_ull_fallback,
)
from literalizer._formatters.format_strings import format_string_backslash
from literalizer._formatters.record_strategy import (
    RecordDeclarationField,
    RecordFieldType,
    RecordLiteralField,
    RecordRenderer,
    RecordStrategy,
    build_record_strategy,
)
from literalizer._formatters.type_inference import (
    record_shape_for_dict,
)
from literalizer._language import (
    NO_CALL_PARAMETER_LIMIT,
    NO_HETEROGENEOUS_BEHAVIOR,
    NON_KEBAB_REF_CASES,
    BareIntegerWidthStrategies,
    CommentConfig,
    DateFormatConfig,
    DatetimeFormatConfig,
    DeclarationStyleConfig,
    DictFormatConfig,
    FloatSpecialsMixin,
    HeterogeneousBehavior,
    IdentifierCase,
    LanguageCls,
    ModifierCombination,
    OrderedMapFormatConfig,
    PositionalCallStyle,
    RenderedRecordLiteral,
    SequenceFormatConfig,
    SetFormatConfig,
    StubReturn,
    TrailingCommaConfig,
    body_preamble_from_scalars,
    default_sequence_binding_declarations,
    default_wrap_calls_with_declarations,
    identity_call_ref_identifier,
    identity_call_statement,
    identity_call_target,
    identity_constructor_target,
    never_inhibits_consuming_form,
    no_call_binding_body_preamble,
    no_call_binding_file_pragmas,
    no_call_stub,
    no_data_preamble,
    no_format_integer_widened,
    no_leading_preamble,
    no_type_hint_preamble,
    no_validate_call_arg,
    prepend_body_preamble,
)
from literalizer._types import OrderedMap, Scalar, Value
from literalizer.exceptions import (
    IncompatibleFormatsError,
    UnrepresentableInputError,
)


@beartype
def _apply_format_c_entry(
    *,
    original: Value,
    formatted: str,
    int_field: str,
    uint_field: str,
    float_field: str,
    string_field: str,
) -> str:
    """Wrap a formatted entry in the appropriate union literal."""
    match original:
        case datetime.datetime() if formatted.lstrip("-").isdigit():
            field = int_field
        case str() | bytes() | datetime.date():
            field = string_field
        case bool():
            return formatted
        # Values above ``LLONG_MAX`` cannot be assigned to the signed
        # ``long long`` field without an implementation-defined
        # narrowing conversion; route them to the unsigned field.
        case int() if original > I64_MAX:
            field = uint_field
        case int():
            field = int_field
        case float():
            field = float_field
        case _:
            return formatted
    return f"((CVal){{.{field} = {formatted}}})"


@beartype
def _make_format_c_entry(
    *,
    int_field: str,
    uint_field: str,
    float_field: str,
    string_field: str,
) -> collections.abc.Callable[[Value, str], str]:
    """Return a formatter that wraps values in the appropriate
    ``CVal`` union literal using the given field names.
    """

    def _format_c_entry(original: Value, formatted: str) -> str:
        """Delegate to module-level implementation."""
        return _apply_format_c_entry(
            original=original,
            formatted=formatted,
            int_field=int_field,
            uint_field=uint_field,
            float_field=float_field,
            string_field=string_field,
        )

    return _format_c_entry


# The ``RECORD`` strategy auto-names generated ``struct`` types
# ``Record0``, ``Record1``, ...  C exposes no ``record_shape_names``
# (see issue #2476), so the shared renderer always gets an empty
# custom-name mapping and the document-order auto counter.
_C_RECORD_PREFIX = "Record"
_C_NO_RECORD_SHAPE_NAMES: Mapping[frozenset[str], str] = MappingProxyType(
    mapping={},
)


@beartype
def _apply_format_c_entry_record(
    *,
    original: Value,
    formatted: str,
    int_field: str,
    uint_field: str,
    float_field: str,
    string_field: str,
    bool_field: str,
    array_field: str,
) -> str:
    """Wrap a formatted entry in the appropriate ``CVal`` union literal
    under the ``RECORD`` strategy.

    Only three element kinds differ from :func:`_apply_format_c_entry`,
    and ``RECORD`` handles them here before delegating the rest:

    * ``bool`` / ``None`` -- ``RECORD`` makes the bare ``true`` /
      ``false`` / ``NULL`` literals (so a ``bool`` / null record field
      is a clean scalar), so one reached as a *collection element* must
      be wrapped here instead of arriving pre-wrapped.
    * ``list`` -- only a list now opens with the bare ``CVal`` array
      form, so a list element is wrapped into a ``CVal`` so the
      enclosing array is well-typed.

    Every other element is wrapped (or passed through, for a record
    ``struct`` literal or an already-complete dict / ordered map / set
    ``CVal`` expression) exactly as the default strategy does.
    """
    match original:
        case bool():
            return f"((CVal){{.{bool_field} = {formatted}}})"
        case None:
            return f"((CVal){{.{string_field} = {formatted}}})"
        case list():
            return f"((CVal){{.{array_field} = {formatted}}})"
        case _:
            return _apply_format_c_entry(
                original=original,
                formatted=formatted,
                int_field=int_field,
                uint_field=uint_field,
                float_field=float_field,
                string_field=string_field,
            )


@beartype
def _make_format_c_entry_record(
    *,
    int_field: str,
    uint_field: str,
    float_field: str,
    string_field: str,
    bool_field: str,
    array_field: str,
) -> collections.abc.Callable[[Value, str], str]:
    """Return the ``RECORD``-strategy ``CVal``-wrapping entry
    formatter.
    """

    def _format_c_entry(original: Value, formatted: str) -> str:
        """Delegate to module-level implementation."""
        return _apply_format_c_entry_record(
            original=original,
            formatted=formatted,
            int_field=int_field,
            uint_field=uint_field,
            float_field=float_field,
            string_field=string_field,
            bool_field=bool_field,
            array_field=array_field,
        )

    return _format_c_entry


@beartype
def _c_record_field_identifier(key: str, /) -> str:
    """Return the C ``struct`` member name for a dict *key*.

    C member identifiers are the dict keys verbatim (no case
    conversion), matching the designated-initializer literal form
    ``(struct Record0){.id = 1, ...}``.
    """
    return key


@beartype
def _all_record_shaped(items: list[Value], /) -> bool:
    """Return whether *items* is a non-empty list whose every element
    is a record-shaped dict (non-empty, all-string-keyed, not an
    ordered map).

    Under the ``RECORD`` strategy such a list renders each element as a
    generated ``(struct RecordN){...}`` literal, so the C sequence
    opener emits a bare ``{`` (a brace-enclosed initializer for the
    enclosing ``struct RecordN`` array member or array variable) rather
    than the ``(CVal[]){`` opener every other list keeps.

    Uniformity of shape need not be checked here: a sibling list whose
    record-shaped dicts do not all share one shape is rejected for
    every ``RECORD`` language by the shared
    :func:`literalizer._checks.check_data` guard before any value is
    formatted, so a list reaching this predicate is single-shape and
    the deduced ``struct RecordN[N]`` member is well-formed.
    """
    if not items:
        return False
    return all(_c_record_dict(item) for item in items)


@beartype
def _c_record_dict(value: Value, /) -> TypeGuard[dict[Scalar, Value]]:
    """Return whether *value* is a record-shaped dict.

    A record-shaped dict (non-empty, all-string-keyed, not an ordered
    map) renders as a ``(struct RecordN){...}`` literal under the
    ``RECORD`` strategy.
    """
    return (
        isinstance(value, dict)
        and not isinstance(value, OrderedMap)
        and record_shape_for_dict(value=value) is not None
    )


_C_RECORD_IN_CVAL_MSG = (
    "C cannot represent a record-shaped dict (or a list whose every "
    "element is one) nested under a non-record container -- a "
    "non-all-record list, a non-record dict, an ordered map, or a set "
    "-- under the RECORD heterogeneous strategy: it renders as a "
    "generated struct, which is not a CVal union member, so it is "
    "representable only as a record-field value, an element of such a "
    "field's struct array, or the document root (cf. the set / "
    "non-record-dict field boundary tracked in #2317)"
)


_C_RECORD_ARRAY_LEN_MSG = (
    "C cannot represent two record-shaped dicts of one shape whose "
    "shared all-record-list field has differing lengths under the "
    "RECORD heterogeneous strategy: that field becomes a fixed-size "
    "struct RecordN [len] member sized from the shape's first-seen "
    "instance, so a later instance with a different-length list would "
    "overflow the array (excess initializers fail to compile) or "
    "silently under-fill it -- neither faithfully represents the input "
    "(cf. the set / non-record-dict field boundary tracked in #2317)"
)


@beartype
def _check_c_record_array_field_lengths(
    *,
    node: dict[Scalar, Value],
    array_lengths_by_shape: dict[tuple[Scalar, ...], dict[Scalar, int]],
) -> None:
    """Raise :class:`UnrepresentableInputError` if a record-shaped dict
    shares a shape with an earlier one but its all-record-list field
    has a different length.

    An all-record-list record field becomes a fixed-size
    ``struct RecordN[len]`` member sized from the shape's first-seen
    instance (``record_strategy`` caches the first-seen field-type
    request per shape, in document order).  A later same-shape instance
    whose list has a different length would overflow that fixed array
    (excess initializers fail to compile) or silently under-fill it, so
    neither faithfully represents the data.  Rejecting it here keeps
    the boundary explicit rather than emitting C that fails to compile
    or misrepresents the input (cf. the set / non-record-dict field
    boundary tracked in #2317).

    A shape is keyed by its ordered key tuple: C does not unify record
    shapes, so identical-keyed dicts (and only those) share one
    generated ``struct``, exactly as
    :func:`literalizer._formatters.type_inference.record_shape_for_dict`
    deduces.  *array_lengths_by_shape* accumulates the first-seen
    length per shape and field across the whole walk.
    """
    field_lengths = array_lengths_by_shape.setdefault(tuple(node), {})
    for field_name, field_value in node.items():
        if isinstance(field_value, list) and _all_record_shaped(field_value):
            first_length = field_lengths.setdefault(
                field_name,
                len(field_value),
            )
            if first_length != len(field_value):
                raise UnrepresentableInputError(_C_RECORD_ARRAY_LEN_MSG)


@beartype
def _check_c_record_nesting(  # noqa: C901
    *,
    node: Value,
    cval_context: bool,
    array_lengths_by_shape: dict[tuple[Scalar, ...], dict[Scalar, int]],
) -> None:
    """Raise :class:`UnrepresentableInputError` if a record-shaped dict
    (or an all-record list) is reachable only through a ``CVal``
    context.

    Under C's ``RECORD`` strategy a record-shaped dict renders as a
    ``(struct RecordN){...}`` literal and a list whose elements are all
    record-shaped dicts as a ``struct RecordN[]`` array; neither is a
    ``CVal`` union member.  Either is therefore representable only as a
    record-field value, an element of such a field's struct array, or
    the document root.  *cval_context* is ``True`` once the walk has
    descended through a non-record container, where the value must
    occupy a ``CVal`` slot and a record there cannot be represented.
    """
    # pylint: disable=too-complex
    if _c_record_dict(node):
        if cval_context:
            raise UnrepresentableInputError(_C_RECORD_IN_CVAL_MSG)
        _check_c_record_array_field_lengths(
            node=node,
            array_lengths_by_shape=array_lengths_by_shape,
        )
        for field_value in node.values():
            _check_c_record_field(
                field_value,
                array_lengths_by_shape=array_lengths_by_shape,
            )
        return
    match node:
        case OrderedMap() | dict():
            for value in node.values():
                _check_c_record_nesting(
                    node=value,
                    cval_context=True,
                    array_lengths_by_shape=array_lengths_by_shape,
                )
        case list() if _all_record_shaped(node):
            if cval_context:
                raise UnrepresentableInputError(_C_RECORD_IN_CVAL_MSG)
            for element in node:
                _check_c_record_nesting(
                    node=element,
                    cval_context=False,
                    array_lengths_by_shape=array_lengths_by_shape,
                )
        case list():
            for element in node:
                _check_c_record_nesting(
                    node=element,
                    cval_context=True,
                    array_lengths_by_shape=array_lengths_by_shape,
                )
        case _:
            return


@beartype
def _check_c_record_field(
    field_value: Value,
    /,
    *,
    array_lengths_by_shape: dict[tuple[Scalar, ...], dict[Scalar, int]],
) -> None:
    """Validate one field value of a record-shaped dict.

    A nested record dict stays a ``struct`` member and an all-record
    list a ``struct`` array (neither a ``CVal``), so those descend
    without entering a ``CVal`` context.  Every other field value is a
    ``CVal`` slot.  *array_lengths_by_shape* is threaded through so the
    walk can reject same-shape records whose shared all-record-list
    field has differing lengths.
    """
    if _c_record_dict(field_value):
        _check_c_record_nesting(
            node=field_value,
            cval_context=False,
            array_lengths_by_shape=array_lengths_by_shape,
        )
    elif isinstance(field_value, list) and _all_record_shaped(field_value):
        for element in field_value:
            _check_c_record_nesting(
                node=element,
                cval_context=False,
                array_lengths_by_shape=array_lengths_by_shape,
            )
    else:
        _check_c_record_nesting(
            node=field_value,
            cval_context=True,
            array_lengths_by_shape=array_lengths_by_shape,
        )


@beartype
def _c_render_record_declaration(
    name: str,
    fields: Sequence[RecordDeclarationField],
    /,
) -> str:
    """Render a C aggregate ``struct`` declaration block.

    A pointer type abuts its identifier (the type already ends in
    ``*``); a fixed-size record-array field carries its dimension after
    the identifier (the type ends in a bracketed length); every other
    type takes a single separating space.
    """
    members: list[str] = []
    for field in fields:
        type_name = field.type_name
        if type_name.endswith("]"):
            base, _, dimension = type_name.partition(" [")
            members.append(f"{base} {field.identifier}[{dimension};")
        elif type_name.endswith("*"):
            members.append(f"{type_name}{field.identifier};")
        else:
            members.append(f"{type_name} {field.identifier};")
    return f"struct {name} {{ {' '.join(members)} }};"


@beartype
def _c_record_literal(
    name: str,
    fields: Sequence[RecordLiteralField],
    /,
) -> RenderedRecordLiteral:
    """Render a C designated-initializer compound literal ``(struct
    Name){.field = value, ...}`` as structured pieces for the shared
    compact/multiline layout code.

    The shared strategy iterates the shape's keys in document order for
    both the declaration and the literal, so designated initializers
    appear in declaration order.  A trailing comma after the last
    initializer is valid in a brace-enclosed initializer list, so the
    language-wide trailing-comma config applies unchanged.
    """
    return RenderedRecordLiteral(
        head=f"(struct {name}){{",
        entries=tuple(
            f".{field.identifier} = {field.formatted}" for field in fields
        ),
        closer="}",
        compact_pad="",
    )


# Maximum parameter count of any existing call case; stubs above this
# get a ``// NOLINTNEXTLINE`` for ``bugprone-easily-swappable-parameters``.
_SWAPPABLE_PARAMS_NOLINT_THRESHOLD = 4


@beartype
def _c_call_stub(
    parts: Sequence[str],
    params: Sequence[str],
    stub_return: StubReturn,
    _args: Sequence[Value],
    /,
) -> tuple[str, ...]:
    """Return C stub declarations for a call name.

    C has no member functions and no type-generic function templates,
    so dotted targets are modeled as a nested chain of ``struct`` types
    whose leaf field is a function pointer.  Each prototype declares
    one ``CVal`` parameter per call argument so call sites pass values
    through the union-typed wrapper defined in the static preamble; this
    avoids the K&R unspecified-parameter syntax (and the
    ``-Wdeprecated-non-prototype`` clang warning it triggers) while
    still letting the same stub accept any mix of argument types.

    Single-name calls emit a ``static`` definition so the fixture links
    under the lint workflow's run step — a bare prototype without a body
    would otherwise fail at link time.
    """
    is_value = stub_return is StubReturn.VALUE
    return_keyword = "CVal" if is_value else "void"
    proto = ", ".join(["CVal"] * len(params)) if params else "void"
    stub_params = ", ".join(f"CVal _a{i}" for i in range(len(params)))
    stub_signature = stub_params or "void"
    discards = "".join(f" (void)_a{i};" for i in range(len(params)))
    return_stmt = " return (CVal){0};" if is_value else ""
    has_body = discards or is_value
    stub_body = f"{{{discards}{return_stmt} }}" if has_body else "{}"
    # Long uniform-typed parameter lists trip clang-tidy's
    # ``bugprone-easily-swappable-parameters`` check past its
    # name-suffix-dissimilarity silencing heuristic.  The stub is
    # generated, so the warning is not actionable.  Suppress it on
    # stubs whose parameter count exceeds anything the existing call
    # cases use, to avoid touching shorter-stub golden files.
    nolint = (
        ("// NOLINTNEXTLINE(bugprone-easily-swappable-parameters)",)
        if len(params) > _SWAPPABLE_PARAMS_NOLINT_THRESHOLD
        else ()
    )
    match parts:
        case [single]:
            return (
                *nolint,
                f"static {return_keyword} {single}({stub_signature}) "
                f"{stub_body}",
            )
        case [root, method]:
            stub_fn = f"{root}_{method}_stub_"
            type_name = f"{root}Type_"
            return (
                *nolint,
                f"static {return_keyword} {stub_fn}({stub_signature}) "
                f"{stub_body}",
                f"struct {type_name} "
                f"{{ {return_keyword} (*{method})({proto}); }};",
                f"static const struct {type_name} {root} = "
                f"{{ .{method} = {stub_fn} }};",
            )
        case _:
            pass
    root = parts[0]
    method = parts[-1]
    fields = parts[1:-1]
    stub_fn = "_".join((*parts, "stub_"))
    lines: list[str] = [
        *nolint,
        f"static {return_keyword} {stub_fn}({stub_signature}) {stub_body}",
    ]
    inner_type = f"{fields[-1]}Type_"
    lines.append(
        f"struct {inner_type} {{ {return_keyword} (*{method})({proto}); }};",
    )
    prev_type = inner_type
    for i in range(len(fields) - 2, -1, -1):
        curr_type = f"{fields[i]}Type_"
        lines.append(
            f"struct {curr_type} {{ struct {prev_type} {fields[i + 1]}; }};",
        )
        prev_type = curr_type
    root_type = f"{root}Type_"
    lines.append(
        f"struct {root_type} {{ struct {prev_type} {fields[0]}; }};",
    )
    init = f"{{ .{method} = {stub_fn} }}"
    for field in reversed(fields):
        init = f"{{ .{field} = {init} }}"
    lines.append(f"static const struct {root_type} {root} = {init};")
    return tuple(lines)


@beartype
def _format_c_cjson_call_declaration(
    name: str,
    value: str,
    _data: Value,
    _modifiers: frozenset[enum.Enum],
) -> str:
    """Format a cJSON declaration binding a call result.

    A call returns a freshly-constructed ``cJSON *`` node directly, so
    the binding is a plain pointer declaration with no node-building
    statements.
    """
    return f"cJSON *{name} = {value};"


@beartype
def _format_c_call_declaration(
    name: str,
    value: str,
    _data: Value,
    _modifiers: frozenset[enum.Enum],
) -> str:
    """Format a C declaration binding a call result.

    A literal binding wraps the right-hand side in a designated-
    initializer compound literal that encodes the value's runtime type:
    a tagged-union projection for the default strategy, or
    ``struct Record0 my_data = (struct Record0){...};`` under the
    ``RECORD`` strategy.  That is wrong for a call, whose return type is
    opaque to the renderer and is neither a union-field projection nor a
    generated ``struct``.

    C has no type inference, so the binding still needs an explicit
    declared type.  No caller-supplied return-type hint is required:
    every generated call stub returns the universal tagged ``CVal``
    union (a ``StubReturn.VALUE`` stub returns ``CVal``), so the call
    result's static type is always ``CVal`` -- exactly the type a C
    literal binding already declares.  The only call-vs-literal
    difference is dropping the value-wrapping compound literal, so the
    call result is bound directly with a plain ``CVal`` declaration.
    """
    return f"CVal {name} = {value};"


@beartype
def _format_c_call_assignment(name: str, value: str, _data: Value) -> str:
    """Format a C reassignment binding a call result.

    The call-expression counterpart of :func:`_format_c_call_declaration`;
    the variable is already declared ``CVal``, so the call result is
    assigned directly with no compound-literal wrapping.
    """
    return f"{name} = {value};"


_CJSON_STATIC_PREAMBLE: tuple[str, ...] = ("#include <cjson/cJSON.h>",)


@beartype
def _c_cjson_call_stub(
    parts: Sequence[str],
    params: Sequence[str],
    stub_return: StubReturn,
    _args: Sequence[Value],
    /,
) -> tuple[str, ...]:
    """Return cJSON-mode C stub declarations for a call name.

    The cJSON-mode counterpart of :func:`_c_call_stub`: every parameter
    and value-returning return type is ``cJSON *`` instead of the
    tagged ``CVal`` union, and a value-returning stub returns ``NULL``
    rather than a zero-initialised ``CVal`` literal.
    """
    # pylint: disable=too-complex,too-many-branches
    is_value = stub_return is StubReturn.VALUE
    return_keyword = "cJSON *" if is_value else "void "
    proto = ", ".join(["cJSON *"] * len(params)) if params else "void"
    stub_params = ", ".join(f"cJSON *_a{i}" for i in range(len(params)))
    stub_signature = stub_params or "void"
    discards = "".join(f" (void)_a{i};" for i in range(len(params)))
    return_stmt = " return NULL;" if is_value else ""
    has_body = discards or is_value
    stub_body = f"{{{discards}{return_stmt} }}" if has_body else "{}"
    nolint = (
        ("// NOLINTNEXTLINE(bugprone-easily-swappable-parameters)",)
        if len(params) > _SWAPPABLE_PARAMS_NOLINT_THRESHOLD
        else ()
    )
    match parts:
        case [single]:
            return (
                *nolint,
                f"static {return_keyword}{single}({stub_signature}) "
                f"{stub_body}",
            )
        case [root, method]:
            stub_fn = f"{root}_{method}_stub_"
            type_name = f"{root}Type_"
            return (
                *nolint,
                f"static {return_keyword}{stub_fn}({stub_signature}) "
                f"{stub_body}",
                f"struct {type_name} "
                f"{{ {return_keyword}(*{method})({proto}); }};",
                f"static const struct {type_name} {root} = "
                f"{{ .{method} = {stub_fn} }};",
            )
        case _:
            pass
    root = parts[0]
    method = parts[-1]
    fields = parts[1:-1]
    stub_fn = "_".join((*parts, "stub_"))
    lines: list[str] = [
        *nolint,
        f"static {return_keyword}{stub_fn}({stub_signature}) {stub_body}",
    ]
    inner_type = f"{fields[-1]}Type_"
    lines.append(
        f"struct {inner_type} {{ {return_keyword}(*{method})({proto}); }};",
    )
    prev_type = inner_type
    for i in range(len(fields) - 2, -1, -1):
        curr_type = f"{fields[i]}Type_"
        lines.append(
            f"struct {curr_type} {{ struct {prev_type} {fields[i + 1]}; }};",
        )
        prev_type = curr_type
    root_type = f"{root}Type_"
    lines.append(
        f"struct {root_type} {{ struct {prev_type} {fields[0]}; }};",
    )
    init = f"{{ .{method} = {stub_fn} }}"
    for field in reversed(fields):
        init = f"{{ .{field} = {init} }}"
    lines.append(f"static const struct {root_type} {root} = {init};")
    return tuple(lines)


@beartype
@dataclasses.dataclass(frozen=True)
class _CjsonRender:
    """Multi-statement cJSON build plus the rendered right-hand side.

    *build_statements* are emitted into the function body before the
    binding line; *binding_rhs* is the C expression that yields the
    root ``cJSON *``.  The build always names the root ``_n0`` (every
    other temporary uses the same ``_n<N>`` zero-padded numbering) so
    that ``compute_body_preamble`` and ``format_variable_declaration``
    can recompute the same plan from the same data without sharing
    state.
    """

    build_statements: tuple[str, ...]
    binding_rhs: str


@beartype
def _cjson_format_scalar(  # noqa: C901, PLR0911
    *,
    value: Value,
    format_integer: Callable[[int], str],
    format_float: Callable[[float], str],
    format_string: Callable[[str], str],
    format_bytes: Callable[[bytes], str],
    format_date: Callable[[datetime.date], str],
    format_datetime: Callable[[datetime.datetime], str],
    format_time: Callable[[datetime.time], str],
    datetime_epoch: bool,
) -> str:
    """Return the ``cJSON_Create*`` expression for one scalar."""
    # pylint: disable=too-many-return-statements,too-complex
    match value:
        case bool():
            return f"cJSON_CreateBool({1 if value else 0})"
        case None:
            return "cJSON_CreateNull()"
        case int():
            return f"cJSON_CreateNumber((double){format_integer(value)})"
        case float():
            return f"cJSON_CreateNumber({format_float(value)})"
        case str():
            return f"cJSON_CreateString({format_string(value)})"
        case bytes():
            return f"cJSON_CreateString({format_bytes(value)})"
        case datetime.datetime() if datetime_epoch:
            return f"cJSON_CreateNumber((double){format_datetime(value)})"
        case datetime.datetime():
            return f"cJSON_CreateString({format_datetime(value)})"
        case datetime.date():
            return f"cJSON_CreateString({format_date(value)})"
        case datetime.time():
            return f"cJSON_CreateString({format_time(value)})"
        case _:
            msg = (
                "C(json_type=CJSON) cannot represent value of type "
                f"{type(value).__name__}"
            )
            raise UnrepresentableInputError(msg)


@beartype
def _cjson_walk(
    *,
    node: Value,
    statements: list[str],
    counter: list[int],
    name_prefix: str,
    format_integer: Callable[[int], str],
    format_float: Callable[[float], str],
    format_string: Callable[[str], str],
    format_bytes: Callable[[bytes], str],
    format_date: Callable[[datetime.date], str],
    format_datetime: Callable[[datetime.datetime], str],
    format_time: Callable[[datetime.time], str],
    datetime_epoch: bool,
) -> str:
    """Walk *node* recursively, emitting cJSON build statements.

    Returns the name of the temporary holding the rendered node.  A
    scalar gets its own ``_nN`` temporary so the binding always
    references ``_n0`` regardless of root shape.
    """
    name = f"{name_prefix}{counter[0]}"
    counter[0] += 1
    match node:
        case dict():
            statements.append(f"cJSON *{name} = cJSON_CreateObject();")
            for key, val in node.items():
                if not isinstance(key, str):
                    msg = (
                        "C(json_type=CJSON) can only represent dict keys "
                        f"as strings, not {type(key).__name__}"
                    )
                    raise UnrepresentableInputError(msg)
                child = _cjson_walk(
                    node=val,
                    statements=statements,
                    counter=counter,
                    name_prefix=name_prefix,
                    format_integer=format_integer,
                    format_float=format_float,
                    format_string=format_string,
                    format_bytes=format_bytes,
                    format_date=format_date,
                    format_datetime=format_datetime,
                    format_time=format_time,
                    datetime_epoch=datetime_epoch,
                )
                statements.append(
                    f"cJSON_AddItemToObject({name}, "
                    f"{format_string(key)}, {child});"
                )
        case list() | set():
            statements.append(f"cJSON *{name} = cJSON_CreateArray();")
            items: list[Value] = (
                sorted(node, key=lambda v: (type(v).__name__, repr(v)))
                if isinstance(node, set)
                else list(node)
            )
            for item in items:
                child = _cjson_walk(
                    node=item,
                    statements=statements,
                    counter=counter,
                    name_prefix=name_prefix,
                    format_integer=format_integer,
                    format_float=format_float,
                    format_string=format_string,
                    format_bytes=format_bytes,
                    format_date=format_date,
                    format_datetime=format_datetime,
                    format_time=format_time,
                    datetime_epoch=datetime_epoch,
                )
                statements.append(f"cJSON_AddItemToArray({name}, {child});")
        case _:
            expr = _cjson_format_scalar(
                value=node,
                format_integer=format_integer,
                format_float=format_float,
                format_string=format_string,
                format_bytes=format_bytes,
                format_date=format_date,
                format_datetime=format_datetime,
                format_time=format_time,
                datetime_epoch=datetime_epoch,
            )
            statements.append(f"cJSON *{name} = {expr};")
    return name


@beartype
def _build_cjson_render(
    *,
    data: Value,
    format_integer: Callable[[int], str],
    format_float: Callable[[float], str],
    format_string: Callable[[str], str],
    format_bytes: Callable[[bytes], str],
    format_date: Callable[[datetime.date], str],
    format_datetime: Callable[[datetime.datetime], str],
    format_time: Callable[[datetime.time], str],
    datetime_epoch: bool,
    name_prefix: str,
) -> _CjsonRender:
    """Build the cJSON statement plan for *data*.

    Empty containers and bare scalars collapse to a single build
    statement that binds directly; nothing about the binding line
    needs to differ.  The *name_prefix* lets callers pick distinct
    temporary names so a combined declaration + reassignment in one
    function body does not collide.
    """
    statements: list[str] = []
    counter = [0]
    _cjson_walk(
        node=data,
        statements=statements,
        counter=counter,
        name_prefix=name_prefix,
        format_integer=format_integer,
        format_float=format_float,
        format_string=format_string,
        format_bytes=format_bytes,
        format_date=format_date,
        format_datetime=format_datetime,
        format_time=format_time,
        datetime_epoch=datetime_epoch,
    )
    return _CjsonRender(
        build_statements=tuple(statements),
        binding_rhs=f"{name_prefix}0",
    )


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class C(metaclass=LanguageCls):
    """C language specification."""

    format_integer_widened = no_format_integer_widened
    format_constructor_target: ClassVar["staticmethod[[str], str]"] = (
        staticmethod(identity_constructor_target)
    )
    sequence_binding_declarations = default_sequence_binding_declarations
    format_call_binding_body_preamble = no_call_binding_body_preamble
    format_call_binding_file_pragmas = no_call_binding_file_pragmas

    module_name: str = "Module"

    leading_preamble = no_leading_preamble
    extension = ".c"
    pygments_name = "c"
    supports_special_floats = True
    supports_variable_names = True
    supports_no_variable_wrap_in_file = False
    dict_supports_heterogeneous_values = True
    supports_dotted_calls = True
    has_free_function_calls = True
    reserved_identifiers: ClassVar[frozenset[str]] = frozenset()
    allows_empty_call_parens = True
    supports_dotted_call_stub = True
    call_returns_expression = True
    supports_zero_parameter_calls = True
    max_call_parameters = NO_CALL_PARAMETER_LIMIT
    supports_inline_multiline_dict_args = True
    supports_standalone_comments_in_wrapped_calls = True
    supports_multi_param_call_wrapper_stub = True
    supports_dict_literal_as_free_expression = True
    supports_module_name = True
    supports_empty_dict_key = False
    supports_call_style = True
    supports_default_dict_key_type = False
    supports_default_dict_value_type = False
    supports_default_sequence_element_type = False
    supports_default_set_element_type = False
    supports_default_ordered_map_value_type = False
    supports_record_struct_name_prefix = False
    supports_record_shape_names = False
    supports_non_string_dict_keys = False

    class DateFormats(enum.Enum):
        """Date format options for C."""

        ISO = DateFormatConfig(formatter=format_date_iso, type_produced=str)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for C."""

        ISO = DatetimeFormatConfig(
            formatter=format_datetime_iso,
            type_produced=str,
        )

        EPOCH = DatetimeFormatConfig(
            formatter=format_datetime_epoch,
            type_produced=int,
        )

        def __call__(self, dt_value: datetime.datetime, /) -> str:
            """Format a datetime."""
            return self.value.formatter(dt_value)

    class BytesFormats(enum.Enum):
        """Bytes formatting options."""

        HEX = enum.member(value=format_bytes_hex)
        BASE64 = enum.member(value=format_bytes_base64)

        def __call__(self, data: bytes, /) -> str:
            """Format bytes."""
            return self.value(value=data)

    class SequenceFormats(enum.Enum):
        """Sequence type options for C."""

        ARRAY = SequenceFormatConfig(
            sequence_open=fixed_open(
                open_str="((CVal){.a = (CVal[]){",
            ),
            close="}})",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            supports_trailing_comma=True,
            empty_sequence=None,
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback=None,
            uses_typed_literal_for_scalars=False,
            requires_uniform_record_shapes=False,
            declared_type=None,
            narrowed_empty_form=None,
        )

    class SetFormats(enum.Enum):
        """Set type options for C."""

        SET = SetFormatConfig(
            set_open=fixed_open(open_str="((CVal){.a = (CVal[]){"),
            close="}})",
            empty_set=None,
            preamble_lines=(),
            set_opener_template="",
            supports_heterogeneity=True,
            supports_trailing_comma=True,
        )

    class CommentFormats(enum.Enum):
        """Comment style options."""

        DOUBLE_SLASH = CommentConfig(
            prefix="//",
            suffix="",
        )
        BLOCK = CommentConfig(
            prefix="/*",
            suffix=" */",
        )

    class DeclarationStyles(enum.Enum):
        """Declaration style options."""

        TYPED = DeclarationStyleConfig(
            formatter=variable_declaration_formatter(
                template="CVal {name} = {value};",
            ),
            supports_redefinition=True,
        )

    class DictEntryStyles(enum.Enum):
        """Dict entry style options."""

        DEFAULT = enum.auto()

    class DictFormats(enum.Enum):
        """Dict/map format options."""

        DEFAULT = enum.auto()

    class EmptyDictKey(enum.Enum):
        """Empty dict key options."""

        ALLOW = enum.auto()

    class FloatFormats(
        FloatSpecialsMixin,
        enum.Enum,
        positive_infinity="INFINITY",
        negative_infinity="-INFINITY",
        nan="NAN",
    ):
        """Float format options."""

        REPR = enum.member(value=format_float_repr)
        SCIENTIFIC = enum.member(value=format_float_scientific)
        FIXED = enum.member(value=format_float_fixed)

    class IntegerFormats(enum.Enum):
        """Integer format options."""

        DECIMAL = enum.member(value=str)
        HEX = enum.member(value=format_integer_hex)

        def __call__(self, value: int, /) -> str:
            """Format an integer."""
            formatter: Callable[[int], str] = self.value
            return formatter(value)

    class NumericLiteralSuffixes(enum.Enum):
        """Numeric literal suffix options."""

        NONE = enum.auto()
        AUTO = enum.auto()

    class NumericSeparators(enum.Enum):
        """Numeric separator options."""

        NONE = enum.auto()

    class NumericStyles(enum.Enum):
        """Numeric literal style options."""

        OVERLOADED = enum.auto()

    class StringFormats(enum.Enum):
        """String format options."""

        DOUBLE = enum.auto()

    class TrailingCommas(enum.Enum):
        """Trailing comma options."""

        YES = TrailingCommaConfig(multiline_trailing_comma=True)
        NO = TrailingCommaConfig(multiline_trailing_comma=False)

    date_formats = DateFormats
    datetime_formats = DatetimeFormats
    bytes_formats = BytesFormats
    sequence_formats = SequenceFormats
    set_formats = SetFormats
    comment_formats = CommentFormats

    class VariableTypeHints(enum.Enum):
        """Variable type hint options."""

        NEVER = enum.auto()
        SAFE = enum.auto()

    variable_type_hints_formats = VariableTypeHints
    declaration_styles = DeclarationStyles
    dict_entry_styles = DictEntryStyles
    dict_formats = DictFormats
    empty_dict_keys = EmptyDictKey
    float_formats = FloatFormats
    integer_formats = IntegerFormats
    integer_width_strategies = BareIntegerWidthStrategies
    numeric_literal_suffixes = NumericLiteralSuffixes
    numeric_separators = NumericSeparators
    numeric_styles = NumericStyles
    string_formats = StringFormats
    trailing_commas = TrailingCommas

    class StatementTerminatorStyles(enum.Enum):
        """Statement terminator options."""

        SEMICOLON = enum.auto()

    statement_terminator_styles = StatementTerminatorStyles

    class CallStyles(enum.Enum):
        """C call style options."""

        POSITIONAL = PositionalCallStyle(
            arg_separator=", ", parenthesize_each_arg=False
        )

    call_styles = CallStyles

    class Modifiers(enum.Enum):
        """C++/Java/C#-style declaration modifiers: this language has none."""

    modifiers = Modifiers

    class HeterogeneousStrategies(enum.Enum):
        """Heterogeneous-scalar strategy options.

        C represents heterogeneous scalar collections with its tagged
        ``CVal`` union by default (``ERROR``).  ``RECORD`` instead
        renders each record-shaped dict (non-empty, string-keyed) as a
        generated aggregate ``struct`` declared in the preamble plus a
        matching ``(struct Record0){.field = value, ...}``
        designated-initializer compound literal, so a field may be a
        cleanly-typed scalar or a nested ``struct`` rather than a
        ``CVal`` union slot.
        """

        ERROR = enum.auto()
        RECORD = enum.auto()

    heterogeneous_strategies = HeterogeneousStrategies

    class JsonTypes(enum.Enum):
        """JSON value type options for C."""

        CJSON = "cJSON *"
        """The ``cJSON`` dynamic JSON value type from the
        ``cjson/cJSON.h`` library.  Every node is constructed
        explicitly via ``cJSON_Create*`` calls and assembled with
        ``cJSON_AddItemToObject`` / ``cJSON_AddItemToArray``; the
        binding type is ``cJSON *``.
        """

    json_types = JsonTypes

    class BoolFormats(enum.Enum):
        """Empty: this language has no alternative boolean formats."""

    bool_formats = BoolFormats

    class VersionFormats(enum.Enum):
        """Version options for C."""

        C99 = enum.auto()

    version_formats = VersionFormats

    module_name_case: ClassVar[IdentifierCase] = IdentifierCase.SNAKE
    modifier_combinations: ClassVar[tuple[ModifierCombination, ...]] = ()
    identifier_cases: ClassVar[tuple[IdentifierCase, ...]] = (
        IdentifierCase.SNAKE,
        IdentifierCase.UPPER_SNAKE,
        IdentifierCase.PASCAL,
    )
    supported_ref_cases: ClassVar[frozenset[IdentifierCase]] = (
        NON_KEBAB_REF_CASES
    )

    def __post_init__(self) -> None:
        """Reject ``json_type`` combinations the generator cannot emit."""
        self._validate_json_type_spec()

    def _validate_json_type_spec(self) -> None:
        """Reject ``json_type`` combinations the generator cannot emit.

        Under :attr:`json_type` the rendered data flows through cJSON
        node-construction calls.  The ``RECORD`` heterogeneous
        strategy generates ``struct`` declarations whose literals do
        not correspond to any cJSON node type, so the two cannot be
        combined in the first slice.
        """
        if not self._json_type_active:
            return
        if self.heterogeneous_strategy.name == "RECORD":
            msg = (
                "C json_type renders data through cJSON node "
                "construction calls and is incompatible with "
                "heterogeneous_strategy=RECORD, which generates "
                "struct declarations. Use heterogeneous_strategy=ERROR."
            )
            raise IncompatibleFormatsError(msg)

    def validate_spec_for_data(self, data: Value) -> None:
        """Raise if the spec cannot produce valid C for *data*.

        Under the ``RECORD`` strategy a record-shaped dict renders as a
        ``(struct RecordN){...}`` literal (and a list whose elements are
        all record-shaped dicts as a ``struct RecordN[]`` array); a
        ``struct`` is not a ``CVal`` union member, so a record reachable
        only through a non-record container would have to occupy a
        ``CVal`` slot and cannot compile.  The same walk rejects two
        same-shape records whose shared all-record-list field has
        differing lengths (the field's fixed-size ``struct`` array is
        sized from the first-seen instance).  Rejecting here keeps the
        boundary explicit rather than emitting C that fails to build
        (cf. the set / non-record-dict field boundary tracked in
        #2317).  The default (``ERROR``) strategy is unconstrained.
        """
        if self._record_strategy_active:
            _check_c_record_nesting(
                node=data,
                cval_context=False,
                array_lengths_by_shape={},
            )

    @cached_property
    def validate_call_arg(self) -> Callable[[Value], None]:
        """Return call-argument validation for this language."""
        return no_validate_call_arg

    @cached_property
    def format_call_statement(self) -> Callable[[str], str]:
        """Return call-statement formatting for this language."""
        return identity_call_statement

    wrap_calls_with_declarations = default_wrap_calls_with_declarations

    def wrap_in_file(
        self,
        content: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap a C declaration in a main function."""
        content = prepend_body_preamble(
            content=content,
            body_preamble=body_preamble,
        )
        use_line = (
            f"\n{self.indent}(void){variable_name};" if variable_name else ""
        )
        return (
            f"int {self.module_name}(void) {{\n{content}{use_line}\n"
            f"{self.indent}return 0;\n}}"
        )

    def wrap_combined_in_file(
        self,
        declaration: str,
        assignment: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap C declaration + assignment in a function.

        Reads ``variable_name`` between the declaration and the
        assignment so the initial value is not a dead store flagged by
        clang-tidy's ``clang-analyzer-deadcode.DeadStores`` check.
        """
        mid_use = f"(void){variable_name};\n"
        return self.wrap_in_file(
            content=f"{declaration}\n{mid_use}{assignment}",
            variable_name=variable_name,
            body_preamble=body_preamble,
        )

    date_format: DateFormats = DateFormats.ISO
    datetime_format: DatetimeFormats = DatetimeFormats.ISO
    bytes_format: BytesFormats = BytesFormats.HEX
    sequence_format: SequenceFormats = SequenceFormats.ARRAY
    set_format: SetFormats = SetFormats.SET
    variable_type_hints: VariableTypeHints = VariableTypeHints.NEVER
    comment_format: CommentFormats = CommentFormats.DOUBLE_SLASH
    declaration_style: DeclarationStyles = DeclarationStyles.TYPED
    dict_entry_style: DictEntryStyles = DictEntryStyles.DEFAULT
    dict_format: DictFormats = DictFormats.DEFAULT
    float_format: FloatFormats = FloatFormats.REPR
    integer_format: IntegerFormats = IntegerFormats.DECIMAL
    integer_width_strategy: BareIntegerWidthStrategies = (
        BareIntegerWidthStrategies.BARE
    )
    numeric_literal_suffix: NumericLiteralSuffixes = (
        NumericLiteralSuffixes.NONE
    )
    numeric_separator: NumericSeparators = NumericSeparators.NONE
    numeric_style: NumericStyles = NumericStyles.OVERLOADED
    string_format: StringFormats = StringFormats.DOUBLE
    trailing_comma: TrailingCommas = TrailingCommas.YES
    statement_terminator_style: StatementTerminatorStyles = (
        StatementTerminatorStyles.SEMICOLON
    )
    heterogeneous_strategy: HeterogeneousStrategies = (
        HeterogeneousStrategies.ERROR
    )
    json_type: JsonTypes | None = None
    # Keep in sync with the ``-std=`` flag passed to clang and clang-tidy
    # in ``.github/workflows/lint.yml``.
    language_version: VersionFormats = VersionFormats.C99
    indent: str = "    "
    bool_field: str = "b"
    int_field: str = "i"
    uint_field: str = "u"
    float_field: str = "f"
    string_field: str = "s"
    array_field: str = "a"
    map_field: str = "m"
    key_field: str = "k"
    value_field: str = "v"

    indent_closing_delimiter: ClassVar[bool] = False
    element_separator: ClassVar[str] = ", "
    skip_null_dict_values: ClassVar[bool] = False
    supports_collection_comments: ClassVar[bool] = True
    supports_scalar_before_comments: ClassVar[bool] = True
    supports_scalar_inline_comments: ClassVar[bool] = False
    statement_terminator: ClassVar[str] = ";"
    static_body_preamble: ClassVar[Sequence[str]] = ()
    special_float_preamble: ClassVar[tuple[str, ...]] = ("#include <math.h>",)
    call_style: CallStyles = CallStyles.POSITIONAL

    @cached_property
    def call_style_config(self) -> PositionalCallStyle:
        """Configuration for the chosen call style."""
        return self.call_style.value

    @cached_property
    def _record_strategy_active(self) -> bool:
        """Return whether the ``RECORD`` heterogeneous strategy is set."""
        return self.heterogeneous_strategy.name == "RECORD"

    @cached_property
    def _json_type_active(self) -> bool:
        """Return whether C should render via the ``cJSON`` API."""
        return self.json_type is not None

    def _c_record_field_type(  # noqa: C901, PLR0911
        self,
        request: RecordFieldType,
        /,
    ) -> str:
        """Return the C ``struct`` member type for one record field.

        A field whose value is itself a nested record-shaped dict uses
        that record's generated ``struct`` type.  A field whose value
        is a list whose every element is a record-shaped dict of one
        shared shape becomes a fixed-size ``struct`` array member
        (records are the uniform, exactly-representable container
        case).  Every scalar maps to its exact C type.

        A scalar or heterogeneous list, or an empty list, is typed a
        pointer to ``CVal`` and rendered as a ``CVal`` array literal:
        C's tagged ``CVal`` union already represents arbitrary
        heterogeneity, so reusing it for these fields keeps every
        literal and type pair valid (a fixed-size scalar array would be
        the wrong length when two same-shape records carry
        different-length lists, and is ill-formed -- a zero-length
        array -- for an empty list).  This is the recorded answer to
        the issue's "fixed-size array versus pointer" container-field
        design call.

        A set, an ordered map, or a non-record dict field (out of
        scope for the base port, #2476/#2317) keeps its own
        self-wrapping ``CVal`` form and is typed ``CVal``.
        """
        # pylint: disable=too-complex
        if request.record_name is not None:
            return f"struct {request.record_name}"
        value = request.value
        if request.element_record_name is not None and isinstance(
            value,
            list,
        ):
            return f"struct {request.element_record_name} [{len(value)}]"
        epoch = self.datetime_format.value.type_produced is int
        match value:
            case bool():
                return "bool"
            case int() as int_value if int_value > I64_MAX:
                return "unsigned long long"
            case int():
                return "long long"
            case float():
                return "double"
            case str() | bytes():
                return "const char *"
            case None:
                return "const void *"
            case datetime.datetime():
                return "long long" if epoch else "const char *"
            case datetime.date() | datetime.time():
                return "const char *"
            case list():
                return "const CVal *"
            case _:
                return "CVal"

    @cached_property
    def _record_renderer(self) -> RecordRenderer:
        """C syntax hooks for the ``RECORD`` strategy."""
        return RecordRenderer(
            name_prefix=_C_RECORD_PREFIX,
            record_shape_names=_C_NO_RECORD_SHAPE_NAMES,
            field_identifier=_c_record_field_identifier,
            field_type=self._c_record_field_type,
            render_declaration=_c_render_record_declaration,
            render_literal=_c_record_literal,
        )

    @cached_property
    def _record_strategy(self) -> RecordStrategy:
        """Behavior + ``struct``-declaration preamble for ``RECORD``."""
        return build_record_strategy(renderer=self._record_renderer)

    @cached_property
    def data_dependent_preamble(self) -> Callable[[Value], tuple[str, ...]]:
        """Return data-dependent preamble lines.

        Under ``RECORD`` these are the generated ``struct RecordN``
        declarations, emitted after the static ``CVal`` / ``CKV`` type
        declarations (a record field may itself be ``const CVal *``).
        """
        if self._record_strategy_active:
            return self._record_strategy.preamble
        return no_data_preamble

    @cached_property
    def heterogeneous_behavior(self) -> HeterogeneousBehavior:
        """Return the heterogeneous-behavior config.

        ``RECORD`` resolves to the shared record behavior (its value
        needs the per-instance renderer, so it cannot be stored on the
        enum member); ``ERROR`` keeps the ``CVal``-union default.
        Under :attr:`json_type` the framework's scalar checks are
        skipped because cJSON's dynamic node type accepts any mix of
        scalar types in a container.
        """
        if self._json_type_active:
            return dataclasses.replace(
                NO_HETEROGENEOUS_BEHAVIOR,
                skip_scalar_checks=True,
            )
        if self._record_strategy_active:
            return self._record_strategy.behavior
        return NO_HETEROGENEOUS_BEHAVIOR

    @cached_property
    def call_data_dependent_preamble(
        self,
    ) -> Callable[[Value], tuple[str, ...]]:
        """Return data-dependent preamble lines for call rendering."""
        return self.data_dependent_preamble

    @cached_property
    def type_hint_collection_preamble_lines(
        self,
    ) -> Callable[[frozenset[type]], tuple[str, ...]]:
        """Return preamble lines for empty-collection type hints."""
        return no_type_hint_preamble

    @cached_property
    def format_call_stub(
        self,
    ) -> Callable[
        [Sequence[str], Sequence[str], StubReturn, Sequence[Value]],
        tuple[str, ...],
    ]:
        """Return stub declarations for a call expression."""
        return no_call_stub

    @cached_property
    def format_call_preamble_stub(
        self,
    ) -> Callable[
        [Sequence[str], Sequence[str], StubReturn, Sequence[Value]],
        tuple[str, ...],
    ]:
        """Return file-scope stubs for a call expression.

        Under :attr:`json_type` every parameter is a ``cJSON *`` rather
        than the tagged ``CVal`` union, since call arguments are emitted
        as ``cJSON_Create*`` expressions.
        """
        if self._json_type_active:
            return _c_cjson_call_stub
        return _c_call_stub

    @cached_property
    def format_call_target(self) -> Callable[[Sequence[str]], str]:
        """Rewrite a dotted call target into the language's call
        syntax.
        """
        return identity_call_target

    @cached_property
    def format_call_ref_identifier(
        self,
    ) -> Callable[[str, Value | None], str]:
        """Rewrite a ``{"$ref": "name"}`` identifier into the
        language's call expression syntax.
        """
        return identity_call_ref_identifier

    @cached_property
    def format_call_arg_ref_identifier(
        self,
    ) -> Callable[[str, Value | None], str]:
        """Rewrite a ``{"$ref": "name"}`` identifier in a call-argument
        context.

        Delegates to :attr:`format_call_ref_identifier`.  Override this to
        allow call-argument ``$ref`` values that would otherwise be rejected.
        """
        return self.format_call_ref_identifier

    @cached_property
    def format_call_arg_ref_identifier_consumable(
        self,
    ) -> Callable[[str, Value | None], str]:
        """Format a ``$ref`` the caller authorized as consumable.

        Delegates to :attr:`format_call_arg_ref_identifier`.  Override
        this to opt into a consuming form (e.g. C++ ``std::move``).
        """
        return self.format_call_arg_ref_identifier

    @cached_property
    def consumable_ref_value_inhibits_consuming_form(
        self,
    ) -> Callable[[Value], bool]:
        """Predicate deciding whether a ref's underlying value type
        inhibits the consume form.

        Delegates to :data:`never_inhibits_consuming_form`.  Languages
        whose consume operator rejects certain value types (notably
        the Mojo ``^`` on register-trivial scalars) override this.
        """
        return never_inhibits_consuming_form

    @cached_property
    def format_call_arg(self) -> Callable[[Value, str], str]:
        """Wrap each call argument in the ``CVal`` union so call sites
        match the concrete prototype emitted by :func:`_c_call_stub`.

        Under :attr:`json_type` each scalar call argument is rendered
        as a ``cJSON_Create*`` expression matching the ``cJSON *``
        parameters emitted by :func:`_c_cjson_call_stub`.
        """
        if self._json_type_active:
            return self._cjson_format_call_arg
        return self._format_entry

    @cached_property
    def _cjson_format_call_arg(self) -> Callable[[Value, str], str]:
        """Return the cJSON-mode call-argument formatter."""
        format_integer = self.format_integer
        format_float = self.format_float
        format_string = self.format_string
        format_bytes = self.format_bytes
        format_date = self.format_date
        format_datetime = self.format_datetime
        format_time = self.format_time
        datetime_epoch = self.datetime_format.value.type_produced is int

        @beartype
        def _format(value: Value, _formatted: str) -> str:
            """Render *value* as a ``cJSON_Create*`` expression."""
            return _cjson_format_scalar(
                value=value,
                format_integer=format_integer,
                format_float=format_float,
                format_string=format_string,
                format_bytes=format_bytes,
                format_date=format_date,
                format_datetime=format_datetime,
                format_time=format_time,
                datetime_epoch=datetime_epoch,
            )

        return _format

    @cached_property
    def format_string(self) -> Callable[[str], str]:
        """Format a string value as a quoted literal."""
        return format_string_backslash

    @cached_property
    def _format_entry(self) -> Callable[[Value, str], str]:
        """Shared entry formatter that wraps values in ``CVal``
        literals.

        Under ``RECORD`` the bare ``true`` / ``false`` / ``NULL``
        literals reach this hook unwrapped (so a scalar record field is
        clean), so the ``RECORD`` variant additionally wraps ``bool`` /
        ``None`` and passes a record-shaped dict (already a ``struct``
        literal) through untouched.
        """
        if self._record_strategy_active:
            return _make_format_c_entry_record(
                int_field=self.int_field,
                uint_field=self.uint_field,
                float_field=self.float_field,
                string_field=self.string_field,
                bool_field=self.bool_field,
                array_field=self.array_field,
            )
        return _make_format_c_entry(
            int_field=self.int_field,
            uint_field=self.uint_field,
            float_field=self.float_field,
            string_field=self.string_field,
        )

    @cached_property
    def _seq_open_str(self) -> str:
        """Opening string for a C sequence literal."""
        return f"((CVal){{.{self.array_field} = (CVal[]){{"

    @cached_property
    def _map_open_str(self) -> str:
        """Opening string for a C map literal."""
        return f"((CVal){{.{self.map_field} = (CKV[]){{"

    @cached_property
    def null_literal(self) -> str:
        """Literal representing ``None``.

        Bare ``NULL`` under ``RECORD`` (a clean ``const void *`` record
        field); ``_format_entry`` re-wraps it for ``CVal`` contexts.
        """
        if self._record_strategy_active:
            return "NULL"
        return f"((CVal){{.{self.string_field} = NULL}})"

    @cached_property
    def true_literal(self) -> str:
        """Literal representing ``True``.

        Bare ``true`` under ``RECORD`` (a clean ``bool`` record field);
        ``_format_entry`` re-wraps it for ``CVal`` contexts.
        """
        if self._record_strategy_active:
            return "true"
        return f"((CVal){{.{self.bool_field} = true}})"

    @cached_property
    def false_literal(self) -> str:
        """Literal representing ``False``.

        Bare ``false`` under ``RECORD`` (a clean ``bool`` record
        field); ``_format_entry`` re-wraps it for ``CVal`` contexts.
        """
        if self._record_strategy_active:
            return "false"
        return f"((CVal){{.{self.bool_field} = false}})"

    @cached_property
    def _record_sequence_open(self) -> Callable[[list[Value]], str]:
        """Return the ``RECORD``-strategy sequence opener.

        A list whose every element is a record-shaped dict opens with a
        bare ``{`` -- the enclosing ``struct RecordN`` array member (or
        array variable) supplies the type and the elements are
        ``(struct RecordN){...}`` literals.  Every other list opens with
        ``(CVal[]){`` and closes with ``}`` (the paired close is set on
        the config), reusing C's tagged union for arbitrary
        heterogeneity; ``_format_entry`` wraps each element so the
        compound-literal array is a valid ``const CVal *`` field value.
        """

        def _open(items: list[Value]) -> str:
            """Return the bare-brace or ``(CVal[]){`` opener."""
            if _all_record_shaped(items):
                return "{"
            return "(CVal[]){"

        return _open

    @cached_property
    def sequence_format_config(self) -> SequenceFormatConfig:
        """Configuration for the chosen sequence format.

        Under ``RECORD`` the asymmetric ``((CVal){.a = (CVal[]){`` ...
        ``}})`` wrapper is dropped: every list is a ``(CVal[]){...}`` /
        ``{...}`` initializer closing with a single ``}`` (a record
        field or a ``struct`` array, never a free-standing ``CVal``), so
        the close pairs with :attr:`_record_sequence_open`.
        """
        fmt = self.sequence_format.value
        if self._record_strategy_active:
            return SequenceFormatConfig(
                sequence_open=self._record_sequence_open,
                close="}",
                supports_heterogeneity=fmt.supports_heterogeneity,
                single_element_trailing_comma=(
                    fmt.single_element_trailing_comma
                ),
                supports_trailing_comma=fmt.supports_trailing_comma,
                empty_sequence=fmt.empty_sequence,
                preamble_lines=fmt.preamble_lines,
                format_entry=fmt.format_entry,
                typed_opener_fallback=fmt.typed_opener_fallback,
                uses_typed_literal_for_scalars=(
                    fmt.uses_typed_literal_for_scalars
                ),
                requires_uniform_record_shapes=(
                    fmt.requires_uniform_record_shapes
                ),
                declared_type=fmt.declared_type,
                narrowed_empty_form=None,
            )
        return SequenceFormatConfig(
            sequence_open=fixed_open(open_str=self._seq_open_str),
            close="}})",
            supports_heterogeneity=fmt.supports_heterogeneity,
            single_element_trailing_comma=(fmt.single_element_trailing_comma),
            supports_trailing_comma=fmt.supports_trailing_comma,
            empty_sequence=fmt.empty_sequence,
            preamble_lines=fmt.preamble_lines,
            format_entry=fmt.format_entry,
            typed_opener_fallback=fmt.typed_opener_fallback,
            uses_typed_literal_for_scalars=(
                fmt.uses_typed_literal_for_scalars
            ),
            requires_uniform_record_shapes=(
                fmt.requires_uniform_record_shapes
            ),
            declared_type=fmt.declared_type,
            narrowed_empty_form=None,
        )

    @cached_property
    def set_format_config(self) -> SetFormatConfig:
        """Configuration for the chosen set format."""
        return SetFormatConfig(
            set_open=fixed_open(open_str=self._seq_open_str),
            close="}})",
            empty_set=self.set_format.value.empty_set,
            preamble_lines=self.set_format.value.preamble_lines,
            set_opener_template=self.set_format.value.set_opener_template,
            supports_heterogeneity=self.set_format.value.supports_heterogeneity,
            supports_trailing_comma=True,
        )

    @cached_property
    def sequence_open(self) -> Callable[[list[Value]], str]:
        """Callable that returns the opening delimiter for a sequence."""
        return self.sequence_format_config.sequence_open

    @cached_property
    def dict_format_config(self) -> DictFormatConfig:
        """Configuration for dict formatting."""
        return DictFormatConfig(
            dict_open=fixed_open(open_str=self._map_open_str),
            close="}})",
            format_entry=braced_dict_entry(
                format_value=self._format_entry,
            ),
            empty_dict=None,
            preamble_lines=(),
            narrowed_open=None,
            supports_trailing_comma=True,
        )

    @cached_property
    def trailing_comma_config(self) -> TrailingCommaConfig:
        """Configuration for trailing-comma behavior."""
        return self.trailing_comma.value

    @cached_property
    def format_bytes(self) -> Callable[[bytes], str]:
        """Callable that formats a bytes value as a string literal."""
        return self.bytes_format

    @cached_property
    def format_date(self) -> Callable[[datetime.date], str]:
        """Callable that formats a date as a string literal."""
        return self.date_format

    @cached_property
    def format_datetime(self) -> Callable[[datetime.datetime], str]:
        """Callable that formats a datetime as a string literal."""
        return self.datetime_format

    @cached_property
    def format_time(self) -> Callable[[datetime.time], str]:
        """Callable that formats a time as a string literal."""
        return format_time_iso

    @cached_property
    def format_float(self) -> Callable[[float], str]:
        """Callable that formats a float value as a literal."""
        return self.float_format

    @cached_property
    def format_integer(self) -> Callable[[int], str]:
        """Callable that formats an int value as a literal."""
        suffix_is_auto = self.numeric_literal_suffix.name == "AUTO"
        base: Callable[[int], str] = (
            make_long_suffix_formatter(base=self.integer_format)
            if suffix_is_auto
            else self.integer_format
        )
        return make_overflow_fallback_formatter(
            base=base,
            fallback=make_ull_fallback(language_name="C"),
        )

    @cached_property
    def format_sequence_entry(self) -> Callable[[Value, str], str]:
        """Callable that formats one sequence entry."""
        return self._format_entry

    @cached_property
    def format_set_entry(self) -> Callable[[Value, str], str]:
        """Callable that formats one set entry."""
        return self._format_entry

    @cached_property
    def comment_config(self) -> CommentConfig:
        """Configuration for the language's comment syntax."""
        return self.comment_format.value

    @cached_property
    def ordered_map_format_config(self) -> OrderedMapFormatConfig:
        """Configuration for ordered-map formatting."""
        return OrderedMapFormatConfig(
            ordered_map_open=fixed_open(open_str=self._map_open_str),
            close="}})",
            preamble_lines=(),
        )

    @cached_property
    def format_ordered_map_entry(self) -> Callable[[str, Value, str], str]:
        """Callable that formats one ordered-map entry."""
        return braced_dict_entry(format_value=self._format_entry)

    def _record_binding_lhs(self, data: Value, /) -> str | None:
        """Return the typed left-hand side for a ``RECORD`` top-level
        binding, or ``None`` to fall back to the ``CVal`` form.

        The shared strategy names record shapes in document order with
        no custom names, so the outermost record-shaped dict (or the
        shared element shape of a top-level all-record list) is always
        ``Record0``: a record-shaped root binds ``struct Record0 NAME``
        and an all-record-list root binds ``struct Record0 NAME[]``;
        every other root keeps the ``CVal`` union.
        """
        if not self._record_strategy_active:
            return None
        root = f"struct {_C_RECORD_PREFIX}0"
        if (
            isinstance(data, dict)
            and not isinstance(data, OrderedMap)
            and record_shape_for_dict(value=data) is not None
        ):
            return root
        if isinstance(data, list) and _all_record_shaped(data):
            return f"{root}[]"
        return None

    @cached_property
    def format_variable_declaration(
        self,
    ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
        """Callable that formats a new variable declaration.

        Under ``RECORD`` a record-shaped root is declared with its
        generated ``struct`` type (``struct Record0 my_data = (struct
        Record0){...};``) and an all-record-list root as an array
        (``struct Record0 my_data[] = {...};``); under
        :attr:`json_type` the value is built up by a sequence of
        ``cJSON_Create*`` / ``cJSON_AddItem*`` statements emitted into
        the binding's body, with the binding line declaring
        ``cJSON *NAME = _n0;``; every other value keeps the
        ``CVal``-wrapped form.
        """
        format_entry = self._format_entry
        if self._json_type_active:
            build_render = self._build_cjson_render_for_data

            @beartype
            def _format_cjson_decl(
                name: str,
                _value: str,
                data: Value,
                _modifiers: frozenset[enum.Enum],
            ) -> str:
                """Format a cJSON declaration as build + bind lines."""
                render = build_render(data=data, name_prefix="_n")
                lines = (
                    *render.build_statements,
                    f"cJSON *{name} = {render.binding_rhs};",
                )
                return "\n".join(lines)

            return _format_cjson_decl

        @beartype
        def _format_decl(
            name: str,
            value: str,
            data: Value,
            _modifiers: frozenset[enum.Enum],
        ) -> str:
            """Format a C variable declaration."""
            lhs = self._record_binding_lhs(data)
            if lhs is not None and lhs.endswith("[]"):
                return f"{lhs[:-2]} {name}[] = {value};"
            if lhs is not None:
                return f"{lhs} {name} = {value};"
            wrapped = format_entry(data, value)
            return f"CVal {name} = {wrapped};"

        return _format_decl

    @cached_property
    def format_variable_assignment(
        self,
    ) -> Callable[[str, str, Value], str]:
        """Callable that formats an assignment to an existing variable.

        The combined declaration+assignment form is only exercised for a
        top-level record-shaped dict, so a ``RECORD`` reassignment is a
        plain ``my_data = (struct Record0){...};`` struct copy.  Under
        :attr:`json_type` the assignment builds a fresh cJSON tree under
        a distinct ``_m<N>`` prefix so its temporaries do not collide
        with the declaration's ``_n<N>`` block in the same function
        body, then rebinds ``NAME`` to the new root.
        """
        format_entry = self._format_entry
        if self._json_type_active:
            build_render = self._build_cjson_render_for_data

            @beartype
            def _format_cjson_assign(
                name: str,
                _value: str,
                data: Value,
            ) -> str:
                """Format a cJSON assignment as build + rebind lines."""
                render = build_render(data=data, name_prefix="_m")
                lines = (
                    *render.build_statements,
                    f"{name} = {render.binding_rhs};",
                )
                return "\n".join(lines)

            return _format_cjson_assign

        @beartype
        def _format_assign(name: str, value: str, data: Value) -> str:
            """Format a C variable assignment."""
            lhs = self._record_binding_lhs(data)
            if lhs is not None and not lhs.endswith("[]"):
                return f"{name} = {value};"
            wrapped = format_entry(data, value)
            return f"{name} = {wrapped};"

        return _format_assign

    def _build_cjson_render_for_data(
        self, *, data: Value, name_prefix: str
    ) -> _CjsonRender:
        """Build a cJSON render plan for *data* using this spec's
        scalar formatters.
        """
        datetime_epoch = self.datetime_format.value.type_produced is int
        return _build_cjson_render(
            data=data,
            format_integer=self.format_integer,
            format_float=self.format_float,
            format_string=self.format_string,
            format_bytes=self.format_bytes,
            format_date=self.format_date,
            format_datetime=self.format_datetime,
            format_time=self.format_time,
            datetime_epoch=datetime_epoch,
            name_prefix=name_prefix,
        )

    @cached_property
    def format_call_variable_declaration(
        self,
    ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
        """Callable that formats a declaration binding a call result.

        A literal binding wraps the right-hand side in a designated-
        initializer compound literal that encodes the value's runtime
        type; a call's return type is opaque to the renderer and is
        always the universal ``CVal`` union (the type every generated
        call stub returns), so the call result is bound directly with a
        plain ``CVal`` declaration and no compound-literal wrapping.
        Under :attr:`json_type` the binding type is ``cJSON *``
        instead, matching the cJSON node-construction API.
        """
        if self._json_type_active:
            return _format_c_cjson_call_declaration
        return _format_c_call_declaration

    @cached_property
    def format_call_variable_assignment(
        self,
    ) -> Callable[[str, str, Value], str]:
        """Callable that formats an assignment binding a call result.

        The call-expression counterpart of
        :attr:`format_variable_assignment`; the compound-literal
        wrapping is dropped since the call already yields a ``CVal``.
        """
        return _format_c_call_assignment

    @cached_property
    def static_preamble(self) -> Sequence[str]:
        """Static preamble lines emitted once per file.

        Under :attr:`json_type` the ``cjson/cJSON.h`` header replaces
        the default ``CVal`` / ``CKV`` type declarations because every
        emitted expression goes through the cJSON node-construction
        API.
        """
        if self._json_type_active:
            return _CJSON_STATIC_PREAMBLE
        return (
            "#include <stdbool.h>",
            "#include <stddef.h>",
            "typedef struct CVal CVal;",
            "typedef struct CKV CKV;",
            "struct CVal {",
            "    union {",
            f"        _Bool {self.bool_field};",
            f"        long long {self.int_field};",
            f"        unsigned long long {self.uint_field};",
            f"        double {self.float_field};",
            f"        const char *{self.string_field};",
            f"        const CVal *{self.array_field};",
            f"        const CKV *{self.map_field};",
            "    };",
            "};",
            (
                f"struct CKV {{ const char *{self.key_field}; "
                f"CVal {self.value_field}; }};"
            ),
        )

    @cached_property
    def scalar_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar preamble (C needs none)."""
        return {}

    @cached_property
    def scalar_body_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar body preamble (C needs none)."""
        return {}

    @cached_property
    def compute_body_preamble(
        self,
    ) -> Callable[[frozenset[type], Value], tuple[str, ...]]:
        """Compute body-preamble lines from the scalar map."""
        return body_preamble_from_scalars(
            scalar_body_preamble=self.scalar_body_preamble,
            format_lines=tuple,
        )
