"""Language-specific tests for literalizer converter."""

import dataclasses
import datetime
import json
import re
import textwrap
from typing import ClassVar

import pytest

from literalizer import (
    CollectionLayout,
    InputFormat,
    NewVariable,
    literalize,
    literalize_call,
)
from literalizer.exceptions import (
    NullInCollectionError,
    UnrepresentableSpecialFloatError,
)
from literalizer.languages import (
    Cobol,
    Dart,
    Elm,
    Fortran,
    Gleam,
    Haskell,
    Java,
    Matlab,
    Python,
    Rust,
    Sml,
)

COBOL = Cobol(
    date_format=Cobol.date_formats.ISO,
    datetime_format=Cobol.datetime_formats.ISO,
    bytes_format=Cobol.bytes_formats.HEX,
    sequence_format=Cobol.sequence_formats.SEQUENCE,
)
FORTRAN = Fortran(
    date_format=Fortran.date_formats.ISO,
    datetime_format=Fortran.datetime_formats.ISO,
    bytes_format=Fortran.bytes_formats.HEX,
    sequence_format=Fortran.sequence_formats.LIST,
    module_name="check",
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


def test_rust_epoch_datetime_tagged_enum_uses_integer_variant() -> None:
    """Epoch datetimes use the integer variant in heterogeneous Rust
    data.
    """
    result = literalize(
        source="ts: 2024-01-15T12:30:00+00:00\nname: hi\n",
        input_format=InputFormat.YAML,
        language=Rust(
            datetime_format=Rust.datetime_formats.EPOCH,
            heterogeneous_strategy=Rust.heterogeneous_strategies.TAGGED_ENUM,
        ),
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=None,
    )

    assert result.preamble == (
        "use std::collections::HashMap;",
        "enum Value {",
        "    I64(i64),",
        "    Str(&'static str),",
        "}",
    )
    assert result.code == (
        "HashMap::from([\n"
        '    ("ts", Value::I64(1705321800)),\n'
        '    ("name", Value::Str("hi")),\n'
        "])"
    )


_COLLAPSED_DART_MAP_COUNT = 2


@dataclasses.dataclass(frozen=True, kw_only=True)
class _DartSkipNulls(Dart):
    """Dart subclass that skips null dict values.

    The widening bug in
    :func:`~literalizer._literalize._compute_dict_open_override` only
    manifests when a language combines a value-type-sensitive
    ``dict_open`` (produced by
    :func:`~literalizer._formatters.collection_openers.typed_dict_open`)
    with ``skip_null_dict_values=True``.  No production language pairs
    those two today — the ``typed_dict_open`` languages (Dart, CSharp,
    Kotlin, Scala, Go) all keep nulls, while the
    ``skip_null_dict_values=True`` languages (Java, Lua, Toml, Wren)
    all use ``fixed_dict_open`` whose constant opener never triggers
    widening.

    That is also why these tests live here rather than in the
    ``tests/integration/cases/`` golden-file suite, which iterates over
    :data:`~literalizer.languages.ALL_LANGUAGES` and has no way to
    inject a test-only language.
    """

    skip_null_dict_values: ClassVar[bool] = True


def test_dart_skip_nulls_widens_across_null_masked_types() -> None:
    """Widening fires when null-masked dict value types differ.

    With ``skip_null_dict_values=True``, filtering ``None`` out of
    ``{"a": None, "b": 1}`` and ``{"a": "hello", "b": None}`` leaves
    dicts whose remaining value types diverge (``int`` vs. ``String``).
    The override must widen so both dicts share a ``dynamic`` opener.
    """
    source = '[{"a": null, "b": 1}, {"a": "hello", "b": null}]'
    result = literalize(
        source=source,
        input_format=InputFormat.JSON,
        language=_DartSkipNulls(),
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


def test_dart_skip_nulls_widens_when_one_dict_collapses_to_empty() -> None:
    """Widening fires when one dict collapses to ``{}`` and another is
    typed.

    ``{"a": None}`` filters to ``{}`` (fallback opener), while
    ``{"x": 1}`` filters to ``{"x": 1}`` (``<String, int>``).  The
    override must widen both to the fallback so the sequence is
    consistent.
    """
    source = '[{"a": null}, {"x": 1}]'
    result = literalize(
        source=source,
        input_format=InputFormat.JSON,
        language=_DartSkipNulls(),
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=None,
    )

    assert result.code == (
        "<Map<String, dynamic>>[\n"
        "    <String, dynamic>{},\n"
        '    <String, dynamic>{"x": 1},\n'
        "]"
    )


def test_dart_skip_nulls_no_widening_when_all_dicts_collapse_to_empty() -> (
    None
):
    """No override is needed when every dict collapses to ``{}``.

    Two all-null dicts filter to ``{}`` each.  Both render with the
    fallback ``<String, dynamic>{`` opener on their own, so widening
    would be a no-op.
    """
    source = '[{"a": null}, {"b": null}]'
    result = literalize(
        source=source,
        input_format=InputFormat.JSON,
        language=_DartSkipNulls(),
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=None,
    )

    assert (
        result.code.count("<String, dynamic>{}") == _COLLAPSED_DART_MAP_COUNT
    )


def test_dart_skip_nulls_no_widening_when_filtered_dicts_match() -> None:
    """No override is needed when filtered dicts all share one opener.

    Null masks hide keys ``a`` and ``b`` in each dict, leaving only
    ``{"n": 1}`` and ``{"n": 2}`` — both ``<String, int>``.  Widening
    would be redundant; each dict renders with its own inferred opener.
    """
    source = '[{"a": null, "n": 1}, {"b": null, "n": 2}]'
    result = literalize(
        source=source,
        input_format=InputFormat.JSON,
        language=_DartSkipNulls(),
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


def test_cobol_level_number_cap() -> None:
    """COBOL level numbers are capped at 49 for deeply nested
    structures.
    """
    yaml_string = (
        "a:\n"
        "  b:\n"
        "    c:\n"
        "      d:\n"
        "        e:\n"
        "          f:\n"
        "            g:\n"
        "              h:\n"
        "                i:\n"
        "                  value: deep\n"
    )
    result = literalize(
        source=yaml_string,
        input_format=InputFormat.YAML,
        language=COBOL,
        pre_indent_level=1,
        include_delimiters=True,
        variable_form=None,
    )

    assert result.code == (
        "\n"
        "        05 F-A.\n"
        "10 F-B.\n"
        "15 F-C.\n"
        "20 F-D.\n"
        "25 F-E.\n"
        "30 F-F.\n"
        "35 F-G.\n"
        "40 F-H.\n"
        "45 F-I.\n"
        '49 F-VALUE PIC X(4) VALUE "deep".\n'
        "    "
    )


def test_fortran_continuation_with_escaped_quote_and_comment() -> None:
    """Line continuation handles escaped quotes before inline comments."""
    yaml_string = "host: it's here  # a comment\nport: 80  # another\n"
    result = literalize(
        source=yaml_string,
        input_format=InputFormat.YAML,
        language=FORTRAN,
        pre_indent_level=0,
        variable_form=NewVariable(name="cfg"),
        include_delimiters=True,
    )

    assert result.code == (
        "type(fval_t) :: cfg\n"
        "cfg = fmap([fval_t :: &\n"
        "    fentry('host', fstr('it''s here')), &  ! a comment\n"
        "    fentry('port', fint(80_int64)) &  ! another\n"
        "])"
    )


def test_fortran_wrap_in_file_no_variable_form() -> None:
    """``literalize(wrap_in_file=True)`` without a variable form omits
    the program's ``contains`` section so the Fortran output stays
    valid.
    """
    result = literalize(
        source="42",
        input_format=InputFormat.JSON,
        language=Fortran(module_name="main"),
        wrap_in_file=True,
        variable_form=None,
    )
    assert result.code == (
        "module fval_m\n"
        "  use, intrinsic :: iso_fortran_env, only: int64\n"
        "  implicit none\n"
        "  type :: fval_t\n"
        "    integer :: t = 0\n"
        "  end type fval_t\n"
        "contains\n"
        "  function fnull() result(v); type(fval_t) :: v; end function\n"
        "  function fbool(b) result(v); logical, intent(in) :: b;"
        " type(fval_t) :: v; end function\n"
        "  function fint(n) result(v); integer(kind=int64), intent(in) :: n;"
        " type(fval_t) :: v; end function\n"
        "  function freal(x) result(v); real, intent(in) :: x;"
        " type(fval_t) :: v; end function\n"
        "  function fstr(s) result(v); character(len=*), intent(in) :: s;"
        " type(fval_t) :: v; end function\n"
        "  function flist(a) result(v); type(fval_t), intent(in) :: a(:);"
        " type(fval_t) :: v; end function\n"
        "  function fmap(a) result(v); type(fval_t), intent(in) :: a(:);"
        " type(fval_t) :: v; end function\n"
        "  function fset(a) result(v); type(fval_t), intent(in) :: a(:);"
        " type(fval_t) :: v; end function\n"
        "  function fentry(k, u) result(v);"
        " character(len=*), intent(in) :: k;"
        " type(fval_t), intent(in) :: u;"
        " type(fval_t) :: v; end function\n"
        "end module fval_m\n"
        "program main\n"
        "    use fval_m\n"
        "    implicit none\n"
        "    42_int64\n"
        "end program main"
    )


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


def test_java_list_rejects_null_elements() -> None:
    """Java's ``List.of()`` does not accept null elements."""
    spec = Java(
        sequence_format=Java.sequence_formats.LIST,
    )
    expected_msg = re.escape(
        pattern="Java's List.of() does not accept null elements"
        " (got 3 items, including null). "
        "Use sequence_format=ARRAY instead."
    )
    with pytest.raises(
        expected_exception=NullInCollectionError,
        match=f"^{expected_msg}$",
    ):
        literalize(
            source=json.dumps(obj=[1, None, "hello"]),
            input_format=InputFormat.JSON,
            language=spec,
            pre_indent_level=0,
            include_delimiters=True,
            variable_form=None,
        )


def test_gleam_call_stub_more_than_26_parameters() -> None:
    """Gleam type-var generation falls back to numeric suffixes past
    the 26-letter alphabet.

    Calls with 27 parameters exercise ``_gleam_type_var``'s numeric
    suffix branch, emitting ``z`` for the last single-letter slot and
    ``a1`` for the next one in the generated stub signature.
    """
    parameter_names = [f"p{i}" for i in range(27)]
    yaml_row = "\n".join(f"  - {i}" for i in range(26))
    source = f"---\n-\n{yaml_row}\n  - [100]\n"
    result = literalize_call(
        source=source,
        input_format=InputFormat.YAML,
        language=Gleam(),
        target_function="process",
        parameter_names=parameter_names,
        wrap_in_file=True,
    )
    signature_params = ", ".join(
        f"_p{i}: {chr(ord('a') + i)}" for i in range(26)
    )
    int_args = ", ".join(f"GInt({i})" for i in range(26))
    call_args = f"{int_args}, GList([GInt(100)])"
    expected = textwrap.dedent(
        text=f"""\
        pub type GVal {{
          GInt(Int)
          GList(List(GVal))
        }}
        pub fn process({signature_params}, _p26: a1) -> Nil {{ Nil }}

        pub fn main() {{
          process({call_args})
        }}""",
    )
    assert result.code == expected


@pytest.mark.parametrize(
    argnames="yaml_value",
    argvalues=[".inf", "-.inf", ".nan"],
    ids=["positive_infinity", "negative_infinity", "nan"],
)
def test_gleam_special_floats_raise(yaml_value: str) -> None:
    """Gleam raises ``UnrepresentableSpecialFloatError`` for non-finite
    floats.

    Gleam targets Erlang, which has no expression that evaluates to a
    non-finite float, so the literalizer surfaces this at literalize
    time rather than producing output that panics at ``gleam run``.
    """
    with pytest.raises(expected_exception=UnrepresentableSpecialFloatError):
        literalize(
            source=f"- {yaml_value}\n",
            input_format=InputFormat.YAML,
            language=Gleam(),
        )


def test_elm_call_wrap_in_file_multiline_dict_arg() -> None:
    """``wrap_in_file`` indents continuation lines without the
    ``_ =`` binding prefix.

    With ``collection_layout=MULTILINE``, a call argument that is a
    dict literal spans multiple lines. Only the top-level line of each
    call gets the ``_ = `` binding prefix; continuation lines must
    remain plain indented Elm.
    """
    result = literalize_call(
        source="- - a: 1\n    b: 2\n  - 42\n",
        input_format=InputFormat.YAML,
        language=Elm(),
        target_function="process",
        parameter_names=["arg1", "arg2"],
        wrap_in_file=True,
        collection_layout=CollectionLayout.MULTILINE,
    )
    expected = textwrap.dedent(
        text="""\
        module Check exposing (..)


        process : ( a, b ) -> ()
        process _ = ()
        type Val
            = EInt Int
            | EStr String
            | EList (List Val)
            | EDict (List ( String, Val ))


        main : Program () () Never
        main =
            let
                _ = process(EDict [
                    ("a", EInt 1),
                    ("b", EInt 2)
                    ], EInt 42)
            in
            Platform.worker
                { init = \\_ -> ( (), Cmd.none )
                , update = \\_ m -> ( m, Cmd.none )
                , subscriptions = \\_ -> Sub.none
                }""",
    )
    assert result.code == expected


def test_elm_wrap_in_file_preserves_empty_lines() -> None:
    """``wrap_in_file`` preserves blank lines from *content* verbatim
    rather than adding the ``_ =`` binding prefix or crashing on the
    empty string.

    An empty source list rendered with ``per_element=True`` yields an
    empty *content* string, which splits to a single empty entry; the
    blank branch must keep the resulting line blank so the surrounding
    ``let`` block scaffolding remains well-formed.
    """
    elm = Elm()
    wrapped = elm.wrap_in_file(
        content="",
        variable_name="",
        body_preamble=(),
    )
    expected = textwrap.dedent(
        text="""\
        module Check exposing (..)





        main : Program () () Never
        main =
            let

            in
            Platform.worker
                { init = \\_ -> ( (), Cmd.none )
                , update = \\_ m -> ( m, Cmd.none )
                , subscriptions = \\_ -> Sub.none
                }"""
    )
    assert wrapped == expected


def test_elm_wrap_calls_with_declarations_preserves_empty_lines() -> None:
    """``wrap_calls_with_declarations`` preserves blank lines from
    *calls* verbatim rather than adding the ``_ =`` binding prefix or
    crashing on the empty string.
    """
    elm = Elm()
    wrapped = elm.wrap_calls_with_declarations(
        declarations=(),
        calls="",
        body_preamble=(),
    )
    expected = textwrap.dedent(
        text="""\
        module Check exposing (..)





        main : Program () () Never
        main =
            let

            in
            Platform.worker
                { init = \\_ -> ( (), Cmd.none )
                , update = \\_ m -> ( m, Cmd.none )
                , subscriptions = \\_ -> Sub.none
                }"""
    )
    assert wrapped == expected


def test_elm_wrap_calls_with_declarations_multiline_continuation() -> None:
    """``wrap_calls_with_declarations`` indents continuation lines
    without the ``_ =`` binding prefix.

    The Elm output for a call whose argument is a multi-line
    collection must indent continuation lines plainly, leaving the
    ``_ = `` only on the call's top-level line.
    """
    elm = Elm()
    wrapped = elm.wrap_calls_with_declarations(
        declarations=("my_var : Val\nmy_var = EInt 42",),
        calls='process(EDict [\n    ("a", EInt 1),\n    ("b", EInt 2)\n    ])',
        body_preamble=(),
    )
    expected = textwrap.dedent(
        text="""\
        module Check exposing (..)





        main : Program () () Never
        main =
            let
                my_var : Val
                my_var = EInt 42
                _ = process(EDict [
                    ("a", EInt 1),
                    ("b", EInt 2)
                    ])
            in
            Platform.worker
                { init = \\_ -> ( (), Cmd.none )
                , update = \\_ m -> ( m, Cmd.none )
                , subscriptions = \\_ -> Sub.none
                }""",
    )
    assert wrapped == expected
