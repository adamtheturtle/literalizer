"""Exercise case lookup through the fixture inventory CLI."""

from click.testing import CliRunner

from tests.integration.list_fixtures import CASES_DIR, main


def test_case_lookup_includes_sibling_golden_and_authored_inputs() -> None:
    """Select by owning case even when the golden lives elsewhere."""
    result = CliRunner().invoke(
        cli=main,
        args=[
            "--case",
            "default_module_name",
            "--language",
            "Java",
            "--include-authored",
        ],
    )
    case_dir = CASES_DIR / "default_module_name"
    default_dir = CASES_DIR.parent / "default_module_names"
    assert result.exit_code == 0
    assert result.output_bytes == b"".join(
        f"{path}".encode() + b"\0"
        for path in (
            case_dir / "case.toml",
            case_dir / "input.yaml",
            default_dir / "Java_default_module_name@jdk_11.java",
            default_dir / "Java_default_module_name@jdk_16.java",
        )
    )
