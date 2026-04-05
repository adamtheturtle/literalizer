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
from collections.abc import Callable, Iterable
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
def _wrap_identity(content: str, _variable_name: str) -> str:
    """Return content unchanged."""
    return content


def _find_redefinition_styles(
    spec: literalizer.Language,
) -> list[enum.Enum]:
    """Return all declaration styles that support redefinition."""
    return [
        style
        for style in spec.declaration_styles
        if style.value.supports_redefinition
    ]


def _newline_combined(
    wrap: Callable[[str, str], str],
) -> Callable[[str, str, str], str]:
    """Build a combined_wrap that joins declaration and assignment with a
    newline and passes through *wrap*.
    """

    def combined_wrap(declaration: str, assignment: str, value: str) -> str:
        """Join declaration and assignment with a newline, then wrap."""
        return wrap(declaration + "\n" + assignment, value)

    return combined_wrap


@beartype
def _wrap_ocaml(content: str, _variable_name: str) -> str:
    """Wrap an OCaml ``let`` declaration in a module."""
    return "module Check = struct\n\n" + content + "\n\nend"


@beartype
def _wrap_occam(content: str, _variable_name: str) -> str:
    """Wrap an occam-pi ``VAL`` declaration in a PROC."""
    indented = "  " + content.replace("\n", "\n  ")
    return (
        "\nPROC check ()\n" + indented + "\n" + "  SEQ\n" + "    SKIP\n" + ":"
    )


@beartype
def _wrap_fsharp(content: str, _variable_name: str) -> str:
    """Wrap an F# ``let`` declaration in a module."""
    return "module Check\n\n" + content


@beartype
def _wrap_fsharp_combined(
    declaration: str,
    assignment: str,
    _variable_name: str,
) -> str:
    """F#: separate private functions to avoid duplicate definitions.

    The declaration includes the body preamble (``type Val = …``)
    before the ``let`` binding.  We split on the first ``let`` line
    so the type definition appears once at module scope while each
    binding lives in its own private function.
    """
    lines = declaration.split(sep="\n")
    let_idx = next(
        idx
        for idx, line in enumerate(iterable=lines)
        if line.startswith("let")
    )
    preamble = "\n".join(lines[:let_idx])
    decl_binding = "\n".join(lines[let_idx:])
    decl_indented = "    " + decl_binding.replace("\n", "\n    ")
    assign_indented = "    " + assignment.replace("\n", "\n    ")
    body = "module Check\n\n" + preamble + "\n"
    body += (
        "let private _checkDeclaration () =\n"
        + decl_indented
        + "\n    ignore my_data\n\n"
        + "let private _checkAssignment () =\n"
        + assign_indented
        + "\n    ignore my_data"
    )
    return body


@beartype
def _wrap_gleam(content: str, variable_name: str) -> str:
    """Wrap a Gleam let binding in a main function."""
    indented = "  " + content.replace("\n", "\n  ")
    return f"\npub fn main() {{\n{indented}\n  let _ = {variable_name}\n}}"


@beartype
def _wrap_go(content: str, variable_name: str) -> str:
    """Wrap a Go short variable declaration in a main function."""
    return f"\nfunc main() {{\n{content}\n_ = {variable_name}\n}}"


@beartype
def _wrap_java(content: str, _variable_name: str) -> str:
    """Wrap a Java var declaration in a static method."""
    return (
        "class Check {\n"
        "    public static void check() {\n"
        f"{content}\n"
        "    }\n"
        "}"
    )


@beartype
def _wrap_ts(content: str, _variable_name: str) -> str:
    """Wrap a TypeScript variable declaration as a module.

    Adding ``export {}`` turns the file into a module so that ``const``
    declarations are module-scoped rather than global, preventing
    duplicate-declaration errors when ``tsc`` checks all ``.ts`` files
    together.
    """
    return f"{content}\nexport {{}};"


@beartype
def _wrap_cpp(content: str, _variable_name: str) -> str:
    """Wrap a C++ variable declaration in a function body."""
    return f"void _check() {{\n{content}\n}}"


@beartype
def _wrap_scala(content: str, _variable_name: str) -> str:
    """Wrap a Scala variable declaration in an object."""
    return f"object Check {{\n{content}\n}}"


@beartype
def _wrap_elixir(content: str, variable_name: str) -> str:
    """Wrap an Elixir variable assignment in a module function."""
    indented = "    " + content.replace("\n", "\n    ")
    return (
        f"defmodule Check do\n"
        f"  def x do\n"
        f"{indented}\n"
        f"    _ = {variable_name}\n"
        f"  end\n"
        f"end"
    )


@beartype
def _wrap_purescript(content: str, variable_name: str) -> str:
    """Wrap a PureScript value declaration in a module."""
    lines = content.split(sep="\n")
    preamble_prefixes = ("import ", "data ")
    # Find the first line that is NOT body-preamble.  A line counts as
    # preamble when it starts with a known prefix or is an indented
    # continuation of a preceding block.
    expr_start = next(
        (
            idx
            for idx, line in enumerate(iterable=lines)
            if not (
                any(line.startswith(p) for p in preamble_prefixes)
                or (line.startswith("    ") and idx > 0)
            )
        ),
        len(lines),
    )

    preamble = "\n".join(lines[:expr_start])
    expression = "\n".join(lines[expr_start:])

    parts = ["module Check where", preamble]
    parts.append(f"{variable_name} :: Val\n{expression}")
    return "\n\n\n".join(parts)


@beartype
def _wrap_elm(content: str, variable_name: str) -> str:
    """Wrap an Elm value declaration in a module."""
    lines = content.split(sep="\n")
    preamble_prefixes = ("type ",)
    # Find the first line that is NOT body-preamble.  A line counts as
    # preamble when it starts with a known prefix or is an indented
    # continuation of a preceding block.
    expr_start = next(
        (
            idx
            for idx, line in enumerate(iterable=lines)
            if not (
                any(line.startswith(p) for p in preamble_prefixes)
                or (line.startswith("    ") and idx > 0)
            )
        ),
        len(lines),
    )

    preamble = "\n".join(lines[:expr_start])
    expression = "\n".join(lines[expr_start:])

    parts = ["module Check exposing (..)", preamble]
    parts.append(f"{variable_name} : Val\n{expression}")
    return "\n\n\n".join(parts)


@beartype
def _wrap_erlang(content: str, variable_name: str) -> str:
    """Wrap an Erlang variable binding in a module function.

    The variable is referenced at the end of the function body so that
    Erlang does not warn about an unused variable.
    """
    erlang_varname = variable_name[0].upper() + variable_name[1:]
    indented = "    " + content.replace("\n", "\n    ")
    return (
        f"-module(check).\n"
        f"-export([x/0]).\n"
        f"x() ->\n"
        f"{indented},\n"
        f"    {erlang_varname}."
    )


@beartype
def _wrap_ada(content: str, _variable_name: str) -> str:
    """Wrap an Ada object declaration inside a procedure."""
    indented = "   " + content.replace("\n", "\n   ")
    return f"procedure Check is\n{indented}\nbegin\n   null;\nend Check;"


@beartype
def _wrap_ada_combined(
    declaration: str,
    assignment: str,
    _variable_name: str,
) -> str:
    """Ada: declaration in one nested procedure, assignment in another."""
    decl_indented = "   " + declaration.replace("\n", "\n   ")
    assign_indented = "   " + assignment.replace("\n", "\n   ")
    inner = (
        "procedure Check_Declaration is\n"
        f"{decl_indented}\n"
        "begin\n"
        "   null;\n"
        "end Check_Declaration;\n"
        "procedure Check_Assignment is\n"
        "begin\n"
        f"{assign_indented}\n"
        "end Check_Assignment;"
    )
    return _wrap_ada(content=inner, _variable_name=_variable_name)


@beartype
def _wrap_d(content: str, _variable_name: str) -> str:
    """Wrap a D ``auto`` declaration in a function."""
    return f"void _check() {{\n{content}\n}}"


@beartype
def _wrap_systemverilog(content: str, _variable_name: str) -> str:
    """Wrap a SystemVerilog declaration in a module with an initial
    block.
    """
    return f"module check;\ninitial begin\n{content}\nend\nendmodule"


@beartype
def _wrap_c(content: str, variable_name: str) -> str:
    """Wrap a C _CVal declaration in a function."""
    return f"void _check(void) {{\n{content}\n    (void){variable_name};\n}}"


@beartype
def _wrap_objc(content: str, variable_name: str) -> str:
    """Wrap an Objective-C variable declaration in a function."""
    return f"void _check(void) {{\n{content}\n    (void){variable_name};\n}}"


@beartype
def _wrap_mojo(content: str, variable_name: str) -> str:
    """Wrap a Mojo variable declaration in a main function.

    Mojo does not support top-level code.  No statements, expressions,
    or variable declarations are allowed at module scope, so generated
    output must be placed inside a function body.

    Inside a function, ``var`` is optional: both ``var x = [...]`` and
    ``x = [...]`` are valid.  Declarations (``new_variable=True``)
    include ``var`` for explicit variable binding; assignments
    (``new_variable=False``) omit it.  The distinction is stylistic
    since Mojo does not require ``var`` inside functions.
    """
    # Consume the variable so ``--Werror`` does not flag the
    # "assignment was never used" warning.
    content = content + f"\n_ = {variable_name}"
    indented = "\n".join(f"    {line}" for line in content.splitlines())
    return f"def main():\n{indented}"


@beartype
def _wrap_mojo_combined(
    declaration: str,
    assignment: str,
    variable_name: str,
) -> str:
    """Wrap Mojo declaration and assignment in a main function.

    Mojo ``--Werror`` treats an assignment that is immediately
    overwritten without being read as an error
    (``assignment to 'x' was never used``).  A bare ``_ = variable``
    must appear *between* the declaration and the reassignment, not
    only at the end.
    """
    use = f"_ = {variable_name}"
    return _wrap_mojo(
        content=declaration + f"\n{use}\n" + assignment,
        variable_name=variable_name,
    )


@beartype
def _wrap_rust(content: str, variable_name: str) -> str:
    """Wrap a Rust let binding in a main function."""
    indented = content.replace("\n", "\n    ")
    return f"fn main() {{\n    {indented}\n    let _ = {variable_name};\n}}"


@beartype
def _wrap_haskell(content: str, variable_name: str) -> str:
    """Wrap a Haskell variable binding in a module."""
    lines = content.split(sep="\n")
    preamble_prefixes = ("import ", "instance ", "data ")
    # Find the first line that is NOT body-preamble.  A line counts as
    # preamble when it starts with a known prefix or is an indented
    # continuation of a preceding block.
    expr_start = next(
        (
            idx
            for idx, line in enumerate(iterable=lines)
            if not (
                any(line.startswith(p) for p in preamble_prefixes)
                or (line.startswith("    ") and idx > 0)
            )
        ),
        len(lines),
    )

    preamble = "\n".join(lines[:expr_start])
    expression = "\n".join(lines[expr_start:])

    header = "module Check where\n" + preamble + "\n"
    # Tuples are not Val-typed, so skip the type annotation for them.
    eq_pos = expression.find("= ")
    rhs = expression[eq_pos + 2 :].lstrip() if eq_pos >= 0 else ""
    if rhs.startswith("("):
        return header + expression
    return header + f"{variable_name} :: Val\n" + expression


@beartype
def _wrap_zig(content: str, variable_name: str) -> str:
    """Wrap a Zig declaration in a main function.

    For ``var`` declarations the wrapper mutates the variable so the Zig
    compiler does not warn about a ``var`` that is never mutated.
    """
    indented = "    " + content.replace("\n", "\n    ")
    if "var " in content:
        use = f"    {variable_name} = .nil;"
    else:
        use = f"    _ = {variable_name};"
    return f"pub fn main() void {{\n{indented}\n{use}\n}}"


@beartype
@beartype
def _wrap_fortran(content: str, _variable_name: str) -> str:
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
def _wrap_fortran_combined(
    declaration: str,
    assignment: str,
    variable_name: str,
) -> str:
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
        f"  type(fval_t) :: {variable_name}\n"
        f"{assign_indented}\n"
        "end subroutine check_assignment\n"
        "\n"
        "program main\n"
        "  call check_declaration()\n"
        "  call check_assignment()\n"
        "end program main"
    )


@beartype
def _wrap_vb(content: str, _variable_name: str) -> str:
    """Wrap a VB.NET Dim declaration inside a Module."""
    indented = "    " + content.replace("\n", "\n    ")
    return f"Module Check\n{indented}\nEnd Module"


@beartype
def _wrap_vb_combined(
    declaration: str,
    assignment: str,
    variable_name: str,
) -> str:
    """VB.NET: Dim declaration in one Sub, assignment in another."""
    decl_indented = "        " + declaration.replace("\n", "\n        ")
    assign_indented = "        " + assignment.replace("\n", "\n        ")
    return (
        "Module Check\n"
        "    Sub _declaration()\n"
        f"{decl_indented}\n"
        "    End Sub\n"
        "    Sub _assignment()\n"
        f"        Dim {variable_name} As Object\n"
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

    name: str
    spec: literalizer.Language
    wrap: Callable[[str, str], str]
    wrap_variable_name: str | None = None


@dataclasses.dataclass
class _LanguageConfig:
    """Language configuration with class, file extension, and wrapper."""

    lang_cls: literalizer.LanguageCls
    wrap: Callable[[str, str], str]
    combined_wrap: Callable[[str, str, str], str]
    wrap_variable_name: str | None = None


_COBOL_PROGRAM_PREFIX = (
    "IDENTIFICATION DIVISION.\n"
    "PROGRAM-ID. CHECK.\n"
    "DATA DIVISION.\n"
    "WORKING-STORAGE SECTION.\n"
)

_COBOL_PROGRAM_SUFFIX = "PROCEDURE DIVISION.\n    STOP RUN."


@beartype
def _wrap_cobol(content: str, _variable_name: str) -> str:
    """Wrap a COBOL variable declaration in a complete program."""
    return _COBOL_PROGRAM_PREFIX + f"{content}\n" + _COBOL_PROGRAM_SUFFIX


@beartype
def _wrap_cobol_combined(
    declaration: str,
    assignment: str,
    _variable_name: str,
) -> str:
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
        combined_wrap=_wrap_ada_combined,
        wrap_variable_name="my_data",
    ),
    literalizer.languages.Bash.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Bash,
        wrap=_wrap_identity,
        combined_wrap=_newline_combined(wrap=_wrap_identity),
        wrap_variable_name="my_data",
    ),
    literalizer.languages.C.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.C,
        wrap=_wrap_c,
        combined_wrap=_newline_combined(wrap=_wrap_c),
        wrap_variable_name="my_data",
    ),
    literalizer.languages.Cobol.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Cobol,
        wrap=_wrap_cobol,
        combined_wrap=_wrap_cobol_combined,
        wrap_variable_name="my_data",
    ),
    literalizer.languages.D.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.D,
        wrap=_wrap_d,
        combined_wrap=_newline_combined(wrap=_wrap_d),
        wrap_variable_name="my_data",
    ),
    literalizer.languages.CommonLisp.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.CommonLisp,
        wrap=_wrap_identity,
        combined_wrap=_newline_combined(wrap=_wrap_identity),
    ),
    literalizer.languages.Clojure.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Clojure,
        wrap=_wrap_identity,
        combined_wrap=_newline_combined(wrap=_wrap_identity),
    ),
    literalizer.languages.Python.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Python,
        wrap=_wrap_identity,
        combined_wrap=_newline_combined(wrap=_wrap_identity),
        wrap_variable_name="my_data",
    ),
    literalizer.languages.JavaScript.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.JavaScript,
        wrap=_wrap_identity,
        combined_wrap=_newline_combined(wrap=_wrap_identity),
        wrap_variable_name="my_data",
    ),
    literalizer.languages.Json5.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Json5,
        wrap=_wrap_identity,
        combined_wrap=_newline_combined(wrap=_wrap_identity),
    ),
    literalizer.languages.Jsonnet.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Jsonnet,
        wrap=_wrap_identity,
        combined_wrap=_newline_combined(wrap=_wrap_identity),
    ),
    literalizer.languages.TypeScript.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.TypeScript,
        wrap=_wrap_ts,
        combined_wrap=_newline_combined(wrap=_wrap_ts),
        wrap_variable_name="my_data",
    ),
    literalizer.languages.Kotlin.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Kotlin,
        wrap=_wrap_identity,
        combined_wrap=_newline_combined(wrap=_wrap_identity),
        wrap_variable_name="my_data",
    ),
    literalizer.languages.Ruby.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Ruby,
        wrap=_wrap_identity,
        combined_wrap=_newline_combined(wrap=_wrap_identity),
    ),
    literalizer.languages.Gleam.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Gleam,
        wrap=_wrap_gleam,
        combined_wrap=_newline_combined(wrap=_wrap_gleam),
        wrap_variable_name="my_data",
    ),
    literalizer.languages.Go.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Go,
        wrap=_wrap_go,
        combined_wrap=_newline_combined(wrap=_wrap_go),
        wrap_variable_name="my_data",
    ),
    literalizer.languages.Java.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Java,
        wrap=_wrap_java,
        combined_wrap=_newline_combined(wrap=_wrap_java),
        wrap_variable_name="my_data",
    ),
    literalizer.languages.CSharp.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.CSharp,
        wrap=_wrap_identity,
        combined_wrap=_newline_combined(wrap=_wrap_identity),
        wrap_variable_name="my_data",
    ),
    literalizer.languages.Dart.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Dart,
        wrap=_wrap_identity,
        combined_wrap=_newline_combined(wrap=_wrap_identity),
        wrap_variable_name="my_data",
    ),
    literalizer.languages.Dhall.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Dhall,
        wrap=_wrap_identity,
        combined_wrap=_newline_combined(wrap=_wrap_identity),
        wrap_variable_name="my_data",
    ),
    literalizer.languages.Swift.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Swift,
        wrap=_wrap_identity,
        combined_wrap=_newline_combined(wrap=_wrap_identity),
        wrap_variable_name="my_data",
    ),
    literalizer.languages.Cpp.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Cpp,
        wrap=_wrap_cpp,
        combined_wrap=_newline_combined(wrap=_wrap_cpp),
        wrap_variable_name="my_data",
    ),
    literalizer.languages.Rust.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Rust,
        wrap=_wrap_rust,
        combined_wrap=_newline_combined(wrap=_wrap_rust),
        wrap_variable_name="my_data",
    ),
    literalizer.languages.Haskell.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Haskell,
        wrap=_wrap_haskell,
        combined_wrap=_newline_combined(wrap=_wrap_haskell),
        wrap_variable_name="my_data",
    ),
    literalizer.languages.Hcl.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Hcl,
        wrap=_wrap_identity,
        combined_wrap=_newline_combined(wrap=_wrap_identity),
        wrap_variable_name="my_data",
    ),
    literalizer.languages.Julia.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Julia,
        wrap=_wrap_identity,
        combined_wrap=_newline_combined(wrap=_wrap_identity),
    ),
    literalizer.languages.Lua.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Lua,
        wrap=_wrap_identity,
        combined_wrap=_newline_combined(wrap=_wrap_identity),
        wrap_variable_name="my_data",
    ),
    literalizer.languages.Perl.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Perl,
        wrap=_wrap_identity,
        combined_wrap=_newline_combined(wrap=_wrap_identity),
        wrap_variable_name="my_data",
    ),
    literalizer.languages.Php.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Php,
        wrap=_wrap_identity,
        combined_wrap=_newline_combined(wrap=_wrap_identity),
        wrap_variable_name="my_data",
    ),
    literalizer.languages.Elixir.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Elixir,
        wrap=_wrap_elixir,
        combined_wrap=_newline_combined(wrap=_wrap_elixir),
        wrap_variable_name="my_data",
    ),
    literalizer.languages.Elm.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Elm,
        wrap=_wrap_elm,
        combined_wrap=_newline_combined(wrap=_wrap_elm),
        wrap_variable_name="my_data",
    ),
    literalizer.languages.Erlang.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Erlang,
        wrap=_wrap_erlang,
        combined_wrap=_newline_combined(wrap=_wrap_erlang),
        wrap_variable_name="my_data",
    ),
    literalizer.languages.FSharp.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.FSharp,
        wrap=_wrap_fsharp,
        combined_wrap=_wrap_fsharp_combined,
        wrap_variable_name="my_data",
    ),
    literalizer.languages.OCaml.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.OCaml,
        wrap=_wrap_ocaml,
        combined_wrap=_newline_combined(wrap=_wrap_ocaml),
        wrap_variable_name="my_data",
    ),
    literalizer.languages.Occam.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Occam,
        wrap=_wrap_occam,
        combined_wrap=_newline_combined(wrap=_wrap_occam),
        wrap_variable_name="my_data",
    ),
    literalizer.languages.Groovy.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Groovy,
        wrap=_wrap_identity,
        combined_wrap=_newline_combined(wrap=_wrap_identity),
        wrap_variable_name="my_data",
    ),
    literalizer.languages.Scala.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Scala,
        wrap=_wrap_scala,
        combined_wrap=_newline_combined(wrap=_wrap_scala),
        wrap_variable_name="my_data",
    ),
    literalizer.languages.R.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.R,
        wrap=_wrap_identity,
        combined_wrap=_newline_combined(wrap=_wrap_identity),
        wrap_variable_name="my_data",
    ),
    literalizer.languages.Racket.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Racket,
        wrap=_wrap_identity,
        combined_wrap=_newline_combined(wrap=_wrap_identity),
    ),
    literalizer.languages.Scheme.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Scheme,
        wrap=_wrap_identity,
        combined_wrap=_newline_combined(wrap=_wrap_identity),
    ),
    literalizer.languages.Crystal.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Crystal,
        wrap=_wrap_identity,
        combined_wrap=_newline_combined(wrap=_wrap_identity),
        wrap_variable_name="my_data",
    ),
    literalizer.languages.Matlab.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Matlab,
        wrap=_wrap_identity,
        combined_wrap=_newline_combined(wrap=_wrap_identity),
        wrap_variable_name="my_data",
    ),
    literalizer.languages.Mojo.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Mojo,
        wrap=_wrap_mojo,
        combined_wrap=_wrap_mojo_combined,
        wrap_variable_name="my_data",
    ),
    literalizer.languages.Nim.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Nim,
        wrap=_wrap_identity,
        combined_wrap=_newline_combined(wrap=_wrap_identity),
        wrap_variable_name="my_data",
    ),
    literalizer.languages.Norg.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Norg,
        wrap=_wrap_identity,
        combined_wrap=_newline_combined(wrap=_wrap_identity),
        wrap_variable_name="my_data",
    ),
    literalizer.languages.VisualBasic.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.VisualBasic,
        wrap=_wrap_vb,
        combined_wrap=_wrap_vb_combined,
        wrap_variable_name="my_data",
    ),
    literalizer.languages.SystemVerilog.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.SystemVerilog,
        wrap=_wrap_systemverilog,
        combined_wrap=_newline_combined(wrap=_wrap_systemverilog),
        wrap_variable_name="my_data",
    ),
    literalizer.languages.Zig.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Zig,
        wrap=_wrap_zig,
        combined_wrap=_newline_combined(wrap=_wrap_zig),
        wrap_variable_name="my_data",
    ),
    literalizer.languages.PureScript.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.PureScript,
        wrap=_wrap_purescript,
        combined_wrap=_newline_combined(wrap=_wrap_purescript),
        wrap_variable_name="my_data",
    ),
    literalizer.languages.PowerShell.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.PowerShell,
        wrap=_wrap_identity,
        combined_wrap=_newline_combined(wrap=_wrap_identity),
        wrap_variable_name="my_data",
    ),
    literalizer.languages.Toml.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Toml,
        wrap=_wrap_identity,
        combined_wrap=_newline_combined(wrap=_wrap_identity),
        wrap_variable_name="my_data",
    ),
    literalizer.languages.ObjectiveC.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.ObjectiveC,
        wrap=_wrap_objc,
        combined_wrap=_newline_combined(wrap=_wrap_objc),
        wrap_variable_name="my_data",
    ),
    literalizer.languages.Fortran.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Fortran,
        wrap=_wrap_fortran,
        combined_wrap=_wrap_fortran_combined,
        wrap_variable_name="my_data",
    ),
    literalizer.languages.Yaml.__name__: _LanguageConfig(
        lang_cls=literalizer.languages.Yaml,
        wrap=_wrap_identity,
        combined_wrap=_newline_combined(wrap=_wrap_identity),
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
def _build_date_variants() -> Iterable[_Variant]:
    """Build date-format variants for scalar dates.

    For each language, create a variant for every non-default date format,
    using ``wrap``.
    """
    variants: list[_Variant] = []
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
            variants.append(
                _Variant(
                    name=f"{lang_name}_date_{fmt.name.lower()}",
                    spec=lang_config.lang_cls(date_format=fmt),
                    wrap=lang_config.wrap,
                    wrap_variable_name=lang_config.wrap_variable_name,
                )
            )
    return variants


@beartype
def _build_datetime_variants() -> Iterable[_Variant]:
    """Build datetime-format variants for scalar datetimes.

    For each language, create a variant for every non-default datetime format,
    using ``wrap``.
    """
    variants: list[_Variant] = []
    for lang_name, lang_config in _LANGUAGES.items():
        spec = lang_config.lang_cls()
        default_format = spec.format_datetime
        for fmt in list(spec.datetime_formats):
            if fmt is default_format:
                continue
            # See _build_date_variants for why "_datetime_" is needed.
            variants.append(
                _Variant(
                    name=f"{lang_name}_datetime_{fmt.name.lower()}",
                    spec=lang_config.lang_cls(datetime_format=fmt),
                    wrap=lang_config.wrap,
                    wrap_variable_name=lang_config.wrap_variable_name,
                )
            )
    return variants


@beartype
def _build_sequence_variants() -> Iterable[_Variant]:
    """Build sequence-format variants for all languages with multiple
    formats.

    For each language that has more than one sequence format, create a variant
    for every non-default format.
    """
    variants: list[_Variant] = []
    for lang_name, lang_config in _LANGUAGES.items():
        spec = lang_config.lang_cls()
        default_format: Any = spec.sequence_format
        for fmt in list(spec.sequence_formats):
            if fmt is default_format:
                continue
            variants.append(
                _Variant(
                    name=f"{lang_name}_sequence_{fmt.name.lower()}",
                    spec=lang_config.lang_cls(sequence_format=fmt),
                    wrap=lang_config.wrap,
                    wrap_variable_name=lang_config.wrap_variable_name,
                )
            )
    return variants


@beartype
def _build_sequence_varname_variants() -> Iterable[_Variant]:
    """Build sequence-format variants with variable declarations.

    Like :func:`_build_sequence_variants` but exercises
    ``_format_variable_declaration`` for each non-default sequence format.
    """
    variants: list[_Variant] = []
    for lang_name, lang_config in _LANGUAGES.items():
        spec = lang_config.lang_cls()
        default_format: Any = spec.sequence_format
        for fmt in list(spec.sequence_formats):
            if fmt is default_format:
                continue
            variants.append(
                _Variant(
                    name=f"{lang_name}_sequence_{fmt.name.lower()}",
                    spec=lang_config.lang_cls(sequence_format=fmt),
                    wrap=lang_config.wrap,
                    wrap_variable_name=lang_config.wrap_variable_name,
                )
            )
    return variants


@beartype
def _build_set_variants() -> Iterable[_Variant]:
    """Build set-format variants for all languages with multiple formats.

    For each language that has more than one set format, create a variant
    for every non-default set format.
    """
    variants: list[_Variant] = []
    for lang_name, lang_config in _LANGUAGES.items():
        spec = lang_config.lang_cls()
        default_format = spec.set_format
        for fmt in list(spec.set_formats):
            if fmt is default_format:
                continue
            variants.append(
                _Variant(
                    name=f"{lang_name}_set_{fmt.name.lower()}",
                    spec=lang_config.lang_cls(set_format=fmt),
                    wrap=lang_config.wrap,
                    wrap_variable_name=lang_config.wrap_variable_name,
                )
            )
    return variants


@beartype
def _build_default_set_element_type_variants() -> Iterable[_Variant]:
    """Build default-set-type variants for languages that support it.

    For each language that advertises ``supports_default_set_element_type``,
    create a variant with a non-default value.
    """
    # The test value must differ from the language's own default *and* be
    # a valid type name for that language's linter / compiler.
    type_overrides: dict[str, str] = {
        "Crystal": "Int32",
        "Go": "string",
        "CSharp": "string",
        "Mojo": "Int",
        "Python": "int",
        "Rust": "i32",
    }
    variants: list[_Variant] = []
    for lang_name, lang_config in _LANGUAGES.items():
        if not lang_config.lang_cls.supports_default_set_element_type:
            continue
        string_type = type_overrides.get(lang_name, "String")
        variants.append(
            _Variant(
                name=f"{lang_name}_default_set_element_type_string",
                spec=lang_config.lang_cls(
                    default_set_element_type=string_type
                ),
                wrap=lang_config.wrap,
                wrap_variable_name=lang_config.wrap_variable_name,
            )
        )
    return variants


@beartype
def _build_default_sequence_element_type_variants() -> Iterable[_Variant]:
    """Build default-sequence-type variants for languages that support it.

    For each language that advertises
    ``supports_default_sequence_element_type``, create a variant with a
    non-default value.
    """
    type_overrides: dict[str, str] = {
        "Go": "interface{}",
        "CSharp": "string",
        "Mojo": "Int",
        "Python": "int",
    }
    variants: list[_Variant] = []
    for lang_name, lang_config in _LANGUAGES.items():
        if not lang_config.lang_cls.supports_default_sequence_element_type:
            continue
        string_type = type_overrides.get(lang_name, "String")
        variants.append(
            _Variant(
                name=f"{lang_name}_default_sequence_element_type_string",
                spec=lang_config.lang_cls(
                    default_sequence_element_type=string_type,
                ),
                wrap=lang_config.wrap,
                wrap_variable_name=lang_config.wrap_variable_name,
            )
        )
    return variants


@beartype
def _build_default_dict_value_type_variants() -> Iterable[_Variant]:
    """Build default-dict-type variants for languages that support it.

    For each language that advertises ``supports_default_dict_value_type``,
    create a variant with a non-default value.
    """
    type_overrides: dict[str, str] = {
        "Crystal": "Int32",
        "Go": "interface{}",
        "CSharp": "object?",
        "Dart": "Object?",
        "Kotlin": "Comparable<*>?",
        "Mojo": "Int",
        "Python": "int",
        "Rust": "i32",
    }
    variants: list[_Variant] = []
    for lang_name, lang_config in _LANGUAGES.items():
        if not lang_config.lang_cls.supports_default_dict_value_type:
            continue
        string_type = type_overrides.get(lang_name, "String")
        variants.append(
            _Variant(
                name=f"{lang_name}_default_dict_value_type_string",
                spec=lang_config.lang_cls(default_dict_value_type=string_type),
                wrap=lang_config.wrap,
                wrap_variable_name=lang_config.wrap_variable_name,
            )
        )
    return variants


@beartype
def _build_default_dict_key_type_variants() -> Iterable[_Variant]:
    """Build default-dict-key-type variants for languages that support it.

    For each language that advertises ``supports_default_dict_key_type``,
    create a variant with a non-default key type.
    """
    type_overrides: dict[str, str] = {
        "Crystal": "Int32",
        "Go": "any",
        "CSharp": "object",
        "Dart": "Object",
        "Kotlin": "Any",
        "Python": "int",
        "Rust": "&str",
        "Swift": "AnyHashable",
        "VisualBasic": "Object",
    }
    variants: list[_Variant] = []
    for lang_name, lang_config in _LANGUAGES.items():
        if not lang_config.lang_cls.supports_default_dict_key_type:
            continue
        key_type = type_overrides.get(lang_name, "String")
        variants.append(
            _Variant(
                name=f"{lang_name}_default_dict_key_type",
                spec=lang_config.lang_cls(default_dict_key_type=key_type),
                wrap=lang_config.wrap,
                wrap_variable_name=lang_config.wrap_variable_name,
            )
        )
    return variants


@beartype
def _build_default_ordered_map_value_type_variants() -> Iterable[_Variant]:
    """Build default-ordered-map-value-type variants for languages that
    support it.

    For each language that advertises
    ``supports_default_ordered_map_value_type``, create a variant with a
    non-default value type.
    """
    type_overrides: dict[str, str] = {
        "Go": "interface{}",
    }
    variants: list[_Variant] = []
    for lang_name, lang_config in _LANGUAGES.items():
        if not lang_config.lang_cls.supports_default_ordered_map_value_type:
            continue
        value_type = type_overrides.get(lang_name, "String")
        variants.append(
            _Variant(
                name=f"{lang_name}_default_ordered_map_value_type",
                spec=lang_config.lang_cls(
                    default_ordered_map_value_type=value_type,
                ),
                wrap=lang_config.wrap,
                wrap_variable_name=lang_config.wrap_variable_name,
            )
        )
    return variants


@beartype
def _build_comment_variants() -> Iterable[_Variant]:
    """Build comment-format variants for all languages with multiple
    formats.

    For each language that has more than one comment format, create a variant
    for every non-default format.
    """
    variants: list[_Variant] = []
    for lang_name, lang_config in _LANGUAGES.items():
        spec = lang_config.lang_cls()
        default_format = spec.comment_format
        for fmt in list(spec.comment_formats):
            if fmt is default_format:
                continue
            variants.append(
                _Variant(
                    name=f"{lang_name}_comment_{fmt.name.lower()}",
                    spec=lang_config.lang_cls(comment_format=fmt),
                    wrap=lang_config.wrap,
                    wrap_variable_name=lang_config.wrap_variable_name,
                )
            )
    return variants


@beartype
def _build_type_hint_variants() -> Iterable[_Variant]:
    """Build variable-type-hint variants for all languages with multiple
    formats.

    For each language that has more than one variable type-hint format,
    create a variant for every non-default type-hint style.
    """
    variants: list[_Variant] = []
    for lang_name, lang_config in _LANGUAGES.items():
        spec = lang_config.lang_cls()
        default_format = spec.variable_type_hints
        for fmt in list(spec.variable_type_hints_formats):
            if fmt is default_format:
                continue
            variants.append(
                _Variant(
                    name=f"{lang_name}_type_hints_{fmt.name.lower()}",
                    spec=lang_config.lang_cls(variable_type_hints=fmt),
                    wrap=lang_config.wrap,
                    wrap_variable_name="my_data",
                )
            )
    return variants


@beartype
def _build_declaration_style_variants() -> Iterable[_Variant]:
    """Build declaration-style variants for all languages with multiple
    styles.
    """
    variants: list[_Variant] = []
    for lang_name, lang_config in _LANGUAGES.items():
        spec = lang_config.lang_cls()
        default_format = spec.declaration_style
        non_defaults = [
            fmt for fmt in spec.declaration_styles if fmt is not default_format
        ]
        variants.extend(
            _Variant(
                name=f"{lang_name}_declaration_style_{fmt.name.lower()}",
                spec=lang_config.lang_cls(
                    declaration_style=fmt,
                ),
                wrap=lang_config.wrap,
                wrap_variable_name=lang_config.wrap_variable_name,
            )
            for fmt in non_defaults
        )
    return variants


@beartype
def _build_dict_format_variants() -> Iterable[_Variant]:
    """Build dict/map-format variants for all languages with multiple
    formats.
    """
    variants: list[_Variant] = []
    for lang_name, lang_config in _LANGUAGES.items():
        spec = lang_config.lang_cls()
        default_format = spec.dict_format
        non_defaults = [
            fmt for fmt in spec.dict_formats if fmt is not default_format
        ]
        variants.extend(
            _Variant(
                name=f"{lang_name}_dict_format_{fmt.name.lower()}",
                spec=lang_config.lang_cls(
                    dict_format=fmt,
                ),
                wrap=lang_config.wrap,
                wrap_variable_name=lang_config.wrap_variable_name,
            )
            for fmt in non_defaults
        )
    return variants


@beartype
def _build_dict_entry_style_variants() -> Iterable[_Variant]:
    """Build dict-entry-style variants for all languages with multiple
    styles.
    """
    variants: list[_Variant] = []
    for lang_name, lang_config in _LANGUAGES.items():
        spec = lang_config.lang_cls()
        default_style = spec.dict_entry_style
        non_defaults = [
            fmt for fmt in spec.dict_entry_styles if fmt is not default_style
        ]
        variants.extend(
            _Variant(
                name=f"{lang_name}_dict_entry_style_{fmt.name.lower()}",
                spec=lang_config.lang_cls(
                    dict_entry_style=fmt,
                ),
                wrap=lang_config.wrap,
                wrap_variable_name=lang_config.wrap_variable_name,
            )
            for fmt in non_defaults
        )
    return variants


@beartype
def _build_integer_format_variants() -> Iterable[_Variant]:
    """Build integer-format variants for all languages with multiple
    formats.
    """
    variants: list[_Variant] = []
    for lang_name, lang_config in _LANGUAGES.items():
        spec = lang_config.lang_cls()
        default_format = spec.integer_format
        non_defaults = [
            fmt for fmt in spec.integer_formats if fmt is not default_format
        ]
        variants.extend(
            _Variant(
                name=f"{lang_name}_integer_format_{fmt.name.lower()}",
                spec=lang_config.lang_cls(
                    integer_format=fmt,
                ),
                wrap=lang_config.wrap,
                wrap_variable_name=lang_config.wrap_variable_name,
            )
            for fmt in non_defaults
        )
    return variants


@beartype
def _build_numeric_literal_suffix_variants() -> Iterable[_Variant]:
    """Build numeric-literal-suffix variants for all languages with
    multiple options.
    """
    variants: list[_Variant] = []
    for lang_name, lang_config in _LANGUAGES.items():
        spec = lang_config.lang_cls()
        default_format = spec.numeric_literal_suffix
        non_defaults = [
            fmt
            for fmt in spec.numeric_literal_suffixes
            if fmt is not default_format
        ]
        variants.extend(
            _Variant(
                name=f"{lang_name}_numeric_literal_suffix_{fmt.name.lower()}",
                spec=lang_config.lang_cls(
                    numeric_literal_suffix=fmt,
                ),
                wrap=lang_config.wrap,
                wrap_variable_name=lang_config.wrap_variable_name,
            )
            for fmt in non_defaults
        )
    return variants


@beartype
def _build_numeric_separator_variants() -> Iterable[_Variant]:
    """Build numeric-separator variants for all languages with multiple
    options.
    """
    variants: list[_Variant] = []
    for lang_name, lang_config in _LANGUAGES.items():
        spec = lang_config.lang_cls()
        default_format = spec.numeric_separator
        non_defaults = [
            fmt for fmt in spec.numeric_separators if fmt is not default_format
        ]
        variants.extend(
            _Variant(
                name=f"{lang_name}_numeric_separator_{fmt.name.lower()}",
                spec=lang_config.lang_cls(
                    numeric_separator=fmt,
                ),
                wrap=lang_config.wrap,
                wrap_variable_name=lang_config.wrap_variable_name,
            )
            for fmt in non_defaults
        )
    return variants


@beartype
def _build_float_format_variants() -> Iterable[_Variant]:
    """Build float-format variants for all languages with multiple
    formats.
    """
    variants: list[_Variant] = []
    for lang_name, lang_config in _LANGUAGES.items():
        spec = lang_config.lang_cls()
        default_format = spec.float_format
        non_defaults = [
            fmt for fmt in spec.float_formats if fmt is not default_format
        ]
        variants.extend(
            _Variant(
                name=f"{lang_name}_float_format_{fmt.name.lower()}",
                spec=lang_config.lang_cls(
                    float_format=fmt,
                ),
                wrap=lang_config.wrap,
                wrap_variable_name=lang_config.wrap_variable_name,
            )
            for fmt in non_defaults
        )
    return variants


@beartype
def _build_string_format_variants() -> Iterable[_Variant]:
    """Build string-format variants for all languages with multiple
    formats.
    """
    variants: list[_Variant] = []
    for lang_name, lang_config in _LANGUAGES.items():
        spec = lang_config.lang_cls()
        default_format = spec.string_format
        non_defaults = [
            fmt for fmt in spec.string_formats if fmt is not default_format
        ]
        variants.extend(
            _Variant(
                name=f"{lang_name}_string_format_{fmt.name.lower()}",
                spec=lang_config.lang_cls(
                    string_format=fmt,
                ),
                wrap=lang_config.wrap,
                wrap_variable_name=lang_config.wrap_variable_name,
            )
            for fmt in non_defaults
        )
    return variants


@beartype
def _build_bytes_format_variants() -> Iterable[_Variant]:
    """Build bytes-format variants for all languages with multiple
    formats.
    """
    variants: list[_Variant] = []
    for lang_name, lang_config in _LANGUAGES.items():
        spec = lang_config.lang_cls()
        default_format = spec.format_bytes
        non_defaults = [
            fmt for fmt in spec.bytes_formats if fmt is not default_format
        ]
        variants.extend(
            _Variant(
                name=f"{lang_name}_bytes_format_{fmt.name.lower()}",
                spec=lang_config.lang_cls(
                    bytes_format=fmt,
                ),
                wrap=lang_config.wrap,
                wrap_variable_name=lang_config.wrap_variable_name,
            )
            for fmt in non_defaults
        )
    return variants


@beartype
def _build_trailing_comma_variants() -> Iterable[_Variant]:
    """Build trailing-comma variants for all languages with multiple
    options.
    """
    variants: list[_Variant] = []
    for lang_name, lang_config in _LANGUAGES.items():
        spec = lang_config.lang_cls()
        default_format = spec.trailing_comma
        non_defaults = [
            fmt for fmt in spec.trailing_commas if fmt is not default_format
        ]
        variants.extend(
            _Variant(
                name=f"{lang_name}_trailing_comma_{fmt.name.lower()}",
                spec=lang_config.lang_cls(
                    trailing_comma=fmt,
                ),
                wrap=lang_config.wrap,
                wrap_variable_name=lang_config.wrap_variable_name,
            )
            for fmt in non_defaults
        )
    return variants


@beartype
def _build_line_ending_variants() -> Iterable[_Variant]:
    """Build line-ending variants for all languages with multiple
    options.
    """
    variants: list[_Variant] = []
    for lang_name, lang_config in _LANGUAGES.items():
        spec = lang_config.lang_cls()
        default_format = spec.line_ending
        non_defaults = [
            fmt for fmt in spec.line_endings if fmt is not default_format
        ]
        variants.extend(
            _Variant(
                name=f"{lang_name}_line_ending_{fmt.name.lower()}",
                spec=lang_config.lang_cls(
                    line_ending=fmt,
                ),
                wrap=lang_config.wrap,
                wrap_variable_name=lang_config.wrap_variable_name,
            )
            for fmt in non_defaults
        )
    return variants


@beartype
def _build_line_ending_decl_variants() -> Iterable[_Variant]:
    """Build line-ending + declaration-style cross-option variants.

    For each language with multiple line endings *and* multiple
    declaration styles, create a variant for every non-default
    line ending paired with every non-default declaration style.
    """
    variants: list[_Variant] = []
    for lang_name, lang_config in _LANGUAGES.items():
        spec = lang_config.lang_cls()
        default_line_ending = spec.line_ending
        default_ds = spec.declaration_style
        non_default_line_endings = [
            line_ending
            for line_ending in spec.line_endings
            if line_ending is not default_line_ending
        ]
        non_default_ds = [
            ds for ds in spec.declaration_styles if ds is not default_ds
        ]
        variants.extend(
            _Variant(
                name=(
                    f"{lang_name}_line_ending_{line_ending.name.lower()}"
                    f"_decl_{ds.name.lower()}"
                ),
                spec=lang_config.lang_cls(
                    line_ending=line_ending,
                    declaration_style=ds,
                ),
                wrap=lang_config.wrap,
                wrap_variable_name=lang_config.wrap_variable_name,
            )
            for line_ending in non_default_line_endings
            for ds in non_default_ds
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
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=lang_config.wrap_variable_name,
        new_variable=True,
        error_on_coercion=False,
    )
    variable_name = lang_config.wrap_variable_name or ""
    wrapped = lang_config.wrap(result.code, variable_name)

    wrapped = _prepend_preamble(wrapped=wrapped, preamble=result.preamble)
    # newline="" prevents Python text-mode from converting \r\n to \n
    # on Windows, which would corrupt golden files containing literal
    # CR bytes (e.g. CommonLisp string_control_chars).
    file_regression.check(
        contents=wrapped + "\n",
        extension=lang_config.lang_cls.extension,
        newline="",
        fullpath=input_path.parent
        / (language + lang_config.lang_cls.extension),
    )


@dataclasses.dataclass
class _CombinedCase:
    """A combined-variable-forms test case for a specific redefinition
    style.
    """

    case_name: str
    lang_name: str
    lang_config: _LanguageConfig
    declaration_style: enum.Enum
    golden_file_name: str


@beartype
def _discover_combined_cases() -> list[_CombinedCase]:
    """Return combined test cases for all redefinition-supporting
    styles.
    """
    cases_dir = Path(__file__).parent / "cases"
    cases: list[_CombinedCase] = []
    for case_dir in sorted(cases_dir.iterdir()):
        for lang_name, lang_config in _LANGUAGES.items():
            spec = lang_config.lang_cls()
            redef_styles = _find_redefinition_styles(spec=spec)
            for style in redef_styles:
                if style is redef_styles[0]:
                    golden_name = f"{lang_name}_combined"
                else:
                    style_suffix = style.name.lower()
                    golden_name = (
                        f"{lang_name}_combined"
                        f"_declaration_style_{style_suffix}"
                    )
                cases.append(
                    _CombinedCase(
                        case_name=case_dir.name,
                        lang_name=lang_name,
                        lang_config=lang_config,
                        declaration_style=style,
                        golden_file_name=golden_name,
                    )
                )
    return cases


_COMBINED_CASES = _discover_combined_cases()


@pytest.mark.parametrize(
    argnames="combined_case",
    argvalues=_COMBINED_CASES,
    ids=[f"{c.case_name}/{c.golden_file_name}" for c in _COMBINED_CASES],
)
def test_golden_file_combined_variable_forms(
    combined_case: _CombinedCase,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
) -> None:
    """Test that literalize_yaml with new_variable=True (declaration) and
    new_variable=False (assignment to existing variable) produce expected
    golden output, combined in one file to show the difference in syntax.
    """
    input_path = cases_dir / combined_case.case_name / "input.yaml"
    lang_config = combined_case.lang_config
    spec = lang_config.lang_cls(
        declaration_style=combined_case.declaration_style,
    )
    yaml_string = input_path.read_text()
    declaration = literalizer.literalize_yaml(
        yaml_string=yaml_string,
        language=spec,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name="my_data",
        new_variable=True,
        error_on_coercion=False,
    )
    assignment = literalizer.literalize_yaml(
        yaml_string=yaml_string,
        language=spec,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name="my_data",
        new_variable=False,
        error_on_coercion=False,
    )
    variable_name = lang_config.wrap_variable_name or ""
    combined = lang_config.combined_wrap(
        declaration.code,
        assignment.bare_code,
        variable_name,
    )
    combined = _prepend_preamble(
        wrapped=combined, preamble=declaration.preamble
    )
    file_regression.check(
        contents=combined + "\n",
        extension=lang_config.lang_cls.extension,
        newline="",
        fullpath=input_path.parent
        / (combined_case.golden_file_name + lang_config.lang_cls.extension),
    )


@beartype
def _build_variant_cases() -> list[_VariantCase]:
    """Collect all format-variant golden-file test cases."""
    cases: list[_VariantCase] = []
    variant_sources: list[tuple[Iterable[_Variant], str, str]] = [
        (_build_date_variants(), "scalar_date", ""),
        (_build_date_variants(), "date_list", ""),
        (_build_date_variants(), "date_set", ""),
        (_build_datetime_variants(), "scalar_datetime", ""),
        (_build_datetime_variants(), "scalar_datetime_naive", "_naive"),
        (_build_datetime_variants(), "scalar_datetime_non_utc", "_non_utc"),
        (_build_sequence_variants(), "simple_sequence", ""),
        (_build_sequence_variants(), "pair_sequence", "_pair"),
        (_build_sequence_variants(), "triple_sequence", "_triple"),
        (_build_sequence_varname_variants(), "simple_sequence", "_varname"),
        (_build_set_variants(), "set", ""),
        (_build_default_set_element_type_variants(), "empty_set", ""),
        (_build_default_set_element_type_variants(), "set", ""),
        (
            _build_default_sequence_element_type_variants(),
            "empty_sequence",
            "",
        ),
        (
            _build_default_sequence_element_type_variants(),
            "simple_sequence",
            "",
        ),
        (_build_default_dict_value_type_variants(), "empty_dict", ""),
        (_build_default_dict_value_type_variants(), "simple_dict", ""),
        (_build_default_dict_key_type_variants(), "empty_dict", ""),
        (_build_default_dict_key_type_variants(), "simple_dict", ""),
        (
            _build_default_ordered_map_value_type_variants(),
            "ordered_map",
            "",
        ),
        (_build_comment_variants(), "comments", ""),
        (_build_type_hint_variants(), "type_hints", ""),
        (_build_type_hint_variants(), "scalar_date", ""),
        (_build_type_hint_variants(), "scalar_datetime", ""),
        (_build_type_hint_variants(), "binary", ""),
        (_build_type_hint_variants(), "mixed_type_dicts_in_sequence", ""),
        (_build_type_hint_variants(), "empty_dicts_in_sequence", ""),
        (_build_declaration_style_variants(), "simple_sequence", ""),
        (_build_declaration_style_variants(), "simple_dict", ""),
        (_build_declaration_style_variants(), "empty_list", ""),
        (_build_dict_format_variants(), "simple_dict", ""),
        (_build_dict_format_variants(), "dict_with_list_value", "_list_val"),
        (_build_dict_entry_style_variants(), "simple_dict", ""),
        (
            _build_dict_entry_style_variants(),
            "dict_with_list_value",
            "_list_val",
        ),
        (_build_float_format_variants(), "float_list", ""),
        (_build_float_format_variants(), "float_scientific_notation", "_s"),
        (_build_float_format_variants(), "float_special_values", "_v"),
        (_build_float_format_variants(), "nested_float_list", "_n"),
        (_build_integer_format_variants(), "int_list", ""),
        (_build_integer_format_variants(), "int_list_large", "_large"),
        (_build_integer_format_variants(), "int_list_with_zero", "_zero"),
        (_build_numeric_literal_suffix_variants(), "int_list", ""),
        (_build_numeric_literal_suffix_variants(), "int_list_large", "_large"),
        (
            _build_numeric_literal_suffix_variants(),
            "int_list_with_zero",
            "_zero",
        ),
        (_build_numeric_separator_variants(), "int_list", ""),
        (_build_numeric_separator_variants(), "int_list_large", "_large"),
        (_build_numeric_separator_variants(), "int_list_with_zero", "_zero"),
        (_build_string_format_variants(), "string_list", ""),
        (_build_string_format_variants(), "string_with_backslash", ""),
        (_build_bytes_format_variants(), "binary", ""),
        (_build_trailing_comma_variants(), "simple_sequence", ""),
        (_build_line_ending_variants(), "simple_sequence", ""),
        (_build_line_ending_variants(), "simple_dict", "_dict"),
        (_build_line_ending_decl_variants(), "simple_sequence", ""),
    ]
    for variants, case_dir_name, suffix in variant_sources:
        cases.extend(
            _VariantCase(
                variant_name=f"{variant.name}{suffix}",
                variant=variant,
                case_dir_name=case_dir_name,
                variable_name=variant.wrap_variable_name,
            )
            for variant in variants
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
            pre_indent_level=0,
            include_delimiters=True,
            variable_name=variant_case.variable_name,
            new_variable=True,
            error_on_coercion=False,
        )
    except NullInCollectionError:
        pytest.skip("Format rejects null elements in this input")
    variable_name = variant.wrap_variable_name or ""
    wrapped = variant.wrap(result.code, variable_name)
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
        if not _find_redefinition_styles(spec=spec):
            continue
        default_line_ending = spec.line_ending
        for line_ending in spec.line_endings:
            if line_ending is default_line_ending:
                continue
            for case_dir_name in ("simple_sequence", "simple_dict"):
                name = (
                    f"{lang_name}_line_ending"
                    f"_{line_ending.name.lower()}_{case_dir_name}"
                )
                cases.append(
                    _LineEndingCombinedCase(
                        name=name,
                        lang_config=lang_config,
                        line_ending=line_ending,
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
    base_spec = case.lang_config.lang_cls()
    redef_styles = _find_redefinition_styles(spec=base_spec)
    assert redef_styles
    spec = case.lang_config.lang_cls(
        line_ending=case.line_ending,
        declaration_style=redef_styles[0],
    )
    declaration = literalizer.literalize_yaml(
        yaml_string=yaml_string,
        language=spec,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name="my_data",
        new_variable=True,
        error_on_coercion=False,
    )
    assignment = literalizer.literalize_yaml(
        yaml_string=yaml_string,
        language=spec,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name="my_data",
        new_variable=False,
        error_on_coercion=False,
    )
    combined = case.lang_config.combined_wrap(
        declaration.code,
        assignment.bare_code,
        case.lang_config.wrap_variable_name or "",
    )
    combined = _prepend_preamble(
        wrapped=combined, preamble=declaration.preamble
    )
    file_regression.check(
        contents=combined + "\n",
        extension=spec.extension,
        fullpath=input_path.parent / (case.name + spec.extension),
    )


def test_no_dead_golden_files(request: pytest.FixtureRequest) -> None:
    """Every file under ``cases/`` must be referenced by a parameterized
    test.  Orphaned golden files silently rot and waste repository space.
    """
    cases_dir = request.config.rootpath / "tests" / "integration" / "cases"
    expected: set[Path] = set()

    for case_dir in sorted(cases_dir.iterdir()):
        expected.add(case_dir / "input.yaml")

    for case_name, lang_name in _CASES:
        lang_config = _LANGUAGES[lang_name]
        ext = lang_config.lang_cls.extension
        expected.add(cases_dir / case_name / (lang_name + ext))

    for combined_case in _COMBINED_CASES:
        ext = combined_case.lang_config.lang_cls.extension
        expected.add(
            cases_dir
            / combined_case.case_name
            / (combined_case.golden_file_name + ext)
        )

    for variant_case in _FORMAT_VARIANT_CASES:
        ext = variant_case.variant.spec.extension
        expected.add(
            cases_dir
            / variant_case.case_dir_name
            / (variant_case.variant_name + ext)
        )

    for line_ending_case in _LINE_ENDING_COMBINED_CASES:
        line_ending_spec = line_ending_case.lang_config.lang_cls(
            line_ending=line_ending_case.line_ending,
        )
        expected.add(
            cases_dir
            / line_ending_case.case_dir_name
            / (line_ending_case.name + line_ending_spec.extension)
        )

    actual = {path for path in cases_dir.rglob(pattern="*") if path.is_file()}
    dead_files = sorted(
        path.relative_to(cases_dir) for path in actual - expected
    )
    assert not dead_files


def _lang_cls_name(cls: literalizer.LanguageCls) -> str:
    """Return the class name for sorting."""
    return cls.__name__


_SORTED_LANGUAGES: list[literalizer.LanguageCls] = sorted(
    ALL_LANGUAGES,
    key=_lang_cls_name,
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
    assert issubclass(spec.float_formats, enum.Enum)
    assert len(spec.float_formats) >= 1
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
