"""Authored alternative gates retain their union under required gates."""

from pathlib import Path

import pytest

import literalizer
from literalizer.languages import ALL_LANGUAGES
from tests.integration.case_manifests import load_case_manifest
from tests.integration.manifest_selection import CapabilitySelection
from tests.language_gates import CapabilityFlagGate


def _selected(
    *, selection: CapabilitySelection
) -> set[literalizer.LanguageCls]:
    """Collect participation without depending on backend identities."""
    return {
        cls for cls in ALL_LANGUAGES if selection.admits_language(lang_cls=cls)
    }


@pytest.mark.parametrize(
    argnames="flags",
    argvalues=[
        ("supports_local_binding_documents",),
        (
            "supports_local_binding_documents",
            "supports_key_value_assignment_documents",
        ),
    ],
    ids=["single", "union"],
)
def test_authored_alternatives_intersect_required_gates(
    tmp_path: Path, flags: tuple[str, ...]
) -> None:
    """Loading a manifest must retain alternatives and use their union."""
    _ = (tmp_path / "input.json").write_text(data="true\n", encoding="utf-8")
    alternatives = ", ".join(
        '{kind = "capability_flag", flag = "' + flag + '"}' for flag in flags
    )
    _ = (tmp_path / "case.toml").write_text(
        data=(
            'schema_version = 1\nsuites = ["base"]\n'
            'gates = [{kind = "capability_flag", '
            'flag = "supports_bare_mapping_documents"}]\n'
            f"any_gates = [{alternatives}]\n"
        ),
        encoding="utf-8",
    )
    actual = _selected(
        selection=load_case_manifest(case_dir=tmp_path).selection
    )
    required = _selected(
        selection=CapabilitySelection(
            gates=[
                CapabilityFlagGate(
                    kind="capability_flag",
                    flag="supports_bare_mapping_documents",
                )
            ]
        )
    )
    union: set[literalizer.LanguageCls] = set()
    for flag in flags:
        union.update(
            _selected(
                selection=CapabilitySelection(
                    gates=[
                        CapabilityFlagGate(kind="capability_flag", flag=flag)
                    ]
                )
            )
        )
    expected = required & union
    assert len(expected) > 0
    assert expected < required
    assert actual == expected


def test_omitted_alternatives_do_not_narrow_participation() -> None:
    """Existing selections keep their original unconstrained default."""
    assert _selected(selection=CapabilitySelection()) == set(ALL_LANGUAGES)
