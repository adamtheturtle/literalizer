"""Call and reference variants retain the axis's layout contract."""

import pytest

import literalizer
from tests.integration.call_variant_cases import build_call_variant_cases
from tests.integration.case_manifests import CallCaseSpec, RefCaseSpec
from tests.integration.literalize_ref_cases import (
    build_literalize_ref_variant_cases,
)
from tests.integration.variant_context import config_with_variant_layout


@pytest.mark.parametrize(
    argnames="explicit", argvalues=[None, "compact", "multiline"]
)
@pytest.mark.parametrize(argnames="kind", argvalues=["call", "ref"])
@pytest.mark.parametrize(
    argnames="layout", argvalues=list(literalizer.CollectionLayout)
)
def test_case_layout_overrides_axis_only_when_explicit(
    *, explicit: str | None, kind: str, layout: literalizer.CollectionLayout
) -> None:
    """An omitted compact default must not mask a multiline axis."""
    settings: dict[str, object] = {}
    if explicit is not None:
        settings["collection_layout"] = explicit
    if kind == "call":
        settings.update(
            target_function="consume",
            parameter_names=["value"],
            per_element=False,
        )
        config: CallCaseSpec | RefCaseSpec = CallCaseSpec.model_validate(
            obj=settings, context={"case_dir_name": "layout"}
        )
    else:
        config = RefCaseSpec.model_validate(
            obj=settings, context={"case_dir_name": "layout"}
        )
    resolved = config_with_variant_layout(config=config, layout=layout)
    assert resolved.collection_layout == (
        explicit if explicit is not None else layout.value
    )
    assert config.collection_layout == (
        explicit if explicit is not None else "compact"
    )


def test_call_and_reference_discovery_preserve_multiline_variants() -> None:
    """Both public API suites keep their declared multiline controls."""
    for case_dir_name, cases in (
        ("call_singleton_list_rendering", build_call_variant_cases()),
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
