"""Tests for the declared variant-axis expansion plans."""

from pathlib import Path

import pytest

from .case_manifests import CaseManifestError
from .variant_axis_names import KNOWN_VARIANT_AXES, SPECIAL_VARIANT_AXES
from .variant_cases import (
    ESCAPE_HATCH_VARIANT_AXES,
    check_axis_coverage,
    variants_for_axis,
)
from .variant_plans import (
    AxisPlanError,
    declared_axis_names,
    load_axis_registry,
    variants_for_declared_axis,
    variants_for_registry_axis,
)

# The axes that resolve to a typed Python builder instead of a declared
# plan.  This list may shrink, never grow: a new axis belongs in
# ``axes.toml``.
_EXPECTED_ESCAPE_HATCH_AXES = frozenset(
    {
        "collection_layout",
        "comment_terminator",
        "dhall_nested_map_widening",
        "dict_decl",
        "empty_container_type_hint",
        "empty_map_narrowing",
        "heterogeneous_strategy_datetime_cross",
        "json_type",
        "json_type_bytes_cross",
        "json_type_datetime_cross",
        "json_type_declaration_cross",
        "json_type_language_version_cross",
        "json_type_record_shape_names_cross",
        "language_version_cross_dict_type",
        "multiline_raw_string_delimiter",
        "nested_map_widening",
        "numeric_style_datetime_cross",
        "record_nested_map_fallback",
        "record_numeric_cross",
        "sequence_decl",
        "set_decl",
        "statement_terminator_style_decl",
        "string_embedded_nul",
        "string_format_date_cross",
        "string_format_datetime_cross",
        "type_hints_cross",
        "typed_dict_null_filtering",
    }
)

_VALID_AXIS = """
schema_version = 1

[axes.example]
plan = "every_non_default_member"
name_template = "{lang}_example_{format}"
option = "date_format"
"""

_VALID_FIXED_AXIS = """
schema_version = 1

[axes.example]
plan = "fixed_overrides"
name_template = "{lang}_example"
"""

_VALID_FILTERED_AXIS = """
schema_version = 1

[axes.example]
plan = "filtered"
base = "date"
"""


def _write_registry(*, tmp_path: Path, contents: str) -> Path:
    """Write one temporary axis registry and return its path."""
    path = tmp_path / "axes.toml"
    path.write_text(data=contents, encoding="utf-8")
    return path


def test_escape_hatch_set_does_not_grow() -> None:
    """The irregular tail stays exactly as small as it is today."""
    assert ESCAPE_HATCH_VARIANT_AXES == _EXPECTED_ESCAPE_HATCH_AXES


def test_every_axis_resolves_to_exactly_one_expansion() -> None:
    """Each expandable axis has one plan or one escape-hatch builder."""
    declared = declared_axis_names()

    assert declared & ESCAPE_HATCH_VARIANT_AXES == frozenset()
    assert declared | ESCAPE_HATCH_VARIANT_AXES == (
        KNOWN_VARIANT_AXES - SPECIAL_VARIANT_AXES
    )


def test_every_declared_axis_expands() -> None:
    """No declared plan silently expands to nothing."""
    for axis_key in sorted(declared_axis_names()):
        assert variants_for_declared_axis(
            axis_key=axis_key,
            resolve_axis=variants_for_axis,
        ), axis_key


def test_declared_axis_names_are_unique_per_language() -> None:
    """A plan never gives one language two identically named
    variants.
    """
    for axis_key in sorted(declared_axis_names()):
        variants = variants_for_declared_axis(
            axis_key=axis_key,
            resolve_axis=variants_for_axis,
        )
        keyed = {
            (variant.name, variant.spec.language_version)
            for variant in variants
        }

        assert len(keyed) == len(variants), axis_key


def test_filtered_axis_narrows_its_base() -> None:
    """A filtered plan keeps its base axis's variants for the languages
    its gates admit, and nothing else.
    """
    base = variants_for_axis(axis_key="json_type")

    assert variants_for_axis(axis_key="json_type_call_result") == [
        variant
        for variant in base
        if variant.lang_cls.supports_json_call_result_binding
    ]


def test_unknown_axis_is_actionable() -> None:
    """An axis with no plan and no builder names both options."""
    with pytest.raises(
        expected_exception=AxisPlanError,
        match="no plan declared for variant axis 'mystery'",
    ):
        variants_for_axis(axis_key="mystery")


@pytest.mark.parametrize(
    argnames=("contents", "message"),
    argvalues=[
        ("schema_version = 2\n[axes]\n", "schema_version"),
        (
            _VALID_AXIS.replace(
                'plan = "every_non_default_member"',
                'plan = "invent"',
            ),
            "does not match any of the expected tags",
        ),
        (
            _VALID_AXIS + 'gates = [{ kind = "vibes", name = "x" }]\n',
            "does not match any of the expected tags",
        ),
        (
            _VALID_AXIS + 'overrides = [{ kind = "vibes", name = "x" }]\n',
            "does not match any of the expected tags",
        ),
        (
            _VALID_AXIS.replace("{lang}_example_{format}", "{lang}_{mystery}"),
            r"unknown name-template placeholder\(s\) \['mystery'\]",
        ),
        (
            _VALID_FIXED_AXIS.replace("{lang}_example", "{lang}_{value}"),
            "needs exactly one override marked 'name_value'",
        ),
        (
            _VALID_AXIS.replace('option = "date_format"', 'option = "vibe"'),
            "unknown option 'vibe'",
        ),
        (
            _VALID_AXIS
            + (
                'gates = [{ kind = "capability_flag", '
                'flag = "supports_vibes" }]\n'
            ),
            "unknown capability flag 'supports_vibes'",
        ),
        (
            _VALID_AXIS
            + 'gates = [{ kind = "spec_field_present", field = "vibe" }]\n',
            "unknown spec field 'vibe'",
        ),
        (
            _VALID_AXIS
            + (
                'overrides = [{ kind = "metadata_enum_member", '
                'option = "language_version", field = "vibe" }]\n'
            ),
            "unknown metadata field 'vibe'",
        ),
        (
            _VALID_AXIS
            + (
                'overrides = [{ kind = "enum_member", '
                'option = "vibe", member = "RECORD" }]\n'
            ),
            "unknown option 'vibe'",
        ),
        (
            _VALID_AXIS
            + (
                'overrides = [{ kind = "non_default_kwarg", '
                'kwarg = "type_name", name_value = true }]\n'
            ),
            "needs exactly one override marked 'name_value'",
        ),
        (
            _VALID_FILTERED_AXIS.replace('base = "date"', 'base = "vibes"'),
            "unknown base axis 'vibes'",
        ),
        (
            _VALID_FILTERED_AXIS.replace('base = "date"', 'base = "example"'),
            "base axis is itself",
        ),
        (
            _VALID_FILTERED_AXIS
            + (
                'gates = [{ kind = "capability_flag", '
                'flag = "supports_vibes" }]\n'
            ),
            "unknown capability flag 'supports_vibes'",
        ),
    ],
)
def test_invalid_registry_is_actionable(
    tmp_path: Path,
    contents: str,
    message: str,
) -> None:
    """Bad plan data fails when the registry loads, not at render
    time.
    """
    path = _write_registry(tmp_path=tmp_path, contents=contents)
    with pytest.raises(expected_exception=AxisPlanError, match=message):
        load_axis_registry(path=path)


def test_invalid_toml_is_actionable(tmp_path: Path) -> None:
    """TOML syntax errors retain the file path and parser detail."""
    path = _write_registry(tmp_path=tmp_path, contents="axes = [\n")
    with pytest.raises(
        expected_exception=AxisPlanError,
        match="invalid TOML",
    ):
        load_axis_registry(path=path)


@pytest.mark.parametrize(
    argnames=("declared", "escape_hatch", "message"),
    argvalues=[
        (
            frozenset({"date", "json_type"}),
            frozenset({"json_type"}),
            "both declared in axes.toml and registered",
        ),
        (
            frozenset({"date"}),
            frozenset[str](),
            r"\['json_type'\] have no expansion",
        ),
        (
            frozenset({"date", "vibes"}),
            frozenset({"json_type"}),
            r"\['vibes'\] expand but are not in KNOWN_VARIANT_AXES",
        ),
    ],
)
def test_axis_coverage_gaps_are_actionable(
    declared: frozenset[str],
    escape_hatch: frozenset[str],
    message: str,
) -> None:
    """An axis with no expansion, or two, names what to do about it."""
    with pytest.raises(expected_exception=CaseManifestError, match=message):
        check_axis_coverage(
            expandable=frozenset({"date", "json_type"}),
            declared=declared,
            escape_hatch=escape_hatch,
        )


_UNDECLARED_SAMPLE_AXIS = """
schema_version = 1

[axes.example]
plan = "fixed_overrides"
name_template = "{lang}_example"
overrides = [{ kind = "non_default_kwarg", kwarg = "type_name" }]
"""

_UNDECLARED_METADATA_AXIS = """
schema_version = 1

[axes.example]
plan = "fixed_overrides"
name_template = "{lang}_example"

[[axes.example.overrides]]
kind = "metadata_enum_member"
option = "heterogeneous_strategy"
field = "heterogeneous_value_variant_name_strategy"
"""


@pytest.mark.parametrize(
    argnames=("contents", "message"),
    argvalues=[
        (_UNDECLARED_SAMPLE_AXIS, "declares no sample value for 'type_name'"),
        (
            _UNDECLARED_METADATA_AXIS,
            "declares no 'heterogeneous_value_variant_name_strategy'",
        ),
    ],
)
def test_missing_language_metadata_is_actionable(
    tmp_path: Path,
    contents: str,
    message: str,
) -> None:
    """A plan reading absent metadata names the file that lacks it.

    Language metadata and the axis registry are separate files, so an
    override with no matching gate can outlive the value it reads.
    Expansion says which language file is missing what, rather than
    building a spec from a silently dropped setting.
    """
    path = _write_registry(tmp_path=tmp_path, contents=contents)
    with pytest.raises(expected_exception=AxisPlanError, match=message):
        variants_for_registry_axis(
            path=path,
            axis_key="example",
            resolve_axis=variants_for_axis,
        )
