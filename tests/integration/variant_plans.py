"""Typed expansion plans for the declared variant axes.

``axes.toml`` names, for each declared axis, one plan from this module
and supplies that plan's parameters.  The plans themselves are typed
Python: the file selects a plan and supplies its parameters, it never
expresses a condition.

Everything a plan looks up by name -- a formatter option, a language
capability flag, a spec field, a language-metadata field -- resolves
through a closed registry declared here, so an unknown name, an unknown
plan, an unknown gate kind, or an unknown name-template placeholder
fails when the registry loads rather than when a golden file is built.

Axes whose expansion is genuinely irregular (the ``json_type`` family,
the layout-pair widening cases) stay as registered escape-hatch
builders in :mod:`variant_cases`.  A ``filtered`` plan narrows any
axis, declared or irregular, to the languages its gates admit, so a
suite needing a smaller slice of an existing expansion names one rather
than writing its own builder.
"""

import dataclasses
import enum
import functools
import string
import tomllib
from collections.abc import Callable, Hashable, Mapping, Sequence
from pathlib import Path
from typing import (
    Annotated,
    Literal,
    Protocol,
    assert_never,
    runtime_checkable,
)

from beartype import beartype
from pydantic import BaseModel, Field, ValidationError

import literalizer

from .language_metadata import (
    LanguageMetadata,
    RecordVariantName,
    language_metadata,
)
from .language_specs import make_spec, sorted_languages
from .variant_axis_names import KNOWN_VARIANT_AXES
from .variant_types import Variant, enum_member_by_name, find_enum_member

AXES_PATH = Path(__file__).parent / "axes.toml"


class AxisPlanError(ValueError):
    """The declared axis registry is missing or invalid."""


@runtime_checkable
class AxisResolver(Hashable, Protocol):
    """Expands any variant axis the suite knows, by name.

    A filtered plan narrows another axis, which may be an escape-hatch
    builder this module cannot see, so callers hand in the suite's own
    resolver instead.
    """

    def __call__(self, *, axis_key: str) -> list[Variant]:
        """Return the variants *axis_key* expands to."""
        ...  # pylint: disable=unnecessary-ellipsis


@runtime_checkable
class _HasBoolFormat(Protocol):
    """A spec exposing a configurable boolean literal spelling."""

    bool_format: enum.Enum
    bool_formats: type[enum.Enum]


@runtime_checkable
class _HasEmptyDictKey(Protocol):
    """A spec exposing a configurable empty-dict key policy."""

    empty_dict_key: enum.Enum
    empty_dict_keys: type[enum.Enum]


@runtime_checkable
class _HasAnnotationEvaluation(Protocol):
    """A spec exposing configurable annotation evaluation."""

    annotation_evaluation: enum.Enum
    annotation_evaluations: type[enum.Enum]


@runtime_checkable
class _HasUnionFormat(Protocol):
    """A spec exposing configurable union annotation syntax."""

    union_format: enum.Enum
    union_formats: type[enum.Enum]


@beartype
def _bool_format(spec: literalizer.Language) -> object:
    """Return the configured boolean literal spelling."""
    assert isinstance(spec, _HasBoolFormat)  # noqa: S101
    return spec.bool_format


@beartype
def _bool_formats(spec: literalizer.Language) -> type[enum.Enum]:
    """Return the boolean literal spellings a language offers."""
    assert isinstance(spec, _HasBoolFormat)  # noqa: S101
    return spec.bool_formats


@beartype
def _empty_dict_key(spec: literalizer.Language) -> object:
    """Return the configured empty-dict key policy."""
    assert isinstance(spec, _HasEmptyDictKey)  # noqa: S101
    return spec.empty_dict_key


@beartype
def _empty_dict_keys(spec: literalizer.Language) -> type[enum.Enum]:
    """Return the empty-dict key policies a language offers."""
    assert isinstance(spec, _HasEmptyDictKey)  # noqa: S101
    return spec.empty_dict_keys


@beartype
def _annotation_evaluation(spec: literalizer.Language) -> object:
    """Return the configured annotation-evaluation mode."""
    assert isinstance(spec, _HasAnnotationEvaluation)  # noqa: S101
    return spec.annotation_evaluation


@beartype
def _annotation_evaluations(spec: literalizer.Language) -> type[enum.Enum]:
    """Return the annotation-evaluation modes a language offers."""
    assert isinstance(spec, _HasAnnotationEvaluation)  # noqa: S101
    return spec.annotation_evaluations


@beartype
def _union_format(spec: literalizer.Language) -> object:
    """Return the configured union annotation syntax."""
    assert isinstance(spec, _HasUnionFormat)  # noqa: S101
    return spec.union_format


@beartype
def _union_formats(spec: literalizer.Language) -> type[enum.Enum]:
    """Return the union annotation forms a language offers."""
    assert isinstance(spec, _HasUnionFormat)  # noqa: S101
    return spec.union_formats


@dataclasses.dataclass(frozen=True, kw_only=True)
class _Option:
    """One configurable formatter option a plan can select values from.

    ``kwarg`` is the language-class constructor parameter name; each
    accessor reads the configured value or the member enum from a built
    spec.  Those sometimes diverge from the constructor name:
    ``bytes_format`` reads its configured value from ``format_bytes``.
    """

    kwarg: str
    get_default: Callable[[literalizer.Language], object]
    get_members: Callable[[literalizer.Language], type[enum.Enum]]


_OPTIONS: Mapping[str, _Option] = {
    "annotation_evaluation": _Option(
        kwarg="annotation_evaluation",
        get_default=_annotation_evaluation,
        get_members=_annotation_evaluations,
    ),
    "bool_format": _Option(
        kwarg="bool_format",
        get_default=_bool_format,
        get_members=_bool_formats,
    ),
    "bytes_format": _Option(
        kwarg="bytes_format",
        get_default=lambda spec: spec.format_bytes,
        get_members=lambda spec: spec.bytes_formats,
    ),
    "comment_format": _Option(
        kwarg="comment_format",
        get_default=lambda spec: spec.comment_format,
        get_members=lambda spec: spec.comment_formats,
    ),
    # ``date_format`` and ``datetime_format`` read the derived
    # ``format_date``/``format_datetime`` callable, which Haskell, OCaml
    # and SML build rather than return the configured enum member.  For
    # those languages the default never compares equal, so an axis using
    # these entries expands the default member as well.  The
    # ``configured_*`` entries read the enum field and expand strictly
    # non-default members; issue #3342 tracks reconciling the two.
    "configured_date_format": _Option(
        kwarg="date_format",
        get_default=lambda spec: spec.date_format,
        get_members=lambda spec: spec.date_formats,
    ),
    "configured_datetime_format": _Option(
        kwarg="datetime_format",
        get_default=lambda spec: spec.datetime_format,
        get_members=lambda spec: spec.datetime_formats,
    ),
    "date_format": _Option(
        kwarg="date_format",
        get_default=lambda spec: spec.format_date,
        get_members=lambda spec: spec.date_formats,
    ),
    "datetime_format": _Option(
        kwarg="datetime_format",
        get_default=lambda spec: spec.format_datetime,
        get_members=lambda spec: spec.datetime_formats,
    ),
    "declaration_style": _Option(
        kwarg="declaration_style",
        get_default=lambda spec: spec.declaration_style,
        get_members=lambda spec: spec.declaration_styles,
    ),
    "dict_entry_style": _Option(
        kwarg="dict_entry_style",
        get_default=lambda spec: spec.dict_entry_style,
        get_members=lambda spec: spec.dict_entry_styles,
    ),
    "dict_format": _Option(
        kwarg="dict_format",
        get_default=lambda spec: spec.dict_format,
        get_members=lambda spec: spec.dict_formats,
    ),
    "empty_dict_key": _Option(
        kwarg="empty_dict_key",
        get_default=_empty_dict_key,
        get_members=_empty_dict_keys,
    ),
    "float_format": _Option(
        kwarg="float_format",
        get_default=lambda spec: spec.float_format,
        get_members=lambda spec: spec.float_formats,
    ),
    "heterogeneous_strategy": _Option(
        kwarg="heterogeneous_strategy",
        get_default=lambda spec: spec.heterogeneous_strategy,
        get_members=lambda spec: spec.heterogeneous_strategies,
    ),
    "integer_format": _Option(
        kwarg="integer_format",
        get_default=lambda spec: spec.integer_format,
        get_members=lambda spec: spec.integer_formats,
    ),
    "integer_width_strategy": _Option(
        kwarg="integer_width_strategy",
        get_default=lambda spec: spec.integer_width_strategy,
        get_members=lambda spec: spec.integer_width_strategies,
    ),
    "language_version": _Option(
        kwarg="language_version",
        get_default=lambda spec: spec.language_version,
        get_members=lambda spec: spec.version_formats,
    ),
    "numeric_literal_suffix": _Option(
        kwarg="numeric_literal_suffix",
        get_default=lambda spec: spec.numeric_literal_suffix,
        get_members=lambda spec: spec.numeric_literal_suffixes,
    ),
    "numeric_separator": _Option(
        kwarg="numeric_separator",
        get_default=lambda spec: spec.numeric_separator,
        get_members=lambda spec: spec.numeric_separators,
    ),
    "numeric_style": _Option(
        kwarg="numeric_style",
        get_default=lambda spec: spec.numeric_style,
        get_members=lambda spec: spec.numeric_styles,
    ),
    "sequence_format": _Option(
        kwarg="sequence_format",
        get_default=lambda spec: spec.sequence_format,
        get_members=lambda spec: spec.sequence_formats,
    ),
    "set_format": _Option(
        kwarg="set_format",
        get_default=lambda spec: spec.set_format,
        get_members=lambda spec: spec.set_formats,
    ),
    "statement_terminator_style": _Option(
        kwarg="statement_terminator_style",
        get_default=lambda spec: spec.statement_terminator_style,
        get_members=lambda spec: spec.statement_terminator_styles,
    ),
    "string_format": _Option(
        kwarg="string_format",
        get_default=lambda spec: spec.string_format,
        get_members=lambda spec: spec.string_formats,
    ),
    "trailing_comma": _Option(
        kwarg="trailing_comma",
        get_default=lambda spec: spec.trailing_comma,
        get_members=lambda spec: spec.trailing_commas,
    ),
    "union_format": _Option(
        kwarg="union_format",
        get_default=_union_format,
        get_members=_union_formats,
    ),
    "variable_type_hints": _Option(
        kwarg="variable_type_hints",
        get_default=lambda spec: spec.variable_type_hints,
        get_members=lambda spec: spec.variable_type_hints_formats,
    ),
}

_CAPABILITY_FLAGS: Mapping[str, Callable[[literalizer.LanguageCls], bool]] = {
    "declares_call_styles": lambda lang_cls: len(lang_cls.CallStyles) > 0,
    "supports_json_call_result_binding": (
        lambda lang_cls: lang_cls.supports_json_call_result_binding
    ),
    "supports_multiline_string_literals": (
        lambda lang_cls: lang_cls.supports_multiline_string_literals
    ),
    "supports_record_shape_names": (
        lambda lang_cls: lang_cls.supports_record_shape_names
    ),
    "supports_record_struct_name_prefix": (
        lambda lang_cls: lang_cls.supports_record_struct_name_prefix
    ),
    "supports_ref_elements_in_tuple_strategy": (
        lambda lang_cls: (
            lang_cls.variant_metadata.supports_ref_elements_in_tuple_strategy
        )
    ),
    "supports_standalone_comments_in_wrapped_calls": (
        lambda lang_cls: lang_cls.supports_standalone_comments_in_wrapped_calls
    ),
}

_METADATA_FIELDS: Mapping[str, Callable[[LanguageMetadata], str | None]] = {
    "heterogeneous_value_variant_name_language_version": (
        lambda metadata: (
            metadata.variants.heterogeneous_value_variant_name_language_version
        )
    ),
    "heterogeneous_value_variant_name_strategy": (
        lambda metadata: (
            metadata.variants.heterogeneous_value_variant_name_strategy
        )
    ),
}

# Optional spec fields a gate may test for.  A language that cannot
# configure the option omits the constructor field entirely, so field
# presence is the capability test.
_SPEC_FIELDS = frozenset(
    {
        "annotation_evaluation",
        "bool_format",
        "empty_dict_key",
        "union_format",
    }
)

_LANG_PLACEHOLDER = "lang"
_FORMAT_PLACEHOLDER = "format"
_VALUE_PLACEHOLDER = "value"
_TAG_PLACEHOLDER = "tag"
_SECONDARY_PLACEHOLDER = "secondary"


class _CapabilityFlagGate(
    BaseModel,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """Admit languages whose class declares a capability flag."""

    kind: Literal["capability_flag"]
    flag: Annotated[str, Field(min_length=1)]


class _RecordVariantGate(
    BaseModel,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """Admit languages that opt into a focused record variant."""

    kind: Literal["record_variant"]
    variant: RecordVariantName


class _NonDefaultKwargGate(
    BaseModel,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """Admit languages that declare a sample constructor value."""

    kind: Literal["non_default_kwarg"]
    kwarg: Annotated[str, Field(min_length=1)]


class _SpecFieldPresentGate(
    BaseModel,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """Admit languages whose spec exposes an optional field."""

    kind: Literal["spec_field_present"]
    field: Annotated[str, Field(min_length=1)]


class _EnumMemberPresentGate(
    BaseModel,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """Admit languages offering a named member of an option enum."""

    kind: Literal["enum_member_present"]
    option: Annotated[str, Field(min_length=1)]
    member: Annotated[str, Field(min_length=1)]


type _Gate = Annotated[
    _CapabilityFlagGate
    | _RecordVariantGate
    | _NonDefaultKwargGate
    | _SpecFieldPresentGate
    | _EnumMemberPresentGate,
    Field(discriminator="kind"),
]


class _NonDefaultKwargOverride(
    BaseModel,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """Pass a language's declared sample value for one parameter."""

    kind: Literal["non_default_kwarg"]
    kwarg: Annotated[str, Field(min_length=1)]
    name_value: bool = False


class _EnumMemberOverride(
    BaseModel,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """Select a named member of an option enum."""

    kind: Literal["enum_member"]
    option: Annotated[str, Field(min_length=1)]
    member: Annotated[str, Field(min_length=1)]


class _MetadataEnumMemberOverride(
    BaseModel,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """Select the option member a language's metadata names."""

    kind: Literal["metadata_enum_member"]
    option: Annotated[str, Field(min_length=1)]
    field: Annotated[str, Field(min_length=1)]
    optional: bool = False


class _TrueFlagOverride(
    BaseModel,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """Turn on a boolean constructor flag."""

    kind: Literal["true_flag"]
    kwarg: Annotated[str, Field(min_length=1)]


class _RecordShapeNamesOverride(
    BaseModel,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """Name the generated record shape carrying a given key set."""

    kind: Literal["record_shape_names"]
    keys: list[Annotated[str, Field(min_length=1)]]
    name: Annotated[str, Field(min_length=1)]


type _Override = Annotated[
    _NonDefaultKwargOverride
    | _EnumMemberOverride
    | _MetadataEnumMemberOverride
    | _TrueFlagOverride
    | _RecordShapeNamesOverride,
    Field(discriminator="kind"),
]


def _no_gates() -> list[_Gate]:
    """Return a typed empty gate list for the models."""
    return []


def _no_overrides() -> list[_Override]:
    """Return a typed empty override list for the models."""
    return []


def _no_excluded_members() -> list[str]:
    """Return a typed empty exclusion list for the models."""
    return []


class _EveryNonDefaultMemberPlan(
    BaseModel,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """One variant per non-default member of one formatter option."""

    plan: Literal["every_non_default_member"]
    name_template: Annotated[str, Field(min_length=1)]
    option: Annotated[str, Field(min_length=1)]
    excluded_members: list[str] = Field(default_factory=_no_excluded_members)
    declaration_style_sequence_override: bool = False
    per_version: bool = False
    gates: list[_Gate] = Field(default_factory=_no_gates)
    overrides: list[_Override] = Field(default_factory=_no_overrides)


class _FixedOverridesPlan(
    BaseModel,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """One variant per admitted language, from fixed overrides."""

    plan: Literal["fixed_overrides"]
    name_template: Annotated[str, Field(min_length=1)]
    record_language_version: bool = False
    external_record_shape_fixture: bool = False
    per_version: bool = False
    gates: list[_Gate] = Field(default_factory=_no_gates)
    overrides: list[_Override] = Field(default_factory=_no_overrides)


class _CrossSecondary(
    BaseModel,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """One option a cross product pairs with its primary.

    ``tag`` names the pairing in the variant name, so a plan crossing
    several secondary options keeps their variants apart.
    """

    tag: Annotated[str, Field(min_length=1)]
    option: Annotated[str, Field(min_length=1)]
    declaration_style_sequence_override: bool = False


class _CrossProductPlan(
    BaseModel,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """One variant per pairing of two options' non-default members.

    ``primary`` expands over its own non-default members.  Omitting it
    pins the first half of the product to whatever the overrides select,
    as the ``RECORD`` numeric crosses do.
    """

    plan: Literal["cross_product"]
    name_template: Annotated[str, Field(min_length=1)]
    secondaries: Annotated[list[_CrossSecondary], Field(min_length=1)]
    primary: Annotated[str, Field(min_length=1)] | None = None
    excluded_primary_members: list[str] = Field(
        default_factory=_no_excluded_members
    )
    per_version: bool = False
    gates: list[_Gate] = Field(default_factory=_no_gates)
    overrides: list[_Override] = Field(default_factory=_no_overrides)


class _FilteredPlan(
    BaseModel,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """Another axis's variants, narrowed to the languages a gate
    admits.

    The narrowed axis keeps the base axis's variant names and specs, so
    a suite that needs the same expansion for a smaller set of
    languages selects one by name instead of filtering in Python.
    """

    plan: Literal["filtered"]
    base: Annotated[str, Field(min_length=1)]
    gates: list[_Gate] = Field(default_factory=_no_gates)


type _ExpandedAxis = (
    _EveryNonDefaultMemberPlan | _FixedOverridesPlan | _CrossProductPlan
)

type _Axis = Annotated[
    _EveryNonDefaultMemberPlan
    | _FixedOverridesPlan
    | _CrossProductPlan
    | _FilteredPlan,
    Field(discriminator="plan"),
]


class _AxisRegistryData(
    BaseModel,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """Strict representation of the data read directly from TOML."""

    schema_version: Literal[1]
    axes: dict[Annotated[str, Field(min_length=1)], _Axis]


@beartype
def _placeholders(*, template: str) -> frozenset[str]:
    """Return the field names a name template interpolates."""
    parsed = string.Formatter().parse(format_string=template)
    return frozenset(
        field_name for _, field_name, _, _ in parsed if field_name is not None
    )


@beartype
def _validate_options(
    *,
    axis_key: str,
    axis: _ExpandedAxis,
    gate_options: Sequence[str],
) -> None:
    """Check every formatter option an axis names."""
    options = list(gate_options)
    options.extend(
        override.option
        for override in axis.overrides
        if isinstance(
            override,
            _EnumMemberOverride | _MetadataEnumMemberOverride,
        )
    )
    if isinstance(axis, _EveryNonDefaultMemberPlan):
        options.append(axis.option)
        if axis.declaration_style_sequence_override:
            options.append("sequence_format")
    if isinstance(axis, _CrossProductPlan):
        if axis.primary is not None:
            options.append(axis.primary)
        options.extend(secondary.option for secondary in axis.secondaries)
        if any(
            secondary.declaration_style_sequence_override
            for secondary in axis.secondaries
        ):
            options.append("sequence_format")
    unknown = sorted({option for option in options if option not in _OPTIONS})
    if unknown:
        msg = f"axis {axis_key!r}: unknown option {unknown[0]!r}"
        raise AxisPlanError(msg)


@beartype
def _validate_gates(*, axis_key: str, gates: Sequence[_Gate]) -> list[str]:
    """Check every gate an axis declares, returning the options they
    name.
    """
    for gate in gates:
        match gate:
            case _CapabilityFlagGate() if gate.flag not in _CAPABILITY_FLAGS:
                msg = (
                    f"axis {axis_key!r}: unknown capability flag {gate.flag!r}"
                )
                raise AxisPlanError(msg)
            case _SpecFieldPresentGate() if gate.field not in _SPEC_FIELDS:
                msg = f"axis {axis_key!r}: unknown spec field {gate.field!r}"
                raise AxisPlanError(msg)
            case _:
                continue
    return [
        gate.option
        for gate in gates
        if isinstance(gate, _EnumMemberPresentGate)
    ]


@beartype
def _validate_names(*, axis_key: str, axis: _ExpandedAxis) -> None:
    """Check every name an axis uses against its closed registry."""
    _validate_options(
        axis_key=axis_key,
        axis=axis,
        gate_options=_validate_gates(axis_key=axis_key, gates=axis.gates),
    )
    for override in axis.overrides:
        if (
            isinstance(override, _MetadataEnumMemberOverride)
            and override.field not in _METADATA_FIELDS
        ):
            msg = (
                f"axis {axis_key!r}: unknown metadata field {override.field!r}"
            )
            raise AxisPlanError(msg)


@beartype
def _offered_placeholders(*, axis: _ExpandedAxis) -> frozenset[str]:
    """Return the name-template placeholders a plan fills in."""
    match axis:
        case _EveryNonDefaultMemberPlan():
            return frozenset({_LANG_PLACEHOLDER, _FORMAT_PLACEHOLDER})
        case _FixedOverridesPlan():
            return frozenset({_LANG_PLACEHOLDER, _VALUE_PLACEHOLDER})
        case _CrossProductPlan():
            primary = (
                frozenset[str]()
                if axis.primary is None
                else frozenset({_FORMAT_PLACEHOLDER})
            )
            return primary | {
                _LANG_PLACEHOLDER,
                _TAG_PLACEHOLDER,
                _SECONDARY_PLACEHOLDER,
            }
        case _ as unreachable:
            assert_never(unreachable)


@beartype
def _validate_template(*, axis_key: str, axis: _ExpandedAxis) -> None:
    """Check a name template against the placeholders its plan
    offers.
    """
    allowed = _offered_placeholders(axis=axis)
    used = _placeholders(template=axis.name_template)
    unknown = sorted(used - allowed)
    if unknown:
        msg = (
            f"axis {axis_key!r}: unknown name-template placeholder(s) "
            f"{unknown}"
        )
        raise AxisPlanError(msg)
    if isinstance(axis, _CrossProductPlan):
        # Every half of a pairing has to reach the name, or two
        # combinations would claim one golden file.
        missing = sorted(allowed - used - {_LANG_PLACEHOLDER})
        if missing:
            msg = (
                f"axis {axis_key!r}: name template omits placeholder(s) "
                f"{missing}"
            )
            raise AxisPlanError(msg)
    naming = [
        override
        for override in axis.overrides
        if isinstance(override, _RecordShapeNamesOverride)
        or (
            isinstance(override, _NonDefaultKwargOverride)
            and override.name_value
        )
    ]
    wants_value = _VALUE_PLACEHOLDER in used
    if wants_value != (len(naming) == 1):
        msg = (
            f"axis {axis_key!r}: a '{{{_VALUE_PLACEHOLDER}}}' name template "
            "needs exactly one override marked 'name_value'"
        )
        raise AxisPlanError(msg)


@beartype
def _validate_axis(*, axis_key: str, axis: _Axis) -> None:
    """Check one declared axis against the closed name registries."""
    match axis:
        case _FilteredPlan():
            _validate_gates(axis_key=axis_key, gates=axis.gates)
            if axis.base == axis_key:
                msg = f"axis {axis_key!r}: base axis is itself"
                raise AxisPlanError(msg)
            if axis.base not in KNOWN_VARIANT_AXES:
                msg = f"axis {axis_key!r}: unknown base axis {axis.base!r}"
                raise AxisPlanError(msg)
        case (
            _EveryNonDefaultMemberPlan()
            | _FixedOverridesPlan()
            | _CrossProductPlan()
        ):
            _validate_names(axis_key=axis_key, axis=axis)
            _validate_template(axis_key=axis_key, axis=axis)
        case _ as unreachable:
            assert_never(unreachable)


@functools.cache
@beartype
def load_axis_registry(*, path: Path) -> Mapping[str, _Axis]:
    """Return the validated axis registry declared in *path*."""
    try:
        raw = tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        msg = f"{path}: invalid TOML: {exc}"
        raise AxisPlanError(msg) from exc
    try:
        data = _AxisRegistryData.model_validate(obj=raw)
    except ValidationError as exc:
        msg = f"{path}: {exc}"
        raise AxisPlanError(msg) from exc
    for axis_key, axis in data.axes.items():
        _validate_axis(axis_key=axis_key, axis=axis)
    return data.axes


@beartype
def declared_axis_names() -> frozenset[str]:
    """Return every axis name expanded by a declared plan."""
    return frozenset(load_axis_registry(path=AXES_PATH))


@dataclasses.dataclass(frozen=True, kw_only=True)
class _ResolvedOverrides:
    """The constructor kwargs an axis's overrides contribute."""

    kwargs: Mapping[str, object]
    name_value: str | None


@dataclasses.dataclass(frozen=True, kw_only=True)
class _Selection:
    """One option combination an axis selects for a single language."""

    kwargs: Mapping[str, object]
    format_name: str | None
    tag: str | None
    secondary_name: str | None


@dataclasses.dataclass(frozen=True, kw_only=True)
class _PrimaryChoice:
    """One value of a cross product's first half."""

    kwargs: Mapping[str, object]
    format_name: str | None


@beartype
def _gate_admits(
    *,
    gate: _Gate,
    lang_cls: literalizer.LanguageCls,
    metadata: LanguageMetadata,
    default_spec: literalizer.Language,
) -> bool:
    """Return whether *gate* admits a language to its axis."""
    match gate:
        case _CapabilityFlagGate():
            return _CAPABILITY_FLAGS[gate.flag](lang_cls)
        case _RecordVariantGate():
            return gate.variant in metadata.record_variants
        case _NonDefaultKwargGate():
            return gate.kwarg in metadata.non_default_kwargs
        case _SpecFieldPresentGate():
            fields = dataclasses.fields(class_or_instance=default_spec)
            return gate.field in {spec_field.name for spec_field in fields}
        case _EnumMemberPresentGate():
            option = _OPTIONS[gate.option]
            member = find_enum_member(
                enum_cls=option.get_members(default_spec),
                name=gate.member,
            )
            return member is not None
        case _ as unreachable:
            assert_never(unreachable)


@beartype
def _sample_kwarg(
    *,
    axis_key: str,
    kwarg: str,
    metadata: LanguageMetadata,
) -> str:
    """Return a language's declared sample value for a parameter."""
    value = metadata.non_default_kwargs.get(kwarg)
    if value is None:
        msg = (
            f"axis {axis_key!r}: {metadata.path} declares no sample value "
            f"for {kwarg!r}"
        )
        raise AxisPlanError(msg)
    return value


@beartype
def _metadata_member(
    *,
    axis_key: str,
    override: _MetadataEnumMemberOverride,
    metadata: LanguageMetadata,
    default_spec: literalizer.Language,
) -> Mapping[str, object]:
    """Resolve the option member a language's metadata names."""
    option = _OPTIONS[override.option]
    declared = _METADATA_FIELDS[override.field](metadata)
    if declared is None:
        if override.optional:
            return {}
        msg = (
            f"axis {axis_key!r}: {metadata.path} declares no "
            f"{override.field!r}"
        )
        raise AxisPlanError(msg)
    return {
        option.kwarg: enum_member_by_name(
            enum_cls=option.get_members(default_spec),
            name=declared,
        )
    }


@beartype
def _resolve_overrides(
    *,
    axis_key: str,
    overrides: Sequence[_Override],
    metadata: LanguageMetadata,
    default_spec: literalizer.Language,
) -> _ResolvedOverrides:
    """Resolve an axis's declared overrides for one language."""
    kwargs: dict[str, object] = {}
    name_value: str | None = None
    for override in overrides:
        match override:
            case _NonDefaultKwargOverride():
                value = _sample_kwarg(
                    axis_key=axis_key,
                    kwarg=override.kwarg,
                    metadata=metadata,
                )
                kwargs[override.kwarg] = value
                if override.name_value:
                    name_value = value
            case _EnumMemberOverride():
                option = _OPTIONS[override.option]
                kwargs[option.kwarg] = enum_member_by_name(
                    enum_cls=option.get_members(default_spec),
                    name=override.member,
                )
            case _MetadataEnumMemberOverride():
                kwargs.update(
                    _metadata_member(
                        axis_key=axis_key,
                        override=override,
                        metadata=metadata,
                        default_spec=default_spec,
                    )
                )
            case _TrueFlagOverride():
                kwargs[override.kwarg] = True
            case _RecordShapeNamesOverride():
                kwargs["record_shape_names"] = {
                    frozenset(override.keys): override.name
                }
                name_value = override.name
            case _ as unreachable:
                assert_never(unreachable)
    return _ResolvedOverrides(kwargs=kwargs, name_value=name_value)


@beartype
def _build_spec(
    *,
    lang_cls: literalizer.LanguageCls,
    kwargs: Mapping[str, object],
) -> literalizer.Language:
    """Return the spec for *kwargs*, bypassing the cache when needed."""
    if not any(isinstance(value, Mapping) for value in kwargs.values()):
        return make_spec(lang_cls=lang_cls, **kwargs)
    # ``record_shape_names`` is a ``Mapping``, which cannot go in
    # :func:`make_spec`'s ``frozenset`` cache key.  Mirror that
    # function's ``module_name`` default so a language whose
    # ``wrap_in_file`` introduces a named scope keeps the name the rest
    # of the suite builds against.
    spec_kwargs = dict(kwargs)
    if lang_cls.supports_module_name:
        spec_kwargs["module_name"] = lang_cls.module_name_case.convert(
            name="main",
        )
    return lang_cls(**spec_kwargs)


@beartype
def _external_record_shape_prefix(
    *,
    lang_cls: literalizer.LanguageCls,
    metadata: LanguageMetadata,
) -> str:
    """Return the fixture preamble hosting an external record shape."""
    declared = metadata.variants.external_record_shape_fixture_prefix
    if lang_cls.record_shape_names_emit_declarations:
        assert declared is None  # noqa: S101
        return ""
    assert declared is not None  # noqa: S101
    return declared


@beartype
def _record_language_version(
    *,
    metadata: LanguageMetadata,
    default_spec: literalizer.Language,
) -> Mapping[str, object]:
    """Return the language version the record variants select."""
    declared = metadata.variants.record_language_version
    if declared is None:
        return {}
    return {
        "language_version": enum_member_by_name(
            enum_cls=_OPTIONS["language_version"].get_members(default_spec),
            name=declared,
        )
    }


@beartype
def _sequence_format_override(
    *,
    metadata: LanguageMetadata,
    default_spec: literalizer.Language,
    declaration_style: enum.Enum,
) -> Mapping[str, object]:
    """Return the sequence format a declaration style substitutes in."""
    overrides = metadata.declaration_style_sequence_format_overrides
    declared = overrides.get(declaration_style.name)
    if declared is None:
        return {}
    return {
        "sequence_format": enum_member_by_name(
            enum_cls=_OPTIONS["sequence_format"].get_members(default_spec),
            name=declared,
        )
    }


@beartype
def _primary_choices(
    *,
    axis: _CrossProductPlan,
    default_spec: literalizer.Language,
) -> list[_PrimaryChoice]:
    """Return the values a cross product's first half takes."""
    if axis.primary is None:
        return [_PrimaryChoice(kwargs={}, format_name=None)]
    option = _OPTIONS[axis.primary]
    default = option.get_default(default_spec)
    excluded = frozenset(axis.excluded_primary_members)
    return [
        _PrimaryChoice(
            kwargs={option.kwarg: member},
            format_name=member.name.lower(),
        )
        for member in option.get_members(default_spec)
        if member is not default and member.name not in excluded
    ]


@beartype
def _cross_selections(
    *,
    axis: _CrossProductPlan,
    metadata: LanguageMetadata,
    default_spec: literalizer.Language,
) -> list[_Selection]:
    """Return every pairing a cross product selects for one language."""
    selections: list[_Selection] = []
    for primary in _primary_choices(axis=axis, default_spec=default_spec):
        for secondary in axis.secondaries:
            option = _OPTIONS[secondary.option]
            default = option.get_default(default_spec)
            for member in option.get_members(default_spec):
                if member is default:
                    continue
                kwargs: dict[str, object] = {
                    **primary.kwargs,
                    option.kwarg: member,
                }
                if secondary.declaration_style_sequence_override:
                    kwargs.update(
                        _sequence_format_override(
                            metadata=metadata,
                            default_spec=default_spec,
                            declaration_style=member,
                        )
                    )
                selections.append(
                    _Selection(
                        kwargs=kwargs,
                        format_name=primary.format_name,
                        tag=secondary.tag,
                        secondary_name=member.name.lower(),
                    )
                )
    return selections


@beartype
def _selections(
    *,
    axis: _ExpandedAxis,
    metadata: LanguageMetadata,
    default_spec: literalizer.Language,
) -> list[_Selection]:
    """Return the option values an axis selects for one language."""
    match axis:
        case _FixedOverridesPlan():
            return [
                _Selection(
                    kwargs={},
                    format_name=None,
                    tag=None,
                    secondary_name=None,
                )
            ]
        case _CrossProductPlan():
            return _cross_selections(
                axis=axis,
                metadata=metadata,
                default_spec=default_spec,
            )
        case _EveryNonDefaultMemberPlan():
            option = _OPTIONS[axis.option]
            default = option.get_default(default_spec)
            excluded = frozenset(axis.excluded_members)
            selections: list[_Selection] = []
            for member in option.get_members(default_spec):
                if member is default or member.name in excluded:
                    continue
                kwargs: dict[str, object] = {option.kwarg: member}
                if axis.declaration_style_sequence_override:
                    kwargs.update(
                        _sequence_format_override(
                            metadata=metadata,
                            default_spec=default_spec,
                            declaration_style=member,
                        )
                    )
                selections.append(
                    _Selection(
                        kwargs=kwargs,
                        format_name=member.name.lower(),
                        tag=None,
                        secondary_name=None,
                    )
                )
            return selections
        case _ as unreachable:
            assert_never(unreachable)


@beartype
def _language_versions(
    *,
    axis: _ExpandedAxis,
    default_spec: literalizer.Language,
) -> list[Mapping[str, object]]:
    """Return the per-version kwargs an axis repeats itself over."""
    if not axis.per_version:
        return [{}]
    members = _OPTIONS["language_version"].get_members(default_spec)
    return [{"language_version": version} for version in members]


@beartype
def _axis_variants(*, axis_key: str, axis: _ExpandedAxis) -> list[Variant]:
    """Expand one declared axis into its variants."""
    variants: list[Variant] = []
    for lang_cls in sorted_languages():
        metadata = language_metadata(language_id=lang_cls.language_id)
        default_spec = make_spec(lang_cls=lang_cls)
        if not all(
            _gate_admits(
                gate=gate,
                lang_cls=lang_cls,
                metadata=metadata,
                default_spec=default_spec,
            )
            for gate in axis.gates
        ):
            continue
        resolved = _resolve_overrides(
            axis_key=axis_key,
            overrides=axis.overrides,
            metadata=metadata,
            default_spec=default_spec,
        )
        fixture_prefix = ""
        record_version: Mapping[str, object] = {}
        if isinstance(axis, _FixedOverridesPlan):
            if axis.external_record_shape_fixture:
                fixture_prefix = _external_record_shape_prefix(
                    lang_cls=lang_cls,
                    metadata=metadata,
                )
            if axis.record_language_version:
                record_version = _record_language_version(
                    metadata=metadata,
                    default_spec=default_spec,
                )
        for selection in _selections(
            axis=axis,
            metadata=metadata,
            default_spec=default_spec,
        ):
            name = axis.name_template.format(
                lang=lang_cls.__name__,
                format=selection.format_name,
                value=resolved.name_value,
                tag=selection.tag,
                secondary=selection.secondary_name,
            )
            variants.extend(
                Variant(
                    name=name,
                    spec=_build_spec(
                        lang_cls=lang_cls,
                        kwargs={
                            **resolved.kwargs,
                            **selection.kwargs,
                            **record_version,
                            **version,
                        },
                    ),
                    lang_cls=lang_cls,
                    collection_layout=literalizer.CollectionLayout.COMPACT,
                    fixture_prefix=fixture_prefix,
                    record_null_substitutions=None,
                )
                for version in _language_versions(
                    axis=axis,
                    default_spec=default_spec,
                )
            )
    return variants


@beartype
def _filtered_variants(
    *,
    axis: _FilteredPlan,
    base: list[Variant],
) -> list[Variant]:
    """Narrow a base axis's variants to the languages its gates admit."""
    return [
        variant
        for variant in base
        if all(
            _gate_admits(
                gate=gate,
                lang_cls=variant.lang_cls,
                metadata=language_metadata(
                    language_id=variant.lang_cls.language_id
                ),
                default_spec=make_spec(lang_cls=variant.lang_cls),
            )
            for gate in axis.gates
        )
    ]


@beartype
def variants_for_declared_axis(
    *,
    axis_key: str,
    resolve_axis: AxisResolver,
) -> list[Variant]:
    """Return the variants the declared plan for *axis_key* expands
    to.

    A filtered plan narrows another axis, which may itself be an
    escape-hatch builder, so callers supply the suite's full axis
    resolver rather than this module reaching back into it.
    """
    return variants_for_registry_axis(
        path=AXES_PATH,
        axis_key=axis_key,
        resolve_axis=resolve_axis,
    )


@functools.cache
@beartype
def variants_for_registry_axis(
    *,
    path: Path,
    axis_key: str,
    resolve_axis: AxisResolver,
) -> list[Variant]:
    """Return the variants one axis of the registry at *path* expands
    to.
    """
    registry = load_axis_registry(path=path)
    axis = registry.get(axis_key)
    match axis:
        case None:
            msg = (
                f"{path}: no plan declared for variant axis {axis_key!r}; "
                "add one here or register an escape-hatch builder"
            )
            raise AxisPlanError(msg)
        case _FilteredPlan():
            return _filtered_variants(
                axis=axis,
                base=resolve_axis(axis_key=axis.base),
            )
        case _:
            return _axis_variants(axis_key=axis_key, axis=axis)
