"""Call and reference variants retain the axis's layout contract."""

from pathlib import Path
from typing import Literal

import pytest
from pydantic import BaseModel, TypeAdapter

import literalizer
from tests.integration.call_variant_cases import build_call_variant_cases
from tests.integration.case_manifests import CallCaseSpec, RefCaseSpec
from tests.integration.literalize_ref_cases import (
    build_literalize_ref_variant_cases,
)
from tests.integration.variant_context import config_with_variant_layout
from tests.toml_cases import load_toml_cases


class _LayoutCase(BaseModel, extra="forbid", frozen=True):
    """One named manifest-owned regression scenario."""

    name: str
    kind: Literal["call", "ref"]
    axis_layout: literalizer.CollectionLayout
    settings: dict[str, object]
    expected_layout: Literal["compact", "multiline"]
    original_layout: Literal["compact", "multiline"]


class _Cases(BaseModel, extra="forbid", frozen=True):
    """The complete declarative regression corpus."""

    cases: tuple[_LayoutCase, ...]


_CASES = TypeAdapter(type=_Cases).validate_python(
    load_toml_cases(name="variant_layout")
)


@pytest.mark.parametrize(
    argnames="case", argvalues=_CASES.cases, ids=lambda case: case.name
)
def test_case_layout_overrides_axis_only_when_explicit(
    case: _LayoutCase,
) -> None:
    """An omitted compact default must not mask a multiline axis."""
    if case.kind == "call":
        config: CallCaseSpec | RefCaseSpec = CallCaseSpec.model_validate(
            obj=case.settings, context={"case_dir_name": "layout"}
        )
    else:
        config = RefCaseSpec.model_validate(
            obj=case.settings, context={"case_dir_name": "layout"}
        )
    resolved = config_with_variant_layout(
        config=config, layout=case.axis_layout
    )
    assert resolved.collection_layout == case.expected_layout
    assert config.collection_layout == case.original_layout


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
