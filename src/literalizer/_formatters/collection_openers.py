"""Collection opener functions and typed opener configuration."""

import datetime
import functools
from collections.abc import Callable
from dataclasses import dataclass

from beartype import beartype

from literalizer._formatters.type_inference import (
    DictType,
    ListType,
    MixedNumeric,
    infer_element_type,
)
from literalizer._types import Value


@beartype
def fixed_set_open(*, open_str: str) -> Callable[[list[Value]], str]:
    """Return a ``set_open`` callable that always returns *open_str*.

    Use this as ``set_open`` when the opening delimiter for sets
    is a fixed string that does not depend on the set contents.

    Example: ``fixed_set_open(open_str="{")([1, 2, 3])`` -> ``"{"``.
    """

    @beartype
    def _open(_items: list[Value]) -> str:
        """Return the fixed opening delimiter."""
        return open_str

    return _open


@beartype
def fixed_sequence_open(*, open_str: str) -> Callable[[list[Value]], str]:
    """Return a ``sequence_open`` callable that always returns *open_str*.

    Use this as ``sequence_open`` when the opening delimiter for sequences
    is a fixed string that does not depend on the sequence contents.

    Example: ``fixed_sequence_open(open_str="[")([1, 2, 3])`` -> ``"["``.
    """

    @beartype
    def _open(_items: list[Value]) -> str:
        """Return the fixed opening delimiter."""
        return open_str

    return _open


@beartype
def fixed_dict_open(*, open_str: str) -> Callable[[dict[str, Value]], str]:
    """Return a ``dict_open`` callable that always returns *open_str*.

    Use this as ``dict_open`` when the opening delimiter for dicts
    is a fixed string that does not depend on the dict contents.

    Example: ``fixed_dict_open(open_str="{")({"a": 1})`` -> ``"{"``.
    """

    @beartype
    def _open(_items: dict[str, Value]) -> str:
        """Return the fixed opening delimiter."""
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
            (datetime.date, date_type),
            (datetime.datetime, datetime_type),
        )
        if name is not None
    }

    @beartype
    def element_to_type(
        element_type: type | ListType | DictType,
    ) -> str | None:
        """Resolve a Python element type to a language type name."""
        if isinstance(element_type, DictType):
            if dict_type_template is None:
                return None
            resolved: str | None = None
            if element_type.value_type is not None:
                resolved = element_to_type(
                    element_type=element_type.value_type,
                )
            inner = resolved if resolved is not None else fallback_value_type
            return dict_type_template.format(inner=inner)
        if isinstance(element_type, ListType):
            inner = element_to_type(element_type=element_type.inner)
            if inner is None:
                return None
            return list_template.format(inner=inner)
        return scalar_types.get(element_type)

    return element_to_type


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

    @beartype
    def type_to_opener(element_type: type | ListType | DictType) -> str | None:
        """Resolve a Python element type to a collection opener."""
        type_name = element_to_type(element_type)
        if type_name is None:
            return None
        return opener_template.format(type_name=type_name)

    return type_to_opener


@beartype
def _typed_set_open(
    items: list[Value],
    *,
    type_to_opener: Callable[[type | ListType | DictType], str | None],
    fallback: str,
) -> str:
    """Infer the common element type and return the language-specific
    opener for sets.

    Uses direct ``type()`` checks on the Python runtime objects to
    determine the element type, then passes it to *type_to_opener*
    which returns the language-specific opening delimiter.  When
    inference is not possible or *type_to_opener* returns ``None``,
    *fallback* is returned instead.
    """
    element_type = infer_element_type(items=items)
    if element_type is None:
        return fallback
    return type_to_opener(element_type) or fallback


@beartype
def typed_set_open(
    *,
    type_to_opener: Callable[[type | ListType | DictType], str | None],
    fallback: str,
) -> Callable[[list[Value]], str]:
    """Return a ``set_open`` callable that infers the common
    element type and delegates to *type_to_opener*.

    When inference is not possible or *type_to_opener* returns
    ``None``, *fallback* is used instead.

    Example::

        def my_opener(element_type: type | ListType) -> str | None:
            if element_type is str:
                return "Set[String]("
            return None

        set_open = typed_set_open(
            type_to_opener=my_opener,
            fallback="Set[String](",
        )
    """
    return functools.partial(
        _typed_set_open,
        type_to_opener=type_to_opener,
        fallback=fallback,
    )


@beartype
def _typed_sequence_open(
    items: list[Value],
    *,
    type_to_opener: Callable[[type | ListType | DictType], str | None],
    fallback: str,
) -> str:
    """Infer the common element type and return the language-specific
    opener.

    Uses direct ``type()`` checks on the Python runtime objects
    to determine the element type, then passes it to
    *type_to_opener* which returns the language-specific opening
    delimiter.  When inference is not possible or *type_to_opener*
    returns ``None``, *fallback* is returned instead.
    """
    element_type = infer_element_type(items=items)
    if element_type is None:
        return fallback
    return type_to_opener(element_type) or fallback


@beartype
def typed_sequence_open(
    *,
    type_to_opener: Callable[[type | ListType | DictType], str | None],
    fallback: str,
) -> Callable[[list[Value]], str]:
    """Return a ``sequence_open`` callable that infers the common
    element type and delegates to *type_to_opener*.

    When inference is not possible or *type_to_opener* returns
    ``None``, *fallback* is used instead.

    Example::

        def my_opener(element_type: type | ListType) -> str | None:
            if element_type is str:
                return "[]string{"
            return None

        sequence_open = typed_sequence_open(
            type_to_opener=my_opener,
            fallback="[]any{",
        )
    """
    return functools.partial(
        _typed_sequence_open,
        type_to_opener=type_to_opener,
        fallback=fallback,
    )


@beartype
def _typed_dict_open(
    items: dict[str, Value],
    *,
    type_to_opener: Callable[[type | ListType | DictType], str | None],
    fallback: str,
) -> str:
    """Infer a common value type and return the language-specific
    opener.

    Treats the dict values as a list and infers a common element
    type, then passes it to *type_to_opener* which returns the
    language-specific opening delimiter.  When inference is not
    possible or *type_to_opener* returns ``None``, *fallback* is
    returned instead.
    """
    values = list(items.values())
    element_type = infer_element_type(items=values)
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
    return functools.partial(
        _typed_dict_open,
        type_to_opener=type_to_opener,
        fallback=fallback,
    )


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
            float_type=self._float_type,
            bytes_type=self._bytes_type,
            mixed_numeric_type=self._mixed_numeric_type,
            date_type=date_type or self._date_type,
            datetime_type=datetime_type or self._datetime_type,
            list_template=list_template or self._list_template,
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
                    set_opener_template or self._set_opener_template
                ),
            ),
        )
