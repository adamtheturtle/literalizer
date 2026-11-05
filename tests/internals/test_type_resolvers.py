"""Type resolution retains independent options and runtime validation."""

from collections.abc import Callable
from dataclasses import dataclass

import pytest
from beartype.roar import BeartypeCallHintParamViolation

from literalizer._formatters.collection_openers import make_element_to_type
from literalizer._formatters.type_inference import DictType, ListType
from literalizer.languages.cpp import (
    _make_cpp_element_to_type,  # pyright: ignore[reportPrivateUsage]
)


@dataclass
class _MappingValueType:
    """A mutable custom callback whose configuration can change."""

    name: str

    def __call__(self, _element_type: type | ListType | DictType, /) -> str:
        """Read the current configuration on each invocation."""
        return self.name


def _element_resolver(
    *,
    int_type: str,
    dict_value_to_type: Callable[[type | ListType | DictType], str | None]
    | None,
) -> Callable[..., str | None]:
    """Build a recursive resolver with explicit scalar and map options."""
    return make_element_to_type(
        str_type="String",
        bool_type="Boolean",
        int_type=int_type,
        float_type="Float",
        bytes_type="Bytes",
        mixed_numeric_type="Float",
        date_type=None,
        datetime_type=None,
        time_type=None,
        list_template="List<{inner}>",
        enable_list_type=True,
        dict_type_template="Map<{inner}>",
        dict_value_to_type=dict_value_to_type,
        fallback_value_type=None,
        wide_int_type=None,
        beyond_i64_type=None,
    )


def test_resolvers_keep_independent_options_and_live_callbacks() -> None:
    """Do not cache custom callbacks or share their
    configuration.
    """
    custom = _MappingValueType(name="First")
    first = _element_resolver(int_type="Small", dict_value_to_type=custom)
    second = _element_resolver(int_type="Large", dict_value_to_type=None)
    same_options = _element_resolver(
        int_type="Small", dict_value_to_type=custom
    )
    assert same_options not in {first, second}
    descriptor = ListType(inner=DictType(value_type=int, values=(1,)))
    assert first(descriptor) == "List<Map<First>>"
    assert second(descriptor) == "List<Map<Large>>"
    custom.name = "Updated"
    assert first(descriptor) == "List<Map<Updated>>"
    assert second(descriptor) == "List<Map<Large>>"
    assert first(int) == "Small"
    assert second(int) == "Large"


@pytest.mark.parametrize(
    argnames="resolver",
    argvalues=[
        _element_resolver(int_type="Integer", dict_value_to_type=None),
        _make_cpp_element_to_type(
            enable_list_type=True,
            int_type="long long",
            date_type=None,
            datetime_type=None,
            dict_type_name="std::map",
        ),
    ],
    ids=["shared", "cpp"],
)
def test_resolver_rejects_invalid_descriptor(
    resolver: Callable[..., object],
) -> None:
    """Each returned callable retains its checked argument boundary."""
    with pytest.raises(expected_exception=BeartypeCallHintParamViolation):
        _ = resolver(object())
