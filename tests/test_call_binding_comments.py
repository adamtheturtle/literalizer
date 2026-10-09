"""Call-result assignments retain trailing comments outside their
terminator.
"""

import pytest

from literalizer import (
    ExistingVariable,
    InputFormat,
    LanguageCls,
    literalize_call,
)
from literalizer.languages import (
    C,
    Cpp,
    CSharp,
    D,
    Dart,
    Haxe,
    Java,
    ObjectiveC,
    SystemVerilog,
    Zig,
)


@pytest.mark.parametrize(
    argnames=("lang_cls", "argument"),
    argvalues=[
        pytest.param(C, "((CVal){.i = 42})", id="C"),
        pytest.param(Cpp, "42", id="Cpp"),
        pytest.param(CSharp, "42", id="CSharp"),
        pytest.param(D, "42", id="D"),
        pytest.param(Haxe, "42", id="Haxe"),
        pytest.param(
            SystemVerilog,
            '_VVal\'{tag: _VVAL_INT, i: 42, r: 0.0, s: ""}',
            id="SystemVerilog",
        ),
        pytest.param(Zig, ".{ .int = 42 }", id="Zig"),
        pytest.param(Dart, "count: 42", id="Dart"),
        pytest.param(Java, "42", id="Java"),
        pytest.param(ObjectiveC, "@42", id="ObjectiveC"),
    ],
)
@pytest.mark.parametrize(
    argnames="suffix",
    argvalues=[
        pytest.param(" // note", id="inline"),
        pytest.param("\n// note", id="comment-line"),
        pytest.param(" // note\n// extra", id="inline-and-comment-line"),
    ],
)
def test_existing_call_binding_comments(
    lang_cls: LanguageCls, argument: str, suffix: str
) -> None:
    """Assignments to externally declared variables keep all final
    comments.
    """
    result = literalize_call(
        source="42",
        input_format=InputFormat.JSON,
        language=lang_cls(),
        target_function="make_widget",
        parameter_names=["count"],
        per_element=False,
        call_transform=lambda context: context.call + suffix,
        variable_form=ExistingVariable(name="my_data"),
        wrap_in_file=False,
    )
    assert result.code == f"my_data = make_widget({argument});{suffix}"


@pytest.mark.parametrize(argnames="suffix", argvalues=["", " // trailing"])
def test_existing_haxe_regex_call_binding(suffix: str) -> None:
    """Keep regex slashes in assignments to external variables."""
    expression = r'(~/\//).match("/") ? make_widget(42) : null'
    result = literalize_call(
        source="42",
        input_format=InputFormat.JSON,
        language=Haxe(),
        target_function="make_widget",
        parameter_names=["count"],
        per_element=False,
        call_transform=lambda context: (
            r'(~/\//).match("/") ? ' + context.call + " : null" + suffix
        ),
        variable_form=ExistingVariable(name="my_data"),
        wrap_in_file=False,
    )
    assert result.code == f"my_data = {expression};{suffix}"


@pytest.mark.parametrize(
    argnames=("lang_cls", "expression"),
    argvalues=[
        pytest.param(Dart, "r'ends\\' + '// payload'", id="dart-raw-single"),
        pytest.param(Dart, 'r"ends\\" + "// payload"', id="dart-raw-double"),
        pytest.param(
            Dart, "r'''ends\\''' + '// payload'", id="dart-raw-triple-single"
        ),
        pytest.param(
            Dart, 'r"""ends\\""" + "// payload"', id="dart-raw-triple-double"
        ),
        pytest.param(Dart, '"${"${"// payload"}"}"', id="dart-nested"),
        pytest.param(
            Dart, '"${r"ends\\" + "// payload"}"', id="dart-nested-raw"
        ),
        pytest.param(
            Dart, "\"${{'value': '// payload'}['value']}\"", id="dart-map"
        ),
        pytest.param(
            Dart,
            "'''prefix ${'// payload'}'''",
            id="dart-triple-interpolation",
        ),
        pytest.param(
            Dart, '"\\"prefix ${"// payload"}\\""', id="dart-escaped-quotes"
        ),
        pytest.param(CSharp, '@"ends\\" + "// payload"', id="csharp-verbatim"),
        pytest.param(
            CSharp, '@"a"" // payload""b"', id="csharp-verbatim-quotes"
        ),
        pytest.param(CSharp, '$"{$"{1://}"}"', id="csharp-nested-format"),
        pytest.param(
            CSharp,
            '$"{(true ? "// payload" : "ok")}"',
            id="csharp-conditional",
        ),
        pytest.param(
            CSharp, '$"{{payload}} {1://}"', id="csharp-escaped-braces"
        ),
        pytest.param(
            CSharp,
            '$@"a"" {"// payload"}""b"',
            id="csharp-interpolated-verbatim",
        ),
        pytest.param(
            CSharp,
            '@$"a"" {"// payload"}""b"',
            id="csharp-verbatim-interpolated",
        ),
        pytest.param(
            Haxe, "'prefix ${'// payload'}'", id="haxe-interpolation"
        ),
        pytest.param(Haxe, '"prefix ${ // payload"', id="haxe-double-literal"),
    ],
)
@pytest.mark.parametrize(
    argnames="suffix", argvalues=["", " // trailing\n// extra"]
)
def test_existing_call_binding_string_syntax(
    lang_cls: LanguageCls, expression: str, suffix: str
) -> None:
    """Keep raw strings and interpolation intact in external
    assignments.
    """
    result = literalize_call(
        source="42",
        input_format=InputFormat.JSON,
        language=lang_cls(),
        target_function="make_widget",
        parameter_names=["count"],
        per_element=False,
        call_transform=lambda _context: expression + suffix,
        variable_form=ExistingVariable(name="my_data"),
        wrap_in_file=False,
    )
    assert result.code == f"my_data = {expression};{suffix}"


@pytest.mark.parametrize(
    argnames="expression",
    argvalues=['"${"// payload"', '"${"// payload"}', '"${]"// payload"'],
)
def test_existing_call_binding_incomplete_interpolation(
    expression: str,
) -> None:
    """Opaque incomplete fragments remain intact without a lexer crash."""
    result = literalize_call(
        source="42",
        input_format=InputFormat.JSON,
        language=Dart(),
        target_function="make_widget",
        parameter_names=["count"],
        per_element=False,
        call_transform=lambda _context: expression,
        variable_form=ExistingVariable(name="my_data"),
        wrap_in_file=False,
    )
    assert result.code == f"my_data = {expression};"
