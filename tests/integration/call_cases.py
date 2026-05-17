"""``literalize_call`` golden-file case configuration and runner.

The configurations describe how each ``cases/call_*`` directory is
driven through :func:`literalizer.literalize_call`.  The runner
(``run_call_golden_case``) is shared by ``test_call_golden_file`` and
``test_call_variant_golden_file``.
"""

import dataclasses
import datetime
import enum
import functools
import json
from collections.abc import Callable, Sequence
from pathlib import Path

import pytest
from beartype import beartype
from pytest_regressions.file_regression import FileRegressionFixture

import literalizer
from literalizer import StubReturn

# ``_literalize_call_with_declarations`` is the shared call/declaration
# reconciliation core; it is intentionally not part of the public API
# (the public surface is ``literalize_call(bound_refs=...)``).  This
# golden-file harness must interpose its own transform-wrapper stubs
# between rendering and composition, so it uses the internal core
# directly.  See issue #1946.
from literalizer._literalize import _literalize_call_with_declarations
from literalizer.exceptions import (
    CallArgNotSupportedError,
    DottedCallTargetNotSupportedError,
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

# Spelled out locally to mirror ``literalizer._types.Value`` without
# importing from a private module (see issue #1947); ``source_data``
# flows in from the parsed YAML, so containers may be ruamel
# comment-tracking subclasses of ``list``/``dict``.
type _Scalar = (
    str
    | int
    | float
    | bool
    | None
    | datetime.date
    | datetime.datetime
    | datetime.time
    | bytes
)
type _Value = _Scalar | list[_Value] | dict[_Scalar, _Value] | set[_Scalar]


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
    call_transform: Callable[[literalizer.CallContext], str] | None
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
    # When set (only meaningful with ``wrap_in_file=True`` and a
    # ``variable_form``), emit a golden for a language only when its
    # ``variable_form`` output is byte-identical to its output under
    # this mirror form.  ``ExistingVariable`` call-binding wrapped in a
    # file is self-contained (compiles standalone) exactly for the
    # languages whose assignment *is* a declaration -- functional
    # ``let`` rebinds (OCaml/F#/Haskell/Roc/PureScript/Elm) and dynamic
    # languages where a bare assignment defines the name.  For those,
    # the ``ExistingVariable`` output equals the ``NewVariable``
    # declaration form, which already has a compiling
    # ``call_variable_form_new`` golden -- so an identical
    # ``ExistingVariable`` fixture provably compiles too, with no
    # hand-maintained allow-list.  Imperative compiled languages emit a
    # bare assignment to an undeclared name (not self-contained, fails
    # the lint-CI compile of every fixture); they diverge from the
    # ``NewVariable`` form and are skipped (no golden) instead.  ``None``
    # disables the gate (every supporting language gets a golden).
    self_contained_mirror_variable_form: literalizer.VariableForm | None
    # When set, drive ``literalize_call(..., variable_form=...)`` to
    # exercise the call-binding output mode.  Only meaningful with
    # ``per_element=False`` and (typically) ``wrap_in_file=True`` so
    # the generated file is self-contained around the binding.
    variable_form: literalizer.VariableForm | None
    # Companion source whose parsed top-level elements pair
    # positionally with the generated calls and are exposed on
    # ``CallContext.zipped``.  Requires ``call_transform``.  Parsed
    # with ``zip_input_format``.
    zip_source: str | None
    zip_input_format: literalizer.InputFormat | None
    # Trailing source-code comments, one per generated call, paired
    # positionally and emitted after the statement terminator using the
    # language's comment syntax.  An empty entry emits no comment.
    comment_source: list[str] | None
    # Parameter names used when stubbing each ``transform_stub_names``
    # wrapper.  The length sets how many parameters the wrapper takes,
    # so a transform that calls the wrapper with the call *and* the
    # zipped value (two arguments) compiles in fixed-parameter-count
    # languages.
    transform_stub_param_names: list[str]
    # Languages (by class name) that cannot represent this case's
    # generated fixture and are skipped (no golden) instead of emitting
    # non-compiling output.
    skip_lang_names: frozenset[str]


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
        call_transform=lambda ctx: f"emit({ctx.call})",
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
        self_contained_mirror_variable_form=None,
        variable_form=None,
        zip_source=None,
        zip_input_format=None,
        comment_source=None,
        transform_stub_param_names=["_arg"],
        skip_lang_names=frozenset(),
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
        self_contained_mirror_variable_form=None,
        variable_form=None,
        zip_source=None,
        zip_input_format=None,
        comment_source=None,
        transform_stub_param_names=["_arg"],
        skip_lang_names=frozenset(),
    ),
    CallCaseConfig(
        case_dir_name="call_line_comments",
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
        # comment_source emits trailing comments through the language's
        # call-sequence form, the same constraint as wrapped standalone
        # comments; languages without that support raise
        # UnsupportedCallShapeError (see _validate_comment_source_supported).
        requires_standalone_wrapped_comments=True,
        self_contained_mirror_variable_form=None,
        variable_form=None,
        zip_source=None,
        zip_input_format=None,
        comment_source=["first edition", "", "cyberpunk"],
        transform_stub_param_names=["_arg"],
        skip_lang_names=frozenset(),
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
        self_contained_mirror_variable_form=None,
        variable_form=None,
        zip_source=None,
        zip_input_format=None,
        comment_source=None,
        transform_stub_param_names=["_arg"],
        skip_lang_names=frozenset(),
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
        self_contained_mirror_variable_form=None,
        variable_form=None,
        zip_source=None,
        zip_input_format=None,
        comment_source=None,
        transform_stub_param_names=["_arg"],
        skip_lang_names=frozenset(),
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
        self_contained_mirror_variable_form=None,
        variable_form=None,
        zip_source=None,
        zip_input_format=None,
        comment_source=None,
        transform_stub_param_names=["_arg"],
        skip_lang_names=frozenset(),
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
        self_contained_mirror_variable_form=None,
        variable_form=None,
        zip_source=None,
        zip_input_format=None,
        comment_source=None,
        transform_stub_param_names=["_arg"],
        skip_lang_names=frozenset(),
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
        self_contained_mirror_variable_form=None,
        variable_form=None,
        zip_source=None,
        zip_input_format=None,
        comment_source=None,
        transform_stub_param_names=["_arg"],
        skip_lang_names=frozenset(),
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
        self_contained_mirror_variable_form=None,
        variable_form=None,
        zip_source=None,
        zip_input_format=None,
        comment_source=None,
        transform_stub_param_names=["_arg"],
        skip_lang_names=frozenset(),
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
        self_contained_mirror_variable_form=None,
        variable_form=None,
        zip_source=None,
        zip_input_format=None,
        comment_source=None,
        transform_stub_param_names=["_arg"],
        skip_lang_names=frozenset(),
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
        self_contained_mirror_variable_form=None,
        variable_form=None,
        zip_source=None,
        zip_input_format=None,
        comment_source=None,
        transform_stub_param_names=["_arg"],
        skip_lang_names=frozenset(),
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
        self_contained_mirror_variable_form=None,
        variable_form=None,
        zip_source=None,
        zip_input_format=None,
        comment_source=None,
        transform_stub_param_names=["_arg"],
        skip_lang_names=frozenset(),
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
        self_contained_mirror_variable_form=None,
        variable_form=None,
        zip_source=None,
        zip_input_format=None,
        comment_source=None,
        transform_stub_param_names=["_arg"],
        skip_lang_names=frozenset(),
    ),
    CallCaseConfig(
        case_dir_name="call_deep_dotted_transformed",
        target_function="app.client.fetch",
        parameter_names=["payload"],
        call_transform=lambda ctx: f"emit({ctx.call})",
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
        self_contained_mirror_variable_form=None,
        variable_form=None,
        zip_source=None,
        zip_input_format=None,
        comment_source=None,
        transform_stub_param_names=["_arg"],
        skip_lang_names=frozenset(),
    ),
    CallCaseConfig(
        case_dir_name="call_dotted_transform_stub",
        target_function="process",
        parameter_names=["value"],
        call_transform=lambda ctx: f"tracer.emit({ctx.call})",
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
        self_contained_mirror_variable_form=None,
        variable_form=None,
        zip_source=None,
        zip_input_format=None,
        comment_source=None,
        transform_stub_param_names=["_arg"],
        skip_lang_names=frozenset(),
    ),
    CallCaseConfig(
        case_dir_name="call_zip_values",
        target_function="process",
        parameter_names=["value"],
        call_transform=lambda ctx: f"emit({ctx.call}, {ctx.zipped})",
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
        self_contained_mirror_variable_form=None,
        variable_form=None,
        zip_source="---\n- true\n- false\n",
        zip_input_format=literalizer.InputFormat.YAML,
        comment_source=None,
        transform_stub_param_names=["_call", "_zip"],
        # Zig types the 2-parameter wrapper stub strongly while the
        # call stub returns ``void``; Groovy stubs the wrapper
        # object-style (``Map``) and rejects the positional 2-arg
        # call.  Neither can host this fixture, so skip them.
        skip_lang_names=frozenset({"Zig", "Groovy"}),
    ),
    CallCaseConfig(
        # Companion to ``call_zip_values`` exercising the
        # ``per_element=False`` path: the whole parsed ``zip_source``
        # value pairs with the single generated call.
        case_dir_name="call_zip_source_whole",
        target_function="process",
        parameter_names=["value"],
        call_transform=lambda ctx: f"emit({ctx.call}, {ctx.zipped})",
        transform_stub_names=["emit"],
        per_element=False,
        call_style_type=None,
        ref_declarations={},
        wrap_in_file=False,
        ref_case_per_language=False,
        consumable_refs=frozenset[str](),
        requires_call_returns_expression=True,
        requires_inline_multiline_dict_args=False,
        requires_standalone_wrapped_comments=False,
        self_contained_mirror_variable_form=None,
        variable_form=None,
        zip_source="--- true\n",
        zip_input_format=literalizer.InputFormat.YAML,
        comment_source=None,
        transform_stub_param_names=["_call", "_zip"],
        # Same wrapper-stub limitations as ``call_zip_values``.
        skip_lang_names=frozenset({"Zig", "Groovy"}),
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
        self_contained_mirror_variable_form=None,
        variable_form=None,
        zip_source=None,
        zip_input_format=None,
        comment_source=None,
        transform_stub_param_names=["_arg"],
        skip_lang_names=frozenset(),
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
        self_contained_mirror_variable_form=None,
        variable_form=None,
        zip_source=None,
        zip_input_format=None,
        comment_source=None,
        transform_stub_param_names=["_arg"],
        skip_lang_names=frozenset(),
    ),
    CallCaseConfig(
        case_dir_name="call_no_params_transform",
        target_function="process",
        parameter_names=[],
        call_transform=lambda ctx: f"emit({ctx.call})",
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
        self_contained_mirror_variable_form=None,
        variable_form=None,
        zip_source=None,
        zip_input_format=None,
        comment_source=None,
        transform_stub_param_names=["_arg"],
        skip_lang_names=frozenset(),
    ),
    CallCaseConfig(
        case_dir_name="call_no_params_dotted",
        target_function="throttler.check",
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
        self_contained_mirror_variable_form=None,
        variable_form=None,
        zip_source=None,
        zip_input_format=None,
        comment_source=None,
        transform_stub_param_names=["_arg"],
        skip_lang_names=frozenset(),
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
        self_contained_mirror_variable_form=None,
        variable_form=None,
        zip_source=None,
        zip_input_format=None,
        comment_source=None,
        transform_stub_param_names=["_arg"],
        skip_lang_names=frozenset(),
    ),
    CallCaseConfig(
        case_dir_name="call_no_params_curried_dotted",
        target_function="throttler.check",
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
        self_contained_mirror_variable_form=None,
        variable_form=None,
        zip_source=None,
        zip_input_format=None,
        comment_source=None,
        transform_stub_param_names=["_arg"],
        skip_lang_names=frozenset(),
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
        self_contained_mirror_variable_form=None,
        variable_form=None,
        zip_source=None,
        zip_input_format=None,
        comment_source=None,
        transform_stub_param_names=["_arg"],
        skip_lang_names=frozenset(),
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
        self_contained_mirror_variable_form=None,
        variable_form=None,
        zip_source=None,
        zip_input_format=None,
        comment_source=None,
        transform_stub_param_names=["_arg"],
        skip_lang_names=frozenset(),
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
        self_contained_mirror_variable_form=None,
        variable_form=None,
        zip_source=None,
        zip_input_format=None,
        comment_source=None,
        transform_stub_param_names=["_arg"],
        skip_lang_names=frozenset(),
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
        self_contained_mirror_variable_form=None,
        variable_form=None,
        zip_source=None,
        zip_input_format=None,
        comment_source=None,
        transform_stub_param_names=["_arg"],
        skip_lang_names=frozenset(),
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
        self_contained_mirror_variable_form=None,
        variable_form=None,
        zip_source=None,
        zip_input_format=None,
        comment_source=None,
        transform_stub_param_names=["_arg"],
        skip_lang_names=frozenset(),
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
        self_contained_mirror_variable_form=None,
        variable_form=None,
        zip_source=None,
        zip_input_format=None,
        comment_source=None,
        transform_stub_param_names=["_arg"],
        skip_lang_names=frozenset(),
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
        self_contained_mirror_variable_form=None,
        variable_form=None,
        zip_source=None,
        zip_input_format=None,
        comment_source=None,
        transform_stub_param_names=["_arg"],
        skip_lang_names=frozenset(),
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
        self_contained_mirror_variable_form=None,
        variable_form=None,
        zip_source=None,
        zip_input_format=None,
        comment_source=None,
        transform_stub_param_names=["_arg"],
        skip_lang_names=frozenset(),
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
        self_contained_mirror_variable_form=None,
        variable_form=None,
        zip_source=None,
        zip_input_format=None,
        comment_source=None,
        transform_stub_param_names=["_arg"],
        skip_lang_names=frozenset(),
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
        self_contained_mirror_variable_form=None,
        variable_form=None,
        zip_source=None,
        zip_input_format=None,
        comment_source=None,
        transform_stub_param_names=["_arg"],
        skip_lang_names=frozenset(),
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
        self_contained_mirror_variable_form=None,
        variable_form=None,
        zip_source=None,
        zip_input_format=None,
        comment_source=None,
        transform_stub_param_names=["_arg"],
        skip_lang_names=frozenset(),
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
        self_contained_mirror_variable_form=None,
        variable_form=None,
        zip_source=None,
        zip_input_format=None,
        comment_source=None,
        transform_stub_param_names=["_arg"],
        skip_lang_names=frozenset(),
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
        self_contained_mirror_variable_form=None,
        variable_form=None,
        zip_source=None,
        zip_input_format=None,
        comment_source=None,
        transform_stub_param_names=["_arg"],
        skip_lang_names=frozenset(),
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
        self_contained_mirror_variable_form=None,
        variable_form=None,
        zip_source=None,
        zip_input_format=None,
        comment_source=None,
        transform_stub_param_names=["_arg"],
        skip_lang_names=frozenset(),
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
        self_contained_mirror_variable_form=None,
        variable_form=None,
        zip_source=None,
        zip_input_format=None,
        comment_source=None,
        transform_stub_param_names=["_arg"],
        skip_lang_names=frozenset(),
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
        self_contained_mirror_variable_form=None,
        variable_form=None,
        zip_source=None,
        zip_input_format=None,
        comment_source=None,
        transform_stub_param_names=["_arg"],
        skip_lang_names=frozenset(),
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
        self_contained_mirror_variable_form=None,
        variable_form=None,
        zip_source=None,
        zip_input_format=None,
        comment_source=None,
        transform_stub_param_names=["_arg"],
        skip_lang_names=frozenset(),
    ),
    CallCaseConfig(
        case_dir_name="call_variable_form_new",
        target_function="make_widget",
        parameter_names=["count"],
        call_transform=None,
        transform_stub_names=[],
        per_element=False,
        call_style_type=None,
        ref_declarations={},
        wrap_in_file=True,
        ref_case_per_language=False,
        consumable_refs=frozenset[str](),
        requires_call_returns_expression=True,
        requires_inline_multiline_dict_args=False,
        requires_standalone_wrapped_comments=False,
        self_contained_mirror_variable_form=None,
        variable_form=literalizer.NewVariable(name="my_data"),
        zip_source=None,
        zip_input_format=None,
        comment_source=None,
        transform_stub_param_names=["_arg"],
        skip_lang_names=frozenset(),
    ),
    CallCaseConfig(
        # ``ExistingVariable`` counterpart of ``call_variable_form_new``.
        # The runner gates each language on
        # ``self_contained_mirror_variable_form``: only languages whose
        # ``ExistingVariable`` wrap-in-file output equals their
        # ``NewVariable`` form (functional ``let`` rebinds and dynamic
        # languages) get a golden; imperative compiled languages emit a
        # bare assignment to an undeclared name and are skipped (no
        # golden) rather than landing a non-compiling fixture.
        case_dir_name="call_variable_form_existing",
        target_function="make_widget",
        parameter_names=["count"],
        call_transform=None,
        transform_stub_names=[],
        per_element=False,
        call_style_type=None,
        ref_declarations={},
        wrap_in_file=True,
        ref_case_per_language=False,
        consumable_refs=frozenset[str](),
        requires_call_returns_expression=True,
        requires_inline_multiline_dict_args=False,
        requires_standalone_wrapped_comments=False,
        self_contained_mirror_variable_form=literalizer.NewVariable(
            name="my_data",
        ),
        variable_form=literalizer.ExistingVariable(name="my_data"),
        zip_source=None,
        zip_input_format=None,
        comment_source=None,
        transform_stub_param_names=["_arg"],
        skip_lang_names=frozenset(),
    ),
    CallCaseConfig(
        # 27-parameter call exercises the type-variable generators in
        # languages whose call-stub signatures use one type variable per
        # parameter past the 26-letter alphabet (Gleam ``a1``, Roc
        # ``a1``, Rust ``A1``).
        case_dir_name="call_27_parameters",
        target_function="process",
        parameter_names=[f"p{i}" for i in range(27)],
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
        self_contained_mirror_variable_form=None,
        variable_form=None,
        zip_source=None,
        zip_input_format=None,
        comment_source=None,
        transform_stub_param_names=["_arg"],
        skip_lang_names=frozenset(),
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
        self_contained_mirror_variable_form=None,
        variable_form=None,
        zip_source=None,
        zip_input_format=None,
        comment_source=None,
        transform_stub_param_names=["_arg"],
        skip_lang_names=frozenset(),
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
        self_contained_mirror_variable_form=None,
        variable_form=None,
        zip_source=None,
        zip_input_format=None,
        comment_source=None,
        transform_stub_param_names=["_arg"],
        skip_lang_names=frozenset(),
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
        self_contained_mirror_variable_form=None,
        variable_form=None,
        zip_source=None,
        zip_input_format=None,
        comment_source=None,
        transform_stub_param_names=["_arg"],
        skip_lang_names=frozenset(),
    ),
    *[
        CallCaseConfig(
            case_dir_name=f"call_{name}",
            target_function="throttler.check",
            parameter_names=["user_id", "ts"],
            # ``call_transform`` is only valid for the expression call
            # styles that can be wrapped.  The command/curried style
            # cannot host one, so that variant exercises the bare
            # curried call (and its per-argument formatting) without a
            # transform.
            call_transform=(
                None
                if issubclass(cls, literalizer.CommandCallStyle)
                else lambda ctx: f"emit({ctx.call})"
            ),
            transform_stub_names=(
                []
                if issubclass(cls, literalizer.CommandCallStyle)
                else ["emit"]
            ),
            per_element=True,
            call_style_type=cls,
            ref_declarations={},
            wrap_in_file=False,
            ref_case_per_language=False,
            consumable_refs=frozenset[str](),
            requires_call_returns_expression=not issubclass(
                cls, literalizer.CommandCallStyle
            ),
            requires_inline_multiline_dict_args=False,
            requires_standalone_wrapped_comments=False,
            self_contained_mirror_variable_form=None,
            variable_form=None,
            zip_source=None,
            zip_input_format=None,
            comment_source=None,
            transform_stub_param_names=["_arg"],
            skip_lang_names=frozenset(),
        )
        for name, cls in CALL_STYLE_VARIANTS
    ],
]


@dataclasses.dataclass(frozen=True)
class CallCase:
    """A parameterized call-style golden-file test case."""

    config: CallCaseConfig
    lang_cls: literalizer.LanguageCls
    expected_exception: type[Exception] | None


_SUBSTITUTION_CALL_STYLES = (
    literalizer.PositionalCallStyle,
    literalizer.KeywordCallStyle,
    literalizer.ObjectCallStyle,
)


@beartype
def _call_transform_style_unsupported(
    *,
    lang_cls: literalizer.LanguageCls,
    config: CallCaseConfig,
) -> bool:
    """Mirror ``_validate_call_preconditions``'s rejection of
    ``call_transform`` for non-substitution call styles.

    ``call_transform`` is only supported when the effective call style
    is positional, keyword, or object.  When ``call_style_type`` is set
    the test pins that style; otherwise the language's default
    (first-listed) style applies.
    """
    if config.call_transform is None:
        return False
    if config.call_style_type is not None:
        return not issubclass(
            config.call_style_type, _SUBSTITUTION_CALL_STYLES
        )
    default_style = next(iter(lang_cls.CallStyles)).value
    return not isinstance(default_style, _SUBSTITUTION_CALL_STYLES)


@beartype
def _wrapper_capability_skip_reason(
    *,
    lang_cls: literalizer.LanguageCls,
    config: CallCaseConfig,
) -> str | None:
    """Return why this language cannot host the case's wrapper stub.

    ``call_transform`` is now opaque to the core (no sentinel probe),
    so the harness -- which knows the wrapper names from
    ``transform_stub_names`` -- decides whether the stub it injects can
    compile in this language: a dotted wrapper (e.g. ``tracer.emit``)
    needs ``supports_dotted_call_stub``; a bare wrapper (e.g. ``emit``)
    needs ``has_free_function_calls``.  Languages that fail the check
    are skipped (no golden) rather than emitting a non-compiling
    fixture.
    """
    if lang_cls.__name__ in config.skip_lang_names:
        return (
            f"{lang_cls.__name__} cannot represent the "
            f"{config.case_dir_name} fixture"
        )
    for wrapper_name in config.transform_stub_names:
        if "." in wrapper_name:
            if not lang_cls.supports_dotted_call_stub:
                return (
                    f"{lang_cls.__name__} cannot declare a dotted call "
                    f"stub for {wrapper_name!r}"
                )
        elif not lang_cls.has_free_function_calls:
            return (
                f"{lang_cls.__name__} has no free function call syntax "
                f"for {wrapper_name!r}"
            )
    return None


@beartype
def _skip_if_wrapper_unsupported(
    *,
    config: CallCaseConfig,
    lang_cls: literalizer.LanguageCls,
    golden_path: Path,
) -> None:
    """Skip (and drop any stale golden) when this language cannot host
    the case's wrapper stub.
    """
    reason = _wrapper_capability_skip_reason(lang_cls=lang_cls, config=config)
    if reason is not None:
        golden_path.unlink(missing_ok=True)
        pytest.skip(reason)


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
    max_params = lang_cls.max_call_parameters
    variable_form_exc = _variable_form_expected_exception(
        lang_cls=lang_cls, variable_form=config.variable_form
    )
    if variable_form_exc is not None:
        return variable_form_exc
    innermost_target_function = config.target_function.split(sep=".")[-1]
    unsupported_signals = (
        parameter_count == 0 and not lang_cls.supports_zero_parameter_calls,
        parameter_count > max_params,
        config.requires_inline_multiline_dict_args
        and not lang_cls.supports_inline_multiline_dict_args,
        config.requires_call_returns_expression
        and not lang_cls.call_returns_expression,
        config.requires_standalone_wrapped_comments
        and not lang_cls.supports_standalone_comments_in_wrapped_calls,
        innermost_target_function in lang_cls.reserved_identifiers,
        _call_transform_style_unsupported(lang_cls=lang_cls, config=config),
    )
    if any(unsupported_signals):
        return UnsupportedCallShapeError
    return None


@beartype
def _variable_form_expected_exception(
    *,
    lang_cls: literalizer.LanguageCls,
    variable_form: literalizer.VariableForm | None,
) -> type[Exception] | None:
    """Mirror ``_validate_call_variable_form`` rejection paths."""
    if variable_form is None:
        return None
    if not lang_cls.supports_variable_names:
        return VariableNameNotSupportedError
    if not lang_cls.call_returns_expression:
        return UnsupportedCallShapeError
    if not lang_cls.supports_call_variable_binding:
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
            zip_source=config.zip_source,
            zip_input_format=config.zip_input_format,
            comment_source=config.comment_source,
            per_element=config.per_element,
            wrap_in_file=True,
            ref_case=effective_ref_case,
            variable_form=config.variable_form,
        )
    except CallArgNotSupportedError as exc:
        golden_path.unlink(missing_ok=True)
        pytest.skip(f"{lang_name} rejected call arg: {exc.reason}")
    mirror_form = config.self_contained_mirror_variable_form
    if mirror_form is not None:
        mirror_result = literalizer.literalize_call(
            source=yaml_string,
            input_format=literalizer.InputFormat.YAML,
            language=spec,
            target_function=config.target_function,
            parameter_names=config.parameter_names,
            call_transform=config.call_transform,
            zip_source=config.zip_source,
            zip_input_format=config.zip_input_format,
            comment_source=config.comment_source,
            per_element=config.per_element,
            wrap_in_file=True,
            ref_case=effective_ref_case,
            variable_form=mirror_form,
        )
        if wrap_result.code != mirror_result.code:
            golden_path.unlink(missing_ok=True)
            pytest.skip(
                f"{lang_name} {config.variable_form!r} call-binding is "
                f"not self-contained (a bare assignment to an undeclared "
                f"name); it diverges from the compilable "
                f"{mirror_form!r} form, so no golden is emitted",
            )
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
            zip_source=config.zip_source,
            zip_input_format=config.zip_input_format,
            comment_source=config.comment_source,
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
    except CallArgNotSupportedError as exc:
        golden_path.unlink(missing_ok=True)
        pytest.skip(f"{lang_name} rejected call arg: {exc.reason}")
    return _CallWithDeclarations(decl_results=decl_results, result=result)


@beartype
def _arg_values_for_stub(
    *,
    source_data: _Value,
    per_element: bool,
) -> Sequence[_Value]:
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
    version: enum.Enum,
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
        version=version,
    )
    _skip_if_wrapper_unsupported(
        config=config, lang_cls=lang_cls, golden_path=golden_path
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
    # Stubs for transform function names.  The parameter count matches
    # ``transform_stub_param_names`` so a wrapper called with the call
    # and the zipped value (two arguments) compiles in
    # fixed-parameter-count languages.
    for wrapper_name in config.transform_stub_names:
        wrapper_name_parts = tuple(wrapper_name.split(sep="."))
        body_stubs.extend(
            spec.format_call_stub(
                wrapper_name_parts,
                config.transform_stub_param_names,
                StubReturn.VOID,
                (),
            ),
        )
        preamble_stubs.extend(
            spec.format_call_preamble_stub(
                wrapper_name_parts,
                config.transform_stub_param_names,
                StubReturn.VOID,
                (),
            ),
        )
    # One library entry point assembles the declarations and the call
    # into a single coherent file: it recomputes the body preamble
    # across the union of types in every declaration *and* the call,
    # recomputes the data-dependent header block over their combined
    # source data (so a single block covers every type, replacing the
    # old multi-line filter heuristic), wraps the pieces via
    # ``wrap_calls_with_declarations``, and places the deduplicated
    # preamble in front.  The call-stub lines this harness synthesizes
    # for the otherwise-undefined target/transform names are folded in
    # as the ``extra_*`` arguments.
    composed = _literalize_call_with_declarations(
        language=spec,
        declarations=decl_results,
        call=result,
        extra_body_preamble=tuple(body_stubs),
        extra_preamble=tuple(preamble_stubs),
    )
    # Anchor the public ``literalize_call(bound_refs=...)`` path to this
    # golden-verified composer output.  ``bound_refs`` injects only the
    # target stub, so the equivalence holds exactly when this case
    # synthesizes no extra (transform-wrapper) stubs and binds no
    # variable; those cases are exercised through the composer call
    # directly above.
    if (
        config.ref_declarations
        and config.call_transform is None
        and not config.transform_stub_names
        and config.variable_form is None
    ):
        bound = literalizer.literalize_call(
            source=yaml_string,
            input_format=literalizer.InputFormat.YAML,
            language=spec,
            target_function=config.target_function,
            parameter_names=config.parameter_names,
            zip_source=config.zip_source,
            zip_input_format=config.zip_input_format,
            comment_source=config.comment_source,
            per_element=config.per_element,
            wrap_in_file=True,
            ref_case=effective_ref_case,
            consumable_refs=config.consumable_refs,
            bound_refs={
                ref_name: json.loads(s=ref_source)
                for ref_name, ref_source in config.ref_declarations.items()
            },
        )
        divergence_message = (
            "literalize_call(bound_refs=...) diverged from the shared "
            f"call/declaration composition for {lang_cls.__name__} / "
            f"{config.case_dir_name}"
        )
        assert bound.code == composed.code, divergence_message  # noqa: S101
    check_golden(
        file_regression=file_regression,
        contents=composed.code + "\n",
        extension=lang_cls.extension,
        newline="",
        golden_path=golden_path,
    )
