"""Shared expansion helpers for the golden suite's Python axes."""

import dataclasses
import enum
from collections.abc import Callable, Iterable, Mapping
from functools import cache

import literalizer
from literalizer.exceptions import IncompatibleFormatsError
from tests.enum_members import enum_member_by_name, find_enum_member
from tests.language_options import OPTIONS, Option

from .language_metadata import LanguageMetadata, language_metadata
from .language_specs import make_spec, sorted_languages
from .variant_types import Variant, compact_variant


class AxisError(ValueError):
    """An invalid axis registration or an incomplete axis definition."""


@dataclasses.dataclass(frozen=True, kw_only=True)
class AxisTarget:
    """The language facts available while expanding an axis."""

    lang_cls: literalizer.LanguageCls
    metadata: LanguageMetadata
    default_spec: literalizer.Language

    @property
    def name(self) -> str:
        """Return the class name used in golden paths."""
        return self.lang_cls.__name__


@dataclasses.dataclass(frozen=True, kw_only=True)
class Choice:
    """One named selection of constructor options."""

    label: str
    kwargs: Mapping[str, object]


type Axis = Callable[[], tuple[Variant, ...]]
type Admission = Callable[[AxisTarget], bool]
type Options = Mapping[str, object]
type Override = Callable[[AxisTarget], Options | None]
type Choices = Callable[[AxisTarget], Iterable[Choice]]
type Name = Callable[[AxisTarget, str], str]

COMPACT = literalizer.CollectionLayout.COMPACT
MULTILINE = literalizer.CollectionLayout.MULTILINE
BOTH_LAYOUTS = ((COMPACT, ""), (MULTILINE, "_multiline"))

_SEQUENCE_FORMAT = OPTIONS["sequence_format"]


def named(*, suffix: str) -> Name:
    """Append a fixed suffix to the language name."""
    return lambda target, _label: f"{target.name}_{suffix}"


def named_choice(*, suffix: str) -> Name:
    """Append a suffix and the selected label to the language name."""
    return lambda target, label: f"{target.name}_{suffix}_{label}"


def fixed_options(**kwargs: object) -> Override:
    """Apply constructor options that are the same for every target."""
    return lambda _target: kwargs


def has_option(*, option: str) -> Admission:
    """Check whether the spec exposes an optional constructor field."""
    return lambda target: (
        option
        in {
            field.name
            for field in dataclasses.fields(
                class_or_instance=target.default_spec
            )
        }
    )


def has_member(*, option: Option, name: str) -> Admission:
    """Check whether the language offers a named member of an option."""
    return lambda target: (
        find_enum_member(
            enum_cls=option.get_members(target.default_spec), name=name
        )
        is not None
    )


def member(*, option: Option, name: str) -> Override:
    """Select the named option member from each language enum."""
    return lambda target: {
        option.kwarg: enum_member_by_name(
            enum_cls=option.get_members(target.default_spec), name=name
        )
    }


def pin(*, option: Option, name: str) -> Override:
    """Exercise a specific member wherever the language offers it."""

    def select(target: AxisTarget) -> Options | None:
        """Resolve the pin, excluding languages that lack the member."""
        value = find_enum_member(
            enum_cls=option.get_members(target.default_spec), name=name
        )
        return None if value is None else {option.kwarg: value}

    return select


def has_sample(*, kwarg: str) -> Admission:
    """Check whether the language provides a sample constructor value."""
    return lambda target: kwarg in target.metadata.non_default_kwargs


def sample_value(*, target: AxisTarget, kwarg: str) -> str:
    """Read a sample constructor value from the language's metadata."""
    try:
        return target.metadata.non_default_kwargs[kwarg]
    except KeyError as error:
        msg = f"{target.metadata.path} declares no sample value for {kwarg!r}"
        raise AxisError(msg) from error


def sample(*, kwarg: str) -> Override:
    """Select the language's sample value for a constructor option."""
    return lambda target: {kwarg: sample_value(target=target, kwarg=kwarg)}


def metadata_member(  # noqa: NOD001
    *,
    option: Option,
    read: Callable[[LanguageMetadata], str | None],
    optional: bool = False,
) -> Callable[[AxisTarget], Options]:
    """Choose an enum member by the name supplied in language metadata."""

    def select(target: AxisTarget) -> Options:
        """Resolve the declared member for the current language."""
        name = read(target.metadata)
        if name is None:
            if optional:
                return {}
            msg = (
                f"{target.metadata.path} declares no member "
                f"for {option.kwarg!r}"
            )
            raise AxisError(msg)
        return {
            option.kwarg: enum_member_by_name(
                enum_cls=option.get_members(target.default_spec), name=name
            )
        }

    return select


def member_with_behavior(
    *, option: Option, admits: Callable[[literalizer.Language], bool]
) -> Override:
    """Select the first member whose effective spec has the behavior."""

    def select(target: AxisTarget) -> Options | None:
        """Find an option member that enables the requested behavior."""
        for candidate in option.get_members(target.default_spec):
            kwargs = {option.kwarg: candidate}
            if admits(make_spec(lang_cls=target.lang_cls, **kwargs)):
                return kwargs
        return None

    return select


def sequence_format_override(
    *,
    metadata: LanguageMetadata,
    default_spec: literalizer.Language,
    declaration_style: enum.Enum,
) -> Options:
    """Honor sequence formats required by a particular declaration
    style.
    """
    name = metadata.declaration_style_sequence_format_overrides.get(
        declaration_style.name
    )
    return (
        {}
        if name is None
        else {
            _SEQUENCE_FORMAT.kwarg: enum_member_by_name(
                enum_cls=_SEQUENCE_FORMAT.get_members(default_spec), name=name
            )
        }
    )


def declaration_sequence(
    target: AxisTarget, declaration_style: enum.Enum
) -> Options:
    """Apply a declaration style's accompanying sequence format."""
    return sequence_format_override(
        metadata=target.metadata,
        default_spec=target.default_spec,
        declaration_style=declaration_style,
    )


def members(  # noqa: NOD001
    *,
    option: Option,
    include_default: bool = False,
    accepts: Callable[[enum.Enum], bool] = lambda _member: True,
    unset: str | None = None,
    label: Callable[[AxisTarget, enum.Enum], str] = (
        lambda _target, selected: selected.name.lower()
    ),
    extra_options: Callable[[AxisTarget, enum.Enum], Options] | None = None,
) -> Choices:
    """Select named option values, usually omitting the default member."""

    def select(target: AxisTarget) -> Iterable[Choice]:
        """Yield the option choices the language supports."""
        default = option.get_default(target.default_spec)
        if unset is not None and default is not None:
            yield Choice(label=unset, kwargs={option.kwarg: None})
        for selected in option.get_members(target.default_spec):
            if (selected is not default or include_default) and accepts(
                selected
            ):
                kwargs: dict[str, object] = {option.kwarg: selected}
                if extra_options is not None:
                    kwargs.update(extra_options(target, selected))
                yield Choice(label=label(target, selected), kwargs=kwargs)

    return select


def values(*, kwarg: str, **choices: str) -> Choices:
    """Exercise explicitly named values for one constructor parameter."""
    return lambda _target: (
        Choice(label=label, kwargs={kwarg: value})
        for label, value in choices.items()
    )


def single_choice(_target: AxisTarget) -> tuple[Choice, ...]:
    """Exercise only the axis's fixed options."""
    return (Choice(label="", kwargs={}),)


def cross(*, primary: Choices, **secondaries: Choices) -> Choices:
    """Pair each primary choice with each named set of secondary
    choices.
    """

    def select(target: AxisTarget) -> Iterable[Choice]:
        """Yield pairings in primary, tag and secondary order."""
        for first in primary(target):
            for tag, choices in secondaries.items():
                for second in choices(target):
                    label = f"{tag}_{second.label}"
                    if first.label != "":
                        label = f"{first.label}_{label}"
                    yield Choice(
                        label=label, kwargs={**first.kwargs, **second.kwargs}
                    )

    return select


@cache
def _target(*, lang_cls: literalizer.LanguageCls) -> AxisTarget:
    """Reuse the language metadata and default spec across axes."""
    return AxisTarget(
        lang_cls=lang_cls,
        metadata=language_metadata(language_id=lang_cls.language_id),
        default_spec=make_spec(lang_cls=lang_cls),
    )


def _options_for(
    *, target: AxisTarget, overrides: tuple[Override, ...]
) -> Options | None:
    """Merge overrides in order, stopping when one excludes the target."""
    kwargs: dict[str, object] = {}
    for override in overrides:
        resolved = override(target)
        if resolved is None:
            return None
        kwargs.update(resolved)
    return kwargs


def _compatible_spec(
    *, lang_cls: literalizer.LanguageCls, kwargs: Options
) -> literalizer.Language | None:
    """Ignore pairings rejected by the constructor's compatibility
    rules.
    """
    try:
        return make_spec(lang_cls=lang_cls, **kwargs)
    except IncompatibleFormatsError:
        return None


def _effective_specs(
    *,
    target: AxisTarget,
    kwargs: Options,
    per_version: bool,
    skip_incompatible: bool,
) -> Iterable[literalizer.Language]:
    """Yield each effective version once, allowing pins and syntax
    floors.
    """
    versions: Iterable[enum.Enum | None] = (
        target.default_spec.version_formats if per_version else (None,)
    )
    seen: set[enum.Enum] = set()
    for version in versions:
        options = (
            kwargs
            if version is None
            else {"language_version": version, **kwargs}
        )
        spec = (
            _compatible_spec(lang_cls=target.lang_cls, kwargs=options)
            if skip_incompatible
            else make_spec(lang_cls=target.lang_cls, **options)
        )
        if spec is not None and spec.language_version not in seen:
            seen.add(spec.language_version)
            yield spec


def expand(  # noqa: NOD001
    *,
    name: Name,
    choices: Choices = single_choice,
    requires: tuple[Admission, ...] = (),
    overrides: tuple[Override, ...] = (),
    requires_configured: Callable[[literalizer.Language], bool] | None = None,
    per_version: bool = True,
    layouts: tuple[tuple[literalizer.CollectionLayout, str], ...] = (
        (COMPACT, ""),
    ),
    sole_choice_name: Name | None = None,
    fixture_options: Callable[[AxisTarget], Options] | None = None,
    preamble: Callable[[AxisTarget], tuple[str, ...]] | None = None,
    skip_incompatible: bool = False,
) -> Axis:
    """Build variants through one shared language, version and layout loop."""

    @cache
    def build() -> tuple[Variant, ...]:
        """Expand this axis across all admitted languages."""
        variants: list[Variant] = []
        for lang_cls in sorted_languages():
            target = _target(lang_cls=lang_cls)
            if not all(admits(target) for admits in requires):
                continue
            kwargs = _options_for(target=target, overrides=overrides)
            if kwargs is None:
                continue
            pinned: Options = (
                {} if fixture_options is None else fixture_options(target)
            )
            extra_preamble = () if preamble is None else preamble(target)
            selected = tuple(choices(target))
            namer = (
                sole_choice_name
                if len(selected) == 1 and sole_choice_name is not None
                else name
            )
            for choice in selected:
                label = namer(target, choice.label)
                for spec in _effective_specs(
                    target=target,
                    kwargs={**kwargs, **choice.kwargs, **pinned},
                    per_version=per_version,
                    skip_incompatible=skip_incompatible,
                ):
                    if (
                        requires_configured is not None
                        and not requires_configured(spec)
                    ):
                        continue
                    variant = compact_variant(
                        name=label, spec=spec, lang_cls=lang_cls
                    )
                    variants.extend(
                        dataclasses.replace(
                            variant,
                            name=f"{label}{suffix}",
                            collection_layout=layout,
                            extra_preamble=extra_preamble,
                        )
                        for layout, suffix in layouts
                    )
        return tuple(variants)

    return build


def filtered(
    *, base: Axis, requires: tuple[Callable[[Variant], bool], ...]
) -> Axis:
    """Reuse a base axis's variants whose effective specs pass the filters."""

    @cache
    def build() -> tuple[Variant, ...]:
        """Keep the base variants that satisfy every predicate."""
        return tuple(
            variant
            for variant in base()
            if all(admits(variant) for admits in requires)
        )

    return build
