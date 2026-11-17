"""Load and validate case-local golden coverage manifests."""

from __future__ import annotations

import dataclasses
import datetime as dt
import functools
import tomllib
from collections.abc import Mapping
from pathlib import Path
from typing import Annotated, Literal, get_args

from beartype import beartype
from pydantic import (
    BaseModel,
    BeforeValidator,
    Field,
    model_validator,
)

import literalizer
from literalizer import ValueInput
from literalizer._types import Scalar
from tests.native_value_sources import RefDatetimeInput, RefValueSource

from . import call_templates, manifest_values
from .case_inputs import CaseInput, ReusedAnchorWarningSpec, infer_case_input
from .manifest_selection import CapabilitySelection
from .owned_case_specs import OwnedCaseSpec
from .variant_axis_names import KNOWN_VARIANT_AXES
from .variant_types import VariantExpectedError

# Keep the template type available through the existing manifest API.
CallTransform = call_templates.CallTransform

MANIFEST_NAME = "case.toml"

type CollectionLayoutName = Literal["compact", "multiline"]
type SuiteName = Literal["base", "combined", "default-module-name"]
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
    "constructor-binding",
    "native-invocation",
    "deep-input",
    "shared-invocation",
]

# Spelled as an assignment rather than a ``type`` statement so the
# accepted names can be read back out with ``get_args``.
_CaseRoleNameLiteral = Literal[
    "concurrent-yaml-input",
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

CASE_ROLE_NAMES = frozenset[CaseRoleName](
    get_args(tp=_CaseRoleNameLiteral),
)

CONCURRENT_YAML_ROLE: CaseRoleName = "concurrent-yaml-input"

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


class CaseManifestError(ValueError):
    """A case manifest is invalid or internally inconsistent."""


class InputRoundtripSpec(
    BaseModel, arbitrary_types_allowed=True, extra="forbid", frozen=True
):
    """Render the input once, then parse that output for the golden."""

    language: manifest_values.ManifestLanguage
    input_format: manifest_values.CallInputFormat


class SubstitutionMappingEntry(
    BaseModel,
    arbitrary_types_allowed=True,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """A mapping entry whose scalar key need not be a TOML table key."""

    key: Scalar
    value: ValueInput


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

    variable_form: manifest_values.VariableFormName = "new"
    variable_name: str = "my_data"
    collection_layout: CollectionLayoutName | None = None
    consumer_templates: dict[manifest_values.ManifestLanguage, str] = Field(
        default_factory=dict[literalizer.LanguageCls, str]
    )
    pre_indent_level: Annotated[int, Field(ge=0)] = 0
    record_null_substitutions: Mapping[str, ValueInput] | None = None
    record_null_mapping_substitutions: dict[
        str, list[SubstitutionMappingEntry]
    ] = Field(default_factory=dict)
    record_null_value_sources: dict[str, RefValueSource] = Field(
        default_factory=dict
    )

    def resolved_record_null_substitutions(
        self,
    ) -> Mapping[str, ValueInput] | None:
        """Resolve ordinary, mapping-key and native-value
        substitutions.
        """
        if (
            len(self.record_null_mapping_substitutions) == 0
            and len(self.record_null_value_sources) == 0
        ):
            return self.record_null_substitutions
        substitutions = dict[str, ValueInput]()
        if self.record_null_substitutions is not None:
            substitutions.update(self.record_null_substitutions)
        for name, entries in self.record_null_mapping_substitutions.items():
            substitutions[name] = {entry.key: entry.value for entry in entries}
        for name, source in self.record_null_value_sources.items():
            substitutions[name] = source.to_value()
        return substitutions


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
    # Generate a declaration before an existing-variable assignment.
    initialize_variable: bool = False
    # Keep explicit module-name options instead of the compiler fixture name.
    apply_fixture_module_name: bool = True
    wrap_in_file: bool = True
    # Native caller syntax around an unwrapped result, by language.
    consumer_templates: dict[manifest_values.ManifestLanguage, str] = Field(
        default_factory=dict[literalizer.LanguageCls, str]
    )
    # Some shape-mapping cases deliberately never use the external type.
    include_extra_preamble: bool = True
    context: RenderContext = Field(default_factory=RenderContext)
    # The language capabilities this input needs in order to render at
    # all.  A variant whose language lacks one of them is skipped (no
    # golden) rather than emitting output the language cannot express.
    requires: list[VariantCapabilityName] = Field(
        default_factory=list[VariantCapabilityName],
    )
    expected_errors: list[VariantExpectedError] = Field(
        default_factory=list[VariantExpectedError],
    )

    @model_validator(mode="after")
    def _validate_requirements(self) -> ManifestVariant:
        """Reject a capability named more than once."""
        if len(self.requires) != len(set(self.requires)):
            msg = "requires contains a duplicate entry"
            raise ValueError(msg)
        return self


class ApiManifestVariant(
    BaseModel,
    arbitrary_types_allowed=True,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """An API case's participation in a named, typed variant axis.

    The language variant names its golden, so a case names only an axis.
    """

    axis: Annotated[str, Field(min_length=1)]

    @model_validator(mode="after")
    def _validate_known_axis(self) -> ApiManifestVariant:
        """Reject an axis name no expansion answers to."""
        if self.axis not in KNOWN_VARIANT_AXES:
            msg = f"unknown variant axis {self.axis!r}"
            raise ValueError(msg)
        return self


def _single_stub_parameter() -> tuple[str, ...]:
    """Return the default wrapper-stub parameter names."""
    return ("_arg",)


def _parse_ref_time(value: object, /) -> object:
    """Resolve an ISO time source while preserving native TOML times."""
    if isinstance(value, str):
        return dt.time.fromisoformat(value)
    return value


type RefTimeInput = Annotated[dt.time, BeforeValidator(func=_parse_ref_time)]


class _RefCallConsumer(BaseModel, extra="forbid", frozen=True, strict=True):
    """Call a consumer after producing the reference result."""

    target_function: Annotated[str, Field(min_length=1)]


class RefConsumerSpec(_RefCallConsumer, frozen=True):
    """Consume the produced reference binding or expression."""

    kind: Literal["call"]


class RefAssignmentConsumerSpec(_RefCallConsumer, frozen=True):
    """Consume both the caller's initial binding and the assigned
    value.
    """

    kind: Literal["assignment"]


class RefValueCheckSpec(BaseModel, extra="forbid", frozen=True, strict=True):
    """Check an independent value without providing inference hints."""

    kind: Literal["value-check"]
    expected_source: str


type RefConsumer = Annotated[
    RefConsumerSpec | RefAssignmentConsumerSpec | RefValueCheckSpec,
    Field(discriminator="kind"),
]


# Defaults below describe omitted TOML keys, as for RenderContext.
class _RefBindings(  # noqa: NOD001
    BaseModel,
    extra="forbid",
    frozen=True,
    strict=True,
    arbitrary_types_allowed=True,
):
    """Bindings materialized by the API, including native TOML values."""

    value_sources: dict[str, str] = Field(default_factory=dict[str, str])
    bound_refs: Mapping[str, ValueInput] | None = None
    bound_ref_times: dict[str, RefTimeInput] = Field(
        default_factory=dict[str, dt.time]
    )
    bound_ref_datetimes: dict[str, RefDatetimeInput] = Field(
        default_factory=dict[str, dt.datetime]
    )
    bound_ref_values: dict[str, RefValueSource] = Field(
        default_factory=dict[str, RefValueSource]
    )
    extra_ref_value_sources: dict[str, str] = Field(
        default_factory=dict[str, str]
    )


class ExternalRefContext(  # noqa: NOD001
    BaseModel, extra="forbid", frozen=True, strict=True
):
    """Caller-owned declarations composed after API rendering."""

    kind: Literal["external"]
    declarations: Annotated[dict[str, str], Field(min_length=1)]
    caller_preamble: manifest_values.StringTuple = Field(
        default_factory=tuple[str, ...]
    )
    consumer: RefConsumer


class BoundRefContext(  # noqa: NOD001
    _RefBindings, frozen=True
):
    """Wrap API-materialized reference bindings in a complete file."""

    kind: Literal["bound"] = "bound"


class RefExpressionContext(_RefBindings, frozen=True):
    """Pass an API-rendered expression directly to a native consumer."""

    kind: Literal["expression"]
    consumer: RefConsumerSpec


type RefContext = Annotated[
    BoundRefContext | ExternalRefContext | RefExpressionContext,
    Field(discriminator="kind"),
]


class RefCaseSpec(
    OwnedCaseSpec,
    CapabilitySelection,
    frozen=True,
):
    """Public reference arguments and one validated fixture context.

    The context distinguishes API-materialized bindings from caller-owned
    declarations. Inference hints remain a separate public API argument.
    """

    ref_key: str = "$ref"
    variable_form: manifest_values.VariableFormName | Literal["none"] = "new"
    variable_name: str = "my_data"
    variable_modifiers: manifest_values.StringTuple = Field(
        default_factory=tuple[str, ...]
    )
    collection_layout: CollectionLayoutName = "compact"
    include_delimiters: bool = True
    pre_indent_level: int = 0
    heterogeneous_strategy: str | None = None
    sequence_format: str | None = None
    default_sequence_element_type: str | None = None
    declaration_style: str | None = None
    variable_type_hints: str | None = None
    json_type: str | None = None
    dict_format: str | None = None
    ref_case_override: manifest_values.RefIdentifierCase | None = None
    ref_case_by_language: dict[
        manifest_values.ManifestLanguage, manifest_values.RefIdentifierCase
    ] = Field(
        default_factory=dict[
            literalizer.LanguageCls, literalizer.IdentifierCase
        ],
    )
    context: RefContext = Field(default_factory=BoundRefContext)
    # Inference hints are independent of caller declarations and bindings.
    # Omission passes None; an explicitly empty table passes {}.
    explicit_ref_value_sources: dict[str, str] | None = None
    variants: list[ApiManifestVariant] = Field(
        default_factory=list[ApiManifestVariant],
    )
    variant_only: bool = False

    @model_validator(mode="after")
    def _validate_ref_variants(self) -> RefCaseSpec:
        """Require distinct axes and an exercised variant-only case."""
        axes = [entry.axis for entry in self.variants]
        if len(axes) != len(set(axes)):
            msg = "duplicate ref variant axis"
            raise ValueError(msg)
        if self.variant_only and len(self.variants) == 0:
            msg = "variant_only requires at least one ref variant axis"
            raise ValueError(msg)
        return self

    @model_validator(mode="after")
    def _validate_consumer_context(self) -> RefCaseSpec:
        """Check consumer requirements against the selected public binding."""
        if (
            isinstance(self.context, RefExpressionContext)
            and self.variable_form != "none"
        ):
            msg = "expression context requires variable_form = none"
            raise ValueError(msg)
        if isinstance(self.context, ExternalRefContext):
            consumer = self.context.consumer
            if (
                isinstance(consumer, RefValueCheckSpec)
                and self.variable_form == "none"
            ):
                msg = "value-check requires a variable binding"
                raise ValueError(msg)
            if isinstance(consumer, RefAssignmentConsumerSpec) and (
                self.variable_form != "existing"
                or "my_data" not in self.context.declarations
            ):
                msg = (
                    "assignment consumer requires an existing my_data binding"
                )
                raise ValueError(msg)
        return self

    def ref_case_for(
        self, *, lang_cls: literalizer.LanguageCls
    ) -> literalizer.IdentifierCase | None:
        """Resolve the explicitly requested case for one language."""
        return self.ref_case_by_language.get(lang_cls, self.ref_case_override)

    def resolved_variable_form(self) -> literalizer.VariableForm | None:
        """Return the public API variable form selected by the
        manifest.
        """
        if self.variable_form == "none":
            return None
        return dataclasses.replace(
            manifest_values.variable_form_for_name(name=self.variable_form),
            name=self.variable_name,
        )


class CallRecipeSpec(  # noqa: NOD001
    BaseModel,
    extra="forbid",
    frozen=True,
    strict=True,
    arbitrary_types_allowed=True,
):
    """Common callback metadata, independent of native expression
    syntax.
    """

    reports_zip_usage: bool = True


class CallStubRecipeSpec(  # noqa: NOD001
    CallRecipeSpec, frozen=True
):
    """Synthetic declarations needed by authored template expressions."""

    stub_names: manifest_values.StringTuple = Field(
        default_factory=tuple[str, ...]
    )
    stub_param_names: manifest_values.StringTuple = Field(
        default_factory=_single_stub_parameter
    )


class NativeCallRecipeSpec(  # noqa: NOD001
    CallStubRecipeSpec, frozen=True
):
    """A native expression optionally composed through an outer
    template.
    """

    outer: manifest_values.CallTransformTemplate | None = None


class CallTemplateSpec(CallStubRecipeSpec, frozen=True):
    """A callback expressed entirely by an authored template."""

    kind: Literal["template"]
    template: manifest_values.CallTransformTemplate


class CallGroupSpec(NativeCallRecipeSpec, frozen=True):
    """Group a template body using the language's expression syntax."""

    kind: Literal["group"]
    body: manifest_values.CallTransformTemplate
    suffix: str


class CallArgumentsSpec(NativeCallRecipeSpec, frozen=True):
    """Pass native lexical operands using the configured call
    convention.
    """

    kind: Literal["arguments"]
    arguments: manifest_values.StringTuple
    suffix: str


class CallOperandSpec(BaseModel, extra="forbid", frozen=True, strict=True):
    """A wrapper parameter and the operand supplied in that position."""

    role: Literal["call", "zipped"]
    parameter: str


class CallWrapperSpec(  # noqa: NOD001
    CallRecipeSpec, frozen=True
):
    """A native wrapper whose operands retain their call/zip roles."""

    kind: Literal["wrapper"]
    outer: manifest_values.CallTransformTemplate | None = None
    target: Annotated[str, Field(min_length=1)]
    arguments: Annotated[tuple[CallOperandSpec, ...], Field(strict=False)]


class CallSequenceSpec(NativeCallRecipeSpec, frozen=True):
    """Wrap the call result in a native one-element sequence."""

    kind: Literal["sequence"]


class CallAddOneSpec(NativeCallRecipeSpec, frozen=True):
    """Add one using the result producer's native grammar."""

    kind: Literal["add-one"]


class CallConditionalSpec(NativeCallRecipeSpec, frozen=True):
    """Place the call in the native conditional for a possibly null object."""

    kind: Literal["nullable-conditional"]


type CallRecipe = Annotated[
    CallTemplateSpec
    | CallGroupSpec
    | CallArgumentsSpec
    | CallWrapperSpec
    | CallSequenceSpec
    | CallAddOneSpec
    | CallConditionalSpec,
    Field(discriminator="kind"),
]


class FollowupCallSpec(  # noqa: NOD001
    BaseModel, extra="forbid", frozen=True, strict=True
):
    """An additional call consuming the primary call's bound result."""

    source: str
    target_function: str | None = None


class CallFixtureSpec(  # noqa: NOD001
    BaseModel, extra="forbid", frozen=True, strict=True
):
    """Reference sources shared by the supported call fixture contexts."""

    ref_declarations: dict[str, str] = Field(default_factory=dict[str, str])


class BoundCallFixture(CallFixtureSpec, frozen=True):
    """Use API-owned reference bindings with the declaration skip
    policy.
    """

    kind: Literal["bound"]


class WrappedCallFixture(CallFixtureSpec, frozen=True):
    """Let the public API assemble the complete file and bound refs."""

    kind: Literal["wrapped"]


class _ComposedCallFixture(  # noqa: NOD001
    CallFixtureSpec, frozen=True
):
    """Compose declarations and synthetic stubs around the call result."""

    followup: FollowupCallSpec | None = None
    unknown_ref_names: manifest_values.StringFrozenSet = Field(
        default_factory=frozenset[str]
    )
    include_target_stub: bool = True
    caller_imports: manifest_values.StringTuple = Field(
        default_factory=tuple[str, ...]
    )
    caller_body_preamble: manifest_values.StringTuple = Field(
        default_factory=tuple[str, ...]
    )


class ComposedCallFixture(  # noqa: NOD001
    _ComposedCallFixture, frozen=True
):
    """Assemble a complete file from result metadata and declarations."""

    kind: Literal["composed"] = "composed"


type CallFixture = Annotated[
    WrappedCallFixture | BoundCallFixture | ComposedCallFixture,
    Field(discriminator="kind"),
]


class CallCaseSpec(
    OwnedCaseSpec,
    CapabilitySelection,
    frozen=True,
):
    """Everything a case declares about driving ``literalize_call``.

    Validation resolves public API arguments and selects a transform recipe
    and fixture context. Native expressions may compose an outer template;
    wrapper operands also supply their own stub parameters.

    ``fixture.ref_declarations`` maps a ``{"$ref": "name"}`` marker in the case
    input to a source in ``ref_input_format`` rendered as a declaration via
    :func:`literalizer.literalize`, emitted before the call so the
    resulting file is self-contained.

    With ``ref_case_per_language``, the harness picks the native case
    for the selected declaration style, falling back to the language's
    first-listed ``IdentifierCases`` member. It converts every
    ``fixture.ref_declarations`` key to that case and passes the
    same case to :func:`literalize_call` so the declaration site and the
    call site agree on identifier spelling.
    """

    target_function: str
    shared_invocation: bool = False
    parameter_names: manifest_values.StringTuple
    per_element: bool
    fixture: CallFixture = Field(default_factory=ComposedCallFixture)
    # Independently authored integer events observed by native receivers.
    # A receiver returns its argument plus 100; wrappers/follow-ups observe
    # that result and any zipped operand in execution order.
    integer_receiver_events: manifest_values.IntegerCallEvents | None = None
    ref_key: str = "$ref"
    collection_layout: CollectionLayoutName = "compact"
    transform: CallRecipe | None = None
    # Spelled ``call_style`` in a manifest, which names a style rather
    # than describing the type the harness passes to ``literalize_call``.
    call_style_type: manifest_values.CallStyleType | None = Field(
        default=None,
        alias="call_style",
    )
    ref_case_per_language: bool = False
    # Use one format for declaration sources and inference-hint sources.
    ref_input_format: manifest_values.CallInputFormat = (
        literalizer.InputFormat.JSON
    )
    # Names from ``ref_declarations`` (in their original case) that
    # ``literalize_call`` may treat as consumable.  Empty means no ref
    # is consumed.
    consumable_refs: manifest_values.StringFrozenSet = Field(
        default_factory=frozenset[str],
    )
    # An explicit mapping overrides declaration-derived inference hints.
    # An empty table passes {}, while omission keeps the inferred hints.
    explicit_ref_value_sources: dict[str, str] | None = None
    # Compare returned source knowledge independently of native bindings.
    # JSON text distinguishes an expected null from an omitted expectation.
    expected_source_data: str | None = None
    # Additional sources used to seed ``ref_values`` without
    # emitting declarations.  This covers mappings whose names are not
    # referenced by the input while keeping generated fixtures free of
    # unused declarations.
    extra_ref_value_sources: dict[str, str] = Field(
        default_factory=dict[str, str],
    )
    # Companion source whose parsed top-level elements pair
    # positionally with the generated calls and are exposed on
    # ``CallContext.zipped``.  Requires ``call_transform``.  Parsed
    # with ``zip_input_format``.
    zip_source: str | None = None
    zip_input_format: manifest_values.CallInputFormat | None = None
    # Trailing source-code comments, one per generated call, paired
    # positionally and emitted after the statement terminator using the
    # language's comment syntax.  An empty entry emits no comment.
    comment_source: manifest_values.StringTuple | None = None
    # TOML documents necessarily parse to a top-level table.  When set,
    # select this table entry as the root value used for call rendering
    # after parsing.  Other formats normally leave this as ``None``.
    input_root_key: str | None = None
    # Keep the public API binding argument independent of the fixture context.
    variable_form: manifest_values.CallVariableForm | None = None
    variable_modifiers: manifest_values.StringTuple = Field(
        default_factory=tuple[str, ...]
    )
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
    variants: list[ApiManifestVariant] = Field(
        default_factory=list[ApiManifestVariant],
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
        if isinstance(self.fixture, ComposedCallFixture):
            followup = self.fixture.followup
            if (
                followup is not None
                and followup.target_function == self.target_function
            ):
                msg = (
                    "followup target_function must differ from target_function"
                )
                raise ValueError(msg)
        axes = [entry.axis for entry in self.variants]
        if len(axes) != len(set(axes)):
            msg = "duplicate call variant axis"
            raise ValueError(msg)
        if self.variant_only and len(self.variants) == 0:
            msg = "variant_only requires at least one call variant axis"
            raise ValueError(msg)
        return self


# Defaults describe omitted manifest fields, as for RenderContext.
class ConstructorCaseSpec(  # noqa: NOD001
    BaseModel, arbitrary_types_allowed=True, extra="forbid", frozen=True
):
    """A constructor target and variable for a generated call binding."""

    class_name: Annotated[str, Field(min_length=1)] = "Playlist"
    parameter_names: tuple[str, ...] = ()
    # A native caller can provide an externally declared constructor.
    consumer_template: str | None = None
    consumer_templates: Mapping[str, str] = Field(default_factory=dict)
    # Render shared input through literalize.
    target_source_template: str | None = None
    # A portable document can use a common renderer after native selection.
    target_language: manifest_values.ManifestLanguage | None = None
    # Bind the case input to the formatted target through the variable API.
    target_variable: bool = False
    # A target supplied through language options can bind a separate name.
    target_variable_name: Annotated[str, Field(min_length=1)] | None = None
    # String-valued language options can consume the formatted target too.
    target_options: Mapping[str, str] = Field(default_factory=dict)
    variable_name: Annotated[str, Field(min_length=1)] = "p"

    @property
    def renders_target(self) -> bool:
        """Whether this case consumes a target instead of calling it."""
        return self.target_source_template is not None or self.target_variable

    @beartype
    def consumer_for_language(self, *, language_name: str) -> str | None:
        """Resolve native syntax after the capability selects a
        backend.
        """
        if len(self.consumer_templates) == 0:
            return self.consumer_template
        try:
            return self.consumer_templates[language_name]
        except KeyError as error:
            msg = f"no constructor consumer for {language_name!r}"
            raise CaseManifestError(msg) from error


# Defaults stand in for omitted keys, as above.
class NativeInvocationCaseSpec(BaseModel, extra="forbid", frozen=True):
    """A real caller program for a native invocation recipe sequence."""

    consumer_template: str


class _CaseManifestData(
    CapabilitySelection,
    frozen=True,
):
    """Strict representation of the data read directly from TOML."""

    schema_version: Literal[1]
    input: str | None = None
    input_roundtrip: InputRoundtripSpec | None = None
    expected_reused_anchor_warning: ReusedAnchorWarningSpec | None = None
    suites: list[SuiteName] = Field(default_factory=list[SuiteName])
    owner: OwnerName | None = None
    # The load-bearing parts this input plays, beyond its participation
    # in a suite or an axis.  A runner that renders one chosen fixture
    # finds it by role rather than by naming the directory.
    roles: list[CaseRoleName] = Field(default_factory=list[CaseRoleName])
    base_context: RenderContext = Field(default_factory=RenderContext)
    variants: list[ManifestVariant] = Field(
        default_factory=list[ManifestVariant]
    )
    constructor: ConstructorCaseSpec | None = None
    native_invocation: NativeInvocationCaseSpec | None = None
    call: CallCaseSpec | None = None
    ref: RefCaseSpec | None = None
    call_examples: list[CallCaseSpec] = Field(
        default_factory=list[CallCaseSpec]
    )
    ref_examples: list[RefCaseSpec] = Field(default_factory=list[RefCaseSpec])

    def _validate_examples(self) -> None:
        """Require named, unique examples with a shared API input
        owner.
        """
        for primary, examples, label in (
            (self.call, self.call_examples, "call_examples"),
            (self.ref, self.ref_examples, "ref_examples"),
        ):
            if primary is not None and primary.example is not None:
                msg = "primary API tables cannot name an example"
                raise ValueError(msg)
            if len(examples) > 0 and primary is None:
                msg = f"{label} requires its primary API table"
                raise ValueError(msg)
            names = [entry.example for entry in examples]
            if None in names:
                msg = f"{label} requires an example name"
                raise ValueError(msg)
            if len(names) != len(set(names)):
                msg = f"{label} contains a duplicate example name"
                raise ValueError(msg)

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
        self._validate_examples()
        if self.input_roundtrip is not None and self.owner is not None:
            msg = "input_roundtrip requires a literal rendering suite"
            raise ValueError(msg)
        self._validate_owned_table(
            table_name="native_invocation",
            table=self.native_invocation,
            owners=frozenset({"native-invocation"}),
        )
        self._validate_owned_table(
            table_name="constructor",
            table=self.constructor,
            owners=frozenset({"constructor-binding"}),
        )
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
        if len(self.suites) > 0 and self.owner is not None:
            msg = "suites and owner are mutually exclusive"
            raise ValueError(msg)
        if len(self.suites) == 0 and self.owner is None:
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
    schema_version: Literal[1]
    input: CaseInput
    input_roundtrip: InputRoundtripSpec | None
    selection: CapabilitySelection
    suites: frozenset[SuiteName]
    owner: OwnerName | None
    roles: frozenset[CaseRoleName]
    base_context: RenderContext
    variants: tuple[ManifestVariant, ...]
    constructor: ConstructorCaseSpec | None
    native_invocation: NativeInvocationCaseSpec | None
    call: CallCaseSpec | None
    ref: RefCaseSpec | None
    call_examples: tuple[CallCaseSpec, ...]
    ref_examples: tuple[RefCaseSpec, ...]

    @property
    def case_dir(self) -> Path:
        """Derive the owning directory from the manifest's source path."""
        return self.path.parent


@beartype
def variable_form_for_context(
    *, context: RenderContext
) -> literalizer.VariableForm:
    """Build the API variable form with the manifest's declared name."""
    return dataclasses.replace(
        manifest_values.variable_form_for_name(name=context.variable_form),
        name=context.variable_name,
    )


def _fail(*, path: Path, message: str) -> CaseManifestError:
    """Build a manifest error containing its source path."""
    return CaseManifestError(f"{path}: {message}")


@functools.cache
@beartype
def load_case_manifest(case_dir: Path) -> CaseManifest:
    """Return one fully validated ``case.toml`` manifest."""
    path = case_dir / MANIFEST_NAME
    if not path.is_file():
        raise _fail(path=path, message="manifest is missing")
    try:
        raw = tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        raise _fail(path=path, message=f"invalid TOML: {exc}") from exc

    try:
        data = _CaseManifestData.model_validate(
            obj=raw,
            context={"case_dir_name": path.parent.name},
        )
    except ValueError as exc:
        raise _fail(path=path, message=str(object=exc)) from exc
    try:
        input_info = infer_case_input(
            case_dir=case_dir,
            input_name=data.input,
            expected_reused_anchor_warning=data.expected_reused_anchor_warning,
        )
    except ValueError as exc:
        raise _fail(path=path, message=str(object=exc)) from exc

    if (
        input_info.expected_reused_anchor_warning is not None
        and input_info.input_format is not literalizer.InputFormat.YAML
    ):
        raise _fail(
            path=path,
            message="expected_reused_anchor_warning requires YAML input",
        )

    return CaseManifest(
        path=path,
        schema_version=data.schema_version,
        input=input_info,
        input_roundtrip=data.input_roundtrip,
        selection=CapabilitySelection(
            gates=data.gates,
            any_gates=data.any_gates,
        ),
        suites=frozenset(data.suites),
        owner=data.owner,
        roles=frozenset(data.roles),
        base_context=data.base_context,
        variants=tuple(data.variants),
        constructor=data.constructor,
        native_invocation=data.native_invocation,
        call=data.call,
        ref=data.ref,
        call_examples=tuple(data.call_examples),
        ref_examples=tuple(data.ref_examples),
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
        config
        for manifest in load_case_manifests(cases_dir=cases_dir)
        if manifest.call is not None
        for config in (manifest.call, *manifest.call_examples)
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
        config
        for manifest in load_case_manifests(cases_dir=cases_dir)
        if manifest.ref is not None and manifest.owner == owner
        for config in (manifest.ref, *manifest.ref_examples)
    )
