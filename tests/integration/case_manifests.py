"""Load and validate case-local golden coverage manifests."""

from __future__ import annotations

import dataclasses
import functools
import string
import tomllib
from collections.abc import Mapping  # noqa: TC003
from pathlib import Path  # noqa: TC003
from typing import Annotated, Literal

from beartype import beartype
from pydantic import BaseModel, Field, ValidationError

import literalizer
from literalizer._types import ValueInput  # noqa: TC001

from .case_inputs import CaseInput, infer_case_input
from .variant_axis_names import KNOWN_VARIANT_AXES

MANIFEST_NAME = "case.toml"

type VariableFormName = Literal["new", "existing", "both"]
type CallVariableFormName = Literal["new", "existing"]
type CollectionLayoutName = Literal["compact", "multiline"]
type SuiteName = Literal["base", "combined"]
type CallStyleName = Literal["keyword", "positional", "object", "command"]
type InputFormatName = Literal["json", "json5", "toml", "yaml"]
type OwnerName = Literal[
    "literalize-call",
    "literalize-ref",
    "literalize-ref-default",
    "new-variable-kebab",
    "new-variable-prime",
    "variant",
]

CALL_OWNER: OwnerName = "literalize-call"

CALL_TRANSFORM_PLACEHOLDERS = frozenset({"call", "zipped"})
"""Every name a ``call_transform`` template may substitute."""


def _empty_suites() -> list[SuiteName]:
    """Return a typed empty suite list for the validation model."""
    return []


_CALL_VARIABLE_FORMS_BY_NAME: Mapping[
    CallVariableFormName,
    literalizer.NewVariable | literalizer.ExistingVariable,
] = {
    "new": literalizer.NewVariable(name="my_data", modifiers=frozenset()),
    "existing": literalizer.ExistingVariable(name="my_data"),
}

_VARIABLE_FORMS_BY_NAME: Mapping[
    VariableFormName, literalizer.VariableForm
] = {
    "new": _CALL_VARIABLE_FORMS_BY_NAME["new"],
    "existing": _CALL_VARIABLE_FORMS_BY_NAME["existing"],
    "both": literalizer.BothVariableForms(
        name="my_data",
        modifiers=frozenset(),
    ),
}

_CALL_STYLE_TYPES_BY_NAME: Mapping[
    CallStyleName, type[literalizer.CallStyle]
] = {
    "keyword": literalizer.KeywordCallStyle,
    "positional": literalizer.PositionalCallStyle,
    "object": literalizer.ObjectCallStyle,
    "command": literalizer.CommandCallStyle,
}

_INPUT_FORMATS_BY_NAME: Mapping[InputFormatName, literalizer.InputFormat] = {
    "json": literalizer.InputFormat.JSON,
    "json5": literalizer.InputFormat.JSON5,
    "toml": literalizer.InputFormat.TOML,
    "yaml": literalizer.InputFormat.YAML,
}


class CaseManifestError(ValueError):
    """A case manifest is invalid or internally inconsistent."""


class RenderContext(
    BaseModel,
    arbitrary_types_allowed=True,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """Simple render arguments declared by a case rather than a runner."""

    variable_form: VariableFormName = "new"
    collection_layout: CollectionLayoutName | None = None
    pre_indent_level: Annotated[int, Field(ge=0)] = 0
    record_null_substitutions: Mapping[str, ValueInput] | None = None


class ManifestVariant(
    BaseModel,
    arbitrary_types_allowed=True,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """One input's participation in a named, typed variant axis."""

    axis: Annotated[str, Field(min_length=1)]
    suffix: str = ""
    context: RenderContext = Field(default_factory=RenderContext)


def _empty_variants() -> list[ManifestVariant]:
    """Return a typed empty variant list for the validation model."""
    return []


def _empty_names() -> list[str]:
    """Return a typed empty name list for the validation model."""
    return []


def _single_stub_parameter() -> list[str]:
    """Return the default wrapper-stub parameter names."""
    return ["_arg"]


def _empty_sources() -> dict[str, str]:
    """Return a typed empty name-to-source mapping."""
    return {}


class _CallData(
    BaseModel,
    arbitrary_types_allowed=True,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """Strict representation of a manifest's ``[call]`` table.

    Every field names data only: enum- and type-valued arguments are
    spelled as strings and resolved by :func:`_resolve_call`, and
    ``call_transform`` is a template over
    :data:`CALL_TRANSFORM_PLACEHOLDERS` rather than evaluated code.
    """

    target_function: str
    parameter_names: list[str]
    per_element: bool
    call_transform: str | None = None
    transform_stub_names: list[str] = Field(default_factory=_empty_names)
    transform_stub_param_names: list[str] = Field(
        default_factory=_single_stub_parameter,
    )
    call_style: CallStyleName | None = None
    wrap_in_file: bool = False
    ref_case_per_language: bool = False
    ref_declarations: dict[str, str] = Field(default_factory=_empty_sources)
    consumable_refs: list[str] = Field(default_factory=_empty_names)
    unknown_ref_names: list[str] = Field(default_factory=_empty_names)
    extra_ref_value_sources: dict[str, str] = Field(
        default_factory=_empty_sources,
    )
    zip_source: str | None = None
    zip_input_format: InputFormatName | None = None
    comment_source: list[str] | None = None
    input_root_key: str | None = None
    variable_form: CallVariableFormName | None = None
    self_contained_mirror_variable_form: CallVariableFormName | None = None
    requires_call_returns_expression: bool = False
    requires_inline_multiline_dict_args: bool = False
    requires_standalone_wrapped_comments: bool = False
    requires_dict_literal_as_free_expression: bool = False
    requires_heterogeneous_dict_values: bool = False
    variant_only: bool = False

    def validate_consistency(self) -> None:
        """Validate the ``call_transform`` template's placeholders."""
        if self.call_transform is None:
            return
        for _, field_name, _, _ in string.Formatter().parse(
            format_string=self.call_transform
        ):
            if field_name is not None and (
                field_name not in CALL_TRANSFORM_PLACEHOLDERS
            ):
                msg = (
                    f"unknown call_transform placeholder {field_name!r}; "
                    f"expected one of {sorted(CALL_TRANSFORM_PLACEHOLDERS)}"
                )
                raise ValueError(msg)


class _CaseManifestData(
    BaseModel,
    arbitrary_types_allowed=True,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """Strict representation of the data read directly from TOML."""

    schema_version: Literal[1]
    input: str | None = None
    suites: list[SuiteName] = Field(default_factory=_empty_suites)
    owner: OwnerName | None = None
    base_context: RenderContext = Field(default_factory=RenderContext)
    variants: list[ManifestVariant] = Field(default_factory=_empty_variants)
    call: _CallData | None = None

    def _validate_call(self) -> None:
        """Validate the ``[call]`` table against its declared owner."""
        if self.owner == CALL_OWNER and self.call is None:
            msg = f"owner {CALL_OWNER!r} requires a [call] table"
            raise ValueError(msg)
        if self.call is None:
            return
        if self.owner != CALL_OWNER:
            msg = f"a [call] table requires owner = {CALL_OWNER!r}"
            raise ValueError(msg)
        self.call.validate_consistency()

    def validate_consistency(self) -> None:
        """Validate relationships that span manifest fields."""
        self._validate_call()
        if len(self.suites) != len(set(self.suites)):
            msg = "suites contains a duplicate entry"
            raise ValueError(msg)
        if self.suites and self.owner is not None:
            msg = "suites and owner are mutually exclusive"
            raise ValueError(msg)
        if not self.suites and self.owner is None:
            msg = "declare suites or a specialized owner"
            raise ValueError(msg)
        if (
            "base_context" in self.model_fields_set
            and "base" not in self.suites
        ):
            msg = "base_context requires participation in the base suite"
            raise ValueError(msg)

        logical_cases = [(entry.axis, entry.suffix) for entry in self.variants]
        if len(logical_cases) != len(set(logical_cases)):
            msg = "duplicate logical variant case"
            raise ValueError(msg)
        for entry in self.variants:
            if entry.axis not in KNOWN_VARIANT_AXES:
                msg = f"unknown variant axis {entry.axis!r}"
                raise ValueError(msg)


@dataclasses.dataclass(frozen=True, kw_only=True)
class CallTransform:
    """A validated ``call_transform`` template, applied per call.

    The template substitutes only :data:`CALL_TRANSFORM_PLACEHOLDERS`,
    so a manifest describes the wrapper text without carrying code.
    """

    template: str

    @beartype
    def __call__(self, context: literalizer.CallContext, /) -> str:
        """Return the transformed text for one generated call."""
        return self.template.format(
            call=context.call,
            zipped=context.zipped,
        )


@dataclasses.dataclass(frozen=True, kw_only=True)
class CallCaseSpec:
    """Everything a case declares about driving ``literalize_call``.

    ``ref_declarations`` maps a ``{"$ref": "name"}`` marker in the case
    input to a JSON source rendered as a variable declaration via
    :func:`literalizer.literalize`, emitted before the call so the
    resulting file is self-contained.

    With ``ref_case_per_language``, the harness picks each language's
    first-listed ``IdentifierCases`` member as the ``ref_case``,
    converts every ``ref_declarations`` key to that case, and passes the
    same case to :func:`literalize_call` so the declaration site and the
    call site agree on identifier spelling.
    """

    case_dir_name: str
    target_function: str
    parameter_names: tuple[str, ...]
    per_element: bool
    call_transform: CallTransform | None
    transform_stub_names: tuple[str, ...]
    # Parameter names used when stubbing each ``transform_stub_names``
    # wrapper.  The length sets how many parameters the wrapper takes,
    # so a transform that calls the wrapper with the call *and* the
    # zipped value (two arguments) compiles in fixed-parameter-count
    # languages.
    transform_stub_param_names: tuple[str, ...]
    call_style_type: type[literalizer.CallStyle] | None
    # When True, drive ``literalize_call(..., wrap_in_file=True)``
    # directly instead of wrapping manually with injected stubs.
    wrap_in_file: bool
    ref_case_per_language: bool
    ref_declarations: Mapping[str, str]
    # Names from ``ref_declarations`` (in their original case) that
    # ``literalize_call`` may treat as consumable.  Empty means no ref
    # is consumed.
    consumable_refs: frozenset[str]
    # Refs that receive declarations in the self-contained golden file
    # but are intentionally omitted from ``ref_values``.  This exercises
    # the historical unknown-ref preamble behavior without leaving the
    # rendered call's identifier undefined for fixture compilation.
    unknown_ref_names: frozenset[str]
    # Additional JSON sources used to seed ``ref_values`` without
    # emitting declarations.  This covers mappings whose names are not
    # referenced by the input while keeping generated fixtures free of
    # unused declarations.
    extra_ref_value_sources: Mapping[str, str]
    # Companion source whose parsed top-level elements pair
    # positionally with the generated calls and are exposed on
    # ``CallContext.zipped``.  Requires ``call_transform``.  Parsed
    # with ``zip_input_format``.
    zip_source: str | None
    zip_input_format: literalizer.InputFormat | None
    # Trailing source-code comments, one per generated call, paired
    # positionally and emitted after the statement terminator using the
    # language's comment syntax.  An empty entry emits no comment.
    comment_source: tuple[str, ...] | None
    # TOML documents necessarily parse to a top-level table.  When set,
    # select this table entry as the root value used for call rendering
    # after parsing.  Other formats normally leave this as ``None``.
    input_root_key: str | None
    # When set, drive ``literalize_call(..., variable_form=...)`` to
    # exercise the call-binding output mode.  Only meaningful with
    # ``per_element=False`` and (typically) ``wrap_in_file=True`` so
    # the generated file is self-contained around the binding.
    variable_form: (
        literalizer.NewVariable | literalizer.ExistingVariable | None
    )
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
    self_contained_mirror_variable_form: (
        literalizer.NewVariable | literalizer.ExistingVariable | None
    )
    requires_call_returns_expression: bool
    requires_inline_multiline_dict_args: bool
    requires_standalone_wrapped_comments: bool
    # When ``True`` the case splices a dict/map ``$zipped`` value into
    # the ``call_transform`` as a free expression.  Languages whose map
    # literal needs a typed left-hand side
    # (``supports_dict_literal_as_free_expression=False``) cannot host
    # the resulting fixture and are skipped (no golden) instead of
    # emitting non-compiling output.
    requires_dict_literal_as_free_expression: bool
    # When ``True``, only languages whose default configuration can
    # represent heterogeneous dict values participate in the case.
    requires_heterogeneous_dict_values: bool
    # When ``True`` the case is driven only by the call *variant*
    # suite, so the default per-language call matrix needs no
    # case-specific opt-out.
    variant_only: bool


@dataclasses.dataclass(frozen=True, kw_only=True)
class CaseManifest:
    """Validated coverage and input metadata for one case directory."""

    path: Path
    case_dir: Path
    schema_version: Literal[1]
    input: CaseInput
    suites: frozenset[SuiteName]
    owner: OwnerName | None
    base_context: RenderContext
    variants: tuple[ManifestVariant, ...]
    call: CallCaseSpec | None


@beartype
def variable_form_for_context(
    *, context: RenderContext
) -> literalizer.VariableForm:
    """Translate a validated manifest variable-form name to the API
    type.
    """
    return _VARIABLE_FORMS_BY_NAME[context.variable_form]


@beartype
def _resolve_call(*, data: _CallData, case_dir_name: str) -> CallCaseSpec:
    """Resolve one validated ``[call]`` table to typed arguments."""
    mirror_form_name = data.self_contained_mirror_variable_form
    return CallCaseSpec(
        case_dir_name=case_dir_name,
        target_function=data.target_function,
        parameter_names=tuple(data.parameter_names),
        per_element=data.per_element,
        call_transform=(
            None
            if data.call_transform is None
            else CallTransform(template=data.call_transform)
        ),
        transform_stub_names=tuple(data.transform_stub_names),
        transform_stub_param_names=tuple(data.transform_stub_param_names),
        call_style_type=(
            None
            if data.call_style is None
            else _CALL_STYLE_TYPES_BY_NAME[data.call_style]
        ),
        wrap_in_file=data.wrap_in_file,
        ref_case_per_language=data.ref_case_per_language,
        ref_declarations=dict(data.ref_declarations),
        consumable_refs=frozenset(data.consumable_refs),
        unknown_ref_names=frozenset(data.unknown_ref_names),
        extra_ref_value_sources=dict(data.extra_ref_value_sources),
        zip_source=data.zip_source,
        zip_input_format=(
            None
            if data.zip_input_format is None
            else _INPUT_FORMATS_BY_NAME[data.zip_input_format]
        ),
        comment_source=(
            None if data.comment_source is None else tuple(data.comment_source)
        ),
        input_root_key=data.input_root_key,
        variable_form=(
            None
            if data.variable_form is None
            else _CALL_VARIABLE_FORMS_BY_NAME[data.variable_form]
        ),
        self_contained_mirror_variable_form=(
            None
            if mirror_form_name is None
            else _CALL_VARIABLE_FORMS_BY_NAME[mirror_form_name]
        ),
        requires_call_returns_expression=(
            data.requires_call_returns_expression
        ),
        requires_inline_multiline_dict_args=(
            data.requires_inline_multiline_dict_args
        ),
        requires_standalone_wrapped_comments=(
            data.requires_standalone_wrapped_comments
        ),
        requires_dict_literal_as_free_expression=(
            data.requires_dict_literal_as_free_expression
        ),
        requires_heterogeneous_dict_values=(
            data.requires_heterogeneous_dict_values
        ),
        variant_only=data.variant_only,
    )


def _fail(*, path: Path, message: str) -> CaseManifestError:
    """Build a manifest error containing its source path."""
    return CaseManifestError(f"{path}: {message}")


def _load_manifest_data(*, path: Path) -> _CaseManifestData:
    """Parse and structurally validate one manifest file."""
    try:
        raw = tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        raise _fail(path=path, message=f"invalid TOML: {exc}") from exc

    try:
        data = _CaseManifestData.model_validate(obj=raw)
        data.validate_consistency()
    except (ValidationError, ValueError) as exc:
        raise _fail(path=path, message=str(object=exc)) from exc
    return data


@functools.cache
@beartype
def load_case_manifest(case_dir: Path) -> CaseManifest:
    """Return one fully validated ``case.toml`` manifest."""
    path = case_dir / MANIFEST_NAME
    if not path.is_file():
        raise _fail(path=path, message="manifest is missing")
    data = _load_manifest_data(path=path)
    try:
        input_info = infer_case_input(
            case_dir=case_dir,
            input_name=data.input,
        )
    except ValueError as exc:
        raise _fail(path=path, message=str(object=exc)) from exc

    return CaseManifest(
        path=path,
        case_dir=case_dir,
        schema_version=data.schema_version,
        input=input_info,
        suites=frozenset(data.suites),
        owner=data.owner,
        base_context=data.base_context,
        variants=tuple(data.variants),
        call=(
            None
            if data.call is None
            else _resolve_call(data=data.call, case_dir_name=case_dir.name)
        ),
    )


@beartype
def case_input(*, case_dir: Path) -> CaseInput:
    """Return the input declared by the case-local manifest."""
    return load_case_manifest(case_dir=case_dir).input


@functools.cache
@beartype
def load_case_manifests(cases_dir: Path) -> tuple[CaseManifest, ...]:
    """Load every case manifest in stable directory-name order."""
    case_dirs = sorted(path for path in cases_dir.iterdir() if path.is_dir())
    return tuple(
        load_case_manifest(case_dir=case_dir) for case_dir in case_dirs
    )


@functools.cache
@beartype
def call_case_specs(cases_dir: Path) -> tuple[CallCaseSpec, ...]:
    """Return every declared ``literalize_call`` case configuration."""
    return tuple(
        manifest.call
        for manifest in load_case_manifests(cases_dir=cases_dir)
        if manifest.call is not None
    )


@functools.cache
@beartype
def case_manifests_by_name(cases_dir: Path) -> Mapping[str, CaseManifest]:
    """Return the shared manifest inventory keyed by case directory
    name.
    """
    return {
        manifest.case_dir.name: manifest
        for manifest in load_case_manifests(cases_dir=cases_dir)
    }
