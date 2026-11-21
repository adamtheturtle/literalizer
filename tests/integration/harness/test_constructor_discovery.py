"""Constructor ownership remains exhaustive when selections overlap."""

from pathlib import Path

import pytest

from literalizer import NewVariable
from literalizer.languages import Elm
from tests.integration import constructor_cases
from tests.integration.case_manifests import (
    CaseManifestError,
    load_case_manifest,
)
from tests.integration.golden_outcomes import Exclusion


def test_selected_backend_requires_native_consumer(tmp_path: Path) -> None:
    """A consumer table must not silently narrow capability selection."""
    case_dir = tmp_path / "data_declaration"
    case_dir.mkdir()
    _ = (case_dir / "input.json").write_text(data="[[]]\n", encoding="utf-8")
    _ = (case_dir / "case.toml").write_text(
        data=(
            "schema_version = 1\n"
            'owner = "constructor-binding"\n'
            "[constructor.consumer_templates]\n"
            'Haskell = "{code}"\n'
        ),
        encoding="utf-8",
    )
    with pytest.raises(
        expected_exception=CaseManifestError,
        match="no constructor consumer",
    ):
        _ = constructor_cases.constructor_binding_cases(cases_dir=tmp_path)


@pytest.mark.parametrize(argnames="owner_count", argvalues=[0, 2])
def test_every_matching_owner(
    tmp_path: Path, cases_dir: Path, owner_count: int
) -> None:
    """Keep every native owner and reject missing fixture ownership."""
    baseline = constructor_cases.constructor_binding_cases(cases_dir=cases_dir)
    expected = {
        case.name
        for case in baseline
        if case.manifest.constructor is not None
        and not case.manifest.constructor.renders_target
    }
    for index in range(owner_count):
        case_dir = tmp_path / f"wrapper_{index}"
        case_dir.mkdir()
        _ = (case_dir / "input.json").write_text(
            data="[[]]\n", encoding="utf-8"
        )
        _ = (case_dir / "case.toml").write_text(
            data=(
                "schema_version = 1\n"
                'owner = "constructor-binding"\n[constructor]\n'
            ),
            encoding="utf-8",
        )
    if owner_count == 0:
        with pytest.raises(
            expected_exception=CaseManifestError,
            match="has no native fixture owner",
        ):
            _ = constructor_cases.constructor_binding_cases(cases_dir=tmp_path)
        return
    actual = constructor_cases.constructor_binding_cases(cases_dir=tmp_path)
    owners = {case.manifest.case_dir.name for case in actual}
    assert owners == {f"wrapper_{index}" for index in range(owner_count)}
    for name in expected:
        matching = [case for case in actual if case.name == name]
        assert len(matching) == owner_count


def test_unsupported_constructor_binding_is_excluded(cases_dir: Path) -> None:
    """A backend that cannot bind the call result supplies no golden
    work.
    """
    manifest = load_case_manifest(case_dir=cases_dir / "constructor_binding")
    case = constructor_cases.ConstructorBindingCase(
        name="Elm_constructor_call",
        lang_cls=Elm,
        spec_overrides={},
        variable_form=NewVariable(name="p", modifiers=frozenset()),
        manifest=manifest,
    )

    (rendering,) = case.renderings
    assert rendering.outcome == Exclusion(
        reason="constructor_binding/Elm_constructor_call@V0_19: "
        "the configuration cannot bind a nullary constructor result",
    )
    assert case.participating_renderings == ()
