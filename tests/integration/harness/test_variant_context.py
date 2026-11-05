"""Call and reference variants retain the axis's layout contract."""

from pathlib import Path

import literalizer
from tests.integration.call_variant_cases import build_call_variant_cases
from tests.integration.literalize_ref_cases import (
    build_literalize_ref_variant_cases,
)


def test_call_and_reference_discovery_preserve_multiline_variants(
    cases_dir: Path,
) -> None:
    """Both public API suites keep their declared multiline controls."""
    for case_dir_name, cases in (
        (
            "call_singleton_list_rendering",
            build_call_variant_cases(cases_dir=cases_dir),
        ),
        (
            "literalize_ref_singleton_list_rendering",
            build_literalize_ref_variant_cases(),
        ),
    ):
        multiline = [
            case
            for case in cases
            if case.config.case_dir_name == case_dir_name
            if case.variant.collection_layout
            is literalizer.CollectionLayout.MULTILINE
        ]
        assert len(multiline) > 0
        assert all(
            case.config.collection_layout == "multiline" for case in multiline
        )
