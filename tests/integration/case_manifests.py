"""Load and validate case-local golden coverage manifests."""

from __future__ import annotations

import dataclasses
import functools
import string
import tomllib
from collections.abc import Callable, Mapping  # noqa: TC003
from pathlib import Path  # noqa: TC003
from typing import Annotated, Literal, Self, get_args

from beartype import beartype
from pydantic import (
    BaseModel,
    BeforeValidator,
    Field,
    InstanceOf,
    ValidationError,
    ValidationInfo,
    model_validator,
)

import literalizer
from literalizer._types import ValueInput  # noqa: TC001
from literalizer.languages import ALL_LANGUAGES

from .case_inputs import CaseInput, infer_case_input
from .language_metadata import language_metadata
from .language_specs import make_spec
from .suite_gates import SuiteGate, gates_admit, no_gates, validate_gate_names
from .variant_axis_names import KNOWN_VARIANT_AXES

MANIFEST_NAME = "case.toml"

type VariableFormName = Literal["new", "existing", "both"]
type CollectionLayoutName = Literal["compact", "multiline"]
type SuiteName = Literal["base", "combined"]
type VariantCapabilityName = Literal[
    "collection_comments",
    "empty_sibling_sequence_type_hints",
    "special_floats",
]
type OwnerName = Literal[
    "literalize-call",
    "literalize-ref",
    "literalize-ref-default",
    "new-variable-kebab",
    "new-variable-prime",
    "variant",
]

# Spelled as an assignment rather than a ``type`` statement so the
# accepted names can be read back out with ``get_args``.
_CaseRoleNameLiteral = Literal[
    "heterogeneous-strategy-default-input",
    "heterogeneous-strategy-tuple-input",
    "indent-input",
    "no-variable-form-input",
    "pre-indent-comment-scalar-input",
    "pre-indent-container-input",
    "statement-terminator-input",
]

type CaseRoleName = _CaseRoleNameLiteral
"""Every load-bearing role a case may declare.

A role names the part an input plays in a runner that renders a chosen
fixture rather than the whole inventory.  The case declares the role, so
its directory name stays a single source of truth on disk and reading
the case tells you it is load-bearing.
"""

CASE_ROLE_NAMES: frozenset[CaseRoleName] = frozenset(
    get_args(tp=_CaseRoleNameLiteral),
)

HETEROGENEOUS_STRATEGY_DEFAULT_ROLE: CaseRoleName = (
    "heterogeneous-strategy-default-input"
)
INDENT_ROLE: CaseRoleName = "indent-input"
NO_VARIABLE_FORM_ROLE: CaseRoleName = "no-variable-form-input"
PRE_INDENT_COMMENT_SCALAR_ROLE: CaseRoleName = (
    "pre-indent-comment-scalar-input"
)
PRE_INDENT_CONTAINER_ROLE: CaseRoleName = "pre-indent-container-input"
STATEMENT_TERMINATOR_ROLE: CaseRoleName = "statement-terminator-input"

CALL_OWNER: OwnerName = "literalize-call"

REF_OWNER: OwnerName = "literalize-ref"
REF_DEFAULT_OWNER: OwnerName = "literalize-ref-default"

_REF_OWNERS: frozenset[OwnerName] = frozenset({REF_OWNER, REF_DEFAULT_OWNER})

KEBAB_NEW_VARIABLE_OWNER: OwnerName = "new-variable-kebab"
PRIMED_NEW_VARIABLE_OWNER: OwnerName = "new-variable-prime"

CALL_TRANSFORM_PLACEHOLDERS = frozenset({"call", "zipped"})
"""Every name a ``call_transform`` template may substitute."""


def _empty_suites() -> list[SuiteName]:
    """Return a typed empty suite list for the validation model."""
    return []


def _empty_capabilities() -> list[VariantCapabilityName]:
    """Return a typed empty capability list for the validation model."""
    return []


def _empty_roles() -> list[CaseRoleName]:
    """Return a typed empty role list for the validation model."""
    return []


_CALL_VARIABLE_FORMS_BY_NAME: Mapping[
    str,
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

_CALL_STYLE_TYPES_BY_NAME: Mapping[str, type[literalizer.CallStyle]] = {
    "keyword": literalizer.KeywordCallStyle,
    "positional": literalizer.PositionalCallStyle,
    "object": literalizer.ObjectCallStyle,
    "command": literalizer.CommandCallStyle,
}

_IDENTIFIER_CASES_BY_NAME: Mapping[str, literalizer.IdentifierCase] = {
    member.value: member for member in literalizer.IdentifierCase
}

_INPUT_FORMATS_BY_NAME: Mapping[str, literalizer.InputFormat] = {
    "json": literalizer.InputFormat.JSON,
    "json5": literalizer.InputFormat.JSON5,
    "toml": literalizer.InputFormat.TOML,
    "yaml": literalizer.InputFormat.YAML,
}


class CaseManifestError(ValueError):
    """A case manifest is invalid or internally inconsistent."""


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


@beartype
def _name_resolver[NamedT](
    *, values_by_name: Mapping[str, NamedT]
) -> Callable[[object], object]:
    """Return a callable resolving a manifest name to its value.

    Names are resolved before the strict-mode type check, so a manifest
    spells a resolved argument as a string while the model field holds
    the ``literalizer`` type itself.  Anything that is not a string is
    passed through for that strict check to reject.
    """

    def resolve(value: object, /) -> object:
        """Resolve one manifest name, or list the accepted names."""
        if not isinstance(value, str):
            return value
        if value not in values_by_name:
            accepted = ", ".join(repr(name) for name in sorted(values_by_name))
            msg = f"Input should be {accepted}"
            raise ValueError(msg)
        return values_by_name[value]

    return resolve


def _to_call_transform(value: object, /) -> object:
    """Build a :class:`CallTransform` from a validated template."""
    if not isinstance(value, str):
        return value
    for _, field_name, _, _ in string.Formatter().parse(format_string=value):
        if field_name is not None and (
            field_name not in CALL_TRANSFORM_PLACEHOLDERS
        ):
            msg = (
                f"unknown call_transform placeholder {field_name!r}; "
                f"expected one of {sorted(CALL_TRANSFORM_PLACEHOLDERS)}"
            )
            raise ValueError(msg)
    return CallTransform(template=value)


# A manifest spells these as TOML arrays, which ``strict=False`` allows
# to be read as the immutable containers the harness holds.  The item
# type is still checked.
type StringTuple = Annotated[tuple[str, ...], Field(strict=False)]
type StringFrozenSet = Annotated[frozenset[str], Field(strict=False)]
_LANGUAGES_BY_NAME = {
    lang_cls.__name__: lang_cls for lang_cls in ALL_LANGUAGES
}
type ManifestLanguage = Annotated[
    literalizer.LanguageCls,
    BeforeValidator(func=_name_resolver(values_by_name=_LANGUAGES_BY_NAME)),
]
type ManifestLanguages = Annotated[
    tuple[ManifestLanguage, ...],
    Field(strict=False),
]
type CallTransformTemplate = Annotated[
    InstanceOf[CallTransform], BeforeValidator(func=_to_call_transform)
]
type CallStyleType = Annotated[
    type[literalizer.CallStyle],
    BeforeValidator(
        func=_name_resolver(values_by_name=_CALL_STYLE_TYPES_BY_NAME)
    ),
]
type CallInputFormat = Annotated[
    literalizer.InputFormat,
    BeforeValidator(
        func=_name_resolver(values_by_name=_INPUT_FORMATS_BY_NAME)
    ),
]
type CallVariableForm = Annotated[
    InstanceOf[literalizer.NewVariable]
    | InstanceOf[literalizer.ExistingVariable],
    BeforeValidator(
        func=_name_resolver(values_by_name=_CALL_VARIABLE_FORMS_BY_NAME)
    ),
]
type RefIdentifierCase = Annotated[
    literalizer.IdentifierCase,
    BeforeValidator(
        func=_name_resolver(values_by_name=_IDENTIFIER_CASES_BY_NAME)
    ),
]


# A field default here is what a manifest means by leaving the key
# out, rather than a value a caller may lean on: a manifest supplies
# only what it has an opinion about, and TOML cannot spell the
# ``None`` many of these values take.
class RenderContext(  # noqa: NOD001
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


# Defaults stand in for omitted keys, as above.
class ManifestVariant(  # noqa: NOD001
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
    # The language capabilities this input needs in order to render at
    # all.  A variant whose language lacks one of them is skipped (no
    # golden) rather than emitting output the language cannot express.
    requires: list[VariantCapabilityName] = Field(
        default_factory=_empty_capabilities,
    )

    @model_validator(mode="after")
    def _validate_requirements(self) -> ManifestVariant:
        """Reject a capability named more than once."""
        if len(self.requires) != len(set(self.requires)):
            msg = "requires contains a duplicate entry"
            raise ValueError(msg)
        return self


# Defaults stand in for omitted keys, as above.
class LanguageSelection(  # noqa: NOD001
    BaseModel,
    arbitrary_types_allowed=True,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """How one manifest table narrows the languages it renders under.

    ``gates`` names the property the narrowing follows from, so a case
    that a language qualifies for by gaining that property picks it up
    without being edited.  ``languages`` names the languages outright,
    for a narrowing no property expresses -- a syntax quirk only one
    language has, or a deliberate one-language sample of a rendering
    that does not vary -- and pairs with ``languages_reason``, which
    says which of those it is.  Naming both would state the same
    narrowing twice, so a table declares at most one.

    A gate reads the language default spec: a case selects languages,
    where a variant axis selects the specs its overrides build.
    """

    languages: ManifestLanguages = ()
    languages_reason: Annotated[str, Field(min_length=1)] | None = None
    gates: list[SuiteGate] = Field(default_factory=no_gates)

    @model_validator(mode="after")
    def _validate_language_selection(self) -> Self:
        """Reject a narrowing stated twice, or stated without a
        reason.
        """
        if self.languages and self.gates:
            msg = "declare either languages or gates, not both"
            raise ValueError(msg)
        if bool(self.languages) != (self.languages_reason is not None):
            msg = "languages and languages_reason require each other"
            raise ValueError(msg)
        validate_gate_names(subject="gates", gates=self.gates)
        return self

    @beartype
    def admits_language(self, *, lang_cls: literalizer.LanguageCls) -> bool:
        """Return whether this narrowing selects *lang_cls*."""
        if self.languages:
            return lang_cls in self.languages
        return gates_admit(
            gates=self.gates,
            lang_cls=lang_cls,
            metadata=language_metadata(language_id=lang_cls.language_id),
            spec=make_spec(lang_cls=lang_cls),
        )


def _empty_variants() -> list[ManifestVariant]:
    """Return a typed empty variant list for the validation model."""
    return []


class CallManifestVariant(
    BaseModel,
    arbitrary_types_allowed=True,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """One call case's participation in a named, typed variant axis.

    A call golden is named by the language variant alone, so a call
    case names an axis and nothing else.
    """

    axis: Annotated[str, Field(min_length=1)]

    @model_validator(mode="after")
    def _validate_known_axis(self) -> CallManifestVariant:
        """Reject an axis name no expansion answers to."""
        if self.axis not in KNOWN_VARIANT_AXES:
            msg = f"unknown variant axis {self.axis!r}"
            raise ValueError(msg)
        return self


def _empty_call_variants() -> list[CallManifestVariant]:
    """Return a typed empty call-variant list for the validation
    model.
    """
    return []


def _empty_names() -> tuple[str, ...]:
    """Return a typed empty name tuple for the validation model."""
    return ()


def _empty_name_set() -> frozenset[str]:
    """Return a typed empty name set for the validation model."""
    return frozenset()


def _single_stub_parameter() -> tuple[str, ...]:
    """Return the default wrapper-stub parameter names."""
    return ("_arg",)


def _empty_sources() -> dict[str, str]:
    """Return a typed empty name-to-source mapping."""
    return {}


class _OwnedCaseSpec(
    BaseModel,
    arbitrary_types_allowed=True,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """Base for an owner-scoped manifest table that knows its case.

    The directory name identifies the case on disk rather than being
    manifest data, so :func:`load_case_manifest` supplies it through the
    validation context instead of a second construction step.
    """

    # Supplied by the loader through the validation context rather than
    # by the manifest, so a case's directory name stays a single source
    # of truth on disk.
    case_dir_name: str

    @model_validator(mode="before")
    @classmethod
    def _add_case_dir_name(
        cls,
        data: Mapping[str, object],
        info: ValidationInfo,
    ) -> Mapping[str, object]:
        """Add the owning case directory name from the load context."""
        context: Mapping[str, str] = info.context or {}
        return {**data, "case_dir_name": context["case_dir_name"]}


class RefCaseSpec(  # noqa: NOD001
    _OwnedCaseSpec,
    LanguageSelection,
    frozen=True,
):
    """Everything a case declares about driving a ``$ref`` golden.

    When *value_sources* is supplied, each entry maps a
    ``{ref_key: name}`` marker in the case input to a JSON source whose
    value seeds ``bound_refs`` on the :func:`literalizer.literalize`
    call and the matching ref stub.  Without it the harness keeps its
    historical behavior: refs render with no value-type knowledge and
    stubs are dict shaped.

    When *ref_case_override* is set, the case forces that identifier
    case for the ``ref_case`` argument of :func:`literalizer.literalize`
    instead of using the language's default (``identifier_cases[0]``).
    Discovery skips any language whose ``supported_ref_cases`` does not
    include the override.
    """

    ref_key: str = "$ref"
    variable_form: VariableFormName = "new"
    collection_layout: CollectionLayoutName = "compact"
    pre_indent_level: int = 0
    heterogeneous_strategy: str | None = None
    ref_case_override: RefIdentifierCase | None = None
    value_sources: dict[str, str] = Field(default_factory=_empty_sources)
    extra_ref_value_sources: dict[str, str] = Field(
        default_factory=_empty_sources,
    )
    explicit_ref_value_sources: dict[str, str] = Field(
        default_factory=_empty_sources,
    )

    def resolved_variable_form(self) -> literalizer.VariableForm:
        """Return the public API variable form selected by the
        manifest.
        """
        return _VARIABLE_FORMS_BY_NAME[self.variable_form]


class CallCaseSpec(  # noqa: NOD001
    _OwnedCaseSpec,
    LanguageSelection,
    frozen=True,
):
    """Everything a case declares about driving ``literalize_call``.

    A manifest spells enum- and type-valued arguments as strings, which
    this model resolves to their ``literalizer`` types during
    validation, and ``call_transform`` is a template over
    :data:`CALL_TRANSFORM_PLACEHOLDERS` rather than evaluated code.

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

    target_function: str
    parameter_names: StringTuple
    per_element: bool
    ref_key: str = "$ref"
    collection_layout: CollectionLayoutName = "compact"
    call_transform: CallTransformTemplate | None = None
    transform_stub_names: StringTuple = Field(default_factory=_empty_names)
    # Parameter names used when stubbing each ``transform_stub_names``
    # wrapper.  The length sets how many parameters the wrapper takes,
    # so a transform that calls the wrapper with the call *and* the
    # zipped value (two arguments) compiles in fixed-parameter-count
    # languages.
    transform_stub_param_names: StringTuple = Field(
        default_factory=_single_stub_parameter,
    )
    # Spelled ``call_style`` in a manifest, which names a style rather
    # than describing the type the harness passes to ``literalize_call``.
    call_style_type: CallStyleType | None = Field(
        default=None,
        alias="call_style",
    )
    # When True, drive ``literalize_call(..., wrap_in_file=True)``
    # directly instead of wrapping manually with injected stubs.
    wrap_in_file: bool = False
    ref_case_per_language: bool = False
    ref_declarations: dict[str, str] = Field(default_factory=_empty_sources)
    # Names from ``ref_declarations`` (in their original case) that
    # ``literalize_call`` may treat as consumable.  Empty means no ref
    # is consumed.
    consumable_refs: StringFrozenSet = Field(
        default_factory=_empty_name_set,
    )
    # Refs that receive declarations in the self-contained golden file
    # but are intentionally omitted from ``ref_values``.  This exercises
    # the historical unknown-ref preamble behavior without leaving the
    # rendered call's identifier undefined for fixture compilation.
    unknown_ref_names: StringFrozenSet = Field(
        default_factory=_empty_name_set,
    )
    # Additional JSON sources used to seed ``ref_values`` without
    # emitting declarations.  This covers mappings whose names are not
    # referenced by the input while keeping generated fixtures free of
    # unused declarations.
    extra_ref_value_sources: dict[str, str] = Field(
        default_factory=_empty_sources,
    )
    # Companion source whose parsed top-level elements pair
    # positionally with the generated calls and are exposed on
    # ``CallContext.zipped``.  Requires ``call_transform``.  Parsed
    # with ``zip_input_format``.
    zip_source: str | None = None
    zip_input_format: CallInputFormat | None = None
    # Trailing source-code comments, one per generated call, paired
    # positionally and emitted after the statement terminator using the
    # language's comment syntax.  An empty entry emits no comment.
    comment_source: StringTuple | None = None
    # TOML documents necessarily parse to a top-level table.  When set,
    # select this table entry as the root value used for call rendering
    # after parsing.  Other formats normally leave this as ``None``.
    input_root_key: str | None = None
    # When set, drive ``literalize_call(..., variable_form=...)`` to
    # exercise the call-binding output mode.  Only meaningful with
    # ``per_element=False`` and (typically) ``wrap_in_file=True`` so
    # the generated file is self-contained around the binding.
    variable_form: CallVariableForm | None = None
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
    requires_call_returns_expression: bool = False
    requires_inline_multiline_dict_args: bool = False
    requires_standalone_wrapped_comments: bool = False
    # When ``True`` the case splices a dict/map ``$zipped`` value into
    # the ``call_transform`` as a free expression.  Languages whose map
    # literal needs a typed left-hand side
    # (``supports_dict_literal_as_free_expression=False``) cannot host
    # the resulting fixture and are skipped (no golden) instead of
    # emitting non-compiling output.
    requires_dict_literal_as_free_expression: bool = False
    # When ``True``, only languages whose default configuration can
    # represent heterogeneous dict values participate in the case.
    requires_heterogeneous_dict_values: bool = False
    # The language-variant axes that drive this case in addition to (or
    # instead of, with ``variant_only``) the default per-language call
    # matrix.  Each axis expands to the specs the case is rendered
    # with, so a case that the default spec rejects names the axis whose
    # specs can represent its input.
    variants: list[CallManifestVariant] = Field(
        default_factory=_empty_call_variants,
    )
    # When ``True`` the case is driven only by the call *variant*
    # suite, so the default per-language call matrix needs no
    # case-specific opt-out.
    variant_only: bool = False

    @model_validator(mode="after")
    def _validate_call_variants(self) -> CallCaseSpec:
        """Validate the variant coverage a call case declares.

        A case names each axis once, and one that opts out of the
        default per-language matrix names at least one, so no call case
        declares itself into having no coverage at all.
        """
        axes = [entry.axis for entry in self.variants]
        if len(axes) != len(set(axes)):
            msg = "duplicate call variant axis"
            raise ValueError(msg)
        if self.variant_only and not self.variants:
            msg = "variant_only requires at least one call variant axis"
            raise ValueError(msg)
        return self


# Defaults stand in for omitted keys, as above.
class _CaseManifestData(  # noqa: NOD001
    LanguageSelection,
    frozen=True,
):
    """Strict representation of the data read directly from TOML."""

    schema_version: Literal[1]
    input: str | None = None
    suites: list[SuiteName] = Field(default_factory=_empty_suites)
    owner: OwnerName | None = None
    # The load-bearing parts this input plays, beyond its participation
    # in a suite or an axis.  A runner that renders one chosen fixture
    # finds it by role rather than by naming the directory.
    roles: list[CaseRoleName] = Field(default_factory=_empty_roles)
    base_context: RenderContext = Field(default_factory=RenderContext)
    variants: list[ManifestVariant] = Field(default_factory=_empty_variants)
    call: CallCaseSpec | None = None
    ref: RefCaseSpec | None = None

    def _validate_owned_table(
        self,
        *,
        table_name: str,
        table: object,
        owners: frozenset[OwnerName],
    ) -> None:
        """Validate one owner-scoped table against the declared owner.

        A table and its owners require each other, so a case cannot
        declare configuration that nothing reads, nor claim an owner
        whose runner has nothing to read.
        """
        if self.owner in owners and table is None:
            msg = f"owner {self.owner!r} requires a [{table_name}] table"
            raise ValueError(msg)
        if table is not None and self.owner not in owners:
            accepted = " or ".join(repr(owner) for owner in sorted(owners))
            msg = f"a [{table_name}] table requires owner = {accepted}"
            raise ValueError(msg)

    @model_validator(mode="after")
    def _validate_consistency(self) -> _CaseManifestData:
        """Validate relationships that span manifest fields."""
        self._validate_owned_table(
            table_name="call",
            table=self.call,
            owners=frozenset({CALL_OWNER}),
        )
        self._validate_owned_table(
            table_name="ref",
            table=self.ref,
            owners=_REF_OWNERS,
        )
        if len(self.suites) != len(set(self.suites)):
            msg = "suites contains a duplicate entry"
            raise ValueError(msg)
        if len(self.roles) != len(set(self.roles)):
            msg = "roles contains a duplicate entry"
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
        return self


@dataclasses.dataclass(frozen=True, kw_only=True)
class CaseManifest:
    """Validated coverage and input metadata for one case directory."""

    path: Path
    case_dir: Path
    schema_version: Literal[1]
    input: CaseInput
    selection: LanguageSelection
    suites: frozenset[SuiteName]
    owner: OwnerName | None
    roles: frozenset[CaseRoleName]
    base_context: RenderContext
    variants: tuple[ManifestVariant, ...]
    call: CallCaseSpec | None
    ref: RefCaseSpec | None


@beartype
def manifest_admits_language(
    *, manifest: CaseManifest, lang_cls: literalizer.LanguageCls
) -> bool:
    """Return whether a case selects *lang_cls*."""
    return manifest.selection.admits_language(lang_cls=lang_cls)


@beartype
def variable_form_for_context(
    *, context: RenderContext
) -> literalizer.VariableForm:
    """Translate a validated manifest variable-form name to the API
    type.
    """
    return _VARIABLE_FORMS_BY_NAME[context.variable_form]


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
        data = _CaseManifestData.model_validate(
            obj=raw,
            context={"case_dir_name": path.parent.name},
        )
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
        selection=LanguageSelection(
            languages=data.languages,
            languages_reason=data.languages_reason,
            gates=data.gates,
        ),
        suites=frozenset(data.suites),
        owner=data.owner,
        roles=frozenset(data.roles),
        base_context=data.base_context,
        variants=tuple(data.variants),
        call=data.call,
        ref=data.ref,
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
def ref_case_specs(
    *,
    cases_dir: Path,
    owner: OwnerName,
) -> tuple[RefCaseSpec, ...]:
    """Return every ``$ref`` case configuration declared by *owner*."""
    return tuple(
        manifest.ref
        for manifest in load_case_manifests(cases_dir=cases_dir)
        if manifest.ref is not None and manifest.owner == owner
    )


@functools.cache
@beartype
def case_dir_name_for_owner(*, cases_dir: Path, owner: OwnerName) -> str:
    """Return the name of the sole case directory declaring *owner*.

    Owners naming a single specialized fixture are looked up through
    their manifests, so the fixture's directory name is declared once,
    on disk, rather than restated by the harness.
    """
    names = [
        manifest.case_dir.name
        for manifest in load_case_manifests(cases_dir=cases_dir)
        if manifest.owner == owner
    ]
    match names:
        case [name]:
            return name
        case _:
            msg = (
                f"expected exactly one case with owner {owner!r}, "
                f"found {sorted(names)}"
            )
            raise CaseManifestError(msg)


@functools.cache
@beartype
def case_dir_names_for_variant_axis(
    *,
    cases_dir: Path,
    axis: str,
) -> tuple[str, ...]:
    """Return the names of the case directories declaring *axis*.

    An axis is declared by the inputs it renders, so the set of inputs
    an axis covers is read off the manifests rather than restated.
    """
    return tuple(
        manifest.case_dir.name
        for manifest in load_case_manifests(cases_dir=cases_dir)
        for manifest_variant in manifest.variants
        if manifest_variant.axis == axis
    )


@functools.cache
@beartype
def case_dir_names_for_role(
    *,
    cases_dir: Path,
    role: CaseRoleName,
) -> tuple[str, ...]:
    """Return the names of the case directories declaring *role*.

    Names come back in directory order so a runner's expansion is
    stable.  A role no case answers to is an error rather than an empty
    expansion, so removing the fixture a runner needs fails naming the
    role instead of silently dropping every golden file behind it.
    """
    names = tuple(
        manifest.case_dir.name
        for manifest in load_case_manifests(cases_dir=cases_dir)
        if role in manifest.roles
    )
    if not names:
        msg = (
            f"no {MANIFEST_NAME} under {cases_dir} declares roles = [{role!r}]"
        )
        raise CaseManifestError(msg)
    return names


@functools.cache
@beartype
def case_dir_name_for_role(*, cases_dir: Path, role: CaseRoleName) -> str:
    """Return the name of the sole case directory declaring *role*."""
    names = case_dir_names_for_role(cases_dir=cases_dir, role=role)
    match names:
        case (name,):
            return name
        case _:
            msg = (
                f"expected exactly one {MANIFEST_NAME} declaring "
                f"roles = [{role!r}], found {sorted(names)}"
            )
            raise CaseManifestError(msg)


@beartype
def heterogeneous_strategy_role(*, strategy_name: str) -> CaseRoleName:
    """Return the role naming the input *strategy_name* renders.

    Most strategies exercise the mixed-scalar dict holding the default
    role.  A strategy that dict cannot exercise pairs with its own
    input, which declares a role named after the strategy: ``TUPLE``
    needs an input carrying a tuple-eligible heterogeneous scalar array,
    so it renders the fixture declaring
    ``heterogeneous-strategy-tuple-input``.

    A strategy claims its own input by adding that role to the
    vocabulary and to one case, rather than by being named here.
    """
    role = f"heterogeneous-strategy-{strategy_name.lower()}-input"
    for name in CASE_ROLE_NAMES:
        if name == role:
            return name
    return HETEROGENEOUS_STRATEGY_DEFAULT_ROLE


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
