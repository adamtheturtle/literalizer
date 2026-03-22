"""Meta-tests for project structure and CI configuration."""

from typing import Any

import pytest
from ruamel.yaml import YAML

from literalizer.languages import ALL_LANGUAGES


def test_all_languages_have_lint_workflow(
    request: pytest.FixtureRequest,
) -> None:
    """Every language has a lint job in the lint workflow."""
    lint_yml = request.config.rootpath / ".github" / "workflows" / "lint.yml"
    ruamel_yaml = YAML()
    workflow: dict[str, Any] = ruamel_yaml.load(  # pyright: ignore[reportUnknownMemberType]
        stream=lint_yml,
    )
    job_ids: set[str] = set(workflow["jobs"])

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
    request: pytest.FixtureRequest,
) -> None:
    """Every lint job is in completion-lint needs."""
    lint_yml = request.config.rootpath / ".github" / "workflows" / "lint.yml"
    ruamel_yaml = YAML()
    workflow: dict[str, Any] = ruamel_yaml.load(  # pyright: ignore[reportUnknownMemberType]
        stream=lint_yml,
    )
    job_ids: set[str] = set(workflow["jobs"])
    completion_needs: set[str] = set(
        workflow["jobs"]["completion-lint"]["needs"],
    )

    lint_jobs = {jid for jid in job_ids if jid.startswith("lint-")}
    assert lint_jobs <= completion_needs
