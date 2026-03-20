"""Integration tests that compare literalize_yaml output against golden
files.

Each subdirectory contains an ``input.yaml`` and one expected-output file
per supported language, using the real file extension for that language.

Golden files contain syntactically valid programs so that pre-commit hooks
can syntax-check them directly without additional wrapping.

To regenerate all golden files after changing output::

    uv run pytest tests/integration/ --regen-all
"""

from __future__ import annotations

import dataclasses
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from beartype import beartype
from pytest_regressions.file_regression import FileRegressionFixture

import literalizer
import literalizer.languages

if TYPE_CHECKING:
    from collections.abc import Callable

_CASES_DIR = Path(__file__).parent / "cases"


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
    return f"package main\n\nvar _ = {content}"


@beartype
def _wrap_java(content: str) -> str:
    """Wrap in a Java class with necessary imports."""
    return f"""\
import java.util.Map;
import java.util.Set;
class Check {{
    Object x = {content};
}}"""


@beartype
def _wrap_kotlin(content: str) -> str:
    """Wrap in a Kotlin variable assignment."""
    return f"val x: Any? = {content}"


@beartype
def _wrap_cpp(content: str) -> str:
    """Wrap in a C++ struct and function for type-flexible
    initialization.
    """
    return (
        "#include <initializer_list>\n"
        "#include <cstddef>\n"
        "#include <map>\n"
        "#include <string>\n"
        "#include <vector>\n"
        "struct _Any {\n"
        "    template<class T> _Any(T&&) noexcept {}\n"
        "    _Any(std::initializer_list<_Any>) noexcept {}\n"
        "};\n"
        "void _check() {\n"
        f"    [[maybe_unused]] _Any _v = {content};\n"
        "}"
    )


@beartype
def _wrap_swift(content: str) -> str:
    """Wrap in a Swift variable assignment."""
    return f"let x: Any? = {content}"


@beartype
def _wrap_csharp(content: str) -> str:
    """Wrap in C# using statement and variable assignment."""
    return f"""\
using System.Collections.Generic;
var x = {content};"""


@beartype
def _wrap_rust(content: str) -> str:
    """Wrap in a Rust main function with necessary imports."""
    indented = content.replace("\n", "\n    ")
    return (
        "use std::collections::HashMap;\n"
        "use std::collections::HashSet;\n"
        "fn main() {\n"
        f"    let _ = {indented};\n"
        "}"
    )


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


@beartype
def _wrap_fsharp(content: str) -> str:
    """Wrap in an F# module with a custom Val discriminated union."""
    typed = literalizer.languages.FSharp().format_sequence_entry(content)
    return (
        "module Check\n\n" + _FSHARP_VAL_TYPE + "\n" + f"let x: Val = {typed}"
    )


@beartype
def _wrap_ocaml(content: str) -> str:
    """Wrap in an OCaml module with a custom val_t variant type."""
    typed = literalizer.languages.OCaml().format_sequence_entry(content)
    return (
        "module Check = struct\n\n"
        + _OCAML_VAL_TYPE
        + "\n"
        + f"let x : val_t = {typed}\n\n"
        + "end"
    )


@beartype
def _wrap_ocaml_varname(content: str) -> str:
    """Wrap an OCaml ``let`` declaration with the val_t type
    definition.
    """
    return (
        "module Check = struct\n\n"
        + _OCAML_VAL_TYPE
        + "\n"
        + content
        + "\n\nend"
    )


@beartype
def _wrap_occam(content: str) -> str:
    """Wrap in an occam-pi PROC with a custom ``LIT`` mobile data type."""
    typed = literalizer.languages.Occam().format_sequence_entry(content)
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
    """Wrap an occam-pi ``VAL`` declaration in a PROC with the LIT
    type.
    """
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
    """Wrap a F# ``let`` declaration with the Val type definition."""
    return "module Check\n\n" + _FSHARP_VAL_TYPE + "\n" + content


@beartype
def _wrap_haskell(content: str) -> str:
    """Wrap in a Haskell module with a custom Val ADT that accepts mixed
    types.
    """
    return (
        "{-# LANGUAGE OverloadedStrings #-}\n"
        "module Check where\n"
        "import Data.String (IsString(fromString))\n"
        "data Val = HNull | HBool Bool | HInt Integer | HFloat Double"
        " | HStr String | HList [Val] | HMap [(String, Val)] | HSet [Val]\n"
        "instance IsString Val where\n"
        "    fromString = HStr\n"
        "instance Num Val where\n"
        "    fromInteger = HInt\n"
        '    a + b = error "not implemented"\n'
        '    a * b = error "not implemented"\n'
        '    abs a = error "not implemented"\n'
        '    signum a = error "not implemented"\n'
        "    negate (HInt n) = HInt (negate n)\n"
        "    negate (HFloat f) = HFloat (negate f)\n"
        '    negate _ = error "not implemented"\n'
        "instance Fractional Val where\n"
        "    fromRational r = HFloat (realToFrac r)\n"
        '    a / b = error "not implemented"\n'
        "x :: Val\n"
        f"x = {content}"
    )


@beartype
def _wrap_hcl(content: str) -> str:
    """Wrap in an HCL attribute assignment for syntax validation."""
    return f"_ = {content}"


_VARIABLE_NAME = "my_data"


@beartype
def _wrap_go_varname(content: str) -> str:
    """Wrap a Go short variable declaration in a main function."""
    return (
        f"package main\n\nfunc main() {{\n{content}\n_ = {_VARIABLE_NAME}\n}}"
    )


@beartype
def _wrap_java_varname(content: str) -> str:
    """Wrap a Java var declaration in a static method."""
    return (
        "import java.util.Map;\n"
        "import java.util.Set;\n"
        "class Check {\n"
        "    public static void check() {\n"
        f"{content}\n"
        "    }\n"
        "}"
    )


@beartype
def _wrap_rust_chrono(content: str) -> str:
    """Wrap in a Rust main function with chrono imports."""
    indented = content.replace("\n", "\n    ")
    return (
        "use chrono::{NaiveDate, NaiveDateTime, NaiveTime};\n"
        "use std::collections::HashMap;\n"
        "use std::collections::HashSet;\n"
        "fn main() {\n"
        f"    let _ = {indented};\n"
        "}"
    )


@beartype
def _wrap_csharp_varname(content: str) -> str:
    """Wrap a C# top-level variable declaration with required imports."""
    return f"using System.Collections.Generic;\n{content}"


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
    """Wrap a C++ variable declaration for mixed-type initializer lists.

    ``auto`` cannot deduce a type for mixed-type braced initializers, so
    the wrapper substitutes the custom ``_Any`` type that accepts any value.
    """
    old_prefix = f"auto {_VARIABLE_NAME} = "
    new_prefix = f"_Any {_VARIABLE_NAME} = "
    content_adapted = (
        new_prefix + content[len(old_prefix) :]
        if content.startswith(old_prefix)
        else content
    )
    return (
        "#include <initializer_list>\n"
        "#include <cstddef>\n"
        "#include <map>\n"
        "#include <string>\n"
        "#include <vector>\n"
        "struct _Any {\n"
        "    template<class T> _Any(T&&) noexcept {}\n"
        "    _Any(std::initializer_list<_Any>) noexcept {}\n"
        "};\n"
        "void _check() {\n"
        f"{content_adapted}\n"
        "}"
    )


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
def _wrap_racket(content: str) -> str:
    """Wrap in a Racket #lang racket module.

    Trailing whitespace is stripped from each line because the
    ``(list ``/``(hash ``/``(set `` opening delimiters produce a
    trailing space before the newline in multi-line mode, which the
    ``trim trailing whitespace`` pre-commit hook removes from the
    committed golden files.
    """
    cleaned = "\n".join(line.rstrip() for line in content.splitlines())
    return f"#lang racket\n{cleaned}"


@beartype
def _wrap_racket_combined(declaration: str, assignment: str) -> str:
    """Wrap Racket declaration and assignment in a #lang racket module."""
    combined = f"{declaration}\n{assignment}"
    cleaned = "\n".join(line.rstrip() for line in combined.splitlines())
    return f"#lang racket\n{cleaned}"


@beartype
def _wrap_perl(content: str) -> str:
    """Wrap in a Perl variable assignment."""
    return f"my $x = {content};"


@beartype
def _wrap_php(content: str) -> str:
    """Wrap in a PHP script variable assignment."""
    return f"<?php\n$x = {content};"


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
    typed = literalizer.languages.Ada().format_sequence_entry(content)
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
    """Wrap in a Nim import json and %* expression."""
    return f"import json\nlet _ = %*{content}"


@beartype
def _wrap_nim_varname(content: str) -> str:
    """Wrap a Nim var declaration with the json import."""
    return f"import json\n{content}"


@beartype
def _wrap_nim_combined(declaration: str, assignment: str) -> str:
    """Wrap Nim declaration and assignment with the json import."""
    return f"import json\n{declaration}\n{assignment}"


@beartype
def _wrap_d(content: str) -> str:
    """Wrap in a D function with ``std.json`` imported."""
    typed = literalizer.languages.D().format_sequence_entry(content)
    return f"import std.json;\n\nvoid _check() {{\n    auto _v = {typed};\n}}"


@beartype
def _wrap_d_varname(content: str) -> str:
    """Wrap a D ``auto`` declaration in a function with ``std.json``
    imported.
    """
    return f"import std.json;\n\nvoid _check() {{\n{content}\n}}"


@beartype
def _wrap_d_combined(declaration: str, assignment: str) -> str:
    """Wrap D declaration and assignment together in one function."""
    return (
        "import std.json;\n"
        "\n"
        "void _check() {\n"
        f"{declaration}\n"
        f"{assignment}\n"
        "}"
    )


@beartype
def _wrap_powershell(content: str) -> str:
    """Wrap in a PowerShell variable assignment."""
    return f"$x = {content}"


_C_PREAMBLE = (
    "#include <stdbool.h>\n"
    "#include <stddef.h>\n"
    "typedef struct _CVal _CVal;\n"
    "typedef struct _CKV _CKV;\n"
    "struct _CVal {\n"
    "    union {\n"
    "        _Bool b;\n"
    "        long long i;\n"
    "        double f;\n"
    "        const char *s;\n"
    "        const _CVal *a;\n"
    "        const _CKV *m;\n"
    "    };\n"
    "};\n"
    "struct _CKV { const char *k; _CVal v; };\n"
)


@beartype
def _wrap_c(content: str) -> str:
    """Wrap in a C function with the _CVal/_CKV type definitions."""
    typed = literalizer.languages.C().format_sequence_entry(content)
    return (
        _C_PREAMBLE
        + "void _check(void) {\n"
        + f"    _CVal _v = {typed};\n"
        + "    (void)_v;\n"
        + "}"
    )


@beartype
def _wrap_c_varname(content: str) -> str:
    """Wrap a C _CVal declaration in a function with type definitions."""
    return (
        _C_PREAMBLE
        + "void _check(void) {\n"
        + f"{content}\n"
        + f"    (void){_VARIABLE_NAME};\n"
        + "}"
    )


@beartype
def _wrap_c_combined(declaration: str, assignment: str) -> str:
    """Wrap C declaration and assignment together in one function."""
    return (
        _C_PREAMBLE
        + "void _check(void) {\n"
        + f"{declaration}\n"
        + f"{assignment}\n"
        + f"    (void){_VARIABLE_NAME};\n"
        + "}"
    )


@beartype
def _wrap_matlab(content: str) -> str:
    """Wrap in a MATLAB/Octave variable assignment."""
    return f"x = {content};"


@beartype
def _in_mojo_main(content: str) -> str:
    """Indent content and wrap in a Mojo ``def main():`` function."""
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
    """Wrap a Mojo variable assignment in a main function."""
    return _in_mojo_main(content=content)


@beartype
def _wrap_mojo_combined(declaration: str, assignment: str) -> str:
    """Wrap Mojo declaration and assignment in a main function."""
    return _in_mojo_main(content=declaration + "\n" + assignment)


@beartype
def _wrap_rust_varname(content: str) -> str:
    """Wrap a Rust let binding in a main function."""
    indented = content.replace("\n", "\n    ")
    return (
        "use std::collections::HashMap;\n"
        "use std::collections::HashSet;\n"
        "fn main() {\n"
        f"    {indented}\n"
        f"    let _ = {_VARIABLE_NAME};\n"
        "}"
    )


@beartype
def _wrap_haskell_varname(content: str) -> str:
    """Wrap a Haskell variable binding in module boilerplate."""
    return (
        "{-# LANGUAGE OverloadedStrings #-}\n"
        "module Check where\n"
        "import Data.String (IsString(fromString))\n"
        "data Val = HNull | HBool Bool | HInt Integer | HFloat Double"
        " | HStr String | HList [Val] | HMap [(String, Val)] | HSet [Val]\n"
        "instance IsString Val where\n"
        "    fromString = HStr\n"
        "instance Num Val where\n"
        "    fromInteger = HInt\n"
        '    a + b = error "not implemented"\n'
        '    a * b = error "not implemented"\n'
        '    abs a = error "not implemented"\n'
        '    signum a = error "not implemented"\n'
        "    negate (HInt n) = HInt (negate n)\n"
        "    negate (HFloat f) = HFloat (negate f)\n"
        '    negate _ = error "not implemented"\n'
        "instance Fractional Val where\n"
        "    fromRational r = HFloat (realToFrac r)\n"
        '    a / b = error "not implemented"\n'
        f"{_VARIABLE_NAME} :: Val\n"
        f"{content}"
    )


@beartype
def _wrap_php_varname(content: str) -> str:
    """Wrap a PHP variable assignment in a PHP script."""
    return f"<?php\n{content}"


_ZIG_PREAMBLE = (
    "const ZVal = union(enum) {\n"
    "    nil,\n"
    "    bool: bool,\n"
    "    int: i64,\n"
    "    float: f64,\n"
    "    str: []const u8,\n"
    "    arr: []const ZVal,\n"
    "    map: []const ZKV,\n"
    "    set: []const ZVal,\n"
    "};\n"
    "const ZKV = struct { key: []const u8, val: ZVal };\n"
)


@beartype
def _wrap_zig(content: str) -> str:
    """Wrap in a Zig main function with ``ZVal``/``ZKV`` type
    definitions.
    """
    typed = literalizer.languages.Zig().format_sequence_entry(content)
    indented = typed.replace("\n", "\n    ")
    return (
        _ZIG_PREAMBLE
        + "pub fn main() void {\n"
        + f"    const v: ZVal = {indented};\n"
        + "    _ = v;\n"
        + "}"
    )


@beartype
def _wrap_zig_varname(content: str) -> str:
    """Wrap a Zig ``const`` declaration in a main function."""
    indented = "    " + content.replace("\n", "\n    ")
    return (
        _ZIG_PREAMBLE
        + "pub fn main() void {\n"
        + f"{indented}\n"
        + f"    _ = {_VARIABLE_NAME};\n"
        + "}"
    )


@beartype
def _wrap_zig_combined(declaration: str, assignment: str) -> str:
    """Zig: ``const`` declaration in an inner block, then ``var`` +
    assignment in the outer scope.
    """
    decl_indented = "        " + declaration.replace("\n", "\n        ")
    assign_indented = "    " + assignment.replace("\n", "\n    ")
    return (
        _ZIG_PREAMBLE
        + "pub fn main() void {\n"
        + "    {\n"
        + f"{decl_indented}\n"
        + f"        _ = {_VARIABLE_NAME};\n"
        + "    }\n"
        + f"    var {_VARIABLE_NAME}: ZVal = undefined;\n"
        + f"{assign_indented}\n"
        + f"    const _{_VARIABLE_NAME}_read = {_VARIABLE_NAME};\n"
        + f"    _ = _{_VARIABLE_NAME}_read;\n"
        + "}"
    )


@beartype
def _wrap_swift_varname(content: str) -> str:
    """Add type annotation to Swift let declaration for mixed-type
    collections.

    The content from format_variable_declaration_swift is like
    "let my_data = [...]", and we need to add a type annotation for Swift
    to accept heterogeneous collections.
    """
    prefix = f"let {_VARIABLE_NAME}"
    return prefix + ": Any =" + content[len(prefix) + 2 :]


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
    """Swift: let declaration (with type annotation) in a do block,
    then var + assignment in the outer scope.
    """
    annotated = _wrap_swift_varname(content=declaration)
    decl_indented = "    " + annotated.replace("\n", "\n    ")
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
        "use std::collections::HashMap;\n"
        "use std::collections::HashSet;\n"
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


_FORTRAN_PREAMBLE = (
    "module fval_m\n"
    "  implicit none\n"
    "  type :: fval_t\n"
    "    integer :: t = 0\n"
    "  end type fval_t\n"
    "contains\n"
    "  function fnull() result(v)"
    "; type(fval_t) :: v; end function\n"
    "  function fbool(b) result(v)"
    "; logical, intent(in) :: b"
    "; type(fval_t) :: v; end function\n"
    "  function fint(n) result(v)"
    "; integer, intent(in) :: n"
    "; type(fval_t) :: v; end function\n"
    "  function freal(x) result(v)"
    "; real, intent(in) :: x"
    "; type(fval_t) :: v; end function\n"
    "  function fstr(s) result(v)"
    "; character(len=*), intent(in) :: s"
    "; type(fval_t) :: v; end function\n"
    "  function flist(a) result(v)"
    "; type(fval_t), intent(in) :: a(:)"
    "; type(fval_t) :: v; end function\n"
    "  function fmap(a) result(v)"
    "; type(fval_t), intent(in) :: a(:)"
    "; type(fval_t) :: v; end function\n"
    "  function fset(a) result(v)"
    "; type(fval_t), intent(in) :: a(:)"
    "; type(fval_t) :: v; end function\n"
    "  function fentry(k, u) result(v)"
    "; character(len=*), intent(in) :: k"
    "; type(fval_t), intent(in) :: u"
    "; type(fval_t) :: v; end function\n"
    "end module fval_m\n"
)


def _fortran_comment_pos(line: str) -> int | None:
    """Return the index of the ``!`` comment in *line* outside strings."""
    in_single_quote = False
    in_double_quote = False
    i = 0
    while i < len(line):
        c = line[i]
        if c == "'" and not in_double_quote:
            next_also_quote = i + 1 < len(line) and line[i + 1] == "'"
            if in_single_quote and next_also_quote:  # pragma: no cover
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
    typed = literalizer.languages.Fortran().format_sequence_entry(content)
    continued = _add_fortran_continuation(content=typed)
    return (
        _FORTRAN_PREAMBLE + "program check\n"
        "  use fval_m\n"
        "  implicit none\n"
        "  type(fval_t) :: x\n"
        f"  x = {continued}\n"
        "end program check"
    )


@beartype
def _wrap_fortran_varname(content: str) -> str:
    """Wrap a Fortran variable declaration in a self-contained program."""
    indented = "  " + content.replace("\n", "\n  ")
    return (
        _FORTRAN_PREAMBLE + "program check\n"
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
        _FORTRAN_PREAMBLE + "subroutine check_declaration()\n"
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
def _wrap_python_datetime(content: str) -> str:
    """Wrap with a datetime import for native Python date literals."""
    return f"import datetime\n{content}"


@beartype
def _wrap_java_time(content: str) -> str:
    """Wrap in a Java class with java.time.* imports."""
    return f"""\
import java.time.Instant;
import java.time.LocalDate;
import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.util.Map;
import java.util.Set;
class Check {{
    Object x = {content};
}}"""


@beartype
def _wrap_kotlin_time(content: str) -> str:
    """Wrap in a Kotlin variable assignment with java.time imports."""
    return (
        f"import java.time.LocalDate\n"
        f"import java.time.LocalDateTime\n"
        f"val x: Any? = {content}"
    )


@beartype
def _wrap_go_time(content: str) -> str:
    """Wrap in a Go package with the time package imported."""
    return f'package main\n\nimport "time"\n\nvar _ = {content}'


@beartype
def _wrap_cpp_chrono(content: str) -> str:
    """Wrap in C++ with the chrono header included."""
    return (
        "#include <chrono>\n"
        "#include <initializer_list>\n"
        "#include <cstddef>\n"
        "#include <map>\n"
        "#include <string>\n"
        "#include <vector>\n"
        "struct _Any {\n"
        "    template<class T> _Any(T&&) noexcept {}\n"
        "    _Any(std::initializer_list<_Any>) noexcept {}\n"
        "};\n"
        "void _check() {\n"
        f"    [[maybe_unused]] _Any _v = {content};\n"
        "}"
    )


@beartype
def _wrap_csharp_date(content: str) -> str:
    """Wrap in C# with System and Collections.Generic namespaces."""
    return (
        f"using System;\nusing System.Collections.Generic;\nvar x = {content};"
    )


@beartype
def _wrap_ruby_date(content: str) -> str:
    """Wrap with require 'date' for Ruby Date literals."""
    return f"require 'date'\n{content}"


@beartype
def _wrap_crystal(content: str) -> str:
    """Wrap in a Crystal variable assignment to suppress unused-expression
    warnings. Adds ``require "set"`` when the content uses ``Set{``.
    """
    prefix = 'require "set"\n' if "Set{" in content else ""
    return f"{prefix}_ = {content}"


@beartype
def _wrap_crystal_varname(content: str) -> str:
    """Identity wrap for Crystal, but adds ``require "set"`` when the
    content uses ``Set{``.
    """
    if "Set{" in content:
        return f'require "set"\n{content}'
    return content


@beartype
def _wrap_crystal_combined(declaration: str, assignment: str) -> str:
    """Join Crystal declaration and assignment with a newline, adding
    ``require "set"`` when either uses ``Set{``.
    """
    combined = declaration + "\n" + assignment
    if "Set{" in combined:
        return f'require "set"\n{combined}'
    return combined


@beartype
def _wrap_julia_dates(content: str) -> str:
    """Wrap with ``using Dates`` for native Julia date literals."""
    return f"using Dates\n{content}"


@beartype
def _wrap_vb(content: str) -> str:
    """Wrap in a VB.NET Module with a Dim declaration.

    Leading comment lines (starting with ``'``) are hoisted before the
    ``Dim`` statement so that the output remains valid VB.NET.
    """
    lines = content.split(sep="\n")
    comment_lines: list[str] = []
    while lines and lines[0].startswith("'"):
        comment_lines.append("    " + lines.pop(0))
    rest = "\n".join(lines)
    rest_indented = rest.replace("\n", "\n    ")
    dim_line = f"    Dim x As Object = {rest_indented}"
    body = "\n".join([*comment_lines, dim_line]) if comment_lines else dim_line
    return (
        f"Imports System.Collections.Generic\nModule Check\n{body}\nEnd Module"
    )


@beartype
def _wrap_vb_varname(content: str) -> str:
    """Wrap a VB.NET Dim declaration inside a Module."""
    indented = "    " + content.replace("\n", "\n    ")
    return (
        "Imports System.Collections.Generic\n"
        "Module Check\n"
        f"{indented}\n"
        "End Module"
    )


@beartype
def _wrap_vb_combined(declaration: str, assignment: str) -> str:
    """VB.NET: Dim declaration in one Sub, assignment in another."""
    decl_indented = "        " + declaration.replace("\n", "\n        ")
    assign_indented = "        " + assignment.replace("\n", "\n        ")
    return (
        "Imports System.Collections.Generic\n"
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


@dataclasses.dataclass
class _DateVariant:
    """A date/datetime formatting variant for a language."""

    spec: literalizer.Language
    extension: str
    wrap: Callable[[str], str]


@dataclasses.dataclass
class _SequenceVariant:
    """A sequence-type formatting variant for a language."""

    spec: literalizer.Language
    extension: str
    wrap: Callable[[str], str]


@dataclasses.dataclass
class _SetVariant:
    """A set-type formatting variant for a language."""

    spec: literalizer.Language
    extension: str
    wrap: Callable[[str], str]


@dataclasses.dataclass
class _LanguageConfig:
    """Language configuration with spec, file extension, and wrapper."""

    spec: literalizer.Language
    extension: str
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
        entry = literalizer.languages.Cobol().format_sequence_entry(scalar)
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
    "ada": _LanguageConfig(
        spec=literalizer.languages.Ada(),
        extension=".adb",
        wrap=_wrap_ada,
        varname_wrap=_wrap_ada_varname,
        combined_wrap=_wrap_ada_combined,
    ),
    "bash": _LanguageConfig(
        spec=literalizer.languages.Bash(),
        extension=".sh",
        wrap=_wrap_bash,
        varname_wrap=_wrap_identity,
        combined_wrap=_wrap_combined_newline,
    ),
    "c": _LanguageConfig(
        spec=literalizer.languages.C(),
        extension=".c",
        wrap=_wrap_c,
        varname_wrap=_wrap_c_varname,
        combined_wrap=_wrap_c_combined,
    ),
    "cobol": _LanguageConfig(
        spec=literalizer.languages.Cobol(),
        extension=".cob",
        wrap=_wrap_cobol,
        varname_wrap=_wrap_cobol_varname,
        combined_wrap=_wrap_cobol_combined,
    ),
    "d": _LanguageConfig(
        spec=literalizer.languages.D(),
        extension=".d",
        wrap=_wrap_d,
        varname_wrap=_wrap_d_varname,
        combined_wrap=_wrap_d_combined,
    ),
    "common_lisp": _LanguageConfig(
        spec=literalizer.languages.CommonLisp(),
        extension=".lisp",
        wrap=_wrap_identity,
        varname_wrap=_wrap_identity,
        combined_wrap=_wrap_combined_newline,
    ),
    "clojure": _LanguageConfig(
        spec=literalizer.languages.Clojure(),
        extension=".clj",
        wrap=_wrap_identity,
        varname_wrap=_wrap_identity,
        combined_wrap=_wrap_combined_newline,
    ),
    "python": _LanguageConfig(
        spec=literalizer.languages.Python(),
        extension=".py",
        wrap=_wrap_identity,
        varname_wrap=_wrap_identity,
        combined_wrap=_wrap_combined_newline,
    ),
    "javascript": _LanguageConfig(
        spec=literalizer.languages.JavaScript(),
        extension=".js",
        wrap=_wrap_js,
        varname_wrap=_wrap_identity,
        combined_wrap=_wrap_js_combined,
    ),
    "typescript": _LanguageConfig(
        spec=literalizer.languages.TypeScript(),
        extension=".ts",
        wrap=_wrap_js,
        varname_wrap=_wrap_ts_varname,
        combined_wrap=_wrap_ts_combined,
    ),
    "kotlin": _LanguageConfig(
        spec=literalizer.languages.Kotlin(),
        extension=".kts",
        wrap=_wrap_kotlin,
        varname_wrap=_wrap_identity,
        combined_wrap=_wrap_kotlin_combined,
    ),
    "ruby": _LanguageConfig(
        spec=literalizer.languages.Ruby(),
        extension=".rb",
        wrap=_wrap_identity,
        varname_wrap=_wrap_identity,
        combined_wrap=_wrap_combined_newline,
    ),
    "go": _LanguageConfig(
        spec=literalizer.languages.Go(),
        extension=".go",
        wrap=_wrap_go,
        varname_wrap=_wrap_go_varname,
        combined_wrap=lambda d, a: _wrap_go_varname(content=d + "\n" + a),
    ),
    "java": _LanguageConfig(
        spec=literalizer.languages.Java(),
        extension=".java",
        wrap=_wrap_java,
        varname_wrap=_wrap_java_varname,
        combined_wrap=lambda d, a: _wrap_java_varname(content=d + "\n" + a),
    ),
    "csharp": _LanguageConfig(
        spec=literalizer.languages.CSharp(),
        extension=".cs",
        wrap=_wrap_csharp,
        varname_wrap=_wrap_csharp_varname,
        combined_wrap=lambda d, a: _wrap_csharp_varname(content=d + "\n" + a),
    ),
    "dart": _LanguageConfig(
        spec=literalizer.languages.Dart(),
        extension=".dart",
        wrap=_wrap_dart,
        varname_wrap=_wrap_identity,
        combined_wrap=_wrap_dart_combined,
    ),
    "swift": _LanguageConfig(
        spec=literalizer.languages.Swift(),
        extension=".swift",
        wrap=_wrap_swift,
        varname_wrap=_wrap_swift_varname,
        combined_wrap=_wrap_swift_combined,
    ),
    "cpp": _LanguageConfig(
        spec=literalizer.languages.Cpp(),
        extension=".cpp",
        wrap=_wrap_cpp,
        varname_wrap=_wrap_cpp_varname,
        combined_wrap=lambda d, a: _wrap_cpp_varname(content=d + "\n" + a),
    ),
    "rust": _LanguageConfig(
        spec=literalizer.languages.Rust(),
        extension=".rs",
        wrap=_wrap_rust,
        varname_wrap=_wrap_rust_varname,
        combined_wrap=_wrap_rust_combined,
    ),
    "haskell": _LanguageConfig(
        spec=literalizer.languages.Haskell(),
        extension=".hs",
        wrap=_wrap_haskell,
        varname_wrap=_wrap_haskell_varname,
        combined_wrap=lambda d, _a: _wrap_haskell_varname(content=d),
    ),
    "hcl": _LanguageConfig(
        spec=literalizer.languages.Hcl(),
        extension=".hcl",
        wrap=_wrap_hcl,
        varname_wrap=_wrap_identity,
        combined_wrap=lambda d, _a: d,
    ),
    "julia": _LanguageConfig(
        spec=literalizer.languages.Julia(),
        extension=".jl",
        wrap=_wrap_identity,
        varname_wrap=_wrap_identity,
        combined_wrap=_wrap_combined_newline,
    ),
    "lua": _LanguageConfig(
        spec=literalizer.languages.Lua(),
        extension=".lua",
        wrap=_wrap_lua,
        varname_wrap=_wrap_identity,
        combined_wrap=_wrap_combined_newline,
    ),
    "perl": _LanguageConfig(
        spec=literalizer.languages.Perl(),
        extension=".pl",
        wrap=_wrap_perl,
        varname_wrap=_wrap_identity,
        combined_wrap=_wrap_combined_newline,
    ),
    "php": _LanguageConfig(
        spec=literalizer.languages.Php(),
        extension=".php",
        wrap=_wrap_php,
        varname_wrap=_wrap_php_varname,
        combined_wrap=lambda d, a: _wrap_php_varname(content=d + "\n" + a),
    ),
    "elixir": _LanguageConfig(
        spec=literalizer.languages.Elixir(),
        extension=".ex",
        wrap=_wrap_elixir,
        varname_wrap=_wrap_elixir_varname,
        combined_wrap=lambda d, _a: _wrap_elixir_varname(content=d),
    ),
    "erlang": _LanguageConfig(
        spec=literalizer.languages.Erlang(),
        extension=".erl",
        wrap=_wrap_erlang,
        varname_wrap=_wrap_erlang_varname,
        combined_wrap=lambda d, _a: _wrap_erlang_varname(content=d),
    ),
    "fsharp": _LanguageConfig(
        spec=literalizer.languages.FSharp(),
        extension=".fs",
        wrap=_wrap_fsharp,
        varname_wrap=_wrap_fsharp_varname,
        combined_wrap=lambda d, _a: _wrap_fsharp_varname(content=d),
    ),
    "ocaml": _LanguageConfig(
        spec=literalizer.languages.OCaml(),
        extension=".ml",
        wrap=_wrap_ocaml,
        varname_wrap=_wrap_ocaml_varname,
        combined_wrap=lambda d, _a: _wrap_ocaml_varname(content=d),
    ),
    "occam": _LanguageConfig(
        spec=literalizer.languages.Occam(),
        extension=".occ",
        wrap=_wrap_occam,
        varname_wrap=_wrap_occam_varname,
        combined_wrap=lambda d, _a: _wrap_occam_varname(content=d),
    ),
    "groovy": _LanguageConfig(
        spec=literalizer.languages.Groovy(),
        extension=".groovy",
        wrap=_wrap_groovy,
        varname_wrap=_wrap_identity,
        combined_wrap=_wrap_combined_newline,
    ),
    "scala": _LanguageConfig(
        spec=literalizer.languages.Scala(),
        extension=".scala",
        wrap=_wrap_scala,
        varname_wrap=_wrap_scala_varname,
        combined_wrap=_wrap_scala_combined,
    ),
    "r": _LanguageConfig(
        spec=literalizer.languages.R(),
        extension=".R",
        wrap=_wrap_r,
        varname_wrap=_wrap_identity,
        combined_wrap=_wrap_combined_newline,
    ),
    "racket": _LanguageConfig(
        spec=literalizer.languages.Racket(),
        extension=".rkt",
        wrap=_wrap_racket,
        varname_wrap=_wrap_racket,
        combined_wrap=_wrap_racket_combined,
    ),
    "crystal": _LanguageConfig(
        spec=literalizer.languages.Crystal(),
        extension=".cr",
        wrap=_wrap_crystal,
        varname_wrap=_wrap_crystal_varname,
        combined_wrap=_wrap_crystal_combined,
    ),
    "matlab": _LanguageConfig(
        spec=literalizer.languages.Matlab(),
        extension=".m",
        wrap=_wrap_matlab,
        varname_wrap=_wrap_identity,
        combined_wrap=_wrap_combined_newline,
    ),
    "mojo": _LanguageConfig(
        spec=literalizer.languages.Mojo(),
        extension=".mojo",
        wrap=_wrap_mojo,
        varname_wrap=_wrap_mojo_varname,
        combined_wrap=_wrap_mojo_combined,
    ),
    "nim": _LanguageConfig(
        spec=literalizer.languages.Nim(),
        extension=".nim",
        wrap=_wrap_nim,
        varname_wrap=_wrap_nim_varname,
        combined_wrap=_wrap_nim_combined,
    ),
    "vb": _LanguageConfig(
        spec=literalizer.languages.VisualBasic(),
        extension=".vb",
        wrap=_wrap_vb,
        varname_wrap=_wrap_vb_varname,
        combined_wrap=_wrap_vb_combined,
    ),
    "zig": _LanguageConfig(
        spec=literalizer.languages.Zig(),
        extension=".zig",
        wrap=_wrap_zig,
        varname_wrap=_wrap_zig_varname,
        combined_wrap=_wrap_zig_combined,
    ),
    "powershell": _LanguageConfig(
        spec=literalizer.languages.PowerShell(),
        extension=".ps1",
        wrap=_wrap_powershell,
        varname_wrap=_wrap_identity,
        combined_wrap=_wrap_combined_newline,
    ),
    "toml": _LanguageConfig(
        spec=literalizer.languages.Toml(),
        extension=".toml",
        wrap=_wrap_toml,
        varname_wrap=_wrap_identity,
        combined_wrap=lambda d, _a: d,
    ),
    "fortran": _LanguageConfig(
        spec=literalizer.languages.Fortran(),
        extension=".f90",
        wrap=_wrap_fortran,
        varname_wrap=_wrap_fortran_varname,
        combined_wrap=_wrap_fortran_combined,
    ),
    "yaml": _LanguageConfig(
        spec=literalizer.languages.Yaml(),
        extension=".yaml",
        wrap=_wrap_identity,
        varname_wrap=_wrap_identity,
        combined_wrap=lambda d, _a: d,
    ),
}


_DATE_VARIANTS: dict[str, _DateVariant] = {
    "python_native": _DateVariant(
        spec=literalizer.languages.Python(
            date_format=literalizer.languages.Python.DateFormat.PYTHON,
            datetime_format=literalizer.languages.Python.DatetimeFormat.PYTHON,
        ),
        extension=".py",
        wrap=_wrap_python_datetime,
    ),
    "python_epoch": _DateVariant(
        spec=literalizer.languages.Python(
            datetime_format=literalizer.languages.Python.DatetimeFormat.EPOCH,
        ),
        extension=".py",
        wrap=_wrap_identity,
    ),
    "js_native": _DateVariant(
        spec=literalizer.languages.JavaScript(
            date_format=literalizer.languages.JavaScript.DateFormat.JS,
            datetime_format=literalizer.languages.JavaScript.DatetimeFormat.JS,
        ),
        extension=".js",
        wrap=_wrap_js,
    ),
    "ts_native": _DateVariant(
        spec=literalizer.languages.TypeScript(
            date_format=literalizer.languages.TypeScript.DateFormat.JS,
            datetime_format=literalizer.languages.TypeScript.DatetimeFormat.JS,
        ),
        extension=".ts",
        wrap=_wrap_js,
    ),
    "kotlin_native": _DateVariant(
        spec=literalizer.languages.Kotlin(
            date_format=literalizer.languages.Kotlin.DateFormat.KOTLIN,
            datetime_format=literalizer.languages.Kotlin.DatetimeFormat.KOTLIN,
        ),
        extension=".kts",
        wrap=_wrap_kotlin_time,
    ),
    "ruby_native": _DateVariant(
        spec=literalizer.languages.Ruby(
            date_format=literalizer.languages.Ruby.DateFormat.RUBY,
            datetime_format=literalizer.languages.Ruby.DatetimeFormat.RUBY,
        ),
        extension=".rb",
        wrap=_wrap_ruby_date,
    ),
    "go_native": _DateVariant(
        spec=literalizer.languages.Go(
            date_format=literalizer.languages.Go.DateFormat.GO,
            datetime_format=literalizer.languages.Go.DatetimeFormat.GO,
        ),
        extension=".go",
        wrap=_wrap_go_time,
    ),
    "java_instant": _DateVariant(
        spec=literalizer.languages.Java(
            date_format=literalizer.languages.Java.DateFormat.JAVA,
            datetime_format=literalizer.languages.Java.DatetimeFormat.INSTANT,
        ),
        extension=".java",
        wrap=_wrap_java_time,
    ),
    "java_zoned": _DateVariant(
        spec=literalizer.languages.Java(
            date_format=literalizer.languages.Java.DateFormat.JAVA,
            datetime_format=literalizer.languages.Java.DatetimeFormat.ZONED,
        ),
        extension=".java",
        wrap=_wrap_java_time,
    ),
    "csharp_native": _DateVariant(
        spec=literalizer.languages.CSharp(
            date_format=literalizer.languages.CSharp.DateFormat.CSHARP,
            datetime_format=literalizer.languages.CSharp.DatetimeFormat.CSHARP,
        ),
        extension=".cs",
        wrap=_wrap_csharp_date,
    ),
    "dart_native": _DateVariant(
        spec=literalizer.languages.Dart(
            date_format=literalizer.languages.Dart.DateFormat.DART,
            datetime_format=literalizer.languages.Dart.DatetimeFormat.DART,
        ),
        extension=".dart",
        wrap=_wrap_dart,
    ),
    "cpp_native": _DateVariant(
        spec=literalizer.languages.Cpp(
            date_format=literalizer.languages.Cpp.DateFormat.CPP,
            datetime_format=literalizer.languages.Cpp.DatetimeFormat.CPP,
        ),
        extension=".cpp",
        wrap=_wrap_cpp_chrono,
    ),
    "rust_native": _DateVariant(
        spec=literalizer.languages.Rust(
            date_format=literalizer.languages.Rust.DateFormat.RUST,
            datetime_format=literalizer.languages.Rust.DatetimeFormat.RUST,
        ),
        extension=".rs",
        wrap=_wrap_rust_chrono,
    ),
    "julia_native": _DateVariant(
        spec=literalizer.languages.Julia(
            date_format=literalizer.languages.Julia.DateFormat.JULIA,
            datetime_format=literalizer.languages.Julia.DatetimeFormat.JULIA,
        ),
        extension=".jl",
        wrap=_wrap_julia_dates,
    ),
    "r_native": _DateVariant(
        spec=literalizer.languages.R(
            date_format=literalizer.languages.R.DateFormat.R,
            datetime_format=literalizer.languages.R.DatetimeFormat.R,
        ),
        extension=".R",
        wrap=_wrap_r,
    ),
}


_SEQUENCE_VARIANTS: dict[str, _SequenceVariant] = {
    "python_list": _SequenceVariant(
        spec=literalizer.languages.Python(
            sequence_format=literalizer.languages.Python.SequenceFormat.LIST,
        ),
        extension=".py",
        wrap=_wrap_identity,
    ),
    "julia_tuple": _SequenceVariant(
        spec=literalizer.languages.Julia(
            sequence_format=literalizer.languages.Julia.SequenceFormat.TUPLE,
        ),
        extension=".jl",
        wrap=_wrap_identity,
    ),
    "elixir_tuple": _SequenceVariant(
        spec=literalizer.languages.Elixir(
            sequence_format=literalizer.languages.Elixir.SequenceFormat.TUPLE,
        ),
        extension=".ex",
        wrap=_wrap_elixir,
    ),
    "erlang_tuple": _SequenceVariant(
        spec=literalizer.languages.Erlang(
            sequence_format=literalizer.languages.Erlang.SequenceFormat.TUPLE,
        ),
        extension=".erl",
        wrap=_wrap_erlang,
    ),
    "crystal_tuple": _SequenceVariant(
        spec=literalizer.languages.Crystal(
            sequence_format=literalizer.languages.Crystal.SequenceFormat.TUPLE,
        ),
        extension=".cr",
        wrap=_wrap_crystal,
    ),
}


@beartype
def _discover_cases() -> list[tuple[str, str, Path]]:
    """Return ``(case_name, language, input_path)`` tuples."""
    cases: list[tuple[str, str, Path]] = []
    for case_dir in sorted(_CASES_DIR.iterdir()):
        cases.extend(
            (case_dir.name, lang_name, case_dir / "input.yaml")
            for lang_name in _LANGUAGES
        )
    return cases


_CASES = _discover_cases()


@pytest.mark.parametrize(
    argnames=("_case_name", "language", "input_path"),
    argvalues=_CASES,
    ids=[f"{c[0]}/{c[1]}" for c in _CASES],
)
def test_golden_file(
    _case_name: str,
    language: str,
    input_path: Path,
    file_regression: FileRegressionFixture,
) -> None:
    """Test that literalize_yaml output matches expected golden file."""
    lang_config = _LANGUAGES[language]
    yaml_string = input_path.read_text()
    result = literalizer.literalize_yaml(
        yaml_string=yaml_string,
        language=lang_config.spec,
        line_prefix="",
        wrap=True,
    )
    wrapped = lang_config.wrap(result)
    file_regression.check(
        contents=wrapped + "\n",
        extension=lang_config.extension,
        fullpath=input_path.parent / (language + lang_config.extension),
    )


@pytest.mark.parametrize(
    argnames=("_case_name", "language", "input_path"),
    argvalues=_CASES,
    ids=[f"{c[0]}/{c[1]}" for c in _CASES],
)
def test_golden_file_with_variable_name(
    _case_name: str,
    language: str,
    input_path: Path,
    file_regression: FileRegressionFixture,
) -> None:
    """Test that literalize_yaml with variable_name matches golden
    file.
    """
    lang_config = _LANGUAGES[language]
    yaml_string = input_path.read_text()
    result = literalizer.literalize_yaml(
        yaml_string=yaml_string,
        language=lang_config.spec,
        line_prefix="",
        wrap=True,
        variable_name=_VARIABLE_NAME,
    )
    wrapped = lang_config.varname_wrap(result)
    file_regression.check(
        contents=wrapped + "\n",
        extension=lang_config.extension,
        fullpath=input_path.parent
        / (language + "_varname" + lang_config.extension),
    )


@pytest.mark.parametrize(
    argnames=("_case_name", "language", "input_path"),
    argvalues=_CASES,
    ids=[f"{c[0]}/{c[1]}" for c in _CASES],
)
def test_golden_file_combined_variable_forms(
    _case_name: str,
    language: str,
    input_path: Path,
    file_regression: FileRegressionFixture,
) -> None:
    """Test that literalize_yaml with new_variable=True (declaration) and
    new_variable=False (assignment to existing variable) produce expected
    golden output, combined in one file to show the difference in syntax.
    """
    lang_config = _LANGUAGES[language]
    yaml_string = input_path.read_text()
    declaration = literalizer.literalize_yaml(
        yaml_string=yaml_string,
        language=lang_config.spec,
        line_prefix="",
        wrap=True,
        variable_name=_VARIABLE_NAME,
        new_variable=True,
    )
    assignment = literalizer.literalize_yaml(
        yaml_string=yaml_string,
        language=lang_config.spec,
        line_prefix="",
        wrap=True,
        variable_name=_VARIABLE_NAME,
        new_variable=False,
    )
    combined = lang_config.combined_wrap(declaration, assignment)
    file_regression.check(
        contents=combined + "\n",
        extension=lang_config.extension,
        fullpath=input_path.parent
        / (language + "_combined" + lang_config.extension),
    )


_DATES_CASE_DIR = _CASES_DIR / "dates"


@pytest.mark.parametrize(
    argnames=("variant_name", "variant"),
    argvalues=list(_DATE_VARIANTS.items()),
    ids=list(_DATE_VARIANTS),
)
def test_date_format_golden_file(
    variant_name: str,
    variant: _DateVariant,
    file_regression: FileRegressionFixture,
) -> None:
    """Test native date format variants against golden files."""
    yaml_string = (_DATES_CASE_DIR / "input.yaml").read_text()
    result = literalizer.literalize_yaml(
        yaml_string=yaml_string,
        language=variant.spec,
        line_prefix="",
        wrap=True,
    )
    wrapped = variant.wrap(result)
    file_regression.check(
        contents=wrapped + "\n",
        extension=variant.extension,
        fullpath=_DATES_CASE_DIR / (variant_name + variant.extension),
    )


_SEQUENCE_CASE_DIR = _CASES_DIR / "simple_sequence"


@pytest.mark.parametrize(
    argnames=("variant_name", "variant"),
    argvalues=list(_SEQUENCE_VARIANTS.items()),
    ids=list(_SEQUENCE_VARIANTS),
)
def test_sequence_format_golden_file(
    variant_name: str,
    variant: _SequenceVariant,
    file_regression: FileRegressionFixture,
) -> None:
    """Test sequence type variants against golden files."""
    yaml_string = (_SEQUENCE_CASE_DIR / "input.yaml").read_text()
    result = literalizer.literalize_yaml(
        yaml_string=yaml_string,
        language=variant.spec,
        line_prefix="",
        wrap=True,
    )
    wrapped = variant.wrap(result)
    file_regression.check(
        contents=wrapped + "\n",
        extension=variant.extension,
        fullpath=_SEQUENCE_CASE_DIR / (variant_name + variant.extension),
    )


_SET_VARIANTS: dict[str, _SetVariant] = {
    "python_frozenset": _SetVariant(
        spec=literalizer.languages.Python(
            set_format=literalizer.languages.Python.SetFormat.FROZENSET,
        ),
        extension=".py",
        wrap=_wrap_identity,
    ),
}

_SET_CASE_DIR = _CASES_DIR / "set"


@pytest.mark.parametrize(
    argnames=("variant_name", "variant"),
    argvalues=list(_SET_VARIANTS.items()),
    ids=list(_SET_VARIANTS),
)
def test_set_format_golden_file(
    variant_name: str,
    variant: _SetVariant,
    file_regression: FileRegressionFixture,
) -> None:
    """Test set type variants against golden files."""
    yaml_string = (_SET_CASE_DIR / "input.yaml").read_text()
    result = literalizer.literalize_yaml(
        yaml_string=yaml_string,
        language=variant.spec,
        line_prefix="",
        wrap=True,
    )
    wrapped = variant.wrap(result)
    file_regression.check(
        contents=wrapped + "\n",
        extension=variant.extension,
        fullpath=_SET_CASE_DIR / (variant_name + variant.extension),
    )
