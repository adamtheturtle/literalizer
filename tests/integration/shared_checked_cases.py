"""Owned complete consumers of shared result-check recipes."""

import dataclasses
import enum
import functools
import tomllib
from collections.abc import Mapping
from pathlib import Path

from pydantic import BaseModel, Field

from literalizer import Language, LanguageCls
from literalizer._enums import enum_payload
from literalizer._language import PositionalCallStyle
from tests.enum_members import enum_member_by_name

from .case_manifests import CaseManifestError, load_case_manifests
from .language_specs import make_golden_path, make_spec, sorted_languages


class CheckedRecipe(BaseModel, extra="forbid", frozen=True):
    """Original source rows, paired expected values and caller program."""

    source: str
    zip_source: str
    pre_indent_level: int
    invocation: dict[str, object]
    consumer_template: str
    expected_calls: int


# Omitted consumer settings retain the recipe's original syntax and placement.
class CheckedConsumer(BaseModel, extra="forbid", frozen=True):  # noqa: NOD001
    """Native syntax selected after functional language participation."""

    template: str | None = None
    pre_indent_level: int | None = None
    heterogeneous_strategy: str | None = None
    execution: list[str] = Field(default_factory=list[str])


@functools.cache
def checked_consumers() -> Mapping[str, CheckedConsumer]:
    """Read caller-owned native syntax without selecting participants."""
    path = Path(__file__).with_name(name="shared_checked_consumers.toml")
    return {
        name: CheckedConsumer.model_validate(obj=config)
        for name, config in tomllib.loads(
            path.read_text(encoding="utf-8")
        ).items()
    }


def checked_consumer_for_language(*, language_name: str) -> CheckedConsumer:
    """Require a native consumer for every selected backend."""
    try:
        return checked_consumers()[language_name]
    except KeyError as exc:
        msg = f"no checked-call consumer for {language_name!r}"
        raise CaseManifestError(msg) from exc


@dataclasses.dataclass(frozen=True)
class SharedCheckedCase:
    """One checked-call recipe, native consumer and backend version."""

    name: str
    recipe: CheckedRecipe
    lang_cls: LanguageCls
    spec: Language
    consumer: CheckedConsumer
    version: enum.Enum
    golden_path: Path


def shared_checked_cases(*, cases_dir: Path) -> tuple[SharedCheckedCase, ...]:
    """Discover and own every declared complete checked-call consumer."""
    return tuple(
        SharedCheckedCase(
            name=manifest.case_dir.name,
            recipe=CheckedRecipe.model_validate(
                obj=tomllib.loads(
                    manifest.input.path.read_text(encoding="utf-8")
                )
            ),
            lang_cls=lang_cls,
            spec=_checked_spec(
                lang_cls=lang_cls, version=version, consumer=consumer
            ),
            consumer=consumer,
            version=version,
            golden_path=make_golden_path(
                parent=manifest.case_dir,
                name=f"{lang_cls.__name__}_shared_checked",
                lang_cls=lang_cls,
                version=version,
            ),
        )
        for manifest in load_case_manifests(cases_dir=cases_dir)
        if manifest.owner == "shared-invocation"
        for lang_cls in sorted_languages()
        if manifest.selection.admits_language(lang_cls=lang_cls)
        for consumer in (
            checked_consumer_for_language(language_name=lang_cls.__name__),
        )
        for version in lang_cls.VersionFormats
    )


def _checked_spec(
    *, lang_cls: LanguageCls, version: enum.Enum, consumer: CheckedConsumer
) -> Language:
    """Choose a positional expression style or the native recipe API."""
    kwargs: dict[str, object] = {"language_version": version}
    if not lang_cls.supports_native_invocations:
        kwargs["call_style"] = next(
            member
            for member in lang_cls.CallStyles
            if isinstance(
                enum_payload(member=member, payload_type=object),
                PositionalCallStyle,
            )
        )
    if consumer.heterogeneous_strategy is not None:
        kwargs["heterogeneous_strategy"] = enum_member_by_name(
            enum_cls=lang_cls.HeterogeneousStrategies,
            name=consumer.heterogeneous_strategy,
        )
    return make_spec(lang_cls=lang_cls, **kwargs)
