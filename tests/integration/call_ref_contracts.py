"""Authored representation limits for call and reference golden
fixtures.
"""

import functools
import re
import tomllib
from collections import defaultdict
from pathlib import Path
from typing import Annotated

from pydantic import BaseModel, Field

import literalizer
from literalizer._literalize import (
    _contains_ref_marker,  # pyright: ignore[reportPrivateUsage]
)
from literalizer._parsing import parse_input
from literalizer.exceptions import CallArgNotSupportedError
from tests.errors.rejection_manifests import ExceptionType
from tests.language_options import OPTIONS

from .case_manifests import (
    CallCaseSpec,
    ComposedCallFixture,
    RefCaseSpec,
    case_input,
)
from .golden_outcomes import Exclusion, Rejection
from .literal_rejection_manifest import option_name
from .manifest_values import ManifestLanguages, StringTuple
from .rejection_contracts import rejected_examples

_CONTRACTS_PATH = Path(__file__).with_name(name="call_ref_contracts.toml")
_FIXTURE_OPTIONS = {"variable_form", "variable_modifiers"}


class _Selector(  # noqa: NOD001
    BaseModel,
    arbitrary_types_allowed=True,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """Authored cases under the given effective options."""

    cases: Annotated[StringTuple, Field(min_length=1)]
    languages: Annotated[ManifestLanguages, Field(min_length=1)]
    options: dict[str, str] = Field(default_factory=dict[str, str])


type _Selectors = Annotated[
    tuple[_Selector, ...], Field(strict=False, min_length=1)
]


class _RejectionContract(BaseModel, extra="forbid", frozen=True, strict=True):
    """An API representation error shared by several fixture inputs."""

    error: ExceptionType
    match: str | None = None  # noqa: NOD001 - message matching is optional
    applies: _Selectors


class _ExclusionContract(BaseModel, extra="forbid", frozen=True, strict=True):
    """A requirement imposed by the native fixture scaffold."""

    reason: str
    applies: _Selectors


class _Contracts(BaseModel, extra="forbid", frozen=True, strict=True):
    """Declared exceptions and fixture prerequisites."""

    rejection: Annotated[tuple[_RejectionContract, ...], Field(strict=False)]
    exclusion: Annotated[tuple[_ExclusionContract, ...], Field(strict=False)]


type _Key = tuple[str, literalizer.LanguageCls]
type _Rule = tuple[_Selector, Rejection | Exclusion]


@functools.cache
def _contracts(*, manifest_path: Path) -> dict[_Key, list[_Rule]]:
    """Load and index the authored contracts by case and language."""
    with manifest_path.open(mode="rb") as source:
        contracts = _Contracts.model_validate(obj=tomllib.load(source))
    rules: dict[_Key, list[_Rule]] = defaultdict(list)
    all_contracts: tuple[_RejectionContract | _ExclusionContract, ...] = (
        *contracts.rejection,
        *contracts.exclusion,
    )
    for contract in all_contracts:
        outcome: Rejection | Exclusion
        if isinstance(contract, _RejectionContract):
            if contract.match is not None:
                _ = re.compile(pattern=contract.match)
            outcome = Rejection(
                error=contract.error, match=contract.match, exact_type=True
            )
        else:
            outcome = Exclusion(reason=contract.reason)
        for selector in contract.applies:
            unknown = (
                selector.options.keys() - OPTIONS.keys() - _FIXTURE_OPTIONS
            )
            if len(unknown) > 0:
                msg = f"Unknown contract options: {sorted(unknown)}"
                raise ValueError(msg)
            for case in selector.cases:
                for language in selector.languages:
                    rules[case, language].append((selector, outcome))
    return rules


def authored_call_ref_outcome(
    *,
    config: CallCaseSpec | RefCaseSpec,
    spec: literalizer.Language,
    lang_cls: literalizer.LanguageCls,
    manifest_path: Path = _CONTRACTS_PATH,  # noqa: NOD001 - test override
) -> Rejection | Exclusion | None:
    """Resolve an authored constraint without calling the renderer."""
    fixture_options = {
        "variable_form": (
            type(config.variable_form).__name__
            if isinstance(config, CallCaseSpec)
            else config.variable_form
        ),
        "variable_modifiers": ",".join(sorted(config.variable_modifiers)),
    }
    matches = {
        outcome
        for selector, outcome in _contracts(manifest_path=manifest_path).get(
            (config.case_dir_name, lang_cls), ()
        )
        if all(
            expected
            == (
                fixture_options[name]
                if name in fixture_options
                else option_name(spec=spec, name=name)
            )
            for name, expected in selector.options.items()
        )
    }
    if len(matches) > 1:
        msg = f"Conflicting contracts for {config.case_dir_name}: {spec!r}"
        raise ValueError(msg)
    return next(iter(matches), None)


@functools.cache
def _languages_rejecting_reference_markers(
    *, contract: str
) -> frozenset[literalizer.LanguageCls]:
    """Read the unsupported reference formats from existing API
    examples.
    """
    return frozenset(
        case.lang_cls
        for case in rejected_examples(
            contract=contract,
            error=CallArgNotSupportedError,
        )
    )


@functools.cache
def _has_reference_marker(
    *, case_dir: Path, ref_key: str, followup: str | None
) -> bool:
    """Check primary and follow-up inputs for actual reference markers."""
    input_info = case_input(case_dir=case_dir)
    source = input_info.path.read_text(encoding="utf-8")
    return any(
        _contains_ref_marker(
            value=parse_input(
                source=text, input_format=input_info.input_format
            ).data,
            ref_key=ref_key,
        )
        for text in (source, followup)
        if text is not None
    )


def unsupported_reference_marker(
    *,
    config: CallCaseSpec | RefCaseSpec,
    lang_cls: literalizer.LanguageCls,
    cases_dir: Path,
) -> Rejection | None:
    """Assert the reference restriction when the input uses a marker."""
    contract = (
        "default_helper_call_reference_zkv"
        if isinstance(config, CallCaseSpec)
        else "default_helper_reference_zkv"
    )
    if lang_cls not in _languages_rejecting_reference_markers(
        contract=contract
    ):
        return None
    followup = (
        config.fixture.followup.source
        if isinstance(config, CallCaseSpec)
        and isinstance(config.fixture, ComposedCallFixture)
        and config.fixture.followup is not None
        else None
    )
    if _has_reference_marker(
        case_dir=cases_dir / config.case_dir_name,
        ref_key=config.ref_key,
        followup=followup,
    ):
        return Rejection(
            error=CallArgNotSupportedError, match=None, exact_type=True
        )
    return None
