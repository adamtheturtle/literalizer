"""``literalize_call`` golden-file case configuration and runner.

The configurations describe how each ``cases/call_*`` directory is
driven through :func:`literalizer.literalize_call`.  The runner
(``run_call_golden_case``) is shared by ``test_call_golden_file`` and
``test_call_variant_golden_file``.
"""

import dataclasses
import functools
from collections.abc import Callable, Sequence
from pathlib import Path

import pytest
from beartype import beartype
from pytest_regressions.file_regression import FileRegressionFixture

import literalizer
from literalizer._language import StubReturn
from literalizer._preamble import deduplicate_preamble_entries
from literalizer._types import Value
from literalizer.exceptions import (
    CallArgNotSupportedError,
    DottedCallStubNotSupportedError,
    DottedCallTargetNotSupportedError,
    FreeFunctionCallNotSupportedError,
    HeterogeneousCollectionError,
    UnsupportedCallShapeError,
    VariableNameNotSupportedError,
)

from .check_golden import check_golden
from .language_specs import (
    make_golden_path,
    sorted_languages,
    with_per_fixture_module_name,
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
    # Names from ``ref_declarations`` (in their original case) that
    # ``literalize_call`` may treat as consumable.  Empty means no ref
    # is consumed.
    consumable_refs: frozenset[str]
    requires_call_returns_expression: bool
    requires_inline_multiline_dict_args: bool
    requires_standalone_wrapped_comments: bool


CALL_STYLE_VARIANTS: list[tuple[str, type[literalizer.CallStyle]]] = [
    ("keyword", literalizer.KeywordCallStyle),
    ("positional", literalizer.PositionalCallStyle),
    ("object", literalizer.ObjectCallStyle),
    ("curried", literalizer.CommandCallStyle),
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
        consumable_refs=frozenset[str](),
        requires_call_returns_expression=True,
        requires_inline_multiline_dict_args=False,
        requires_standalone_wrapped_comments=False,
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
        consumable_refs=frozenset[str](),
        requires_call_returns_expression=False,
        requires_inline_multiline_dict_args=False,
        requires_standalone_wrapped_comments=False,
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
        consumable_refs=frozenset[str](),
        requires_call_returns_expression=False,
        requires_inline_multiline_dict_args=False,
        requires_standalone_wrapped_comments=True,
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
        consumable_refs=frozenset[str](),
        requires_call_returns_expression=False,
        requires_inline_multiline_dict_args=True,
        requires_standalone_wrapped_comments=True,
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
        consumable_refs=frozenset[str](),
        requires_call_returns_expression=False,
        requires_inline_multiline_dict_args=False,
        requires_standalone_wrapped_comments=False,
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
        consumable_refs=frozenset[str](),
        requires_call_returns_expression=False,
        requires_inline_multiline_dict_args=False,
        requires_standalone_wrapped_comments=False,
    ),
    CallCaseConfig(
        # Four-parameter call.
        case_dir_name="call_quad_args",
        target_function="process",
        parameter_names=["a", "b", "c", "d"],
        call_transform=None,
        transform_stub_names=[],
        per_element=True,
        call_style_type=None,
        ref_declarations={},
        wrap_in_file=False,
        ref_case_per_language=False,
        consumable_refs=frozenset[str](),
        requires_call_returns_expression=False,
        requires_inline_multiline_dict_args=False,
        requires_standalone_wrapped_comments=False,
    ),
    CallCaseConfig(
        case_dir_name="call_reserved_target",
        target_function="op",  # Reserved in SML.
        parameter_names=["value"],
        call_transform=None,
        transform_stub_names=[],
        per_element=True,
        call_style_type=None,
        ref_declarations={},
        wrap_in_file=False,
        ref_case_per_language=False,
        consumable_refs=frozenset[str](),
        requires_call_returns_expression=False,
        requires_inline_multiline_dict_args=False,
        requires_standalone_wrapped_comments=False,
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
        consumable_refs=frozenset[str](),
        requires_call_returns_expression=False,
        requires_inline_multiline_dict_args=False,
        requires_standalone_wrapped_comments=False,
    ),
    CallCaseConfig(
        case_dir_name="call_homogeneous_dotted_method",
        target_function="app.client.fetch",
        parameter_names=["value"],
        call_transform=None,
        transform_stub_names=[],
        per_element=True,
        call_style_type=None,
        ref_declarations={},
        wrap_in_file=False,
        ref_case_per_language=False,
        consumable_refs=frozenset[str](),
        requires_call_returns_expression=False,
        requires_inline_multiline_dict_args=False,
        requires_standalone_wrapped_comments=False,
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
        consumable_refs=frozenset[str](),
        requires_call_returns_expression=False,
        requires_inline_multiline_dict_args=False,
        requires_standalone_wrapped_comments=False,
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
        consumable_refs=frozenset[str](),
        requires_call_returns_expression=False,
        requires_inline_multiline_dict_args=False,
        requires_standalone_wrapped_comments=False,
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
        consumable_refs=frozenset[str](),
        requires_call_returns_expression=True,
        requires_inline_multiline_dict_args=False,
        requires_standalone_wrapped_comments=False,
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
        consumable_refs=frozenset[str](),
        requires_call_returns_expression=True,
        requires_inline_multiline_dict_args=False,
        requires_standalone_wrapped_comments=False,
    ),
    CallCaseConfig(
        case_dir_name="call_transform_no_wrapper",
        target_function="process",
        parameter_names=["value"],
        call_transform=None,
        transform_stub_names=[],
        per_element=True,
        call_style_type=None,
        ref_declarations={},
        wrap_in_file=False,
        ref_case_per_language=False,
        consumable_refs=frozenset[str](),
        requires_call_returns_expression=False,
        requires_inline_multiline_dict_args=False,
        requires_standalone_wrapped_comments=False,
    ),
    CallCaseConfig(
        case_dir_name="call_no_params",
        target_function="process",
        parameter_names=[],
        call_transform=None,
        transform_stub_names=[],
        per_element=True,
        call_style_type=None,
        ref_declarations={},
        wrap_in_file=False,
        ref_case_per_language=False,
        consumable_refs=frozenset[str](),
        requires_call_returns_expression=False,
        requires_inline_multiline_dict_args=False,
        requires_standalone_wrapped_comments=False,
    ),
    CallCaseConfig(
        case_dir_name="call_no_params_transform",
        target_function="process",
        parameter_names=[],
        call_transform=lambda c: f"emit({c})",
        transform_stub_names=["emit"],
        per_element=True,
        call_style_type=None,
        ref_declarations={},
        wrap_in_file=False,
        ref_case_per_language=False,
        consumable_refs=frozenset[str](),
        requires_call_returns_expression=True,
        requires_inline_multiline_dict_args=False,
        requires_standalone_wrapped_comments=False,
    ),
    CallCaseConfig(
        case_dir_name="call_no_params_curried",
        target_function="process",
        parameter_names=[],
        call_transform=None,
        transform_stub_names=[],
        per_element=True,
        call_style_type=literalizer.CommandCallStyle,
        ref_declarations={},
        wrap_in_file=False,
        ref_case_per_language=False,
        consumable_refs=frozenset[str](),
        requires_call_returns_expression=False,
        requires_inline_multiline_dict_args=False,
        requires_standalone_wrapped_comments=False,
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
        consumable_refs=frozenset[str](),
        requires_call_returns_expression=False,
        requires_inline_multiline_dict_args=False,
        requires_standalone_wrapped_comments=False,
    ),
    CallCaseConfig(
        case_dir_name="call_per_element_false_dict_arg",
        target_function="process",
        parameter_names=["value"],
        call_transform=None,
        transform_stub_names=[],
        per_element=False,
        call_style_type=None,
        ref_declarations={},
        wrap_in_file=False,
        ref_case_per_language=False,
        consumable_refs=frozenset[str](),
        requires_call_returns_expression=False,
        requires_inline_multiline_dict_args=True,
        requires_standalone_wrapped_comments=False,
    ),
    CallCaseConfig(
        case_dir_name="call_homogeneous_value_dict_arg",
        target_function="process",
        parameter_names=["value"],
        call_transform=None,
        transform_stub_names=[],
        per_element=False,
        call_style_type=None,
        ref_declarations={},
        wrap_in_file=False,
        ref_case_per_language=False,
        consumable_refs=frozenset[str](),
        requires_call_returns_expression=False,
        requires_inline_multiline_dict_args=True,
        requires_standalone_wrapped_comments=False,
    ),
    CallCaseConfig(
        case_dir_name="call_existing_ref_arg",
        target_function="process",
        parameter_names=["value"],
        call_transform=None,
        transform_stub_names=[],
        per_element=True,
        call_style_type=None,
        ref_declarations={"existing": "42"},
        wrap_in_file=False,
        ref_case_per_language=False,
        consumable_refs=frozenset[str](),
        requires_call_returns_expression=False,
        requires_inline_multiline_dict_args=False,
        requires_standalone_wrapped_comments=False,
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
        consumable_refs=frozenset({"my_var", "my_other"}),
        requires_call_returns_expression=False,
        requires_inline_multiline_dict_args=False,
        requires_standalone_wrapped_comments=False,
    ),
    CallCaseConfig(
        # Same ref reused across multiple per-element calls.  The
        # caller declares both refs consumable; the renderer must still
        # avoid the consuming form (e.g. C++ ``std::move``, Mojo ``^``)
        # for the reused ref so the second call does not read a
        # moved-from variable.  ``repeated_var`` is a scalar int so it
        # is ``Copy`` in Rust and can be referenced twice; ``single_var``
        # is a list so the consuming form rendered in C++ / Mojo
        # operates on a non-trivial type and does not trigger
        # trivial-type "no effect" lints.  Variable names avoid
        # ``shared``, which is reserved in D, V, and VisualBasic.
        case_dir_name="call_ref_args_reused",
        target_function="process",
        parameter_names=["data", "count"],
        call_transform=None,
        transform_stub_names=[],
        per_element=True,
        call_style_type=None,
        ref_declarations={
            "single_var": "[4, 5, 6]",
            "repeated_var": "1",
        },
        wrap_in_file=False,
        ref_case_per_language=False,
        consumable_refs=frozenset({"repeated_var", "single_var"}),
        requires_call_returns_expression=False,
        requires_inline_multiline_dict_args=False,
        requires_standalone_wrapped_comments=False,
    ),
    CallCaseConfig(
        # Mix of register-trivial (Int / Bool / Float64) and non-trivial
        # (List) consumable refs.  Each ref is single-use, so without
        # the consume-suppression hook every ref would be eligible for
        # the consuming form.  the Mojo ``^`` is a hard error under
        # ``--Werror`` for register-trivial scalars, so the trivial refs
        # must emit as bare identifiers while ``my_list`` keeps ``^``.
        # Other languages that move consumable refs (notably C++) still
        # render the consuming form for every ref.
        case_dir_name="call_ref_args_trivial_register",
        target_function="process",
        parameter_names=["value", "count"],
        call_transform=None,
        transform_stub_names=[],
        per_element=True,
        call_style_type=None,
        ref_declarations={
            "my_int": "1",
            "my_bool": "true",
            "my_float": "3.14",
            "my_list": "[1, 2, 3]",
        },
        wrap_in_file=False,
        ref_case_per_language=False,
        consumable_refs=frozenset(
            {"my_int", "my_bool", "my_float", "my_list"},
        ),
        requires_call_returns_expression=False,
        requires_inline_multiline_dict_args=False,
        requires_standalone_wrapped_comments=False,
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
        consumable_refs=frozenset({"my_var", "my_other"}),
        requires_call_returns_expression=False,
        requires_inline_multiline_dict_args=False,
        requires_standalone_wrapped_comments=False,
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
        consumable_refs=frozenset({"my_var"}),
        requires_call_returns_expression=False,
        requires_inline_multiline_dict_args=False,
        requires_standalone_wrapped_comments=False,
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
        consumable_refs=frozenset({"myVar", "MyOther"}),
        requires_call_returns_expression=False,
        requires_inline_multiline_dict_args=False,
        requires_standalone_wrapped_comments=False,
    ),
    CallCaseConfig(
        # Slot 0 holds lists whose Mojo element type disagrees across
        # calls (``List[Int]`` vs ``List[String]``), forcing
        # ``_mojo_typed_param_list`` to fall back to the generic
        # ``[*Ts: AnyType](*args: *Ts)`` stub so the typed list-slot
        # path stays the only producer of ``data: List[T]`` signatures.
        case_dir_name="call_ref_args_heterogeneous_list",
        target_function="process",
        parameter_names=["data", "count"],
        call_transform=None,
        transform_stub_names=[],
        per_element=True,
        call_style_type=None,
        ref_declarations={
            "my_ints": "[1, 2, 3]",
            "my_strings": '["a", "b"]',
            "my_empty": "[]",
        },
        wrap_in_file=False,
        ref_case_per_language=False,
        consumable_refs=frozenset({"my_ints", "my_strings", "my_empty"}),
        requires_call_returns_expression=False,
        requires_inline_multiline_dict_args=False,
        requires_standalone_wrapped_comments=False,
    ),
    CallCaseConfig(
        case_dir_name="call_ref_args_escaped_quote",
        target_function="process",
        parameter_names=["v"],
        call_transform=None,
        transform_stub_names=[],
        per_element=True,
        call_style_type=None,
        ref_declarations={"my_str": '"a\\"b"'},
        wrap_in_file=False,
        ref_case_per_language=False,
        consumable_refs=frozenset[str](),
        requires_call_returns_expression=False,
        requires_inline_multiline_dict_args=False,
        requires_standalone_wrapped_comments=False,
    ),
    CallCaseConfig(
        case_dir_name="call_ref_nested_in_list",
        target_function="process",
        parameter_names=["data"],
        call_transform=None,
        transform_stub_names=[],
        per_element=True,
        call_style_type=None,
        ref_declarations={
            "my_var": "42",
            "my_other": "7",
        },
        wrap_in_file=False,
        ref_case_per_language=False,
        consumable_refs=frozenset[str](),
        requires_call_returns_expression=False,
        requires_inline_multiline_dict_args=False,
        requires_standalone_wrapped_comments=False,
    ),
    CallCaseConfig(
        case_dir_name="call_ref_nested_in_dict",
        target_function="process",
        parameter_names=["data"],
        call_transform=None,
        transform_stub_names=[],
        per_element=True,
        call_style_type=None,
        ref_declarations={
            "my_var": "42",
        },
        wrap_in_file=False,
        ref_case_per_language=False,
        consumable_refs=frozenset[str](),
        requires_call_returns_expression=False,
        requires_inline_multiline_dict_args=False,
        requires_standalone_wrapped_comments=False,
    ),
    CallCaseConfig(
        case_dir_name="call_ref_nested_converted",
        target_function="process",
        parameter_names=["data"],
        call_transform=None,
        transform_stub_names=[],
        per_element=True,
        call_style_type=None,
        ref_declarations={
            "myVar": "42",
        },
        wrap_in_file=False,
        ref_case_per_language=True,
        consumable_refs=frozenset[str](),
        requires_call_returns_expression=False,
        requires_inline_multiline_dict_args=False,
        requires_standalone_wrapped_comments=False,
    ),
    CallCaseConfig(
        case_dir_name="call_mixed_type_dicts",
        target_function="app.mgr.run",
        parameter_names=["operation"],
        call_transform=None,
        transform_stub_names=[],
        per_element=True,
        call_style_type=None,
        ref_declarations={},
        wrap_in_file=False,
        ref_case_per_language=False,
        consumable_refs=frozenset[str](),
        requires_call_returns_expression=False,
        requires_inline_multiline_dict_args=True,
        requires_standalone_wrapped_comments=False,
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
        consumable_refs=frozenset[str](),
        requires_call_returns_expression=False,
        requires_inline_multiline_dict_args=False,
        requires_standalone_wrapped_comments=False,
    ),
    CallCaseConfig(
        case_dir_name="call_wrap_in_file_escaped_quote",
        target_function="process",
        parameter_names=["v"],
        call_transform=None,
        transform_stub_names=[],
        per_element=True,
        call_style_type=None,
        ref_declarations={},
        wrap_in_file=True,
        ref_case_per_language=False,
        consumable_refs=frozenset[str](),
        requires_call_returns_expression=False,
        requires_inline_multiline_dict_args=False,
        requires_standalone_wrapped_comments=False,
    ),
    CallCaseConfig(
        case_dir_name="call_scalar_args_uniform_second_slot",
        target_function="process",
        parameter_names=["value", "label"],
        call_transform=None,
        transform_stub_names=[],
        per_element=True,
        call_style_type=None,
        ref_declarations={},
        wrap_in_file=False,
        ref_case_per_language=False,
        consumable_refs=frozenset[str](),
        requires_call_returns_expression=False,
        requires_inline_multiline_dict_args=False,
        requires_standalone_wrapped_comments=False,
    ),
    CallCaseConfig(
        case_dir_name="call_scalar_args_with_null",
        target_function="process",
        parameter_names=["value"],
        call_transform=None,
        transform_stub_names=[],
        per_element=True,
        call_style_type=None,
        ref_declarations={},
        wrap_in_file=False,
        ref_case_per_language=False,
        consumable_refs=frozenset[str](),
        requires_call_returns_expression=False,
        requires_inline_multiline_dict_args=False,
        requires_standalone_wrapped_comments=False,
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
            consumable_refs=frozenset[str](),
            requires_call_returns_expression=True,
            requires_inline_multiline_dict_args=False,
            requires_standalone_wrapped_comments=False,
        )
        for name, cls in CALL_STYLE_VARIANTS
    ],
]


@dataclasses.dataclass(frozen=True)
class CallCase:
    """A parameterized call-style golden-file test case."""

    config: CallCaseConfig
    lang_cls: literalizer.LanguageCls
    expected_exception: type[Exception] | None = None


@beartype
def _expected_call_shape_exception(
    *,
    lang_cls: literalizer.LanguageCls,
    config: CallCaseConfig,
) -> type[Exception] | None:
    """Return the exception ``literalize_call`` is expected to raise for
    this (lang, config) pair, or ``None`` if it should produce output.
    """
    parameter_count = len(config.parameter_names)
    if parameter_count == 0 and not lang_cls.supports_zero_parameter_calls:
        return UnsupportedCallShapeError
    if (
        config.requires_inline_multiline_dict_args
        and not lang_cls.supports_inline_multiline_dict_args
    ):
        return UnsupportedCallShapeError
    if (
        config.requires_call_returns_expression
        and not lang_cls.call_returns_expression
    ):
        return UnsupportedCallShapeError
    if (
        config.requires_standalone_wrapped_comments
        and not lang_cls.supports_standalone_comments_in_wrapped_calls
    ):
        return UnsupportedCallShapeError
    innermost_target_function = config.target_function.split(sep=".")[-1]
    if innermost_target_function in lang_cls.reserved_identifiers:
        return UnsupportedCallShapeError
    return None


@functools.cache
@beartype
def discover_call_cases() -> list[CallCase]:
    """Return call test cases for all languages."""
    cases: list[CallCase] = []
    for config in CALL_CASE_CONFIGS:
        for lang_cls in sorted_languages():
            if len(lang_cls.CallStyles) == 0:
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
            expected_exception = _expected_call_shape_exception(
                lang_cls=lang_cls,
                config=config,
            )
            cases.append(
                CallCase(
                    config=config,
                    lang_cls=lang_cls,
                    expected_exception=expected_exception,
                )
            )
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


@dataclasses.dataclass(frozen=True)
class _CallWithDeclarations:
    """Result of literalizing ref declarations and a call together."""

    decl_results: list[literalizer.LiteralizeResult]
    result: literalizer.LiteralizeResult


@beartype
def _run_call_with_declarations(
    *,
    config: CallCaseConfig,
    spec: literalizer.Language,
    yaml_string: str,
    declaration_names: dict[str, str],
    effective_ref_case: literalizer.IdentifierCase | None,
    lang_name: str,
    golden_path: Path,
) -> _CallWithDeclarations:
    """Run ref declarations and the call, skipping on typed unsupported
    signals.
    """
    try:
        decl_results_by_ref_name: dict[str, literalizer.LiteralizeResult] = {
            ref_name: literalizer.literalize(
                source=ref_source,
                input_format=literalizer.InputFormat.JSON,
                language=spec,
                variable_form=literalizer.NewVariable(
                    name=declaration_names[ref_name],
                ),
            )
            for ref_name, ref_source in config.ref_declarations.items()
        }
        decl_results = list(decl_results_by_ref_name.values())
        ref_values = {
            ref_name: declaration.source_data
            for ref_name, declaration in decl_results_by_ref_name.items()
        }
        result = literalizer.literalize_call(
            source=yaml_string,
            input_format=literalizer.InputFormat.YAML,
            language=spec,
            target_function=config.target_function,
            parameter_names=config.parameter_names,
            call_transform=config.call_transform,
            per_element=config.per_element,
            ref_case=effective_ref_case,
            consumable_refs=config.consumable_refs,
            ref_values=ref_values or None,
        )
    except VariableNameNotSupportedError:
        golden_path.unlink(missing_ok=True)
        pytest.skip(
            f"{lang_name} does not support variable-name wrapping "
            f"for ref declarations",
        )
    except HeterogeneousCollectionError:
        golden_path.unlink(missing_ok=True)
        pytest.skip(
            f"{lang_name} cannot represent this heterogeneous input",
        )
    except DottedCallTargetNotSupportedError:
        golden_path.unlink(missing_ok=True)
        pytest.skip(f"{lang_name} does not support dotted call targets")
    except DottedCallStubNotSupportedError:
        golden_path.unlink(missing_ok=True)
        pytest.skip(f"{lang_name} does not support dotted call stubs")
    except FreeFunctionCallNotSupportedError:
        golden_path.unlink(missing_ok=True)
        pytest.skip(f"{lang_name} has no free function call syntax")
    except CallArgNotSupportedError as exc:
        golden_path.unlink(missing_ok=True)
        pytest.skip(f"{lang_name} rejected call arg: {exc.reason}")
    return _CallWithDeclarations(decl_results=decl_results, result=result)


@beartype
def _arg_values_for_stub(
    *,
    source_data: Value,
    per_element: bool,
) -> Sequence[Value]:
    """Mirror ``_literalize.py``'s ``arg_values`` shape: a list of
    arguments rows for per-element calls; a single-entry list
    wrapping the whole data otherwise.

    A per-element call always yields a list ``source_data``; the
    ``isinstance`` check narrows the type for the static checker.
    """
    if per_element and isinstance(source_data, list):
        return source_data
    return [source_data]


@beartype
def run_call_golden_case(
    *,
    config: CallCaseConfig,
    spec: literalizer.Language,
    lang_cls: literalizer.LanguageCls,
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
    input_path = cases_dir / config.case_dir_name / "input.yaml"
    yaml_string = input_path.read_text()
    golden_path = make_golden_path(
        parent=input_path.parent,
        name=golden_name,
        extension=lang_cls.extension,
        lang_cls=lang_cls,
    )
    spec = with_per_fixture_module_name(spec=spec, golden_path=golden_path)
    effective_ref_case: literalizer.IdentifierCase | None
    if config.ref_case_per_language:
        # First element of ``identifier_cases`` is the language's
        # default — convert declaration names to that case so the
        # ref-site and declaration-site spellings agree.
        default_case = spec.identifier_cases[0]
        effective_ref_case = default_case
        declaration_names = {
            ref_name: default_case.convert(name=ref_name)
            for ref_name in config.ref_declarations
        }
    else:
        effective_ref_case = None
        declaration_names = {
            ref_name: ref_name for ref_name in config.ref_declarations
        }
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
    call_outcome = _run_call_with_declarations(
        config=config,
        spec=spec,
        yaml_string=yaml_string,
        declaration_names=declaration_names,
        effective_ref_case=effective_ref_case,
        lang_name=lang_cls.__name__,
        golden_path=golden_path,
    )
    decl_results = call_outcome.decl_results
    result = call_outcome.result
    # Build stub declarations for undefined names.
    body_stubs: list[str] = []
    preamble_stubs: list[str] = []
    stub_return = (
        StubReturn.VALUE
        if config.call_transform is not None
        else StubReturn.VOID
    )
    target_function_parts = tuple(config.target_function.split(sep="."))
    call_arg_values = _arg_values_for_stub(
        source_data=result.source_data,
        per_element=config.per_element,
    )
    body_stubs.extend(
        spec.format_call_stub(
            target_function_parts,
            config.parameter_names,
            stub_return,
            call_arg_values,
        ),
    )
    try:
        preamble_stubs.extend(
            spec.format_call_preamble_stub(
                target_function_parts,
                config.parameter_names,
                stub_return,
                call_arg_values,
            ),
        )
    except HeterogeneousCollectionError:
        golden_path.unlink(missing_ok=True)
        pytest.skip(
            f"{lang_cls.__name__} cannot represent this heterogeneous "
            "input in its typed call stub",
        )
    # Stubs for transform function names (single argument).
    for wrapper_name in config.transform_stub_names:
        wrapper_name_parts = tuple(wrapper_name.split(sep="."))
        body_stubs.extend(
            spec.format_call_stub(
                wrapper_name_parts,
                ["_arg"],
                StubReturn.VOID,
                (),
            ),
        )
        preamble_stubs.extend(
            spec.format_call_preamble_stub(
                wrapper_name_parts,
                ["_arg"],
                StubReturn.VOID,
                (),
            ),
        )
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
    if (
        result.contains_standalone_comments
        and not spec.supports_standalone_comments_in_wrapped_calls
    ):
        raise UnsupportedCallShapeError(
            language_name=lang_cls.__name__,
            reason=(
                "standalone comments cannot be preserved when wrapping "
                "calls in this language"
            ),
        )
    declarations_bare_codes = tuple(d.bare_code for d in decl_results)
    wrapped = spec.wrap_calls_with_declarations(
        declarations=declarations_bare_codes,
        calls=result.bare_code,
        body_preamble=call_body_preamble,
    )
    # ``literalize_call`` substitutes ``ref_values`` into the data fed
    # to its preamble computation, so ``result.preamble`` already
    # contains the union version of any multi-line data-dependent block
    # (e.g. Gleam's ``pub type GVal {...}``) covering every type
    # observed across the declarations *and* the call.  Each
    # declaration's own multi-line block, by contrast, was computed
    # from that declaration's data alone and would conflict with the
    # union version under string-level duplicate filtering.  Drop the
    # multi-line entries from declaration preambles and keep their
    # single-line entries (e.g. the Nim ``import json`` line);
    # filtering duplicate lines handles the rest.
    decl_preamble_lines = tuple(
        entry
        for d in decl_results
        for entry in d.preamble
        if "\n" not in entry
    )
    all_preamble = deduplicate_preamble_entries(
        entries=decl_preamble_lines + result.preamble + tuple(preamble_stubs),
    )
    wrapped = _prepend_preamble(wrapped=wrapped, preamble=all_preamble)
    check_golden(
        file_regression=file_regression,
        contents=wrapped + "\n",
        extension=lang_cls.extension,
        newline="",
        golden_path=golden_path,
    )
