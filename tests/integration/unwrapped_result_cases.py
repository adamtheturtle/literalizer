"""Declarations and paths for unwrapped result-view golden files."""

import enum
import tomllib
from pathlib import Path
from typing import Literal

from pydantic import BaseModel

import literalizer

from .language_specs import make_golden_path, make_spec
from .manifest_values import (
    ManifestLanguage,
    ManifestLanguages,
)

type ResultAttribute = Literal["code", "bare_code"]


class _PrefixCases(
    BaseModel, arbitrary_types_allowed=True, extra="forbid", frozen=True
):
    """Declared languages and result views for a commented scalar."""

    languages: ManifestLanguages
    input_case: str
    variable_name: str


class RecordConsumer(
    BaseModel, arbitrary_types_allowed=True, extra="forbid", frozen=True
):
    """Caller-owned collection syntax around an unwrapped record."""

    language: ManifestLanguage
    template: str


class _ResultCases(
    BaseModel, arbitrary_types_allowed=True, extra="forbid", frozen=True
):
    """TOML-owned inputs and expectations for unwrapped result views."""

    prefix: _PrefixCases
    attributes: tuple[ResultAttribute, ...]
    record_input_case: str
    record_consumers: tuple[RecordConsumer, ...]


RESULT_CASES: _ResultCases = _ResultCases.model_validate(
    obj=tomllib.loads(
        Path(__file__).with_suffix(suffix=".toml").read_text(encoding="utf-8")
    ),
)


def record_consumer_specs(
    *, consumer: RecordConsumer
) -> tuple[literalizer.Language, ...]:
    """Expand versions while retaining constructor pins such as Java
    16.
    """
    specs = (
        make_spec(
            lang_cls=consumer.language,
            heterogeneous_strategy=consumer.language.HeterogeneousStrategies[
                "RECORD"
            ],
            language_version=version,
        )
        for version in consumer.language.VersionFormats
    )
    return tuple({spec.language_version: spec for spec in specs}.values())


def prefix_result_golden_path(
    *,
    cases_dir: Path,
    lang_cls: literalizer.LanguageCls,
    attribute: ResultAttribute,
) -> Path:
    """Locate the unwrapped result view for a commented scalar."""
    return make_golden_path(
        parent=cases_dir / RESULT_CASES.prefix.input_case,
        name=f"{lang_cls.__name__}_unwrapped_{attribute}",
        lang_cls=lang_cls,
        version=lang_cls().language_version,
    )


def record_result_golden_path(
    *,
    cases_dir: Path,
    consumer: RecordConsumer,
    attribute: ResultAttribute,
    version: enum.Enum,
) -> Path:
    """Locate a versioned caller-owned record consumer."""
    return make_golden_path(
        parent=cases_dir / RESULT_CASES.record_input_case,
        name=f"{consumer.language.__name__}_unwrapped_record_{attribute}",
        lang_cls=consumer.language,
        version=version,
    )


def result_view_golden_paths(*, cases_dir: Path) -> set[Path]:
    """Return the compiling paths owned by the result-view runner."""
    paths = {
        prefix_result_golden_path(
            cases_dir=cases_dir,
            lang_cls=lang_cls,
            attribute=attribute,
        )
        for lang_cls in RESULT_CASES.prefix.languages
        for attribute in RESULT_CASES.attributes
    }
    paths.update(
        record_result_golden_path(
            cases_dir=cases_dir,
            consumer=consumer,
            attribute=attribute,
            version=spec.language_version,
        )
        for consumer in RESULT_CASES.record_consumers
        for attribute in RESULT_CASES.attributes
        for spec in record_consumer_specs(consumer=consumer)
    )
    return paths
