"""Versioned rejection snapshots survive real verification and
regeneration.
"""

import tomllib
from pathlib import Path
from types import SimpleNamespace

import pytest
from pydantic import TypeAdapter
from pytest_regressions.file_regression import FileRegressionFixture

from tests.errors import test_rejections as runner
from tests.errors.rejection_manifests import (
    RejectionManifest,
    load_rejection_manifest,
)

type _Messages = dict[str, dict[str, str | dict[str, str]]]

_INITIAL = """[ReservedVariableNameError]
"Python['class']" = { default = "modern", "3.12" = "older" }
"Python['def']" = "old"
"Python['stale']" = "deleted case"
[StaleError]
case = "deleted exception"
"""


def _reserved_name_manifest(*, tmp_path: Path) -> RejectionManifest:
    """Load a real rejection scenario for snapshot lifecycle checks."""
    manifest_path = tmp_path / "rejection.toml"
    _ = manifest_path.write_text(
        data=(
            "schema_version = 1\n"
            'summary = "Versioned diagnostic regeneration"\n'
            'exceptions = ["ReservedVariableNameError"]\n'
            'values = ["class", "def", "lambda"]\n'
            "[call]\n"
            'api = "literalize"\n'
            "sources = ['42']\n"
            'input_format = "json"\n'
            'variable_form = "new"\n'
            'variable_name = "{value}"\n'
        ),
        encoding="utf-8",
    )
    return load_rejection_manifest(manifest_path=manifest_path)


@pytest.mark.parametrize(argnames="regenerate", argvalues=[False, True])
@pytest.mark.parametrize(
    argnames=("message", "diagnostic"),
    argvalues=[
        pytest.param(
            '{ "3.12" = "old" }',
            "requires a default",
            id="missing_default",
        ),
        pytest.param(
            '{ default = "new", py312 = "old" }',
            "invalid Python version key",
            id="invalid_named_version",
        ),
        pytest.param(
            '{ default = "new", "3.12.1" = "old" }',
            "invalid Python version key",
            id="patch_version_not_supported",
        ),
        pytest.param(
            "{ default = 1 }", "valid string", id="non_string_default"
        ),
        pytest.param("1", "valid string", id="non_string_message"),
    ],
)
def test_invalid_snapshot_survives_verification_and_regeneration(
    *,
    tmp_path: Path,
    message: str,
    diagnostic: str,
    regenerate: bool,
    file_regression: FileRegressionFixture,
    monkeypatch: pytest.MonkeyPatch,
    request: pytest.FixtureRequest,
) -> None:
    """Real rendering must reject malformed snapshots without overwriting
    them.
    """
    manifest = _reserved_name_manifest(tmp_path=tmp_path)
    original = (
        "[ReservedVariableNameError]\n\"Python['class']\" = " + message + "\n"
    ).encode(encoding="utf-8")
    _ = manifest.golden_path.write_bytes(data=original)
    monkeypatch.setattr(
        target=request.config.option, name="regen_all", value=regenerate
    )
    with pytest.raises(expected_exception=ValueError, match=diagnostic):
        runner.test_rejection_messages(
            manifest=manifest, file_regression=file_regression
        )
    assert manifest.golden_path.read_bytes() == original
    assert {path.name for path in tmp_path.iterdir()} == {
        "rejection.toml",
        "expected.toml",
    }


def test_missing_snapshot_can_be_regenerated_and_verified(
    tmp_path: Path,
    file_regression: FileRegressionFixture,
    monkeypatch: pytest.MonkeyPatch,
    request: pytest.FixtureRequest,
) -> None:
    """Generate a new snapshot from public errors, then verify it."""
    manifest = _reserved_name_manifest(tmp_path=tmp_path)
    assert not manifest.golden_path.exists()
    monkeypatch.setattr(
        target=request.config.option, name="regen_all", value=True
    )
    runner.test_rejection_messages(
        manifest=manifest, file_regression=file_regression
    )
    generated = manifest.golden_path.read_bytes()
    messages = TypeAdapter[_Messages](type=_Messages).validate_python(
        tomllib.loads(generated.decode(encoding="utf-8"))
    )
    assert messages["ReservedVariableNameError"]["Python['class']"] == (
        "Python cannot use NewVariable name 'class': "
        "it is a reserved identifier"
    )
    monkeypatch.setattr(
        target=request.config.option, name="regen_all", value=False
    )
    runner.test_rejection_messages(
        manifest=manifest, file_regression=file_regression
    )
    assert manifest.golden_path.read_bytes() == generated


@pytest.mark.parametrize(
    argnames="version", argvalues=["3.12", "3.13", "3.99"]
)
def test_versioned_rejection_snapshot_regeneration(
    tmp_path: Path,
    version: str,
    file_regression: FileRegressionFixture,
    monkeypatch: pytest.MonkeyPatch,
    request: pytest.FixtureRequest,
) -> None:
    """Render real errors, preserve inactive variants, and verify the
    result.

    Only the runner's version selector is simulated; rendering uses the
    current interpreter and every language admitted by the manifest.
    """
    manifest = _reserved_name_manifest(tmp_path=tmp_path)
    major, minor = (int(part) for part in version.split(sep="."))
    monkeypatch.setattr(
        target=runner,
        name="sys",
        value=SimpleNamespace(
            version_info=SimpleNamespace(major=major, minor=minor)
        ),
    )
    golden_path = manifest.golden_path
    _ = golden_path.write_text(data=_INITIAL, encoding="utf-8")
    monkeypatch.setattr(
        target=request.config.option, name="regen_all", value=True
    )
    runner.test_rejection_messages(
        manifest=manifest, file_regression=file_regression
    )
    generated = golden_path.read_text(encoding="utf-8")
    messages = TypeAdapter[_Messages](type=_Messages).validate_python(
        tomllib.loads(generated)
    )
    actual = messages["ReservedVariableNameError"]
    class_message = (
        "Python cannot use NewVariable name 'class': "
        "it is a reserved identifier"
    )
    assert actual["Python['class']"] == (
        {"default": "modern", "3.12": class_message}
        if version == "3.12"
        else {"default": class_message, "3.12": "older"}
    )
    for name in ("def", "lambda"):
        assert actual[f"Python[{name!r}]"] == (
            f"Python cannot use NewVariable name {name!r}: "
            "it is a reserved identifier"
        )
    assert "Python['stale']" not in actual
    assert "StaleError" not in messages
    monkeypatch.setattr(
        target=request.config.option, name="regen_all", value=False
    )
    runner.test_rejection_messages(
        manifest=manifest, file_regression=file_regression
    )
    assert golden_path.read_text(encoding="utf-8") == generated
    corrupted = generated.replace(class_message, "incorrect active message")
    _ = golden_path.write_text(data=corrupted, encoding="utf-8")
    with pytest.raises(expected_exception=AssertionError):
        runner.test_rejection_messages(
            manifest=manifest, file_regression=file_regression
        )
    assert golden_path.read_text(encoding="utf-8") == corrupted
