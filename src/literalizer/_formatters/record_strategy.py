"""Language-agnostic orchestration for the ``RECORD`` heterogeneous
strategy.

The ``RECORD`` strategy renders record-shaped dicts (non-empty,
string-keyed) as generated struct/record declarations plus matching
literals, rather than a homogeneous map.  Shape detection lives in
:mod:`literalizer._formatters.type_inference`; this module owns the
parts that are the same for every target language (document-order
shape naming, post-order declaration emission) and delegates the
language-specific syntax to a :class:`RecordRenderer`.

Declaration field types are derived from the already-formatted literal
value (not re-inferred from the raw value) so a field's declared type
always matches the value the normal formatter emitted, including when
that value was widened by sibling context.  The behavior caches the
first-seen formatted fields per shape during literal rendering; the
preamble (assembled after all literals are formatted) reads that cache.

Rust keeps its own copy of this logic because it additionally supports
``record_shape_names`` and optional-field unification; this module
deliberately omits those knobs (out of scope for the non-Rust ports),
so :attr:`RecordShape.optional_keys` is always empty here.
"""

import dataclasses
from collections.abc import Callable, Mapping, Sequence

from beartype import beartype

from literalizer._formatters.type_inference import (
    RecordShape,
    collect_record_shapes,
)
from literalizer._language import (
    HeterogeneousBehavior,
    RenderedRecordLiteral,
    no_compute_call_slot_wrap_ids,
    no_compute_wrap_ids,
)
from literalizer._types import Scalar, Value


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
class RecordRenderer:
    """Per-language syntax hooks for the ``RECORD`` strategy.

    ``name_prefix`` is the auto-naming prefix (``Record`` -> ``Record0``,
    ``Record1``, ...).  ``field_identifier`` maps an original dict key
    to the language's field identifier (identity for most languages,
    PascalCase for Go).  ``field_type`` maps a field's already-formatted
    literal value to its declared type.  ``render_declaration`` builds
    one declaration block from the resolved fields, and
    ``render_literal`` builds the literal as a
    :class:`RenderedRecordLiteral` (structured pieces; the shared code
    in :mod:`literalizer._literalize` assembles the compact or multiline
    form from them, so no language flattens then re-parses).
    """

    name_prefix: str
    field_identifier: Callable[[str], str]
    field_type: Callable[[str], str]
    render_declaration: Callable[
        [str, Sequence[RecordDeclarationField]],
        str,
    ]
    render_literal: Callable[
        [str, Sequence[RecordLiteralField]],
        RenderedRecordLiteral,
    ]


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
) -> dict[RecordShape, str]:
    """Assign ``{prefix}{index}`` names in *shapes* order."""
    return {
        shape: f"{prefix}{index}"
        for index, shape in enumerate(iterable=shapes)
    }


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
    ``render_record_literal`` records the first-seen formatted fields
    per shape so the preamble can derive each field's declared type
    from the value the formatter actually emitted.
    """
    name_by_shape: dict[RecordShape, str] = {}
    id_to_shape: dict[int, RecordShape] = {}
    formatted_by_shape: dict[RecordShape, dict[str, str]] = {}

    def _compute_shapes(data: Value) -> Mapping[int, RecordShape]:
        """Walk *data*, assign names in document order, and reset the
        per-pass caches (a cached spec is reused across calls).
        """
        shapes_by_id = collect_record_shapes(data=data)
        name_by_shape.clear()
        id_to_shape.clear()
        formatted_by_shape.clear()
        id_to_shape.update(shapes_by_id)
        ordered = _ordered_record_shapes(
            data=data,
            shapes_by_id=shapes_by_id,
        )
        name_by_shape.update(
            _assign_names(shapes=ordered, prefix=renderer.name_prefix),
        )
        return shapes_by_id

    def _render_literal(
        value: "dict[Scalar, Value]",
        fields: Mapping[str, str],
    ) -> RenderedRecordLiteral:
        """Render a record-shape dict as a language-specific literal,
        caching the first-seen formatted fields for its shape.
        """
        shape = id_to_shape[id(value)]
        formatted_by_shape.setdefault(shape, dict(fields))
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
        order, typing each field from its first-seen formatted value.
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
            formatted = formatted_by_shape[shape]
            fields = [
                RecordDeclarationField(
                    identifier=renderer.field_identifier(key),
                    type_name=renderer.field_type(formatted[key]),
                )
                for key in shape.keys
            ]
            blocks.append(
                renderer.render_declaration(name_by_shape[shape], fields),
            )
        return tuple(blocks)

    return RecordStrategy(behavior=behavior, preamble=_preamble)
