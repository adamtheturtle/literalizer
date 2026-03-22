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
import enum
from pathlib import Path
from typing import TYPE_CHECKING, Any

import pytest
from beartype import beartype
from pytest_regressions.file_regression import FileRegressionFixture

import literalizer
import literalizer.languages

if TYPE_CHECKING:
    from collections.abc import Callable

_CASES_REL = Path("tests") / "integration" / "cases"


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
def _go_time_import(content: str) -> str:
    """Return a Go time import block if the content uses time types."""
    if "time." in content:
        return '\nimport "time"'
    return ""


@beartype
def _wrap_go(content: str) -> str:
    """Wrap in a Go package-level variable declaration."""
    time_import = _go_time_import(content=content)
    return f"package main{time_import}\n\nvar _ = {content}"


@beartype
def _java_time_imports(content: str) -> str:
    """Return java.time import lines if the content uses java.time
    types.
    """
    types: list[str] = []
    if "Instant" in content:
        types.append("Instant")
    if "LocalDate" in content:
        types.append("LocalDate")
    return "".join(f"import java.time.{t};\n" for t in types)


@beartype
def _wrap_java(content: str) -> str:
    """Wrap in a Java class with necessary imports."""
    time_imports = _java_time_imports(content=content)
    return f"""\
{time_imports}import java.util.Map;
import java.util.Set;
class Check {{
    Object x = {content};
}}"""


@beartype
def _kotlin_time_imports(content: str) -> str:
    """Return Kotlin java.time import lines if needed."""
    imports = ""
    if "LocalDate" in content:
        imports += "import java.time.LocalDate\n"
    if "LocalDateTime" in content:
        imports += "import java.time.LocalDateTime\n"
    return imports


@beartype
def _wrap_kotlin(content: str) -> str:
    """Wrap in a Kotlin variable assignment."""
    time_imports = _kotlin_time_imports(content=content)
    return f"{time_imports}val x: Any? = {content}"


@beartype
def _wrap_kotlin_varname(content: str) -> str:
    """Wrap a Kotlin variable declaration with time imports if needed."""
    time_imports = _kotlin_time_imports(content=content)
    return f"{time_imports}{content}"


@beartype
def _wrap_cpp(content: str) -> str:
    """Wrap in a C++ struct and function for type-flexible
    initialization.
    """
    chrono = "#include <chrono>\n" if "std::chrono" in content else ""
    return (
        f"{chrono}"
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
    needs_system = "DateOnly" in content or "DateTime" in content
    system = "using System;\n" if needs_system else ""
    return f"""\
{system}using System.Collections.Generic;
var x = {content};"""


@beartype
def _rust_collections_use(content: str) -> str:
    """Return a use statement for std::collections types used in
    content.
    """
    names: list[str] = []
    if "HashMap" in content:
        names.append("HashMap")
    if "HashSet" in content:
        names.append("HashSet")
    if not names:
        return ""
    return f"use std::collections::{{{', '.join(names)}}};\n"


@beartype
def _rust_chrono_use(content: str) -> str:
    """Return a chrono use statement if the content uses chrono types."""
    names: list[str] = []
    if "NaiveDate" in content:
        names.append("NaiveDate")
    if "NaiveDateTime" in content:
        names.append("NaiveDateTime")
    if "NaiveTime" in content:
        names.append("NaiveTime")
    if not names:
        return ""
    return f"use chrono::{{{', '.join(names)}}};\n"


@beartype
def _wrap_rust(content: str) -> str:
    """Wrap in a Rust main function with necessary imports."""
    indented = content.replace("\n", "\n    ")
    return (
        _rust_collections_use(content=content)
        + _rust_chrono_use(content=content)
        + "fn main() {\n"
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
    fsharp = literalizer.languages.FSharp()
    typed = fsharp.format_sequence_entry(content)
    return (
        "module Check\n\n" + _FSHARP_VAL_TYPE + "\n" + f"let x: Val = {typed}"
    )


@beartype
def _wrap_ocaml(content: str) -> str:
    """Wrap in an OCaml module with a custom val_t variant type."""
    ocaml = literalizer.languages.OCaml()
    typed = ocaml.format_sequence_entry(content)
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
    time_import = _go_time_import(content=content)
    return (
        f"package main{time_import}\n\nfunc main() {{\n{content}\n"
        f"_ = {_VARIABLE_NAME}\n}}"
    )


@beartype
def _wrap_java_varname(content: str) -> str:
    """Wrap a Java var declaration in a static method."""
    time_imports = _java_time_imports(content=content)
    return (
        f"{time_imports}"
        "import java.util.Map;\n"
        "import java.util.Set;\n"
        "class Check {\n"
        "    public static void check() {\n"
        f"{content}\n"
        "    }\n"
        "}"
    )


@beartype
def _wrap_csharp_varname(content: str) -> str:
    """Wrap a C# top-level variable declaration with required imports."""
    needs_system = "DateOnly" in content or "DateTime" in content
    system = "using System;\n" if needs_system else ""
    return f"{system}using System.Collections.Generic;\n{content}"


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
    chrono = "#include <chrono>\n" if "std::chrono" in content else ""
    return (
        f"{chrono}"
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
def _wrap_norg(content: str) -> str:
    """Wrap in a Norg ranged verbatim tag."""
    return f"@code json\n{content}\n@end"


@beartype
def _wrap_d(content: str) -> str:
    """Wrap in a D function with ``std.json`` imported."""
    d_lang = literalizer.languages.D()
    typed = d_lang.format_sequence_entry(content)
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
    c_lang = literalizer.languages.C()
    typed = c_lang.format_sequence_entry(content)
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


_OBJC_PREAMBLE = (
    "typedef signed char BOOL;\n"
    "#define YES ((BOOL)1)\n"
    "#define NO ((BOOL)0)\n"
    "@interface NSObject\n"
    "+ (instancetype)alloc;\n"
    "- (instancetype)init;\n"
    "@end\n"
    "@interface NSString : NSObject\n"
    "@end\n"
    "@interface NSNumber : NSObject\n"
    "+ (instancetype)numberWithBool:(BOOL)value;\n"
    "+ (instancetype)numberWithChar:(signed char)value;\n"
    "+ (instancetype)numberWithInt:(int)value;\n"
    "+ (instancetype)numberWithUnsignedInt:(unsigned int)value;\n"
    "+ (instancetype)numberWithLong:(long)value;\n"
    "+ (instancetype)numberWithUnsignedLong:(unsigned long)value;\n"
    "+ (instancetype)numberWithLongLong:(long long)value;\n"
    "+ (instancetype)numberWithUnsignedLongLong:(unsigned long long)value;\n"
    "+ (instancetype)numberWithFloat:(float)value;\n"
    "+ (instancetype)numberWithDouble:(double)value;\n"
    "@end\n"
    "@interface NSArray : NSObject\n"
    "+ (instancetype)arrayWithObjects:(const id [])objects"
    " count:(unsigned long)cnt;\n"
    "@end\n"
    "@interface NSDictionary : NSObject\n"
    "+ (instancetype)dictionaryWithObjects:(const id [])objects"
    " forKeys:(const id [])keys count:(unsigned long)cnt;\n"
    "@end\n"
    "@interface NSNull : NSObject\n"
    "+ (instancetype)null;\n"
    "@end\n"
    "@interface NSSet : NSObject\n"
    "+ (instancetype)set;\n"
    "+ (instancetype)setWithArray:(NSArray *)array;\n"
    "@end\n"
)


@beartype
def _wrap_objc(content: str) -> str:
    """Wrap in an Objective-C function with Foundation import."""
    return (
        _OBJC_PREAMBLE
        + "void _check(void) {\n"
        + f"    id _v = {content};\n"
        + "    (void)_v;\n"
        + "}"
    )


@beartype
def _wrap_objc_varname(content: str) -> str:
    """Wrap an Objective-C variable declaration in a function."""
    return (
        _OBJC_PREAMBLE
        + "void _check(void) {\n"
        + f"{content}\n"
        + f"    (void){_VARIABLE_NAME};\n"
        + "}"
    )


@beartype
def _wrap_objc_combined(declaration: str, assignment: str) -> str:
    """Wrap Objective-C declaration and assignment in a function."""
    return (
        _OBJC_PREAMBLE
        + "void _check(void) {\n"
        + f"{declaration}\n"
        + f"{assignment}\n"
        + f"    (void){_VARIABLE_NAME};\n"
        + "}"
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
        _rust_collections_use(content=content)
        + _rust_chrono_use(content=content)
        + "fn main() {\n"
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
    zig = literalizer.languages.Zig()
    typed = zig.format_sequence_entry(content)
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
    combined = declaration + assignment
    time_imports = _kotlin_time_imports(content=combined)
    return (
        f"{time_imports}"
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
    combined = declaration + assignment
    return (
        _rust_collections_use(content=combined)
        + _rust_chrono_use(content=combined)
        + "fn main() {\n"
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
    fortran = literalizer.languages.Fortran()
    typed = fortran.format_sequence_entry(content)
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
def _python_imports(content: str) -> str:
    """Return import lines needed by the Python content."""
    imports: list[str] = []
    if "OrderedDict(" in content:
        imports.append("from collections import OrderedDict")
    if "[Any" in content or "Any]" in content:
        imports.append("from typing import Any")
    if "datetime." in content:
        imports.append("import datetime")
    if not imports:
        return ""
    return "\n".join(imports) + "\n"


@beartype
def _wrap_python(content: str) -> str:
    """Wrap with any imports needed by the generated Python code."""
    return _python_imports(content=content) + content


@beartype
def _wrap_python_combined(declaration: str, assignment: str) -> str:
    """Join declaration and assignment with imports prepended."""
    combined = declaration + "\n" + assignment
    return _python_imports(content=combined) + combined


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
def _wrap_ruby(content: str) -> str:
    """Wrap with require 'date' when Ruby Date literals are present."""
    prefix = "require 'date'\n" if "Date.new" in content else ""
    return f"{prefix}{content}"


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
def _wrap_julia(content: str) -> str:
    """Wrap with ``using Dates`` when Julia date literals are present."""
    needs_dates = "Date(" in content or "DateTime(" in content
    prefix = "using Dates\n" if needs_dates else ""
    return f"{prefix}{content}"


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
class _Variant:
    """A formatting variant for a language (date, sequence, set, etc.)."""

    spec: literalizer.Language
    extension: str
    wrap: Callable[[str], str]


@dataclasses.dataclass
class _LanguageConfig:
    """Language configuration with spec, file extension, and wrapper."""

    lang_cls: literalizer.HasFormatEnums
    spec: literalizer.Language
    extension: str
    wrap: Callable[[str], str]
    varname_wrap: Callable[[str], str]
    combined_wrap: Callable[[str, str], str]
    date_wrap: Callable[[str], str]
    set_wrap: Callable[[str], str]


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
    "ada": _LanguageConfig(
        lang_cls=literalizer.languages.Ada,
        spec=literalizer.languages.Ada(),
        extension=".adb",
        wrap=_wrap_ada,
        varname_wrap=_wrap_ada_varname,
        combined_wrap=_wrap_ada_combined,
        date_wrap=_wrap_identity,
        set_wrap=_wrap_identity,
    ),
    "bash": _LanguageConfig(
        lang_cls=literalizer.languages.Bash,
        spec=literalizer.languages.Bash(),
        extension=".sh",
        wrap=_wrap_bash,
        varname_wrap=_wrap_identity,
        combined_wrap=_wrap_combined_newline,
        date_wrap=_wrap_identity,
        set_wrap=_wrap_identity,
    ),
    "c": _LanguageConfig(
        lang_cls=literalizer.languages.C,
        spec=literalizer.languages.C(),
        extension=".c",
        wrap=_wrap_c,
        varname_wrap=_wrap_c_varname,
        combined_wrap=_wrap_c_combined,
        date_wrap=_wrap_identity,
        set_wrap=_wrap_identity,
    ),
    "cobol": _LanguageConfig(
        lang_cls=literalizer.languages.Cobol,
        spec=literalizer.languages.Cobol(),
        extension=".cob",
        wrap=_wrap_cobol,
        varname_wrap=_wrap_cobol_varname,
        combined_wrap=_wrap_cobol_combined,
        date_wrap=_wrap_identity,
        set_wrap=_wrap_identity,
    ),
    "d": _LanguageConfig(
        lang_cls=literalizer.languages.D,
        spec=literalizer.languages.D(),
        extension=".d",
        wrap=_wrap_d,
        varname_wrap=_wrap_d_varname,
        combined_wrap=_wrap_d_combined,
        date_wrap=_wrap_identity,
        set_wrap=_wrap_identity,
    ),
    "common_lisp": _LanguageConfig(
        lang_cls=literalizer.languages.CommonLisp,
        spec=literalizer.languages.CommonLisp(),
        extension=".lisp",
        wrap=_wrap_identity,
        varname_wrap=_wrap_identity,
        combined_wrap=_wrap_combined_newline,
        date_wrap=_wrap_identity,
        set_wrap=_wrap_identity,
    ),
    "clojure": _LanguageConfig(
        lang_cls=literalizer.languages.Clojure,
        spec=literalizer.languages.Clojure(),
        extension=".clj",
        wrap=_wrap_identity,
        varname_wrap=_wrap_identity,
        combined_wrap=_wrap_combined_newline,
        date_wrap=_wrap_identity,
        set_wrap=_wrap_identity,
    ),
    "python": _LanguageConfig(
        lang_cls=literalizer.languages.Python,
        spec=literalizer.languages.Python(),
        extension=".py",
        wrap=_wrap_python,
        varname_wrap=_wrap_python,
        combined_wrap=_wrap_python_combined,
        date_wrap=_wrap_python,
        set_wrap=_wrap_identity,
    ),
    "javascript": _LanguageConfig(
        lang_cls=literalizer.languages.JavaScript,
        spec=literalizer.languages.JavaScript(),
        extension=".js",
        wrap=_wrap_js,
        varname_wrap=_wrap_identity,
        combined_wrap=_wrap_js_combined,
        date_wrap=_wrap_js,
        set_wrap=_wrap_identity,
    ),
    "typescript": _LanguageConfig(
        lang_cls=literalizer.languages.TypeScript,
        spec=literalizer.languages.TypeScript(),
        extension=".ts",
        wrap=_wrap_js,
        varname_wrap=_wrap_ts_varname,
        combined_wrap=_wrap_ts_combined,
        date_wrap=_wrap_js,
        set_wrap=_wrap_identity,
    ),
    "kotlin": _LanguageConfig(
        lang_cls=literalizer.languages.Kotlin,
        spec=literalizer.languages.Kotlin(),
        extension=".kts",
        wrap=_wrap_kotlin,
        varname_wrap=_wrap_kotlin_varname,
        combined_wrap=_wrap_kotlin_combined,
        date_wrap=_wrap_identity,
        set_wrap=_wrap_identity,
    ),
    "ruby": _LanguageConfig(
        lang_cls=literalizer.languages.Ruby,
        spec=literalizer.languages.Ruby(),
        extension=".rb",
        wrap=_wrap_ruby,
        varname_wrap=_wrap_ruby,
        combined_wrap=lambda d, a: _wrap_ruby(content=d + "\n" + a),
        date_wrap=_wrap_identity,
        set_wrap=_wrap_identity,
    ),
    "go": _LanguageConfig(
        lang_cls=literalizer.languages.Go,
        spec=literalizer.languages.Go(),
        extension=".go",
        wrap=_wrap_go,
        varname_wrap=_wrap_go_varname,
        combined_wrap=lambda d, a: _wrap_go_varname(content=d + "\n" + a),
        date_wrap=_wrap_identity,
        set_wrap=_wrap_identity,
    ),
    "java": _LanguageConfig(
        lang_cls=literalizer.languages.Java,
        spec=literalizer.languages.Java(),
        extension=".java",
        wrap=_wrap_java,
        varname_wrap=_wrap_java_varname,
        combined_wrap=lambda d, a: _wrap_java_varname(content=d + "\n" + a),
        date_wrap=_wrap_java_time,
        set_wrap=_wrap_identity,
    ),
    "csharp": _LanguageConfig(
        lang_cls=literalizer.languages.CSharp,
        spec=literalizer.languages.CSharp(),
        extension=".cs",
        wrap=_wrap_csharp,
        varname_wrap=_wrap_csharp_varname,
        combined_wrap=lambda d, a: _wrap_csharp_varname(content=d + "\n" + a),
        date_wrap=_wrap_identity,
        set_wrap=_wrap_identity,
    ),
    "dart": _LanguageConfig(
        lang_cls=literalizer.languages.Dart,
        spec=literalizer.languages.Dart(),
        extension=".dart",
        wrap=_wrap_dart,
        varname_wrap=_wrap_identity,
        combined_wrap=_wrap_dart_combined,
        date_wrap=_wrap_dart,
        set_wrap=_wrap_identity,
    ),
    "swift": _LanguageConfig(
        lang_cls=literalizer.languages.Swift,
        spec=literalizer.languages.Swift(),
        extension=".swift",
        wrap=_wrap_swift,
        varname_wrap=_wrap_swift_varname,
        combined_wrap=_wrap_swift_combined,
        date_wrap=_wrap_identity,
        set_wrap=_wrap_identity,
    ),
    "cpp": _LanguageConfig(
        lang_cls=literalizer.languages.Cpp,
        spec=literalizer.languages.Cpp(),
        extension=".cpp",
        wrap=_wrap_cpp,
        varname_wrap=_wrap_cpp_varname,
        combined_wrap=lambda d, a: _wrap_cpp_varname(content=d + "\n" + a),
        date_wrap=_wrap_identity,
        set_wrap=_wrap_identity,
    ),
    "rust": _LanguageConfig(
        lang_cls=literalizer.languages.Rust,
        spec=literalizer.languages.Rust(),
        extension=".rs",
        wrap=_wrap_rust,
        varname_wrap=_wrap_rust_varname,
        combined_wrap=_wrap_rust_combined,
        date_wrap=_wrap_rust,
        set_wrap=_wrap_identity,
    ),
    "haskell": _LanguageConfig(
        lang_cls=literalizer.languages.Haskell,
        spec=literalizer.languages.Haskell(),
        extension=".hs",
        wrap=_wrap_haskell,
        varname_wrap=_wrap_haskell_varname,
        combined_wrap=lambda d, _a: _wrap_haskell_varname(content=d),
        date_wrap=_wrap_identity,
        set_wrap=_wrap_identity,
    ),
    "hcl": _LanguageConfig(
        lang_cls=literalizer.languages.Hcl,
        spec=literalizer.languages.Hcl(),
        extension=".hcl",
        wrap=_wrap_hcl,
        varname_wrap=_wrap_identity,
        combined_wrap=lambda d, _a: d,
        date_wrap=_wrap_identity,
        set_wrap=_wrap_identity,
    ),
    "julia": _LanguageConfig(
        lang_cls=literalizer.languages.Julia,
        spec=literalizer.languages.Julia(),
        extension=".jl",
        wrap=_wrap_julia,
        varname_wrap=_wrap_julia,
        combined_wrap=lambda d, a: _wrap_julia(content=d + "\n" + a),
        date_wrap=_wrap_identity,
        set_wrap=_wrap_identity,
    ),
    "lua": _LanguageConfig(
        lang_cls=literalizer.languages.Lua,
        spec=literalizer.languages.Lua(),
        extension=".lua",
        wrap=_wrap_lua,
        varname_wrap=_wrap_identity,
        combined_wrap=_wrap_combined_newline,
        date_wrap=_wrap_identity,
        set_wrap=_wrap_identity,
    ),
    "perl": _LanguageConfig(
        lang_cls=literalizer.languages.Perl,
        spec=literalizer.languages.Perl(),
        extension=".pl",
        wrap=_wrap_perl,
        varname_wrap=_wrap_identity,
        combined_wrap=_wrap_combined_newline,
        date_wrap=_wrap_identity,
        set_wrap=_wrap_identity,
    ),
    "php": _LanguageConfig(
        lang_cls=literalizer.languages.Php,
        spec=literalizer.languages.Php(),
        extension=".php",
        wrap=_wrap_php,
        varname_wrap=_wrap_php_varname,
        combined_wrap=lambda d, a: _wrap_php_varname(content=d + "\n" + a),
        date_wrap=_wrap_identity,
        set_wrap=_wrap_identity,
    ),
    "elixir": _LanguageConfig(
        lang_cls=literalizer.languages.Elixir,
        spec=literalizer.languages.Elixir(),
        extension=".ex",
        wrap=_wrap_elixir,
        varname_wrap=_wrap_elixir_varname,
        combined_wrap=lambda d, _a: _wrap_elixir_varname(content=d),
        date_wrap=_wrap_identity,
        set_wrap=_wrap_identity,
    ),
    "erlang": _LanguageConfig(
        lang_cls=literalizer.languages.Erlang,
        spec=literalizer.languages.Erlang(),
        extension=".erl",
        wrap=_wrap_erlang,
        varname_wrap=_wrap_erlang_varname,
        combined_wrap=lambda d, _a: _wrap_erlang_varname(content=d),
        date_wrap=_wrap_identity,
        set_wrap=_wrap_identity,
    ),
    "fsharp": _LanguageConfig(
        lang_cls=literalizer.languages.FSharp,
        spec=literalizer.languages.FSharp(),
        extension=".fs",
        wrap=_wrap_fsharp,
        varname_wrap=_wrap_fsharp_varname,
        combined_wrap=lambda d, _a: _wrap_fsharp_varname(content=d),
        date_wrap=_wrap_identity,
        set_wrap=_wrap_identity,
    ),
    "ocaml": _LanguageConfig(
        lang_cls=literalizer.languages.OCaml,
        spec=literalizer.languages.OCaml(),
        extension=".ml",
        wrap=_wrap_ocaml,
        varname_wrap=_wrap_ocaml_varname,
        combined_wrap=lambda d, _a: _wrap_ocaml_varname(content=d),
        date_wrap=_wrap_identity,
        set_wrap=_wrap_identity,
    ),
    "occam": _LanguageConfig(
        lang_cls=literalizer.languages.Occam,
        spec=literalizer.languages.Occam(),
        extension=".occ",
        wrap=_wrap_occam,
        varname_wrap=_wrap_occam_varname,
        combined_wrap=lambda d, _a: _wrap_occam_varname(content=d),
        date_wrap=_wrap_identity,
        set_wrap=_wrap_identity,
    ),
    "groovy": _LanguageConfig(
        lang_cls=literalizer.languages.Groovy,
        spec=literalizer.languages.Groovy(),
        extension=".groovy",
        wrap=_wrap_groovy,
        varname_wrap=_wrap_identity,
        combined_wrap=_wrap_combined_newline,
        date_wrap=_wrap_identity,
        set_wrap=_wrap_identity,
    ),
    "scala": _LanguageConfig(
        lang_cls=literalizer.languages.Scala,
        spec=literalizer.languages.Scala(),
        extension=".scala",
        wrap=_wrap_scala,
        varname_wrap=_wrap_scala_varname,
        combined_wrap=_wrap_scala_combined,
        date_wrap=_wrap_identity,
        set_wrap=_wrap_identity,
    ),
    "r": _LanguageConfig(
        lang_cls=literalizer.languages.R,
        spec=literalizer.languages.R(),
        extension=".R",
        wrap=_wrap_r,
        varname_wrap=_wrap_identity,
        combined_wrap=_wrap_combined_newline,
        date_wrap=_wrap_r,
        set_wrap=_wrap_identity,
    ),
    "racket": _LanguageConfig(
        lang_cls=literalizer.languages.Racket,
        spec=literalizer.languages.Racket(),
        extension=".rkt",
        wrap=_wrap_racket,
        varname_wrap=_wrap_racket,
        combined_wrap=_wrap_racket_combined,
        date_wrap=_wrap_identity,
        set_wrap=_wrap_identity,
    ),
    "crystal": _LanguageConfig(
        lang_cls=literalizer.languages.Crystal,
        spec=literalizer.languages.Crystal(),
        extension=".cr",
        wrap=_wrap_crystal,
        varname_wrap=_wrap_crystal_varname,
        combined_wrap=_wrap_crystal_combined,
        date_wrap=_wrap_identity,
        set_wrap=_wrap_identity,
    ),
    "matlab": _LanguageConfig(
        lang_cls=literalizer.languages.Matlab,
        spec=literalizer.languages.Matlab(),
        extension=".m",
        wrap=_wrap_matlab,
        varname_wrap=_wrap_identity,
        combined_wrap=_wrap_combined_newline,
        date_wrap=_wrap_identity,
        set_wrap=_wrap_identity,
    ),
    "mojo": _LanguageConfig(
        lang_cls=literalizer.languages.Mojo,
        spec=literalizer.languages.Mojo(),
        extension=".mojo",
        wrap=_wrap_mojo,
        varname_wrap=_wrap_mojo_varname,
        combined_wrap=_wrap_mojo_combined,
        date_wrap=_wrap_identity,
        set_wrap=_wrap_identity,
    ),
    "nim": _LanguageConfig(
        lang_cls=literalizer.languages.Nim,
        spec=literalizer.languages.Nim(),
        extension=".nim",
        wrap=_wrap_nim,
        varname_wrap=_wrap_nim_varname,
        combined_wrap=_wrap_nim_combined,
        date_wrap=_wrap_identity,
        set_wrap=_wrap_identity,
    ),
    "norg": _LanguageConfig(
        lang_cls=literalizer.languages.Norg,
        spec=literalizer.languages.Norg(),
        extension=".norg",
        wrap=_wrap_norg,
        varname_wrap=_wrap_identity,
        combined_wrap=lambda d, _a: d,
        date_wrap=_wrap_identity,
        set_wrap=_wrap_identity,
    ),
    "vb": _LanguageConfig(
        lang_cls=literalizer.languages.VisualBasic,
        spec=literalizer.languages.VisualBasic(),
        extension=".vb",
        wrap=_wrap_vb,
        varname_wrap=_wrap_vb_varname,
        combined_wrap=_wrap_vb_combined,
        date_wrap=_wrap_identity,
        set_wrap=_wrap_identity,
    ),
    "zig": _LanguageConfig(
        lang_cls=literalizer.languages.Zig,
        spec=literalizer.languages.Zig(),
        extension=".zig",
        wrap=_wrap_zig,
        varname_wrap=_wrap_zig_varname,
        combined_wrap=_wrap_zig_combined,
        date_wrap=_wrap_identity,
        set_wrap=_wrap_identity,
    ),
    "powershell": _LanguageConfig(
        lang_cls=literalizer.languages.PowerShell,
        spec=literalizer.languages.PowerShell(),
        extension=".ps1",
        wrap=_wrap_powershell,
        varname_wrap=_wrap_identity,
        combined_wrap=_wrap_combined_newline,
        date_wrap=_wrap_identity,
        set_wrap=_wrap_identity,
    ),
    "toml": _LanguageConfig(
        lang_cls=literalizer.languages.Toml,
        spec=literalizer.languages.Toml(),
        extension=".toml",
        wrap=_wrap_toml,
        varname_wrap=_wrap_identity,
        combined_wrap=lambda d, _a: d,
        date_wrap=_wrap_identity,
        set_wrap=_wrap_identity,
    ),
    "objective_c": _LanguageConfig(
        lang_cls=literalizer.languages.ObjectiveC,
        spec=literalizer.languages.ObjectiveC(),
        extension=".m",
        wrap=_wrap_objc,
        varname_wrap=_wrap_objc_varname,
        combined_wrap=_wrap_objc_combined,
        date_wrap=_wrap_identity,
        set_wrap=_wrap_identity,
    ),
    "fortran": _LanguageConfig(
        lang_cls=literalizer.languages.Fortran,
        spec=literalizer.languages.Fortran(),
        extension=".f90",
        wrap=_wrap_fortran,
        varname_wrap=_wrap_fortran_varname,
        combined_wrap=_wrap_fortran_combined,
        date_wrap=_wrap_identity,
        set_wrap=_wrap_identity,
    ),
    "yaml": _LanguageConfig(
        lang_cls=literalizer.languages.Yaml,
        spec=literalizer.languages.Yaml(),
        extension=".yaml",
        wrap=_wrap_identity,
        varname_wrap=_wrap_identity,
        combined_wrap=lambda d, _a: d,
        date_wrap=_wrap_identity,
        set_wrap=_wrap_identity,
    ),
}


@beartype
def _build_date_variants() -> dict[str, _Variant]:
    """Build datetime-format variants for all languages with multiple
    formats.

    For each language that has more than one datetime format, create a variant
    for every non-default format.
    """
    variants: dict[str, _Variant] = {}
    for lang_name, lang_config in _LANGUAGES.items():
        spec = lang_config.spec
        default_format: Any = spec.format_datetime
        for fmt in list(spec.datetime_formats):
            if fmt is default_format:
                continue
            variant_key = f"{lang_name}_{fmt.name.lower()}"
            variants[variant_key] = _Variant(
                spec=lang_config.lang_cls(datetime_format=fmt),
                extension=lang_config.extension,
                wrap=lang_config.date_wrap,
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
        spec = lang_config.spec
        default_format: Any = spec.sequence_format
        for fmt in list(spec.sequence_formats):
            if fmt is default_format:
                continue
            variant_key = f"{lang_name}_{fmt.name.lower()}"
            variants[variant_key] = _Variant(
                spec=lang_config.lang_cls(sequence_format=fmt),
                extension=lang_config.extension,
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
        spec = lang_config.spec
        default_config = spec.set_format_config
        for fmt in list(spec.set_formats):
            if fmt.value is default_config:
                continue
            variant_key = f"{lang_name}_{fmt.name.lower()}"
            variants[variant_key] = _Variant(
                spec=lang_config.lang_cls(set_format=fmt),
                extension=lang_config.extension,
                wrap=lang_config.set_wrap,
            )
    return variants


def _build_comment_variants() -> dict[str, _Variant]:
    """Build comment-format variants for all languages with multiple
    formats.

    For each language that has more than one comment format, create a variant
    for every non-default format.
    """
    variants: dict[str, _Variant] = {}
    for lang_name, lang_config in _LANGUAGES.items():
        spec = lang_config.spec
        default_config = spec.comment_config
        for fmt in list(spec.comment_formats):
            if fmt.value is default_config:
                continue
            variant_key = f"{lang_name}_{fmt.name.lower()}"
            variants[variant_key] = _Variant(
                spec=lang_config.lang_cls(comment_format=fmt),
                extension=lang_config.extension,
                wrap=lang_config.wrap,
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
    request: pytest.FixtureRequest,
    file_regression: FileRegressionFixture,
) -> None:
    """Test that literalize_yaml output matches expected golden file."""
    cases_dir = request.config.rootpath / _CASES_REL
    input_path = cases_dir / _case_name / "input.yaml"
    lang_config = _LANGUAGES[language]
    yaml_string = input_path.read_text()
    result = literalizer.literalize_yaml(
        yaml_string=yaml_string,
        language=lang_config.spec,
        line_prefix="",
        indent="    ",
        wrap=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    wrapped = lang_config.wrap(result)
    file_regression.check(
        contents=wrapped + "\n",
        extension=lang_config.extension,
        fullpath=input_path.parent / (language + lang_config.extension),
    )


@pytest.mark.parametrize(
    argnames=("_case_name", "language"),
    argvalues=_CASES,
    ids=[f"{c[0]}/{c[1]}" for c in _CASES],
)
def test_golden_file_with_variable_name(
    _case_name: str,
    language: str,
    request: pytest.FixtureRequest,
    file_regression: FileRegressionFixture,
) -> None:
    """Test that literalize_yaml with variable_name matches golden
    file.
    """
    cases_dir = request.config.rootpath / _CASES_REL
    input_path = cases_dir / _case_name / "input.yaml"
    lang_config = _LANGUAGES[language]
    yaml_string = input_path.read_text()
    result = literalizer.literalize_yaml(
        yaml_string=yaml_string,
        language=lang_config.spec,
        line_prefix="",
        indent="    ",
        wrap=True,
        variable_name=_VARIABLE_NAME,
        new_variable=True,
        error_on_coercion=False,
    )
    wrapped = lang_config.varname_wrap(result)
    file_regression.check(
        contents=wrapped + "\n",
        extension=lang_config.extension,
        fullpath=input_path.parent
        / (language + "_varname" + lang_config.extension),
    )


@pytest.mark.parametrize(
    argnames=("_case_name", "language"),
    argvalues=_CASES,
    ids=[f"{c[0]}/{c[1]}" for c in _CASES],
)
def test_golden_file_combined_variable_forms(
    _case_name: str,
    language: str,
    request: pytest.FixtureRequest,
    file_regression: FileRegressionFixture,
) -> None:
    """Test that literalize_yaml with new_variable=True (declaration) and
    new_variable=False (assignment to existing variable) produce expected
    golden output, combined in one file to show the difference in syntax.
    """
    cases_dir = request.config.rootpath / _CASES_REL
    input_path = cases_dir / _case_name / "input.yaml"
    lang_config = _LANGUAGES[language]
    yaml_string = input_path.read_text()
    declaration = literalizer.literalize_yaml(
        yaml_string=yaml_string,
        language=lang_config.spec,
        line_prefix="",
        indent="    ",
        wrap=True,
        variable_name=_VARIABLE_NAME,
        new_variable=True,
        error_on_coercion=False,
    )
    assignment = literalizer.literalize_yaml(
        yaml_string=yaml_string,
        language=lang_config.spec,
        line_prefix="",
        indent="    ",
        wrap=True,
        variable_name=_VARIABLE_NAME,
        new_variable=False,
        error_on_coercion=False,
    )
    combined = lang_config.combined_wrap(declaration, assignment)
    file_regression.check(
        contents=combined + "\n",
        extension=lang_config.extension,
        fullpath=input_path.parent
        / (language + "_combined" + lang_config.extension),
    )


@dataclasses.dataclass
class _VariantCase:
    """A format-variant golden-file test case."""

    variant_name: str
    variant: _Variant
    case_dir_name: str
    variable_name: str | None


@beartype
def _build_variant_cases() -> list[_VariantCase]:
    """Collect all format-variant golden-file test cases."""
    cases: list[_VariantCase] = []
    variant_sources: list[tuple[dict[str, _Variant], str]] = [
        (_build_date_variants(), "dates"),
        (_build_sequence_variants(), "simple_sequence"),
        (_build_set_variants(), "set"),
        (_build_comment_variants(), "comments"),
    ]
    for variants, case_dir_name in variant_sources:
        for variant_name, variant in variants.items():
            cases.append(
                _VariantCase(
                    variant_name=variant_name,
                    variant=variant,
                    case_dir_name=case_dir_name,
                    variable_name=None,
                )
            )
    variable_type_hints_variants: dict[str, _Variant] = {
        "python_inline": _Variant(
            spec=literalizer.languages.Python(
                variable_type_hints=literalizer.languages.Python.VariableTypeHints.INLINE,
            ),
            extension=".py",
            wrap=_wrap_python,
        ),
    }
    for variant_name, variant in variable_type_hints_variants.items():
        cases.append(
            _VariantCase(
                variant_name=variant_name,
                variant=variant,
                case_dir_name="simple_dict",
                variable_name=_VARIABLE_NAME,
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
    request: pytest.FixtureRequest,
    file_regression: FileRegressionFixture,
) -> None:
    """Test format-variant options (dates, sequences, sets, type hints)
    against golden files.
    """
    case_dir = (
        request.config.rootpath / _CASES_REL / variant_case.case_dir_name
    )
    variant = variant_case.variant
    yaml_string = (case_dir / "input.yaml").read_text()
    result = literalizer.literalize_yaml(
        yaml_string=yaml_string,
        language=variant.spec,
        line_prefix="",
        indent="    ",
        wrap=True,
        variable_name=variant_case.variable_name,
        new_variable=True,
        error_on_coercion=False,
    )
    wrapped = variant.wrap(result)
    file_regression.check(
        contents=wrapped + "\n",
        extension=variant.extension,
        fullpath=case_dir / (variant_case.variant_name + variant.extension),
    )


@pytest.mark.parametrize(
    argnames="lang_config",
    argvalues=_LANGUAGES.values(),
    ids=list(_LANGUAGES),
)
def test_format_enumeration_properties(lang_config: _LanguageConfig) -> None:
    """Every language exposes iterable format-enumeration properties."""
    spec = lang_config.spec
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
