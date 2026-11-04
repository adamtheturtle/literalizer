"""Validation tests for case-local golden coverage manifests."""

from pathlib import Path
from typing import Literal

import pytest
from pydantic import BaseModel, TypeAdapter

import literalizer.languages
from tests.integration.case_discovery import load_case_data
from tests.integration.case_manifests import (
    CASE_ROLE_NAMES,
    INDENT_ROLE,
    KEBAB_NEW_VARIABLE_OWNER,
    CaseManifestError,
    case_dir_name_for_owner,
    case_dir_name_for_role,
    case_dir_names_for_role,
    case_dir_names_for_variant_axis,
    case_input,
    case_manifests_by_name,
    load_case_manifest,
    manifest_admits_language,
)
from tests.integration.variant_cases import (
    build_variant_cases,
    validate_unique_variant_targets,
)
from tests.toml_cases import load_toml_cases


class _ManifestErrorCase(BaseModel, extra="forbid", frozen=True):
    """One invalid manifest and its diagnostic."""

    name: str
    manifest: str
    message: str


class _ReferenceErrorCase(BaseModel, extra="forbid", frozen=True):
    """One invalid typed reference source."""

    name: str
    field: str
    source: str


class _Cases(BaseModel, extra="forbid", frozen=True):
    """Manifest validation scenarios declared in TOML."""

    cases: tuple[_ManifestErrorCase, ...]
    references: tuple[_ReferenceErrorCase, ...]


_CASES = TypeAdapter(type=_Cases).validate_python(
    load_toml_cases(name="case_manifest_validation")
)


@pytest.mark.parametrize(argnames="table", argvalues=["call", "ref"])
@pytest.mark.parametrize(
    argnames=("failure", "message"),
    argvalues=[
        ("missing_primary", "requires its primary API table"),
        ("unnamed", "requires an example name"),
        ("duplicate", "contains a duplicate example name"),
        ("primary_named", "primary API tables cannot name an example"),
        ("invalid_name", "String should match pattern"),
    ],
)
def test_api_examples_reject_ambiguous_ownership(
    tmp_path: Path,
    table: Literal["call", "ref"],
    failure: str,
    message: str,
) -> None:
    """Examples must have one shared input owner and unique golden
    names.
    """
    fields = (
        'target_function = "target"\nparameter_names = ["value"]\n'
        "per_element = false\n"
        if table == "call"
        else 'variable_name = "result"\n'
    )
    primary = f"[{table}]\n{fields}"
    example = f'[[{table}_examples]]\nexample = "native"\n{fields}'
    if failure == "missing_primary":
        primary = ""
    elif failure == "unnamed":
        example = f"[[{table}_examples]]\n{fields}"
    elif failure == "duplicate":
        example += example
    elif failure == "primary_named":
        primary = f'[{table}]\nexample = "native"\n{fields}'
    else:
        example = example.replace('"native"', '"invalid-name"')
    case_dir = _write_case(
        tmp_path=tmp_path,
        manifest=(
            f'schema_version = 1\nowner = "literalize-{table}"\n'
            f"{primary}{example}"
        ),
        input_name="input.yaml",
    )
    with pytest.raises(expected_exception=CaseManifestError, match=message):
        _ = load_case_manifest(case_dir=case_dir)


def _write_case(*, tmp_path: Path, manifest: str, input_name: str) -> Path:
    """Create one temporary case directory and return its path."""
    case_dir = tmp_path / "example"
    case_dir.mkdir()
    _ = (case_dir / input_name).write_text(data="value: 1\n", encoding="utf-8")
    _ = (case_dir / "case.toml").write_text(data=manifest, encoding="utf-8")
    return case_dir


@pytest.mark.parametrize(
    argnames="case", argvalues=_CASES.cases, ids=lambda case: case.name
)
def test_invalid_manifest_is_actionable(
    tmp_path: Path, case: _ManifestErrorCase
) -> None:
    """Invalid schema data reports the manifest and specific problem."""
    case_dir = _write_case(
        tmp_path=tmp_path, manifest=case.manifest, input_name="input.yaml"
    )
    with pytest.raises(
        expected_exception=CaseManifestError, match=case.message
    ):
        _ = load_case_manifest(case_dir=case_dir)


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
        _ = load_case_manifest(case_dir=case_dir)


def test_missing_manifest_is_actionable(tmp_path: Path) -> None:
    """A case directory cannot silently participate without a manifest."""
    case_dir = tmp_path / "example"
    case_dir.mkdir()
    with pytest.raises(
        expected_exception=CaseManifestError,
        match="manifest is missing",
    ):
        _ = load_case_manifest(case_dir=case_dir)


def test_manifest_inventory_is_keyed_in_directory_order(
    tmp_path: Path,
) -> None:
    """The shared inventory preserves stable case-directory ordering."""
    for name in ("second", "first"):
        case_dir = tmp_path / name
        case_dir.mkdir()
        _ = (case_dir / "input.yaml").write_text(
            data="value: 1\n",
            encoding="utf-8",
        )
        _ = (case_dir / "case.toml").write_text(
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
        _ = load_case_manifest(case_dir=case_dir)


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
        _ = load_case_manifest(case_dir=case_dir)


def test_input_inference_requires_a_candidate(tmp_path: Path) -> None:
    """Input inference fails when the case contains no supported input."""
    case_dir = tmp_path / "example"
    case_dir.mkdir()
    _ = (case_dir / "case.toml").write_text(
        data='schema_version = 1\nsuites = ["base"]\n',
        encoding="utf-8",
    )

    with pytest.raises(
        expected_exception=CaseManifestError,
        match="expected exactly one inferable input file",
    ):
        _ = load_case_manifest(case_dir=case_dir)


def test_input_inference_rejects_multiple_candidates(tmp_path: Path) -> None:
    """Input inference fails when more than one supported input exists."""
    case_dir = _write_case(
        tmp_path=tmp_path,
        manifest='schema_version = 1\nsuites = ["base"]\n',
        input_name="input.yaml",
    )
    _ = (case_dir / "input.json").write_text(data="{}\n", encoding="utf-8")

    with pytest.raises(
        expected_exception=CaseManifestError,
        match="expected exactly one inferable input file",
    ):
        _ = load_case_manifest(case_dir=case_dir)


@pytest.mark.parametrize(argnames="count", argvalues=[1, 3])
def test_anchor_warning_count_must_match_input(
    tmp_path: Path, count: int
) -> None:
    """Reject a manifest whose warning count disagrees with its YAML."""
    case_dir = _write_case(
        tmp_path=tmp_path,
        manifest=(
            'schema_version = 1\nsuites = ["base"]\n'
            '[expected_reused_anchor_warning]\nanchor = "other+"\n'
            f"count = {count}\n"
        ),
        input_name="input.yaml",
    )
    source = (
        Path(__file__).parents[1]
        / "cases"
        / "yaml_rebound_anchor_multiple"
        / "input.yaml"
    ).read_text(encoding="utf-8")
    _ = (case_dir / "input.yaml").write_text(data=source, encoding="utf-8")
    with pytest.raises(
        expected_exception=pytest.fail.Exception,
        match=f"Expected {count} reused-anchor warnings for 'other\\+', got 2",
    ):
        _ = load_case_data(input_info=case_input(case_dir=case_dir))


def test_anchor_warning_requires_yaml(tmp_path: Path) -> None:
    """A YAML parser warning cannot be declared for another input
    format.
    """
    case_dir = _write_case(
        tmp_path=tmp_path,
        manifest=(
            'schema_version = 1\nsuites = ["base"]\n'
            '[expected_reused_anchor_warning]\nanchor = "x"\ncount = 1\n'
        ),
        input_name="input.json",
    )
    with pytest.raises(
        expected_exception=CaseManifestError,
        match="expected_reused_anchor_warning requires YAML input",
    ):
        _ = load_case_manifest(case_dir=case_dir)


def test_input_roundtrip_rejects_non_literal_owner(tmp_path: Path) -> None:
    """Other runners cannot silently ignore a declared roundtrip."""
    case_dir = _write_case(
        tmp_path=tmp_path,
        manifest=(
            "schema_version = 1\n"
            'owner = "literalize-ref"\n'
            "[ref]\n"
            "[input_roundtrip]\n"
            'language = "Jsonc"\n'
            'input_format = "jsonc"\n'
        ),
        input_name="input.yaml",
    )
    with pytest.raises(
        expected_exception=CaseManifestError,
        match="input_roundtrip requires a literal rendering suite",
    ):
        _ = load_case_manifest(case_dir=case_dir)


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


def test_owner_lookup_requires_exactly_one_case(tmp_path: Path) -> None:
    """An owner naming a single fixture cannot match zero directories."""
    _ = _write_case(
        tmp_path=tmp_path,
        manifest='schema_version = 1\nsuites = ["base"]\n',
        input_name="input.yaml",
    )
    with pytest.raises(
        expected_exception=CaseManifestError,
        match="expected exactly one case with owner 'new-variable-kebab'",
    ):
        _ = case_dir_name_for_owner(
            cases_dir=tmp_path,
            owner=KEBAB_NEW_VARIABLE_OWNER,
        )


def test_every_declared_role_has_a_case(cases_dir: Path) -> None:
    """Every role the schema accepts is claimed by a real case."""
    for role in sorted(CASE_ROLE_NAMES):
        assert len(case_dir_names_for_role(cases_dir=cases_dir, role=role)) > 0


def test_role_lookup_requires_a_declaring_case(tmp_path: Path) -> None:
    """A role no case declares fails naming the role and the manifest."""
    _ = _write_case(
        tmp_path=tmp_path,
        manifest='schema_version = 1\nsuites = ["base"]\n',
        input_name="input.yaml",
    )
    with pytest.raises(
        expected_exception=CaseManifestError,
        match=r"no case\.toml under .* declares roles = \['indent-input'\]",
    ):
        _ = case_dir_names_for_role(cases_dir=tmp_path, role=INDENT_ROLE)


def test_sole_role_lookup_rejects_a_shared_role(tmp_path: Path) -> None:
    """A role two cases declare cannot be read as a single fixture."""
    manifest = (
        'schema_version = 1\nsuites = ["base"]\nroles = ["indent-input"]\n'
    )
    for name in ("first", "second"):
        case_dir = tmp_path / name
        case_dir.mkdir()
        _ = (case_dir / "input.yaml").write_text(
            data="value: 1\n",
            encoding="utf-8",
        )
        _ = (case_dir / "case.toml").write_text(
            data=manifest,
            encoding="utf-8",
        )
    with pytest.raises(
        expected_exception=CaseManifestError,
        match=(
            "expected exactly one case.toml declaring "
            r"roles = \['indent-input'\], found \['first', 'second'\]"
        ),
    ):
        _ = case_dir_name_for_role(cases_dir=tmp_path, role=INDENT_ROLE)


def test_variant_axis_lookup_finds_no_case_for_an_unused_axis(
    cases_dir: Path,
) -> None:
    """An axis no case declares expands to no inputs."""
    assert (
        len(
            case_dir_names_for_variant_axis(
                cases_dir=cases_dir, axis="not_an_axis"
            )
        )
        == 0
    )


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


@pytest.mark.parametrize(
    argnames="case", argvalues=_CASES.references, ids=lambda case: case.name
)
def test_invalid_reference_value_source(
    tmp_path: Path, case: _ReferenceErrorCase
) -> None:
    """Malformed native bindings fail with their owning manifest path."""
    case_dir = _write_case(
        tmp_path=tmp_path,
        manifest=(
            "schema_version = 1\n"
            'owner = "literalize-ref-default"\n'
            "[ref]\n"
            f"{case.field} = {{ value = {case.source} }}\n"
        ),
        input_name="input.json",
    )
    with pytest.raises(
        expected_exception=CaseManifestError, match=rf"{case.field}\.value"
    ):
        _ = load_case_manifest(case_dir=case_dir)


def test_modifier_gate_selects_supported_declarations(tmp_path: Path) -> None:
    """A declarative modifier requirement admits only supporting specs."""
    case_dir = _write_case(
        tmp_path=tmp_path,
        manifest=(
            "schema_version = 1\n"
            'suites = ["base"]\n'
            'gates = [{kind = "modifier_present", modifier = "PUBLIC"}]\n'
        ),
        input_name="input.yaml",
    )
    manifest = load_case_manifest(case_dir=case_dir)
    assert manifest_admits_language(
        manifest=manifest, lang_cls=literalizer.languages.Java
    )
    assert not manifest_admits_language(
        manifest=manifest, lang_cls=literalizer.languages.Python
    )


@pytest.mark.parametrize(
    argnames="grammar_gate",
    argvalues=[
        '{kind = "call_literal_flag", flag = "verbatim_strings"}',
        '{kind = "call_character_quote", quote = "\'"}',
        '{kind = "call_hash_raw_prefix", prefix = "r", marker = "#"}',
        '{kind = "call_identifier_prefix", prefix = "`"}',
        '{kind = "call_raw_string_prefix", prefix = "r"}',
        '{kind = "call_interpolation", opener = "${", quotes = "\'"}',
    ],
)
def test_literal_grammar_gates_compose_with_call_capabilities(
    tmp_path: Path, grammar_gate: str
) -> None:
    """Adding a satisfied call requirement preserves grammar selection."""
    text = (
        'schema_version = 1\nsuites = ["base"]\ngates = ['
        + grammar_gate
        + "]\n"
    )
    grammar_path = tmp_path / "grammar"
    grammar_path.mkdir()
    case_dir = _write_case(
        tmp_path=grammar_path, manifest=text, input_name="input.yaml"
    )
    grammar_only = load_case_manifest(case_dir=case_dir)
    combined = text.replace(
        "gates = [",
        'gates = [{kind = "capability_flag", flag = "declares_call_styles"}, ',
    )
    combined_path = tmp_path / "combined"
    combined_path.mkdir()
    combined_dir = _write_case(
        tmp_path=combined_path, manifest=combined, input_name="input.yaml"
    )
    with_capability = load_case_manifest(case_dir=combined_dir)
    admitted = {
        lang_cls
        for lang_cls in literalizer.languages.ALL_LANGUAGES
        if manifest_admits_language(manifest=grammar_only, lang_cls=lang_cls)
    }
    combined_admitted = {
        lang_cls
        for lang_cls in literalizer.languages.ALL_LANGUAGES
        if manifest_admits_language(
            manifest=with_capability, lang_cls=lang_cls
        )
    }
    assert len(admitted) > 0
    assert admitted == combined_admitted


@pytest.mark.parametrize(
    argnames="grammar_gate",
    argvalues=[
        '{kind = "call_character_quote", quote = "~"}',
        '{kind = "call_hash_raw_prefix", prefix = "r", marker = "@"}',
        '{kind = "call_hash_raw_prefix", prefix = "unknown", marker = "#"}',
        '{kind = "call_identifier_prefix", prefix = "#"}',
    ],
)
def test_unsupported_token_grammars_admit_no_producers(
    tmp_path: Path, grammar_gate: str
) -> None:
    """A similar token family does not admit an incompatible delimiter."""
    text = (
        'schema_version = 1\nsuites = ["base"]\ngates = ['
        + grammar_gate
        + "]\n"
    )
    case_dir = _write_case(
        tmp_path=tmp_path, manifest=text, input_name="input.yaml"
    )
    manifest = load_case_manifest(case_dir=case_dir)
    admitted = [
        lang_cls
        for lang_cls in literalizer.languages.ALL_LANGUAGES
        if manifest_admits_language(manifest=manifest, lang_cls=lang_cls)
    ]
    assert len(admitted) == 0
