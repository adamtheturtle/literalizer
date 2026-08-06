"""Tests for the declared variant-axis expansion plans."""

from pathlib import Path

import pytest

from literalizer import CollectionLayout
from literalizer.languages import ALL_LANGUAGES

from .case_manifests import CaseManifestError
from .language_specs import make_spec
from .variant_axis_names import KNOWN_VARIANT_AXES, SPECIAL_VARIANT_AXES
from .variant_cases import (
    ESCAPE_HATCH_VARIANT_AXES,
    _HasJsonType,  # pyright: ignore[reportPrivateUsage]
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
from .variant_types import find_enum_member

# The axes that resolve to a typed Python builder instead of a declared
# plan.  This list may shrink, never grow: a new axis belongs in
# ``axes.toml``.
_EXPECTED_ESCAPE_HATCH_AXES = frozenset(
    {
        "comment_terminator",
        "string_embedded_nul",
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

_VALID_KWARG_VALUES_AXIS = """
schema_version = 1

[axes.example]
plan = "kwarg_values"
name_template = "{lang}_example_{format}"
kwarg = "multiline_raw_string_delimiter_base"
values = [{ name = "punctuation", value = "!?" }]
"""

_VALID_FILTERED_AXIS = """
schema_version = 1

[axes.example]
plan = "filtered"
base = "date"
"""

_VALID_CROSS_AXIS = """
schema_version = 1

[axes.example]
plan = "cross_product"
name_template = "{lang}_example_{format}_{tag}_{secondary}"
primary = "date_format"
secondaries = [{ tag = "dt", option = "datetime_format" }]
"""

_VALID_PAIRED_AXES = """
schema_version = 1

[axes.base]
plan = "every_non_default_member"
name_template = "{lang}_base_{format}"
option = "date_format"

[axes.example]
plan = "fixed_overrides"
name_template = "{lang}_example_{format}"
primary_axis = "base"
"""

_CHAINED_OVERRIDES_AXES = """
schema_version = 1

[axes.source]
plan = "fixed_overrides"
name_template = "{lang}_source"
overrides = [
  { kind = "true_flag", kwarg = "record_unify_optional_fields" },
]

[axes.other]
plan = "fixed_overrides"
name_template = "{lang}_other"
overrides_from = "source"

[axes.example]
plan = "fixed_overrides"
name_template = "{lang}_example"
overrides_from = "other"
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


def test_json_type_axis_covers_every_capable_language() -> None:
    """Every language with a JSON value type gets JSON-type variants.

    The axis selects languages by the presence of the ``json_type``
    field, so a future JSON-capable language cannot land without
    coverage.
    """
    supported = {
        lang_cls
        for lang_cls in ALL_LANGUAGES
        if isinstance(make_spec(lang_cls=lang_cls), _HasJsonType)
    }
    covered = {
        variant.lang_cls for variant in variants_for_axis(axis_key="json_type")
    }

    assert covered == supported


def test_json_type_name_suffixes_rename_a_member() -> None:
    """A declared JSON-type variant name suffix does something.

    The suffix belongs to a JSON-capable language and differs from the
    member name it stands in for, so neither a dead override nor a
    silent duplicate of the member name survives.
    """
    for lang_cls in ALL_LANGUAGES:
        suffix = lang_cls.json_type_variant_name_suffix
        if suffix is None:
            continue
        spec = make_spec(lang_cls=lang_cls)

        assert isinstance(spec, _HasJsonType), lang_cls.__name__
        assert suffix not in {
            member.name.lower()
            for member in spec.json_types
            if member is not spec.json_type
        }, lang_cls.__name__


def test_layout_paired_axis_renders_both_layouts() -> None:
    """A declared pair of layouts renders each variant twice.

    The compact and multiline paths render a widened literal
    separately, so each participating language contributes one variant
    per layout under one spec.
    """
    variants = variants_for_axis(axis_key="empty_map_narrowing")
    by_layout = {
        layout: sorted(
            variant.name
            for variant in variants
            if variant.collection_layout is layout
        )
        for layout in CollectionLayout
    }

    assert by_layout[CollectionLayout.MULTILINE] == [
        f"{name}_multiline" for name in by_layout[CollectionLayout.COMPACT]
    ]
    assert by_layout[CollectionLayout.COMPACT] != []


def test_behavior_flag_gate_selects_the_widening_languages() -> None:
    """The ``RECORD`` fallback axis follows the rendering behavior.

    A language reaches the axis when its ``RECORD`` strategy widens the
    nested sibling maps no record shape fits, so gaining that behavior
    is what enrolls it rather than a list naming it.
    """
    widening = set[str]()
    for lang_cls in ALL_LANGUAGES:
        strategy = find_enum_member(
            enum_cls=make_spec(lang_cls=lang_cls).heterogeneous_strategies,
            name="RECORD",
        )
        if strategy is None:
            continue
        spec = make_spec(lang_cls=lang_cls, heterogeneous_strategy=strategy)
        behavior = spec.heterogeneous_behavior
        if behavior.widens_unrecordizable_nested_sibling_maps:
            widening.add(lang_cls.__name__)
    covered = {
        variant.lang_cls.__name__
        for variant in variants_for_axis(axis_key="record_nested_map_fallback")
    }

    assert covered == widening


def test_nested_map_widening_axes_partition_their_languages() -> None:
    """The two nested-map widening axes never share a language.

    They render one input under one name, so a language reaching both
    would claim one golden path twice.
    """
    declared = {
        variant.lang_cls
        for variant in variants_for_axis(axis_key="nested_map_widening")
    }
    wrapping = {
        variant.lang_cls
        for variant in variants_for_axis(
            axis_key="nested_map_widening_scalar_wrapping"
        )
    }

    assert declared & wrapping == set()
    assert wrapping != set()


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
            _VALID_CROSS_AXIS.replace("_{tag}_{secondary}", ""),
            r"name template omits placeholder\(s\) \['secondary', 'tag'\]",
        ),
        (
            _VALID_CROSS_AXIS.replace('primary = "date_format"\n', ""),
            r"unknown name-template placeholder\(s\) \['format'\]",
        ),
        (
            _VALID_CROSS_AXIS.replace(
                'option = "datetime_format"',
                'option = "vibe"',
            ),
            "unknown option 'vibe'",
        ),
        (
            _VALID_AXIS + 'member_name_source = "vibes"\n',
            "unknown member name source 'vibes'",
        ),
        (
            _VALID_AXIS
            + 'gates = [{ kind = "metadata_field", field = "vibe", '
            'value = "default" }]\n',
            "unknown metadata field 'vibe'",
        ),
        (
            _VALID_AXIS + 'gates = [{ kind = "spec_config_field_present", '
            'field = "vibe_config.vibe" }]\n',
            "unknown spec config field 'vibe_config.vibe'",
        ),
        (
            _VALID_AXIS
            + 'gates = [{ kind = "behavior_flag", flag = "vibes" }]\n',
            "unknown behavior flag 'vibes'",
        ),
        (
            _VALID_AXIS
            + (
                'overrides = [{ kind = "behavior_flag_member", '
                'option = "heterogeneous_strategy", flag = "vibes" }]\n'
            ),
            "unknown behavior flag 'vibes'",
        ),
        (
            _VALID_AXIS + 'gates = [{ kind = "metadata_table_present", '
            'table = "vibes" }]\n',
            "unknown metadata table 'vibes'",
        ),
        (
            _VALID_AXIS
            + (
                'overrides = [{ kind = "metadata_table", kwarg = "vibes", '
                'table = "vibes" }]\n'
            ),
            "unknown metadata table 'vibes'",
        ),
        (
            _VALID_KWARG_VALUES_AXIS.replace("_{format}", ""),
            r"name template omits placeholder\(s\) \['format'\]",
        ),
        (
            _VALID_AXIS + 'layouts = [{ layout = "SIDEWAYS" }]\n',
            "unknown layout 'SIDEWAYS'",
        ),
        (
            _VALID_FIXED_AXIS + 'name_metadata_field = "vibes"\n',
            "unknown name metadata field 'vibes'",
        ),
        (
            _VALID_FIXED_AXIS
            + 'name_metadata_field = "collection_layout_category"\n',
            r"name template omits placeholder\(s\) \['category'\]",
        ),
        (
            _VALID_FIXED_AXIS.replace("{lang}_example", "{lang}_{category}"),
            r"unknown name-template placeholder\(s\) \['category'\]",
        ),
        (
            _VALID_CROSS_AXIS + 'primary_axis = "date"\n',
            "declares both a 'primary' option and a 'primary_axis'",
        ),
        (
            _VALID_PAIRED_AXES.replace("{lang}_example_{format}", "{lang}_x"),
            r"name template omits placeholder\(s\) \['format'\]",
        ),
        (
            _VALID_PAIRED_AXES.replace('primary_axis = "base"', ""),
            r"unknown name-template placeholder\(s\) \['format'\]",
        ),
        (
            _VALID_PAIRED_AXES.replace(
                'primary_axis = "base"', 'primary_axis = "vibes"'
            ),
            "primary axis 'vibes' is not a declared",
        ),
        (
            _VALID_PAIRED_AXES
            + (
                '[[axes.base.overrides]]\nkind = "true_flag"\n'
                'kwarg = "record_unify_optional_fields"\n'
            ),
            "primary axis 'base' declares overrides",
        ),
        (
            _VALID_FIXED_AXIS + 'overrides_from = "vibes"\n',
            "unknown overrides source 'vibes'",
        ),
        (
            _CHAINED_OVERRIDES_AXES,
            "overrides source 'other' reuses overrides itself",
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


_UNDECLARED_TABLE_MEMBER_AXIS = """
schema_version = 1

[axes.example]
plan = "fixed_overrides"
name_template = "{lang}_example"

[[axes.example.overrides]]
kind = "metadata_enum_member"
option = "heterogeneous_strategy"
field = "empty_container_type_hint_heterogeneous_strategy"
"""

_UNDECLARED_TABLE_AXIS = """
schema_version = 1

[axes.example]
plan = "fixed_overrides"
name_template = "{lang}_example"

[[axes.example.overrides]]
kind = "metadata_table"
kwarg = "empty_container_type_hints"
table = "empty_container_type_hints"
"""


@pytest.mark.parametrize(
    argnames=("contents", "message"),
    argvalues=[
        (_UNDECLARED_SAMPLE_AXIS, "declares no sample value for 'type_name'"),
        (
            _UNDECLARED_METADATA_AXIS,
            "declares no 'heterogeneous_value_variant_name_strategy'",
        ),
        (
            _UNDECLARED_TABLE_MEMBER_AXIS,
            "declares no 'empty_container_type_hint_heterogeneous_strategy'",
        ),
        (
            _UNDECLARED_TABLE_AXIS,
            "declares no 'empty_container_type_hints'",
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
