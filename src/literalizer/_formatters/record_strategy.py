"""Language-agnostic orchestration for the ``RECORD`` and ``TUPLE``
heterogeneous strategies.

The ``RECORD`` strategy renders record-shaped dicts (non-empty,
string-keyed) as generated struct/record declarations plus matching
literals, rather than a homogeneous map.  Shape detection lives in
:mod:`literalizer._formatters.type_inference`; this module owns the
parts that are the same for every target language (document-order
shape naming, post-order declaration emission) and delegates the
language-specific syntax to a :class:`RecordRenderer`.

The ``TUPLE`` strategy composes ``RECORD``: :func:`build_tuple_strategy`
reuses every piece above and additionally renders each tuple-eligible
heterogeneous scalar array (a record field, another dict value, or the
document root) as the language's native fixed-size tuple, typing a
tuple-valued record field as ``(T0, T1, ...)`` instead of a
homogeneous sequence.  Tuple scope detection lives in
:mod:`literalizer._formatters.tuple_strategy`.

Declaration field types are derived from the raw field value through
the language's own collection openers (the same opener functions the
value formatter uses), not by re-parsing the formatted literal.
Because a record field is formatted with no sibling override, the
opener a language returns for the field's value is exactly the one it
emitted (including a widening to an ``any``-typed container), so the
declared type still matches the rendered literal.  The behavior caches
the first-seen :class:`RecordFieldType` request per shape during
literal rendering; the preamble (assembled after all literals are
formatted) reads that cache.

Rust keeps its own copy of this logic because it additionally
supports optional-field unification; this module supports
``record_shape_names`` (custom per-shape struct names, keyed by the
shape's key-set) but deliberately omits unification (out of scope
for the non-Rust ports), so :attr:`RecordShape.optional_keys` is
always empty here.
"""

import dataclasses
from collections.abc import Callable, Mapping, Sequence

from beartype import beartype

from literalizer._formatters.tuple_strategy import (
    collect_tuple_lists,
    is_tuple_eligible,
)
from literalizer._formatters.type_inference import (
    RecordShape,
    collect_record_shapes,
)
from literalizer._language import (
    HeterogeneousBehavior,
    RenderedRecordLiteral,
    RenderedTupleLiteral,
    no_compute_call_slot_wrap_ids,
    no_compute_wrap_ids,
)
from literalizer._types import Scalar, Value
from literalizer.exceptions import TupleArityNotRepresentableError


@dataclasses.dataclass(frozen=True)
class RecordDeclarationField:
    """One resolved field of a generated record declaration."""

    identifier: str
    type_name: str


@dataclasses.dataclass(frozen=True)
class RecordLiteralField:
    """One resolved field of a generated record literal.

    ``formatted`` is the already-formatted field value produced by the
    normal value formatter.
    """

    identifier: str
    formatted: str


@dataclasses.dataclass(frozen=True)
class RecordFieldType:
    """The structured input to :attr:`RecordRenderer.field_type`.

    ``value`` is the raw field value (first-seen for its shape); a
    language maps it to a declared type through its own collection
    openers / scalar mapping rather than prefix-matching a formatted
    literal.  ``record_name`` is the generated declaration name when
    ``value`` is itself a nested record-shaped dict (resolved here, the
    one piece a language cannot recover from the value alone), and
    ``None`` otherwise.
    """

    value: Value
    record_name: str | None


@dataclasses.dataclass(frozen=True)
class RecordRenderer:
    """Per-language syntax hooks for the ``RECORD`` strategy.

    ``name_prefix`` is the auto-naming prefix (``Record`` -> ``Record0``,
    ``Record1``, ...).  ``record_shape_names`` maps a shape's key-set
    (``frozenset`` of its keys) to a custom struct name; a mapped shape
    uses that name and the auto ``{prefix}{index}`` counter advances
    only for the shapes with no custom name (mirrors Rust).
    ``field_identifier`` maps an original dict key to the language's
    field identifier (identity for most languages, PascalCase for Go).
    ``field_type`` maps a :class:`RecordFieldType`
    (raw field value plus any resolved nested-record name) to its
    declared type, using the language's own collection openers rather
    than re-parsing the formatted literal.  ``render_declaration`` builds
    one declaration block from the resolved fields, and
    ``render_literal`` builds the literal as a
    :class:`RenderedRecordLiteral` (structured pieces; the shared code
    in :mod:`literalizer._literalize` assembles the compact or multiline
    form from them, so no language flattens then re-parses).
    """

    name_prefix: str
    record_shape_names: Mapping[frozenset[str], str]
    field_identifier: Callable[[str], str]
    field_type: Callable[[RecordFieldType], str]
    render_declaration: Callable[
        [str, Sequence[RecordDeclarationField]],
        str,
    ]
    render_literal: Callable[
        [str, Sequence[RecordLiteralField]],
        RenderedRecordLiteral,
    ]


@dataclasses.dataclass(frozen=True)
class TupleRenderer:
    """Per-language syntax hooks for the ``TUPLE`` strategy.

    The ``TUPLE`` strategy composes ``RECORD`` (a record field whose
    value is a tuple-eligible heterogeneous scalar array becomes a
    tuple-typed field) and adds two pieces of syntax on top of a
    :class:`RecordRenderer`:

    ``render_type`` joins the already-resolved element type names into
    the language's tuple *type* (Scala ``(T0, T1, ...)``), used for the
    declared type of a record field whose value is such an array.
    ``render_literal`` builds the tuple *literal* as a
    :class:`RenderedTupleLiteral` (structured pieces the shared layout
    code in :mod:`literalizer._literalize` assembles into compact or
    multiline form) from the raw list and its pre-formatted elements.
    ``arity_limit`` is the most elements a native tuple may hold in
    the language (Scala's ``Tuple22`` -> ``22``); a tuple-eligible
    array longer than the limit raises
    :exc:`~literalizer.exceptions.TupleArityNotRepresentableError` at
    check time rather than silently downgrading.  Every language that
    composes ``RECORD`` through :func:`build_tuple_strategy` is
    statically typed with a finite tuple-element cap, so the limit is
    always required (a language with unbounded tuples builds its
    behavior directly, like Rust, rather than through this shared
    helper).
    """

    render_type: Callable[[Sequence[str]], str]
    render_literal: Callable[
        [list[Value], Sequence[str]],
        RenderedTupleLiteral,
    ]
    arity_limit: int


@dataclasses.dataclass(frozen=True)
class RecordStrategy:
    """The two pieces a language wires into its strategy config: the
    :class:`HeterogeneousBehavior` and the data-dependent preamble.
    """

    behavior: HeterogeneousBehavior
    preamble: Callable[[Value], tuple[str, ...]]


@beartype
def _ordered_record_shapes(
    *,
    data: Value,
    shapes_by_id: Mapping[int, RecordShape],
) -> list[RecordShape]:
    """Return record shapes in document order, one per distinct shape."""
    ordered: list[RecordShape] = []
    seen: set[RecordShape] = set()
    _accumulate_ordered_shapes(
        data=data,
        shapes_by_id=shapes_by_id,
        ordered=ordered,
        seen=seen,
    )
    return ordered


@beartype
def _accumulate_ordered_shapes(
    *,
    data: Value,
    shapes_by_id: Mapping[int, RecordShape],
    ordered: list[RecordShape],
    seen: set[RecordShape],
) -> None:
    """Walk *data* appending each newly-seen record shape to *ordered*."""
    match data:
        case dict():
            if id(data) in shapes_by_id:
                shape = shapes_by_id[id(data)]
                if shape not in seen:
                    seen.add(shape)
                    ordered.append(shape)
            for value in data.values():
                _accumulate_ordered_shapes(
                    data=value,
                    shapes_by_id=shapes_by_id,
                    ordered=ordered,
                    seen=seen,
                )
        case list():
            for item in data:
                _accumulate_ordered_shapes(
                    data=item,
                    shapes_by_id=shapes_by_id,
                    ordered=ordered,
                    seen=seen,
                )
        case _:
            return


@beartype
def _assign_names(
    *,
    shapes: Sequence[RecordShape],
    prefix: str,
    record_shape_names: Mapping[frozenset[str], str],
) -> dict[RecordShape, str]:
    """Assign struct names in *shapes* order.

    A shape whose key-set is mapped in *record_shape_names* takes the
    custom name; every other shape gets ``{prefix}{index}`` where
    *index* advances only for the auto-named shapes (mirrors Rust's
    ``_compute_shapes``/``_build_record_preamble``).
    """
    names: dict[RecordShape, str] = {}
    prefix_index = 0
    for shape in shapes:
        custom = record_shape_names.get(frozenset(shape.keys))
        if custom is None:
            names[shape] = f"{prefix}{prefix_index}"
            prefix_index += 1
        else:
            names[shape] = custom
    return names


@beartype
def _accumulate_emit_order(
    *,
    data: Value,
    shapes_by_id: Mapping[int, RecordShape],
    emit_ordered: list[RecordShape],
    emit_seen: set[RecordShape],
) -> None:
    """Walk *data* post-order so a shape is emitted after its
    dependencies (nested records declared before their parents).
    """
    match data:
        case dict():
            for value in data.values():
                _accumulate_emit_order(
                    data=value,
                    shapes_by_id=shapes_by_id,
                    emit_ordered=emit_ordered,
                    emit_seen=emit_seen,
                )
            if id(data) in shapes_by_id:
                shape = shapes_by_id[id(data)]
                if shape not in emit_seen:
                    emit_seen.add(shape)
                    emit_ordered.append(shape)
        case list():
            for item in data:
                _accumulate_emit_order(
                    data=item,
                    shapes_by_id=shapes_by_id,
                    emit_ordered=emit_ordered,
                    emit_seen=emit_seen,
                )
        case _:
            return


@beartype
def build_record_strategy(
    *,
    renderer: RecordRenderer,
) -> RecordStrategy:
    """Build the behavior + preamble for the ``RECORD`` strategy.

    The two share per-pass caches: ``compute_record_shapes`` (run first,
    during data checking) assigns the document-order names, and
    ``render_record_literal`` records the first-seen
    :class:`RecordFieldType` request per shape so the preamble can
    derive each field's declared type from the raw value through the
    language's own collection openers.
    """
    name_by_shape: dict[RecordShape, str] = {}
    id_to_shape: dict[int, RecordShape] = {}
    request_by_shape: dict[RecordShape, dict[str, RecordFieldType]] = {}

    def _compute_shapes(data: Value) -> Mapping[int, RecordShape]:
        """Walk *data*, assign names in document order, and reset the
        per-pass caches (a cached spec is reused across calls).
        """
        shapes_by_id = collect_record_shapes(data=data)
        name_by_shape.clear()
        id_to_shape.clear()
        request_by_shape.clear()
        id_to_shape.update(shapes_by_id)
        ordered = _ordered_record_shapes(
            data=data,
            shapes_by_id=shapes_by_id,
        )
        name_by_shape.update(
            _assign_names(
                shapes=ordered,
                prefix=renderer.name_prefix,
                record_shape_names=renderer.record_shape_names,
            ),
        )
        return shapes_by_id

    def _field_type_request(field_value: Value) -> RecordFieldType:
        """Build the structured field-type request for *field_value*.

        ``record_name`` is set only when *field_value* is itself a
        nested record-shaped dict (the one piece a language cannot
        recover from the raw value); every other value, including a
        list of record-shaped dicts, is typed by the language from the
        value via its own collection openers.
        """
        nested_name = (
            name_by_shape.get(id_to_shape[id(field_value)])
            if isinstance(field_value, dict) and id(field_value) in id_to_shape
            else None
        )
        return RecordFieldType(
            value=field_value,
            record_name=nested_name,
        )

    def _render_literal(
        value: "dict[Scalar, Value]",
        fields: Mapping[str, str],
    ) -> RenderedRecordLiteral:
        """Render a record-shape dict as a language-specific literal,
        caching the first-seen field-type requests for its shape.
        """
        shape = id_to_shape[id(value)]
        if shape not in request_by_shape:
            request_by_shape[shape] = {
                key: _field_type_request(field_value=value[key])
                for key in shape.keys
            }
        literal_fields = [
            RecordLiteralField(
                identifier=renderer.field_identifier(key),
                formatted=fields[key],
            )
            for key in shape.keys
        ]
        return renderer.render_literal(name_by_shape[shape], literal_fields)

    behavior = HeterogeneousBehavior(
        skip_scalar_checks=False,
        compute_wrap_ids=no_compute_wrap_ids,
        wrap_scalar=None,
        wrap_non_scalar=None,
        compute_call_slot_wrap_ids=no_compute_call_slot_wrap_ids,
        render_record_literal=_render_literal,
        compute_record_shapes=_compute_shapes,
    )

    def _preamble(data: Value, /) -> tuple[str, ...]:
        """Build one declaration block per record shape, in dependency
        order, typing each field from its first-seen
        :class:`RecordFieldType` request.
        """
        shapes_by_id = collect_record_shapes(data=data)
        if not shapes_by_id:
            return ()
        emit_order: list[RecordShape] = []
        emit_seen: set[RecordShape] = set()
        _accumulate_emit_order(
            data=data,
            shapes_by_id=shapes_by_id,
            emit_ordered=emit_order,
            emit_seen=emit_seen,
        )
        blocks: list[str] = []
        for shape in emit_order:
            requests = request_by_shape[shape]
            fields = [
                RecordDeclarationField(
                    identifier=renderer.field_identifier(key),
                    type_name=renderer.field_type(requests[key]),
                )
                for key in shape.keys
            ]
            blocks.append(
                renderer.render_declaration(name_by_shape[shape], fields),
            )
        return tuple(blocks)

    return RecordStrategy(behavior=behavior, preamble=_preamble)


@beartype
def build_tuple_strategy(
    *,
    record_renderer: RecordRenderer,
    tuple_renderer: TupleRenderer,
) -> RecordStrategy:
    """Build the behavior + preamble for the ``TUPLE`` strategy.

    ``TUPLE`` composes ``RECORD``: record-shaped dicts still become
    generated declarations, but a record field whose value is a
    tuple-eligible heterogeneous scalar array is typed as the
    language's native tuple ``(T0, T1, ...)`` (via
    :attr:`TupleRenderer.render_type`) instead of the homogeneous
    sequence type, and every tuple-eligible array (a record field,
    another dict value, or the document root) renders as a tuple
    literal.  An array longer than :attr:`TupleRenderer.arity_limit`
    raises :exc:`~literalizer.exceptions.TupleArityNotRepresentableError`
    at check time rather than silently downgrading.
    """
    base_field_type = record_renderer.field_type

    def _tuple_aware_field_type(request: RecordFieldType) -> str:
        """Type a tuple-eligible list field as the native tuple type.

        A record field is a dict value, so the positional half of
        tuple-eligibility holds and :func:`is_tuple_eligible` supplies
        the structural half.  Each element is itself a scalar
        (tuple-eligible arrays are all-scalar) typed through the
        language's own ``field_type``, then joined by
        :attr:`TupleRenderer.render_type`.
        """
        value = request.value
        if isinstance(value, list) and is_tuple_eligible(value=value):
            element_types = [
                base_field_type(
                    RecordFieldType(value=element, record_name=None),
                )
                for element in value
            ]
            return tuple_renderer.render_type(element_types)
        return base_field_type(request)

    record_strategy = build_record_strategy(
        renderer=dataclasses.replace(
            record_renderer,
            field_type=_tuple_aware_field_type,
        ),
    )

    def _compute_tuple_list_ids(data: Value, /) -> frozenset[int]:
        """Return the tuple-eligible list ids, enforcing the
        tuple-length limit first.

        The limit is checked against the same lists
        :func:`collect_tuple_lists` marks (dict values / record fields
        / the document root); a list reached only as a list element is
        out of tuple scope and keeps raising the ordinary
        heterogeneous-scalar error instead.
        """
        tuple_lists = collect_tuple_lists(data=data)
        limit = tuple_renderer.arity_limit
        for tuple_list in tuple_lists:
            if len(tuple_list) > limit:
                raise TupleArityNotRepresentableError(
                    arity=len(tuple_list),
                    limit=limit,
                )
        return frozenset(id(tuple_list) for tuple_list in tuple_lists)

    behavior = dataclasses.replace(
        record_strategy.behavior,
        render_tuple_literal=tuple_renderer.render_literal,
        compute_tuple_list_ids=_compute_tuple_list_ids,
    )
    return RecordStrategy(
        behavior=behavior,
        preamble=record_strategy.preamble,
    )
