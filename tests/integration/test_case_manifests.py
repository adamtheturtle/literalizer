"""Validation tests for case-local golden coverage manifests."""

from pathlib import Path

import pytest

import literalizer
import literalizer.languages

from .case_manifests import (
    CASE_ROLE_NAMES,
    INDENT_ROLE,
    KEBAB_NEW_VARIABLE_OWNER,
    CaseManifestError,
    RenderContext,
    VariableFormName,
    case_dir_name_for_owner,
    case_dir_name_for_role,
    case_dir_names_for_role,
    case_dir_names_for_variant_axis,
    case_input,
    case_manifests_by_name,
    load_case_manifest,
    load_case_manifests,
    manifest_admits_language,
    variable_form_for_context,
)
from .variant_cases import build_variant_cases, validate_unique_variant_targets


def _write_case(*, tmp_path: Path, manifest: str, input_name: str) -> Path:
    """Create one temporary case directory and return its path."""
    case_dir = tmp_path / "example"
    case_dir.mkdir()
    (case_dir / input_name).write_text(data="value: 1\n", encoding="utf-8")
    (case_dir / "case.toml").write_text(data=manifest, encoding="utf-8")
    return case_dir


@pytest.mark.parametrize(
    argnames=("manifest", "message"),
    argvalues=[
        ('schema_version = 2\nsuites = ["base"]\n', "schema_version"),
        ('schema_version = "1"\nsuites = ["base"]\n', "Input should be 1"),
        (
            'schema_version = 1\nsuites = ["base"]\nextra = true\n',
            "Extra inputs are not permitted",
        ),
        (
            'schema_version = 1\nowner = "mystery"\n',
            "Input should be 'literalize-call'",
        ),
        (
            (
                'schema_version = 1\nsuites = ["base"]\n'
                '[[variants]]\naxis = "made_up"\n'
            ),
            "unknown variant axis",
        ),
        (
            (
                'schema_version = 1\nsuites = ["base"]\n'
                '[[variants]]\naxis = "date"\n'
                '[[variants]]\naxis = "date"\n'
            ),
            "duplicate logical variant case",
        ),
        (
            (
                'schema_version = 1\nsuites = ["base"]\n'
                '[[variants]]\naxis = "date"\n'
                'requires = ["teleportation"]\n'
            ),
            "Input should be 'collection_comments'",
        ),
        (
            (
                'schema_version = 1\nsuites = ["base"]\n'
                '[[variants]]\naxis = "date"\n'
                'requires = ["special_floats", "special_floats"]\n'
            ),
            "requires contains a duplicate entry",
        ),
        (
            'schema_version = 1\nsuites = ["base", "base"]\n',
            "suites contains a duplicate entry",
        ),
        (
            'schema_version = 1\nsuites = ["base"]\nroles = ["mascot"]\n',
            "Input should be 'heterogeneous-strategy-default-input'",
        ),
        (
            (
                'schema_version = 1\nsuites = ["base"]\n'
                'roles = ["indent-input", "indent-input"]\n'
            ),
            "roles contains a duplicate entry",
        ),
        (
            ('schema_version = 1\nsuites = ["base"]\nowner = "variant"\n'),
            "suites and owner are mutually exclusive",
        ),
        (
            "schema_version = 1\n",
            "declare suites or a specialized owner",
        ),
        (
            ('schema_version = 1\nsuites = ["combined"]\n[base_context]\n'),
            "base_context requires participation in the base suite",
        ),
        (
            'schema_version = 1\nowner = "literalize-call"\n',
            r"requires a \[call\] table",
        ),
        (
            (
                'schema_version = 1\nsuites = ["base"]\n'
                "[call]\n"
                'target_function = "process"\n'
                'parameter_names = ["value"]\n'
                "per_element = true\n"
            ),
            r"a \[call\] table requires owner",
        ),
        (
            (
                'schema_version = 1\nowner = "literalize-call"\n'
                "[call]\n"
                'target_function = "process"\n'
                'parameter_names = ["value"]\n'
                "per_element = true\n"
                'call_transform = "emit({bogus})"\n'
            ),
            "unknown call_transform placeholder 'bogus'",
        ),
        (
            (
                'schema_version = 1\nowner = "literalize-call"\n'
                "[call]\n"
                'target_function = "process"\n'
                'parameter_names = ["value"]\n'
                "per_element = true\n"
                'call_style = "mystery"\n'
            ),
            ("Input should be 'command', 'keyword', 'object', 'positional'"),
        ),
        (
            (
                'schema_version = 1\nowner = "literalize-call"\n'
                "[call]\n"
                'target_function = "process"\n'
                'parameter_names = ["value"]\n'
                "per_element = true\n"
                "call_style = 1\n"
            ),
            "call_style",
        ),
        (
            (
                'schema_version = 1\nowner = "literalize-call"\n'
                "[call]\n"
                'target_function = "process"\n'
                'parameter_names = ["value"]\n'
                "per_element = true\n"
                "call_transform = 1\n"
            ),
            "call_transform",
        ),
        (
            (
                'schema_version = 1\nowner = "literalize-call"\n'
                "[call]\n"
                'target_function = "process"\n'
                'parameter_names = ["value"]\n'
                "per_element = true\n"
                'zip_input_format = "mystery"\n'
            ),
            "Input should be 'json', 'json5', 'toml', 'yaml'",
        ),
        (
            (
                'schema_version = 1\nowner = "literalize-call"\n'
                "[call]\n"
                'target_function = "process"\n'
                'parameter_names = ["value"]\n'
                "per_element = true\n"
                'variable_form = "mystery"\n'
            ),
            "Input should be 'existing', 'new'",
        ),
        (
            (
                'schema_version = 1\nowner = "literalize-call"\n'
                "[call]\n"
                'target_function = "process"\n'
                'parameter_names = ["value"]\n'
                "per_element = true\n"
                '[[call.variants]]\naxis = "made_up"\n'
            ),
            "unknown variant axis 'made_up'",
        ),
        (
            (
                'schema_version = 1\nowner = "literalize-call"\n'
                "[call]\n"
                'target_function = "process"\n'
                'parameter_names = ["value"]\n'
                "per_element = true\n"
                '[[call.variants]]\naxis = "json_type"\n'
                '[[call.variants]]\naxis = "json_type"\n'
            ),
            "duplicate call variant axis",
        ),
        (
            (
                'schema_version = 1\nowner = "literalize-call"\n'
                "[call]\n"
                'target_function = "process"\n'
                'parameter_names = ["value"]\n'
                "per_element = true\n"
                "variant_only = true\n"
            ),
            "variant_only requires at least one call variant axis",
        ),
        (
            'schema_version = 1\nowner = "literalize-ref"\n',
            r"requires a \[ref\] table",
        ),
        (
            'schema_version = 1\nowner = "literalize-ref-default"\n',
            r"requires a \[ref\] table",
        ),
        (
            'schema_version = 1\nsuites = ["base"]\n[ref]\n',
            (
                r"a \[ref\] table requires owner = 'literalize-ref' or "
                "'literalize-ref-default'"
            ),
        ),
        (
            'schema_version = 1\nowner = "variant"\n[ref]\n',
            r"a \[ref\] table requires owner",
        ),
        (
            (
                'schema_version = 1\nowner = "literalize-ref"\n'
                "[ref]\n"
                'ref_case_override = "mystery"\n'
            ),
            (
                "Input should be 'camel', 'kebab', 'pascal', 'snake', "
                "'upper_snake'"
            ),
        ),
        (
            (
                'schema_version = 1\nowner = "literalize-ref"\n'
                "[ref]\n"
                "ref_case_override = 1\n"
            ),
            "ref_case_override",
        ),
        (
            (
                'schema_version = 1\nowner = "literalize-ref"\n'
                "[ref]\n"
                "extra = true\n"
            ),
            "Extra inputs are not permitted",
        ),
        (
            'schema_version = 1\nsuites = ["base"]\nlanguages = ["Python"]\n',
            "languages and languages_reason require each other",
        ),
        (
            (
                'schema_version = 1\nsuites = ["base"]\n'
                'languages_reason = "sampled"\n'
            ),
            "languages and languages_reason require each other",
        ),
        (
            (
                'schema_version = 1\nsuites = ["base"]\n'
                'languages = ["Python"]\nlanguages_reason = "sampled"\n'
                'gates = [{ kind = "capability_flag", '
                'flag = "supports_comments" }]\n'
            ),
            "declare either languages or gates, not both",
        ),
        (
            (
                'schema_version = 1\nsuites = ["base"]\n'
                'gates = [{ kind = "vibes", name = "x" }]\n'
            ),
            "does not match any of the expected tags",
        ),
        (
            (
                'schema_version = 1\nsuites = ["base"]\n'
                'gates = [{ kind = "capability_flag", '
                'flag = "supports_vibes" }]\n'
            ),
            "gates: unknown capability flag 'supports_vibes'",
        ),
        (
            (
                'schema_version = 1\nsuites = ["base"]\n'
                'gates = [{ kind = "enum_member_present", option = "vibe", '
                'member = "RECORD" }]\n'
            ),
            "gates: unknown option 'vibe'",
        ),
        (
            (
                'schema_version = 1\nowner = "literalize-ref"\n'
                "[ref]\n"
                'languages = ["Python"]\n'
            ),
            "languages and languages_reason require each other",
        ),
        (
            (
                'schema_version = 1\nowner = "literalize-call"\n'
                "[call]\n"
                'target_function = "process"\n'
                'parameter_names = ["value"]\n'
                "per_element = true\n"
                'languages = ["Python"]\n'
            ),
            "languages and languages_reason require each other",
        ),
        (
            (
                'schema_version = 1\nsuites = ["base"]\n'
                'languages = ["Pythonic"]\nlanguages_reason = "sampled"\n'
            ),
            "Input should be",
        ),
    ],
)
def test_invalid_manifest_is_actionable(
    tmp_path: Path,
    manifest: str,
    message: str,
) -> None:
    """Invalid schema data reports the manifest and specific problem."""
    case_dir = _write_case(
        tmp_path=tmp_path, manifest=manifest, input_name="input.yaml"
    )
    with pytest.raises(expected_exception=CaseManifestError, match=message):
        load_case_manifest(case_dir=case_dir)


def test_invalid_toml_is_actionable(tmp_path: Path) -> None:
    """TOML syntax errors retain the manifest path and parser detail."""
    case_dir = _write_case(
        tmp_path=tmp_path,
        manifest="schema_version = [\n",
        input_name="input.yaml",
    )
    with pytest.raises(
        expected_exception=CaseManifestError,
        match="invalid TOML",
    ):
        load_case_manifest(case_dir=case_dir)


def test_missing_manifest_is_actionable(tmp_path: Path) -> None:
    """A case directory cannot silently participate without a manifest."""
    case_dir = tmp_path / "example"
    case_dir.mkdir()
    with pytest.raises(
        expected_exception=CaseManifestError,
        match="manifest is missing",
    ):
        load_case_manifest(case_dir=case_dir)


def test_manifest_inventory_is_keyed_in_directory_order(
    tmp_path: Path,
) -> None:
    """The shared inventory preserves stable case-directory ordering."""
    for name in ("second", "first"):
        case_dir = tmp_path / name
        case_dir.mkdir()
        (case_dir / "input.yaml").write_text(
            data="value: 1\n",
            encoding="utf-8",
        )
        (case_dir / "case.toml").write_text(
            data='schema_version = 1\nsuites = ["base"]\n',
            encoding="utf-8",
        )

    manifests = case_manifests_by_name(cases_dir=tmp_path)
    assert tuple(manifests) == ("first", "second")
    assert manifests["first"].case_dir == tmp_path / "first"


def test_declared_input_must_exist(tmp_path: Path) -> None:
    """An explicit input cannot silently fall back to another file."""
    case_dir = _write_case(
        tmp_path=tmp_path,
        manifest=(
            'schema_version = 1\ninput = "input.json"\nsuites = ["base"]\n'
        ),
        input_name="input.yaml",
    )
    with pytest.raises(
        expected_exception=CaseManifestError,
        match="declared input does not exist",
    ):
        load_case_manifest(case_dir=case_dir)


def test_declared_input_name_must_be_supported(tmp_path: Path) -> None:
    """An explicit input must use one of the supported file names."""
    case_dir = _write_case(
        tmp_path=tmp_path,
        manifest=(
            'schema_version = 1\ninput = "data.yaml"\nsuites = ["base"]\n'
        ),
        input_name="input.yaml",
    )
    with pytest.raises(
        expected_exception=CaseManifestError,
        match="input must name one of",
    ):
        load_case_manifest(case_dir=case_dir)


def test_input_inference_requires_a_candidate(tmp_path: Path) -> None:
    """Input inference fails when the case contains no supported input."""
    case_dir = tmp_path / "example"
    case_dir.mkdir()
    (case_dir / "case.toml").write_text(
        data='schema_version = 1\nsuites = ["base"]\n',
        encoding="utf-8",
    )

    with pytest.raises(
        expected_exception=CaseManifestError,
        match="expected exactly one inferable input file",
    ):
        load_case_manifest(case_dir=case_dir)


def test_input_inference_rejects_multiple_candidates(tmp_path: Path) -> None:
    """Input inference fails when more than one supported input exists."""
    case_dir = _write_case(
        tmp_path=tmp_path,
        manifest='schema_version = 1\nsuites = ["base"]\n',
        input_name="input.yaml",
    )
    (case_dir / "input.json").write_text(data="{}\n", encoding="utf-8")

    with pytest.raises(
        expected_exception=CaseManifestError,
        match="expected exactly one inferable input file",
    ):
        load_case_manifest(case_dir=case_dir)


def test_case_input_returns_manifest_input(tmp_path: Path) -> None:
    """The harness helper returns the input validated by the manifest."""
    case_dir = _write_case(
        tmp_path=tmp_path,
        manifest='schema_version = 1\nsuites = ["base"]\n',
        input_name="input.yaml",
    )

    assert (
        case_input(case_dir=case_dir)
        == load_case_manifest(case_dir=case_dir).input
    )


def test_render_context_is_loaded(tmp_path: Path) -> None:
    """Simple rendering arguments load into the typed context."""
    expected_pre_indent_level = 2
    case_dir = _write_case(
        tmp_path=tmp_path,
        manifest=(
            "schema_version = 1\n"
            'suites = ["base", "combined"]\n'
            "[base_context]\n"
            'variable_form = "existing"\n'
            'collection_layout = "multiline"\n'
            "pre_indent_level = 2\n"
            "[base_context.record_null_substitutions]\n"
            "missing = -1\n"
        ),
        input_name="input.yaml",
    )
    context = load_case_manifest(case_dir=case_dir).base_context
    assert context.variable_form == "existing"
    assert context.collection_layout == "multiline"
    assert context.pre_indent_level == expected_pre_indent_level
    assert context.record_null_substitutions == {"missing": -1}


def test_ref_table_is_loaded(tmp_path: Path) -> None:
    """A ``[ref]`` table resolves its case name and defaults its key."""
    case_dir = _write_case(
        tmp_path=tmp_path,
        manifest=(
            "schema_version = 1\n"
            'owner = "literalize-ref"\n'
            "[ref]\n"
            'ref_case_override = "camel"\n'
            "[ref.value_sources]\n"
            'my_int = "42"\n'
        ),
        input_name="input.yaml",
    )
    ref = load_case_manifest(case_dir=case_dir).ref
    assert ref is not None
    assert ref.case_dir_name == "example"
    assert ref.ref_key == "$ref"
    assert ref.ref_case_override == literalizer.IdentifierCase.CAMEL
    assert ref.value_sources == {"my_int": "42"}


def test_gates_select_the_languages_declaring_the_property(
    tmp_path: Path,
) -> None:
    """A gated case renders under the languages the property admits."""
    case_dir = _write_case(
        tmp_path=tmp_path,
        manifest=(
            "schema_version = 1\n"
            'suites = ["base"]\n'
            'gates = [{ kind = "metadata_field", '
            'field = "nested_list_widening", value = "integer_width" }]\n'
        ),
        input_name="input.yaml",
    )
    manifest = load_case_manifest(case_dir=case_dir)
    selected = [
        lang_cls.__name__
        for lang_cls in literalizer.languages.ALL_LANGUAGES
        if manifest_admits_language(manifest=manifest, lang_cls=lang_cls)
    ]
    assert sorted(selected) == ["Nim", "V"]


def test_an_ungated_case_selects_every_language(tmp_path: Path) -> None:
    """A case narrowing nothing renders under every language."""
    case_dir = _write_case(
        tmp_path=tmp_path,
        manifest='schema_version = 1\nsuites = ["base"]\n',
        input_name="input.yaml",
    )
    manifest = load_case_manifest(case_dir=case_dir)
    assert all(
        manifest_admits_language(manifest=manifest, lang_cls=lang_cls)
        for lang_cls in literalizer.languages.ALL_LANGUAGES
    )


def test_named_languages_select_themselves(tmp_path: Path) -> None:
    """A case naming its languages renders under exactly those."""
    case_dir = _write_case(
        tmp_path=tmp_path,
        manifest=(
            "schema_version = 1\n"
            'suites = ["base"]\n'
            'languages = ["Python"]\n'
            'languages_reason = "Sampled: one language shows this."\n'
        ),
        input_name="input.yaml",
    )
    manifest = load_case_manifest(case_dir=case_dir)
    selected = [
        lang_cls.__name__
        for lang_cls in literalizer.languages.ALL_LANGUAGES
        if manifest_admits_language(manifest=manifest, lang_cls=lang_cls)
    ]
    assert selected == ["Python"]


def test_every_named_language_set_records_its_reason(cases_dir: Path) -> None:
    """No case narrows to named languages without saying why.

    A narrowing that follows from a language property is a ``gates``
    entry; one that does not names its languages and says which it is,
    so a pin and a deliberate one-language sample stay distinguishable
    rather than reading alike.
    """
    unexplained = sorted(
        manifest.case_dir.name
        for manifest in load_case_manifests(cases_dir=cases_dir)
        for selection in (
            manifest.selection,
            *(table for table in (manifest.call, manifest.ref) if table),
        )
        if selection.languages and selection.languages_reason is None
    )
    assert unexplained == []


def test_owner_lookup_requires_exactly_one_case(tmp_path: Path) -> None:
    """An owner naming a single fixture cannot match zero directories."""
    _write_case(
        tmp_path=tmp_path,
        manifest='schema_version = 1\nsuites = ["base"]\n',
        input_name="input.yaml",
    )
    with pytest.raises(
        expected_exception=CaseManifestError,
        match="expected exactly one case with owner 'new-variable-kebab'",
    ):
        case_dir_name_for_owner(
            cases_dir=tmp_path,
            owner=KEBAB_NEW_VARIABLE_OWNER,
        )


def test_every_declared_role_has_a_case(cases_dir: Path) -> None:
    """Every role the schema accepts is claimed by a real case."""
    for role in sorted(CASE_ROLE_NAMES):
        assert case_dir_names_for_role(cases_dir=cases_dir, role=role)


def test_role_lookup_requires_a_declaring_case(tmp_path: Path) -> None:
    """A role no case declares fails naming the role and the manifest."""
    _write_case(
        tmp_path=tmp_path,
        manifest='schema_version = 1\nsuites = ["base"]\n',
        input_name="input.yaml",
    )
    with pytest.raises(
        expected_exception=CaseManifestError,
        match=r"no case\.toml under .* declares roles = \['indent-input'\]",
    ):
        case_dir_names_for_role(cases_dir=tmp_path, role=INDENT_ROLE)


def test_sole_role_lookup_rejects_a_shared_role(tmp_path: Path) -> None:
    """A role two cases declare cannot be read as a single fixture."""
    manifest = (
        'schema_version = 1\nsuites = ["base"]\nroles = ["indent-input"]\n'
    )
    for name in ("first", "second"):
        case_dir = tmp_path / name
        case_dir.mkdir()
        (case_dir / "input.yaml").write_text(
            data="value: 1\n",
            encoding="utf-8",
        )
        (case_dir / "case.toml").write_text(data=manifest, encoding="utf-8")
    with pytest.raises(
        expected_exception=CaseManifestError,
        match=(
            "expected exactly one case.toml declaring "
            r"roles = \['indent-input'\], found \['first', 'second'\]"
        ),
    ):
        case_dir_name_for_role(cases_dir=tmp_path, role=INDENT_ROLE)


def test_variant_axis_lookup_finds_no_case_for_an_unused_axis(
    cases_dir: Path,
) -> None:
    """An axis no case declares expands to no inputs."""
    assert not case_dir_names_for_variant_axis(
        cases_dir=cases_dir,
        axis="not_an_axis",
    )


@pytest.mark.parametrize(
    argnames=("name", "expected_type"),
    argvalues=[
        ("new", literalizer.NewVariable),
        ("existing", literalizer.ExistingVariable),
        ("both", literalizer.BothVariableForms),
    ],
)
def test_variable_form_for_context(
    name: VariableFormName,
    expected_type: type[literalizer.VariableForm],
) -> None:
    """Every manifest variable form maps to its public API
    representation.
    """
    variable_form = variable_form_for_context(
        context=RenderContext(variable_form=name)
    )
    assert isinstance(variable_form, expected_type)


def test_duplicate_golden_target_is_actionable() -> None:
    """Resolved path collisions fail instead of disappearing into a
    set.
    """
    example = build_variant_cases()[0]
    with pytest.raises(
        expected_exception=CaseManifestError,
        match="duplicate golden target",
    ):
        validate_unique_variant_targets(cases=[example, example])
