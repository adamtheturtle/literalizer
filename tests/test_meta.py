"""Meta-tests for project structure and CI configuration."""

from typing import Any, cast

import pytest
from ruamel.yaml import YAML

from literalizer.languages import ALL_LANGUAGES


@pytest.fixture(scope="session", name="lint_workflow")
def fixture_lint_workflow(
    pytestconfig: pytest.Config,
) -> dict[str, Any]:
    """Parse ``.github/workflows/lint.yml`` once per session."""
    lint_yml = pytestconfig.rootpath / ".github" / "workflows" / "lint.yml"
    ruamel_yaml = YAML()
    loaded = ruamel_yaml.load(stream=lint_yml)  # pyright: ignore[reportUnknownMemberType]
    return cast("dict[str, Any]", loaded)


def test_all_languages_have_lint_workflow(
    lint_workflow: dict[str, Any],
) -> None:
    """Every language has a lint job in the lint workflow."""
    job_ids: set[str] = set(lint_workflow["jobs"])

    # Python is linted by the "build" job (pre-commit hooks),
    # not a dedicated lint workflow.
    no_dedicated_workflow: frozenset[str] = frozenset(
        {"Python"},
    )

    expected_jobs = {
        f"lint-{lang_cls.__name__.lower()}"
        for lang_cls in ALL_LANGUAGES
        if lang_cls.__name__ not in no_dedicated_workflow
    }
    assert expected_jobs <= job_ids


def test_all_lint_jobs_in_completion_gate(
    lint_workflow: dict[str, Any],
) -> None:
    """Every lint job is in completion-lint needs."""
    job_ids: set[str] = set(lint_workflow["jobs"])
    completion_needs: set[str] = set(
        lint_workflow["jobs"]["completion-lint"]["needs"],
    )

    lint_jobs = {jid for jid in job_ids if jid.startswith("lint-")}
    assert lint_jobs <= completion_needs
