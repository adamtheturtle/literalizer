"""Load and validate test-owned language metadata.

The production language classes describe what a renderer can represent
and which options stay compatible with each other.  Everything needed
only to construct, name, or host a golden fixture lives here instead,
in ``tests/integration/languages/<language_id>.toml``, keyed by the
stable ``language_id`` a language declares.

Production keeps the behavior and compatibility facts:
``string_literals_escape_null_byte`` and
``supports_ref_elements_in_tuple_strategy`` (what the renderer can
represent) and ``modifier_sequence_format_overrides`` (which option
values stay compatible).  A value that is both a real capability and
useful to the suite stays in production and is read from there rather
than restated here, so no supported option value, default, version, or
compatibility rule is duplicated in these files.

Everything else that used to live on a language class is golden-suite
policy and is declared here: golden filename casing, the
collection-layout name segment, per-fixture module-name templates and
casing, external record-shape fixture prefixes, the strategy and
language-version names a focused variant selects, opt-ins for the
focused record, nested-map-widening, pre-indent comment-scalar and
empty-container-hint cases.
"""

from __future__ import annotations

import dataclasses
import functools
import tomllib
from collections.abc import Mapping  # noqa: TC003
from pathlib import Path
from typing import Annotated, Literal

from beartype import beartype
from pydantic import BaseModel, Field, ValidationError, model_validator

LANGUAGES_DIR = Path(__file__).parent / "languages"

type RecordVariantName = Literal[
    "unify_optional_fields",
    "nonrecord_dict_field",
    "keyword_field",
    "quoted_field",
    "field_type_split",
]
type NestedMapWideningName = Literal["none", "default", "uniform_keys"]


class LanguageMetadataError(ValueError):
    """A language metadata file is missing or invalid."""


def _empty_record_variants() -> list[RecordVariantName]:
    """Return a typed empty record-variant list for the model."""
    return []


def _empty_string_mapping() -> dict[str, str]:
    """Return a typed empty string mapping for the model."""
    return {}


class GoldenPolicy(  # noqa: NOD001
    BaseModel,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """Naming policy for a language's golden files and fixtures."""

    filename_lowercase: bool = False
    """Whether a whole golden filename is lower-cased on disk."""

    collection_layout_category: Annotated[str, Field(min_length=1)] = (
        "collection_layout"
    )
    """Name segment the collection-layout goldens use."""

    fixture_module_name_template: str | None = None
    """Per-fixture module name, formatted with ``parent`` and ``stem``."""

    fixture_module_name_lowercase: bool = False
    """Whether a formatted per-fixture module name is lower-cased."""


class EmptyContainerTypeHint(
    BaseModel,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """One concrete empty-container hint declared by a golden variant."""

    path: list[int]
    hint: Annotated[str, Field(min_length=1)]


class EmptyContainerTypeHintVariant(
    BaseModel,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """Settings for a language's empty-container-hint golden variant."""

    heterogeneous_strategy: Annotated[str, Field(min_length=1)]
    type_hints: list[EmptyContainerTypeHint]


class VariantPolicy(  # noqa: NOD001
    BaseModel,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """Focused golden variants a language opts into."""

    pre_indent_comment_scalar: bool = False
    """Whether the focused pre-indent comment-scalar case runs."""

    record: list[RecordVariantName] = Field(
        default_factory=_empty_record_variants
    )
    """Focused record cases whose inputs this language renders."""

    nested_map_widening: NestedMapWideningName = "none"
    """Which nested-map widening input this language renders, if any."""

    record_language_version: str | None = None
    """``VersionFormats`` member name the record variants select."""

    external_record_shape_fixture_prefix: str | None = None
    """Fixture preamble hosting an externally declared record shape."""

    heterogeneous_value_variant_name_strategy: str | None = None
    """Strategy name the value-variant-name goldens select."""

    heterogeneous_value_variant_name_language_version: str | None = None
    """``VersionFormats`` member name those goldens select."""

    empty_container_type_hint: EmptyContainerTypeHintVariant | None = None
    """Settings for the empty-container-hint golden, when it runs."""

    non_default_kwargs: dict[
        Annotated[str, Field(min_length=1)],
        Annotated[str, Field(min_length=1)],
    ] = Field(default_factory=_empty_string_mapping)
    """Sample non-default values the golden suite passes to a language.

    Keys are constructor field names.  These are chosen fixture inputs,
    not capabilities: a language supports an option whether or not this
    file names a value to exercise it with.
    """

    declaration_style_sequence_format_overrides: dict[
        Annotated[str, Field(min_length=1)],
        Annotated[str, Field(min_length=1)],
    ] = Field(default_factory=_empty_string_mapping)
    """Sequence formats the declaration-style goldens substitute in.

    Production rejects the incompatible pairing itself, in
    ``__post_init__``; this only records which compatible format the
    fixture picks instead so that it keeps compiling.
    """

    @model_validator(mode="after")
    def _validate_consistency(self) -> VariantPolicy:
        """Validate relationships that span variant fields."""
        if len(self.record) != len(set(self.record)):
            msg = "record contains a duplicate entry"
            raise ValueError(msg)
        return self


class _LanguageMetadataData(  # noqa: NOD001
    BaseModel,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """Strict representation of the data read directly from TOML."""

    schema_version: Literal[1]
    golden: GoldenPolicy = Field(default_factory=GoldenPolicy)
    variants: VariantPolicy = Field(default_factory=VariantPolicy)


@dataclasses.dataclass(frozen=True, kw_only=True)
class LanguageMetadata:
    """Validated golden-suite policy for one language."""

    path: Path
    language_id: str
    schema_version: Literal[1]
    golden: GoldenPolicy
    variants: VariantPolicy

    @property
    def record_variants(self) -> frozenset[RecordVariantName]:
        """Return the focused record variants this language opts into."""
        return frozenset(self.variants.record)

    @property
    def non_default_kwargs(self) -> Mapping[str, str]:
        """Return the sample constructor values this suite passes in."""
        return dict(self.variants.non_default_kwargs)

    @property
    def declaration_style_sequence_format_overrides(
        self,
    ) -> Mapping[str, str]:
        """Return the sequence formats declaration-style cases use."""
        return dict(self.variants.declaration_style_sequence_format_overrides)


def _fail(*, path: Path, message: str) -> LanguageMetadataError:
    """Build a metadata error containing its source path."""
    return LanguageMetadataError(f"{path}: {message}")


@functools.cache
@beartype
def load_language_metadata(
    *,
    languages_dir: Path,
    language_id: str,
) -> LanguageMetadata:
    """Return one fully validated language metadata file."""
    path = languages_dir / f"{language_id}.toml"
    if not path.is_file():
        raise _fail(
            path=path,
            message=(
                f"no test metadata for language {language_id!r}; add this "
                "file to describe its golden-suite policy"
            ),
        )
    try:
        raw = tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        raise _fail(path=path, message=f"invalid TOML: {exc}") from exc
    try:
        data = _LanguageMetadataData.model_validate(obj=raw)
    except (ValidationError, ValueError) as exc:
        raise _fail(path=path, message=str(object=exc)) from exc

    return LanguageMetadata(
        path=path,
        language_id=language_id,
        schema_version=data.schema_version,
        golden=data.golden,
        variants=data.variants,
    )


@beartype
def language_metadata(*, language_id: str) -> LanguageMetadata:
    """Return the golden-suite policy declared for *language_id*."""
    return load_language_metadata(
        languages_dir=LANGUAGES_DIR,
        language_id=language_id,
    )


@functools.cache
@beartype
def language_metadata_by_id(
    *,
    languages_dir: Path,
) -> Mapping[str, LanguageMetadata]:
    """Return every metadata file in *languages_dir*, keyed by
    language.
    """
    return {
        path.stem: load_language_metadata(
            languages_dir=languages_dir,
            language_id=path.stem,
        )
        for path in sorted(languages_dir.glob(pattern="*.toml"))
    }
