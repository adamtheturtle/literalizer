"""Validation tests for the declared rejection manifests."""

from pathlib import Path

import pytest
from beartype import beartype

from tests.errors.rejection_manifests import (
    GOLDEN_NAME,
    MANIFEST_NAME,
    REJECTIONS_DIR,
    RejectionManifestError,
    load_rejection_manifest,
    load_rejection_manifests,
)

_JSON_TYPE_GATE = (
    'gates = [{ kind = "spec_field_present", field = "json_type" }]'
)
_NO_EXTRA = ""
_CONSTRUCTOR = 'api = "constructor"'


@beartype
def _manifest(
    *,
    selection: str,
    extra: str,
    call: str,
) -> str:
    """Return a manifest with one part of a valid one replaced."""
    return (
        "schema_version = 1\n"
        'summary = "example"\n'
        'exceptions = ["IncompatibleFormatsError"]\n'
        f"{selection}\n{extra}\n[call]\n{call}\n"
    )


@beartype
def _write_manifest(*, tmp_path: Path, manifest: str) -> Path:
    """Create one temporary rejection directory and return its
    manifest.
    """
    rejection_dir = tmp_path / "example"
    rejection_dir.mkdir()
    manifest_path = rejection_dir / MANIFEST_NAME
    manifest_path.write_text(data=manifest, encoding="utf-8")
    return manifest_path


@pytest.mark.parametrize(
    argnames=("manifest", "message"),
    argvalues=[
        (
            _manifest(
                selection=_JSON_TYPE_GATE,
                call=_CONSTRUCTOR,
                extra="mystery = true",
            ),
            "Extra inputs are not permitted",
        ),
        (
            _manifest(
                selection=_JSON_TYPE_GATE, extra=_NO_EXTRA, call=_CONSTRUCTOR
            ).replace(
                '"IncompatibleFormatsError"',
                '"NoSuchError"',
            ),
            "Input should be 'CallArgNotSupportedError'",
        ),
        (
            _manifest(
                selection=_JSON_TYPE_GATE, extra=_NO_EXTRA, call=_CONSTRUCTOR
            ).replace('"IncompatibleFormatsError"', "7"),
            "Input should be a subclass of Exception",
        ),
        (
            _manifest(
                extra=_NO_EXTRA,
                call=_CONSTRUCTOR,
                selection=f'{_JSON_TYPE_GATE}\nlanguages = ["Rust"]',
            ),
            "declare either gates or languages, not both",
        ),
        (
            _manifest(extra=_NO_EXTRA, call=_CONSTRUCTOR, selection=""),
            "declare either gates or languages, not both",
        ),
        (
            _manifest(
                call=_CONSTRUCTOR,
                selection='languages = ["Rust"]',
                extra='[[accepts]]\nlanguages = ["Go"]\nreason = "renders"',
            ),
            "accepts applies to a gated manifest",
        ),
        (
            _manifest(
                selection=_JSON_TYPE_GATE,
                call=_CONSTRUCTOR,
                extra='[[accepts]]\nlanguages = ["Rust", "Go"]\nreason = "x"',
            ),
            "accepts is not in sorted order",
        ),
        (
            _manifest(
                selection=_JSON_TYPE_GATE,
                call=_CONSTRUCTOR,
                extra=(
                    '[[accepts]]\nlanguages = ["Go"]\nreason = "x"\n'
                    '[[accepts]]\nlanguages = ["Go"]\nreason = "y"'
                ),
            ),
            "accepts contains a duplicate entry",
        ),
        (
            _manifest(
                extra=_NO_EXTRA,
                call=_CONSTRUCTOR,
                selection='languages = ["Rust", "Cpp"]',
            ),
            "languages is not in sorted order",
        ),
        (
            _manifest(
                extra=_NO_EXTRA,
                call=_CONSTRUCTOR,
                selection='languages = ["Klingon"]',
            ),
            r"unknown language\(s\) \['Klingon'\]",
        ),
        (
            _manifest(
                selection=_JSON_TYPE_GATE,
                call=_CONSTRUCTOR,
                extra='option = "sorcery"',
            ),
            "unknown option 'sorcery'",
        ),
        (
            _manifest(
                selection=(
                    'gates = [{ kind = "capability_flag", flag = "sorcery" }]'
                ),
                call=_CONSTRUCTOR,
                extra=_NO_EXTRA,
            ),
            "unknown capability flag 'sorcery'",
        ),
        (
            _manifest(
                selection=(
                    'gates = [{ kind = "enum_member_present", '
                    'option = "sorcery", member = "MAGIC" }]'
                ),
                call=_CONSTRUCTOR,
                extra=_NO_EXTRA,
            ),
            "unknown gate option 'sorcery'",
        ),
        (
            _manifest(
                selection=_JSON_TYPE_GATE,
                call=_CONSTRUCTOR,
                extra=(
                    '[[accepts]]\nlanguages = ["Go"]\n'
                    'reason = "not selected by the gate"'
                ),
            ),
            r"accepts language\(s\) not admitted by gates \['Go'\]",
        ),
        (
            _manifest(
                selection=_JSON_TYPE_GATE,
                extra='values = ["b", "a"]',
                call=(
                    'api = "constructor"\nkwargs = [{ kind = "text", '
                    'kwarg = "module_name", value = "{value}" }]'
                ),
            ),
            "values is not in sorted order",
        ),
        (
            _manifest(
                selection=_JSON_TYPE_GATE,
                call=_CONSTRUCTOR,
                extra='values = ["a"]',
            ),
            "declare values exactly when an argument substitutes one",
        ),
        (
            _manifest(
                selection=_JSON_TYPE_GATE,
                extra=_NO_EXTRA,
                call=(
                    'api = "constructor"\nkwargs = [{ kind = "text", '
                    'kwarg = "module_name", value = "{value}" }]'
                ),
            ),
            "declare values exactly when an argument substitutes one",
        ),
        (
            _manifest(
                selection=_JSON_TYPE_GATE,
                extra=_NO_EXTRA,
                call=(
                    'api = "constructor"\nkwargs = [{ kind = "text", '
                    'kwarg = "module_name", value = "{module}" }]'
                ),
            ),
            r"unknown placeholder\(s\) \['module'\]",
        ),
        (
            _manifest(
                selection=_JSON_TYPE_GATE,
                extra=_NO_EXTRA,
                call=(
                    'api = "constructor"\nkwargs = [{ kind = '
                    '"record_shape_names", key_sets = [["id"]], '
                    'names = ["A", "B"] }]'
                ),
            ),
            "key_sets and names must be the same length",
        ),
        (
            _manifest(
                selection=_JSON_TYPE_GATE,
                extra=_NO_EXTRA,
                call='api = "constructor"\nsource = "1"',
            ),
            "requires exactly a source",
        ),
        (
            _manifest(
                selection=_JSON_TYPE_GATE,
                extra=_NO_EXTRA,
                call='api = "literalize"\ninput_format = "yaml"',
            ),
            "requires exactly a source",
        ),
        (
            _manifest(
                selection=_JSON_TYPE_GATE,
                extra=_NO_EXTRA,
                call='api = "literalize"\nsource = "1"',
            ),
            "requires exactly an input_format",
        ),
        (
            _manifest(
                selection=_JSON_TYPE_GATE,
                extra=_NO_EXTRA,
                call=(
                    'api = "literalize"\nsource = "1"\n'
                    'input_format = "json"\ntarget_function = "process"'
                ),
            ),
            "requires exactly a target_function",
        ),
        (
            _manifest(
                selection=_JSON_TYPE_GATE,
                extra=_NO_EXTRA,
                call=(
                    'api = "literalize_call"\nsource = "1"\n'
                    'input_format = "json"\ntarget_function = "process"'
                ),
            ),
            "requires exactly parameter_names",
        ),
        (
            _manifest(
                selection=_JSON_TYPE_GATE,
                extra=_NO_EXTRA,
                call=(
                    'api = "literalize_call"\nsource = "1"\n'
                    'input_format = "json"\ntarget_function = "process"\n'
                    'parameter_names = ["x"]\nmodifiers = ["CONST"]'
                ),
            ),
            "modifiers apply to api = 'literalize'",
        ),
        (
            _manifest(
                selection=_JSON_TYPE_GATE,
                extra=_NO_EXTRA,
                call=(
                    'api = "literalize"\nsource = "1"\ninput_format = "csv"'
                ),
            ),
            "Input should be 'json', 'json5', 'toml', 'yaml'",
        ),
    ],
)
def test_invalid_manifest_is_rejected(
    manifest: str,
    message: str,
    tmp_path: Path,
) -> None:
    """Every declared inconsistency fails when the manifest loads."""
    manifest_path = _write_manifest(tmp_path=tmp_path, manifest=manifest)
    with pytest.raises(
        expected_exception=RejectionManifestError,
        match=message,
    ):
        load_rejection_manifest(manifest_path=manifest_path)


def test_directory_without_manifests_is_rejected(tmp_path: Path) -> None:
    """A rejections directory holding nothing is a mistake, not an
    empty suite.
    """
    with pytest.raises(
        expected_exception=RejectionManifestError,
        match=f"no {MANIFEST_NAME} found",
    ):
        load_rejection_manifests(rejections_dir=tmp_path)


def test_every_rejection_directory_holds_exactly_its_two_files() -> None:
    """No rejection carries a stray file, and none is missing a
    golden.
    """
    expected = {MANIFEST_NAME, GOLDEN_NAME}
    for manifest in load_rejection_manifests(rejections_dir=REJECTIONS_DIR):
        found = {path.name for path in manifest.path.parent.iterdir()}
        assert found == expected, manifest.name


def test_every_rejection_directory_is_declared() -> None:
    """Every directory under ``rejections`` declares a manifest."""
    declared = {
        manifest.path.parent
        for manifest in load_rejection_manifests(
            rejections_dir=REJECTIONS_DIR,
        )
    }
    found = {path for path in REJECTIONS_DIR.iterdir() if path.is_dir()}
    assert found == declared
