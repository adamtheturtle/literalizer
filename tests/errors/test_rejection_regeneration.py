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
from tests.errors.rejection_manifests import load_rejection_manifest

type _Messages = dict[str, dict[str, str | dict[str, str]]]

_INITIAL = """[ReservedVariableNameError]
"Python['class']" = { default = "modern", "3.12" = "older" }
"Python['def']" = "old"
"Python['stale']" = "deleted case"
[StaleError]
case = "deleted exception"
"""


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
    major, minor = (int(part) for part in version.split(sep="."))
    monkeypatch.setattr(
        target=runner,
        name="sys",
        value=SimpleNamespace(
            version_info=SimpleNamespace(major=major, minor=minor)
        ),
    )
    manifest = load_rejection_manifest(manifest_path=manifest_path)
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
