"""Language-agnostic orchestration for the ``RECORD`` heterogeneous
strategy.

The ``RECORD`` strategy renders record-shaped dicts (non-empty,
string-keyed) as generated struct/record declarations plus matching
literals, rather than a homogeneous map.  Shape detection lives in
:mod:`literalizer._formatters.type_inference`; this module owns the
parts that are the same for every target language (document-order
shape naming, post-order declaration emission) and delegates the
language-specific syntax to a :class:`RecordRenderer`.

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
supports optional-field unification; this module deliberately omits
that (out of scope for the non-Rust ports), so
:attr:`RecordShape.optional_keys` is always empty here.  Splitting
same-key-set shapes whose field types conflict (issue #2888) is
supported behind the ``split_conflicting_field_types`` flag of
:func:`build_record_strategy`; because this module has no
optional-field unification its refinement is simpler than Rust's (no
absent-key wildcard rule), and it reuses each language's own
:attr:`RecordRenderer.field_type` hook as the field-type signature
rather than a separate mirror function.  This module also supports
``record_shape_names`` (custom per-shape struct names, keyed by the
shape's key-set).
"""

import dataclasses
from collections import Counter
from collections.abc import Callable, Hashable, Mapping, Sequence

from beartype import beartype

from literalizer._formatters.type_inference import (
    RecordShape,
    collect_record_shapes,
    drop_unrecordizable_nested_sibling_maps,
)
from literalizer._language import (
    HeterogeneousBehavior,
    RenderedRecordLiteral,
    no_compute_call_slot_wrap_ids,
    no_compute_wrap_ids,
)
from literalizer._types import Scalar, Value
from literalizer.exceptions import UnrepresentableInputError


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
    ``None`` otherwise.  ``element_record_name`` is the analogous
    generated name when ``value`` is a non-empty list whose every
    element is a record-shaped dict of one shared shape (a sibling list
    spanning more than one record shape is rejected before formatting),
    so a language that types such a list precisely -- e.g. C++
    ``std::vector<RecordN>`` -- can name the element struct; it is
    ``None`` for every other value, including a list of plain scalars.
    Languages that widen a record-dict list to a single catch-all
    element type (Go ``[]any``, Java ``Object[]``) ignore it.
    """

    value: Value
    record_name: str | None
    element_record_name: str | None = None


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
class RecordStrategy:
    """The two pieces a language wires into its strategy config: the
    :class:`HeterogeneousBehavior` and the data-dependent preamble.
    """

    behavior: HeterogeneousBehavior
    preamble: Callable[[Value], tuple[str, ...]]


@dataclasses.dataclass(frozen=True)
class _FieldVariantRecordShape(RecordShape):
    """A record shape split off from same-key-set dicts whose field
    types conflict (issue #2888).

    Mirrors Rust's ``_FieldVariantRecordShape``: two dicts with equal
    key tuples share one :class:`RecordShape`, but when a field's
    declared type differs between them (e.g. the nested record under a
    key has different fields, or a different scalar type) they cannot
    share one generated declaration -- the declaration would take the
    field types of the first dict and the literal for the other dict
    would not compile.  :func:`_refine_record_shapes` gives each
    conflicting group its own instance; ``variant`` (numbered in
    document order of each group's first dict) keeps the instances
    distinct so every shape-keyed lookup treats each group as a
    separate record shape.
    """

    # ``dataclasses`` requires a default here because the base class's
    # ``optional_keys`` field has one; every construction site passes
    # ``variant`` explicitly.
    variant: int = 0


@beartype
def _record_dicts_in_document_order(
    *,
    data: Value,
    shapes_by_id: Mapping[int, RecordShape],
) -> list[dict[Scalar, Value]]:
    """Return every record-shaped dict in *data*, in document order.

    A dict aliased into the tree more than once (e.g. via a YAML
    anchor) appears once.
    """
    ordered: list[dict[Scalar, Value]] = []
    seen: set[int] = set()

    def walk(node: Value) -> None:
        """Append record dicts under *node* in document order."""
        match node:
            case dict():
                if id(node) in shapes_by_id and id(node) not in seen:
                    seen.add(id(node))
                    ordered.append(node)
                for child in node.values():
                    walk(node=child)
            case list():
                for item in node:
                    walk(node=item)
            case _:
                return

    walk(node=data)
    return ordered


@beartype
def _group_token_strings(
    *,
    instances: Sequence[dict[Scalar, Value]],
    group_of: Mapping[int, Hashable],
) -> dict[int, str]:
    """Assign a stable, distinct string to each current refinement
    group, mapping ``id(instance)`` to its group's string.

    The strings stand in for the (not-yet-assigned) generated record
    names when a nested record dict is fed to a language's
    :attr:`RecordRenderer.field_type` hook during signature
    computation: two dicts in the same group get the same string, so
    the hook returns the same field type for a nested record they
    share, and different strings otherwise.  Numbered in document order
    so the result is deterministic across runs.
    """
    index_of_group: dict[Hashable, int] = {}
    string_of_id: dict[int, str] = {}
    for instance in instances:
        token = group_of[id(instance)]
        if token not in index_of_group:
            index_of_group[token] = len(index_of_group)
        string_of_id[id(instance)] = (
            f"\x00record-group-{index_of_group[token]}"
        )
    return string_of_id


@beartype
def _list_element_token(
    *,
    field_value: Value,
    id_to_shape: Mapping[int, RecordShape],
    token_string_of: Mapping[int, str],
) -> str | None:
    """Return the group string of the first element when *field_value*
    is a non-empty list whose every element is a record-shaped dict,
    else ``None``.

    Mirrors :func:`_list_element_record_name` but at signature level,
    substituting the current refinement-group string for the (unknown)
    generated name.  When the elements land in different groups the
    list spans more than one record shape and is rejected before
    formatting, so the first element's string is a fine deterministic
    stand-in for the whole list.
    """
    if not isinstance(field_value, list) or not field_value:
        return None
    if any(
        not (isinstance(item, dict) and id(item) in id_to_shape)
        for item in field_value
    ):
        return None
    return token_string_of[id(field_value[0])]


@beartype
def _instance_signature(
    *,
    instance: dict[Scalar, Value],
    shape: RecordShape,
    id_to_shape: Mapping[int, RecordShape],
    token_string_of: Mapping[int, str],
    field_type: Callable[[RecordFieldType], str],
) -> tuple[str, ...]:
    """Return the per-key declared field types of *instance*, in
    shape-key order.

    Each key's entry is the language's own
    :attr:`RecordRenderer.field_type` output for that field value, with
    any nested record dict represented by its current refinement-group
    string rather than a generated name (see
    :func:`_group_token_strings`).  Because this reuses the very hook
    that types the emitted declaration, two dicts whose signatures
    differ would be declared with different field types and so cannot
    share one generated declaration; a widening language (Go ``[]any``)
    returns the same type for values it collapses, so those do not
    split.
    """
    signature: list[str] = []
    for key in shape.keys:
        field_value = instance[key]
        nested_name = (
            token_string_of[id(field_value)]
            if isinstance(field_value, dict) and id(field_value) in id_to_shape
            else None
        )
        element_name = _list_element_token(
            field_value=field_value,
            id_to_shape=id_to_shape,
            token_string_of=token_string_of,
        )
        request = RecordFieldType(
            value=field_value,
            record_name=nested_name,
            element_record_name=element_name,
        )
        signature.append(field_type(request))
    return tuple(signature)


@beartype
def _regroup_by_field_signatures(
    *,
    instances: Sequence[dict[Scalar, Value]],
    id_to_shape: Mapping[int, RecordShape],
    group_of: Mapping[int, Hashable],
    field_type: Callable[[RecordFieldType], str],
) -> dict[int, Hashable]:
    """Run one refinement round: split each group whose members'
    field-type signatures disagree, keeping agreeing groups whole.

    Unlike Rust there are no optional keys here, so every member of a
    group has the same key set and a group agrees exactly when all its
    members share one signature.
    """
    token_string_of = _group_token_strings(
        instances=instances,
        group_of=group_of,
    )
    members_by_group: dict[Hashable, list[dict[Scalar, Value]]] = {}
    for instance in instances:
        members_by_group.setdefault(group_of[id(instance)], []).append(
            instance
        )
    new_group_of: dict[int, Hashable] = {}
    for token, members in members_by_group.items():
        signatures = [
            _instance_signature(
                instance=member,
                shape=id_to_shape[id(member)],
                id_to_shape=id_to_shape,
                token_string_of=token_string_of,
                field_type=field_type,
            )
            for member in members
        ]
        if len(set(signatures)) == 1:
            for member in members:
                new_group_of[id(member)] = token
        else:
            for member, signature in zip(members, signatures, strict=True):
                new_group_of[id(member)] = (token, signature)
    return new_group_of


@beartype
def _partition(
    *,
    instances: Sequence[dict[Scalar, Value]],
    group_of: Mapping[int, Hashable],
) -> frozenset[tuple[int, ...]]:
    """Return the grouping of *instances* induced by *group_of* in a
    form comparable across refinement rounds (group tokens change
    representation between rounds even when the grouping does not).
    """
    ids_by_group: dict[Hashable, list[int]] = {}
    for instance in instances:
        ids_by_group.setdefault(group_of[id(instance)], []).append(
            id(instance)
        )
    return frozenset(tuple(ids) for ids in ids_by_group.values())


@beartype
def _materialize_refined_shapes(
    *,
    instances: Sequence[dict[Scalar, Value]],
    shapes_by_id: Mapping[int, RecordShape],
    group_of: Mapping[int, Hashable],
) -> dict[int, RecordShape]:
    """Map each dict to its refined shape.

    A shape whose dicts all landed in one group keeps its original
    :class:`RecordShape` object, so unaffected inputs render exactly as
    before; a split shape's groups become
    :class:`_FieldVariantRecordShape` instances numbered in document
    order of each group's first dict.
    """
    tokens_by_shape: dict[RecordShape, set[Hashable]] = {}
    for instance in instances:
        tokens_by_shape.setdefault(shapes_by_id[id(instance)], set()).add(
            group_of[id(instance)]
        )
    shape_for_token: dict[Hashable, RecordShape] = {}
    variant_counter: Counter[RecordShape] = Counter()
    refined: dict[int, RecordShape] = {}
    for instance in instances:
        token = group_of[id(instance)]
        base = shapes_by_id[id(instance)]
        if token not in shape_for_token:
            if len(tokens_by_shape[base]) == 1:
                shape_for_token[token] = base
            else:
                shape_for_token[token] = _FieldVariantRecordShape(
                    keys=base.keys,
                    optional_keys=base.optional_keys,
                    variant=variant_counter[base],
                )
                variant_counter[base] += 1
        refined[id(instance)] = shape_for_token[token]
    return refined


@beartype
def _refine_record_shapes(
    *,
    data: Value,
    shapes_by_id: Mapping[int, RecordShape],
    field_type: Callable[[RecordFieldType], str],
) -> dict[int, RecordShape]:
    """Split record shapes whose dicts disagree on a field's declared
    type (issue #2888).

    *shapes_by_id* keys shapes by key tuple, so two dicts with the same
    keys share a shape even when a field's value type differs; declaring
    the field with the type from the first dict then makes the literal
    for the other dict fail to compile.  This pass splits each shape's
    dicts into groups by per-field type signature so each group gets its
    own declaration.  Sibling lists spanning split groups then fail
    :func:`~literalizer._checks.check_data`'s mixed-record-shape gate
    (the honest heterogeneous-siblings outcome) instead of silently
    emitting mismatched field types, while groups that never share a
    list each render as a genuinely distinct declaration that compiles.

    Signatures reference nested records by group, so the grouping is
    computed to a fixed point: splitting a nested shape can in turn
    split the shape of the dicts embedding it.
    """
    instances = _record_dicts_in_document_order(
        data=data,
        shapes_by_id=shapes_by_id,
    )
    group_of: dict[int, Hashable] = {
        id(instance): shapes_by_id[id(instance)] for instance in instances
    }
    while True:
        regrouped = _regroup_by_field_signatures(
            instances=instances,
            id_to_shape=shapes_by_id,
            group_of=group_of,
            field_type=field_type,
        )
        old_partition = _partition(instances=instances, group_of=group_of)
        new_partition = _partition(instances=instances, group_of=regrouped)
        if new_partition == old_partition:
            break
        group_of = regrouped
    return _materialize_refined_shapes(
        instances=instances,
        shapes_by_id=shapes_by_id,
        group_of=group_of,
    )


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
    reject_split_key_sets: bool,
) -> dict[RecordShape, str]:
    """Assign struct names in *shapes* order.

    A shape whose key-set is mapped in *record_shape_names* takes the
    custom name; every other shape gets ``{prefix}{index}`` where
    *index* advances only for the auto-named shapes (mirrors Rust's
    ``_compute_shapes``/``_build_record_preamble``).

    When *reject_split_key_sets* is set (field-type splitting is on) and
    more than one distinct shape carries a custom-named key set (same
    keys but conflicting field types -- see
    :func:`_refine_record_shapes`), the custom name cannot identify one
    declaration, so the input is rejected rather than emitting duplicate
    declarations under that name (mirrors Rust's
    ``_assign_record_struct_names``).
    """
    key_set_counts = Counter(frozenset(shape.keys) for shape in shapes)
    names: dict[RecordShape, str] = {}
    prefix_index = 0
    for shape in shapes:
        key_set = frozenset(shape.keys)
        custom = record_shape_names.get(key_set)
        if custom is None:
            names[shape] = f"{prefix}{prefix_index}"
            prefix_index += 1
        elif reject_split_key_sets and key_set_counts[key_set] > 1:
            sorted_keys = ", ".join(sorted(key_set))
            msg = (
                f"record_shape_names maps the key set {{{sorted_keys}}} "
                f"to {custom!r}, but the data contains multiple distinct "
                f"record shapes with that key set (their field types "
                f"differ), so one custom name cannot identify one "
                f"generated declaration"
            )
            raise UnrepresentableInputError(msg)
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
def _list_element_record_name(
    *,
    field_value: Value,
    id_to_shape: Mapping[int, RecordShape],
    name_by_shape: Mapping[RecordShape, str],
) -> str | None:
    """Return the generated record name for *field_value* when it is a
    non-empty list whose every element is a record-shaped dict of one
    shared shape, else ``None``.

    A list mixing record dicts with other values returns ``None`` (the
    language types it through its own openers).  A sibling list
    spanning more than one record shape is rejected by
    :func:`literalizer._checks.check_data` before any value is
    formatted, so every element of an all-record-dict list that reaches
    here shares one shape and the first element's resolved name applies
    to the whole list.
    """
    if not isinstance(field_value, list) or not field_value:
        return None
    shapes = [
        id_to_shape.get(id(item)) if isinstance(item, dict) else None
        for item in field_value
    ]
    if any(shape is None for shape in shapes):
        return None
    # Every element is a record-shaped dict; the upstream mixed-shape
    # guard guarantees one shared shape, so the first element names the
    # whole list.
    return name_by_shape[id_to_shape[id(field_value[0])]]


@beartype
def build_record_strategy(  # noqa: C901  # pylint: disable=too-complex
    *,
    renderer: RecordRenderer,
    split_conflicting_field_types: bool,
    widen_unrecordizable_nested_sibling_maps: bool,
    derecordized_map_open: str | None,
) -> RecordStrategy:
    """Build the behavior + preamble for the ``RECORD`` strategy.

    The two share per-pass caches: ``compute_record_shapes`` (run first,
    during data checking) assigns the document-order names, and
    ``render_record_literal`` records the first-seen
    :class:`RecordFieldType` request per shape so the preamble can
    derive each field's declared type from the raw value through the
    language's own collection openers.

    When *split_conflicting_field_types* is set, ``compute_record_shapes``
    additionally runs :func:`_refine_record_shapes` so same-key-set dicts
    whose declared field types conflict resolve to distinct record shapes
    (issue #2888); a language opts in once its
    :attr:`RecordRenderer.field_type` hook is a faithful field-type
    signature (widening hooks are checked for polarity first).  Left off,
    the strategy behaves exactly as before.

    When *widen_unrecordizable_nested_sibling_maps* is set, nested maps
    whose sibling instances cannot share one record shape are dropped
    from the shape mapping before field-type refinement (issue #2910).
    They consequently fall through to the language's plain-map renderer;
    their ids are exposed through ``compute_wrap_ids`` so the shared
    heterogeneous checks treat their scalar children as representable by
    the language's widened map value type.  The identity scalar wrapper
    leaves those children unchanged in languages such as Go, whose top
    type accepts the original literals directly.  Such a language can
    provide *derecordized_map_open* to force the corresponding widened
    literal opener even when one map's raw values look homogeneous.
    """
    name_by_shape: dict[RecordShape, str] = {}
    id_to_shape: dict[int, RecordShape] = {}
    request_by_shape: dict[RecordShape, dict[str, RecordFieldType]] = {}

    def _compute_shapes(data: Value) -> Mapping[int, RecordShape]:
        """Walk *data*, assign names in document order, and reset the
        per-pass caches (a cached spec is reused across calls).

        With *split_conflicting_field_types* on, same-key-set dicts
        whose declared field types conflict are first refined into
        distinct shapes (see :func:`_refine_record_shapes`) so the
        naming and later the mixed-record-shape gate treat them apart.
        """
        raw_shapes_by_id = collect_record_shapes(data=data)
        widened_shapes_by_id = (
            drop_unrecordizable_nested_sibling_maps(
                data=data,
                shapes_by_id=raw_shapes_by_id,
            )
            if widen_unrecordizable_nested_sibling_maps
            else raw_shapes_by_id
        )
        shapes_by_id = (
            _refine_record_shapes(
                data=data,
                shapes_by_id=widened_shapes_by_id,
                field_type=renderer.field_type,
            )
            if split_conflicting_field_types
            else widened_shapes_by_id
        )
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
                reject_split_key_sets=split_conflicting_field_types,
            ),
        )
        return shapes_by_id

    def _field_type_request(field_value: Value) -> RecordFieldType:
        """Build the structured field-type request for *field_value*.

        ``record_name`` is set only when *field_value* is itself a
        nested record-shaped dict; ``element_record_name`` is set only
        when *field_value* is a non-empty list whose every element is a
        record-shaped dict of one shared shape (its generated name).
        Both are pieces a language cannot recover from the raw value;
        every other value is typed by the language from the value via
        its own collection openers.
        """
        nested_name = (
            name_by_shape.get(id_to_shape[id(field_value)])
            if isinstance(field_value, dict) and id(field_value) in id_to_shape
            else None
        )
        element_name = _list_element_record_name(
            field_value=field_value,
            id_to_shape=id_to_shape,
            name_by_shape=name_by_shape,
        )
        return RecordFieldType(
            value=field_value,
            record_name=nested_name,
            element_record_name=element_name,
        )

    def _render_literal(
        value: "dict[Scalar, Value]",
        fields: Mapping[str, str],
    ) -> RenderedRecordLiteral | None:
        """Render a record-shape dict as a language-specific literal,
        caching the first-seen field-type requests for its shape.

        A record-eligible dict absent from ``id_to_shape`` was widened
        to a plain map, so return ``None`` and let the shared formatter
        fall through to normal map rendering.
        """
        if id(value) not in id_to_shape:
            return None
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

    def _compute_wrap_ids(data: Value) -> frozenset[int]:
        """Return ids of maps widened out of the record-shape mapping."""
        raw_shapes_by_id = collect_record_shapes(data=data)
        widened_shapes_by_id = drop_unrecordizable_nested_sibling_maps(
            data=data,
            shapes_by_id=raw_shapes_by_id,
        )
        return frozenset(set(raw_shapes_by_id) - set(widened_shapes_by_id))

    def _identity_scalar_wrapper(_raw: Scalar, formatted: str) -> str:
        """Leave a scalar unchanged inside a top-type widened map."""
        return formatted

    behavior = HeterogeneousBehavior(
        skip_scalar_checks=False,
        compute_wrap_ids=(
            _compute_wrap_ids
            if widen_unrecordizable_nested_sibling_maps
            else no_compute_wrap_ids
        ),
        wrap_scalar=(
            _identity_scalar_wrapper
            if widen_unrecordizable_nested_sibling_maps
            else None
        ),
        wrap_non_scalar=None,
        compute_call_slot_wrap_ids=no_compute_call_slot_wrap_ids,
        dict_open_for_wrap_ids=derecordized_map_open,
        widens_nested_maps_by_wrapping_scalars=False,
        render_record_literal=_render_literal,
        compute_record_shapes=_compute_shapes,
        render_tuple_literal=None,
        compute_tuple_list_ids=None,
    )

    def _preamble(data: Value, /) -> tuple[str, ...]:
        """Build one declaration block per record shape, in dependency
        order, typing each field from its first-seen
        :class:`RecordFieldType` request.

        Emit order is read from the shared ``id_to_shape`` cache
        (populated by ``_compute_shapes`` during data checking) rather
        than recomputed, so it reflects any field-type refinement; the
        raw shapes would miss the split ``_FieldVariantRecordShape``
        entries the literal rendering and naming are keyed by.
        """
        if not id_to_shape:
            return ()
        emit_order: list[RecordShape] = []
        emit_seen: set[RecordShape] = set()
        _accumulate_emit_order(
            data=data,
            shapes_by_id=id_to_shape,
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
