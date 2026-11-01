"""Load and validate language-independent rejection scenarios.

A manifest describes input values and API options. The suite records how
each applicable language handles that scenario, including both accepted
calls and exact errors. Capability gates and enum declarations determine
which combinations apply, so new implementations join without owner lists.

The manifest never carries the message a language raises with.  That
is kept in a golden file next to the manifest, which is itself TOML so
that a malformed one fails the repository's own TOML check.
"""

from __future__ import annotations

import dataclasses
import functools
import string
import sys
import tomllib
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Annotated, Literal, Self, assert_never

from beartype import beartype
from pydantic import (
    BaseModel,
    BeforeValidator,
    Field,
    ValidationError,
    model_validator,
)

import literalizer
from literalizer import exceptions as literalizer_exceptions
from literalizer.languages import ALL_LANGUAGES
from tests.integration.case_manifests import RefTimeInput
from tests.language_gates import (
    CapabilityFlagGate,
    EnumMemberPresentGate,
    LanguageGate,
)
from tests.language_options import CAPABILITY_FLAGS, OPTIONS
from tests.native_value_sources import RefDatetimeInput, RefValueSource

REJECTIONS_DIR = Path(__file__).parent / "rejections"
"""Where the declared rejections live."""

MANIFEST_NAME = "rejection.toml"
GOLDEN_NAME = "expected.toml"

VALUE_PLACEHOLDER = "value"
"""The only placeholder a manifest's constructor arguments substitute."""

_CALL_TRANSFORM_PLACEHOLDERS = frozenset({"call", "zipped"})
"""Names a rejection-manifest call transform may substitute."""

type ApiName = Literal[
    "literalize",
    "literalize_call",
    "literalize_call_with_declarations",
    "constructor",
    "sequence_type_annotation",
    "declaration_formatter",
]
type VariableFormName = Literal["new", "existing", "both", "none"]


def _bound_refs_items(
    value: dict[object, object], /
) -> tuple[tuple[object, object], ...]:
    """Make a TOML inline table usable as a frozen model key."""
    return tuple(value.items())


type BoundRefs = Annotated[
    tuple[tuple[str, int | str], ...],
    BeforeValidator(func=_bound_refs_items),
]

type BoundRefYaml = Annotated[
    tuple[tuple[str, str], ...],
    BeforeValidator(func=_bound_refs_items),
]


type BoundRefTimes = Annotated[
    tuple[tuple[str, RefTimeInput], ...],
    BeforeValidator(func=_bound_refs_items),
]


type BoundRefDatetimes = Annotated[
    tuple[tuple[str, RefDatetimeInput], ...],
    BeforeValidator(func=_bound_refs_items),
]


type BoundRefValueSources = Annotated[
    tuple[tuple[str, RefValueSource], ...],
    BeforeValidator(func=_bound_refs_items),
]


class RejectionManifestError(ValueError):
    """A rejection manifest is invalid or internally inconsistent."""


def _language_class_name(language_cls: literalizer.LanguageCls, /) -> str:
    """Return the language class name."""
    return language_cls.__name__


LANGUAGE_CLASSES: tuple[literalizer.LanguageCls, ...] = tuple(
    sorted(ALL_LANGUAGES, key=_language_class_name)
)

_EXCEPTIONS_BY_NAME: Mapping[str, type[Exception]] = {
    name: value
    for name, value in vars(literalizer_exceptions).items()
    if isinstance(value, type) and issubclass(value, Exception)
} | {
    "TypeError": TypeError,
    "ValueError": ValueError,
    "NotImplementedError": NotImplementedError,
}

_INPUT_FORMATS_BY_NAME: Mapping[str, literalizer.InputFormat] = {
    member.name.lower(): member for member in literalizer.InputFormat
}


@beartype
def _name_resolver[NamedT](
    *, values_by_name: Mapping[str, NamedT]
) -> Callable[[object], object]:
    """Return a callable resolving a manifest name to its value.

    Names resolve before the strict-mode type check, so a manifest
    spells a resolved argument as a string while the model field holds
    the value itself.  Anything that is not a string is passed through
    for that check to reject.
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


type ExceptionType = Annotated[
    type[Exception],
    BeforeValidator(func=_name_resolver(values_by_name=_EXCEPTIONS_BY_NAME)),
]
type ExceptionTypes = Annotated[
    tuple[ExceptionType, ...],
    Field(min_length=1, strict=False),
]
type RejectionInputFormat = Annotated[
    literalizer.InputFormat,
    BeforeValidator(
        func=_name_resolver(values_by_name=_INPUT_FORMATS_BY_NAME)
    ),
]
type DeclaredName = Annotated[str, Field(min_length=1)]
"""A name a manifest spells: an enum member or a parameter."""

type DeclaredNames = Annotated[tuple[DeclaredName, ...], Field(strict=False)]
"""Several of those, spelled as a TOML array."""


@beartype
def substituted(*, template: str, value: str | None) -> str:
    """Return *template* with the case's declared value substituted."""
    return template.format(**{VALUE_PLACEHOLDER: value})


@beartype
def _placeholders(*, template: str) -> frozenset[str]:
    """Return the field names *template* substitutes."""
    return frozenset(
        field_name
        for _, field_name, _, _ in string.Formatter().parse(
            format_string=template,
        )
        if field_name is not None
    )


class OptionMemberKwarg(
    BaseModel,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """Pass a named member of an option enum.

    ``member`` may be the case's value, which is how one manifest
    covers several members of one option without naming a directory
    apiece.
    """

    kind: Literal["option_member"]
    option: Annotated[str, Field(min_length=1)]
    member: Annotated[str, Field(min_length=1)]


class OptionUnsetKwarg(
    BaseModel,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """Pass ``None`` for an option whose default is a member.

    A few options select a mode by being left unset rather than by
    naming a member -- ``D(json_type=None)`` is the narrow-typed mode,
    and its default is ``STD_JSON_VALUE`` -- so no ``option_member``
    can reach them (issue #4699).
    """

    kind: Literal["option_unset"]
    option: Annotated[str, Field(min_length=1)]


class BooleanKwarg(BaseModel, extra="forbid", frozen=True, strict=True):
    """Pass a literal boolean constructor argument."""

    kind: Literal["boolean"]
    kwarg: Annotated[str, Field(min_length=1)]
    value: bool


class TextKwarg(
    BaseModel,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """Pass a literal string, which may name the case's value."""

    kind: Literal["text"]
    kwarg: Annotated[str, Field(min_length=1)]
    value: str


class RecordShapeNamesKwarg(
    BaseModel,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """Name the generated record shape carrying a given key set.

    ``names`` maps one external name to each key set, so a manifest
    covering a collision between two shapes declares both.  Either name
    may be the case's value.
    """

    kind: Literal["record_shape_names"]
    key_sets: Annotated[
        tuple[DeclaredNames, ...],
        Field(min_length=1, strict=False),
    ]
    names: Annotated[tuple[str, ...], Field(min_length=1, strict=False)]

    @model_validator(mode="after")
    def _validate_pairing(self) -> Self:
        """Reject a shape without a name, or a name without a shape."""
        if len(self.key_sets) != len(self.names):
            msg = "key_sets and names must be the same length"
            raise ValueError(msg)
        return self


class EmptyContainerHint(BaseModel, extra="forbid", frozen=True, strict=True):
    """One input path and its declared container type."""

    path: Annotated[tuple[str | int, ...], Field(strict=False)]
    type_name: str


class EmptyContainerTypeHintsKwarg(
    BaseModel, extra="forbid", frozen=True, strict=True
):
    """Pass literal type hints for empty containers."""

    kind: Literal["empty_container_type_hints"]
    hints: Annotated[
        tuple[EmptyContainerHint, ...], Field(min_length=1, strict=False)
    ]


type RejectionKwarg = Annotated[
    OptionMemberKwarg
    | OptionUnsetKwarg
    | BooleanKwarg
    | TextKwarg
    | EmptyContainerTypeHintsKwarg
    | RecordShapeNamesKwarg,
    Field(discriminator="kind"),
]


def _no_kwargs() -> tuple[RejectionKwarg, ...]:
    """Return a typed empty argument list for the models."""
    return ()


def _no_gates() -> tuple[LanguageGate, ...]:
    """Return a typed empty gate list for the models."""
    return ()


def _no_names() -> tuple[DeclaredName, ...]:
    """Return a typed empty name list for the models."""
    return ()


def _no_sources() -> tuple[str, ...]:
    """Return a typed empty source list for the models."""
    return ()


@beartype
def _validate_gate_references(*, gates: tuple[LanguageGate, ...]) -> None:
    """Reject gate names that the shared gate evaluator cannot resolve."""
    for gate in gates:
        match gate:
            case CapabilityFlagGate() if gate.flag not in CAPABILITY_FLAGS:
                msg = f"unknown capability flag {gate.flag!r}"
                raise ValueError(msg)
            case EnumMemberPresentGate() if gate.option not in OPTIONS:
                msg = f"unknown gate option {gate.option!r}"
                raise ValueError(msg)
            case _:
                pass


class DeclarationSpec(BaseModel, extra="forbid", frozen=True, strict=True):
    """One fragment supplied to the declaration composition boundary."""

    source: str
    variable_form: Literal["new", "existing"]
    variable_name: str


def _no_declarations() -> tuple[DeclarationSpec, ...]:
    """Return a typed empty declaration sequence."""
    return ()


class CallSpec(  # noqa: NOD001
    BaseModel,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """The call a rejection manifest provokes its rejection with.

    A manifest declaring several sources makes the same call once per
    source, which is how one refusal shown by inputs that differ only
    in shape -- a null on its own, in a mapping, in a sequence -- is
    declared once rather than as a directory apiece.

    ``ref_value_yaml`` supplies reference inference hints without emitting
    bindings, using the same native YAML value syntax as ``bound_ref_yaml``.
    """

    api: ApiName
    declarations: Annotated[
        tuple[DeclarationSpec, ...], Field(strict=False)
    ] = Field(default_factory=_no_declarations)
    element_type: str = "Element"
    length: Annotated[int, Field(ge=0)] = 2
    formatted_value: str = "v"
    formatter_data: int | str | None = None
    sources: Annotated[tuple[str, ...], Field(strict=False)] = Field(
        default_factory=_no_sources,
    )
    input_format: RejectionInputFormat | None = None
    input_root_key: str | None = None
    call_transform: str | None = None
    zip_source: str | None = None
    zip_input_format: RejectionInputFormat | None = None
    modifiers: Annotated[tuple[DeclaredName, ...], Field(strict=False)] = (
        Field(default_factory=_no_names)
    )
    modifier_source: Literal["target", "all"] = "target"
    target_function: str | None = None
    parameter_names: Annotated[
        tuple[DeclaredName, ...],
        Field(strict=False),
    ] = Field(default_factory=_no_names)
    parameter_names_bare: str = ""
    per_element: bool = True
    wrap_in_file: bool = False
    ref_key: str | None = None
    ref_case: str | None = None
    bound_refs: BoundRefs = ()
    record_null_substitutions: BoundRefs = ()
    bound_ref_yaml: BoundRefYaml = ()
    bound_ref_times: BoundRefTimes = ()
    bound_ref_datetimes: BoundRefDatetimes = ()
    bound_ref_values: BoundRefValueSources = ()
    ref_value_yaml: BoundRefYaml = ()
    comment_source: Annotated[tuple[str, ...], Field(strict=False)] | None = (
        None
    )
    comment_source_bare: str = ""
    pre_indent_level: int = 0
    include_delimiters: bool = True
    variable_form: VariableFormName | None = None
    variable_name: str = "my_data"
    kwargs: Annotated[tuple[RejectionKwarg, ...], Field(strict=False)] = Field(
        default_factory=_no_kwargs
    )

    @model_validator(mode="after")
    def _validate_api_arguments(self) -> Self:
        """Reject arguments the declared API does not take."""
        renders = self.api in {
            "literalize",
            "literalize_call",
            "literalize_call_with_declarations",
        }
        if renders != bool(self.sources):
            msg = f"api = {self.api!r} requires exactly sources"
            raise ValueError(msg)
        if len(self.sources) != len(set(self.sources)):
            msg = "sources contains a duplicate entry"
            raise ValueError(msg)
        if renders != (self.input_format is not None):
            msg = f"api = {self.api!r} requires exactly an input_format"
            raise ValueError(msg)
        calls = self.api in {
            "literalize_call",
            "literalize_call_with_declarations",
        }
        if calls != (self.target_function is not None):
            msg = f"api = {self.api!r} requires exactly a target_function"
            raise ValueError(msg)
        has_parameter_names = "parameter_names" in self.model_fields_set
        has_parameter_names_bare = (
            "parameter_names_bare" in self.model_fields_set
        )
        if calls != (has_parameter_names or has_parameter_names_bare):
            msg = (
                f"api = {self.api!r} requires exactly parameter_names "
                "or parameter_names_bare"
            )
            raise ValueError(msg)
        if has_parameter_names and has_parameter_names_bare:
            msg = "declare parameter_names or parameter_names_bare, not both"
            raise ValueError(msg)
        has_comment_source = "comment_source" in self.model_fields_set
        has_comment_source_bare = (
            "comment_source_bare" in self.model_fields_set
        )
        if has_comment_source and has_comment_source_bare:
            msg = "declare comment_source or comment_source_bare, not both"
            raise ValueError(msg)
        if len(self.modifiers) > 0 and not (
            self.api != "constructor"
            and (
                self.variable_form in {"new", "both"}
                or (self.api == "literalize" and self.variable_form is None)
            )
        ):
            msg = "modifiers require a new or both variable form"
            raise ValueError(msg)
        _ = self._validate_modifier_source()
        _ = self._validate_operation_arguments()
        _ = self._validate_call_only_arguments()
        _ = self._validate_call_transform()
        return self

    def _validate_modifier_source(self) -> Self:
        """Require modifier names when expanding their enum sources."""
        if self.modifier_source == "all" and len(self.modifiers) == 0:
            msg = "modifier_source = 'all' requires modifiers"
            raise ValueError(msg)
        return self

    def _validate_operation_arguments(self) -> Self:
        """Reject operation arguments that the selected boundary
        ignores.
        """
        owners = {
            "declarations": "literalize_call_with_declarations",
            "element_type": "sequence_type_annotation",
            "length": "sequence_type_annotation",
            "formatted_value": "declaration_formatter",
            "formatter_data": "declaration_formatter",
            "record_null_substitutions": "literalize",
        }
        for name, owner in owners.items():
            if name in self.model_fields_set and self.api != owner:
                msg = f"{name} applies to api = {owner!r}"
                raise ValueError(msg)
        if (
            self.api == "literalize_call_with_declarations"
            and len(self.declarations) == 0
        ):
            msg = "composition requires declarations"
            raise ValueError(msg)
        if (
            self.api in {"sequence_type_annotation", "declaration_formatter"}
            and len(self.kwargs) > 0
        ):
            msg = "formatter operations do not construct a language"
            raise ValueError(msg)
        return self

    def _validate_call_only_arguments(self) -> Self:
        """Reject call arguments declared for another API."""
        call_only_arguments = {
            "call_transform": self.call_transform,
            "input_root_key": self.input_root_key,
            "zip_input_format": self.zip_input_format,
            "zip_source": self.zip_source,
        }
        invalid = sorted(
            name
            for name, value in call_only_arguments.items()
            if self.api
            not in {"literalize_call", "literalize_call_with_declarations"}
            and value is not None
        )
        if len(invalid) > 0:
            msg = f"{invalid[0]} applies to api = 'literalize_call'"
            raise ValueError(msg)
        return self

    def _validate_call_transform(self) -> Self:
        """Reject placeholders the declarative transform cannot fill."""
        if self.call_transform is None:
            return self
        for _, field_name, _, _ in string.Formatter().parse(
            format_string=self.call_transform
        ):
            if field_name is not None and (
                field_name not in _CALL_TRANSFORM_PLACEHOLDERS
            ):
                msg = (
                    f"unknown call_transform placeholder {field_name!r}; "
                    f"expected one of {sorted(_CALL_TRANSFORM_PLACEHOLDERS)}"
                )
                raise ValueError(msg)
        return self


class ErrorAttributes(  # noqa: NOD001
    BaseModel, extra="forbid", frozen=True, strict=True
):
    """Known public error attributes a manifest can assert."""

    path: Annotated[tuple[str | int, ...], Field(strict=False)] | None = None
    language_name: str | None = None
    option: str | None = None


class _RejectionData(  # noqa: NOD001
    BaseModel,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """Strict representation of the data read directly from TOML."""

    schema_version: Literal[1]
    summary: Annotated[str, Field(min_length=1)]
    exceptions: ExceptionTypes
    integer_digit_limit: Annotated[int, Field(ge=0)] | None = None
    record_output: bool = False
    position: Annotated[tuple[int, int], Field(strict=False)] | None = None
    attributes: ErrorAttributes | None = None
    gates: Annotated[tuple[LanguageGate, ...], Field(strict=False)] = Field(
        default_factory=_no_gates,
    )
    option: Annotated[str, Field(min_length=1)] | None = None
    values: Annotated[tuple[str, ...], Field(strict=False)] = Field(
        default_factory=_no_names,
    )
    call: CallSpec

    @model_validator(mode="after")
    def _validate_selection(self) -> Self:
        """Validate shared selectors and the values varied by a
        scenario.
        """
        if list(self.values) != sorted(self.values):
            msg = "values is not in sorted order"
            raise ValueError(msg)
        if len(self.values) != len(set(self.values)):
            msg = "values contains a duplicate entry"
            raise ValueError(msg)
        if self.option is not None and self.option not in OPTIONS:
            msg = f"unknown option {self.option!r}"
            raise ValueError(msg)
        _validate_gate_references(gates=self.gates)
        _ = self._validate_operation()
        return self

    def _validate_operation(self) -> Self:
        """Validate runtime settings and the option used by a direct
        call.
        """
        required = {
            "sequence_type_annotation": "sequence_format",
            "declaration_formatter": "declaration_style",
        }.get(self.call.api)
        if required is not None and self.option != required:
            msg = f"api = {self.call.api!r} requires option = {required!r}"
            raise ValueError(msg)
        if self.record_output and self.call.api == "constructor":
            msg = "record_output requires an operation that returns code"
            raise ValueError(msg)
        if self.integer_digit_limit is not None and (
            0
            < self.integer_digit_limit
            < sys.int_info.str_digits_check_threshold
        ):
            msg = (
                "integer_digit_limit must be zero or at least "
                "the interpreter threshold"
            )
            raise ValueError(msg)
        return self

    @model_validator(mode="after")
    def _validate_values(self) -> Self:
        """Reject a value no argument reads, or a read of no value."""
        templates = [
            template
            for kwarg in self.call.kwargs
            for template in _kwarg_templates(kwarg=kwarg)
        ]
        templates.extend(self.call.parameter_names)
        templates.extend(
            declaration.variable_name for declaration in self.call.declarations
        )
        templates.extend(source for _, source in self.call.bound_ref_yaml)
        templates.extend(source for _, source in self.call.ref_value_yaml)
        templates.append(self.call.variable_name)
        if self.call.target_function is not None:
            templates.append(self.call.target_function)
        unknown = sorted(
            placeholder
            for template in templates
            for placeholder in _placeholders(template=template)
            if placeholder != VALUE_PLACEHOLDER
        )
        if len(unknown) > 0:
            msg = f"unknown placeholder(s) {unknown}"
            raise ValueError(msg)
        substitutes = any(
            VALUE_PLACEHOLDER in _placeholders(template=template)
            for template in templates
        )
        if bool(self.values) != substitutes:
            msg = "declare values exactly when an argument substitutes one"
            raise ValueError(msg)
        return self


@beartype
def _kwarg_templates(*, kwarg: RejectionKwarg) -> tuple[str, ...]:
    """Return the strings a declared argument substitutes into."""
    templates: tuple[str, ...]
    match kwarg:
        case TextKwarg():
            templates = (kwarg.value,)
        case EmptyContainerTypeHintsKwarg():
            templates = ()
        case RecordShapeNamesKwarg():
            templates = tuple(kwarg.names)
        case OptionMemberKwarg():
            templates = (kwarg.member,)
        case BooleanKwarg() | OptionUnsetKwarg():
            templates = ()
        case _ as unreachable:
            assert_never(unreachable)
    return templates


@dataclasses.dataclass(frozen=True, kw_only=True)
class RejectionManifest:
    """One validated rejection, and where its golden file lives."""

    path: Path
    name: str
    summary: str
    exceptions: tuple[type[Exception], ...]
    integer_digit_limit: int | None
    record_output: bool
    position: tuple[int, int] | None
    attributes: ErrorAttributes | None
    gates: tuple[LanguageGate, ...]
    option: str | None
    values: tuple[str, ...]
    call: CallSpec

    @property
    def golden_path(self) -> Path:
        """Return the golden file holding every case's message."""
        return self.path.parent / GOLDEN_NAME


@beartype
def load_rejection_manifest(*, manifest_path: Path) -> RejectionManifest:
    """Load and validate one rejection manifest."""
    text = manifest_path.read_text(encoding="utf-8")
    try:
        data = _RejectionData.model_validate(obj=tomllib.loads(text))
    except ValidationError as exc:
        msg = f"{manifest_path}: {exc}"
        raise RejectionManifestError(msg) from exc
    return RejectionManifest(
        path=manifest_path,
        name=manifest_path.parent.name,
        summary=data.summary,
        exceptions=data.exceptions,
        integer_digit_limit=data.integer_digit_limit,
        record_output=data.record_output,
        position=data.position,
        attributes=data.attributes,
        gates=tuple(data.gates),
        option=data.option,
        values=tuple(data.values),
        call=data.call,
    )


@functools.cache
@beartype
def load_rejection_manifests(
    *,
    rejections_dir: Path,
) -> tuple[RejectionManifest, ...]:
    """Load every rejection manifest under *rejections_dir*."""
    manifests = [
        load_rejection_manifest(manifest_path=path)
        for path in sorted(rejections_dir.glob(pattern=f"*/{MANIFEST_NAME}"))
    ]
    if len(manifests) == 0:
        msg = f"no {MANIFEST_NAME} found under {rejections_dir}"
        raise RejectionManifestError(msg)
    return tuple(manifests)
