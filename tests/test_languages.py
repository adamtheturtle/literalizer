"""Language-specific tests for literalizer converter."""

import dataclasses
import datetime
from typing import ClassVar

from literalizer import (
    InputFormat,
    NewVariable,
    literalize,
    literalize_call,
)
from literalizer.languages import (
    Cpp,
    Dart,
    Haskell,
    Python,
)

# Issue #2518 replaced the per-language ``datetime.time`` coverage
# shims with golden-file cases, but the
# :func:`~literalizer._preamble._structural_type_id`
# ``case datetime.time(): return "time"`` arm cannot ride the
# all-languages ``type_hints`` golden axis.  That arm only fires on
# the *Python* type-hint path: ``_has_union_in_type_hints`` walks
# nested lists with divergent inner shapes (e.g. ``[[t], []]``) and
# computes a structural id for the time scalar.  The empty inner list
# that forces the union walk also makes the Kotlin renderer emit a
# nested-time-list under ``ALWAYS`` whose rendered value type
# disagrees with its inferred type annotation; since the per-language
# lint CI compiles every golden fixture, an all-languages golden case
# for this input fails to build.  No other reachable input exercises
# the arm.  So, like the Dart ``skip_null_dict_values`` cases below,
# this Python-only arm stays a focused pytest test driven through the
# public API.


def test_cpp14_time_call_slot_uses_explicit_value_carrier() -> None:
    """C++14 wraps every temporal scalar in a heterogeneous call slot."""
    time = datetime.time(hour=9, minute=30)
    timestamp = datetime.datetime(
        year=2024,
        month=1,
        day=15,
        tzinfo=datetime.UTC,
    )
    behavior = Cpp(
        language_version=Cpp.version_formats.CPP14,
    ).heterogeneous_behavior

    wrap_ids = behavior.compute_call_slot_wrap_ids([time, timestamp, 1])

    assert id(time) in wrap_ids
    assert id(timestamp) in wrap_ids


def test_python_time_union_annotation_renders() -> None:
    """Python ``ALWAYS`` type hints render a nested time union.

    Covers the ``case datetime.time(): return "time"`` arm of
    :func:`~literalizer._preamble._structural_type_id`, which only runs
    when a typed Python variable declaration drives
    ``_has_union_in_type_hints`` to walk a list containing a time
    scalar.  See the module comment above for why this is not an
    all-languages golden-file case.
    """
    result = literalize(
        source="mixed = [[09:30:00], []]\n",
        input_format=InputFormat.TOML,
        language=Python(
            variable_type_hints=Python.variable_type_hints_formats.ALWAYS,
        ),
        variable_form=NewVariable(name="x", modifiers=frozenset()),
        wrap_in_file=True,
    )

    assert result.code


def test_haskell_explicit_epoch_datetime_uses_int_constructor() -> None:
    """Explicit Haskell epoch datetimes use the integer constructor.

    Issue #2519 migrated the production-language string-assertion tests
    in this module to golden-file cases, but this one cannot ride the
    golden harness for two independent reasons, so it stays a focused
    public-API pytest test (like the Dart ``skip_null_dict_values``
    cases below and the #2518 ``time`` union arm above):

    * It is the only thing that exercises the
      :attr:`~literalizer._literalize.LiteralizeResult.code` arm that
      joins ``body_preamble`` / ``pre_declaration_comments`` ahead of
      the declaration.  That arm only fires when ``wrap_in_file`` is
      ``False`` (otherwise the file wrapper absorbs the preamble), but
      every golden-file harness path calls ``literalize`` with
      ``wrap_in_file=True``, so no generated golden can reach it.
    * It pins the Haskell ``format_datetime`` override that fires only
      when ``datetime_format == EPOCH`` *and* ``numeric_style ==
      EXPLICIT``.  No variant axis crosses ``datetime_format`` with
      ``numeric_style``, so there is no golden configuration that
      activates the override.
    """
    result = literalize(
        source="ts: 2024-01-15T12:30:00+00:00\nname: hi\n",
        input_format=InputFormat.YAML,
        language=Haskell(
            datetime_format=Haskell.datetime_formats.EPOCH,
            numeric_style=Haskell.numeric_styles.EXPLICIT,
        ),
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=None,
    )

    assert not result.preamble
    assert result.code == (
        "data Val = HStr String | HMap [(String, Val)] | HInt Integer\n"
        "HMap [\n"
        '    ("ts", HInt 1705321800),\n'
        '    ("name", HStr "hi")\n'
        "    ]"
    )


# The null-filtering step in
# :func:`~literalizer._literalize._compute_dict_open_override` (the
# ``filtered_dicts`` comprehension) only runs when a language combines
# a value-type-sensitive ``dict_open`` (from
# :func:`~literalizer._formatters.collection_openers.typed_dict_open`)
# with ``skip_null_dict_values=True``. No production language pairs
# those two: the ``typed_dict_open`` languages (Dart, CSharp, Kotlin,
# Scala, Go) all keep nulls, while the ``skip_null_dict_values=True``
# languages (Java, Lua, Toml, Wren) all use ``fixed_dict_open`` whose
# constant opener never triggers widening. The golden-file suite
# iterates over :data:`~literalizer.languages.ALL_LANGUAGES` and has
# no way to inject a test-only language, so the two cases below define
# a Dart subclass inline to pin the divergent-types and matching-types
# outcomes of that filtering. The surrounding widening logic (override
# computation and the collapse-to-empty paths) is exercised by
# production golden cases with type-divergent dicts and is not
# re-asserted here.


def test_dart_skip_nulls_widens_across_null_masked_types() -> None:
    """Widening fires when null-masked dict value types differ.

    With ``skip_null_dict_values=True``, filtering ``None`` out of
    ``{"a": None, "b": 1}`` and ``{"a": "hello", "b": None}`` leaves
    dicts whose remaining value types diverge (``int`` vs. ``String``).
    The override must widen so both dicts share a ``dynamic`` opener.
    """

    @dataclasses.dataclass(frozen=True, kw_only=True)
    class DartSkipNulls(Dart):
        """Dart variant that drops null dict values."""

        skip_null_dict_values: ClassVar[bool] = True

    source = '[{"a": null, "b": 1}, {"a": "hello", "b": null}]'
    result = literalize(
        source=source,
        input_format=InputFormat.JSON,
        language=DartSkipNulls(),
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=None,
    )

    assert result.code == (
        "<Map<String, dynamic>>[\n"
        '    <String, dynamic>{"b": 1},\n'
        '    <String, dynamic>{"a": "hello"},\n'
        "]"
    )


def test_dart_skip_nulls_no_widening_when_filtered_dicts_match() -> None:
    """No override is needed when filtered dicts all share one opener.

    Null masks hide keys ``a`` and ``b`` in each dict, leaving only
    ``{"n": 1}`` and ``{"n": 2}``, both ``<String, int>``.  Widening
    would be redundant; each dict renders with its own inferred opener.
    """

    @dataclasses.dataclass(frozen=True, kw_only=True)
    class DartSkipNulls(Dart):
        """Dart variant that drops null dict values."""

        skip_null_dict_values: ClassVar[bool] = True

    source = '[{"a": null, "n": 1}, {"b": null, "n": 2}]'
    result = literalize(
        source=source,
        input_format=InputFormat.JSON,
        language=DartSkipNulls(),
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=None,
    )

    assert result.code == (
        "<Map<String, dynamic>>[\n"
        '    <String, int>{"n": 1},\n'
        '    <String, int>{"n": 2},\n'
        "]"
    )


def test_haskell_unknown_ref_values_keep_strip_behavior() -> None:
    """Haskell unknown refs do not contribute marker dict types."""
    result = literalize_call(
        source='[[{"$ref": "myList"}]]',
        input_format=InputFormat.JSON,
        language=Haskell(),
        target_function="process",
        parameter_names=["data"],
        ref_values={},
    )

    assert result.types_present == frozenset({list})
    assert result.body_preamble == ("data Val = HList [Val]",)


def test_haskell_unknown_ref_values_strip_top_level_ref() -> None:
    """Haskell strips unknown top-level refs even when ref_values is
    set.
    """
    result = literalize_call(
        source='{"$ref": "myList"}',
        input_format=InputFormat.JSON,
        language=Haskell(),
        target_function="process",
        parameter_names=["data"],
        per_element=False,
        ref_values={"other": 1},
    )

    assert result.types_present == frozenset({list})
    assert result.body_preamble == ("data Val = HList [Val]",)


def test_haskell_unknown_refs_strip_from_nested_preamble() -> None:
    """Haskell unknown nested refs do not shape preamble type
    inference.
    """
    result = literalize_call(
        source=(
            '[[{"$ref": "known"}, {"$ref": "missing"}, '
            '{"inner": {"$ref": "missing"}}]]'
        ),
        input_format=InputFormat.JSON,
        language=Haskell(),
        target_function="process",
        parameter_names=["a", "b", "c"],
        ref_values={"known": [1, {"nested": "value"}]},
    )

    assert result.body_preamble == (
        "data Val = HInt Integer | HStr String | HList [Val] | HMap "
        "[(String, Val)]",
        "instance Num Val where\n"
        "    fromInteger = HInt\n"
        '    _ + _ = error "not implemented"\n'
        '    _ * _ = error "not implemented"\n'
        '    abs _ = error "not implemented"\n'
        '    signum _ = error "not implemented"\n'
        "    negate (HInt n) = HInt (negate n)\n"
        '    negate _ = error "not implemented"',
    )


def test_haskell_without_ref_values_strips_top_level_ref() -> None:
    """Haskell's historical top-level ref strip behavior is retained."""
    result = literalize_call(
        source='{"$ref": "myList"}',
        input_format=InputFormat.JSON,
        language=Haskell(),
        target_function="process",
        parameter_names=["data"],
        per_element=False,
    )

    assert result.types_present == frozenset({list})
    assert result.body_preamble == ("data Val = HList [Val]",)


def test_haskell_without_ref_values_strips_per_element_ref() -> None:
    """Haskell per-element preamble inference skips ref marker
    elements.
    """
    result = literalize_call(
        source='[{"$ref": "myList"}]',
        input_format=InputFormat.JSON,
        language=Haskell(),
        target_function="process",
        parameter_names=["data"],
    )

    assert result.types_present == frozenset({list})
    assert result.body_preamble == ("data Val = HList [Val]",)
