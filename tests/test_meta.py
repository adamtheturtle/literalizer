"""Meta-tests for project structure and CI configuration."""

from typing import Any

import pytest
from beartype import beartype
from ruamel.yaml import YAML

from literalizer.languages import ALL_LANGUAGES


@pytest.fixture(scope="session", name="lint_workflow")
@beartype
def fixture_lint_workflow(
    pytestconfig: pytest.Config,
) -> dict[str, Any]:
    """Parse ``.github/workflows/lint.yml`` once per session."""
    lint_yml = pytestconfig.rootpath / ".github" / "workflows" / "lint.yml"
    ruamel_yaml = YAML()
    loaded: dict[str, Any] = ruamel_yaml.load(stream=lint_yml)  # pyright: ignore[reportUnknownMemberType]
    return loaded


def test_all_languages_have_lint_workflow(
    lint_workflow: dict[str, Any],
) -> None:
    """Every language is covered by a ``Lint <Class>`` step or
    ``lint-<class>`` job.
    """
    job_ids: set[str] = set(lint_workflow["jobs"])
    step_names: set[str] = set()
    for job in lint_workflow["jobs"].values():
        steps: list[dict[str, Any]] = job.get("steps") or []
        for step in steps:
            if "name" in step:
                step_names.add(step["name"])

    # Python is linted by the "build" job (pre-commit hooks),
    # not a dedicated lint workflow.
    no_dedicated_workflow: frozenset[str] = frozenset(
        {"Python"},
    )

    for lang_cls in ALL_LANGUAGES:
        name = lang_cls.__name__
        if name in no_dedicated_workflow:
            continue
        has_dedicated_job = f"lint-{name.lower()}" in job_ids
        has_named_step = f"Lint {name}" in step_names
        assert has_dedicated_job or has_named_step, (
            f"No lint coverage for {name}: "
            f"expected job 'lint-{name.lower()}' or step 'Lint {name}'"
        )


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
