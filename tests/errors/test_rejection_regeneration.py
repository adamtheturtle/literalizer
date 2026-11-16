"""Versioned rejection snapshots survive real verification and
regeneration.
"""

import subprocess
import sys
import tomllib
from pathlib import Path

import pytest
from pydantic import TypeAdapter

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


def _run_snapshot_pytest(
    *, tmp_path: Path, regenerate: bool
) -> subprocess.CompletedProcess[str]:
    """Exercise the golden runner with real pytest command-line
    options.
    """
    test_path = tmp_path / "test_snapshot.py"
    _ = test_path.write_text(
        data=(
            "from pathlib import Path\n"
            "from tests.errors import test_rejections as runner\n"
            "from tests.errors.rejection_manifests import "
            "load_rejection_manifest\n\n"
            "def test_snapshot(file_regression):\n"
            "    manifest = load_rejection_manifest(\n"
            "        manifest_path=Path(__file__).parent "
            "/ 'case' / 'rejection.toml'\n"
            "    )\n"
            "    runner.test_rejection_messages(\n"
            "        manifest=manifest, file_regression=file_regression\n"
            "    )\n"
        ),
        encoding="utf-8",
    )
    project_root = Path(__file__).resolve().parents[2]
    return subprocess.run(  # noqa: S603 - run the real pytest golden workflow
        args=[
            sys.executable,
            "-m",
            "pytest",
            "-c",
            str(object=project_root / "pyproject.toml"),
            "-o",
            "addopts=",
            "-q",
            "--tb=short",
            str(object=test_path),
            *(["--regen-all"] if regenerate else []),
        ],
        cwd=project_root,
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )


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
) -> None:
    """Both CLI modes reject malformed snapshots without overwriting
    them.
    """
    case_dir = tmp_path / "case"
    case_dir.mkdir()
    manifest = _reserved_name_manifest(tmp_path=case_dir)
    original = (
        "[ReservedVariableNameError]\n\"Python['class']\" = " + message + "\n"
    ).encode(encoding="utf-8")
    _ = manifest.golden_path.write_bytes(data=original)
    completed = _run_snapshot_pytest(tmp_path=tmp_path, regenerate=regenerate)
    assert completed.returncode == pytest.ExitCode.TESTS_FAILED, (
        completed.stdout + completed.stderr
    )
    assert diagnostic in completed.stdout
    assert manifest.golden_path.read_bytes() == original
    assert {path.name for path in case_dir.iterdir()} == {
        "rejection.toml",
        "expected.toml",
    }


def test_missing_snapshot_can_be_regenerated_and_verified(
    tmp_path: Path,
) -> None:
    """Generate a new snapshot from public errors, then verify it."""
    case_dir = tmp_path / "case"
    case_dir.mkdir()
    manifest = _reserved_name_manifest(tmp_path=case_dir)
    assert not manifest.golden_path.exists()
    regenerated = _run_snapshot_pytest(tmp_path=tmp_path, regenerate=True)
    assert regenerated.returncode == pytest.ExitCode.OK, (
        regenerated.stdout + regenerated.stderr
    )
    generated = manifest.golden_path.read_bytes()
    messages = TypeAdapter[_Messages](type=_Messages).validate_python(
        tomllib.loads(generated.decode(encoding="utf-8"))
    )
    assert messages["ReservedVariableNameError"]["Python['class']"] == (
        "Python cannot use NewVariable name 'class': "
        "it is a reserved identifier"
    )
    verified = _run_snapshot_pytest(tmp_path=tmp_path, regenerate=False)
    assert verified.returncode == pytest.ExitCode.OK, (
        verified.stdout + verified.stderr
    )
    assert manifest.golden_path.read_bytes() == generated


@pytest.mark.parametrize(
    argnames="active_override",
    argvalues=[False, True],
    ids=["default_message", "active_override"],
)
def test_versioned_rejection_snapshot_regeneration(
    *,
    tmp_path: Path,
    active_override: bool,
) -> None:
    """Preserve inactive variants and verify real runtime diagnostics."""
    case_dir = tmp_path / "case"
    case_dir.mkdir()
    manifest = _reserved_name_manifest(tmp_path=case_dir)
    current_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    inactive_version = "3.12" if current_version != "3.12" else "3.13"
    version = current_version if active_override else inactive_version
    golden_path = manifest.golden_path
    _ = golden_path.write_text(
        data=_INITIAL.replace('"3.12"', f'"{version}"'), encoding="utf-8"
    )
    regenerated = _run_snapshot_pytest(tmp_path=tmp_path, regenerate=True)
    assert regenerated.returncode == pytest.ExitCode.OK, (
        regenerated.stdout + regenerated.stderr
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
        {"default": "modern", version: class_message}
        if active_override
        else {"default": class_message, version: "older"}
    )
    for name in ("def", "lambda"):
        assert actual[f"Python[{name!r}]"] == (
            f"Python cannot use NewVariable name {name!r}: "
            "it is a reserved identifier"
        )
    assert "Python['stale']" not in actual
    assert "StaleError" not in messages
    verified = _run_snapshot_pytest(tmp_path=tmp_path, regenerate=False)
    assert verified.returncode == pytest.ExitCode.OK, (
        verified.stdout + verified.stderr
    )
    assert golden_path.read_text(encoding="utf-8") == generated
    corrupted = generated.replace(class_message, "incorrect active message")
    _ = golden_path.write_text(data=corrupted, encoding="utf-8")
    failed = _run_snapshot_pytest(tmp_path=tmp_path, regenerate=False)
    assert failed.returncode == pytest.ExitCode.TESTS_FAILED, (
        failed.stdout + failed.stderr
    )
    assert "incorrect active message" in failed.stdout
    assert golden_path.read_text(encoding="utf-8") == corrupted
