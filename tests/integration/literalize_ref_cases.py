"""``literalize`` golden-file case configuration and runner for ``$ref``
support.

The configurations describe how each ``cases/literalize_ref_*`` directory is
driven through :func:`literalizer.literalize` with a ``ref_case`` set to the
language's default identifier case.  The runner
(``run_literalize_ref_golden_case``) is shared by
``test_literalize_ref_golden_file``.
"""

import dataclasses
import functools
import re
from pathlib import Path
from typing import cast

import pytest
from beartype import beartype
from pytest_regressions.file_regression import FileRegressionFixture
from ruamel.yaml import YAML as _YAML

import literalizer
from literalizer.exceptions import (
    CallArgNotSupportedError,
    HeterogeneousCollectionError,
)

from .case_discovery import (
    LITERALIZE_REF_CASE_CONFIGS,
    LiteralizeRefCaseConfig,
)
from .check_golden import check_golden
from .language_specs import sorted_languages, with_per_fixture_module_name
from .variant_cases import wrap_variable_form


@dataclasses.dataclass(frozen=True)
class LiteralizeRefCase:
    """A parameterized literalize-ref golden-file test case."""

    config: LiteralizeRefCaseConfig
    lang_cls: literalizer.LanguageCls


@functools.cache
@beartype
def discover_literalize_ref_cases() -> list[LiteralizeRefCase]:
    """Return literalize-ref test cases for all languages."""
    return [
        LiteralizeRefCase(config=config, lang_cls=lang_cls)
        for config in LITERALIZE_REF_CASE_CONFIGS
        for lang_cls in sorted_languages()
    ]


def _collect_ref_names(data: object) -> list[str]:
    """Recursively collect all ``$ref`` name values from parsed data."""
    match data:
        case dict():
            typed_data = cast("dict[object, object]", data)
            if len(typed_data) == 1 and "$ref" in typed_data:
                name = typed_data["$ref"]
                return [name] if isinstance(name, str) else []
            return [
                n
                for v in typed_data.values()
                for n in _collect_ref_names(data=v)
            ]
        case list():
            typed_list = cast("list[object]", data)
            return [
                n for item in typed_list for n in _collect_ref_names(data=item)
            ]
        case _:
            return []


_STUB_ASSIGN_LINE_RE = re.compile(pattern=r"^\w+\s*=(?!=)")
_NIX_STUB_IN_RE = re.compile(pattern=r"^(.*;\s+in)\s+\w+\s*$")


def _split_stub(stub_code: str) -> tuple[list[str], list[str]]:
    """Split a single Fortran-style stub into declaration and assignment
    lines.

    The split point is the first line (after stripping leading whitespace)
    that looks like ``identifier =``, indicating the start of an executable
    assignment.  Lines before that point are type declarations; from that
    point on are executable statements.

    The caller guarantees the stub contains at least one assignment line.
    """
    stub_lines = stub_code.split(sep="\n")
    split_idx = next(
        j
        for j, stub_line in enumerate(iterable=stub_lines)
        if _STUB_ASSIGN_LINE_RE.match(string=stub_line.lstrip())
    )
    return stub_lines[:split_idx], stub_lines[split_idx:]


def _split_stubs(
    stub_codes: list[str],
) -> tuple[list[str], list[str]]:
    """Aggregate declaration and assignment lines across multiple stubs.

    Each stub is split via :func:`_split_stub`.  The results are
    concatenated so all declaration lines precede all assignment lines.
    """
    decl_lines: list[str] = []
    assign_lines: list[str] = []
    for stub_code in stub_codes:
        stub_decl, stub_assign = _split_stub(stub_code=stub_code)
        decl_lines.extend(stub_decl)
        assign_lines.extend(stub_assign)
    return decl_lines, assign_lines


def _strip_nix_stub_in_expr(stub_code: str) -> str:
    """For Nix-style stubs ending in ``; in var_name``, strip ``var_name``.

    This transforms ``let var = {...}; in var`` into ``let var = {...}; in``
    so that when the stub is prepended before the next expression the result
    is valid nested Nix: ``let a = ...; in let b = ...; in b``.
    """
    lines = stub_code.split(sep="\n")
    for i in range(len(lines) - 1, -1, -1):
        m = _NIX_STUB_IN_RE.match(string=lines[i])
        if m:
            lines[i] = m.group(1)
            return "\n".join(lines)
    return stub_code


def _find_first_occurrence(lines: list[str], lower_name: str) -> int | None:
    """Return the index of the first line containing ``lower_name`` that
    is not immediately preceded by ``[``.
    """
    for i, line in enumerate(iterable=lines):
        idx = line.lower().find(lower_name)
        if idx == -1:
            continue
        if idx > 0 and line[idx - 1] == "[":
            continue
        return i
    return None


def _find_assignment_line(
    lines: list[str], lower_name: str, after_idx: int
) -> int:
    """Return the index of the first line at or after ``after_idx`` whose
    stripped content starts with ``lower_name`` followed by ``=``.

    This locates the main-variable assignment statement in Fortran-style
    code where the type declaration and assignment are on separate lines.
    The caller guarantees the assignment exists.
    """
    return next(
        i
        for i in range(after_idx, len(lines))
        if lines[i].lstrip().lower().startswith(lower_name)
        and _STUB_ASSIGN_LINE_RE.match(string=lines[i].lstrip().lower())
    )


def _stub_needs_global_split(stub_code: str, stub_var: str) -> bool:
    """Return True only when the stub uses Fortran-style two-phase layout.

    Fortran stubs have a type declaration line that does NOT start with
    the variable name, followed by an assignment line that does.  For
    annotation-style stubs (Roc, PureScript, Haskell, Elm, etc.) the
    annotation line starts with the variable name, so those stubs must
    be kept together as a unit.

    The detection works by finding the assignment line (first line
    starting with ``stub_var`` followed by ``=``), then checking whether
    any line before it also starts with ``stub_var``.  If a preceding
    line starts with ``stub_var``, the stub uses annotation style and
    must not be split globally.  If no assignment line exists at all
    (e.g. Nix ``let var = {...}``) the stub is also kept as a unit.
    """
    lower_var = stub_var.lower()
    stub_lines = stub_code.split(sep="\n")
    assign_idx: int | None = None
    for j, stub_line in enumerate(iterable=stub_lines):
        stripped = stub_line.lstrip().lower()
        if _STUB_ASSIGN_LINE_RE.match(string=stripped) and stripped.startswith(
            lower_var
        ):
            assign_idx = j
            break
    if assign_idx is None:
        return False
    return not any(
        stub_line.lstrip().lower().startswith(lower_var)
        for stub_line in stub_lines[:assign_idx]
    )


def inject_stubs_before_variable(
    code: str,
    variable_name: str,
    stub_entries: list[tuple[str, str]],
) -> str:
    """Insert stub declarations before ``variable_name`` using a
    case-insensitive match.

    Each entry in ``stub_entries`` is a ``(stub_var_name, stub_code)``
    pair.

    For annotation-style languages (Roc, PureScript, Haskell, Elm, etc.)
    each stub is injected as a complete unit immediately before
    ``variable_name`` so that annotations immediately precede their
    definitions.

    For Fortran-style stubs where the declaration and assignment must be
    separated, all stubs are split and injected in two phases:

    1. Declaration lines inserted before the first line that contains
       ``variable_name``.
    2. Assignment lines inserted before the first line whose stripped
       content starts with ``variable_name``.

    The case-insensitive search handles languages such as Erlang that
    capitalize variable names in output (e.g. ``my_data`` ->
    ``My_data``).  Matches where the variable name is immediately
    preceded by ``[`` are skipped to avoid false positives on
    module-declaration lines in Roc such as ``module [my_data]``.
    """
    if not stub_entries or not variable_name:
        return code

    lines = code.split(sep="\n")
    lower_name = variable_name.lower()

    decl_idx = _find_first_occurrence(lines=lines, lower_name=lower_name)
    if decl_idx is None:
        return code

    indent = len(lines[decl_idx]) - len(lines[decl_idx].lstrip())
    prefix = " " * indent

    def _indented(stub_line_list: list[str]) -> list[str]:
        """Apply the main variable's indentation prefix to stub lines."""
        return [prefix + sl if sl else "" for sl in stub_line_list]

    needs_global_split = any(
        _stub_needs_global_split(stub_code=stub_code, stub_var=stub_var)
        for stub_var, stub_code in stub_entries
    )

    stub_codes = [stub_code for _stub_var, stub_code in stub_entries]

    if needs_global_split:
        decl_stub_lines, assign_stub_lines = _split_stubs(
            stub_codes=stub_codes
        )
        assign_idx = _find_assignment_line(
            lines=lines, lower_name=lower_name, after_idx=decl_idx
        )

        result = list(lines)
        indented_decl = _indented(stub_line_list=decl_stub_lines)
        result = result[:decl_idx] + indented_decl + result[decl_idx:]
        adjusted_assign = assign_idx + len(decl_stub_lines)
        result = (
            result[:adjusted_assign]
            + _indented(stub_line_list=assign_stub_lines)
            + result[adjusted_assign:]
        )
        return "\n".join(result)

    all_stub_lines: list[str] = []
    for stub_code in stub_codes:
        processed = _strip_nix_stub_in_expr(stub_code=stub_code)
        all_stub_lines.extend(processed.split(sep="\n"))
    indented = _indented(stub_line_list=all_stub_lines)
    return "\n".join(lines[:decl_idx] + indented + lines[decl_idx:])


@beartype
def run_literalize_ref_golden_case(
    *,
    config: LiteralizeRefCaseConfig,
    lang_cls: literalizer.LanguageCls,
    spec: literalizer.Language,
    golden_name: str,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
) -> None:
    """Run a literalize ``$ref`` golden-file case against *golden_name*.

    Uses the language's first (default) identifier case so the ref
    identifier is spelled idiomatically for each language.  A stub
    declaration for each referenced identifier is injected before the
    first use so the golden file is a complete unit that can be compiled.
    """
    input_path = cases_dir / config.case_dir_name / "input.yaml"
    yaml_string = input_path.read_text()
    golden_path = input_path.parent / (golden_name + lang_cls.extension)
    spec = with_per_fixture_module_name(spec=spec, golden_path=golden_path)
    ref_case = spec.identifier_cases[0]
    try:
        result = literalizer.literalize(
            source=yaml_string,
            input_format=literalizer.InputFormat.YAML,
            language=spec,
            variable_form=wrap_variable_form(lang_cls=lang_cls),
            wrap_in_file=True,
            ref_case=ref_case,
        )
    except HeterogeneousCollectionError:
        golden_path.unlink(missing_ok=True)
        pytest.skip(
            f"{lang_cls.__name__} cannot represent this heterogeneous input",
        )
    except CallArgNotSupportedError as exc:
        golden_path.unlink(missing_ok=True)
        pytest.skip(
            f"{lang_cls.__name__} rejected ref identifier: {exc.reason}"
        )
    final_code = result.code
    if wrap_variable_form(lang_cls=lang_cls) is not None:
        ruamel_yaml = _YAML()
        raw_data: object = ruamel_yaml.load(  # pyright: ignore[reportUnknownMemberType]
            stream=yaml_string,
        )
        stub_entries: list[tuple[str, str]] = []
        for raw_name in _collect_ref_names(data=raw_data):
            converted_name = ref_case.convert(name=raw_name)
            stub = literalizer.literalize(
                source='{"_": "_"}',
                input_format=literalizer.InputFormat.JSON,
                language=spec,
                variable_form=literalizer.NewVariable(
                    name=converted_name,
                ),
                wrap_in_file=False,
            )
            stub_entries.append((converted_name, stub.declaration_code))
        variable_form_obj = wrap_variable_form(lang_cls=lang_cls)
        final_code = inject_stubs_before_variable(
            code=result.code,
            variable_name=variable_form_obj.name if variable_form_obj else "",
            stub_entries=stub_entries,
        )
    check_golden(
        file_regression=file_regression,
        contents=final_code + "\n",
        extension=lang_cls.extension,
        newline="",
        golden_path=golden_path,
    )
