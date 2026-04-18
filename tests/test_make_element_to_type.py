"""Unit tests for :func:`make_element_to_type`."""

from literalizer._formatters.collection_openers import make_element_to_type
from literalizer._formatters.type_inference import DictType


def test_none_fallback_value_type_returns_none_for_unresolvable_dict() -> None:
    """When ``fallback_value_type`` is ``None`` and a ``DictType`` has no
    resolvable value type, the resolver returns ``None`` rather than
    interpolating the string ``"None"`` into ``dict_type_template``.
    """
    resolver = make_element_to_type(
        str_type="string",
        bool_type="bool",
        int_type="int",
        float_type="float64",
        mixed_numeric_type="float64",
        bytes_type="string",
        date_type=None,
        datetime_type=None,
        list_template="[]{inner}",
        dict_type_template="map[string]{inner}",
        fallback_value_type=None,
    )

    assert resolver(DictType(value_type=None)) is None


def test_resolved_dict_value_type_uses_template() -> None:
    """When the dict value type resolves, the template is applied with
    the resolved inner type.
    """
    resolver = make_element_to_type(
        str_type="string",
        bool_type="bool",
        int_type="int",
        float_type="float64",
        mixed_numeric_type="float64",
        bytes_type="string",
        date_type=None,
        datetime_type=None,
        list_template="[]{inner}",
        dict_type_template="map[string]{inner}",
        fallback_value_type=None,
    )

    assert resolver(DictType(value_type=int)) == "map[string]int"
