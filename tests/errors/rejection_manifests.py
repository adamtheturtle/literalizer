"""Load and validate the declared per-language rejection manifests.

A rejection manifest names one thing a language refuses to represent --
non-string JSON object keys, a record name that is not PascalCase --
and the call that provokes the refusal.  The suite expands it across
every language the manifest's gates admit, so a rejection that holds
for a family of languages is declared once and a language joining that
family is covered the day it lands.

The manifest never carries the message a language raises with.  That
is kept in a golden file next to the manifest, which is itself TOML so
that a malformed one fails the repository's own TOML check.
"""

from __future__ import annotations

import dataclasses
import functools
import string
import tomllib
from collections.abc import Callable, Mapping  # noqa: TC003
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
from tests.language_gates import (
    CapabilityFlagGate,
    EnumMemberPresentGate,
    LanguageGate,
    language_gate_admits,
)
from tests.language_options import CAPABILITY_FLAGS, OPTIONS

REJECTIONS_DIR = Path(__file__).parent / "rejections"
"""Where the declared rejections live."""

MANIFEST_NAME = "rejection.toml"
GOLDEN_NAME = "expected.toml"

VALUE_PLACEHOLDER = "value"
"""The only placeholder a manifest's constructor arguments substitute."""

type ApiName = Literal["literalize", "literalize_call", "constructor"]
type VariableFormName = Literal["new", "existing", "both"]


def _bound_refs_items(
    value: dict[object, object], /
) -> tuple[tuple[object, object], ...]:
    """Make a TOML inline table usable as a frozen model key."""
    return tuple(value.items())


type BoundRefs = Annotated[
    tuple[tuple[str, int | str], ...],
    BeforeValidator(func=_bound_refs_items),
]


class RejectionManifestError(ValueError):
    """A rejection manifest is invalid or internally inconsistent."""


LANGUAGES_BY_NAME: Mapping[str, literalizer.LanguageCls] = {
    lang_cls.__name__: lang_cls
    for lang_cls in sorted(ALL_LANGUAGES, key=lambda cls: cls.__name__)
}

_EXCEPTIONS_BY_NAME: Mapping[str, type[Exception]] = {
    name: value
    for name, value in vars(literalizer_exceptions).items()
    if isinstance(value, type) and issubclass(value, Exception)
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
"""A name a manifest spells: a language, an enum member, a parameter."""

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


type RejectionKwarg = Annotated[
    OptionMemberKwarg | OptionUnsetKwarg | TextKwarg | RecordShapeNamesKwarg,
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


def _no_acceptances() -> tuple[Acceptance, ...]:
    """Return a typed empty acceptance list for the models."""
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


@beartype
def _unadmitted_acceptances(
    *, gates: tuple[LanguageGate, ...], names: tuple[str, ...]
) -> list[str]:
    """Return accepted languages that the manifest's gates exclude."""
    return sorted(
        name
        for name in names
        if not all(
            language_gate_admits(
                gate=gate,
                lang_cls=LANGUAGES_BY_NAME[name],
                spec=LANGUAGES_BY_NAME[name](),
            )
            for gate in gates
        )
    )


class Acceptance(
    BaseModel,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """Languages a gate admits that represent the manifest's input.

    Declaring one is an assertion, not a mute: the suite makes the same
    call for these languages and fails if it stops going through, so a
    language that starts rejecting cannot sit here behind a stale
    reason.  Languages sharing a reason are declared together.
    """

    languages: Annotated[
        tuple[DeclaredName, ...],
        Field(min_length=1, strict=False),
    ]
    reason: Annotated[str, Field(min_length=1)]


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
    """

    api: ApiName
    sources: Annotated[tuple[str, ...], Field(strict=False)] = Field(
        default_factory=_no_sources,
    )
    input_format: RejectionInputFormat | None = None
    modifiers: Annotated[tuple[DeclaredName, ...], Field(strict=False)] = (
        Field(default_factory=_no_names)
    )
    target_function: str | None = None
    parameter_names: Annotated[
        tuple[DeclaredName, ...],
        Field(strict=False),
    ] = Field(default_factory=_no_names)
    parameter_names_bare: str | None = None
    per_element: bool = True
    wrap_in_file: bool = False
    ref_key: str | None = None
    ref_case: str | None = None
    bound_refs: BoundRefs = ()
    comment_source: Annotated[tuple[str, ...], Field(strict=False)] | None = (
        None
    )
    comment_source_bare: str | None = None
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
        renders = self.api != "constructor"
        if renders != bool(self.sources):
            msg = f"api = {self.api!r} requires exactly sources"
            raise ValueError(msg)
        if len(self.sources) != len(set(self.sources)):
            msg = "sources contains a duplicate entry"
            raise ValueError(msg)
        if renders != (self.input_format is not None):
            msg = f"api = {self.api!r} requires exactly an input_format"
            raise ValueError(msg)
        calls = self.api == "literalize_call"
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
        if self.api != "literalize" and self.modifiers:
            msg = "modifiers apply to api = 'literalize'"
            raise ValueError(msg)
        return self


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
    gates: Annotated[tuple[LanguageGate, ...], Field(strict=False)] = Field(
        default_factory=_no_gates,
    )
    languages: Annotated[tuple[DeclaredName, ...], Field(strict=False)] = (
        Field(default_factory=_no_names)
    )
    option: Annotated[str, Field(min_length=1)] | None = None
    values: Annotated[tuple[str, ...], Field(strict=False)] = Field(
        default_factory=_no_names,
    )
    accepts: Annotated[tuple[Acceptance, ...], Field(strict=False)] = Field(
        default_factory=_no_acceptances,
    )
    call: CallSpec

    @model_validator(mode="after")
    def _validate_selection(self) -> Self:
        """Reject a manifest that selects no languages, or selects them
        twice over.
        """
        if bool(self.gates) == bool(self.languages):
            msg = "declare either gates or languages, not both"
            raise ValueError(msg)
        if self.languages and self.accepts:
            msg = "accepts applies to a gated manifest"
            raise ValueError(msg)
        accepting = tuple(
            name
            for acceptance in self.accepts
            for name in acceptance.languages
        )
        # Each accepts entry is sorted in itself; the entries are
        # ordered by the reason they share rather than by language, so
        # only their languages taken together must not repeat.
        sorted_lists = (
            (self.languages, "languages"),
            (self.values, "values"),
            *(
                (acceptance.languages, "accepts")
                for acceptance in self.accepts
            ),
        )
        for names, field_name in sorted_lists:
            if list(names) != sorted(names):
                msg = f"{field_name} is not in sorted order"
                raise ValueError(msg)
        for names, field_name in (*sorted_lists, (accepting, "accepts")):
            if len(names) != len(set(names)):
                msg = f"{field_name} contains a duplicate entry"
                raise ValueError(msg)
        unknown = sorted(
            set(self.languages + accepting) - set(LANGUAGES_BY_NAME)
        )
        if unknown:
            msg = f"unknown language(s) {unknown}"
            raise ValueError(msg)
        if self.option is not None and self.option not in OPTIONS:
            msg = f"unknown option {self.option!r}"
            raise ValueError(msg)
        _validate_gate_references(gates=self.gates)
        unadmitted = _unadmitted_acceptances(
            gates=self.gates,
            names=accepting,
        )
        if unadmitted:
            msg = f"accepts language(s) not admitted by gates {unadmitted}"
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
        templates.append(self.call.variable_name)
        if self.call.target_function is not None:
            templates.append(self.call.target_function)
        unknown = sorted(
            placeholder
            for template in templates
            for placeholder in _placeholders(template=template)
            if placeholder != VALUE_PLACEHOLDER
        )
        if unknown:
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
        case RecordShapeNamesKwarg():
            templates = tuple(kwarg.names)
        case OptionMemberKwarg():
            templates = (kwarg.member,)
        case OptionUnsetKwarg():
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
    gates: tuple[LanguageGate, ...]
    languages: tuple[str, ...]
    option: str | None
    values: tuple[str, ...]
    accepts: tuple[Acceptance, ...]
    call: CallSpec

    @property
    def golden_path(self) -> Path:
        """Return the golden file holding every case's message."""
        return self.path.parent / GOLDEN_NAME

    @property
    def accepting_languages(self) -> tuple[str, ...]:
        """Return every language the manifest records as accepting."""
        return tuple(
            sorted(
                name
                for acceptance in self.accepts
                for name in acceptance.languages
            )
        )


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
        gates=tuple(data.gates),
        languages=tuple(data.languages),
        option=data.option,
        values=tuple(data.values),
        accepts=tuple(data.accepts),
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
    if not manifests:
        msg = f"no {MANIFEST_NAME} found under {rejections_dir}"
        raise RejectionManifestError(msg)
    return tuple(manifests)
