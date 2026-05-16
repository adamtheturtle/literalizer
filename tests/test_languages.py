"""Language-specific tests for literalizer converter."""

import dataclasses
import datetime
import textwrap
from typing import TYPE_CHECKING, ClassVar

import pytest

from literalizer import (
    ExistingVariable,
    IdentifierCase,
    InputFormat,
    Language,
    LanguageCls,
    NewVariable,
    literalize,
    literalize_call,
)
from literalizer.languages import (
    ALL_LANGUAGES,
    Cobol,
    CSharp,
    Dart,
    Dhall,
    FSharp,
    Go,
    Haskell,
    Java,
    Kotlin,
    Matlab,
    Nim,
    OCaml,
    Python,
    Rust,
    Sml,
    Swift,
    TypeScript,
)

if TYPE_CHECKING:
    from collections.abc import Mapping

    from literalizer._types import Scalar, ValueInput

COBOL = Cobol(
    date_format=Cobol.date_formats.ISO,
    datetime_format=Cobol.datetime_formats.ISO,
    bytes_format=Cobol.bytes_formats.HEX,
    sequence_format=Cobol.sequence_formats.SEQUENCE,
)


def test_python_datetime_whole_hour_offset_omits_minutes() -> None:
    """Whole-hour timezone offsets do not include zero minutes."""
    result = Python(
        date_format=Python.date_formats.PYTHON,
        datetime_format=Python.datetime_formats.PYTHON,
    ).format_datetime(
        datetime.datetime(
            year=2024,
            month=1,
            day=1,
            hour=12,
            tzinfo=datetime.timezone(offset=datetime.timedelta(hours=5)),
        )
    )

    assert result == (
        "datetime.datetime("
        "year=2024, "
        "month=1, "
        "day=1, "
        "hour=12, "
        "minute=0, "
        "second=0, "
        "tzinfo=datetime.timezone("
        "offset=datetime.timedelta(hours=5)"
        ")"
        ")"
    )


def test_haskell_explicit_epoch_datetime_uses_int_constructor() -> None:
    """Explicit Haskell epoch datetimes use the integer constructor."""
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


def test_sml_negative_epoch_datetime_parenthesizes_int_constructor() -> None:
    """Negative SML epoch datetimes wrap the converted integer."""
    result = literalize(
        source="1900-01-01T00:00:00+00:00",
        input_format=InputFormat.YAML,
        language=Sml(datetime_format=Sml.datetime_formats.EPOCH),
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=NewVariable(name="my_data"),
    )

    assert result.code == (
        "datatype val_t =\n"
        "    SInt of LargeInt.int\n"
        "val my_data : val_t = SInt (~2208988800)"
    )


def test_fsharp_call_binding_existing_variable_infers_type() -> None:
    """An F# ``ExistingVariable`` call binding rebinds with a plain
    inference-style ``let``.

    The literal-binding assignment injects a ``: Val`` annotation and a
    tagged-enum constructor (``FInt``) derived from the value's runtime
    type; a call expression has no such tag, so
    ``format_call_variable_assignment`` omits both and lets F# infer
    the return type.  It also never emits ``let mutable`` -- even under
    the ``LET_MUTABLE`` declaration style -- mirroring
    ``format_variable_assignment``, because an F# rebinding shadows
    with ``let``.  This output is not self-contained across the
    compiled languages (a bare assignment to an undeclared name), so it
    is asserted here rather than as a golden fixture.
    """
    for declaration_style in (
        FSharp.declaration_styles.LET,
        FSharp.declaration_styles.LET_MUTABLE,
    ):
        result = literalize_call(
            source="42",
            input_format=InputFormat.YAML,
            language=FSharp(declaration_style=declaration_style),
            target_function="make_widget",
            parameter_names=["count"],
            variable_form=ExistingVariable(name="my_data"),
            per_element=False,
        )

        assert result.code == (
            "type Val =\n    | FInt of int64\nlet my_data = make_widget(42)"
        )


def test_ocaml_call_binding_existing_variable_infers_type() -> None:
    """An OCaml ``ExistingVariable`` call binding rebinds with a bare,
    inference-style ``let``, matching the ``NewVariable`` form.

    The OCaml literal-binding assignment reuses the annotated,
    tag-wrapping ``let x : val_t = OInt ...`` declaration.  A call
    expression has no tag, so ``format_call_variable_assignment`` omits
    both the ``: val_t`` annotation and the constructor and lets OCaml
    infer the return type -- emitting ``let x = make_widget(...)``, not
    ``let x : val_t = OInt make_widget(...)``.  This output is not
    self-contained across the compiled languages (a bare assignment to
    an undeclared name), so it is asserted here rather than as a golden
    fixture.
    """
    ocaml = OCaml()
    expected = "type val_t =\n  | OInt of int\nlet my_data = make_widget(42)"
    new_result = literalize_call(
        source="42",
        input_format=InputFormat.YAML,
        language=ocaml,
        target_function="make_widget",
        parameter_names=["count"],
        variable_form=NewVariable(name="my_data"),
        per_element=False,
    )
    existing_result = literalize_call(
        source="42",
        input_format=InputFormat.YAML,
        language=ocaml,
        target_function="make_widget",
        parameter_names=["count"],
        variable_form=ExistingVariable(name="my_data"),
        per_element=False,
    )

    assert new_result.code == expected
    assert existing_result.code == expected


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


def test_matlab_dict_key_with_quote() -> None:
    """MATLAB struct keys containing double quotes are decoded correctly.

    The ``_decode_matlab_string_expr`` helper must handle ``""`` inside a
    double-quoted string, which represents a literal ``"`` character.
    """
    yaml_string = '{"hello \\"world\\"": 1}\n'
    result = literalize(
        source=yaml_string,
        input_format=InputFormat.YAML,
        language=Matlab(
            date_format=Matlab.date_formats.ISO,
            datetime_format=Matlab.datetime_formats.ISO,
            bytes_format=Matlab.bytes_formats.HEX,
            sequence_format=Matlab.sequence_formats.CELL_ARRAY,
        ),
        pre_indent_level=0,
        include_delimiters=False,
        variable_form=None,
    )

    assert result.code == "'hello \"world\"', 1"


def test_cobol_key_name_trailing_hyphen_after_truncation() -> None:
    """COBOL data names must not end with a hyphen after truncation."""
    long_key = "a-b-c-d-e-f-g-h-i-j-k-l-m-n-o"
    yaml_string = f'"{long_key}": 1\n'
    result = literalize(
        source=yaml_string,
        input_format=InputFormat.YAML,
        language=COBOL,
        pre_indent_level=1,
        include_delimiters=True,
        variable_form=None,
    )
    for line in result.code.splitlines():
        stripped = line.strip()
        if stripped.startswith("05 F-"):
            name = stripped.split()[1]
            assert not name.endswith("-")


def test_literalize_call_wrap_in_file_emits_stubs() -> None:
    """``wrap_in_file=True`` produces a self-contained file that
    defines the ``target_function`` so the output compiles on its own.
    """
    go_result = literalize_call(
        source="[[1, 2]]",
        input_format=InputFormat.JSON,
        language=Go(),
        target_function="process",
        parameter_names=["a", "b"],
        wrap_in_file=True,
    )
    expected_go = textwrap.dedent(
        text="""\
        package main
        func process(args ...any) any { return nil }

        func main() {
        process(1, 2)
        }""",
    )
    assert go_result.code == expected_go
    assert not go_result.preamble
    assert not go_result.body_preamble

    py_result = literalize_call(
        source="[[1, 2]]",
        input_format=InputFormat.JSON,
        language=Python(),
        target_function="process",
        parameter_names=["a", "b"],
        wrap_in_file=True,
    )
    expected_py = textwrap.dedent(
        text="""\
        from __future__ import annotations
        def process(*_args: object, **_kwargs: object) -> object: ...
        process(a=1, b=2)""",
    )
    assert py_result.code == expected_py
    assert not py_result.preamble


def test_literalize_call_wrap_in_file_transform_stub_returns_value() -> None:
    """When ``call_transform`` consumes the call result, the stub
    returns a value instead of ``void``.
    """
    result = literalize_call(
        source="[[1, 2]]",
        input_format=InputFormat.JSON,
        language=Python(),
        target_function="process",
        parameter_names=["a", "b"],
        call_transform=lambda ctx: f"emit({ctx.call})",
        wrap_in_file=True,
    )
    expected = textwrap.dedent(
        text="""\
        from __future__ import annotations
        def process(*_args: object, **_kwargs: object) -> object: ...
        emit(process(a=1, b=2))""",
    )
    assert result.code == expected


def test_dhall_quoted_dict_key() -> None:
    """Dhall backtick-label validation decodes simple escapes."""
    result = literalize(
        source='{"a\\"b": 1}\n',
        input_format=InputFormat.YAML,
        language=Dhall(),
        pre_indent_level=0,
        include_delimiters=True,
    )

    assert result.code == '{\n  `a"b` = +1,\n}'


def test_python_dotted_target_function_renders() -> None:
    """Dotted ``target_function`` succeeds when the language supports
    it.
    """
    result = literalize_call(
        source="[[1]]",
        input_format=InputFormat.JSON,
        language=Python(),
        target_function="module.fn",
        parameter_names=["a"],
    )
    assert result.code == "module.fn(a=1)"


def test_python_accepts_syntactic_non_idiomatic_ref_case() -> None:
    """Cases legal in the language but absent from the idiomatic
    preference list are accepted and rendered.

    Python's ``identifier_cases`` lists only ``SNAKE``, ``UPPER_SNAKE``,
    and ``PASCAL``; ``CAMEL`` is non-idiomatic but still a syntactically
    legal Python identifier.  Validation uses ``supported_ref_cases``,
    which exposes ``CAMEL``.
    """
    assert Python().identifier_cases == (
        IdentifierCase.SNAKE,
        IdentifierCase.UPPER_SNAKE,
        IdentifierCase.PASCAL,
    )
    assert Python().supported_ref_cases == frozenset(
        {
            IdentifierCase.SNAKE,
            IdentifierCase.UPPER_SNAKE,
            IdentifierCase.PASCAL,
            IdentifierCase.CAMEL,
        },
    )

    result = literalize(
        source='{"$ref": "user_obj"}',
        input_format=InputFormat.JSON,
        language=Python(),
        ref_case=IdentifierCase.CAMEL,
    )

    assert result.declaration_code == "userObj"


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
    inner_arg: Mapping[Scalar, ValueInput] = {"nested": "value"}
    known_arg: list[ValueInput] = [1, inner_arg]
    ref_values: dict[str, ValueInput] = {"known": known_arg}
    result = literalize_call(
        source=(
            '[[{"$ref": "known"}, {"$ref": "missing"}, '
            '{"inner": {"$ref": "missing"}}]]'
        ),
        input_format=InputFormat.JSON,
        language=Haskell(),
        target_function="process",
        parameter_names=["a", "b", "c"],
        ref_values=ref_values,
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


_SORTED_LANGUAGES: list[LanguageCls] = sorted(
    ALL_LANGUAGES,
    key=lambda c: c.__name__,
)


@pytest.mark.parametrize(
    argnames="lang_cls",
    argvalues=_SORTED_LANGUAGES,
    ids=[c.__name__ for c in _SORTED_LANGUAGES],
)
@pytest.mark.parametrize(
    argnames="source",
    argvalues=[
        "starts_at = 09:30:00\n",
        "starts_at = 09:30:15.123456\n",
    ],
)
def test_datetime_time_renders(lang_cls: LanguageCls, source: str) -> None:
    """Every language renders a ``datetime.time`` value without crashing.

    Coverage shim for the per-language ``format_time`` and
    ``datetime.time`` scalar-hint arms.  Delete once issue #2230 lands
    per-language golden-file cases for time scalars.
    """
    spec = lang_cls()
    variable_form = (
        NewVariable(name="my_data") if spec.supports_variable_names else None
    )
    wrap_in_file = (
        variable_form is not None or spec.supports_no_variable_wrap_in_file
    )
    result = literalize(
        source=source,
        input_format=InputFormat.TOML,
        language=spec,
        variable_form=variable_form,
        wrap_in_file=wrap_in_file,
    )
    assert result.code


def test_datetime_time_csharp_typed_decl_renders() -> None:
    """C# emits ``TimeOnly`` in a typed declaration for a
    ``datetime.time``.

    Covers the ``case datetime.time(): return "TimeOnly"`` arm of
    ``_csharp_scalar_type``, which only runs when modifiers force a
    typed declaration.  Delete with the rest of the time-coverage
    shims once issue #2230 lands.
    """
    result = literalize(
        source="starts_at = 09:30:00\n",
        input_format=InputFormat.TOML,
        language=CSharp(),
        variable_form=NewVariable(
            name="x",
            modifiers=frozenset({CSharp.modifiers.PUBLIC}),
        ),
        wrap_in_file=True,
    )
    assert "TimeOnly" in result.code


_ALWAYS_TYPE_HINT_LANGUAGES: tuple[tuple[str, Language], ...] = (
    (
        "Dart",
        Dart(
            variable_type_hints=Dart.variable_type_hints_formats.ALWAYS,
        ),
    ),
    (
        "Java",
        Java(
            variable_type_hints=Java.variable_type_hints_formats.ALWAYS,
        ),
    ),
    (
        "Kotlin",
        Kotlin(
            variable_type_hints=Kotlin.variable_type_hints_formats.ALWAYS,
        ),
    ),
    (
        "Python",
        Python(
            variable_type_hints=Python.variable_type_hints_formats.ALWAYS,
        ),
    ),
    (
        "Swift",
        Swift(
            variable_type_hints=Swift.variable_type_hints_formats.ALWAYS,
        ),
    ),
    (
        "TypeScript",
        TypeScript(
            variable_type_hints=(
                TypeScript.variable_type_hints_formats.ALWAYS
            ),
        ),
    ),
)


@pytest.mark.parametrize(
    argnames="spec",
    argvalues=[s for _, s in _ALWAYS_TYPE_HINT_LANGUAGES],
    ids=[name for name, _ in _ALWAYS_TYPE_HINT_LANGUAGES],
)
def test_datetime_time_always_type_hint_renders(spec: Language) -> None:
    """Languages with ALWAYS variable_type_hints render time scalars.

    Covers the ``case datetime.time():`` arm of each language's
    scalar-hint match (and Python's ``time_hint`` propagation).
    Delete with the rest of the time-coverage shims once issue #2230
    lands.
    """
    result = literalize(
        source="starts_at = 09:30:00\n",
        input_format=InputFormat.TOML,
        language=spec,
        variable_form=NewVariable(name="x"),
        wrap_in_file=True,
    )
    assert result.code


_HETEROGENEOUS_VARIANT_LANGUAGES: tuple[tuple[str, Language], ...] = (
    (
        "Rust",
        Rust(heterogeneous_strategy=Rust.heterogeneous_strategies.TAGGED_ENUM),
    ),
    (
        "Dhall",
        Dhall(
            heterogeneous_strategy=Dhall.heterogeneous_strategies.UNION_TYPE,
        ),
    ),
    (
        "Nim",
        Nim(
            heterogeneous_strategy=Nim.heterogeneous_strategies.OBJECT_VARIANT,
        ),
    ),
)


@pytest.mark.parametrize(
    argnames="spec",
    argvalues=[s for _, s in _HETEROGENEOUS_VARIANT_LANGUAGES],
    ids=[name for name, _ in _HETEROGENEOUS_VARIANT_LANGUAGES],
)
def test_datetime_time_heterogeneous_variant_renders(spec: Language) -> None:
    """Wrap-as-variant strategies emit a Time variant for
    ``datetime.time``.

    Covers the ``case datetime.time():`` arm of each language's
    heterogeneous-variant signature builder.  Delete with the rest of
    the time-coverage shims once issue #2230 lands.
    """
    result = literalize(
        source='mixed = [09:30:00, "hello"]\n',
        input_format=InputFormat.TOML,
        language=spec,
    )
    assert "Time" in result.code


def test_datetime_time_rust_lazy_static_renders() -> None:
    """Rust LAZY_STATIC infers ``&str`` for a ``datetime.time`` value.

    Covers the ``case datetime.time():`` arm of ``_rust_scalar_type``,
    which only runs when a typed declaration walks scalar values.
    Delete with the rest of the time-coverage shims once issue #2230
    lands.
    """
    result = literalize(
        source="val = 09:30:00\n",
        input_format=InputFormat.TOML,
        language=Rust(declaration_style=Rust.declaration_styles.LAZY_STATIC),
        variable_form=NewVariable(name="X"),
        wrap_in_file=True,
    )
    assert "HashMap<&str, &str>" in result.code


def test_datetime_time_union_annotation_renders() -> None:
    """Annotated heterogeneous sequence with a ``datetime.time`` element
    renders without crashing.

    Covers the ``case datetime.time(): return "time"`` arm of
    ``_structural_type_id`` in ``_preamble.py``, which only runs when a
    variable declaration drives ``_has_union_in_type_hints`` to walk a
    list containing a time scalar.  Delete with the rest of the
    time-coverage shims once issue #2230 lands.
    """
    result = literalize(
        source="mixed = [[09:30:00], []]\n",
        input_format=InputFormat.TOML,
        language=Python(
            variable_type_hints=Python.variable_type_hints_formats.ALWAYS,
        ),
        variable_form=NewVariable(name="x"),
        wrap_in_file=True,
    )
    assert result.code


def test_format_time_csharp_exact_millisecond_renders() -> None:
    """``new TimeOnly(...)`` handles times whose microseconds are exact ms.

    Covers the millisecond-only branch of ``_time_only_args`` where
    ``microsecond % 1000 == 0``.  Delete with the rest of the
    time-coverage shims once issue #2230 lands.
    """
    result = literalize(
        source="starts_at = 09:30:15.123000\n",
        input_format=InputFormat.TOML,
        language=CSharp(),
    )
    assert "new TimeOnly(9, 30, 15, 123)" in result.code


def test_format_time_local_time_of_with_microseconds_exact_ms() -> None:
    """``LocalTime.of(...)`` handles times whose microseconds are exact ms.

    Covers the ``microseconds`` branch of ``_time_only_args`` and the
    nanosecond-output branch of ``format_time_local_time_of``.  Delete
    with the rest of the time-coverage shims once issue #2230 lands.
    """
    result = literalize(
        source="starts_at = 09:30:15.123000\n",
        input_format=InputFormat.TOML,
        language=Java(),
        variable_form=NewVariable(name="x"),
        wrap_in_file=True,
    )
    assert "LocalTime.of(9, 30, 15, 123000000)" in result.code


def test_rust_tagged_enum_epoch_datetime_uses_integer_variant() -> None:
    """Epoch datetime variants use the configured integer type."""
    rust = Rust(
        datetime_format=Rust.datetime_formats.EPOCH,
        heterogeneous_strategy=Rust.heterogeneous_strategies.TAGGED_ENUM,
    )
    timestamp = datetime.datetime(
        year=2024,
        month=1,
        day=1,
        tzinfo=datetime.UTC,
    )
    result = literalize(
        source=f"- {timestamp.isoformat()}\n- 1\n",
        input_format=InputFormat.YAML,
        language=rust,
        variable_form=None,
    )

    assert result.preamble == (
        "enum Value {",
        "    I64(i64),",
        "    I32(i32),",
        "}",
    )
    assert result.code == (
        "vec![\n    Value::I64(1704067200),\n    Value::I32(1),\n]"
    )
