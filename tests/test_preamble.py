"""Tests for preamble computation helpers."""

import datetime
from collections import OrderedDict
from typing import TYPE_CHECKING, cast

from ruamel.yaml.compat import ordereddict

from literalizer._preamble import (
    _has_union_in_type_hints,  # pyright: ignore[reportPrivateUsage]
    _list_merge_dicts,  # pyright: ignore[reportPrivateUsage]
    _structural_type_id,  # pyright: ignore[reportPrivateUsage]
)

if TYPE_CHECKING:
    from literalizer._types import Value


class TestListMergeDicts:
    """Tests for _list_merge_dicts."""

    def test_ordered_dict_elements_pooled(self) -> None:
        """Ordered-dict siblings are merged into one ordereddict."""
        od1 = ordereddict({"a": 1})
        od2 = ordereddict({"b": 2})
        result = _list_merge_dicts(
            elements=cast("list[Value]", [od1, od2]),
        )
        assert len(result) == 1
        assert isinstance(result[0], ordereddict)

    def test_standard_ordered_dict_elements_pooled(self) -> None:
        """Collections.OrderedDict siblings are also pooled."""
        od: Value = cast("Value", OrderedDict({"x": 1}))
        result = _list_merge_dicts(elements=[od, 42])
        assert isinstance(result[0], int)
        assert isinstance(result[1], ordereddict)

    def test_mixed_ordered_and_plain_dict(self) -> None:
        """Plain dicts and ordered dicts are pooled into separate
        slots.
        """
        od = ordereddict({"a": 1})
        plain: Value = cast("Value", {"b": 2})
        result = _list_merge_dicts(
            elements=cast("list[Value]", [od, plain]),
        )
        plain_slot, odict_slot = result
        assert isinstance(plain_slot, dict)
        assert isinstance(odict_slot, ordereddict)

    def test_no_dicts(self) -> None:
        """Non-dict elements pass through unchanged."""
        result = _list_merge_dicts(elements=[1, "hello", None])
        assert result == [1, "hello", None]

    def test_empty_input(self) -> None:
        """Empty list produces empty list."""
        assert _list_merge_dicts(elements=[]) == []


class TestStructuralTypeId:
    """Tests for _structural_type_id."""

    def test_bool(self) -> None:
        """True maps to 'bool'."""
        assert _structural_type_id(value=True) == "bool"

    def test_int(self) -> None:
        """An integer maps to 'int'."""
        assert _structural_type_id(value=1) == "int"

    def test_float(self) -> None:
        """A float maps to 'float'."""
        assert _structural_type_id(value=1.5) == "float"

    def test_str(self) -> None:
        """A string maps to 'str'."""
        assert _structural_type_id(value="hello") == "str"

    def test_bytes(self) -> None:
        """A bytes value maps to 'bytes'."""
        assert _structural_type_id(value=b"data") == "bytes"

    def test_datetime(self) -> None:
        """A datetime maps to 'datetime'."""
        assert (
            _structural_type_id(
                value=datetime.datetime(
                    year=2020,
                    month=1,
                    day=1,
                    tzinfo=datetime.UTC,
                )
            )
            == "datetime"
        )

    def test_date(self) -> None:
        """A date maps to 'date'."""
        assert (
            _structural_type_id(value=datetime.date(year=2020, month=1, day=1))
            == "date"
        )

    def test_none(self) -> None:
        """None maps to 'None'."""
        assert _structural_type_id(value=None) == "None"

    def test_empty_list(self) -> None:
        """An empty list maps to 'empty_list'."""
        assert _structural_type_id(value=[]) == "empty_list"

    def test_nonempty_list(self) -> None:
        """A list of ints maps to 'list(int)'."""
        assert _structural_type_id(value=cast("Value", [1, 2])) == "list(int)"

    def test_empty_set(self) -> None:
        """An empty set maps to 'empty_set'."""
        assert _structural_type_id(value=set()) == "empty_set"

    def test_nonempty_set(self) -> None:
        """A set of ints maps to 'set(int)'."""
        assert _structural_type_id(value=cast("Value", {1, 2})) == "set(int)"

    def test_empty_ordereddict(self) -> None:
        """An empty ordereddict maps to 'empty_odict'."""
        assert _structural_type_id(value=ordereddict()) == "empty_odict"

    def test_nonempty_ordereddict(self) -> None:
        """An ordereddict with int values maps to 'odict(int)'."""
        assert _structural_type_id(value=ordereddict({"a": 1})) == "odict(int)"

    def test_empty_dict(self) -> None:
        """An empty dict maps to 'empty_dict'."""
        assert _structural_type_id(value={}) == "empty_dict"

    def test_nonempty_dict(self) -> None:
        """A dict with int values maps to 'dict(int)'."""
        assert (
            _structural_type_id(value=cast("Value", {"a": 1})) == "dict(int)"
        )

    def test_list_with_merged_dicts(self) -> None:
        """Dicts in a list are pooled before computing the ID."""
        assert (
            _structural_type_id(value=cast("Value", [{"a": 1}, {"b": 2}]))
            == "list(dict(int))"
        )


class TestHasUnionInTypeHints:
    """Tests for _has_union_in_type_hints."""

    def test_dict_with_heterogeneous_annotated_values(self) -> None:
        """Dict with values of different annotated types is detected."""
        data: Value = cast("Value", {"a": [], "b": [1]})
        assert _has_union_in_type_hints(data=data) is True

    def test_dict_with_homogeneous_annotated_values(self) -> None:
        """Dict with values of the same annotated type has no union."""
        data: Value = {"a": cast("Value", []), "b": cast("Value", [])}
        assert _has_union_in_type_hints(data=data) is False

    def test_dict_with_non_annotated_values(self) -> None:
        """Dict whose values need no annotation returns False."""
        data: Value = cast("Value", {"a": 1})
        assert _has_union_in_type_hints(data=data) is False

    def test_list_without_annotation(self) -> None:
        """List with non-empty uniform scalars needs no annotation."""
        assert _has_union_in_type_hints(data=cast("Value", [1, 2])) is False

    def test_scalar_returns_false(self) -> None:
        """Scalars never produce a union."""
        assert _has_union_in_type_hints(data=42) is False

    def test_dict_with_nested_union(self) -> None:
        """Union in a nested list inside a dict value is detected."""
        data: Value = cast("Value", {"key": [[1], []]})
        assert _has_union_in_type_hints(data=data) is True
