"""Meta-tests for project structure and CI configuration."""

from typing import Annotated

import pytest
from beartype import beartype
from pydantic import AliasPath, BaseModel, Field
from ruamel.yaml import YAML

from literalizer._language import LanguageCls
from literalizer.languages import ALL_LANGUAGES


class _NamedLintStep(BaseModel):
    """Workflow step carrying the display name these tests inspect."""

    name: str


type _LintStep = _NamedLintStep | dict[str, object]


class _LintJob(BaseModel):
    """Workflow job fields inspected by these tests."""

    steps: tuple[_LintStep, ...]


class _LintWorkflow(BaseModel):
    """Validated subset of the lint workflow document."""

    jobs: dict[str, _LintJob]
    completion_needs: Annotated[
        tuple[str, ...],
        Field(validation_alias=AliasPath("jobs", "completion-lint", "needs")),
    ]


@pytest.fixture(scope="session", name="lint_workflow")
@beartype
def fixture_lint_workflow(
    pytestconfig: pytest.Config,
) -> _LintWorkflow:
    """Parse ``.github/workflows/lint.yml`` once per session."""
    lint_yml = pytestconfig.rootpath / ".github" / "workflows" / "lint.yml"
    ruamel_yaml = YAML()
    loaded: object = ruamel_yaml.load(  # pyright: ignore[reportUnknownMemberType]
        stream=lint_yml,
    )
    return _LintWorkflow.model_validate(obj=loaded)


def test_all_languages_have_lint_workflow(
    lint_workflow: _LintWorkflow,
) -> None:
    """Every language is covered by a ``Lint <Class>`` step or
    ``lint-<class>`` job.
    """
    jobs = lint_workflow.jobs
    job_ids: set[str] = set(jobs)
    step_names: set[str] = set()
    for job in jobs.values():
        for step in job.steps:
            if isinstance(step, _NamedLintStep):
                step_names.add(step.name)

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
    lint_workflow: _LintWorkflow,
) -> None:
    """Every lint job is in completion-lint needs."""
    jobs = lint_workflow.jobs
    job_ids: set[str] = set(jobs)
    completion_needs = set(lint_workflow.completion_needs)

    lint_jobs = {jid for jid in job_ids if jid.startswith("lint-")}
    assert lint_jobs <= completion_needs


def test_every_language_declares_the_explicit_attributes() -> None:
    """No language inherits a behavior it has not said something about.

    :attr:`~literalizer._language.LanguageCls.explicit_language_attributes`
    names what each language declares for itself.  No default is
    held for any of them, so a language that leaves one out reads as an
    attribute error at render time (issue #4655).
    """
    absent = {
        language_cls.__name__: sorted(
            name
            for name in LanguageCls.explicit_language_attributes
            if name not in vars(language_cls)
        )
        for language_cls in ALL_LANGUAGES
    }
    assert {
        name: names for name, names in absent.items() if len(names) > 0
    } == {}
