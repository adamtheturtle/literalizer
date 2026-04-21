"""Language-specific tests for literalizer converter."""

import dataclasses
import json
import re
import textwrap
from functools import cached_property

import pytest
from pygments.lexers import find_lexer_class_by_name

import literalizer.languages
from literalizer import (
    BothVariableForms,
    InputFormat,
    NewVariable,
    literalize,
    literalize_call,
)
from literalizer._language import (
    NO_HETEROGENEOUS_BEHAVIOR,
    HeterogeneousBehavior,
    LanguageCls,
)
from literalizer._types import Value
from literalizer.exceptions import (
    CallsNotSupportedByLanguageError,
    CallsNotSupportedByToolError,
    NullInCollectionError,
    PerElementNotListError,
)
from literalizer.languages import (
    Cobol,
    Fortran,
    FSharp,
    Go,
    Java,
    Matlab,
    Python,
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
)
FSHARP = FSharp()
JAVA = Java(
    date_format=Java.date_formats.JAVA,
    datetime_format=Java.datetime_formats.INSTANT,
    bytes_format=Java.bytes_formats.HEX,
    sequence_format=Java.sequence_formats.ARRAY,
)


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


def test_java_yaml_dict_null_values_with_comments() -> None:
    """Java YAML dict with null values and comments does not crash."""
    yaml_string = "# comment\nname: Alice\nscore: null\n"
    result = literalize(
        source=yaml_string,
        input_format=InputFormat.YAML,
        language=JAVA,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=None,
    )
    expected = textwrap.dedent(
        text="""\
        Map.ofEntries(
            // comment
            Map.entry("name", "Alice")
        )"""
    )
    assert result.code == expected


def test_java_yaml_dict_null_value_inline_comment_preserved() -> None:
    """Inline comment on a null-valued dict entry is preserved as a before
    comment on the next non-null entry when skip_null_dict_values=True.
    """
    yaml_string = textwrap.dedent(
        text="""\
        host: localhost
        port: null  # not configured yet
        debug: true
        """,
    )
    result = literalize(
        source=yaml_string,
        input_format=InputFormat.YAML,
        language=JAVA,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=None,
    )
    expected = textwrap.dedent(
        text="""\
        Map.ofEntries(
            Map.entry("host", "localhost"),
            // not configured yet
            Map.entry("debug", true)
        )"""
    )
    assert result.code == expected


def test_java_yaml_null_value_inline_comment_as_trailing() -> None:
    """Inline comment on a null-valued dict entry at the end becomes a
    trailing comment when skip_null_dict_values=True.
    """
    yaml_string = textwrap.dedent(
        text="""\
        host: localhost
        port: null  # not configured yet
        """,
    )
    result = literalize(
        source=yaml_string,
        input_format=InputFormat.YAML,
        language=JAVA,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=None,
    )
    expected = textwrap.dedent(
        text="""\
        Map.ofEntries(
            Map.entry("host", "localhost")
            // not configured yet
        )"""
    )
    assert result.code == expected


def test_java_yaml_all_null_dict_with_trailing_comments() -> None:
    """All-null Java YAML dict with trailing comments does not duplicate
    delimiters.
    """
    yaml_string = "a: null\nb: null\n# trailing\n"
    result = literalize(
        source=yaml_string,
        input_format=InputFormat.YAML,
        language=JAVA,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=None,
    )
    expected = "Map.ofEntries()\n    // trailing"
    assert result.code == expected


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
    assert callable(spec.format_variable_declaration)
    assert callable(spec.format_variable_assignment)
    assert callable(spec.type_hint_collection_preamble_lines)
    assert isinstance(spec.scalar_body_preamble, dict)


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


def test_literalize_call_wrap_in_file() -> None:
    """Literalize_call with wrap_in_file returns a complete file."""
    # Go has a static preamble ("package main") — covers the preamble
    # prepend branch.
    result = literalize_call(
        source="[[1, 2]]",
        input_format=InputFormat.JSON,
        language=Go(),
        target_function="process",
        parameter_names=["a", "b"],
        wrap_in_file=True,
    )
    assert "package main" in result.code
    assert "func main()" in result.code
    assert "process(" in result.code
    assert not result.preamble
    assert not result.body_preamble
    # Python has no static preamble — covers the no-preamble branch.
    result_no_preamble = literalize_call(
        source="[[1, 2]]",
        input_format=InputFormat.JSON,
        language=Python(),
        target_function="process",
        parameter_names=["a", "b"],
        wrap_in_file=True,
    )
    assert "process(" in result_no_preamble.code
    assert not result_no_preamble.preamble


def test_literalize_call_per_element_false() -> None:
    """Literalize_call with per_element=False passes the whole value."""
    result = literalize_call(
        source="[1, 2, 3]",
        input_format=InputFormat.JSON,
        language=Python(),
        target_function="process",
        parameter_names=["data"],
        per_element=False,
    )
    assert "process(" in result.code
    assert "1," in result.code


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
    with pytest.raises(expected_exception=NotImplementedError):
        language_cls.wrap_combined_in_file(
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
