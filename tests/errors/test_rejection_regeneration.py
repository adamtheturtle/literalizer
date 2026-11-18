"""Versioned rejection snapshots survive real verification and
regeneration.
"""

import sys
import tomllib
from pathlib import Path

import pytest
from pydantic import TypeAdapter

from tests.errors import test_rejections as rejection_runner
from tests.errors.rejection_manifests import (
    RejectionManifest,
    load_rejection_manifest,
)

pytest_plugins: tuple[str, ...] = ("pytester",)

type _Messages = dict[str, dict[str, str | dict[str, str]]]

_INITIAL = """[ReservedVariableNameError]
"Python['class']" = { default = "modern", "3.12" = "older" }
"Python['def']" = "old"
"Python['stale']" = "deleted case"
[StaleError]
case = "deleted exception"
"""


def _reserved_name_manifest(*, tmp_path: Path) -> RejectionManifest:
    """Load a real rejection scenario for snapshot life cycle checks."""
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
    *, pytester: pytest.Pytester, regenerate: bool
) -> pytest.RunResult:
    """Exercise the golden runner with real pytest command-line
    options.
    """
    # Keep the runner and its fixture types loaded across pytester runs.
    test_path = pytester.makepyfile(
        test_snapshot=(
            "from pathlib import Path\n"
            f"import {rejection_runner.__name__} as runner\n"
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
    )
    _ = pytester.makeini(source="[pytest]")
    return pytester.runpytest_inprocess(
        "--disable-plugin-autoload",
        "-p",
        "pytest_regressions.plugin",
        "-p",
        "pytest_datadir.plugin",
        "-q",
        "--tb=short",
        test_path,
        *(["--regen-all"] if regenerate else []),
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
    pytester: pytest.Pytester,
    message: str,
    diagnostic: str,
    regenerate: bool,
) -> None:
    """Reject malformed snapshots in both modes without overwriting
    them.
    """
    case_dir = pytester.path / "case"
    case_dir.mkdir()
    manifest = _reserved_name_manifest(tmp_path=case_dir)
    original = (
        "[ReservedVariableNameError]\n\"Python['class']\" = " + message + "\n"
    ).encode(encoding="utf-8")
    _ = manifest.golden_path.write_bytes(data=original)
    result = _run_snapshot_pytest(pytester=pytester, regenerate=regenerate)
    assert result.ret == pytest.ExitCode.TESTS_FAILED
    assert diagnostic in result.stdout.str()
    assert manifest.golden_path.read_bytes() == original
    assert {path.name for path in case_dir.iterdir()} == {
        "rejection.toml",
        "expected.toml",
    }


def test_missing_snapshot_can_be_regenerated_and_verified(
    pytester: pytest.Pytester,
) -> None:
    """Generate a new snapshot from public errors, then verify it."""
    case_dir = pytester.path / "case"
    case_dir.mkdir()
    manifest = _reserved_name_manifest(tmp_path=case_dir)
    assert not manifest.golden_path.exists()
    regenerated = _run_snapshot_pytest(pytester=pytester, regenerate=True)
    assert regenerated.ret == pytest.ExitCode.OK
    generated = manifest.golden_path.read_bytes()
    messages = TypeAdapter[_Messages](type=_Messages).validate_python(
        tomllib.loads(generated.decode(encoding="utf-8"))
    )
    assert messages["ReservedVariableNameError"]["Python['class']"] == (
        "Python cannot use NewVariable name 'class': "
        "it is a reserved identifier"
    )
    verified = _run_snapshot_pytest(pytester=pytester, regenerate=False)
    assert verified.ret == pytest.ExitCode.OK
    assert manifest.golden_path.read_bytes() == generated


@pytest.mark.parametrize(
    argnames="active_override",
    argvalues=[False, True],
    ids=["default_message", "active_override"],
)
def test_versioned_rejection_snapshot_regeneration(
    *,
    pytester: pytest.Pytester,
    active_override: bool,
) -> None:
    """Preserve inactive variants and verify real runtime diagnostics."""
    case_dir = pytester.path / "case"
    case_dir.mkdir()
    manifest = _reserved_name_manifest(tmp_path=case_dir)
    current_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    inactive_version = "3.12" if current_version != "3.12" else "3.13"
    version = current_version if active_override else inactive_version
    golden_path = manifest.golden_path
    _ = golden_path.write_text(
        data=_INITIAL.replace('"3.12"', f'"{version}"'), encoding="utf-8"
    )
    regenerated = _run_snapshot_pytest(pytester=pytester, regenerate=True)
    assert regenerated.ret == pytest.ExitCode.OK
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
    verified = _run_snapshot_pytest(pytester=pytester, regenerate=False)
    assert verified.ret == pytest.ExitCode.OK
    assert golden_path.read_text(encoding="utf-8") == generated
    corrupted = generated.replace(class_message, "incorrect active message")
    _ = golden_path.write_text(data=corrupted, encoding="utf-8")
    failed = _run_snapshot_pytest(pytester=pytester, regenerate=False)
    assert failed.ret == pytest.ExitCode.TESTS_FAILED
    assert "incorrect active message" in failed.stdout.str()
    assert golden_path.read_text(encoding="utf-8") == corrupted
