"""``literalize_call`` golden-file case configuration and runner.

The configurations describe how each ``cases/call_*`` directory is
driven through :func:`literalizer.literalize_call`.  The runner
(``run_call_golden_case``) is shared by ``test_call_golden_file`` and
``test_call_variant_golden_file``.
"""

import dataclasses
import functools
from collections.abc import Callable, Iterable
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from beartype import beartype
from pytest_regressions.file_regression import FileRegressionFixture

import literalizer
from literalizer._language import StubReturn
from literalizer.exceptions import (
    CallArgNotSupportedError,
    HeterogeneousCollectionError,
)
from literalizer.languages import (
    Ada,
    Cobol,
    Dhall,
    Elm,
    Erlang,
    Fortran,
    Gleam,
    Haskell,
    Hcl,
    Jsonnet,
    Mojo,
    ObjectiveC,
    OCaml,
    Php,
    PowerShell,
    PureScript,
    Raku,
    Roc,
    Sml,
    SystemVerilog,
    Wren,
)

from .check_golden import check_golden
from .language_specs import sorted_languages, with_per_fixture_module_name

if TYPE_CHECKING:
    from literalizer._types import Value


@beartype
def _prepend_preamble(
    wrapped: str,
    preamble: tuple[str, ...],
) -> str:
    """Prepend *preamble* lines before *wrapped*."""
    if not preamble:
        return wrapped
    return "\n".join(preamble) + "\n" + wrapped


@beartype
def _dedupe_preamble_blocks(*, blocks: Iterable[str]) -> tuple[str, ...]:
    """Return preamble *blocks* with duplicate headers removed.

    Some languages emit multi-line preamble blocks whose first line is a
    stable header (for example, ``pub type GVal {`` in Gleam). When the
    call-test harness combines declaration preambles with call
    preambles, the same header can appear multiple times with identical
    bodies. Keep the first block per header.
    """
    seen: set[str] = set()
    result: list[str] = []
    for block in blocks:
        header = block.splitlines()[0] if block else ""
        if header in seen:
            continue
        seen.add(header)
        result.append(block)
    return tuple(result)


@dataclasses.dataclass(frozen=True)
class CallCaseConfig:
    """Configuration for a ``literalize_call`` golden-file test case.

    When *ref_declarations* is non-empty, each entry maps a
    ``{"$ref": "name"}`` marker in ``input.yaml`` to a JSON source
    string that is rendered as a variable declaration via
    :func:`literalizer.literalize`.  The declarations are emitted
    before the call so the resulting file is self-contained.  Only
    meaningful when at least one call argument in ``input.yaml`` uses
    the ``{"$ref": "name"}`` marker.

    When *ref_case_per_language* is ``True``, the harness picks each
    language's first-listed ``IdentifierCases`` member as the
    ``ref_case`` for that language, converts each
    *ref_declarations* key to that case, and passes the same case
    through to :func:`literalize_call` so the declaration site and
    the call site agree on identifier spelling.
    """

    case_dir_name: str
    target_function: str
    parameter_names: list[str]
    call_transform: Callable[[str], str] | None
    transform_stub_names: list[str]
    per_element: bool
    call_style_type: type[literalizer.CallStyle] | None
    ref_declarations: dict[str, str]
    # When True, drive ``literalize_call(..., wrap_in_file=True)``
    # directly instead of wrapping manually with injected stubs.
    wrap_in_file: bool
    ref_case_per_language: bool


CALL_STYLE_VARIANTS: list[tuple[str, type[literalizer.CallStyle]]] = [
    ("keyword", literalizer.KeywordCallStyle),
    ("positional", literalizer.PositionalCallStyle),
    ("object", literalizer.ObjectCallStyle),
]


CALL_CASE_CONFIGS: list[CallCaseConfig] = [
    CallCaseConfig(
        case_dir_name="call_keyword_args",
        target_function="throttler.check",
        parameter_names=["user_id", "ts"],
        call_transform=lambda c: f"emit({c})",
        transform_stub_names=["emit"],
        per_element=True,
        call_style_type=None,
        ref_declarations={},
        wrap_in_file=False,
        ref_case_per_language=False,
    ),
    CallCaseConfig(
        case_dir_name="call_scalar_args",
        target_function="process",
        parameter_names=["value"],
        call_transform=None,
        transform_stub_names=[],
        per_element=True,
        call_style_type=None,
        ref_declarations={},
        wrap_in_file=False,
        ref_case_per_language=False,
    ),
    CallCaseConfig(
        case_dir_name="call_comments",
        target_function="process",
        parameter_names=["value"],
        call_transform=None,
        transform_stub_names=[],
        per_element=True,
        call_style_type=None,
        ref_declarations={},
        wrap_in_file=False,
        ref_case_per_language=False,
    ),
    CallCaseConfig(
        case_dir_name="call_comments_dict_args",
        target_function="process",
        parameter_names=["value"],
        call_transform=None,
        transform_stub_names=[],
        per_element=True,
        call_style_type=None,
        ref_declarations={},
        wrap_in_file=False,
        ref_case_per_language=False,
    ),
    CallCaseConfig(
        case_dir_name="call_negative_int",
        target_function="process",
        parameter_names=["value"],
        call_transform=None,
        transform_stub_names=[],
        per_element=True,
        call_style_type=None,
        ref_declarations={},
        wrap_in_file=False,
        ref_case_per_language=False,
    ),
    CallCaseConfig(
        case_dir_name="call_multi_args",
        target_function="process",
        parameter_names=["value", "count"],
        call_transform=None,
        transform_stub_names=[],
        per_element=True,
        call_style_type=None,
        ref_declarations={},
        wrap_in_file=False,
        ref_case_per_language=False,
    ),
    CallCaseConfig(
        case_dir_name="call_dotted_method",
        target_function="app.client.fetch",
        parameter_names=["payload"],
        call_transform=None,
        transform_stub_names=[],
        per_element=True,
        call_style_type=None,
        ref_declarations={},
        wrap_in_file=False,
        ref_case_per_language=False,
    ),
    CallCaseConfig(
        case_dir_name="call_deep_dotted_method",
        target_function="obj.api.client.post",
        parameter_names=["data"],
        call_transform=None,
        transform_stub_names=[],
        per_element=True,
        call_style_type=None,
        ref_declarations={},
        wrap_in_file=False,
        ref_case_per_language=False,
    ),
    CallCaseConfig(
        case_dir_name="call_snake_dotted_method",
        target_function="my_app.http_client.fetch",
        parameter_names=["payload"],
        call_transform=None,
        transform_stub_names=[],
        per_element=True,
        call_style_type=None,
        ref_declarations={},
        wrap_in_file=False,
        ref_case_per_language=False,
    ),
    CallCaseConfig(
        case_dir_name="call_deep_dotted_transformed",
        target_function="app.client.fetch",
        parameter_names=["payload"],
        call_transform=lambda c: f"emit({c})",
        transform_stub_names=["emit"],
        per_element=True,
        call_style_type=None,
        ref_declarations={},
        wrap_in_file=False,
        ref_case_per_language=False,
    ),
    CallCaseConfig(
        case_dir_name="call_dotted_transform_stub",
        target_function="process",
        parameter_names=["value"],
        call_transform=lambda c: f"tracer.emit({c})",
        transform_stub_names=["tracer.emit"],
        per_element=True,
        call_style_type=None,
        ref_declarations={},
        wrap_in_file=False,
        ref_case_per_language=False,
    ),
    CallCaseConfig(
        case_dir_name="call_transform_no_wrapper",
        target_function="process",
        parameter_names=["value"],
        call_transform=lambda c: c,
        transform_stub_names=[],
        per_element=True,
        call_style_type=None,
        ref_declarations={},
        wrap_in_file=False,
        ref_case_per_language=False,
    ),
    CallCaseConfig(
        case_dir_name="call_per_element_false",
        target_function="process",
        parameter_names=["data"],
        call_transform=None,
        transform_stub_names=[],
        per_element=False,
        call_style_type=None,
        ref_declarations={},
        wrap_in_file=False,
        ref_case_per_language=False,
    ),
    CallCaseConfig(
        case_dir_name="call_ref_args",
        target_function="process",
        parameter_names=["data", "count"],
        call_transform=None,
        transform_stub_names=[],
        per_element=True,
        call_style_type=None,
        ref_declarations={
            "my_var": "[1, 2, 3]",
            "my_other": "[4, 5, 6]",
        },
        wrap_in_file=False,
        ref_case_per_language=False,
    ),
    CallCaseConfig(
        case_dir_name="call_ref_args_converted",
        target_function="process",
        parameter_names=["data", "count"],
        call_transform=None,
        transform_stub_names=[],
        per_element=True,
        call_style_type=None,
        ref_declarations={
            "my_var": "[1, 2, 3]",
            "my_other": "[4, 5, 6]",
        },
        wrap_in_file=False,
        ref_case_per_language=True,
    ),
    CallCaseConfig(
        case_dir_name="call_ref_args_converted_whole",
        target_function="process",
        parameter_names=["data"],
        call_transform=None,
        transform_stub_names=[],
        per_element=False,
        call_style_type=None,
        ref_declarations={
            "my_var": "[1, 2, 3]",
        },
        wrap_in_file=False,
        ref_case_per_language=True,
    ),
    CallCaseConfig(
        case_dir_name="call_ref_args_converted_nonsnake",
        target_function="process",
        parameter_names=["data", "count"],
        call_transform=None,
        transform_stub_names=[],
        per_element=True,
        call_style_type=None,
        ref_declarations={
            "myVar": "[1, 2, 3]",
            "MyOther": "[4, 5, 6]",
        },
        wrap_in_file=False,
        ref_case_per_language=True,
    ),
    CallCaseConfig(
        case_dir_name="call_mixed_type_dicts",
        target_function="app.mgr.op",
        parameter_names=["operation"],
        call_transform=None,
        transform_stub_names=[],
        per_element=True,
        call_style_type=None,
        ref_declarations={},
        wrap_in_file=False,
        ref_case_per_language=False,
    ),
    CallCaseConfig(
        # Drive ``literalize_call(..., wrap_in_file=True)`` directly so
        # the generated file includes its own target-function stub.
        case_dir_name="call_wrap_in_file",
        target_function="process",
        parameter_names=["a", "b"],
        call_transform=None,
        transform_stub_names=[],
        per_element=True,
        call_style_type=None,
        ref_declarations={},
        wrap_in_file=True,
        ref_case_per_language=False,
    ),
    *[
        CallCaseConfig(
            case_dir_name=f"call_{name}",
            target_function="throttler.check",
            parameter_names=["user_id", "ts"],
            call_transform=lambda c: f"emit({c})",
            transform_stub_names=["emit"],
            per_element=True,
            call_style_type=cls,
            ref_declarations={},
            wrap_in_file=False,
            ref_case_per_language=False,
        )
        for name, cls in CALL_STYLE_VARIANTS
    ],
]


# Per-case language exclusions: cases whose target function, parameter
# names, or call_transform wrapper use syntax that is invalid in a given
# language, making a valid lint-passing output impossible to generate.
CASE_LANGUAGE_INCOMPATIBLE: dict[str, frozenset[literalizer.LanguageCls]] = {
    # target_function "app.mgr.op" has "op" as the innermost name; "op"
    # is a reserved word in SML and cannot be used as a fun or val
    # identifier, so no valid stub can be produced.  COBOL cannot pass
    # multi-line DATA DIVISION entries inline in a CALL statement.
    "call_mixed_type_dicts": frozenset({Cobol, Sml}),
    # Ada and Fortran do not allow function-call results to be silently
    # discarded: a function call cannot appear as a statement.  The
    # identity call_transform (lambda c: c) causes a VALUE stub but the
    # call is used as a bare statement, which both compilers reject.
    # SystemVerilog requires void'(...) to discard a function return value;
    # a bare function call as a statement is non-standard.
    "call_transform_no_wrapper": frozenset({Ada, Fortran, SystemVerilog}),
    # call_transform wraps output as "emit(inner)", which is invalid in
    # Wren (no free-function call syntax) and COBOL (CALL statement
    # produces no expression value that can be passed to another call).
    "call_keyword_args": frozenset({Cobol, Wren}),
    "call_deep_dotted_transformed": frozenset({Cobol, Wren}),
    # call_transform wraps output as "tracer.emit(inner)" — a dotted method
    # call — and transform_stub_names=["tracer.emit"] requires a struct/object
    # stub whose syntax is invalid or unsupported in several languages.
    # OCaml module names must begin with an uppercase letter, so the stub
    # is emitted as "module Tracer = struct" but the embedded call_transform
    # produces the lowercase "tracer.emit(...)" which is unbound at the call
    # site.
    "call_dotted_transform_stub": frozenset(
        {
            Ada,
            Cobol,
            Elm,
            Erlang,
            Fortran,
            Gleam,
            Haskell,
            Hcl,
            OCaml,
            ObjectiveC,
            Php,
            PowerShell,
            Raku,
            Roc,
        }
    ),
    # Languages whose default call wrappers prepend a token to each
    # statement (Elm, Haskell, and PureScript ``_ = ``/``_ <- ``, Roc
    # ``dbg(...)``) or whose comment syntax interacts with the
    # statement separator (Erlang trailing ``.``, Jsonnet array
    # comma being swallowed by ``//``). These cannot represent a
    # standalone comment line in the wrapped self-contained file even
    # though :func:`literalizer.literalize_call` itself produces
    # syntactically valid per-call comments.
    "call_comments": frozenset(
        {
            Elm,
            Erlang,
            Haskell,
            Jsonnet,
            PureScript,
            Roc,
        }
    ),
    "call_comments_dict_args": frozenset(
        {
            Cobol,
            Dhall,
            Elm,
            Erlang,
            Haskell,
            Jsonnet,
            Mojo,
            PureScript,
            Roc,
        }
    ),
}


@dataclasses.dataclass(frozen=True)
class CallCase:
    """A parameterized call-style golden-file test case."""

    config: CallCaseConfig
    lang_cls: literalizer.LanguageCls


@functools.cache
@beartype
def discover_call_cases() -> list[CallCase]:
    """Return call test cases for all languages."""
    cases: list[CallCase] = []
    for config in CALL_CASE_CONFIGS:
        for lang_cls in sorted_languages():
            if len(lang_cls.CallStyles) == 0:
                continue
            has_dotted_target = "." in config.target_function
            if has_dotted_target and not lang_cls.supports_dotted_calls:
                continue
            if lang_cls in CASE_LANGUAGE_INCOMPATIBLE.get(
                config.case_dir_name, frozenset()
            ):
                continue
            if config.call_style_type is not None:
                # Only include languages that have this as a
                # non-default style.
                styles = list(lang_cls.CallStyles)
                matching = [
                    s
                    for s in styles
                    if isinstance(s.value, config.call_style_type)
                ]
                if not matching:
                    continue
                default_style = styles[0]
                if isinstance(default_style.value, config.call_style_type):
                    continue
            cases.append(CallCase(config=config, lang_cls=lang_cls))
    return cases


@beartype
def _run_wrap_in_file_case(
    *,
    config: CallCaseConfig,
    spec: literalizer.Language,
    yaml_string: str,
    effective_ref_case: literalizer.IdentifierCase | None,
    lang_name: str,
    lang_extension: str,
    golden_path: Path,
    file_regression: FileRegressionFixture,
) -> None:
    """Run ``literalize_call(..., wrap_in_file=True)`` and check
    golden.
    """
    try:
        wrap_result = literalizer.literalize_call(
            source=yaml_string,
            input_format=literalizer.InputFormat.YAML,
            language=spec,
            target_function=config.target_function,
            parameter_names=config.parameter_names,
            call_transform=config.call_transform,
            per_element=config.per_element,
            wrap_in_file=True,
            ref_case=effective_ref_case,
        )
    except CallArgNotSupportedError as exc:
        golden_path.unlink(missing_ok=True)
        pytest.skip(f"{lang_name} rejected call arg: {exc.reason}")
    check_golden(
        file_regression=file_regression,
        contents=wrap_result.code + "\n",
        extension=lang_extension,
        newline="",
        golden_path=golden_path,
    )


@beartype
def run_call_golden_case(
    *,
    config: CallCaseConfig,
    spec: literalizer.Language,
    golden_name: str,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
) -> None:
    """Assemble a literalize_call golden-file case against *golden_name*.

    Shared by ``test_call_golden_file`` (default-spec per language)
    and ``test_call_variant_golden_file`` (non-default language
    variants, e.g. Rust's ``TAGGED_ENUM`` on an input the default
    ``ERROR`` strategy rejects).
    """
    lang_cls = type(spec)
    input_path = cases_dir / config.case_dir_name / "input.yaml"
    yaml_string = input_path.read_text()
    golden_path = input_path.parent / (golden_name + lang_cls.extension)
    spec = with_per_fixture_module_name(spec=spec, golden_path=golden_path)
    effective_ref_case: literalizer.IdentifierCase | None
    if config.ref_case_per_language:
        # First element of ``identifier_cases`` is the language's
        # default — convert declaration names to that case so the
        # ref-site and declaration-site spellings agree.
        default_case = spec.identifier_cases[0]
        effective_ref_case = default_case
        declarations = {
            default_case.convert(name=ref_name): ref_source
            for ref_name, ref_source in config.ref_declarations.items()
        }
    else:
        effective_ref_case = None
        declarations = config.ref_declarations
    if config.wrap_in_file:
        _run_wrap_in_file_case(
            config=config,
            spec=spec,
            yaml_string=yaml_string,
            effective_ref_case=effective_ref_case,
            lang_name=lang_cls.__name__,
            lang_extension=lang_cls.extension,
            golden_path=golden_path,
            file_regression=file_regression,
        )
        return
    try:
        # Literalize each ``{"$ref": "name"}`` target into a variable
        # declaration so the generated file is self-contained and the
        # golden file can lint cleanly.
        decl_results: list[literalizer.LiteralizeResult] = [
            literalizer.literalize(
                source=ref_source,
                input_format=literalizer.InputFormat.JSON,
                language=spec,
                variable_form=literalizer.NewVariable(name=ref_name),
            )
            for ref_name, ref_source in declarations.items()
        ]
        result = literalizer.literalize_call(
            source=yaml_string,
            input_format=literalizer.InputFormat.YAML,
            language=spec,
            target_function=config.target_function,
            parameter_names=config.parameter_names,
            call_transform=config.call_transform,
            per_element=config.per_element,
            ref_case=effective_ref_case,
        )
    except HeterogeneousCollectionError:
        golden_path.unlink(missing_ok=True)
        pytest.skip(
            f"{lang_cls.__name__} cannot represent this heterogeneous input",
        )
    except CallArgNotSupportedError as exc:
        golden_path.unlink(missing_ok=True)
        pytest.skip(
            f"{lang_cls.__name__} rejected call arg: {exc.reason}",
        )
    # Build stub declarations for undefined names.
    body_stubs: list[str] = []
    preamble_stubs: list[str] = []
    stub_return = (
        StubReturn.VALUE
        if config.call_transform is not None
        else StubReturn.VOID
    )
    target_function_parts = tuple(config.target_function.split(sep="."))
    # Stubs for the call function (with full parameter names).
    body_stubs.extend(
        spec.format_call_stub(
            target_function_parts,
            config.parameter_names,
            stub_return,
        ),
    )
    preamble_stubs.extend(
        spec.format_call_preamble_stub(
            target_function_parts,
            config.parameter_names,
            stub_return,
        ),
    )
    # Stubs for transform function names (single argument).
    for wrapper_name in config.transform_stub_names:
        wrapper_name_parts = tuple(wrapper_name.split(sep="."))
        body_stubs.extend(
            spec.format_call_stub(
                wrapper_name_parts,
                ["_arg"],
                StubReturn.VOID,
            ),
        )
        preamble_stubs.extend(
            spec.format_call_preamble_stub(
                wrapper_name_parts,
                ["_arg"],
                StubReturn.VOID,
            ),
        )
    decl_preambles = tuple(line for d in decl_results for line in d.preamble)
    # Recompute the body preamble across the union of types observed in
    # every declaration *and* the call.  Concatenating each piece's
    # already-rendered body preamble would emit overlapping
    # type-definition strings (e.g. Haskell's ``data Val = ...`` with
    # different constructor sets) that no string-level duplicate
    # filter can reconcile.  Combine ``source_data`` from every piece
    # so ``compute_body_preamble`` can inspect actual values when it
    # needs to (e.g. Haskell's datetime microsecond-precision check).
    empty_types: frozenset[type] = frozenset()
    union_types = empty_types.union(
        *(d.types_present for d in decl_results),
        result.types_present,
    )
    combined_source_data: list[Value] = [
        *(d.source_data for d in decl_results),
        result.source_data,
    ]
    unified_body_preamble = spec.compute_body_preamble(
        union_types, combined_source_data
    )
    call_body_preamble = unified_body_preamble + tuple(body_stubs)
    declarations_bare_codes = tuple(d.bare_code for d in decl_results)
    wrapped = spec.wrap_calls_with_declarations(
        declarations=declarations_bare_codes,
        calls=result.bare_code,
        body_preamble=call_body_preamble,
    )
    all_preamble = _dedupe_preamble_blocks(
        blocks=decl_preambles + result.preamble + tuple(preamble_stubs)
    )
    wrapped = _prepend_preamble(wrapped=wrapped, preamble=all_preamble)
    check_golden(
        file_regression=file_regression,
        contents=wrapped + "\n",
        extension=lang_cls.extension,
        newline="",
        golden_path=golden_path,
    )
