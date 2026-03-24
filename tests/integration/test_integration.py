"""Integration tests that compare literalize_yaml output against golden
files.

Each subdirectory contains an ``input.yaml`` and one expected-output file
per supported language, using the real file extension for that language.

Golden files contain syntactically valid programs so that pre-commit hooks
can syntax-check them directly without additional wrapping.

To regenerate all golden files after changing output::

    uv run pytest tests/integration/ --regen-all
"""

import dataclasses
import enum
import itertools
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest
from beartype import beartype
from pytest_regressions.file_regression import FileRegressionFixture

import literalizer
import literalizer.languages
from literalizer.exceptions import NullInCollectionError
from literalizer.languages import ALL_LANGUAGES


@pytest.fixture(name="cases_dir")
def fixture_cases_dir(request: pytest.FixtureRequest) -> Path:
    """Return the absolute path to the integration test cases
    directory.
    """
    return request.config.rootpath / "tests" / "integration" / "cases"


@beartype
def _wrap_identity(content: str) -> str:
    """Return content unchanged."""
    return content


@beartype
def _wrap_js(content: str) -> str:
    """Wrap in ``void(...)`` so bare object/array literals parse as
    expressions in JavaScript and TypeScript.
    """
    return f"void (\n{content}\n)"


@beartype
def _wrap_go(content: str) -> str:
    """Wrap in a Go package-level variable declaration."""
    return f"\nvar _ = {content}"


@beartype
def _wrap_java(content: str) -> str:
    """Wrap in a Java class with necessary imports."""
    return f"""\
class Check {{
    Object x = {content};
}}"""


@beartype
def _wrap_kotlin(content: str) -> str:
    """Wrap in a Kotlin variable assignment."""
    return f"val x: Any? = {content}"


@beartype
def _wrap_kotlin_varname(content: str) -> str:
    """Wrap a Kotlin variable declaration with time imports if needed."""
    return content


@beartype
def _wrap_cpp(content: str) -> str:
    """Wrap a C++ expression in a function body."""
    return f"void _check() {{\n    [[maybe_unused]] _Any _v = {content};\n}}"


@beartype
def _wrap_swift(content: str) -> str:
    """Wrap in a Swift variable assignment."""
    return f"let x: Any? = {content}"


@beartype
def _wrap_csharp(content: str) -> str:
    """Wrap in C# variable assignment."""
    return f"var x = {content};"


@beartype
def _wrap_rust(content: str) -> str:
    """Wrap in a Rust main function with necessary imports."""
    indented = content.replace("\n", "\n    ")
    return f"fn main() {{\n    let _ = {indented};\n}}"


_FSHARP_VAL_TYPE = (
    "type Val =\n"
    "    | FNull\n"
    "    | FBool of bool\n"
    "    | FInt of int64\n"
    "    | FFloat of float\n"
    "    | FStr of string\n"
    "    | FList of Val list\n"
    "    | FMap of (string * Val) list\n"
    "    | FSet of Val list\n"
    "    | FDate of System.DateTime\n"
    "    | FDatetime of System.DateTime\n"
)

_OCAML_VAL_TYPE = (
    "type val_t =\n"
    "  | ONull\n"
    "  | OBool of bool\n"
    "  | OInt of int\n"
    "  | OFloat of float\n"
    "  | OStr of string\n"
    "  | OList of val_t list\n"
    "  | OMap of (string * val_t) list\n"
    "  | OSet of val_t list\n"
    "  | ODate of (int * int * int)\n"
    "  | ODatetime of ((int * int * int) * (int * int * int))\n"
)

_OCCAM_LIT_TYPE = (
    "MOBILE DATA TYPE LIT IS\n"
    "  CASE\n"
    "    lit.null\n"
    "    lit.bool ; BOOL\n"
    "    lit.int ; INT\n"
    "    lit.float ; REAL32\n"
    "    lit.str ; MOBILE []BYTE\n"
    "    lit.list ; MOBILE []MOBILE LIT\n"
    "    lit.map ; MOBILE []MOBILE LIT\n"
    "    lit.pair ; MOBILE []BYTE ; MOBILE LIT\n"
    "    lit.set ; MOBILE []MOBILE LIT\n"
    ":"
)

_HASKELL_VAL_TYPE = (
    "data Val = HNull | HBool Bool | HInt Integer | HFloat Double"
    " | HStr String | HList [Val] | HMap [(String, Val)] | HSet [Val]"
    " | HDate Day | HDatetime UTCTime\n"
)

_HASKELL_MODULE_HEADER = (
    "module Check where\n"
    "import Data.Time (Day, UTCTime(..), fromGregorian,"
    " secondsToDiffTime, picosecondsToDiffTime)\n"
)


@beartype
def _wrap_fsharp(content: str) -> str:
    """Wrap in an F# module with a Val assignment."""
    fsharp = literalizer.languages.FSharp()
    if content.lstrip().startswith("[|"):
        val_type = "Val array"
        typed = content
    else:
        val_type = "Val"
        typed = fsharp.format_sequence_entry(content)
    return (
        "module Check\n\n"
        + _FSHARP_VAL_TYPE
        + "\n"
        + f"let x: {val_type} = {typed}"
    )


@beartype
def _wrap_ocaml(content: str) -> str:
    """Wrap in an OCaml module with a val_t assignment."""
    ocaml = literalizer.languages.OCaml()
    if content.lstrip().startswith("[|"):
        val_type = "val_t array"
        typed = content
    else:
        val_type = "val_t"
        typed = ocaml.format_sequence_entry(content)
    return (
        "module Check = struct\n\n"
        + _OCAML_VAL_TYPE
        + "\n"
        + f"let x : {val_type} = {typed}\n\n"
        + "end"
    )


@beartype
def _wrap_ocaml_varname(content: str) -> str:
    """Wrap an OCaml ``let`` declaration in a module."""
    return (
        "module Check = struct\n\n"
        + _OCAML_VAL_TYPE
        + "\n"
        + content
        + "\n\nend"
    )


@beartype
def _wrap_occam(content: str) -> str:
    """Wrap in an occam-pi PROC."""
    occam = literalizer.languages.Occam()
    typed = occam.format_sequence_entry(content)
    return (
        _OCCAM_LIT_TYPE
        + "\n\n"
        + "PROC check ()\n"
        + f"  VAL MOBILE LIT x IS {typed}:\n"
        + "  SEQ\n"
        + "    SKIP\n"
        + ":"
    )


@beartype
def _wrap_occam_varname(content: str) -> str:
    """Wrap an occam-pi ``VAL`` declaration in a PROC."""
    indented = "  " + content.replace("\n", "\n  ")
    return (
        _OCCAM_LIT_TYPE
        + "\n\n"
        + "PROC check ()\n"
        + indented
        + "\n"
        + "  SEQ\n"
        + "    SKIP\n"
        + ":"
    )


@beartype
def _wrap_fsharp_varname(content: str) -> str:
    """Wrap an F# ``let`` declaration in a module."""
    return "module Check\n\n" + _FSHARP_VAL_TYPE + "\n" + content


@dataclasses.dataclass(frozen=True)
class _HaskellBodySplit:
    """Result of splitting body-preamble lines from a Haskell code
    string.
    """

    body_preamble: str
    expression: str


@beartype
def _split_haskell_body_preamble(*, content: str) -> _HaskellBodySplit:
    """Split body-preamble lines from the expression in *content*.

    Body-preamble lines (imports, typeclass instances) are now included
    at the start of ``code`` by the library.  This helper separates them
    from the trailing expression so the test wrapper can place them in
    the correct structural position within the Haskell module.
    """
    lines = content.split(sep="\n")

    # Body-preamble lines start with "import " or "instance ", plus
    # indented continuation lines of instance blocks.
    def _is_body_line(pair: tuple[int, str]) -> bool:
        """Return whether *pair* is a body-preamble line."""
        idx, line = pair
        return line.startswith(("import ", "instance ")) or (
            line.startswith("    ") and idx > 0
        )

    body_lines: list[tuple[int, str]] = list(
        itertools.takewhile(
            _is_body_line,
            enumerate(iterable=lines),
        ),
    )
    expr_start = len(body_lines)
    return _HaskellBodySplit(
        body_preamble="\n".join(lines[:expr_start]),
        expression="\n".join(lines[expr_start:]),
    )


@beartype
def _wrap_haskell(content: str) -> str:
    """Wrap in a Haskell module with a Val binding."""
    split = _split_haskell_body_preamble(content=content)
    header = _HASKELL_MODULE_HEADER
    if split.body_preamble:
        header += split.body_preamble + "\n"
    header += _HASKELL_VAL_TYPE
    if split.expression.lstrip().startswith("("):
        return header + f"x = {split.expression}"
    return header + "x :: Val\n" + f"x = {split.expression}"


@beartype
def _wrap_hcl(content: str) -> str:
    """Wrap in an HCL attribute assignment for syntax validation."""
    return f"_ = {content}"


_VARIABLE_NAME = "my_data"


@beartype
def _wrap_go_varname(content: str) -> str:
    """Wrap a Go short variable declaration in a main function."""
    return f"\nfunc main() {{\n{content}\n_ = {_VARIABLE_NAME}\n}}"


@beartype
def _wrap_java_varname(content: str) -> str:
    """Wrap a Java var declaration in a static method."""
    return (
        "class Check {\n"
        "    public static void check() {\n"
        f"{content}\n"
        "    }\n"
        "}"
    )


@beartype
def _wrap_csharp_varname(content: str) -> str:
    """Wrap a C# top-level variable declaration."""
    return content


@beartype
def _wrap_ts_varname(content: str) -> str:
    """Wrap a TypeScript variable declaration as a module.

    Adding ``export {}`` turns the file into a module so that ``const``
    declarations are module-scoped rather than global, preventing
    duplicate-declaration errors when ``tsc`` checks all ``.ts`` files
    together.
    """
    return f"{content}\nexport {{}};"


@beartype
def _wrap_cpp_varname(content: str) -> str:
    """Wrap a C++ variable declaration in a function body."""
    return f"void _check() {{\n{content}\n}}"


@beartype
def _wrap_scala(content: str) -> str:
    """Wrap in a Scala object with a typed variable assignment."""
    return f"object Check {{\nval x: Any = {content}\n}}"


@beartype
def _wrap_scala_varname(content: str) -> str:
    """Wrap a Scala variable declaration in an object."""
    return f"object Check {{\n{content}\n}}"


@beartype
def _wrap_scala_combined(declaration: str, assignment: str) -> str:
    """Scala: val declaration in one object, var + assignment in
    another.
    """
    decl_indented = "  " + declaration.replace("\n", "\n  ")
    assign_indented = "  " + assignment.replace("\n", "\n  ")
    return (
        f"object Declaration {{\n"
        f"{decl_indented}\n"
        f"}}\n"
        f"object Assignment {{\n"
        f"  var {_VARIABLE_NAME}: Any = null\n"
        f"{assign_indented}\n"
        f"}}"
    )


@beartype
def _wrap_dart(content: str) -> str:
    """Wrap in a Dart final variable assignment."""
    return f"final x = {content};"


@beartype
def _wrap_dart_combined(declaration: str, assignment: str) -> str:
    """Dart: final declaration in one function, dynamic + assignment in
    another, with a main that calls both to avoid unused-element warnings.
    """
    decl_indented = "  " + declaration.replace("\n", "\n  ")
    assign_indented = "  " + assignment.replace("\n", "\n  ")
    return (
        f"void _declaration() {{\n"
        f"{decl_indented}\n"
        f"  {_VARIABLE_NAME}.hashCode;\n"
        f"}}\n"
        f"void _assignment() {{\n"
        f"  dynamic {_VARIABLE_NAME};\n"
        f"{assign_indented}\n"
        f"  {_VARIABLE_NAME}.hashCode;\n"
        f"}}\n"
        f"void main() {{\n"
        f"  _declaration();\n"
        f"  _assignment();\n"
        f"}}"
    )


@beartype
def _wrap_perl(content: str) -> str:
    """Wrap in a Perl variable assignment."""
    return f"my $x = {content};"


@beartype
def _wrap_php(content: str) -> str:
    """Wrap in a PHP variable assignment."""
    return f"$x = {content};"


@beartype
def _wrap_elixir(content: str) -> str:
    """Wrap in an Elixir module function."""
    return f"defmodule Check do\n  def x do\n    {content}\n  end\nend"


@beartype
def _wrap_elixir_varname(content: str) -> str:
    """Wrap an Elixir variable assignment in a module function."""
    return (
        f"defmodule Check do\n"
        f"  def x do\n"
        f"    {content}\n"
        f"    _ = {_VARIABLE_NAME}\n"
        f"  end\n"
        f"end"
    )


@beartype
def _wrap_erlang(content: str) -> str:
    """Wrap in an Erlang module function."""
    return f"-module(check).\n-export([x/0]).\nx() ->\n    {content}."


@beartype
def _wrap_erlang_varname(content: str) -> str:
    """Wrap an Erlang variable binding in a module function.

    The variable is referenced at the end of the function body so that
    Erlang does not warn about an unused variable.
    """
    erlang_varname = _VARIABLE_NAME[0].upper() + _VARIABLE_NAME[1:]
    return (
        f"-module(check).\n"
        f"-export([x/0]).\n"
        f"x() ->\n"
        f"    {content},\n"
        f"    {erlang_varname}."
    )


@beartype
def _wrap_groovy(content: str) -> str:
    """Wrap in a Groovy variable assignment."""
    return f"def x = {content}"


@beartype
def _wrap_ada(content: str) -> str:
    """Wrap in an Ada procedure with a local variable assignment."""
    ada = literalizer.languages.Ada()
    typed = ada.format_sequence_entry(content)
    indented = typed.replace("\n", "\n   ")
    return (
        "procedure Check is\n"
        f"   X : A_Val := {indented};\n"
        "begin\n"
        "   null;\n"
        "end Check;"
    )


@beartype
def _wrap_ada_varname(content: str) -> str:
    """Wrap an Ada object declaration inside a procedure."""
    indented = "   " + content.replace("\n", "\n   ")
    return f"procedure Check is\n{indented}\nbegin\n   null;\nend Check;"


@beartype
def _wrap_ada_combined(declaration: str, assignment: str) -> str:
    """Ada: declaration in one nested procedure, assignment in another."""
    decl_indented = "      " + declaration.replace("\n", "\n      ")
    assign_indented = "      " + assignment.replace("\n", "\n      ")
    return (
        "procedure Check is\n"
        "   procedure Check_Declaration is\n"
        f"{decl_indented}\n"
        "   begin\n"
        "      null;\n"
        "   end Check_Declaration;\n"
        "   procedure Check_Assignment is\n"
        "   begin\n"
        f"{assign_indented}\n"
        "   end Check_Assignment;\n"
        "begin\n"
        "   Check_Declaration;\n"
        "   Check_Assignment;\n"
        "end Check;"
    )


@beartype
def _wrap_lua(content: str) -> str:
    """Wrap a Lua table constructor in a local variable assignment."""
    return f"local _ = {content}"


@beartype
def _wrap_r(content: str) -> str:
    """Wrap in an R variable assignment."""
    return f"x <- {content}"


@beartype
def _wrap_nim(content: str) -> str:
    """Wrap in a Nim ``%*`` JSON-node expression."""
    return f"let _ = %* {content}"


@beartype
def _wrap_nim_varname(content: str) -> str:
    """Pass through Nim content unchanged."""
    return content


@beartype
def _wrap_nim_combined(declaration: str, assignment: str) -> str:
    """Join Nim declaration and assignment with a newline."""
    return f"{declaration}\n{assignment}"


@beartype
def _wrap_norg(content: str) -> str:
    """Wrap in a Norg ranged verbatim tag."""
    return f"@code json\n{content}\n@end"


@beartype
def _wrap_d(content: str) -> str:
    """Wrap in a D function."""
    d_lang = literalizer.languages.D()
    typed = d_lang.format_sequence_entry(content)
    return f"void _check() {{\n    auto _v = {typed};\n}}"


@beartype
def _wrap_d_varname(content: str) -> str:
    """Wrap a D ``auto`` declaration in a function."""
    return f"void _check() {{\n{content}\n}}"


@beartype
def _wrap_d_combined(declaration: str, assignment: str) -> str:
    """Wrap D declaration and assignment together in one function."""
    return f"void _check() {{\n{declaration}\n{assignment}\n}}"


@beartype
def _wrap_powershell(content: str) -> str:
    """Wrap in a PowerShell variable assignment."""
    return f"$x = {content}"


@beartype
def _wrap_c(content: str) -> str:
    """Wrap in a C function."""
    c_lang = literalizer.languages.C()
    typed = c_lang.format_sequence_entry(content)
    return f"void _check(void) {{\n    _CVal _v = {typed};\n    (void)_v;\n}}"


@beartype
def _wrap_c_varname(content: str) -> str:
    """Wrap a C _CVal declaration in a function."""
    return f"void _check(void) {{\n{content}\n    (void){_VARIABLE_NAME};\n}}"


@beartype
def _wrap_c_combined(declaration: str, assignment: str) -> str:
    """Wrap C declaration and assignment together in one function."""
    return (
        "void _check(void) {\n"
        f"{declaration}\n"
        f"{assignment}\n"
        f"    (void){_VARIABLE_NAME};\n"
        "}"
    )


@beartype
def _wrap_matlab(content: str) -> str:
    """Wrap in a MATLAB/Octave variable assignment."""
    return f"x = {content};"


@beartype
def _wrap_objc(content: str) -> str:
    """Wrap in an Objective-C function."""
    return f"void _check(void) {{\n    id _v = {content};\n    (void)_v;\n}}"


@beartype
def _wrap_objc_varname(content: str) -> str:
    """Wrap an Objective-C variable declaration in a function."""
    return f"void _check(void) {{\n{content}\n    (void){_VARIABLE_NAME};\n}}"


@beartype
def _wrap_objc_combined(declaration: str, assignment: str) -> str:
    """Wrap Objective-C declaration and assignment in a function."""
    return (
        "void _check(void) {\n"
        f"{declaration}\n"
        f"{assignment}\n"
        f"    (void){_VARIABLE_NAME};\n"
        "}"
    )


@beartype
def _in_mojo_main(content: str) -> str:
    """Indent content and wrap in a Mojo ``def main():`` function.

    Mojo does not support top-level code.  No statements, expressions,
    or variable declarations are allowed at module scope, so generated
    output must be placed inside a function body.

    Inside a function, ``var`` is optional: both ``var x = [...]`` and
    ``x = [...]`` are valid.  Declarations (``new_variable=True``)
    include ``var`` for explicit variable binding; assignments
    (``new_variable=False``) omit it.  The distinction is stylistic
    since Mojo does not require ``var`` inside functions.
    """
    indented = "\n".join(f"    {line}" for line in content.splitlines())
    return f"def main():\n{indented}"


@beartype
def _wrap_mojo(content: str) -> str:
    """Wrap in a Mojo main function with assignment for syntax
    validation.
    """
    return _in_mojo_main(content=f"_ = {content}")


@beartype
def _wrap_mojo_varname(content: str) -> str:
    """Wrap a Mojo variable declaration in a main function."""
    # Consume the variable so ``--Werror`` does not flag the
    # "assignment was never used" warning.
    return _in_mojo_main(
        content=content + f"\n_ = {_VARIABLE_NAME}",
    )


@beartype
def _wrap_mojo_combined(declaration: str, assignment: str) -> str:
    """Wrap Mojo declaration and assignment in a main function."""
    # Consume the variable after each assignment so ``--Werror`` does
    # not flag the "assignment was never used" warning.
    use = f"_ = {_VARIABLE_NAME}"
    return _in_mojo_main(
        content=declaration + f"\n{use}\n" + assignment + f"\n{use}",
    )


@beartype
def _wrap_rust_varname(content: str) -> str:
    """Wrap a Rust let binding in a main function."""
    indented = content.replace("\n", "\n    ")
    return f"fn main() {{\n    {indented}\n    let _ = {_VARIABLE_NAME};\n}}"


@beartype
def _wrap_haskell_varname(content: str) -> str:
    """Wrap a Haskell variable binding in a module."""
    split = _split_haskell_body_preamble(content=content)
    header = _HASKELL_MODULE_HEADER
    if split.body_preamble:
        header += split.body_preamble + "\n"
    header += _HASKELL_VAL_TYPE
    return header + f"{_VARIABLE_NAME} :: Val\n" + split.expression


@beartype
def _wrap_php_varname(content: str) -> str:
    """Wrap a PHP variable assignment."""
    return content


@beartype
def _wrap_zig(content: str) -> str:
    """Wrap in a Zig main function."""
    zig = literalizer.languages.Zig()
    typed = zig.format_sequence_entry(content)
    indented = typed.replace("\n", "\n    ")
    return (
        "pub fn main() void {\n"
        f"    const v: ZVal = {indented};\n"
        "    _ = v;\n"
        "}"
    )


@beartype
def _wrap_zig_varname(content: str) -> str:
    """Wrap a Zig ``const`` declaration in a main function."""
    indented = "    " + content.replace("\n", "\n    ")
    return f"pub fn main() void {{\n{indented}\n    _ = {_VARIABLE_NAME};\n}}"


@beartype
def _wrap_zig_combined(declaration: str, assignment: str) -> str:
    """Zig: ``const`` declaration in an inner block, then ``var`` +
    assignment in the outer scope.
    """
    decl_indented = "        " + declaration.replace("\n", "\n        ")
    assign_indented = "    " + assignment.replace("\n", "\n    ")
    return (
        "pub fn main() void {\n"
        "    {\n"
        f"{decl_indented}\n"
        f"        _ = {_VARIABLE_NAME};\n"
        "    }\n"
        f"    var {_VARIABLE_NAME}: ZVal = undefined;\n"
        f"{assign_indented}\n"
        f"    const _{_VARIABLE_NAME}_read = {_VARIABLE_NAME};\n"
        f"    _ = _{_VARIABLE_NAME}_read;\n"
        "}"
    )


_wrap_swift_varname = _wrap_identity


@beartype
def _wrap_js_combined(declaration: str, assignment: str) -> str:
    """Wrap a JavaScript declaration in an IIFE to scope the variable,
    then assign to an outer var.
    """
    return (
        f"void (function() {{\n{declaration}\n}})();\n"
        f"var {_VARIABLE_NAME};\n"
        f"{assignment}"
    )


@beartype
def _wrap_ts_combined(declaration: str, assignment: str) -> str:
    """TypeScript combined: same as JavaScript but as a module with export."""
    return (
        f"void (function() {{\n{declaration}\n}})();\n"
        f"var {_VARIABLE_NAME};\n"
        f"{assignment}\n"
        f"export {{}};"
    )


@beartype
def _wrap_kotlin_combined(declaration: str, assignment: str) -> str:
    """Kotlin: val declaration in one fun, var + assignment in another."""
    decl_indented = "    " + declaration.replace("\n", "\n    ")
    assign_indented = "    " + assignment.replace("\n", "\n    ")
    return (
        f"fun _declaration() {{\n"
        f"{decl_indented}\n"
        f"}}\n"
        f"fun _assignment() {{\n"
        f"    var {_VARIABLE_NAME}: Any? = null\n"
        f"{assign_indented}\n"
        f"}}"
    )


@beartype
def _wrap_swift_combined(declaration: str, assignment: str) -> str:
    """Swift: let declaration in a do block,
    then var + assignment in the outer scope.
    """
    decl_indented = "    " + declaration.replace("\n", "\n    ")
    return (
        f"do {{\n{decl_indented}\n}}\nvar {_VARIABLE_NAME}: Any\n{assignment}"
    )


@beartype
def _wrap_rust_combined(declaration: str, assignment: str) -> str:
    """Rust: let declaration in an inner block, then a deferred-init
    let + assignment in the outer scope.
    """
    decl_indented = "        " + declaration.replace("\n", "\n        ")
    assign_indented = "    " + assignment.replace("\n", "\n    ")
    return (
        "fn main() {\n"
        "    {\n"
        f"{decl_indented}\n"
        f"        let _ = {_VARIABLE_NAME};\n"
        "    }\n"
        f"    let {_VARIABLE_NAME};\n"
        f"{assign_indented}\n"
        f"    let _ = {_VARIABLE_NAME};\n"
        "}"
    )


@beartype
def _fortran_comment_pos(line: str) -> int | None:
    """Return the index of the ``!`` comment in *line* outside strings."""
    in_single_quote = False
    in_double_quote = False
    i = 0
    while i < len(line):
        c = line[i]
        if c == "'" and not in_double_quote:
            next_also_quote = i + 1 < len(line) and line[i + 1] == "'"
            if in_single_quote and next_also_quote:
                i += 2
                continue
            in_single_quote = not in_single_quote
        elif c == '"' and not in_single_quote:
            in_double_quote = not in_double_quote
        elif c == "!" and not in_single_quote and not in_double_quote:
            return i
        i += 1
    return None


@beartype
def _add_fortran_continuation(content: str) -> str:
    """Add Fortran ``&`` line-continuation to non-comment, non-last
    lines.

    Pure comment lines (blank or starting with ``!``) are transparent to
    the Fortran continuation mechanism and receive no ``&``.  For lines
    with inline comments the ``&`` is inserted before the ``!``.
    """
    lines = content.splitlines()
    if len(lines) <= 1:
        return content
    result: list[str] = []
    for i, line in enumerate(iterable=lines):
        is_last = i == len(lines) - 1
        stripped = line.strip()
        is_pure_comment = not stripped or stripped.startswith("!")
        if is_last or is_pure_comment:
            result.append(line)
        else:
            pos = _fortran_comment_pos(line=line)
            if pos is not None:
                result.append(line[:pos].rstrip() + " &  " + line[pos:])
            else:
                result.append(line + " &")
    return "\n".join(result)


@beartype
def _wrap_fortran(content: str) -> str:
    """Wrap in a self-contained Fortran program with the ``fval_m``
    module embedded.
    """
    fortran = literalizer.languages.Fortran()
    typed = fortran.format_sequence_entry(content)
    continued = _add_fortran_continuation(content=typed)
    return (
        "program check\n"
        "  use fval_m\n"
        "  implicit none\n"
        "  type(fval_t) :: x\n"
        f"  x = {continued}\n"
        "end program check"
    )


@beartype
def _wrap_fortran_varname(content: str) -> str:
    """Wrap a Fortran variable declaration in a program."""
    indented = "  " + content.replace("\n", "\n  ")
    return (
        "program check\n"
        "  use fval_m\n"
        "  implicit none\n"
        f"{indented}\n"
        "end program check"
    )


@beartype
def _wrap_fortran_combined(declaration: str, assignment: str) -> str:
    """Fortran: declaration in one subroutine, assignment in another."""
    decl_indented = "  " + declaration.replace("\n", "\n  ")
    assign_indented = "  " + assignment.replace("\n", "\n  ")
    return (
        "subroutine check_declaration()\n"
        "  use fval_m\n"
        "  implicit none\n"
        f"{decl_indented}\n"
        "end subroutine check_declaration\n"
        "\n"
        "subroutine check_assignment()\n"
        "  use fval_m\n"
        "  implicit none\n"
        f"  type(fval_t) :: {_VARIABLE_NAME}\n"
        f"{assign_indented}\n"
        "end subroutine check_assignment\n"
        "\n"
        "program main\n"
        "  call check_declaration()\n"
        "  call check_assignment()\n"
        "end program main"
    )


@beartype
def _wrap_combined_newline(declaration: str, assignment: str) -> str:
    """Join declaration and assignment with a newline."""
    return declaration + "\n" + assignment


@beartype
def _wrap_python(content: str) -> str:
    """Pass through Python content unchanged."""
    return content


@beartype
def _wrap_ruby(content: str) -> str:
    """Pass through Ruby content unchanged."""
    return content


@beartype
def _wrap_crystal(content: str) -> str:
    """Wrap in a Crystal variable assignment to suppress unused-expression
    warnings.
    """
    return f"_ = {content}"


@beartype
def _wrap_crystal_varname(content: str) -> str:
    """Pass through Crystal content unchanged."""
    return content


@beartype
def _wrap_crystal_combined(declaration: str, assignment: str) -> str:
    """Join Crystal declaration and assignment with a newline."""
    return declaration + "\n" + assignment


@beartype
def _wrap_julia(content: str) -> str:
    """Pass through Julia content unchanged."""
    return content


@beartype
def _wrap_vb(content: str) -> str:
    """Wrap in a VB.NET Module with a Dim declaration.

    Comment hoisting is delegated to the language module's
    ``format_variable_declaration``.
    """
    lang = literalizer.languages.VisualBasic()
    declaration = lang.format_variable_declaration(
        "x As Object",
        content,
        None,
    )
    return _wrap_vb_varname(content=declaration)


@beartype
def _wrap_vb_varname(content: str) -> str:
    """Wrap a VB.NET Dim declaration inside a Module."""
    indented = "    " + content.replace("\n", "\n    ")
    return f"Module Check\n{indented}\nEnd Module"


@beartype
def _wrap_vb_combined(declaration: str, assignment: str) -> str:
    """VB.NET: Dim declaration in one Sub, assignment in another."""
    decl_indented = "        " + declaration.replace("\n", "\n        ")
    assign_indented = "        " + assignment.replace("\n", "\n        ")
    return (
        "Module Check\n"
        "    Sub _declaration()\n"
        f"{decl_indented}\n"
        "    End Sub\n"
        "    Sub _assignment()\n"
        f"        Dim {_VARIABLE_NAME} As Object\n"
        f"{assign_indented}\n"
        "    End Sub\n"
        "End Module"
    )


@beartype
def _prepend_preamble(
    wrapped: str,
    preamble: tuple[str, ...],
) -> str:
    """Prepend *preamble* lines before *wrapped*."""
    if not preamble:
        return wrapped
    return "\n".join(preamble) + "\n" + wrapped


@dataclasses.dataclass
class _Variant:
    """A formatting variant for a language (date, sequence, set, etc.)."""

    spec: literalizer.Language
    wrap: Callable[[str], str]


@dataclasses.dataclass
class _LanguageConfig:
    """Language configuration with class, file extension, and wrapper."""

    lang_cls: literalizer.LanguageCls
    wrap: Callable[[str], str]
    varname_wrap: Callable[[str], str]
    combined_wrap: Callable[[str, str], str]


@beartype
def _wrap_bash(content: str) -> str:
    """Wrap in a Bash ``declare`` statement for syntax validation."""
    flag = (
        " -A"
        if any(line.lstrip().startswith("[") for line in content.splitlines())
        else ""
    )
    return f"declare{flag} _v={content}"


@beartype
def _wrap_toml(content: str) -> str:
    """Wrap in a TOML key assignment for syntax validation.

    TOML v1.1 permits newlines and comments within inline tables, so the
    multiline output from ``_literalize`` can be used directly as a TOML
    value.
    """
    return f"x = {content}"


_COBOL_PROGRAM_PREFIX = (
    "IDENTIFICATION DIVISION.\n"
    "PROGRAM-ID. CHECK.\n"
    "DATA DIVISION.\n"
    "WORKING-STORAGE SECTION.\n"
)

_COBOL_PROGRAM_SUFFIX = "PROCEDURE DIVISION.\n    STOP RUN."


@beartype
def _wrap_cobol(content: str) -> str:
    """Wrap in a free-format GnuCOBOL program for syntax checking."""
    cobol_level_field_sep = 2
    cobol_level_min_len = 3
    stripped = content.strip("\n")
    scalar = stripped.strip()
    is_data_entry = (
        scalar
        and scalar[0].isdigit()
        and len(scalar) > cobol_level_min_len
        and scalar[cobol_level_field_sep] == " "
    )
    if "\n" in stripped or is_data_entry:
        # Already DATA DIVISION entries
        data_body = stripped
    else:
        # Scalar literal - convert to a DATA entry
        cobol = literalizer.languages.Cobol()
        entry = cobol.format_sequence_entry(scalar)
        data_body = f"    {entry}"
    return (
        _COBOL_PROGRAM_PREFIX
        + f"01 LITERAL-VALUE.\n{data_body}\n"
        + _COBOL_PROGRAM_SUFFIX
    )


@beartype
def _wrap_cobol_varname(content: str) -> str:
    """Wrap a COBOL variable declaration in a complete program."""
    return _COBOL_PROGRAM_PREFIX + f"{content}\n" + _COBOL_PROGRAM_SUFFIX


@beartype
def _wrap_cobol_combined(declaration: str, assignment: str) -> str:
    """Wrap COBOL declaration (DATA DIVISION) and assignment (PROCEDURE
    DIVISION).
    """
    return (
        _COBOL_PROGRAM_PREFIX
        + f"{declaration}\n"
        + "PROCEDURE DIVISION.\n"
        + f"    {assignment}\n"
        + "    STOP RUN."
    )


_LANGUAGES: dict[str, _LanguageConfig] = {
    literalizer.languages.Ada.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Ada,
        wrap=_wrap_ada,
        varname_wrap=_wrap_ada_varname,
        combined_wrap=_wrap_ada_combined,
    ),
    literalizer.languages.Bash.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Bash,
        wrap=_wrap_bash,
        varname_wrap=_wrap_identity,
        combined_wrap=_wrap_combined_newline,
    ),
    literalizer.languages.C.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.C,
        wrap=_wrap_c,
        varname_wrap=_wrap_c_varname,
        combined_wrap=_wrap_c_combined,
    ),
    literalizer.languages.Cobol.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Cobol,
        wrap=_wrap_cobol,
        varname_wrap=_wrap_cobol_varname,
        combined_wrap=_wrap_cobol_combined,
    ),
    literalizer.languages.D.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.D,
        wrap=_wrap_d,
        varname_wrap=_wrap_d_varname,
        combined_wrap=_wrap_d_combined,
    ),
    literalizer.languages.CommonLisp.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.CommonLisp,
        wrap=_wrap_identity,
        varname_wrap=_wrap_identity,
        combined_wrap=_wrap_combined_newline,
    ),
    literalizer.languages.Clojure.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Clojure,
        wrap=_wrap_identity,
        varname_wrap=_wrap_identity,
        combined_wrap=_wrap_combined_newline,
    ),
    literalizer.languages.Python.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Python,
        wrap=_wrap_python,
        varname_wrap=_wrap_python,
        combined_wrap=_wrap_combined_newline,
    ),
    literalizer.languages.JavaScript.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.JavaScript,
        wrap=_wrap_js,
        varname_wrap=_wrap_identity,
        combined_wrap=_wrap_js_combined,
    ),
    literalizer.languages.TypeScript.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.TypeScript,
        wrap=_wrap_js,
        varname_wrap=_wrap_ts_varname,
        combined_wrap=_wrap_ts_combined,
    ),
    literalizer.languages.Kotlin.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Kotlin,
        wrap=_wrap_kotlin,
        varname_wrap=_wrap_kotlin_varname,
        combined_wrap=_wrap_kotlin_combined,
    ),
    literalizer.languages.Ruby.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Ruby,
        wrap=_wrap_ruby,
        varname_wrap=_wrap_ruby,
        combined_wrap=lambda d, a: _wrap_ruby(content=d + "\n" + a),
    ),
    literalizer.languages.Go.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Go,
        wrap=_wrap_go,
        varname_wrap=_wrap_go_varname,
        combined_wrap=lambda d, a: _wrap_go_varname(content=d + "\n" + a),
    ),
    literalizer.languages.Java.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Java,
        wrap=_wrap_java,
        varname_wrap=_wrap_java_varname,
        combined_wrap=lambda d, a: _wrap_java_varname(content=d + "\n" + a),
    ),
    literalizer.languages.CSharp.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.CSharp,
        wrap=_wrap_csharp,
        varname_wrap=_wrap_csharp_varname,
        combined_wrap=lambda d, a: _wrap_csharp_varname(content=d + "\n" + a),
    ),
    literalizer.languages.Dart.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Dart,
        wrap=_wrap_dart,
        varname_wrap=_wrap_identity,
        combined_wrap=_wrap_dart_combined,
    ),
    literalizer.languages.Swift.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Swift,
        wrap=_wrap_swift,
        varname_wrap=_wrap_swift_varname,
        combined_wrap=_wrap_swift_combined,
    ),
    literalizer.languages.Cpp.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Cpp,
        wrap=_wrap_cpp,
        varname_wrap=_wrap_cpp_varname,
        combined_wrap=lambda d, a: _wrap_cpp_varname(content=d + "\n" + a),
    ),
    literalizer.languages.Rust.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Rust,
        wrap=_wrap_rust,
        varname_wrap=_wrap_rust_varname,
        combined_wrap=_wrap_rust_combined,
    ),
    literalizer.languages.Haskell.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Haskell,
        wrap=_wrap_haskell,
        varname_wrap=_wrap_haskell_varname,
        combined_wrap=lambda d, _a: _wrap_haskell_varname(content=d),
    ),
    literalizer.languages.Hcl.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Hcl,
        wrap=_wrap_hcl,
        varname_wrap=_wrap_identity,
        combined_wrap=lambda d, _a: d,
    ),
    literalizer.languages.Julia.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Julia,
        wrap=_wrap_julia,
        varname_wrap=_wrap_julia,
        combined_wrap=lambda d, a: _wrap_julia(content=d + "\n" + a),
    ),
    literalizer.languages.Lua.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Lua,
        wrap=_wrap_lua,
        varname_wrap=_wrap_identity,
        combined_wrap=_wrap_combined_newline,
    ),
    literalizer.languages.Perl.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Perl,
        wrap=_wrap_perl,
        varname_wrap=_wrap_identity,
        combined_wrap=_wrap_combined_newline,
    ),
    literalizer.languages.Php.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Php,
        wrap=_wrap_php,
        varname_wrap=_wrap_php_varname,
        combined_wrap=lambda d, a: _wrap_php_varname(content=d + "\n" + a),
    ),
    literalizer.languages.Elixir.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Elixir,
        wrap=_wrap_elixir,
        varname_wrap=_wrap_elixir_varname,
        combined_wrap=lambda d, _a: _wrap_elixir_varname(content=d),
    ),
    literalizer.languages.Erlang.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Erlang,
        wrap=_wrap_erlang,
        varname_wrap=_wrap_erlang_varname,
        combined_wrap=lambda d, _a: _wrap_erlang_varname(content=d),
    ),
    literalizer.languages.FSharp.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.FSharp,
        wrap=_wrap_fsharp,
        varname_wrap=_wrap_fsharp_varname,
        combined_wrap=lambda d, _a: _wrap_fsharp_varname(content=d),
    ),
    literalizer.languages.OCaml.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.OCaml,
        wrap=_wrap_ocaml,
        varname_wrap=_wrap_ocaml_varname,
        combined_wrap=lambda d, _a: _wrap_ocaml_varname(content=d),
    ),
    literalizer.languages.Occam.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Occam,
        wrap=_wrap_occam,
        varname_wrap=_wrap_occam_varname,
        combined_wrap=lambda d, _a: _wrap_occam_varname(content=d),
    ),
    literalizer.languages.Groovy.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Groovy,
        wrap=_wrap_groovy,
        varname_wrap=_wrap_identity,
        combined_wrap=_wrap_combined_newline,
    ),
    literalizer.languages.Scala.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Scala,
        wrap=_wrap_scala,
        varname_wrap=_wrap_scala_varname,
        combined_wrap=_wrap_scala_combined,
    ),
    literalizer.languages.R.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.R,
        wrap=_wrap_r,
        varname_wrap=_wrap_identity,
        combined_wrap=_wrap_combined_newline,
    ),
    literalizer.languages.Racket.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Racket,
        wrap=_wrap_identity,
        varname_wrap=_wrap_identity,
        combined_wrap=_wrap_combined_newline,
    ),
    literalizer.languages.Crystal.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Crystal,
        wrap=_wrap_crystal,
        varname_wrap=_wrap_crystal_varname,
        combined_wrap=_wrap_crystal_combined,
    ),
    literalizer.languages.Matlab.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Matlab,
        wrap=_wrap_matlab,
        varname_wrap=_wrap_identity,
        combined_wrap=_wrap_combined_newline,
    ),
    literalizer.languages.Mojo.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Mojo,
        wrap=_wrap_mojo,
        varname_wrap=_wrap_mojo_varname,
        combined_wrap=_wrap_mojo_combined,
    ),
    literalizer.languages.Nim.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Nim,
        wrap=_wrap_nim,
        varname_wrap=_wrap_nim_varname,
        combined_wrap=_wrap_nim_combined,
    ),
    literalizer.languages.Norg.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Norg,
        wrap=_wrap_norg,
        varname_wrap=_wrap_identity,
        combined_wrap=lambda d, _a: d,
    ),
    literalizer.languages.VisualBasic.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.VisualBasic,
        wrap=_wrap_vb,
        varname_wrap=_wrap_vb_varname,
        combined_wrap=_wrap_vb_combined,
    ),
    literalizer.languages.Zig.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Zig,
        wrap=_wrap_zig,
        varname_wrap=_wrap_zig_varname,
        combined_wrap=_wrap_zig_combined,
    ),
    literalizer.languages.PowerShell.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.PowerShell,
        wrap=_wrap_powershell,
        varname_wrap=_wrap_identity,
        combined_wrap=_wrap_combined_newline,
    ),
    literalizer.languages.Toml.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Toml,
        wrap=_wrap_toml,
        varname_wrap=_wrap_identity,
        combined_wrap=lambda d, _a: d,
    ),
    literalizer.languages.ObjectiveC.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.ObjectiveC,
        wrap=_wrap_objc,
        varname_wrap=_wrap_objc_varname,
        combined_wrap=_wrap_objc_combined,
    ),
    literalizer.languages.Fortran.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Fortran,
        wrap=_wrap_fortran,
        varname_wrap=_wrap_fortran_varname,
        combined_wrap=_wrap_fortran_combined,
    ),
    literalizer.languages.Yaml.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Yaml,
        wrap=_wrap_identity,
        varname_wrap=_wrap_identity,
        combined_wrap=lambda d, _a: d,
    ),
}

_COVERED_LANGUAGES = frozenset(cfg.lang_cls for cfg in _LANGUAGES.values())
assert _COVERED_LANGUAGES == ALL_LANGUAGES, (
    f"Missing from integration tests: {ALL_LANGUAGES - _COVERED_LANGUAGES}"
)


@dataclasses.dataclass
class _VariantCase:
    """A format-variant golden-file test case."""

    variant_name: str
    variant: _Variant
    case_dir_name: str
    variable_name: str | None


@beartype
def _build_date_variants() -> dict[str, _Variant]:
    """Build date-format variants for scalar dates.

    For each language, create a variant for every non-default date format,
    using ``wrap``.
    """
    variants: dict[str, _Variant] = {}
    for lang_name, lang_config in _LANGUAGES.items():
        spec = lang_config.lang_cls()
        default_format = spec.format_date
        for fmt in list(spec.date_formats):
            if fmt is default_format:
                continue
            # Date and datetime formats can share enum member names
            # within the same language (e.g. Python has both
            # DateFormats.ISO and DatetimeFormats.ISO), so we include
            # a "_date_" infix to keep keys unique.
            variant_key = f"{lang_name}_date_{fmt.name.lower()}"
            variants[variant_key] = _Variant(
                spec=lang_config.lang_cls(date_format=fmt),
                wrap=lang_config.wrap,
            )
    return variants


@beartype
def _build_datetime_variants() -> dict[str, _Variant]:
    """Build datetime-format variants for scalar datetimes.

    For each language, create a variant for every non-default datetime format,
    using ``wrap``.
    """
    variants: dict[str, _Variant] = {}
    for lang_name, lang_config in _LANGUAGES.items():
        spec = lang_config.lang_cls()
        default_format = spec.format_datetime
        for fmt in list(spec.datetime_formats):
            if fmt is default_format:
                continue
            # See _build_date_variants for why "_datetime_" is needed.
            variant_key = f"{lang_name}_datetime_{fmt.name.lower()}"
            variants[variant_key] = _Variant(
                spec=lang_config.lang_cls(datetime_format=fmt),
                wrap=lang_config.wrap,
            )
    return variants


@beartype
def _build_sequence_variants() -> dict[str, _Variant]:
    """Build sequence-format variants for all languages with multiple
    formats.

    For each language that has more than one sequence format, create a variant
    for every non-default format.
    """
    variants: dict[str, _Variant] = {}
    for lang_name, lang_config in _LANGUAGES.items():
        spec = lang_config.lang_cls()
        default_format: Any = spec.sequence_format
        for fmt in list(spec.sequence_formats):
            if fmt is default_format:
                continue
            variant_key = f"{lang_name}_sequence_{fmt.name.lower()}"
            variants[variant_key] = _Variant(
                spec=lang_config.lang_cls(sequence_format=fmt),
                wrap=lang_config.wrap,
            )
    return variants


@beartype
def _build_set_variants() -> dict[str, _Variant]:
    """Build set-format variants for all languages with multiple formats.

    For each language that has more than one set format, create a variant
    for every non-default set format.
    """
    variants: dict[str, _Variant] = {}
    for lang_name, lang_config in _LANGUAGES.items():
        spec = lang_config.lang_cls()
        default_format = spec.set_format
        for fmt in list(spec.set_formats):
            if fmt is default_format:
                continue
            variant_key = f"{lang_name}_set_{fmt.name.lower()}"
            variants[variant_key] = _Variant(
                spec=lang_config.lang_cls(set_format=fmt),
                wrap=lang_config.wrap,
            )
    return variants


@beartype
def _build_comment_variants() -> dict[str, _Variant]:
    """Build comment-format variants for all languages with multiple
    formats.

    For each language that has more than one comment format, create a variant
    for every non-default format.
    """
    variants: dict[str, _Variant] = {}
    for lang_name, lang_config in _LANGUAGES.items():
        spec = lang_config.lang_cls()
        default_format = spec.comment_format
        for fmt in list(spec.comment_formats):
            if fmt is default_format:
                continue
            variant_key = f"{lang_name}_comment_{fmt.name.lower()}"
            variants[variant_key] = _Variant(
                spec=lang_config.lang_cls(comment_format=fmt),
                wrap=lang_config.wrap,
            )
    return variants


@beartype
def _build_type_hint_variants() -> dict[str, _Variant]:
    """Build variable-type-hint variants for all languages with multiple
    formats.

    For each language that has more than one variable type-hint format,
    create a variant for every non-default type-hint style.
    """
    variants: dict[str, _Variant] = {}
    for lang_name, lang_config in _LANGUAGES.items():
        spec = lang_config.lang_cls()
        default_format = spec.variable_type_hints
        for fmt in list(spec.variable_type_hints_formats):
            if fmt is default_format:
                continue
            variant_key = f"{lang_name}_type_hints_{fmt.name.lower()}"
            variants[variant_key] = _Variant(
                spec=lang_config.lang_cls(variable_type_hints=fmt),
                wrap=lang_config.wrap,
            )
    return variants


@beartype
def _build_declaration_style_variants() -> dict[str, _Variant]:
    """Build declaration-style variants for all languages with multiple
    styles.
    """
    variants: dict[str, _Variant] = {}
    for lang_name, lang_config in _LANGUAGES.items():
        spec = lang_config.lang_cls()
        default_format = spec.declaration_style
        non_defaults = [
            fmt for fmt in spec.declaration_styles if fmt is not default_format
        ]
        for fmt in non_defaults:
            key = f"{lang_name}_declaration_style_"
            variant_key = key + fmt.name.lower()
            variants[variant_key] = _Variant(
                spec=lang_config.lang_cls(
                    declaration_style=fmt,
                ),
                wrap=lang_config.varname_wrap,
            )
    return variants


@beartype
def _build_dict_format_variants() -> dict[str, _Variant]:
    """Build dict/map-format variants for all languages with multiple
    formats.
    """
    variants: dict[str, _Variant] = {}
    for lang_name, lang_config in _LANGUAGES.items():
        spec = lang_config.lang_cls()
        default_format = spec.dict_format
        non_defaults = [
            fmt for fmt in spec.dict_formats if fmt is not default_format
        ]
        for fmt in non_defaults:
            key = f"{lang_name}_dict_format_"
            variant_key = key + fmt.name.lower()
            variants[variant_key] = _Variant(
                spec=lang_config.lang_cls(
                    dict_format=fmt,
                ),
                wrap=lang_config.wrap,
            )
    return variants


@beartype
def _build_integer_format_variants() -> dict[str, _Variant]:
    """Build integer-format variants for all languages with multiple
    formats.
    """
    variants: dict[str, _Variant] = {}
    for lang_name, lang_config in _LANGUAGES.items():
        spec = lang_config.lang_cls()
        default_format = spec.integer_format
        non_defaults = [
            fmt for fmt in spec.integer_formats if fmt is not default_format
        ]
        for fmt in non_defaults:
            key = f"{lang_name}_integer_format_"
            variant_key = key + fmt.name.lower()
            variants[variant_key] = _Variant(
                spec=lang_config.lang_cls(
                    integer_format=fmt,
                ),
                wrap=lang_config.wrap,
            )
    return variants


@beartype
def _build_numeric_separator_variants() -> dict[str, _Variant]:
    """Build numeric-separator variants for all languages with multiple
    options.
    """
    variants: dict[str, _Variant] = {}
    for lang_name, lang_config in _LANGUAGES.items():
        spec = lang_config.lang_cls()
        default_format = spec.numeric_separator
        non_defaults = [
            fmt for fmt in spec.numeric_separators if fmt is not default_format
        ]
        for fmt in non_defaults:
            key = f"{lang_name}_numeric_separator_"
            variant_key = key + fmt.name.lower()
            variants[variant_key] = _Variant(
                spec=lang_config.lang_cls(
                    numeric_separator=fmt,
                ),
                wrap=lang_config.wrap,
            )
    return variants


@beartype
def _build_string_format_variants() -> dict[str, _Variant]:
    """Build string-format variants for all languages with multiple
    formats.
    """
    variants: dict[str, _Variant] = {}
    for lang_name, lang_config in _LANGUAGES.items():
        spec = lang_config.lang_cls()
        default_format = spec.string_format
        non_defaults = [
            fmt for fmt in spec.string_formats if fmt is not default_format
        ]
        for fmt in non_defaults:
            key = f"{lang_name}_string_format_"
            variant_key = key + fmt.name.lower()
            variants[variant_key] = _Variant(
                spec=lang_config.lang_cls(
                    string_format=fmt,
                ),
                wrap=lang_config.wrap,
            )
    return variants


@beartype
def _build_bytes_format_variants() -> dict[str, _Variant]:
    """Build bytes-format variants for all languages with multiple
    formats.
    """
    variants: dict[str, _Variant] = {}
    for lang_name, lang_config in _LANGUAGES.items():
        spec = lang_config.lang_cls()
        default_format = spec.format_bytes
        non_defaults = [
            fmt for fmt in spec.bytes_formats if fmt is not default_format
        ]
        for fmt in non_defaults:
            key = f"{lang_name}_bytes_format_"
            variant_key = key + fmt.name.lower()
            variants[variant_key] = _Variant(
                spec=lang_config.lang_cls(
                    bytes_format=fmt,
                ),
                wrap=lang_config.wrap,
            )
    return variants


@beartype
def _build_trailing_comma_variants() -> dict[str, _Variant]:
    """Build trailing-comma variants for all languages with multiple
    options.
    """
    variants: dict[str, _Variant] = {}
    for lang_name, lang_config in _LANGUAGES.items():
        spec = lang_config.lang_cls()
        default_format = spec.trailing_comma
        non_defaults = [
            fmt for fmt in spec.trailing_commas if fmt is not default_format
        ]
        for fmt in non_defaults:
            key = f"{lang_name}_trailing_comma_"
            variant_key = key + fmt.name.lower()
            variants[variant_key] = _Variant(
                spec=lang_config.lang_cls(
                    trailing_comma=fmt,
                ),
                wrap=lang_config.wrap,
            )
    return variants


@beartype
def _build_line_ending_variants() -> dict[str, _Variant]:
    """Build line-ending variants for all languages with multiple
    options.
    """
    variants: dict[str, _Variant] = {}
    for lang_name, lang_config in _LANGUAGES.items():
        spec = lang_config.lang_cls()
        default_format = spec.line_ending
        non_defaults = [
            fmt for fmt in spec.line_endings if fmt is not default_format
        ]
        for fmt in non_defaults:
            key = f"{lang_name}_line_ending_"
            variant_key = key + fmt.name.lower()
            variants[variant_key] = _Variant(
                spec=lang_config.lang_cls(
                    line_ending=fmt,
                ),
                wrap=lang_config.varname_wrap,
            )
    return variants


@beartype
def _build_line_ending_decl_variants() -> dict[str, _Variant]:
    """Build line-ending + declaration-style cross-option variants.

    For each language with multiple line endings *and* multiple
    declaration styles, create a variant for every non-default
    line ending paired with every non-default declaration style.
    """
    variants: dict[str, _Variant] = {}
    for lang_name, lang_config in _LANGUAGES.items():
        spec = lang_config.lang_cls()
        default_le = spec.line_ending
        default_ds = spec.declaration_style
        non_default_le = [
            le for le in spec.line_endings if le is not default_le
        ]
        non_default_ds = [
            ds for ds in spec.declaration_styles if ds is not default_ds
        ]
        for le in non_default_le:
            for ds in non_default_ds:
                key = (
                    f"{lang_name}_line_ending_{le.name.lower()}"
                    f"_decl_{ds.name.lower()}"
                )
                variants[key] = _Variant(
                    spec=lang_config.lang_cls(
                        line_ending=le,
                        declaration_style=ds,
                    ),
                    wrap=lang_config.varname_wrap,
                )
    return variants


@beartype
def _discover_cases() -> list[tuple[str, str]]:
    """Return ``(case_name, language)`` tuples."""
    cases_dir = Path(__file__).parent / "cases"
    cases: list[tuple[str, str]] = []
    for case_dir in sorted(cases_dir.iterdir()):
        cases.extend((case_dir.name, lang_name) for lang_name in _LANGUAGES)
    return cases


_CASES = _discover_cases()


@pytest.mark.parametrize(
    argnames=("_case_name", "language"),
    argvalues=_CASES,
    ids=[f"{c[0]}/{c[1]}" for c in _CASES],
)
def test_golden_file(
    _case_name: str,
    language: str,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
) -> None:
    """Test that literalize_yaml output matches expected golden file."""
    input_path = cases_dir / _case_name / "input.yaml"
    lang_config = _LANGUAGES[language]
    yaml_string = input_path.read_text()
    result = literalizer.literalize_yaml(
        yaml_string=yaml_string,
        language=lang_config.lang_cls(),
        line_prefix="",
        indent="    ",
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    wrapped = lang_config.wrap(result.code)

    wrapped = _prepend_preamble(wrapped=wrapped, preamble=result.preamble)
    file_regression.check(
        contents=wrapped + "\n",
        extension=lang_config.lang_cls.extension,
        fullpath=input_path.parent
        / (language + lang_config.lang_cls.extension),
    )


@pytest.mark.parametrize(
    argnames=("_case_name", "language"),
    argvalues=_CASES,
    ids=[f"{c[0]}/{c[1]}" for c in _CASES],
)
def test_golden_file_with_variable_name(
    _case_name: str,
    language: str,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
) -> None:
    """Test that literalize_yaml with variable_name matches golden
    file.
    """
    input_path = cases_dir / _case_name / "input.yaml"
    lang_config = _LANGUAGES[language]
    yaml_string = input_path.read_text()
    result = literalizer.literalize_yaml(
        yaml_string=yaml_string,
        language=lang_config.lang_cls(),
        line_prefix="",
        indent="    ",
        include_delimiters=True,
        variable_name=_VARIABLE_NAME,
        new_variable=True,
        error_on_coercion=False,
    )
    wrapped = lang_config.varname_wrap(result.code)

    wrapped = _prepend_preamble(wrapped=wrapped, preamble=result.preamble)
    file_regression.check(
        contents=wrapped + "\n",
        extension=lang_config.lang_cls.extension,
        fullpath=input_path.parent
        / (language + "_varname" + lang_config.lang_cls.extension),
    )


@pytest.mark.parametrize(
    argnames=("_case_name", "language"),
    argvalues=_CASES,
    ids=[f"{c[0]}/{c[1]}" for c in _CASES],
)
def test_golden_file_combined_variable_forms(
    _case_name: str,
    language: str,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
) -> None:
    """Test that literalize_yaml with new_variable=True (declaration) and
    new_variable=False (assignment to existing variable) produce expected
    golden output, combined in one file to show the difference in syntax.
    """
    input_path = cases_dir / _case_name / "input.yaml"
    lang_config = _LANGUAGES[language]
    yaml_string = input_path.read_text()
    declaration = literalizer.literalize_yaml(
        yaml_string=yaml_string,
        language=lang_config.lang_cls(),
        line_prefix="",
        indent="    ",
        include_delimiters=True,
        variable_name=_VARIABLE_NAME,
        new_variable=True,
        error_on_coercion=False,
    )
    assignment = literalizer.literalize_yaml(
        yaml_string=yaml_string,
        language=lang_config.lang_cls(),
        line_prefix="",
        indent="    ",
        include_delimiters=True,
        variable_name=_VARIABLE_NAME,
        new_variable=False,
        error_on_coercion=False,
    )
    combined = lang_config.combined_wrap(declaration.code, assignment.code)
    combined = _prepend_preamble(
        wrapped=combined, preamble=declaration.preamble
    )
    file_regression.check(
        contents=combined + "\n",
        extension=lang_config.lang_cls.extension,
        fullpath=input_path.parent
        / (language + "_combined" + lang_config.lang_cls.extension),
    )


@beartype
def _build_variant_cases() -> list[_VariantCase]:
    """Collect all format-variant golden-file test cases."""
    cases: list[_VariantCase] = []
    variant_sources: list[tuple[dict[str, _Variant], str, str | None, str]] = [
        (_build_date_variants(), "scalar_date", None, ""),
        (_build_date_variants(), "date_list", None, ""),
        (_build_date_variants(), "date_set", None, ""),
        (_build_datetime_variants(), "scalar_datetime", None, ""),
        (_build_datetime_variants(), "scalar_datetime_naive", None, "_naive"),
        (
            _build_datetime_variants(),
            "scalar_datetime_non_utc",
            None,
            "_non_utc",
        ),
        (_build_sequence_variants(), "simple_sequence", None, ""),
        (_build_sequence_variants(), "pair_sequence", None, "_pair"),
        (_build_sequence_variants(), "triple_sequence", None, "_triple"),
        (_build_set_variants(), "set", None, ""),
        (_build_comment_variants(), "comments", None, ""),
        (_build_type_hint_variants(), "type_hints", _VARIABLE_NAME, ""),
        (
            _build_declaration_style_variants(),
            "simple_sequence",
            _VARIABLE_NAME,
            "",
        ),
        (
            _build_declaration_style_variants(),
            "simple_dict",
            _VARIABLE_NAME,
            "",
        ),
        (
            _build_declaration_style_variants(),
            "empty_list",
            _VARIABLE_NAME,
            "",
        ),
        (_build_dict_format_variants(), "simple_dict", None, ""),
        (_build_integer_format_variants(), "int_list", None, ""),
        (_build_integer_format_variants(), "int_list_large", None, "_large"),
        (_build_numeric_separator_variants(), "int_list", None, ""),
        (
            _build_numeric_separator_variants(),
            "int_list_large",
            None,
            "_large",
        ),
        (_build_string_format_variants(), "string_list", None, ""),
        (_build_bytes_format_variants(), "binary", None, ""),
        (_build_trailing_comma_variants(), "simple_sequence", None, ""),
        (
            _build_line_ending_variants(),
            "simple_sequence",
            _VARIABLE_NAME,
            "",
        ),
        (
            _build_line_ending_variants(),
            "simple_dict",
            _VARIABLE_NAME,
            "_dict",
        ),
        (
            _build_line_ending_decl_variants(),
            "simple_sequence",
            _VARIABLE_NAME,
            "",
        ),
    ]
    for variants, case_dir_name, variable_name, suffix in variant_sources:
        for variant_name, variant in variants.items():
            cases.append(
                _VariantCase(
                    variant_name=f"{variant_name}{suffix}",
                    variant=variant,
                    case_dir_name=case_dir_name,
                    variable_name=variable_name,
                )
            )
    return cases


_FORMAT_VARIANT_CASES = _build_variant_cases()


@pytest.mark.parametrize(
    argnames="variant_case",
    argvalues=_FORMAT_VARIANT_CASES,
    ids=[c.variant_name for c in _FORMAT_VARIANT_CASES],
)
def test_format_variant_golden_file(
    variant_case: _VariantCase,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
) -> None:
    """Test format-variant options (dates, sequences, sets, type hints)
    against golden files.
    """
    case_dir = cases_dir / variant_case.case_dir_name
    variant = variant_case.variant
    yaml_string = (case_dir / "input.yaml").read_text()
    try:
        result = literalizer.literalize_yaml(
            yaml_string=yaml_string,
            language=variant.spec,
            line_prefix="",
            indent="    ",
            include_delimiters=True,
            variable_name=variant_case.variable_name,
            new_variable=True,
            error_on_coercion=False,
        )
    except NullInCollectionError:
        pytest.skip("Format rejects null elements in this input")
    wrapped = variant.wrap(result.code)
    wrapped = _prepend_preamble(wrapped=wrapped, preamble=result.preamble)
    file_regression.check(
        contents=wrapped + "\n",
        extension=variant.spec.extension,
        fullpath=case_dir
        / (variant_case.variant_name + variant.spec.extension),
    )


@dataclasses.dataclass
class _LineEndingCombinedCase:
    """A combined-variable-forms test case with a non-default line
    ending.
    """

    name: str
    lang_config: _LanguageConfig
    line_ending: enum.Enum
    case_dir_name: str


@beartype
def _build_line_ending_combined_cases() -> list[_LineEndingCombinedCase]:
    """Collect combined (declaration + assignment) test cases for
    non-default line endings.
    """
    cases: list[_LineEndingCombinedCase] = []
    for lang_name, lang_config in _LANGUAGES.items():
        spec = lang_config.lang_cls()
        default_le = spec.line_ending
        for le in spec.line_endings:
            if le is default_le:
                continue
            for case_dir_name in ("simple_sequence", "simple_dict"):
                name = (
                    f"{lang_name}_line_ending"
                    f"_{le.name.lower()}_{case_dir_name}"
                )
                cases.append(
                    _LineEndingCombinedCase(
                        name=name,
                        lang_config=lang_config,
                        line_ending=le,
                        case_dir_name=case_dir_name,
                    )
                )
    return cases


_LINE_ENDING_COMBINED_CASES = _build_line_ending_combined_cases()


@pytest.mark.parametrize(
    argnames="case",
    argvalues=_LINE_ENDING_COMBINED_CASES,
    ids=[c.name for c in _LINE_ENDING_COMBINED_CASES],
)
def test_line_ending_combined_variable_forms(
    case: _LineEndingCombinedCase,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
) -> None:
    """Test that combined (declaration + assignment) output with a
    non-default line ending matches the golden file.
    """
    input_path = cases_dir / case.case_dir_name / "input.yaml"
    yaml_string = input_path.read_text()
    spec = case.lang_config.lang_cls(line_ending=case.line_ending)
    declaration = literalizer.literalize_yaml(
        yaml_string=yaml_string,
        language=spec,
        line_prefix="",
        indent="    ",
        include_delimiters=True,
        variable_name=_VARIABLE_NAME,
        new_variable=True,
        error_on_coercion=False,
    )
    assignment = literalizer.literalize_yaml(
        yaml_string=yaml_string,
        language=spec,
        line_prefix="",
        indent="    ",
        include_delimiters=True,
        variable_name=_VARIABLE_NAME,
        new_variable=False,
        error_on_coercion=False,
    )
    combined = case.lang_config.combined_wrap(
        declaration.code, assignment.code
    )
    combined = _prepend_preamble(
        wrapped=combined, preamble=declaration.preamble
    )
    file_regression.check(
        contents=combined + "\n",
        extension=spec.extension,
        fullpath=input_path.parent / (case.name + spec.extension),
    )


_SORTED_LANGUAGES: list[literalizer.LanguageCls] = sorted(
    ALL_LANGUAGES,
    key=lambda c: c.__name__,
)


@pytest.mark.parametrize(
    argnames="language_cls",
    argvalues=_SORTED_LANGUAGES,
    ids=[c.__name__ for c in _SORTED_LANGUAGES],
)
def test_format_enumeration_properties(
    language_cls: literalizer.LanguageCls,
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
    assert issubclass(spec.integer_formats, enum.Enum)
    assert len(spec.integer_formats) >= 1
    assert issubclass(spec.numeric_separators, enum.Enum)
    assert len(spec.numeric_separators) >= 1
    assert issubclass(spec.string_formats, enum.Enum)
    assert len(spec.string_formats) >= 1
    assert issubclass(spec.trailing_commas, enum.Enum)
    assert len(spec.trailing_commas) >= 1
    assert issubclass(spec.line_endings, enum.Enum)
    assert len(spec.line_endings) >= 1


def test_fortran_comment_pos_escaped_single_quote() -> None:
    """Doubled single quotes inside a Fortran string are not treated as
    the end of the string when locating ``!`` comments.
    """
    line = "fstr('it''s here')  ! note"
    expected = 20
    assert _fortran_comment_pos(line=line) == expected
