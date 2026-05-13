"""Collection opener functions and typed opener configuration."""

import datetime
from collections.abc import Callable, Sequence
from dataclasses import dataclass

from beartype import beartype

from literalizer._formatters.type_inference import (
    DictType,
    ListType,
    MixedNumeric,
    WideInt,
    infer_element_type,
)
from literalizer._types import Value


@beartype
def fixed_open(
    *, open_str: str
) -> Callable[[list[Value] | dict[str, Value]], str]:
    """Return an opener callable that always returns *open_str*.

    Use this as ``sequence_open``, ``set_open``, ``dict_open``, or
    ``ordered_map_open`` when the opening delimiter is a fixed string
    that does not depend on the collection contents.

    Example: ``fixed_open(open_str="[")([1, 2, 3])`` -> ``"["``.
    """

    def _open(_items: list[Value] | dict[str, Value], /) -> str:
        """Return the fixed opening delimiter, ignoring *_items*."""
        return open_str

    return _open


@beartype
def make_element_to_type(
    *,
    str_type: str | None,
    bool_type: str | None,
    int_type: str | None,
    float_type: str | None,
    bytes_type: str | None,
    mixed_numeric_type: str | None,
    date_type: str | None,
    datetime_type: str | None,
    list_template: str,
    dict_type_template: str | None,
    fallback_value_type: str | None,
    wide_int_type: str | None = None,
) -> Callable[[type | ListType | DictType], str | None]:
    """Create a recursive type resolver from scalar types and a list
    template.

    The *list_template* must contain ``{inner}`` which will be replaced
    with the recursively-resolved inner type name.

    When *dict_type_template* is given it must contain ``{inner}``
    and is used to resolve ``DictType`` elements.  *fallback_value_type*
    is used when the dict value type is ``None`` or cannot be resolved.

    Example::

        go_element_to_type = make_element_to_type(
            str_type="string",
            int_type="int",
            list_template="[]{inner}",
            dict_type_template="map[string]{inner}",
            fallback_value_type="any",
        )
    """
    scalar_types: dict[type, str] = {
        py_type: name
        for py_type, name in (
            (str, str_type),
            (bool, bool_type),
            (int, int_type),
            (float, float_type),
            (bytes, bytes_type),
            (MixedNumeric, mixed_numeric_type),
            (
                WideInt,
                wide_int_type if wide_int_type is not None else int_type,
            ),
            (datetime.date, date_type),
            (datetime.datetime, datetime_type),
        )
        if name is not None
    }

    def element_to_type(
        element_type: type | ListType | DictType,
    ) -> str | None:
        """Delegate to module-level implementation."""
        return _resolve_element_to_type(
            element_type=element_type,
            scalar_types=scalar_types,
            list_template=list_template,
            dict_type_template=dict_type_template,
            fallback_value_type=fallback_value_type,
        )

    return element_to_type


@beartype
def make_narrowed_empty_form(
    *,
    element_to_type: Callable[[type | ListType | DictType], str | None],
    template: str,
    fallback_type: str,
) -> Callable[[Sequence[list[Value]]], str]:
    """Return a ``narrowed_empty_form`` callback.

    The returned function reads the inferred element type of the first
    non-empty sibling list, maps it through *element_to_type*, and
    substitutes the resolved type name into *template* (which must
    contain ``{type}``).  *fallback_type* is used when the type cannot
    be resolved (heterogeneous siblings, or an element type that
    *element_to_type* does not handle).

    Example::

        narrowed_empty_form = make_narrowed_empty_form(
            element_to_type=mojo_element_to_type,
            template="List[{type}]()",
            fallback_type="String",
        )
    """

    def _narrowed_empty_form(siblings: Sequence[list[Value]]) -> str:
        """Compute the typed empty literal for the parent's siblings."""
        inner = infer_element_type(items=siblings[0])
        type_name = element_to_type(inner) if inner is not None else None
        return template.format(type=type_name or fallback_type)

    return _narrowed_empty_form


@beartype
def _resolve_element_to_type(
    *,
    element_type: type | ListType | DictType,
    scalar_types: dict[type, str],
    list_template: str,
    dict_type_template: str | None,
    fallback_value_type: str | None,
) -> str | None:
    """Resolve a Python element type to a language type name."""
    match element_type:
        case DictType():
            if dict_type_template is None:
                return None
            resolved: str | None = None
            if element_type.value_type is not None:
                resolved = _resolve_element_to_type(
                    element_type=element_type.value_type,
                    scalar_types=scalar_types,
                    list_template=list_template,
                    dict_type_template=dict_type_template,
                    fallback_value_type=fallback_value_type,
                )
            inner = resolved if resolved is not None else fallback_value_type
            if inner is None:
                return None
            return dict_type_template.format(inner=inner)
        case ListType():
            inner = _resolve_element_to_type(
                element_type=element_type.inner,
                scalar_types=scalar_types,
                list_template=list_template,
                dict_type_template=dict_type_template,
                fallback_value_type=fallback_value_type,
            )
            if inner is None:
                return None
            return list_template.format(inner=inner)
        case _:
            return scalar_types.get(element_type)


@beartype
def _apply_type_to_opener(
    element_type: type | ListType | DictType,
    element_to_type: Callable[[type | ListType | DictType], str | None],
    opener_template: str,
) -> str | None:
    """Resolve a Python element type to a collection opener."""
    type_name = element_to_type(element_type)
    if type_name is None:
        return None
    return opener_template.format(type_name=type_name)


@beartype
def make_type_to_opener(
    *,
    element_to_type: Callable[[type | ListType | DictType], str | None],
    opener_template: str,
) -> Callable[[type | ListType | DictType], str | None]:
    """Create a typed collection opener from an element-to-type resolver.

    The *opener_template* must contain ``{type_name}`` which will be
    replaced with the resolved type name.

    Example::

        go_type_to_opener = make_type_to_opener(
            element_to_type=go_element_to_type,
            opener_template="[]{type_name}{{",
        )
    """

    def type_to_opener(element_type: type | ListType | DictType) -> str | None:
        """Delegate to module-level implementation."""
        return _apply_type_to_opener(
            element_type=element_type,
            element_to_type=element_to_type,
            opener_template=opener_template,
        )

    return type_to_opener


@beartype
def _typed_collection_open_impl(
    items: list[Value],
    type_to_opener: Callable[[type | ListType | DictType], str | None],
    fallback: str,
) -> str:
    """Infer element type and return the opener or fallback."""
    element_type = infer_element_type(items=items)
    if element_type is None:
        return fallback
    return type_to_opener(element_type) or fallback


@beartype
def typed_collection_open(
    *,
    type_to_opener: Callable[[type | ListType | DictType], str | None],
    fallback: str,
) -> Callable[[list[Value]], str]:
    """Return a callable that infers the common element type and
    delegates to *type_to_opener*.

    Works for both sequences and sets — any collection whose items
    are presented as a ``list[Value]``.

    When inference is not possible or *type_to_opener* returns
    ``None``, *fallback* is used instead.

    Example::

        def my_opener(element_type: type | ListType) -> str | None:
            if element_type is str:
                return "[]string{"
            return None

        sequence_open = typed_collection_open(
            type_to_opener=my_opener,
            fallback="[]any{",
        )
    """

    def _open(items: list[Value]) -> str:
        """Delegate to module-level implementation."""
        return _typed_collection_open_impl(
            items=items, type_to_opener=type_to_opener, fallback=fallback
        )

    return _open


@beartype
def _typed_dict_open_impl(
    items: dict[str, Value],
    type_to_opener: Callable[[type | ListType | DictType], str | None],
    fallback: str,
) -> str:
    """Infer value type and return the opener or fallback."""
    element_type = infer_element_type(items=list(items.values()))
    if element_type is None:
        return fallback
    return type_to_opener(element_type) or fallback


@beartype
def typed_dict_open(
    *,
    type_to_opener: Callable[[type | ListType | DictType], str | None],
    fallback: str,
) -> Callable[[dict[str, Value]], str]:
    """Return a ``dict_open`` callable that infers a common value type
    and delegates to *type_to_opener*.

    When inference is not possible or *type_to_opener* returns
    ``None``, *fallback* is used instead.

    Example::

        def my_opener(element_type: type | ListType) -> str | None:
            if element_type is str:
                return "map[string]string{"
            return None

        dict_open = typed_dict_open(
            type_to_opener=my_opener,
            fallback="map[string]any{",
        )
    """

    def _open(items: dict[str, Value]) -> str:
        """Delegate to module-level implementation."""
        return _typed_dict_open_impl(
            items=items, type_to_opener=type_to_opener, fallback=fallback
        )

    return _open


@dataclass(frozen=True)
class TypeOpeners:
    """Resolved type-to-opener functions for sequences, dicts, and
    sets.
    """

    seq: Callable[[type | ListType | DictType], str | None]
    dict: Callable[[type | ListType | DictType], str | None]
    set: Callable[[type | ListType | DictType], str | None]


class TypedOpenerConfig:
    """Configuration for typed collection openers in a language.

    Holds scalar type mappings and template strings needed to build
    type-to-opener functions.
    """

    @beartype
    def __init__(
        self,
        *,
        str_type: str | None,
        bool_type: str | None,
        int_type: str | None,
        float_type: str | None,
        bytes_type: str | None,
        mixed_numeric_type: str | None,
        date_type: str | None,
        datetime_type: str | None,
        list_template: str,
        sequence_opener_template: str,
        dict_opener_template: str,
        set_opener_template: str,
        dict_type_template: str | None,
        fallback_value_type: str | None,
        wide_int_type: str | None = None,
    ) -> None:
        """Initialize with scalar type mappings and template strings."""
        self._str_type = str_type
        self._bool_type = bool_type
        self._int_type = int_type
        self._float_type = float_type
        self._bytes_type = bytes_type
        self._mixed_numeric_type = mixed_numeric_type
        self._date_type = date_type
        self._datetime_type = datetime_type
        self._list_template = list_template
        self._sequence_opener_template = sequence_opener_template
        self._dict_opener_template = dict_opener_template
        self._set_opener_template = set_opener_template
        self._dict_type_template = dict_type_template
        self._fallback_value_type = fallback_value_type
        self._wide_int_type = wide_int_type

    @beartype
    def type_name(self, py_type: type) -> str | None:
        """Look up the language type name for a Python type."""
        return self._scalar_types().get(py_type)

    def _scalar_types(self) -> dict[type, str]:
        """Build a dict mapping Python types to language type names."""
        return {
            py_type: name
            for py_type, name in (
                (str, self._str_type),
                (bool, self._bool_type),
                (int, self._int_type),
                (float, self._float_type),
                (bytes, self._bytes_type),
                (MixedNumeric, self._mixed_numeric_type),
                (
                    WideInt,
                    self._wide_int_type
                    if self._wide_int_type is not None
                    else self._int_type,
                ),
                (datetime.date, self._date_type),
                (datetime.datetime, self._datetime_type),
            )
            if name is not None
        }

    @beartype
    def element_to_type(
        self,
        *,
        list_template: str | None,
        date_type: str | None,
        datetime_type: str | None,
        enable_dict_type: bool,
        dict_key_type: str = "",
    ) -> Callable[[type | ListType | DictType], str | None]:
        """Build an element-to-type resolver.

        If *list_template* is given it overrides the default.
        If *date_type* or *datetime_type* is given they override the
        base values.  When *enable_dict_type* is ``False`` the
        resolver will not handle ``DictType``.

        When *dict_key_type* is given, ``{key_type}`` placeholders in
        ``dict_type_template`` are resolved before the template is
        used.
        """
        raw_template = self._dict_type_template if enable_dict_type else None
        resolved_template = (
            raw_template.replace("{key_type}", dict_key_type)
            if raw_template is not None and dict_key_type
            else raw_template
        )
        return make_element_to_type(
            str_type=self._str_type,
            bool_type=self._bool_type,
            int_type=self._int_type,
            wide_int_type=self._wide_int_type,
            float_type=self._float_type,
            bytes_type=self._bytes_type,
            mixed_numeric_type=self._mixed_numeric_type,
            date_type=(
                date_type if date_type is not None else self._date_type
            ),
            datetime_type=(
                datetime_type
                if datetime_type is not None
                else self._datetime_type
            ),
            list_template=(
                list_template
                if list_template is not None
                else self._list_template
            ),
            dict_type_template=resolved_template,
            fallback_value_type=(
                self._fallback_value_type if enable_dict_type else None
            ),
        )

    @beartype
    def build(
        self,
        *,
        date_type: str | None,
        datetime_type: str | None,
        set_opener_template: str | None,
        narrow_dict_values: bool,
        dict_key_type: str = "",
    ) -> TypeOpeners:
        """Build openers from the base scalar type mapping plus
        overrides.

        If *date_type* or *datetime_type* is given, they override the
        base values.  If *set_opener_template* is given it overrides
        the template used for ``set`` openers, allowing a single
        ``TypedOpenerConfig`` to serve multiple set formats.

        When *narrow_dict_values* is ``False``, the dict and set
        openers use a resolver that cannot resolve ``DictType``.
        Set this to ``False`` when the ``list_template``
        does not match the actual sequence format (e.g.
        ``Array<…>`` vs ``List<…>``), which would cause type
        mismatches in the generated code.

        When *dict_key_type* is given, ``{key_type}`` placeholders in
        ``dict_opener_template`` and ``dict_type_template`` are
        resolved before the templates are used.
        """
        seq_resolver = self.element_to_type(
            list_template=None,
            date_type=date_type,
            datetime_type=datetime_type,
            enable_dict_type=True,
            dict_key_type=dict_key_type,
        )
        dict_set_resolver = self.element_to_type(
            list_template=None,
            date_type=date_type,
            datetime_type=datetime_type,
            enable_dict_type=narrow_dict_values,
            dict_key_type=dict_key_type,
        )
        resolved_dict_opener = (
            self._dict_opener_template.replace(
                "{key_type}",
                dict_key_type,
            )
            if dict_key_type
            else self._dict_opener_template
        )
        return TypeOpeners(
            seq=make_type_to_opener(
                element_to_type=seq_resolver,
                opener_template=self._sequence_opener_template,
            ),
            dict=make_type_to_opener(
                element_to_type=dict_set_resolver,
                opener_template=resolved_dict_opener,
            ),
            set=make_type_to_opener(
                element_to_type=dict_set_resolver,
                opener_template=(
                    set_opener_template
                    if set_opener_template is not None
                    else self._set_opener_template
                ),
            ),
        )
