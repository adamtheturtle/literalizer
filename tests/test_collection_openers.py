"""Tests for collection opener helpers.

These call an opener directly with values assembled in Python, which
is what makes them useful: the typing they check has to hold for a
shape the language then refuses, so there is no output for a golden
file to hold (issue #4699).
"""

import pytest

from literalizer._formatters.collection_openers import (
    TypedOpenerConfig,
    make_narrowed_empty_form,
    replace_optional_type_name,
    sequence_surrogate_set_open,
)
from literalizer._formatters.fallbacks import nonempty_or_default
from literalizer._formatters.type_inference import (
    BeyondI64,
    WideInt,
    single_concrete_type,
)
from literalizer._language import Language
from literalizer._types import OrderedMap, Scalar, Value
from literalizer.languages import Cpp, Haxe, Nim, Raku


def test_sequence_surrogate_set_open_delegates() -> None:
    """The semantic marker preserves its wrapped opener's behavior."""

    def opener(items: list[Value]) -> str:
        """Return an opener string that exposes the delegated items."""
        return f"sequence({len(items)})"

    marked_opener = sequence_surrogate_set_open(opener)

    assert marked_opener([1, "two", None]) == "sequence(3)"


def test_cpp_sequence_surrogate_set_helpers_remain_consistent() -> None:
    """C++'s rejected surrogate still has internally consistent typing."""

    def make_set(*items: Scalar) -> Value:
        """Return a recursively typed scalar set."""
        result: set[Scalar] = set(items)
        return result

    language = Cpp()
    nested_set = make_set(1, 2)

    assert (
        language.set_format_config.set_open([1, "two"])
        == "std::vector<std::variant<int, std::string>>{"
    )
    assert (
        language.set_format_config.set_open([nested_set, "two"])
        == "std::vector<std::variant<std::vector<int>, std::string>>{"
    )
    assert language.data_dependent_preamble([nested_set, "two"]) == (
        "#include <variant>",
    )
    assert language.data_dependent_preamble(make_set(1, "two")) == (
        "#include <variant>",
    )

    cpp14 = Cpp(language_version=Cpp.version_formats.CPP14)
    outer: Value = [nested_set, "two"]
    assert cpp14.heterogeneous_behavior.compute_wrap_ids(outer) == frozenset(
        {id(outer)}
    )


def test_cpp_record_ordered_map_opener_falls_back_without_one_record() -> None:
    """The opener retains its base fallback for unresolved record
    lists.
    """
    language = Cpp(
        heterogeneous_strategy=Cpp.heterogeneous_strategies.RECORD,
    )
    value = OrderedMap()
    first_record: dict[Scalar, Value] = {"id": 1}
    second_record: dict[Scalar, Value] = {"name": "example"}
    first: list[Value] = []
    second: list[Value] = []
    first.append(first_record)
    second.append(second_record)
    value["first"] = first
    value["second"] = second

    opener = language.ordered_map_format_config.ordered_map_open(value)

    assert opener.startswith("std::vector<std::pair<std::string, ")


@pytest.mark.parametrize(
    argnames="language",
    argvalues=[Cpp(), Haxe(), Nim(), Raku()],
)
def test_sequence_surrogate_set_entries_delegate(language: Language) -> None:
    """Rejected sequence surrogates retain their entry formatter
    contract.
    """
    assert language.format_set_entry(1, "one") == "one"


@pytest.mark.parametrize(
    argnames="resolved_type",
    argvalues=[None, "", "Element"],
)
def test_narrowed_empty_form_resolver_fallback(
    resolved_type: str | None,
) -> None:
    """Unknown and empty type names preserve the documented fallback."""
    opener = make_narrowed_empty_form(
        element_to_type=lambda _kind: resolved_type,
        template="List[{type}]()",
        fallback_type="Fallback",
    )
    expected_type = nonempty_or_default(
        value=resolved_type, default="Fallback"
    )
    assert opener([[1]]) == f"List[{expected_type}]()"
    assert opener([[1, "two"]]) == "List[Fallback]()"


def test_integer_type_fallbacks() -> None:
    """Unspecified wider integer types inherit the base integer type."""
    config = TypedOpenerConfig(
        str_type=None,
        bool_type=None,
        int_type="Integer",
        float_type=None,
        bytes_type=None,
        mixed_numeric_type=None,
        date_type=None,
        datetime_type=None,
        time_type=None,
        list_template="List[{type}]",
        sequence_opener_template="List[{type}](",
        dict_opener_template="Map[{type}](",
        set_opener_template="Set[{type}](",
        dict_type_template=None,
        fallback_value_type=None,
        wide_int_type=None,
        beyond_i64_type=None,
    )
    assert config.type_name(py_type=WideInt) == "Integer"
    assert config.type_name(py_type=BeyondI64) == "Integer"


@pytest.mark.parametrize(
    argnames=("names", "expected"),
    argvalues=[
        (set[str](), None),
        ({"Integer"}, "Integer"),
        ({"Any"}, None),
        ({"Integer", "String"}, None),
        ({"Any", "Integer"}, None),
    ],
)
def test_shared_concrete_type(names: set[str], expected: str | None) -> None:
    """A type can narrow only when every value shares a concrete type."""
    assert single_concrete_type(types=names, fallback_type="Any") == expected


@pytest.mark.parametrize(
    argnames=("template", "expected"),
    argvalues=[(None, None), ("", ""), ("List[Val]", "List[Custom]")],
)
def test_optional_declared_type_template(
    template: str | None, expected: str | None
) -> None:
    """Substitution preserves absent hints and empty configured hints."""
    assert (
        replace_optional_type_name(
            template=template, placeholder="Val", type_name="Custom"
        )
        == expected
    )
