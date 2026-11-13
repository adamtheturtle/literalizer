"""Shared receiver recipes expand beyond their original Python host."""

from pathlib import Path

import pytest

from literalizer.languages import ALL_LANGUAGES
from tests.integration.case_manifests import CaseManifestError
from tests.integration.shared_checked_cases import (
    checked_consumer_for_language,
    shared_checked_cases,
)


def test_checked_receiver_recipes_cover_every_capable_backend() -> None:
    """Both regressions own every supported language and version."""
    cases_dir = Path(__file__).parents[1] / "cases"
    cases = shared_checked_cases(cases_dir=cases_dir)
    expected = {
        (name, lang_cls, version)
        for name in (
            "shared_checked_counter_pairing",
            "shared_checked_counter_result_wrapper",
        )
        for lang_cls in ALL_LANGUAGES
        if lang_cls.supports_stateful_receiver_result_checks
        for version in lang_cls.VersionFormats
    }
    assert {
        (case.name, case.lang_cls, case.version) for case in cases
    } == expected


def test_missing_checked_consumer_is_an_error() -> None:
    """A native syntax table cannot silently filter participants."""
    with pytest.raises(
        expected_exception=CaseManifestError,
        match="no checked-call consumer for 'Dhall'",
    ):
        _ = checked_consumer_for_language(language_name="Dhall")
