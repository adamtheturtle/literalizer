"""Integration tests that compare literalize_yaml output against golden
files.

Each subdirectory contains an ``input.yaml`` and one expected-output file
per supported language, using the real file extension for that language.

Golden files contain syntactically valid programs so that pre-commit hooks
can syntax-check them directly without additional wrapping.
"""

from __future__ import annotations

import dataclasses
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from pytest_regressions.file_regression import FileRegressionFixture

import literalizer
import literalizer.formatters
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


def _wrap_php(content: str) -> str:
    """Wrap in a PHP script variable assignment."""
    return f"<?php\n$x = {content};"


def _wrap_r(content: str) -> str:
    """Wrap in an R variable assignment."""
    return f"x <- {content}"


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

    spec: literalizer.LanguageSpec
    extension: str
    wrap: Callable[[str], str]
    date_variants: tuple[_DateVariant, ...]


_LANGUAGES: dict[str, _LanguageConfig] = {
    "python": _LanguageConfig(
        spec=literalizer.languages.PYTHON,
        extension=".py",
        wrap=_wrap_identity,
        date_variants=(
            _DateVariant(
                name="python_native",
                format_date=literalizer.formatters.format_date_python,
                format_datetime=literalizer.formatters.format_datetime_python,
                wrap=_wrap_python_datetime,
            ),
            _DateVariant(
                name="python_epoch",
                format_date=literalizer.formatters.format_date_iso,
                format_datetime=literalizer.formatters.format_datetime_epoch,
                wrap=_wrap_identity,
            ),
        ),
    ),
    "javascript": _LanguageConfig(
        spec=literalizer.languages.JAVASCRIPT,
        extension=".js",
        wrap=_wrap_js,
        date_variants=(
            _DateVariant(
                name="js_native",
                format_date=literalizer.formatters.format_date_js,
                format_datetime=literalizer.formatters.format_datetime_js,
                wrap=_wrap_js,
            ),
        ),
    ),
    "typescript": _LanguageConfig(
        spec=literalizer.languages.TYPESCRIPT,
        extension=".ts",
        wrap=_wrap_js,
        date_variants=(
            _DateVariant(
                name="ts_native",
                format_date=literalizer.formatters.format_date_js,
                format_datetime=literalizer.formatters.format_datetime_js,
                wrap=_wrap_js,
            ),
        ),
    ),
    "kotlin": _LanguageConfig(
        spec=literalizer.languages.KOTLIN,
        extension=".kts",
        wrap=_wrap_kotlin,
        date_variants=(
            _DateVariant(
                name="kotlin_native",
                format_date=literalizer.formatters.format_date_kotlin,
                format_datetime=literalizer.formatters.format_datetime_kotlin,
                wrap=_wrap_kotlin_time,
            ),
        ),
    ),
    "ruby": _LanguageConfig(
        spec=literalizer.languages.RUBY,
        extension=".rb",
        wrap=_wrap_identity,
        date_variants=(
            _DateVariant(
                name="ruby_native",
                format_date=literalizer.formatters.format_date_ruby,
                format_datetime=literalizer.formatters.format_datetime_ruby,
                wrap=_wrap_ruby_date,
            ),
        ),
    ),
    "go": _LanguageConfig(
        spec=literalizer.languages.GO,
        extension=".go",
        wrap=_wrap_go,
        date_variants=(
            _DateVariant(
                name="go_native",
                format_date=literalizer.formatters.format_date_go,
                format_datetime=literalizer.formatters.format_datetime_go,
                wrap=_wrap_go_time,
            ),
        ),
    ),
    "java": _LanguageConfig(
        spec=literalizer.languages.JAVA,
        extension=".java",
        wrap=_wrap_java,
        date_variants=(
            _DateVariant(
                name="java_instant",
                format_date=literalizer.formatters.format_date_java,
                format_datetime=literalizer.formatters.format_datetime_java_instant,
                wrap=_wrap_java_time,
            ),
            _DateVariant(
                name="java_zoned",
                format_date=literalizer.formatters.format_date_java,
                format_datetime=literalizer.formatters.format_datetime_java_zoned,
                wrap=_wrap_java_time,
            ),
        ),
    ),
    "csharp": _LanguageConfig(
        spec=literalizer.languages.CSHARP,
        extension=".cs",
        wrap=_wrap_csharp,
        date_variants=(
            _DateVariant(
                name="csharp_native",
                format_date=literalizer.formatters.format_date_csharp,
                format_datetime=literalizer.formatters.format_datetime_csharp,
                wrap=_wrap_csharp_date,
            ),
        ),
    ),
    "swift": _LanguageConfig(
        spec=literalizer.languages.SWIFT,
        extension=".swift",
        wrap=_wrap_swift,
        date_variants=(),
    ),
    "cpp": _LanguageConfig(
        spec=literalizer.languages.CPP,
        extension=".cpp",
        wrap=_wrap_cpp,
        date_variants=(
            _DateVariant(
                name="cpp_native",
                format_date=literalizer.formatters.format_date_cpp,
                format_datetime=literalizer.formatters.format_datetime_cpp,
                wrap=_wrap_cpp_chrono,
            ),
        ),
    ),
    "rust": _LanguageConfig(
        spec=literalizer.languages.RUST,
        extension=".rs",
        wrap=_wrap_rust,
        date_variants=(
            _DateVariant(
                name="rust_native",
                format_date=literalizer.formatters.format_date_rust,
                format_datetime=literalizer.formatters.format_datetime_rust,
                wrap=_wrap_rust_chrono,
            ),
        ),
    ),
    "haskell": _LanguageConfig(
        spec=literalizer.languages.HASKELL,
        extension=".hs",
        wrap=_wrap_haskell,
        date_variants=(),
    ),
    "julia": _LanguageConfig(
        spec=literalizer.languages.JULIA,
        extension=".jl",
        wrap=_wrap_identity,
        date_variants=(
            _DateVariant(
                name="julia_native",
                format_date=literalizer.formatters.format_date_julia,
                format_datetime=literalizer.formatters.format_datetime_julia,
                wrap=_wrap_julia_dates,
            ),
        ),
    ),
    "php": _LanguageConfig(
        spec=literalizer.languages.PHP,
        extension=".php",
        wrap=_wrap_php,
        date_variants=(),
    ),
    "r": _LanguageConfig(
        spec=literalizer.languages.R,
        extension=".R",
        wrap=_wrap_r,
        date_variants=(
            _DateVariant(
                name="r_native",
                format_date=literalizer.formatters.format_date_r,
                format_datetime=literalizer.formatters.format_datetime_r,
                wrap=_wrap_r,
            ),
        ),
    ),
}


_LANGUAGES_WITH_VARNAME: dict[str, _LanguageConfig] = {
    "python": _LanguageConfig(
        spec=literalizer.languages.PYTHON,
        extension=".py",
        wrap=_wrap_identity,
        date_variants=(),
    ),
    "javascript": _LanguageConfig(
        spec=literalizer.languages.JAVASCRIPT,
        extension=".js",
        wrap=_wrap_identity,
        date_variants=(),
    ),
    "typescript": _LanguageConfig(
        spec=literalizer.languages.TYPESCRIPT,
        extension=".ts",
        wrap=_wrap_ts_varname,
        date_variants=(),
    ),
    "kotlin": _LanguageConfig(
        spec=literalizer.languages.KOTLIN,
        extension=".kts",
        wrap=_wrap_identity,
        date_variants=(),
    ),
    "ruby": _LanguageConfig(
        spec=literalizer.languages.RUBY,
        extension=".rb",
        wrap=_wrap_identity,
        date_variants=(),
    ),
    "go": _LanguageConfig(
        spec=literalizer.languages.GO,
        extension=".go",
        wrap=_wrap_go_varname,
        date_variants=(),
    ),
    "java": _LanguageConfig(
        spec=literalizer.languages.JAVA,
        extension=".java",
        wrap=_wrap_java_varname,
        date_variants=(),
    ),
    "csharp": _LanguageConfig(
        spec=literalizer.languages.CSHARP,
        extension=".cs",
        wrap=_wrap_csharp_varname,
        date_variants=(),
    ),
    "cpp": _LanguageConfig(
        spec=literalizer.languages.CPP,
        extension=".cpp",
        wrap=_wrap_cpp_varname,
        date_variants=(),
    ),
    "julia": _LanguageConfig(
        spec=literalizer.languages.JULIA,
        extension=".jl",
        wrap=_wrap_identity,
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
            for lang_name in _LANGUAGES_WITH_VARNAME
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
    lang_config = _LANGUAGES_WITH_VARNAME[language]
    yaml_string = input_path.read_text()
    result = literalizer.literalize_yaml(
        yaml_string=yaml_string,
        language=lang_config.spec,
        prefix="",
        wrap=True,
        variable_name=_VARIABLE_NAME,
    )
    wrapped = lang_config.wrap(result)
    file_regression.check(
        contents=wrapped + "\n",
        extension=lang_config.extension,
        fullpath=input_path.parent
        / (language + "_varname" + lang_config.extension),
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
