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
from pytest_regressions.file_regression import FileRegressionFixture

import literalizer
import literalizer._formatters as literalizer_formatters
import literalizer.languages

if TYPE_CHECKING:
    import datetime
    from collections.abc import Callable

_CASES_DIR = Path(__file__).parent / "cases"


def _wrap_identity(content: str) -> str:
    """Return content unchanged."""
    return content


def _wrap_js(content: str) -> str:
    """Wrap in ``void(...)`` so bare object/array literals parse as
    expressions in JavaScript and TypeScript.
    """
    return f"void (\n{content}\n)"


def _wrap_go(content: str) -> str:
    """Wrap in a Go package-level variable declaration."""
    return f"package main\n\nvar _ = {content}"


def _wrap_java(content: str) -> str:
    """Wrap in a Java class with necessary imports."""
    return f"""\
import java.util.Map;
import java.util.Set;
class Check {{
    Object x = {content};
}}"""


def _wrap_kotlin(content: str) -> str:
    """Wrap in a Kotlin variable assignment."""
    return f"val x: Any? = {content}"


def _wrap_cpp(content: str) -> str:
    """Wrap in a C++ struct and function for type-flexible
    initialization.
    """
    return (
        "#include <initializer_list>\n"
        "#include <cstddef>\n"
        "struct _Any {\n"
        "    template<class T> _Any(T&&) noexcept {}\n"
        "    _Any(std::initializer_list<_Any>) noexcept {}\n"
        "};\n"
        "void _check() {\n"
        f"    [[maybe_unused]] _Any _v = {content};\n"
        "}"
    )


def _wrap_swift(content: str) -> str:
    """Wrap in a Swift variable assignment."""
    return f"let x: Any? = {content}"


def _wrap_csharp(content: str) -> str:
    """Wrap in C# using statement and variable assignment."""
    return f"""\
using System.Collections.Generic;
var x = {content};"""


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


def _wrap_fsharp(content: str) -> str:
    """Wrap in an F# module with a custom Val discriminated union."""
    return (
        "module Check\n"
        "\n" + _FSHARP_VAL_TYPE + "\n" + f"let x: Val = {content}"
    )


def _wrap_ocaml(content: str) -> str:
    """Wrap in an OCaml module with a custom val_t variant type."""
    return (
        "module Check = struct\n\n"
        + _OCAML_VAL_TYPE
        + "\n"
        + f"let x : val_t = {content}\n\n"
        + "end"
    )


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


def _wrap_occam(content: str) -> str:
    """Wrap in an occam-pi PROC with a custom ``LIT`` mobile data type."""
    return (
        _OCCAM_LIT_TYPE
        + "\n\n"
        + "PROC check ()\n"
        + f"  VAL MOBILE LIT x IS {content}:\n"
        + "  SEQ\n"
        + "    SKIP\n"
        + ":"
    )


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


def _wrap_fsharp_varname(content: str) -> str:
    """Wrap a F# ``let`` declaration with the Val type definition."""
    return "module Check\n\n" + _FSHARP_VAL_TYPE + "\n" + content


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


_VARIABLE_NAME = "my_data"


def _wrap_go_varname(content: str) -> str:
    """Wrap a Go short variable declaration in a main function."""
    return (
        f"package main\n\nfunc main() {{\n{content}\n_ = {_VARIABLE_NAME}\n}}"
    )


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


def _wrap_csharp_varname(content: str) -> str:
    """Wrap a C# top-level variable declaration with required imports."""
    return f"using System.Collections.Generic;\n{content}"


def _wrap_ts_varname(content: str) -> str:
    """Wrap a TypeScript variable declaration as a module.

    Adding ``export {}`` turns the file into a module so that ``const``
    declarations are module-scoped rather than global, preventing
    duplicate-declaration errors when ``tsc`` checks all ``.ts`` files
    together.
    """
    return f"{content}\nexport {{}};"


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
        "struct _Any {\n"
        "    template<class T> _Any(T&&) noexcept {}\n"
        "    _Any(std::initializer_list<_Any>) noexcept {}\n"
        "};\n"
        "void _check() {\n"
        f"{content_adapted}\n"
        "}"
    )


def _wrap_scala(content: str) -> str:
    """Wrap in a Scala object with a typed variable assignment."""
    return f"object Check {{\nval x: Any = {content}\n}}"


def _wrap_scala_varname(content: str) -> str:
    """Wrap a Scala variable declaration in an object."""
    return f"object Check {{\n{content}\n}}"


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


def _wrap_dart(content: str) -> str:
    """Wrap in a Dart final variable assignment."""
    return f"final x = {content};"


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


def _wrap_perl(content: str) -> str:
    """Wrap in a Perl variable assignment."""
    return f"my $x = {content};"


def _wrap_php(content: str) -> str:
    """Wrap in a PHP script variable assignment."""
    return f"<?php\n$x = {content};"


def _wrap_elixir(content: str) -> str:
    """Wrap in an Elixir module function."""
    return f"defmodule Check do\n  def x do\n    {content}\n  end\nend"


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


def _wrap_erlang(content: str) -> str:
    """Wrap in an Erlang module function."""
    return f"-module(check).\n-export([x/0]).\nx() ->\n    {content}."


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


def _wrap_groovy(content: str) -> str:
    """Wrap in a Groovy variable assignment."""
    return f"def x = {content}"


def _wrap_ada(content: str) -> str:
    """Wrap in an Ada procedure with a local variable assignment."""
    indented = content.replace("\n", "\n   ")
    return (
        "procedure Check is\n"
        f"   X : A_Val := {indented};\n"
        "begin\n"
        "   null;\n"
        "end Check;"
    )


def _wrap_ada_varname(content: str) -> str:
    """Wrap an Ada object declaration inside a procedure."""
    indented = "   " + content.replace("\n", "\n   ")
    return f"procedure Check is\n{indented}\nbegin\n   null;\nend Check;"


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


def _wrap_lua(content: str) -> str:
    """Wrap a Lua table constructor in a local variable assignment."""
    return f"local _ = {content}"


def _wrap_r(content: str) -> str:
    """Wrap in an R variable assignment."""
    return f"x <- {content}"


def _wrap_d(content: str) -> str:
    """Wrap in a D function with ``std.json`` imported."""
    return (
        f"import std.json;\n\nvoid _check() {{\n    auto _v = {content};\n}}"
    )


def _wrap_d_varname(content: str) -> str:
    """Wrap a D ``auto`` declaration in a function with ``std.json``
    imported.
    """
    return f"import std.json;\n\nvoid _check() {{\n{content}\n}}"


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


def _wrap_c(content: str) -> str:
    """Wrap in a C function with the _CVal/_CKV type definitions."""
    return (
        _C_PREAMBLE
        + "void _check(void) {\n"
        + f"    _CVal _v = {content};\n"
        + "    (void)_v;\n"
        + "}"
    )


def _wrap_c_varname(content: str) -> str:
    """Wrap a C _CVal declaration in a function with type definitions."""
    return (
        _C_PREAMBLE
        + "void _check(void) {\n"
        + f"{content}\n"
        + f"    (void){_VARIABLE_NAME};\n"
        + "}"
    )


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


def _wrap_php_varname(content: str) -> str:
    """Wrap a PHP variable assignment in a PHP script."""
    return f"<?php\n{content}"


def _wrap_swift_varname(content: str) -> str:
    """Add type annotation to Swift let declaration for mixed-type
    collections.

    The content from format_variable_declaration_swift is like
    "let my_data = [...]", and we need to add a type annotation for Swift
    to accept heterogeneous collections.
    """
    prefix = f"let {_VARIABLE_NAME}"
    return prefix + ": Any =" + content[len(prefix) + 2 :]


def _wrap_js_combined(declaration: str, assignment: str) -> str:
    """Wrap a JavaScript declaration in an IIFE to scope the variable,
    then assign to an outer var.
    """
    return (
        f"void (function() {{\n{declaration}\n}})();\n"
        f"var {_VARIABLE_NAME};\n"
        f"{assignment}"
    )


def _wrap_ts_combined(declaration: str, assignment: str) -> str:
    """TypeScript combined: same as JavaScript but as a module with export."""
    return (
        f"void (function() {{\n{declaration}\n}})();\n"
        f"var {_VARIABLE_NAME};\n"
        f"{assignment}\n"
        f"export {{}};"
    )


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


def _wrap_swift_combined(declaration: str, assignment: str) -> str:
    """Swift: let declaration (with type annotation) in a do block,
    then var + assignment in the outer scope.
    """
    annotated = _wrap_swift_varname(content=declaration)
    decl_indented = "    " + annotated.replace("\n", "\n    ")
    return (
        f"do {{\n{decl_indented}\n}}\nvar {_VARIABLE_NAME}: Any\n{assignment}"
    )


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


def _wrap_combined_newline(declaration: str, assignment: str) -> str:
    """Join declaration and assignment with a newline."""
    return declaration + "\n" + assignment


def _wrap_python_datetime(content: str) -> str:
    """Wrap with a datetime import for native Python date literals."""
    return f"import datetime\n{content}"


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


def _wrap_kotlin_time(content: str) -> str:
    """Wrap in a Kotlin variable assignment with java.time imports."""
    return (
        f"import java.time.LocalDate\n"
        f"import java.time.LocalDateTime\n"
        f"val x: Any? = {content}"
    )


def _wrap_go_time(content: str) -> str:
    """Wrap in a Go package with the time package imported."""
    return f'package main\n\nimport "time"\n\nvar _ = {content}'


def _wrap_cpp_chrono(content: str) -> str:
    """Wrap in C++ with the chrono header included."""
    return (
        "#include <chrono>\n"
        "#include <initializer_list>\n"
        "#include <cstddef>\n"
        "struct _Any {\n"
        "    template<class T> _Any(T&&) noexcept {}\n"
        "    _Any(std::initializer_list<_Any>) noexcept {}\n"
        "};\n"
        "void _check() {\n"
        f"    [[maybe_unused]] _Any _v = {content};\n"
        "}"
    )


def _wrap_csharp_date(content: str) -> str:
    """Wrap in C# with System and Collections.Generic namespaces."""
    return (
        f"using System;\nusing System.Collections.Generic;\nvar x = {content};"
    )


def _wrap_ruby_date(content: str) -> str:
    """Wrap with require 'date' for Ruby Date literals."""
    return f"require 'date'\n{content}"


def _wrap_crystal(content: str) -> str:
    """Wrap in a Crystal variable assignment to suppress unused-expression
    warnings.
    """
    return f"_ = {content}"


def _wrap_julia_dates(content: str) -> str:
    """Wrap with ``using Dates`` for native Julia date literals."""
    return f"using Dates\n{content}"


@dataclasses.dataclass
class _DateVariant:
    """A date/datetime formatting variant for a language."""

    name: str
    format_date: Callable[[datetime.date], str]
    format_datetime: Callable[[datetime.datetime], str]
    wrap: Callable[[str], str]


@dataclasses.dataclass
class _LanguageConfig:
    """Language configuration with spec, file extension, and wrapper."""

    spec: literalizer.Language
    extension: str
    wrap: Callable[[str], str]
    varname_wrap: Callable[[str], str]
    combined_wrap: Callable[[str, str], str]
    date_variants: tuple[_DateVariant, ...]


_LANGUAGES: dict[str, _LanguageConfig] = {
    "ada": _LanguageConfig(
        spec=literalizer.languages.ADA,
        extension=".adb",
        wrap=_wrap_ada,
        varname_wrap=_wrap_ada_varname,
        combined_wrap=_wrap_ada_combined,
        date_variants=(),
    ),
    "c": _LanguageConfig(
        spec=literalizer.languages.C,
        extension=".c",
        wrap=_wrap_c,
        varname_wrap=_wrap_c_varname,
        combined_wrap=_wrap_c_combined,
        date_variants=(),
    ),
    "d": _LanguageConfig(
        spec=literalizer.languages.D,
        extension=".d",
        wrap=_wrap_d,
        varname_wrap=_wrap_d_varname,
        combined_wrap=_wrap_d_combined,
        date_variants=(),
    ),
    "clojure": _LanguageConfig(
        spec=literalizer.languages.CLOJURE,
        extension=".clj",
        wrap=_wrap_identity,
        varname_wrap=_wrap_identity,
        combined_wrap=_wrap_combined_newline,
        date_variants=(),
    ),
    "python": _LanguageConfig(
        spec=literalizer.languages.PYTHON,
        extension=".py",
        wrap=_wrap_identity,
        varname_wrap=_wrap_identity,
        combined_wrap=_wrap_combined_newline,
        date_variants=(
            _DateVariant(
                name="python_native",
                format_date=literalizer_formatters.format_date_python,
                format_datetime=literalizer_formatters.format_datetime_python,
                wrap=_wrap_python_datetime,
            ),
            _DateVariant(
                name="python_epoch",
                format_date=literalizer_formatters.format_date_iso,
                format_datetime=literalizer_formatters.format_datetime_epoch,
                wrap=_wrap_identity,
            ),
        ),
    ),
    "javascript": _LanguageConfig(
        spec=literalizer.languages.JAVASCRIPT,
        extension=".js",
        wrap=_wrap_js,
        varname_wrap=_wrap_identity,
        combined_wrap=_wrap_js_combined,
        date_variants=(
            _DateVariant(
                name="js_native",
                format_date=literalizer_formatters.format_date_js,
                format_datetime=literalizer_formatters.format_datetime_js,
                wrap=_wrap_js,
            ),
        ),
    ),
    "typescript": _LanguageConfig(
        spec=literalizer.languages.TYPESCRIPT,
        extension=".ts",
        wrap=_wrap_js,
        varname_wrap=_wrap_ts_varname,
        combined_wrap=_wrap_ts_combined,
        date_variants=(
            _DateVariant(
                name="ts_native",
                format_date=literalizer_formatters.format_date_js,
                format_datetime=literalizer_formatters.format_datetime_js,
                wrap=_wrap_js,
            ),
        ),
    ),
    "kotlin": _LanguageConfig(
        spec=literalizer.languages.KOTLIN,
        extension=".kts",
        wrap=_wrap_kotlin,
        varname_wrap=_wrap_identity,
        combined_wrap=_wrap_kotlin_combined,
        date_variants=(
            _DateVariant(
                name="kotlin_native",
                format_date=literalizer_formatters.format_date_kotlin,
                format_datetime=literalizer_formatters.format_datetime_kotlin,
                wrap=_wrap_kotlin_time,
            ),
        ),
    ),
    "ruby": _LanguageConfig(
        spec=literalizer.languages.RUBY,
        extension=".rb",
        wrap=_wrap_identity,
        varname_wrap=_wrap_identity,
        combined_wrap=_wrap_combined_newline,
        date_variants=(
            _DateVariant(
                name="ruby_native",
                format_date=literalizer_formatters.format_date_ruby,
                format_datetime=literalizer_formatters.format_datetime_ruby,
                wrap=_wrap_ruby_date,
            ),
        ),
    ),
    "go": _LanguageConfig(
        spec=literalizer.languages.GO,
        extension=".go",
        wrap=_wrap_go,
        varname_wrap=_wrap_go_varname,
        combined_wrap=lambda d, a: _wrap_go_varname(content=d + "\n" + a),
        date_variants=(
            _DateVariant(
                name="go_native",
                format_date=literalizer_formatters.format_date_go,
                format_datetime=literalizer_formatters.format_datetime_go,
                wrap=_wrap_go_time,
            ),
        ),
    ),
    "java": _LanguageConfig(
        spec=literalizer.languages.JAVA,
        extension=".java",
        wrap=_wrap_java,
        varname_wrap=_wrap_java_varname,
        combined_wrap=lambda d, a: _wrap_java_varname(content=d + "\n" + a),
        date_variants=(
            _DateVariant(
                name="java_instant",
                format_date=literalizer_formatters.format_date_java,
                format_datetime=literalizer_formatters.format_datetime_java_instant,
                wrap=_wrap_java_time,
            ),
            _DateVariant(
                name="java_zoned",
                format_date=literalizer_formatters.format_date_java,
                format_datetime=literalizer_formatters.format_datetime_java_zoned,
                wrap=_wrap_java_time,
            ),
        ),
    ),
    "csharp": _LanguageConfig(
        spec=literalizer.languages.CSHARP,
        extension=".cs",
        wrap=_wrap_csharp,
        varname_wrap=_wrap_csharp_varname,
        combined_wrap=lambda d, a: _wrap_csharp_varname(content=d + "\n" + a),
        date_variants=(
            _DateVariant(
                name="csharp_native",
                format_date=literalizer_formatters.format_date_csharp,
                format_datetime=literalizer_formatters.format_datetime_csharp,
                wrap=_wrap_csharp_date,
            ),
        ),
    ),
    "dart": _LanguageConfig(
        spec=literalizer.languages.DART,
        extension=".dart",
        wrap=_wrap_dart,
        varname_wrap=_wrap_identity,
        combined_wrap=_wrap_dart_combined,
        date_variants=(
            _DateVariant(
                name="dart_native",
                format_date=literalizer_formatters.format_date_dart,
                format_datetime=literalizer_formatters.format_datetime_dart,
                wrap=_wrap_dart,
            ),
        ),
    ),
    "swift": _LanguageConfig(
        spec=literalizer.languages.SWIFT,
        extension=".swift",
        wrap=_wrap_swift,
        varname_wrap=_wrap_swift_varname,
        combined_wrap=_wrap_swift_combined,
        date_variants=(),
    ),
    "cpp": _LanguageConfig(
        spec=literalizer.languages.CPP,
        extension=".cpp",
        wrap=_wrap_cpp,
        varname_wrap=_wrap_cpp_varname,
        combined_wrap=lambda d, a: _wrap_cpp_varname(content=d + "\n" + a),
        date_variants=(
            _DateVariant(
                name="cpp_native",
                format_date=literalizer_formatters.format_date_cpp,
                format_datetime=literalizer_formatters.format_datetime_cpp,
                wrap=_wrap_cpp_chrono,
            ),
        ),
    ),
    "rust": _LanguageConfig(
        spec=literalizer.languages.RUST,
        extension=".rs",
        wrap=_wrap_rust,
        varname_wrap=_wrap_rust_varname,
        combined_wrap=_wrap_rust_combined,
        date_variants=(
            _DateVariant(
                name="rust_native",
                format_date=literalizer_formatters.format_date_rust,
                format_datetime=literalizer_formatters.format_datetime_rust,
                wrap=_wrap_rust_chrono,
            ),
        ),
    ),
    "haskell": _LanguageConfig(
        spec=literalizer.languages.HASKELL,
        extension=".hs",
        wrap=_wrap_haskell,
        varname_wrap=_wrap_haskell_varname,
        combined_wrap=lambda d, _a: _wrap_haskell_varname(content=d),
        date_variants=(),
    ),
    "julia": _LanguageConfig(
        spec=literalizer.languages.JULIA,
        extension=".jl",
        wrap=_wrap_identity,
        varname_wrap=_wrap_identity,
        combined_wrap=_wrap_combined_newline,
        date_variants=(
            _DateVariant(
                name="julia_native",
                format_date=literalizer_formatters.format_date_julia,
                format_datetime=literalizer_formatters.format_datetime_julia,
                wrap=_wrap_julia_dates,
            ),
        ),
    ),
    "lua": _LanguageConfig(
        spec=literalizer.languages.LUA,
        extension=".lua",
        wrap=_wrap_lua,
        varname_wrap=_wrap_identity,
        combined_wrap=_wrap_combined_newline,
        date_variants=(),
    ),
    "perl": _LanguageConfig(
        spec=literalizer.languages.PERL,
        extension=".pl",
        wrap=_wrap_perl,
        varname_wrap=_wrap_identity,
        combined_wrap=_wrap_combined_newline,
        date_variants=(),
    ),
    "php": _LanguageConfig(
        spec=literalizer.languages.PHP,
        extension=".php",
        wrap=_wrap_php,
        varname_wrap=_wrap_php_varname,
        combined_wrap=lambda d, a: _wrap_php_varname(content=d + "\n" + a),
        date_variants=(),
    ),
    "elixir": _LanguageConfig(
        spec=literalizer.languages.ELIXIR,
        extension=".ex",
        wrap=_wrap_elixir,
        varname_wrap=_wrap_elixir_varname,
        combined_wrap=lambda d, _a: _wrap_elixir_varname(content=d),
        date_variants=(),
    ),
    "erlang": _LanguageConfig(
        spec=literalizer.languages.ERLANG,
        extension=".erl",
        wrap=_wrap_erlang,
        varname_wrap=_wrap_erlang_varname,
        combined_wrap=lambda d, _a: _wrap_erlang_varname(content=d),
        date_variants=(),
    ),
    "fsharp": _LanguageConfig(
        spec=literalizer.languages.FSHARP,
        extension=".fs",
        wrap=_wrap_fsharp,
        varname_wrap=_wrap_fsharp_varname,
        combined_wrap=lambda d, _a: _wrap_fsharp_varname(content=d),
        date_variants=(),
    ),
    "ocaml": _LanguageConfig(
        spec=literalizer.languages.OCAML,
        extension=".ml",
        wrap=_wrap_ocaml,
        varname_wrap=_wrap_ocaml_varname,
        combined_wrap=lambda d, _a: _wrap_ocaml_varname(content=d),
        date_variants=(),
    ),
    "occam": _LanguageConfig(
        spec=literalizer.languages.OCCAM,
        extension=".occ",
        wrap=_wrap_occam,
        varname_wrap=_wrap_occam_varname,
        combined_wrap=lambda d, _a: _wrap_occam_varname(content=d),
        date_variants=(),
    ),
    "groovy": _LanguageConfig(
        spec=literalizer.languages.GROOVY,
        extension=".groovy",
        wrap=_wrap_groovy,
        varname_wrap=_wrap_identity,
        combined_wrap=_wrap_combined_newline,
        date_variants=(),
    ),
    "scala": _LanguageConfig(
        spec=literalizer.languages.SCALA,
        extension=".scala",
        wrap=_wrap_scala,
        varname_wrap=_wrap_scala_varname,
        combined_wrap=_wrap_scala_combined,
        date_variants=(),
    ),
    "r": _LanguageConfig(
        spec=literalizer.languages.R,
        extension=".R",
        wrap=_wrap_r,
        varname_wrap=_wrap_identity,
        combined_wrap=_wrap_combined_newline,
        date_variants=(
            _DateVariant(
                name="r_native",
                format_date=literalizer_formatters.format_date_r,
                format_datetime=literalizer_formatters.format_datetime_r,
                wrap=_wrap_r,
            ),
        ),
    ),
    "crystal": _LanguageConfig(
        spec=literalizer.languages.CRYSTAL,
        extension=".cr",
        wrap=_wrap_crystal,
        varname_wrap=_wrap_identity,
        combined_wrap=_wrap_combined_newline,
        date_variants=(),
    ),
}


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


def _discover_varname_cases() -> list[tuple[str, str, Path]]:
    """Return ``(case_name, language, input_path)`` tuples for variable-
    name
    tests.
    """
    cases: list[tuple[str, str, Path]] = []
    for case_dir in sorted(_CASES_DIR.iterdir()):
        cases.extend(
            (case_dir.name, lang_name, case_dir / "input.yaml")
            for lang_name in _LANGUAGES
        )
    return cases


_VARNAME_CASES = _discover_varname_cases()


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
        prefix="",
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
    argvalues=_VARNAME_CASES,
    ids=[f"{c[0]}/{c[1]}" for c in _VARNAME_CASES],
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
        prefix="",
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
        prefix="",
        wrap=True,
        variable_name=_VARIABLE_NAME,
        new_variable=True,
    )
    assignment = literalizer.literalize_yaml(
        yaml_string=yaml_string,
        language=lang_config.spec,
        prefix="",
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

_DATE_VARIANT_CASES: list[tuple[str, _LanguageConfig, _DateVariant]] = [
    (variant.name, lang_config, variant)
    for lang_config in _LANGUAGES.values()
    for variant in lang_config.date_variants
]


@pytest.mark.parametrize(
    argnames=("variant_name", "lang_config", "variant"),
    argvalues=_DATE_VARIANT_CASES,
    ids=[c[0] for c in _DATE_VARIANT_CASES],
)
def test_date_format_golden_file(
    variant_name: str,
    lang_config: _LanguageConfig,
    variant: _DateVariant,
    file_regression: FileRegressionFixture,
) -> None:
    """Test native date format variants against golden files."""
    spec = dataclasses.replace(
        lang_config.spec,
        format_date=variant.format_date,
        format_datetime=variant.format_datetime,
    )
    yaml_string = (_DATES_CASE_DIR / "input.yaml").read_text()
    result = literalizer.literalize_yaml(
        yaml_string=yaml_string,
        language=spec,
        prefix="",
        wrap=True,
    )
    wrapped = variant.wrap(result)
    file_regression.check(
        contents=wrapped + "\n",
        extension=lang_config.extension,
        fullpath=_DATES_CASE_DIR / (variant_name + lang_config.extension),
    )
