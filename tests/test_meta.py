"""Meta-tests for project structure and CI configuration."""

from typing import Any

import pytest
from ruamel.yaml import YAML

from literalizer.languages import ALL_LANGUAGES


def test_all_languages_have_lint_workflow(
    request: pytest.FixtureRequest,
) -> None:
    """Every language has a lint job in lint.yml."""
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

    missing: list[str] = []
    for lang_cls in sorted(
        ALL_LANGUAGES,
        key=lambda c: c.__name__,
    ):
        if lang_cls.__name__ in no_dedicated_workflow:
            continue
        expected = f"lint-{lang_cls.__name__.lower()}"
        if expected not in job_ids:
            name = lang_cls.__name__
            missing.append(
                f"{name} (expected job {expected!r})",
            )

    assert not missing, (
        "Languages missing a lint job in lint.yml:\n"
        + "\n".join(f"  - {m}" for m in missing)
    )


def test_all_lint_jobs_in_completion_gate(
    request: pytest.FixtureRequest,
) -> None:
    """Every lint-* job is in completion-lint.needs."""
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
    missing = lint_jobs - completion_needs

    assert not missing, (
        "Lint jobs not in completion-lint.needs:\n"
        + "\n".join(f"  - {m}" for m in sorted(missing))
    )
