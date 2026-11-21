"""Fixture-specific representation contracts for the literal runner."""

from __future__ import annotations

import enum
import functools
import re
import tomllib
from collections import defaultdict
from pathlib import Path
from typing import TYPE_CHECKING, Annotated, Literal

from pydantic import BaseModel, Field

import literalizer
from tests.errors.rejection_manifests import ExceptionType
from tests.language_options import OPTIONS, HasJsonType

from .golden_outcomes import Rejection
from .manifest_values import ManifestLanguages, StringFrozenSet, StringTuple

if TYPE_CHECKING:
    from .golden_renderings import RenderArguments

LITERAL_REJECTION_MANIFEST: Path = Path(__file__).with_name(
    name="literal_rejections.toml"
)


# Omitted selector fields leave the corresponding dimension unrestricted.
class LiteralRejectionSelector(  # noqa: NOD001
    BaseModel,
    arbitrary_types_allowed=True,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """An authored input and the effective modes a contract applies to."""

    cases: Annotated[StringTuple, Field(min_length=1)]
    languages: Annotated[ManifestLanguages, Field(min_length=1)]
    options: dict[str, str] = Field(default_factory=dict[str, str])
    variable_form: (
        Literal["NewVariable", "ExistingVariable", "BothVariableForms"] | None
    ) = None
    variable_modifiers: StringFrozenSet | None = None
    record_null_substitutions: bool | None = None

    def matches(
        self, *, spec: literalizer.Language, render: RenderArguments
    ) -> bool:
        """Match resolved constructor options and fixture arguments."""
        variable_form = (
            render.variable_form if spec.supports_variable_names else None
        )
        if (
            self.variable_form is not None
            and type(variable_form).__name__ != self.variable_form
        ):
            return False
        if self.variable_modifiers is not None:
            modifiers = (
                frozenset(
                    modifier.name for modifier in variable_form.modifiers
                )
                if isinstance(
                    variable_form,
                    literalizer.NewVariable | literalizer.BothVariableForms,
                )
                else frozenset[str]()
            )
            if modifiers != self.variable_modifiers:
                return False
        if (
            self.record_null_substitutions is not None
            and (render.record_null_substitutions is not None)
            != self.record_null_substitutions
        ):
            return False
        return all(
            expected == _option_name(spec=spec, name=name)
            for name, expected in self.options.items()
        )


def _option_name(*, spec: literalizer.Language, name: str) -> str:
    """Normalize selected enum options and unset optional formats."""
    value = (
        None
        if name == "json_type" and not isinstance(spec, HasJsonType)
        else OPTIONS[name].get_default(spec)
    )
    return value.name if isinstance(value, enum.Enum) else "NONE"


class _Contract(BaseModel, extra="forbid", frozen=True, strict=True):
    """The exception and stable diagnostic shared by some combinations."""

    error: ExceptionType
    match: str
    applies: Annotated[
        tuple[LiteralRejectionSelector, ...], Field(strict=False, min_length=1)
    ]


class _Manifest(BaseModel, extra="forbid", frozen=True, strict=True):
    """The representation contracts of authored literal and variant
    cases.
    """

    rejection: Annotated[tuple[_Contract, ...], Field(strict=False)]


type LiteralRejectionKey = tuple[str, literalizer.LanguageCls]
type LiteralRejectionRule = tuple[LiteralRejectionSelector, Rejection]


@functools.cache
def literal_rejection_rules(
    *, manifest_path: Path
) -> dict[LiteralRejectionKey, list[LiteralRejectionRule]]:
    """Index each contract by fixture and language."""
    with manifest_path.open(mode="rb") as source:
        manifest = _Manifest.model_validate(obj=tomllib.load(source))
    rules: dict[LiteralRejectionKey, list[LiteralRejectionRule]] = defaultdict(
        list
    )
    for contract in manifest.rejection:
        _ = re.compile(pattern=contract.match)
        rejection = Rejection(error=contract.error, match=contract.match)
        for selector in contract.applies:
            unknown = selector.options.keys() - OPTIONS.keys()
            if len(unknown) > 0:
                msg = f"Unknown literal rejection options: {sorted(unknown)}"
                raise ValueError(msg)
            for case in selector.cases:
                for language in selector.languages:
                    rules[case, language].append((selector, rejection))
    return rules


def authored_literal_rejection(
    *,
    case_name: str,
    lang_cls: literalizer.LanguageCls,
    spec: literalizer.Language,
    render: RenderArguments,
    manifest_path: Path,
) -> Rejection | None:
    """Return the contract declared for this rendering, if any."""
    matches = {
        rejection
        for selector, rejection in literal_rejection_rules(
            manifest_path=manifest_path
        ).get((case_name, lang_cls), ())
        if selector.matches(spec=spec, render=render)
    }
    if len(matches) > 1:
        msg = f"Conflicting rejections for fixture {case_name}: {spec!r}"
        raise ValueError(msg)
    return next(iter(matches), None)
