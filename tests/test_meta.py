"""Meta-tests for project structure and CI configuration."""

import ast
import pathlib
from typing import Any

import pytest
from beartype import beartype
from ruamel.yaml import YAML

from literalizer.languages import ALL_LANGUAGES

_TESTS_ROOT = pathlib.Path(__file__).parent


@beartype
def _private_literalizer_imports(*, tree: ast.Module) -> list[str]:
    """Return a description of every ``literalizer._*`` import in *tree*.

    ``ast.walk`` visits ``TYPE_CHECKING``-guarded imports too, so this
    catches both module-level and type-checking-only offenders.
    """
    offenders: list[str] = []
    for node in ast.walk(node=tree):
        if isinstance(node, ast.Import):
            offenders.extend(
                f"line {node.lineno}: import {alias.name}"
                for alias in node.names
                if alias.name.startswith("literalizer._")
            )
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            from_private_module = module.startswith("literalizer._")
            private_names = (
                [
                    alias.name
                    for alias in node.names
                    if alias.name.startswith("_")
                ]
                if module == "literalizer"
                else []
            )
            if from_private_module or private_names:
                imported = ", ".join(alias.name for alias in node.names)
                offenders.append(
                    f"line {node.lineno}: from {module} import {imported}"
                )
    return offenders


def test_no_private_literalizer_imports_in_tests() -> None:
    """No ``tests/**/*.py`` file imports from a ``literalizer._*``
    module (issue #1947).

    Private imports pin internal structure and hide public-API gaps;
    tests must exercise the package through its public surface.  This
    check also covers ``TYPE_CHECKING``-only imports so a future test
    cannot reintroduce one.
    """
    violations: dict[str, list[str]] = {}
    for path in sorted(_TESTS_ROOT.rglob(pattern="*.py")):
        tree = ast.parse(source=path.read_text(encoding="utf-8"))
        offenders = _private_literalizer_imports(tree=tree)
        if offenders:
            violations[str(object=path)] = offenders

    assert not violations, (
        "tests/ must not import from private literalizer._* modules; "
        f"offenders: {violations}"
    )


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
