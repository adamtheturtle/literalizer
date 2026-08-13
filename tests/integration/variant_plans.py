"""Typed expansion plans for the declared variant axes.

``axes.toml`` names, for each declared axis, one plan from this module
and supplies that plan's parameters.  The plans themselves are typed
Python: the file selects a plan and supplies its parameters, it never
expresses a condition.

Everything a plan looks up by name -- a formatter option, a language
capability flag, a spec field, a rendering behavior flag, a fact about
one option member, a language-metadata field, a language-metadata
sub-table -- resolves through a closed registry declared here, so an
unknown name, an unknown plan, an unknown gate kind, or an unknown
name-template placeholder fails when the registry loads rather than
when a golden file is built.

An axis whose expansion is genuinely irregular stays as a registered
escape-hatch builder in :mod:`variant_escape_hatches`.  A ``filtered``
plan narrows any axis, declared or irregular, to the languages its gates
admit, so a suite needing a smaller slice of an existing expansion names
one rather than writing its own builder.  A plan may also start from another
declared axis, either pairing its own settings with that axis's option
values or reusing its overrides outright.
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
from literalizer.exceptions import IncompatibleFormatsError
from tests.enum_members import enum_member_by_name
from tests.language_gates import (
    CapabilityFlagGate,
    EnumMemberPresentGate,
    SpecFieldPresentGate,
    language_gate_admits,
)
from tests.language_options import CAPABILITY_FLAGS, OPTIONS

from .language_metadata import (
    LanguageMetadata,
    RecordVariantName,
    language_metadata,
)
from .language_specs import make_spec, sorted_languages
from .variant_escape_hatches import ESCAPE_HATCH_VARIANT_AXES
from .variant_types import Variant

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
class _EscapesNullByte(Protocol):
    """An option member declaring how it renders an embedded null byte.

    A JSON value type answers for itself, whatever its language's
    default string formatter does.
    """

    string_literals_escape_null_byte: bool


@beartype
def _comment_suffix(member: enum.Enum) -> bool:
    """Return whether a comment format closes with a terminator."""
    config = member.value
    assert isinstance(config, literalizer.CommentConfig)  # noqa: S101
    return bool(config.suffix)


@beartype
def _escapes_null_byte(member: enum.Enum) -> bool:
    """Return whether a member encodes an embedded null byte."""
    assert isinstance(member, _EscapesNullByte)  # noqa: S101
    return member.string_literals_escape_null_byte


@beartype
def _widens_nested_maps_by_wrapping_scalars(
    spec: literalizer.Language,
) -> bool:
    """Return whether the strategy wraps sibling maps' scalar leaves."""
    behavior = spec.heterogeneous_behavior
    return behavior.widens_nested_maps_by_wrapping_scalars


@beartype
def _widens_unrecordizable_nested_sibling_maps(
    spec: literalizer.Language,
) -> bool:
    """Return whether the strategy widens nested maps no record fits."""
    behavior = spec.heterogeneous_behavior
    return behavior.widens_unrecordizable_nested_sibling_maps


# Facts about one member of an option enum.  Every other registry here
# decides whether a language participates in an axis; these decide which
# of that language's members do, for an axis whose subject is a property
# of the member rather than of the language offering it.
_MEMBER_FLAGS: Mapping[str, Callable[[enum.Enum], bool]] = {
    "comment_suffix": _comment_suffix,
    "string_literals_escape_null_byte": _escapes_null_byte,
}

# Language-owned replacements for the enum member name a plan would
# otherwise put in a variant name.  A language declaring one names its
# variants after the representation rather than the member.
_MEMBER_NAME_SOURCES: Mapping[
    str,
    Callable[[literalizer.LanguageCls], str | None],
] = {
    "json_type_variant_name_suffix": (
        lambda lang_cls: lang_cls.json_type_variant_name_suffix
    ),
}


@beartype
def _empty_container_type_hint_strategy(
    metadata: LanguageMetadata,
) -> str | None:
    """Return the strategy the empty-container hints are declared
    under.
    """
    settings = metadata.variants.empty_container_type_hint
    if settings is None:
        return None
    return settings.heterogeneous_strategy


@beartype
def _empty_container_type_hints(
    metadata: LanguageMetadata,
) -> Mapping[object, object] | None:
    """Return the declared empty-container hints, keyed by value path."""
    settings = metadata.variants.empty_container_type_hint
    if settings is None:
        return None
    return {tuple(entry.path): entry.hint for entry in settings.type_hints}


_METADATA_FIELDS: Mapping[str, Callable[[LanguageMetadata], str | None]] = {
    "empty_container_type_hint_heterogeneous_strategy": (
        _empty_container_type_hint_strategy
    ),
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
    "nested_map_widening": (
        lambda metadata: metadata.variants.nested_map_widening
    ),
    "nested_list_widening": (
        lambda metadata: metadata.variants.nested_list_widening
    ),
}

# Language-metadata fields a plan may put in a variant name.
_NAME_METADATA_FIELDS: Mapping[str, Callable[[LanguageMetadata], str]] = {
    "collection_layout_category": (
        lambda metadata: metadata.golden.collection_layout_category
    ),
}

# Rendering behaviors a strategy either has or has not.  A gate reads
# one from the spec an axis's overrides select, and an override picks
# the option member whose spec has it; the flag is named here once so
# neither spells it itself.
_BEHAVIOR_FLAGS: Mapping[str, Callable[[literalizer.Language], bool]] = {
    "widens_nested_maps_by_wrapping_scalars": (
        _widens_nested_maps_by_wrapping_scalars
    ),
    "widens_unrecordizable_nested_sibling_maps": (
        _widens_unrecordizable_nested_sibling_maps
    ),
}

# Language-declared metadata sub-tables a plan passes through as a
# constructor argument.  A language declaring one participates in the
# axis reading it; the entry here is what turns the declared table into
# the value the constructor takes.
_METADATA_TABLES: Mapping[
    str,
    Callable[[LanguageMetadata], Mapping[object, object] | None],
] = {
    "empty_container_type_hints": _empty_container_type_hints,
}

# Optional fields on a spec's nested format configuration, which a
# language either declares a value for or leaves unset.
_SPEC_CONFIG_FIELDS: Mapping[str, Callable[[literalizer.Language], object]] = {
    "dict_format_config.narrowed_empty_form": (
        lambda spec: spec.dict_format_config.narrowed_empty_form
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
        "json_rendering",
        "json_type",
        "record_map_value_typing",
        "union_format",
    }
)

_LANG_PLACEHOLDER = "lang"
_CATEGORY_PLACEHOLDER = "category"
_FORMAT_PLACEHOLDER = "format"
_VALUE_PLACEHOLDER = "value"
_TAG_PLACEHOLDER = "tag"
_SECONDARY_PLACEHOLDER = "secondary"


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


class _MetadataFieldGate(
    BaseModel,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """Admit languages whose metadata field holds a given value."""

    kind: Literal["metadata_field"]
    field: Annotated[str, Field(min_length=1)]
    value: Annotated[str, Field(min_length=1)]


class _SpecConfigFieldPresentGate(
    BaseModel,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """Admit languages whose spec configuration sets an optional
    field.
    """

    kind: Literal["spec_config_field_present"]
    field: Annotated[str, Field(min_length=1)]


class _BehaviorFlagGate(
    BaseModel,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """Admit languages whose selected strategy sets a behavior flag.

    Unlike every other gate, this one reads the spec an axis's
    overrides build rather than the language default, because the
    behavior it tests belongs to the strategy those overrides select.
    """

    kind: Literal["behavior_flag"]
    flag: Annotated[str, Field(min_length=1)]


type _Gate = Annotated[
    CapabilityFlagGate
    | _RecordVariantGate
    | _NonDefaultKwargGate
    | SpecFieldPresentGate
    | EnumMemberPresentGate
    | _MetadataFieldGate
    | _SpecConfigFieldPresentGate
    | _BehaviorFlagGate,
    Field(discriminator="kind"),
]


# A field default here is what a declared axis means by leaving the
# key out, rather than a value a caller may lean on: an entry supplies
# only what it has an opinion about, and TOML cannot spell the
# ``None`` many of these values take.
class _NonDefaultKwargOverride(  # noqa: NOD001
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


# Defaults stand in for omitted keys, as above.
class _MetadataEnumMemberOverride(  # noqa: NOD001
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


class _MetadataTableOverride(
    BaseModel,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """Pass a language's declared metadata sub-table as a parameter.

    The table is fixture data the language file owns, so a plan names
    which table reaches which constructor parameter and nothing else.
    A language declaring no such table does not participate in the axis,
    so the table that supplies the value also decides who renders it.
    """

    kind: Literal["metadata_table"]
    kwarg: Annotated[str, Field(min_length=1)]
    table: Annotated[str, Field(min_length=1)]


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


class _BehaviorFlagMemberOverride(
    BaseModel,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """Select the option member whose spec sets a behavior flag.

    A language offering no such member does not participate in the
    axis, so the flag that names the member also decides who renders
    it.
    """

    kind: Literal["behavior_flag_member"]
    option: Annotated[str, Field(min_length=1)]
    flag: Annotated[str, Field(min_length=1)]


type _Override = Annotated[
    _NonDefaultKwargOverride
    | _EnumMemberOverride
    | _MetadataEnumMemberOverride
    | _MetadataTableOverride
    | _TrueFlagOverride
    | _RecordShapeNamesOverride
    | _BehaviorFlagMemberOverride,
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


def _no_member_flags() -> list[str]:
    """Return a typed empty member-flag list for the models."""
    return []


# Defaults stand in for omitted keys, as above.
class _LayoutChoice(  # noqa: NOD001
    BaseModel,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """One collection layout an axis renders each variant under."""

    layout: Annotated[str, Field(min_length=1)]
    name_suffix: str = ""


def _compact_layout() -> list[_LayoutChoice]:
    """Return the single compact layout most axes render under."""
    return [_LayoutChoice(layout="COMPACT")]


# Defaults stand in for omitted keys, as above.
class _EveryNonDefaultMemberPlan(  # noqa: NOD001
    BaseModel,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """One variant per non-default member of one formatter option.

    ``unset_member_name`` adds the unset value to the members expanded
    over, under that name, for an option a language may turn off as well
    as choose between.  ``member_name_source`` names the language
    attribute that replaces a member's own name in a variant name.

    ``include_default`` keeps the language's own default member, for an
    axis whose subject is a property some defaults have.
    ``member_flags`` narrows the members to those declaring that
    property, and ``sole_member_name_template`` names the variant of a
    language left with a single member, for an axis where naming that
    member would say nothing.
    """

    plan: Literal["every_non_default_member"]
    name_template: Annotated[str, Field(min_length=1)]
    option: Annotated[str, Field(min_length=1)]
    unset_member_name: Annotated[str, Field(min_length=1)] | None = None
    member_name_source: Annotated[str, Field(min_length=1)] | None = None
    sole_member_name_template: Annotated[str, Field(min_length=1)] | None = (
        None
    )
    include_default: bool = False
    member_flags: list[str] = Field(default_factory=_no_member_flags)
    excluded_members: list[str] = Field(default_factory=_no_excluded_members)
    declaration_style_sequence_override: bool = False
    per_version: bool = False
    layouts: Annotated[list[_LayoutChoice], Field(min_length=1)] = Field(
        default_factory=_compact_layout
    )
    gates: list[_Gate] = Field(default_factory=_no_gates)
    overrides: list[_Override] = Field(default_factory=_no_overrides)


# Defaults stand in for omitted keys, as above.
class _FixedOverridesPlan(  # noqa: NOD001
    BaseModel,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """One variant per admitted language, from fixed overrides.

    ``primary_axis`` repeats those overrides once per variant of another
    axis, which supplies the option value and the ``{format}`` half of
    the name.  ``overrides_from`` reuses another axis's overrides, so a
    setting two axes share is declared once.
    ``name_metadata_field`` fills the ``{category}`` half of the name
    from a language-metadata field.
    """

    plan: Literal["fixed_overrides"]
    name_template: Annotated[str, Field(min_length=1)]
    primary_axis: Annotated[str, Field(min_length=1)] | None = None
    overrides_from: Annotated[str, Field(min_length=1)] | None = None
    name_metadata_field: Annotated[str, Field(min_length=1)] | None = None
    record_language_version: bool = False
    external_record_shape_fixture: bool = False
    per_version: bool = False
    layouts: Annotated[list[_LayoutChoice], Field(min_length=1)] = Field(
        default_factory=_compact_layout
    )
    gates: list[_Gate] = Field(default_factory=_no_gates)
    overrides: list[_Override] = Field(default_factory=_no_overrides)


# Defaults stand in for omitted keys, as above.
class _KwargValueChoice(  # noqa: NOD001
    BaseModel,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """One value the axis passes for its constructor parameter.

    Omitting ``value`` takes the language's own declared sample value
    for the parameter, so a base every participating language shares is
    declared once here and a language-specific one stays in its
    manifest.
    """

    name: Annotated[str, Field(min_length=1)]
    value: Annotated[str, Field(min_length=1)] | None = None


# Defaults stand in for omitted keys, as above.
class _KwargValuesPlan(  # noqa: NOD001
    BaseModel,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """One variant per declared value of one constructor parameter."""

    plan: Literal["kwarg_values"]
    name_template: Annotated[str, Field(min_length=1)]
    kwarg: Annotated[str, Field(min_length=1)]
    values: Annotated[list[_KwargValueChoice], Field(min_length=1)]
    per_version: bool = False
    layouts: Annotated[list[_LayoutChoice], Field(min_length=1)] = Field(
        default_factory=_compact_layout
    )
    gates: list[_Gate] = Field(default_factory=_no_gates)
    overrides: list[_Override] = Field(default_factory=_no_overrides)


# Defaults stand in for omitted keys, as above.
class _CrossSecondary(  # noqa: NOD001
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


# Defaults stand in for omitted keys, as above.
class _CrossProductPlan(  # noqa: NOD001
    BaseModel,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """One variant per pairing of two options' non-default members.

    ``primary`` expands over its own non-default members, and
    ``primary_axis`` instead takes that first half from another declared
    axis, whose variant names the pairing extends.  Omitting both pins
    the first half to whatever the overrides select, as the ``RECORD``
    numeric crosses do.

    ``skip_incompatible_formats`` drops the pairings a language rejects
    upfront, for an option whose members are not all compatible with the
    first half.
    """

    plan: Literal["cross_product"]
    name_template: Annotated[str, Field(min_length=1)]
    secondaries: Annotated[list[_CrossSecondary], Field(min_length=1)]
    primary: Annotated[str, Field(min_length=1)] | None = None
    primary_axis: Annotated[str, Field(min_length=1)] | None = None
    excluded_primary_members: list[str] = Field(
        default_factory=_no_excluded_members
    )
    skip_incompatible_formats: bool = False
    per_version: bool = False
    layouts: Annotated[list[_LayoutChoice], Field(min_length=1)] = Field(
        default_factory=_compact_layout
    )
    gates: list[_Gate] = Field(default_factory=_no_gates)
    overrides: list[_Override] = Field(default_factory=_no_overrides)


# Defaults stand in for omitted keys, as above.
class _FilteredPlan(  # noqa: NOD001
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
    _EveryNonDefaultMemberPlan
    | _FixedOverridesPlan
    | _CrossProductPlan
    | _KwargValuesPlan
)

type _Axis = Annotated[
    _EveryNonDefaultMemberPlan
    | _FixedOverridesPlan
    | _CrossProductPlan
    | _KwargValuesPlan
    | _FilteredPlan,
    Field(discriminator="plan"),
]


class _SpecialAxis(
    BaseModel,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """An axis named by a manifest but assembled with render context."""

    reason: Annotated[str, Field(min_length=1)]


def _no_special_axes() -> dict[str, _SpecialAxis]:
    """Return a typed empty special-axis table for the models."""
    return {}


# Defaults stand in for omitted keys, as above.
class _AxisRegistryData(  # noqa: NOD001
    BaseModel,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """Strict representation of the data read directly from TOML."""

    schema_version: Literal[1]
    axes: dict[Annotated[str, Field(min_length=1)], _Axis]
    special_axes: dict[Annotated[str, Field(min_length=1)], _SpecialAxis] = (
        Field(default_factory=_no_special_axes)
    )


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
            _EnumMemberOverride
            | _MetadataEnumMemberOverride
            | _BehaviorFlagMemberOverride,
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
    unknown = sorted({option for option in options if option not in OPTIONS})
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
            case CapabilityFlagGate() if gate.flag not in CAPABILITY_FLAGS:
                msg = (
                    f"axis {axis_key!r}: unknown capability flag {gate.flag!r}"
                )
                raise AxisPlanError(msg)
            case SpecFieldPresentGate() if gate.field not in _SPEC_FIELDS:
                msg = f"axis {axis_key!r}: unknown spec field {gate.field!r}"
                raise AxisPlanError(msg)
            case _MetadataFieldGate() if gate.field not in _METADATA_FIELDS:
                msg = (
                    f"axis {axis_key!r}: unknown metadata field {gate.field!r}"
                )
                raise AxisPlanError(msg)
            case _SpecConfigFieldPresentGate() if (
                gate.field not in _SPEC_CONFIG_FIELDS
            ):
                msg = (
                    f"axis {axis_key!r}: unknown spec config field "
                    f"{gate.field!r}"
                )
                raise AxisPlanError(msg)
            case _BehaviorFlagGate() if gate.flag not in _BEHAVIOR_FLAGS:
                msg = f"axis {axis_key!r}: unknown behavior flag {gate.flag!r}"
                raise AxisPlanError(msg)
            case _:
                continue
    return [
        gate.option
        for gate in gates
        if isinstance(gate, EnumMemberPresentGate)
    ]


@beartype
def _validate_member_names(
    *,
    axis_key: str,
    axis: _EveryNonDefaultMemberPlan,
) -> None:
    """Check the member-facing names a member expansion declares."""
    if (
        axis.member_name_source is not None
        and axis.member_name_source not in _MEMBER_NAME_SOURCES
    ):
        msg = (
            f"axis {axis_key!r}: unknown member name source "
            f"{axis.member_name_source!r}"
        )
        raise AxisPlanError(msg)
    unknown = sorted(
        flag for flag in axis.member_flags if flag not in _MEMBER_FLAGS
    )
    if unknown:
        msg = f"axis {axis_key!r}: unknown member flag {unknown[0]!r}"
        raise AxisPlanError(msg)


@beartype
def _validate_names(*, axis_key: str, axis: _ExpandedAxis) -> None:
    """Check every name an axis uses against its closed registry."""
    _validate_options(
        axis_key=axis_key,
        axis=axis,
        gate_options=_validate_gates(axis_key=axis_key, gates=axis.gates),
    )
    if (
        isinstance(axis, _CrossProductPlan)
        and axis.primary is not None
        and axis.primary_axis is not None
    ):
        msg = (
            f"axis {axis_key!r}: declares both a 'primary' option and a "
            "'primary_axis'"
        )
        raise AxisPlanError(msg)
    if isinstance(axis, _EveryNonDefaultMemberPlan):
        _validate_member_names(axis_key=axis_key, axis=axis)
    if (
        isinstance(axis, _FixedOverridesPlan)
        and axis.name_metadata_field is not None
        and axis.name_metadata_field not in _NAME_METADATA_FIELDS
    ):
        msg = (
            f"axis {axis_key!r}: unknown name metadata field "
            f"{axis.name_metadata_field!r}"
        )
        raise AxisPlanError(msg)
    for layout in axis.layouts:
        if layout.layout not in literalizer.CollectionLayout.__members__:
            msg = f"axis {axis_key!r}: unknown layout {layout.layout!r}"
            raise AxisPlanError(msg)
    for override in axis.overrides:
        if (
            isinstance(override, _MetadataEnumMemberOverride)
            and override.field not in _METADATA_FIELDS
        ):
            msg = (
                f"axis {axis_key!r}: unknown metadata field {override.field!r}"
            )
            raise AxisPlanError(msg)
        if (
            isinstance(override, _MetadataTableOverride)
            and override.table not in _METADATA_TABLES
        ):
            msg = (
                f"axis {axis_key!r}: unknown metadata table {override.table!r}"
            )
            raise AxisPlanError(msg)
        if (
            isinstance(override, _BehaviorFlagMemberOverride)
            and override.flag not in _BEHAVIOR_FLAGS
        ):
            msg = f"axis {axis_key!r}: unknown behavior flag {override.flag!r}"
            raise AxisPlanError(msg)


@beartype
def _offered_placeholders(*, axis: _ExpandedAxis) -> frozenset[str]:
    """Return the name-template placeholders a plan fills in."""
    match axis:
        case _EveryNonDefaultMemberPlan() | _KwargValuesPlan():
            return frozenset({_LANG_PLACEHOLDER, _FORMAT_PLACEHOLDER})
        case _FixedOverridesPlan():
            named = frozenset({_LANG_PLACEHOLDER, _VALUE_PLACEHOLDER})
            if axis.primary_axis is not None:
                named |= {_FORMAT_PLACEHOLDER}
            if axis.name_metadata_field is not None:
                named |= {_CATEGORY_PLACEHOLDER}
            return named
        case _CrossProductPlan():
            primary = (
                frozenset[str]()
                if axis.primary is None and axis.primary_axis is None
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
def _validate_sole_member_template(
    *,
    axis_key: str,
    axis: _EveryNonDefaultMemberPlan,
    allowed: frozenset[str],
) -> None:
    """Check the name template for a language left with one member.

    That template names the whole variant, so it answers to the same
    placeholder registry as any other, minus the member name it exists
    to leave out.
    """
    if axis.sole_member_name_template is None:
        return
    unknown = sorted(
        _placeholders(template=axis.sole_member_name_template)
        - (allowed - {_FORMAT_PLACEHOLDER})
    )
    if unknown:
        msg = (
            f"axis {axis_key!r}: unknown sole-member name-template "
            f"placeholder(s) {unknown}"
        )
        raise AxisPlanError(msg)


@beartype
def _required_placeholders(*, axis: _ExpandedAxis) -> frozenset[str]:
    """Return the placeholders a plan's name template has to use.

    Whatever tells one variant of an axis from another has to reach the
    name, or the two would claim one golden file.
    """
    required = frozenset[str]()
    if isinstance(axis, _KwargValuesPlan):
        required |= {_FORMAT_PLACEHOLDER}
    if isinstance(axis, _FixedOverridesPlan):
        if axis.primary_axis is not None:
            required |= {_FORMAT_PLACEHOLDER}
        if axis.name_metadata_field is not None:
            required |= {_CATEGORY_PLACEHOLDER}
    return required


@beartype
def _validate_template(*, axis_key: str, axis: _ExpandedAxis) -> None:
    """Check a name template against the placeholders its plan
    offers.
    """
    allowed = _offered_placeholders(axis=axis)
    used = _placeholders(template=axis.name_template)
    if isinstance(axis, _EveryNonDefaultMemberPlan):
        _validate_sole_member_template(
            axis_key=axis_key,
            axis=axis,
            allowed=allowed,
        )
    unknown = sorted(used - allowed)
    if unknown:
        msg = (
            f"axis {axis_key!r}: unknown name-template placeholder(s) "
            f"{unknown}"
        )
        raise AxisPlanError(msg)
    omitted = sorted(_required_placeholders(axis=axis) - used)
    if omitted:
        msg = (
            f"axis {axis_key!r}: name template omits placeholder(s) {omitted}"
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
def _primary_axis_plan(
    *,
    axis_key: str,
    primary_axis: str,
    axes: Mapping[str, _Axis],
) -> _EveryNonDefaultMemberPlan:
    """Return the axis a plan takes the first half of its pairings
    from.

    Only a member expansion can supply that half: the pairing repeats
    one option's members, and carries neither the base's overrides nor
    its name template.
    """
    base = axes.get(primary_axis)
    if not isinstance(base, _EveryNonDefaultMemberPlan):
        msg = (
            f"axis {axis_key!r}: primary axis {primary_axis!r} is not a "
            "declared 'every_non_default_member' axis"
        )
        raise AxisPlanError(msg)
    if base.overrides:
        msg = (
            f"axis {axis_key!r}: primary axis {primary_axis!r} declares "
            "overrides, which a pairing does not carry"
        )
        raise AxisPlanError(msg)
    return base


@beartype
def _primary_plan_for(
    *,
    axis_key: str,
    axis: _ExpandedAxis,
    axes: Mapping[str, _Axis],
) -> _EveryNonDefaultMemberPlan | None:
    """Return the axis *axis* pairs its overrides and secondaries
    with.
    """
    if isinstance(axis, _EveryNonDefaultMemberPlan | _KwargValuesPlan) or (
        axis.primary_axis is None
    ):
        return None
    return _primary_axis_plan(
        axis_key=axis_key,
        primary_axis=axis.primary_axis,
        axes=axes,
    )


@beartype
def _shared_overrides(
    *,
    axis_key: str,
    overrides_from: str,
    axes: Mapping[str, _Axis],
) -> list[_Override]:
    """Return the overrides an axis reuses from another axis."""
    source = axes.get(overrides_from)
    if not isinstance(
        source,
        _EveryNonDefaultMemberPlan | _FixedOverridesPlan | _CrossProductPlan,
    ):
        msg = f"axis {axis_key!r}: unknown overrides source {overrides_from!r}"
        raise AxisPlanError(msg)
    if isinstance(source, _FixedOverridesPlan) and (
        source.overrides_from is not None
    ):
        msg = (
            f"axis {axis_key!r}: overrides source {overrides_from!r} reuses "
            "overrides itself"
        )
        raise AxisPlanError(msg)
    return source.overrides


@beartype
def _resolved_axis(
    *,
    axis_key: str,
    axis: _Axis,
    axes: Mapping[str, _Axis],
) -> _Axis:
    """Return *axis* with any reused overrides spliced in.

    Reuse is resolved once, when the registry loads, so everything
    downstream sees one override list however it was declared.
    """
    if not isinstance(axis, _FixedOverridesPlan) or (
        axis.overrides_from is None
    ):
        return axis
    shared = _shared_overrides(
        axis_key=axis_key,
        overrides_from=axis.overrides_from,
        axes=axes,
    )
    return axis.model_copy(
        update={
            "overrides": [*shared, *axis.overrides],
            "overrides_from": None,
        }
    )


@beartype
def _validate_references(
    *,
    axis_key: str,
    axis: _Axis,
    axes: Mapping[str, _Axis],
) -> None:
    """Check the axes one axis names against the loaded registry."""
    if isinstance(axis, _FixedOverridesPlan | _CrossProductPlan) and (
        axis.primary_axis is not None
    ):
        _primary_axis_plan(
            axis_key=axis_key,
            primary_axis=axis.primary_axis,
            axes=axes,
        )


@beartype
def _validate_axis(
    *,
    axis_key: str,
    axis: _Axis,
    axes: Mapping[str, _Axis],
) -> None:
    """Check one declared axis against the closed name registries."""
    match axis:
        case _FilteredPlan():
            _validate_gates(axis_key=axis_key, gates=axis.gates)
            if axis.base == axis_key:
                msg = f"axis {axis_key!r}: base axis is itself"
                raise AxisPlanError(msg)
            if axis.base not in axes.keys() | ESCAPE_HATCH_VARIANT_AXES:
                msg = f"axis {axis_key!r}: unknown base axis {axis.base!r}"
                raise AxisPlanError(msg)
        case (
            _EveryNonDefaultMemberPlan()
            | _FixedOverridesPlan()
            | _CrossProductPlan()
            | _KwargValuesPlan()
        ):
            _validate_names(axis_key=axis_key, axis=axis)
            _validate_template(axis_key=axis_key, axis=axis)
        case _ as unreachable:
            assert_never(unreachable)


@functools.cache
@beartype
def _registry_data(*, path: Path) -> _AxisRegistryData:
    """Return the registry declared in *path*, parsed and typed."""
    try:
        raw = tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        msg = f"{path}: invalid TOML: {exc}"
        raise AxisPlanError(msg) from exc
    try:
        return _AxisRegistryData.model_validate(obj=raw)
    except ValidationError as exc:
        msg = f"{path}: {exc}"
        raise AxisPlanError(msg) from exc


@functools.cache
@beartype
def load_axis_registry(*, path: Path) -> Mapping[str, _Axis]:
    """Return the validated expansion plans declared in *path*."""
    data = _registry_data(path=path)
    axes = {
        axis_key: _resolved_axis(
            axis_key=axis_key,
            axis=axis,
            axes=data.axes,
        )
        for axis_key, axis in data.axes.items()
    }
    for axis_key, axis in axes.items():
        _validate_axis(axis_key=axis_key, axis=axis, axes=axes)
        _validate_references(axis_key=axis_key, axis=axis, axes=axes)
    return axes


@beartype
def declared_axis_names() -> frozenset[str]:
    """Return every axis name expanded by a declared plan."""
    return frozenset(load_axis_registry(path=AXES_PATH))


@beartype
def special_axis_names() -> frozenset[str]:
    """Return every axis name whose cases carry their own render context.

    These axes name an input rather than an expansion: a builder in
    :mod:`variant_cases` assembles their cases, so no plan expands them.
    """
    return frozenset(_registry_data(path=AXES_PATH).special_axes)


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


@dataclasses.dataclass(frozen=True, kw_only=True)
class _MemberExpansion:
    """How an axis walks one option's members into named values."""

    option_key: str
    excluded_members: frozenset[str]
    member_flags: tuple[str, ...]
    include_default: bool
    unset_member_name: str | None
    member_name_source: str | None
    declaration_style_sequence_override: bool


@beartype
def _gate_admits(
    *,
    gate: _Gate,
    lang_cls: literalizer.LanguageCls,
    metadata: LanguageMetadata,
    spec: literalizer.Language,
) -> bool:
    """Return whether *gate* admits a language to its axis.

    *spec* is the language default for every gate but
    :class:`_BehaviorFlagGate`, which reads the spec built from the
    axis's overrides.
    """
    match gate:
        case (
            CapabilityFlagGate()
            | SpecFieldPresentGate()
            | EnumMemberPresentGate()
        ):
            admits = language_gate_admits(
                gate=gate,
                lang_cls=lang_cls,
                spec=spec,
            )
        case _RecordVariantGate():
            admits = gate.variant in metadata.record_variants
        case _NonDefaultKwargGate():
            admits = gate.kwarg in metadata.non_default_kwargs
        case _MetadataFieldGate():
            admits = _METADATA_FIELDS[gate.field](metadata) == gate.value
        case _SpecConfigFieldPresentGate():
            admits = _SPEC_CONFIG_FIELDS[gate.field](spec) is not None
        case _BehaviorFlagGate():
            admits = _BEHAVIOR_FLAGS[gate.flag](spec)
        case _ as unreachable:
            assert_never(unreachable)
    return admits


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
    option = OPTIONS[override.option]
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
def _metadata_table(
    *,
    override: _MetadataTableOverride,
    metadata: LanguageMetadata,
) -> Mapping[str, object] | None:
    """Resolve the metadata sub-table a language declares.

    Returns ``None`` for a language declaring no such table, which is
    how this override excludes it from the axis.
    """
    declared = _METADATA_TABLES[override.table](metadata)
    if declared is None:
        return None
    return {override.kwarg: declared}


@beartype
def _behavior_flag_member(
    *,
    override: _BehaviorFlagMemberOverride,
    lang_cls: literalizer.LanguageCls,
    default_spec: literalizer.Language,
) -> enum.Enum | None:
    """Return the option member whose spec sets a behavior flag."""
    option = OPTIONS[override.option]
    has_flag = _BEHAVIOR_FLAGS[override.flag]
    for member in option.get_members(default_spec):
        spec = make_spec(lang_cls=lang_cls, **{option.kwarg: member})
        if has_flag(spec):
            return member
    return None


@beartype
def _override_selection(
    *,
    axis_key: str,
    override: _Override,
    lang_cls: literalizer.LanguageCls,
    metadata: LanguageMetadata,
    default_spec: literalizer.Language,
) -> _ResolvedOverrides | None:
    """Resolve one declared override for one language."""
    resolved: _ResolvedOverrides | None
    match override:
        case _NonDefaultKwargOverride():
            value = _sample_kwarg(
                axis_key=axis_key,
                kwarg=override.kwarg,
                metadata=metadata,
            )
            resolved = _ResolvedOverrides(
                kwargs={override.kwarg: value},
                name_value=value if override.name_value else None,
            )
        case _EnumMemberOverride():
            option = OPTIONS[override.option]
            resolved = _ResolvedOverrides(
                kwargs={
                    option.kwarg: enum_member_by_name(
                        enum_cls=option.get_members(default_spec),
                        name=override.member,
                    )
                },
                name_value=None,
            )
        case _MetadataEnumMemberOverride():
            resolved = _ResolvedOverrides(
                kwargs=_metadata_member(
                    axis_key=axis_key,
                    override=override,
                    metadata=metadata,
                    default_spec=default_spec,
                ),
                name_value=None,
            )
        case _MetadataTableOverride():
            table = _metadata_table(override=override, metadata=metadata)
            resolved = (
                None
                if table is None
                else _ResolvedOverrides(kwargs=table, name_value=None)
            )
        case _TrueFlagOverride():
            resolved = _ResolvedOverrides(
                kwargs={override.kwarg: True},
                name_value=None,
            )
        case _RecordShapeNamesOverride():
            resolved = _ResolvedOverrides(
                kwargs={
                    "record_shape_names": {
                        frozenset(override.keys): override.name
                    }
                },
                name_value=override.name,
            )
        case _BehaviorFlagMemberOverride():
            member = _behavior_flag_member(
                override=override,
                lang_cls=lang_cls,
                default_spec=default_spec,
            )
            resolved = (
                None
                if member is None
                else _ResolvedOverrides(
                    kwargs={OPTIONS[override.option].kwarg: member},
                    name_value=None,
                )
            )
        case _ as unreachable:
            assert_never(unreachable)
    return resolved


@beartype
def _resolve_overrides(
    *,
    axis_key: str,
    overrides: Sequence[_Override],
    lang_cls: literalizer.LanguageCls,
    metadata: LanguageMetadata,
    default_spec: literalizer.Language,
) -> _ResolvedOverrides | None:
    """Resolve an axis's declared overrides for one language.

    Returns ``None`` when a ``behavior_flag_member`` override finds no
    member to select, or a ``metadata_table`` override finds no declared
    table, which is how those overrides exclude a language.  An override
    that excludes stops the rest of the list, so one naming a table
    comes before any override reading that table's own fields.
    """
    kwargs: dict[str, object] = {}
    name_value: str | None = None
    for override in overrides:
        resolved = _override_selection(
            axis_key=axis_key,
            override=override,
            lang_cls=lang_cls,
            metadata=metadata,
            default_spec=default_spec,
        )
        if resolved is None:
            return None
        kwargs.update(resolved.kwargs)
        if resolved.name_value is not None:
            name_value = resolved.name_value
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
            enum_cls=OPTIONS["language_version"].get_members(default_spec),
            name=declared,
        )
    }


@beartype
def sequence_format_override(
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
            enum_cls=OPTIONS["sequence_format"].get_members(default_spec),
            name=declared,
        )
    }


@beartype
def _member_expansion(*, axis: _EveryNonDefaultMemberPlan) -> _MemberExpansion:
    """Return how a declared member expansion walks its option."""
    return _MemberExpansion(
        option_key=axis.option,
        excluded_members=frozenset(axis.excluded_members),
        member_flags=tuple(axis.member_flags),
        include_default=axis.include_default,
        unset_member_name=axis.unset_member_name,
        member_name_source=axis.member_name_source,
        declaration_style_sequence_override=(
            axis.declaration_style_sequence_override
        ),
    )


@beartype
def _member_name(
    *,
    expansion: _MemberExpansion,
    lang_cls: literalizer.LanguageCls,
    member: enum.Enum,
) -> str:
    """Return the name a selected member contributes to a variant
    name.
    """
    if expansion.member_name_source is None:
        return member.name.lower()
    source = _MEMBER_NAME_SOURCES[expansion.member_name_source]
    declared = source(lang_cls)
    if declared is None:
        return member.name.lower()
    return declared


@beartype
def _member_choices(
    *,
    expansion: _MemberExpansion,
    lang_cls: literalizer.LanguageCls,
    metadata: LanguageMetadata,
    default_spec: literalizer.Language,
) -> list[_PrimaryChoice]:
    """Return the values one option takes for a single language."""
    option = OPTIONS[expansion.option_key]
    default = option.get_default(default_spec)
    choices: list[_PrimaryChoice] = []
    if expansion.unset_member_name is not None and default is not None:
        choices.append(
            _PrimaryChoice(
                kwargs={option.kwarg: None},
                format_name=expansion.unset_member_name,
            )
        )
    for member in option.get_members(default_spec):
        if member is default and not expansion.include_default:
            continue
        if member.name in expansion.excluded_members:
            continue
        if not all(
            _MEMBER_FLAGS[flag](member) for flag in expansion.member_flags
        ):
            continue
        kwargs: dict[str, object] = {option.kwarg: member}
        if expansion.declaration_style_sequence_override:
            kwargs.update(
                sequence_format_override(
                    metadata=metadata,
                    default_spec=default_spec,
                    declaration_style=member,
                )
            )
        choices.append(
            _PrimaryChoice(
                kwargs=kwargs,
                format_name=_member_name(
                    expansion=expansion,
                    lang_cls=lang_cls,
                    member=member,
                ),
            )
        )
    return choices


@beartype
def _primary_choices(
    *,
    axis: _CrossProductPlan,
    primary_plan: _EveryNonDefaultMemberPlan | None,
    lang_cls: literalizer.LanguageCls,
    metadata: LanguageMetadata,
    default_spec: literalizer.Language,
) -> list[_PrimaryChoice]:
    """Return the values a cross product's first half takes."""
    if primary_plan is not None:
        return _member_choices(
            expansion=_member_expansion(axis=primary_plan),
            lang_cls=lang_cls,
            metadata=metadata,
            default_spec=default_spec,
        )
    if axis.primary is None:
        return [_PrimaryChoice(kwargs={}, format_name=None)]
    return _member_choices(
        expansion=_MemberExpansion(
            option_key=axis.primary,
            excluded_members=frozenset(axis.excluded_primary_members),
            member_flags=(),
            include_default=False,
            unset_member_name=None,
            member_name_source=None,
            declaration_style_sequence_override=False,
        ),
        lang_cls=lang_cls,
        metadata=metadata,
        default_spec=default_spec,
    )


@beartype
def _cross_selections(
    *,
    axis: _CrossProductPlan,
    primary_plan: _EveryNonDefaultMemberPlan | None,
    lang_cls: literalizer.LanguageCls,
    metadata: LanguageMetadata,
    default_spec: literalizer.Language,
) -> list[_Selection]:
    """Return every pairing a cross product selects for one language."""
    selections: list[_Selection] = []
    for primary in _primary_choices(
        axis=axis,
        primary_plan=primary_plan,
        lang_cls=lang_cls,
        metadata=metadata,
        default_spec=default_spec,
    ):
        for secondary in axis.secondaries:
            option = OPTIONS[secondary.option]
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
                        sequence_format_override(
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
def _choice_selections(*, choices: list[_PrimaryChoice]) -> list[_Selection]:
    """Return one unpaired selection per option value."""
    return [
        _Selection(
            kwargs=choice.kwargs,
            format_name=choice.format_name,
            tag=None,
            secondary_name=None,
        )
        for choice in choices
    ]


@beartype
def _kwarg_value_selections(
    *,
    axis_key: str,
    axis: _KwargValuesPlan,
    metadata: LanguageMetadata,
) -> list[_Selection]:
    """Return the parameter values an axis passes for one language."""
    return [
        _Selection(
            kwargs={
                axis.kwarg: (
                    _sample_kwarg(
                        axis_key=axis_key,
                        kwarg=axis.kwarg,
                        metadata=metadata,
                    )
                    if choice.value is None
                    else choice.value
                )
            },
            format_name=choice.name,
            tag=None,
            secondary_name=None,
        )
        for choice in axis.values
    ]


@beartype
def _selections(
    *,
    axis_key: str,
    axis: _ExpandedAxis,
    primary_plan: _EveryNonDefaultMemberPlan | None,
    lang_cls: literalizer.LanguageCls,
    metadata: LanguageMetadata,
    default_spec: literalizer.Language,
) -> list[_Selection]:
    """Return the option values an axis selects for one language."""
    match axis:
        case _KwargValuesPlan():
            return _kwarg_value_selections(
                axis_key=axis_key,
                axis=axis,
                metadata=metadata,
            )
        case _FixedOverridesPlan() if primary_plan is not None:
            return _choice_selections(
                choices=_member_choices(
                    expansion=_member_expansion(axis=primary_plan),
                    lang_cls=lang_cls,
                    metadata=metadata,
                    default_spec=default_spec,
                )
            )
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
                primary_plan=primary_plan,
                lang_cls=lang_cls,
                metadata=metadata,
                default_spec=default_spec,
            )
        case _EveryNonDefaultMemberPlan():
            return _choice_selections(
                choices=_member_choices(
                    expansion=_member_expansion(axis=axis),
                    lang_cls=lang_cls,
                    metadata=metadata,
                    default_spec=default_spec,
                )
            )
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
    members = OPTIONS["language_version"].get_members(default_spec)
    return [{"language_version": version} for version in members]


@beartype
def _paired_spec(
    *,
    axis: _ExpandedAxis,
    lang_cls: literalizer.LanguageCls,
    kwargs: Mapping[str, object],
) -> literalizer.Language | None:
    """Return the spec for one pairing, or ``None`` if rejected.

    A cross product may pair option members a language rejects upfront;
    such a pairing has no golden file rather than a failing one.
    """
    skips = isinstance(axis, _CrossProductPlan) and (
        axis.skip_incompatible_formats
    )
    if not skips:
        return _build_spec(lang_cls=lang_cls, kwargs=kwargs)
    try:
        return _build_spec(lang_cls=lang_cls, kwargs=kwargs)
    except IncompatibleFormatsError:
        return None


@beartype
def _name_category(
    *,
    axis: _ExpandedAxis,
    metadata: LanguageMetadata,
) -> str | None:
    """Return the metadata-supplied half of a variant name."""
    if not isinstance(axis, _FixedOverridesPlan) or (
        axis.name_metadata_field is None
    ):
        return None
    return _NAME_METADATA_FIELDS[axis.name_metadata_field](metadata)


@beartype
def _name_template(
    *,
    axis: _ExpandedAxis,
    selections: Sequence[_Selection],
) -> str:
    """Return the name template an axis uses for one language.

    An axis declaring a sole-member template uses it for a language
    whose members narrow to one, where naming that member would say
    nothing about the variant.
    """
    if (
        isinstance(axis, _EveryNonDefaultMemberPlan)
        and axis.sole_member_name_template is not None
        and len(selections) == 1
    ):
        return axis.sole_member_name_template
    return axis.name_template


@beartype
def _admitted_overrides(
    *,
    axis_key: str,
    overrides: Sequence[_Override],
    gates: Sequence[_Gate],
    lang_cls: literalizer.LanguageCls,
    metadata: LanguageMetadata,
    default_spec: literalizer.Language,
) -> _ResolvedOverrides | None:
    """Return one language's resolved overrides, or ``None``.

    A behavior-flag gate reads the spec the overrides build, so the
    two are resolved together: the gates that decide on the language
    alone run first, then the overrides, then the gates that decide on
    what those overrides selected.
    """
    admits = functools.partial(
        _gate_admits,
        lang_cls=lang_cls,
        metadata=metadata,
    )
    behavior_gates = [
        gate for gate in gates if isinstance(gate, _BehaviorFlagGate)
    ]
    language_gates = [
        gate for gate in gates if not isinstance(gate, _BehaviorFlagGate)
    ]
    if not all(
        admits(gate=gate, spec=default_spec) for gate in language_gates
    ):
        return None
    resolved = _resolve_overrides(
        axis_key=axis_key,
        overrides=overrides,
        lang_cls=lang_cls,
        metadata=metadata,
        default_spec=default_spec,
    )
    if resolved is None:
        return None
    if not all(
        admits(
            gate=gate,
            spec=_build_spec(lang_cls=lang_cls, kwargs=resolved.kwargs),
        )
        for gate in behavior_gates
    ):
        return None
    return resolved


@dataclasses.dataclass(frozen=True, kw_only=True)
class _FixtureContext:
    """What an axis pins about the fixture hosting its variants."""

    fixture_prefix: str
    record_version: Mapping[str, object]


@beartype
def _fixture_context(
    *,
    axis: _ExpandedAxis,
    lang_cls: literalizer.LanguageCls,
    metadata: LanguageMetadata,
    default_spec: literalizer.Language,
) -> _FixtureContext:
    """Return the fixture preamble and record version an axis pins."""
    if not isinstance(axis, _FixedOverridesPlan):
        return _FixtureContext(fixture_prefix="", record_version={})
    return _FixtureContext(
        fixture_prefix=(
            _external_record_shape_prefix(
                lang_cls=lang_cls,
                metadata=metadata,
            )
            if axis.external_record_shape_fixture
            else ""
        ),
        record_version=(
            _record_language_version(
                metadata=metadata,
                default_spec=default_spec,
            )
            if axis.record_language_version
            else {}
        ),
    )


@beartype
def _axis_variants(
    *,
    axis_key: str,
    axis: _ExpandedAxis,
    primary_plan: _EveryNonDefaultMemberPlan | None,
) -> list[Variant]:
    """Expand one declared axis into its variants."""
    variants: list[Variant] = []
    primary_gates = [] if primary_plan is None else primary_plan.gates
    for lang_cls in sorted_languages():
        metadata = language_metadata(language_id=lang_cls.language_id)
        default_spec = make_spec(lang_cls=lang_cls)
        resolved = _admitted_overrides(
            axis_key=axis_key,
            overrides=axis.overrides,
            gates=[*primary_gates, *axis.gates],
            lang_cls=lang_cls,
            metadata=metadata,
            default_spec=default_spec,
        )
        if resolved is None:
            continue
        fixture = _fixture_context(
            axis=axis,
            lang_cls=lang_cls,
            metadata=metadata,
            default_spec=default_spec,
        )
        selections = _selections(
            axis_key=axis_key,
            axis=axis,
            primary_plan=primary_plan,
            lang_cls=lang_cls,
            metadata=metadata,
            default_spec=default_spec,
        )
        template = _name_template(axis=axis, selections=selections)
        for selection in selections:
            name = template.format(
                lang=lang_cls.__name__,
                category=_name_category(axis=axis, metadata=metadata),
                format=selection.format_name,
                value=resolved.name_value,
                tag=selection.tag,
                secondary=selection.secondary_name,
            )
            seen_versions: set[enum.Enum] = set()
            for version in _language_versions(
                axis=axis,
                default_spec=default_spec,
            ):
                spec = _paired_spec(
                    axis=axis,
                    lang_cls=lang_cls,
                    kwargs={
                        **resolved.kwargs,
                        **selection.kwargs,
                        **fixture.record_version,
                        **version,
                    },
                )
                # Two declared versions may resolve to one effective
                # version once the axis's overrides raise the floor, as
                # Java's ``JDK_11`` does under ``RECORD``; the pair
                # renders one golden file, not two.
                if spec is None or spec.language_version in seen_versions:
                    continue
                seen_versions.add(spec.language_version)
                variants.extend(
                    Variant(
                        name=f"{name}{layout.name_suffix}",
                        spec=spec,
                        lang_cls=lang_cls,
                        collection_layout=literalizer.CollectionLayout[
                            layout.layout
                        ],
                        fixture_prefix=fixture.fixture_prefix,
                        record_null_substitutions=None,
                    )
                    for layout in axis.layouts
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
                spec=variant.spec,
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
            return _axis_variants(
                axis_key=axis_key,
                axis=axis,
                primary_plan=_primary_plan_for(
                    axis_key=axis_key,
                    axis=axis,
                    axes=registry,
                ),
            )
