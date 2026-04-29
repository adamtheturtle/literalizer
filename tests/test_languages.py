"""Language-specific tests for literalizer converter."""

import dataclasses
import enum
import json
import re
import textwrap
from functools import cached_property
from typing import ClassVar

import pytest
from pygments.lexers import find_lexer_class_by_name

import literalizer.languages
from literalizer import (
    BothVariableForms,
    IdentifierCase,
    InputFormat,
    NewVariable,
    literalize,
    literalize_call,
)
from literalizer._language import (
    NO_HETEROGENEOUS_BEHAVIOR,
    HeterogeneousBehavior,
    LanguageCls,
    StubReturn,
)
from literalizer._types import Value
from literalizer.exceptions import (
    CallArgNotSupportedError,
    CallsNotSupportedByLanguageError,
    CallsNotSupportedByToolError,
    NullInCollectionError,
    ParameterCountMismatchError,
    PerElementNotListError,
    UnrepresentableSpecialFloatError,
    UnsupportedIdentifierCaseError,
    WrapCombinedInFileNotSupportedError,
)
from literalizer.languages import (
    Bash,
    Cobol,
    Dart,
    Fortran,
    FSharp,
    Gleam,
    Go,
    Java,
    JavaScript,
    Jsonnet,
    Matlab,
    Python,
    Racket,
    Yaml,
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
FSHARP = FSharp(module_name="check")


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
    expected = textwrap.dedent(
        text="""\
        <Map<String, dynamic>>[
            <String, dynamic>{"b": 1},
            <String, dynamic>{"a": "hello"},
        ]""",
    )
    assert result.code == expected


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
    expected = textwrap.dedent(
        text="""\
        <Map<String, dynamic>>[
            <String, dynamic>{},
            <String, dynamic>{"x": 1},
        ]""",
    )
    assert result.code == expected


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
    expected = textwrap.dedent(
        text="""\
        <Map<String, dynamic>>[
            <String, dynamic>{},
            <String, dynamic>{},
        ]""",
    )
    assert result.code == expected


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
    expected = textwrap.dedent(
        text="""\
        <Map<String, dynamic>>[
            <String, int>{"n": 1},
            <String, int>{"n": 2},
        ]""",
    )
    assert result.code == expected


def _flag_top_dict(data: Value) -> frozenset[int]:
    """Return a set containing *data*'s id.

    The test input is always a top-level dict, so flagging it
    guarantees :func:`~literalizer._literalize._maybe_wrap_child`
    dispatches to the language's ``wrap_scalar``.
    """
    return frozenset({id(data)})


@dataclasses.dataclass(frozen=True, kw_only=True)
class _IdentityWrapPython(Python):
    """Python subclass whose :attr:`heterogeneous_behavior` flags
    every dict but reuses
    :data:`~literalizer._language.NO_HETEROGENEOUS_BEHAVIOR`'s
    identity ``wrap_scalar``.

    Used to exercise the identity ``wrap_scalar`` path through a real
    ``literalize`` call — a scenario no production language triggers.
    """

    @cached_property
    def heterogeneous_behavior(self) -> HeterogeneousBehavior:
        """Return an identity-wrap behavior that flags every dict."""
        return dataclasses.replace(
            NO_HETEROGENEOUS_BEHAVIOR,
            compute_wrap_ids=_flag_top_dict,
        )


def test_identity_wrap_scalar_leaves_formatted_output_unchanged() -> None:
    """A language that flags containers but keeps
    :data:`~literalizer._language.NO_HETEROGENEOUS_BEHAVIOR`'s
    identity ``wrap_scalar`` produces output identical to the same
    language without any wrapping.
    """
    source = '{"a": 1, "b": "x"}'
    base = literalize(
        source=source,
        input_format=InputFormat.JSON,
        language=Python(),
    )
    wrapped = literalize(
        source=source,
        input_format=InputFormat.JSON,
        language=_IdentityWrapPython(),
    )
    assert wrapped.code == base.code


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
    yaml_string = textwrap.dedent(
        text="""\
        a:
          b:
            c:
              d:
                e:
                  f:
                    g:
                      h:
                        i:
                          value: deep
        """
    )
    result = literalize(
        source=yaml_string,
        input_format=InputFormat.YAML,
        language=COBOL,
        pre_indent_level=1,
        include_delimiters=True,
        variable_form=None,
    )
    expected = (
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
    assert result.code == expected


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
    expected = textwrap.dedent(
        text="""\
        type(fval_t) :: cfg
        cfg = fmap([fval_t :: &
            fentry('host', fstr('it''s here')), &  ! a comment
            fentry('port', fint(80_int64)) &  ! another
        ])""",
    )
    assert result.code == expected


def test_fsharp_scalar_very_large_int_uses_bigint_suffix() -> None:
    """Bare F# scalar integer values above i64 range use the ``I``
    suffix.
    """
    result = literalize(
        source="9223372036854775808",
        input_format=InputFormat.JSON,
        language=FSHARP,
        pre_indent_level=0,
        include_delimiters=False,
        variable_form=None,
    )
    expected = textwrap.dedent(
        text="""\
        type Val =
            | FInt of bigint
        9223372036854775808I"""
    )
    assert result.code == expected


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


_SORTED_LANGUAGES: list[LanguageCls] = sorted(
    literalizer.languages.ALL_LANGUAGES,
    key=lambda c: c.__name__,
)


_UNSUPPORTED_COMBINED_LANGUAGES: list[LanguageCls] = [
    cls
    for cls in _SORTED_LANGUAGES
    if not any(
        style.value.supports_redefinition for style in cls.DeclarationStyles
    )
]


@pytest.mark.parametrize(
    argnames="language_cls",
    argvalues=_SORTED_LANGUAGES,
    ids=[c.__name__ for c in _SORTED_LANGUAGES],
)
def test_language_version_is_non_empty_string(
    *,
    language_cls: LanguageCls,
) -> None:
    """Every language class declares a non-empty ``language_version``."""
    assert isinstance(language_cls.language_version, str)
    assert language_cls.language_version


@pytest.mark.parametrize(
    argnames="language_cls",
    argvalues=_SORTED_LANGUAGES,
    ids=[c.__name__ for c in _SORTED_LANGUAGES],
)
def test_pygments_name_is_valid(
    *,
    language_cls: LanguageCls,
) -> None:
    """Every language's ``pygments_name`` is recognized by Pygments."""
    if language_cls.pygments_name is None:
        return
    # Raises ClassNotFound if the name is not a valid Pygments alias.
    find_lexer_class_by_name(_alias=language_cls.pygments_name)


@pytest.mark.parametrize(
    argnames="language_cls",
    argvalues=_SORTED_LANGUAGES,
    ids=[c.__name__ for c in _SORTED_LANGUAGES],
)
def test_protocol_properties_accessible(
    *,
    language_cls: LanguageCls,
) -> None:
    """Every Language exposes its Protocol attributes for any language.

    Many ``@cached_property`` members are only exercised by tests for
    the subset of languages that opt in to a feature (variable
    reassignment, type-hint preambles, call stubs).  Accessing every
    documented member here keeps coverage at 100% across the matrix.
    """
    spec = language_cls()
    assert callable(spec.format_call_stub)
    assert callable(spec.format_call_preamble_stub)
    assert callable(spec.format_call_target)
    assert callable(spec.format_call_ref_identifier)
    assert callable(spec.format_variable_declaration)
    assert callable(spec.format_variable_assignment)
    assert callable(spec.type_hint_collection_preamble_lines)
    assert isinstance(spec.scalar_body_preamble, dict)


@pytest.mark.parametrize(
    argnames="language_cls",
    argvalues=_SORTED_LANGUAGES,
    ids=[c.__name__ for c in _SORTED_LANGUAGES],
)
def test_format_enumeration_properties(
    language_cls: LanguageCls,
) -> None:
    """Every language exposes iterable format-enumeration properties."""
    spec = language_cls()
    assert issubclass(spec.bytes_formats, enum.Enum)
    assert len(spec.bytes_formats) >= 1
    assert issubclass(spec.sequence_formats, enum.Enum)
    assert len(spec.sequence_formats) >= 1
    assert issubclass(spec.set_formats, enum.Enum)
    assert len(spec.set_formats) >= 1
    assert issubclass(spec.date_formats, enum.Enum)
    assert len(spec.date_formats) >= 1
    assert issubclass(spec.datetime_formats, enum.Enum)
    assert len(spec.datetime_formats) >= 1
    assert issubclass(spec.comment_formats, enum.Enum)
    assert len(spec.comment_formats) >= 1
    assert issubclass(spec.declaration_styles, enum.Enum)
    assert len(spec.declaration_styles) >= 1
    assert issubclass(spec.dict_formats, enum.Enum)
    assert len(spec.dict_formats) >= 1
    assert issubclass(spec.float_formats, enum.Enum)
    assert len(spec.float_formats) >= 1
    assert issubclass(spec.integer_formats, enum.Enum)
    assert len(spec.integer_formats) >= 1
    assert issubclass(spec.numeric_separators, enum.Enum)
    assert len(spec.numeric_separators) >= 1
    assert issubclass(spec.numeric_styles, enum.Enum)
    assert len(spec.numeric_styles) >= 1
    assert issubclass(spec.string_formats, enum.Enum)
    assert len(spec.string_formats) >= 1
    assert issubclass(spec.trailing_commas, enum.Enum)
    assert len(spec.trailing_commas) >= 1
    assert issubclass(spec.line_endings, enum.Enum)
    assert len(spec.line_endings) >= 1
    assert issubclass(spec.call_styles, enum.Enum)


def test_python_no_any_import_when_all_defaults_overridden() -> None:
    """When all Python default collection types are non-Any, the
    ``from typing import Any`` import is not emitted.
    """
    spec = Python(
        default_set_element_type="str",
        default_sequence_element_type="str",
        default_dict_value_type="str",
        default_dict_key_type="str",
    )
    result = literalize(
        source="{}\n",
        input_format=InputFormat.YAML,
        language=spec,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=NewVariable(name="my_data"),
    )
    assert result.code == "my_data: dict[str, str] = {}"
    assert not result.preamble


def test_literalize_call_wrap_in_file_emits_stubs() -> None:
    """``wrap_in_file=True`` produces a self-contained file that
    defines the ``target_function`` so the output compiles on its own.
    """
    # Go: stub lands in the file-scope preamble (Go can't declare
    # functions inside ``main``).  The static ``package main`` preamble
    # is also prepended.
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
        process(1, 2);
        }""",
    )
    assert go_result.code == expected_go
    assert not go_result.preamble
    assert not go_result.body_preamble
    # Python: stub lands inside the wrapper (no language wrapper here,
    # so it sits above the call) and covers the no-static-preamble
    # branch.
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
        call_transform=lambda c: f"emit({c})",
        wrap_in_file=True,
    )
    # ``process`` still gets a value-returning stub; ``emit`` is out of
    # scope here — callers that use ``call_transform`` are responsible
    # for providing their own wrapper definition.
    expected = textwrap.dedent(
        text="""\
        def process(*_args: object, **_kwargs: object) -> object: ...
        emit(process(a=1, b=2))""",
    )
    assert result.code == expected


def test_gleam_call_preamble_stub_many_parameters() -> None:
    """Gleam call stubs handle more than 26 parameters.

    ``_gleam_type_var`` falls back to numeric suffixes past the 26-letter
    alphabet, so a 27-parameter call must emit a ``z`` for the last
    single-letter slot and an ``a1`` for the next one.
    """
    params = [f"p{i}" for i in range(27)]
    (line,) = Gleam().format_call_preamble_stub(
        ("target",),
        params,
        StubReturn.VOID,
    )
    assert "_p25: z" in line
    assert "_p26: a1" in line


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


def test_both_variable_forms_without_wrap_in_file_raises() -> None:
    """BothVariableForms without wrap_in_file=True raises ValueError."""
    expected_msg = "BothVariableForms requires wrap_in_file=True"
    with pytest.raises(
        expected_exception=ValueError,
        match=f"^{re.escape(pattern=expected_msg)}$",
    ):
        literalize(
            source="42",
            input_format=InputFormat.JSON,
            language=Python(),
            variable_form=BothVariableForms(name="x"),
        )


def test_both_variable_forms_without_redefinition_support_raises() -> None:
    """BothVariableForms raises when the declaration_style does not
    support redefinition.
    """
    expected = (
        "BothVariableForms requires a declaration_style that supports "
        "redefinition; 'ASSIGN' does not."
    )
    with pytest.raises(
        expected_exception=ValueError,
        match=rf"^{re.escape(pattern=expected)}$",
    ):
        literalize(
            source="42",
            input_format=InputFormat.JSON,
            language=Yaml(),
            variable_form=BothVariableForms(name="x"),
            wrap_in_file=True,
        )


@pytest.mark.parametrize(
    argnames="language_cls",
    argvalues=_UNSUPPORTED_COMBINED_LANGUAGES,
    ids=[c.__name__ for c in _UNSUPPORTED_COMBINED_LANGUAGES],
)
def test_wrap_combined_in_file_unsupported_raises(
    *,
    language_cls: LanguageCls,
) -> None:
    """Check wrap_combined_in_file raises when redefinition is unsupported.

    :func:`literalizer.literalize` rejects ``BothVariableForms`` for
    these languages before reaching ``wrap_combined_in_file``, but the
    method itself must still satisfy the :class:`Language` protocol.
    """
    with pytest.raises(expected_exception=WrapCombinedInFileNotSupportedError):
        language_cls().wrap_combined_in_file(
            declaration="x = 1",
            assignment="x = 2",
            variable_name="x",
            body_preamble=(),
        )


def test_literalize_call_per_element_non_list_raises() -> None:
    """Literalize_call raises PerElementNotListError for non-list."""
    with pytest.raises(
        expected_exception=PerElementNotListError,
        match=r"^per_element=True requires a top-level list, got str$",
    ):
        literalize_call(
            source='"hello"',
            input_format=InputFormat.JSON,
            language=Python(),
            target_function="process",
            parameter_names=["value"],
            per_element=True,
        )


def test_literalize_call_parameter_count_too_few_raises() -> None:
    """Literalize_call raises when fewer parameter_names than values."""
    with pytest.raises(
        expected_exception=ParameterCountMismatchError,
        match=r"^Expected 1 parameters but got 2 values$",
    ):
        literalize_call(
            source="[[1, 2]]",
            input_format=InputFormat.JSON,
            language=Python(),
            target_function="process",
            parameter_names=["a"],
        )


def test_literalize_call_parameter_count_too_many_raises() -> None:
    """Literalize_call raises when more parameter_names than values."""
    with pytest.raises(
        expected_exception=ParameterCountMismatchError,
        match=r"^Expected 3 parameters but got 2 values$",
    ):
        literalize_call(
            source="[[1, 2]]",
            input_format=InputFormat.JSON,
            language=Python(),
            target_function="process",
            parameter_names=["a", "b", "c"],
        )


def test_literalize_call_parameter_count_mismatch_object_style() -> None:
    """Literalize_call raises ParameterCountMismatchError for object
    call styles (e.g. JavaScript) too.
    """
    with pytest.raises(
        expected_exception=ParameterCountMismatchError,
        match=r"^Expected 2 parameters but got 1 values$",
    ):
        literalize_call(
            source="[[1]]",
            input_format=InputFormat.JSON,
            language=JavaScript(),
            target_function="process",
            parameter_names=["a", "b"],
        )


def test_literalize_call_parameter_count_mismatch_prefix_style() -> None:
    """Literalize_call raises ParameterCountMismatchError for prefix
    (S-expression) call styles like Racket.
    """
    with pytest.raises(
        expected_exception=ParameterCountMismatchError,
        match=r"^Expected 2 parameters but got 1 values$",
    ):
        literalize_call(
            source="[[1]]",
            input_format=InputFormat.JSON,
            language=Racket(),
            target_function="process",
            parameter_names=["a", "b"],
        )


def test_literalize_call_parameter_count_mismatch_later_row() -> None:
    """Literalize_call raises when a later per_element row has a
    different value count than parameter_names.
    """
    with pytest.raises(
        expected_exception=ParameterCountMismatchError,
        match=r"^Expected 2 parameters but got 1 values$",
    ):
        literalize_call(
            source="[[1, 2], [3]]",
            input_format=InputFormat.JSON,
            language=Python(),
            target_function="process",
            parameter_names=["a", "b"],
        )


def test_literalize_call_language_without_calls_raises() -> None:
    """Literalize_call raises CallsNotSupportedByLanguageError for a
    data-format language (Yaml) that has no call syntax.
    """
    with pytest.raises(
        expected_exception=CallsNotSupportedByLanguageError,
        match=r"^Yaml has no function call syntax$",
    ):
        literalize_call(
            source="[[1, 2]]",
            input_format=InputFormat.JSON,
            language=Yaml(),
            target_function="f",
            parameter_names=["a", "b"],
        )


def test_literalize_call_language_without_calls_per_element_false() -> None:
    """Literalize_call raises CallsNotSupportedByLanguageError for a
    data-format language with per_element=False.
    """
    with pytest.raises(
        expected_exception=CallsNotSupportedByLanguageError,
        match=r"^Yaml has no function call syntax$",
    ):
        literalize_call(
            source="[1, 2]",
            input_format=InputFormat.JSON,
            language=Yaml(),
            target_function="f",
            parameter_names=["data"],
            per_element=False,
        )


def test_literalize_call_tool_unsupported_language_raises() -> None:
    """Literalize_call raises CallsNotSupportedByToolError for a
    programming language whose calls literalizer has not yet
    implemented (Cobol).
    """
    with pytest.raises(
        expected_exception=CallsNotSupportedByToolError,
        match=(
            r"^literalizer does not support function call rendering "
            r"for Cobol$"
        ),
    ):
        literalize_call(
            source="[[1, 2]]",
            input_format=InputFormat.JSON,
            language=COBOL,
            target_function="f",
            parameter_names=["a", "b"],
        )


def test_literalize_call_tool_unsupported_language_per_element_false() -> None:
    """Literalize_call raises CallsNotSupportedByToolError for a
    programming language with per_element=False.
    """
    with pytest.raises(
        expected_exception=CallsNotSupportedByToolError,
        match=(
            r"^literalizer does not support function call rendering "
            r"for Cobol$"
        ),
    ):
        literalize_call(
            source="[1, 2]",
            input_format=InputFormat.JSON,
            language=COBOL,
            target_function="f",
            parameter_names=["data"],
            per_element=False,
        )


def test_literalize_call_bash_rejects_list_arg() -> None:
    """Bash raises ``CallArgNotSupportedError`` when a call argument
    is a list, because ``cmd (1 2 3)`` parses as ``cmd`` followed by
    a nested ``(...)`` child-process group, not an inline array
    literal.
    """
    with pytest.raises(
        expected_exception=CallArgNotSupportedError,
        match=(
            r"^Bash cannot accept this value as a call argument: "
            r"list values have no inline literal form"
        ),
    ):
        literalize_call(
            source="[[[1, 2, 3]]]",
            input_format=InputFormat.JSON,
            language=Bash(),
            target_function="cmd",
            parameter_names=["items"],
        )


def test_literalize_call_bash_rejects_dict_arg() -> None:
    """Bash raises ``CallArgNotSupportedError`` when a call argument
    is a dict, because Bash associative-array literals cannot appear
    as a single positional argument.
    """
    with pytest.raises(
        expected_exception=CallArgNotSupportedError,
        match=(
            r"^Bash cannot accept this value as a call argument: "
            r"dict values have no inline literal form"
        ),
    ):
        literalize_call(
            source='[[{"k": 1}]]',
            input_format=InputFormat.JSON,
            language=Bash(),
            target_function="cmd",
            parameter_names=["m"],
        )


def test_literalize_call_bash_rejects_list_arg_per_element_false() -> None:
    """Bash's call-argument guard also fires on the
    ``per_element=False`` path where the whole parsed value is passed
    as a single argument.
    """
    with pytest.raises(
        expected_exception=CallArgNotSupportedError,
        match=r"^Bash cannot accept this value as a call argument",
    ):
        literalize_call(
            source="[1, 2, 3]",
            input_format=InputFormat.JSON,
            language=Bash(),
            target_function="cmd",
            parameter_names=["items"],
            per_element=False,
        )


def test_literalize_call_arg_ref_all_refs() -> None:
    """A call whose every argument is a ref still renders correctly;
    the empty non-ref list must not break wrap-id computation.
    """
    result = literalize_call(
        source='[[{"$ref": "a"}, {"$ref": "b"}]]',
        input_format=InputFormat.JSON,
        language=Go(),
        target_function="combine",
        parameter_names=["x", "y"],
    )
    assert result.code == "combine(a, b);"


def test_literalize_call_arg_ref_top_level_element() -> None:
    """A bare ref marker at the top level of a per_element list works
    without an inner list wrapper; each element becomes a one-argument
    call whose argument is the referenced identifier.
    """
    result = literalize_call(
        source='[{"$ref": "a"}, {"$ref": "b"}]',
        input_format=InputFormat.JSON,
        language=Go(),
        target_function="run",
        parameter_names=["x"],
    )
    assert result.code == "run(a);\nrun(b);"


def test_literalize_call_arg_ref_per_element_false() -> None:
    """A top-level ref in per_element=False mode emits the identifier
    as the single argument.
    """
    result = literalize_call(
        source='{"$ref": "payload"}',
        input_format=InputFormat.JSON,
        language=Python(),
        target_function="publish",
        parameter_names=["body"],
        per_element=False,
    )
    assert result.code == "publish(body=payload)"


def test_literalize_call_arg_ref_non_ref_dict_still_literalized() -> None:
    """A dict without the exact ``{"$ref": str}`` shape renders as a
    normal dict literal (e.g. two-key dicts, or non-string ``$ref``
    values).
    """
    two_key = literalize_call(
        source='[[{"$ref": "x", "extra": 1}]]',
        input_format=InputFormat.JSON,
        language=Python(),
        target_function="process",
        parameter_names=["data"],
    )
    assert two_key.code == 'process(data={"$ref": "x", "extra": 1})'
    non_string_ref = literalize_call(
        source='[[{"$ref": 42}]]',
        input_format=InputFormat.JSON,
        language=Python(),
        target_function="process",
        parameter_names=["data"],
    )
    assert non_string_ref.code == 'process(data={"$ref": 42})'


def test_literalize_call_arg_ref_parameter_count_still_validated() -> None:
    """Refs count as arguments; parameter-count mismatch still raises."""
    with pytest.raises(
        expected_exception=ParameterCountMismatchError,
        match=r"^Expected 1 parameters but got 2 values$",
    ):
        literalize_call(
            source='[[{"$ref": "a"}, {"$ref": "b"}]]',
            input_format=InputFormat.JSON,
            language=Python(),
            target_function="f",
            parameter_names=["only"],
        )


def test_literalize_call_ref_case_unsupported_raises() -> None:
    """``ref_case`` outside the language's ``IdentifierCases`` raises."""
    with pytest.raises(
        expected_exception=UnsupportedIdentifierCaseError,
        match=r"^Python does not support identifier case 'CAMEL'$",
    ):
        literalize_call(
            source='[[{"$ref": "user_obj"}, 42]]',
            input_format=InputFormat.JSON,
            language=Python(),
            target_function="process",
            parameter_names=["data", "count"],
            ref_case=IdentifierCase.CAMEL,
        )


def test_jsonnet_wrap_calls_with_declarations_prepends_bindings() -> None:
    """Non-empty declarations are placed before the wrapped call
    expression.

    Jsonnet ``local`` bindings are invalid inside an array literal, so
    ``wrap_calls_with_declarations`` emits them before the
    ``wrap_in_file`` output rather than splicing them inside the array.
    """
    spec = Jsonnet()
    result = spec.wrap_calls_with_declarations(
        declarations=("local x = 1;",),
        calls="[x]",
        body_preamble=(),
    )
    assert result == "local x = 1;\n[x]"
