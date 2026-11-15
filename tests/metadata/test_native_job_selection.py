"""Check repository-specific native CI filters against their consumers."""

import ast
import re
from collections import defaultdict
from pathlib import Path

import pytest
from pydantic import TypeAdapter
from ruamel.yaml import YAML

from literalizer.languages import ALL_LANGUAGES
from tests.yaml_support import as_yaml_parser

_ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(name="native_filters")
def fixture_native_filters() -> dict[str, list[str]]:
    """Load the declarative policy consumed by paths-filter."""
    parser = as_yaml_parser(parser=YAML())
    return TypeAdapter(type=dict[str, list[str]]).validate_python(
        parser.load(stream=_ROOT / ".github/native-filters.yml"),
    )


@pytest.fixture(name="lint_jobs")
def fixture_lint_jobs() -> dict[str, str]:
    """Retain shell fixture commands in top-level workflow job blocks."""
    return dict(
        re.findall(
            pattern=r"^  ([\w-]+):\n(.*?)(?=^  [\w-]+:|\Z)",
            string=(_ROOT / ".github/workflows/lint.yml").read_text(
                encoding="utf-8",
            ),
            flags=re.MULTILINE | re.DOTALL,
        ),
    )


def _extensions(*, pattern: str) -> set[str]:
    """Read the extension group declared by a fixture glob."""
    assert pattern.startswith("tests/integration/cases/*/*@*.")
    return {
        f".{suffix}"
        for suffix in pattern.rsplit(sep=".", maxsplit=1)[1]
        .strip("{}")
        .split(sep=",")
    }


def test_selection_covers_workflow_commands(
    native_filters: dict[str, list[str]], lint_jobs: dict[str, str]
) -> None:
    """Every native job and consumed extension has a matching filter."""
    native_jobs = {
        job
        for job in lint_jobs
        if job.startswith("lint-") or job == "build-cpp-toolchain"
    }
    assert native_jobs == native_filters.keys() - {"full"}
    known_extensions: set[str] = set()
    for job_id in native_jobs:
        extensions = _extensions(pattern=native_filters[job_id][0])
        known_extensions.update(extensions)
        job = lint_jobs[job_id]
        assert (
            re.search(
                pattern=r"^    needs: \[.*\bnative-changes\b.*\]$",
                string=job,
                flags=re.MULTILINE,
            )
            is not None
        )
        assert "needs.native-changes.outputs.all == 'true'" in job
        assert (
            "contains(fromJSON(needs.native-changes.outputs.jobs), "
            f"'{job_id}')"
        ) in job
        referenced = set(
            re.findall(pattern=r"-name '[^']*?(\.[\w]+)'", string=job),
        )
        referenced.update(
            re.findall(pattern=r"list_fixtures (\.[\w]+)", string=job),
        )
        assert referenced <= extensions, job_id
    (goldens,) = [
        pattern
        for pattern in native_filters["full"]
        if pattern.startswith("!tests/integration/cases/")
    ]
    assert goldens == (
        "!tests/integration/cases/*/*@*.{"
        + ",".join(sorted(extension[1:] for extension in known_extensions))
        + "}"
    )
    assert "      - native-changes\n" in lint_jobs["completion-lint"]


def test_backend_and_helper_ownership(
    native_filters: dict[str, list[str]], lint_jobs: dict[str, str]
) -> None:
    """Backend metadata and native commands determine path ownership."""
    owned_paths: set[str] = set()
    for job, patterns in native_filters.items():
        if job == "full":
            continue
        extensions = _extensions(pattern=patterns[0])
        sources = {
            f"src/{language.__module__.replace('.', '/')}.py"
            for language in ALL_LANGUAGES
            if language.extension in extensions
        }
        helpers = {
            f"scripts/{name}.py"
            for name in re.findall(
                pattern=r"\bpython\s+-m\s+scripts\.([\w]+)",
                string=lint_jobs[job],
            )
        } | set(
            re.findall(
                pattern=r"\b(?:bash\s+)?(scripts/[\w-]+\.sh)",
                string=lint_jobs[job],
            ),
        )
        # Generic shell wrappers deliberately retain the full-suite fallback.
        helpers -= {"scripts/retry.sh", "scripts/run-bounded.sh"}
        assert set(patterns[1:]) == sources | helpers, job
        owned_paths.update(patterns[1:])
    # New or shared paths must not silently become eligible for filtering.
    assert {
        pattern[1:]
        for pattern in native_filters["full"]
        if pattern.startswith(("!src/", "!scripts/"))
    } == owned_paths


def test_backend_modules_are_independent() -> None:
    """A backend must not import another backend behind its filter."""
    for language in ALL_LANGUAGES:
        path = _ROOT / f"src/{language.__module__.replace('.', '/')}.py"
        for node in ast.walk(node=ast.parse(source=path.read_text())):
            if isinstance(node, ast.ImportFrom):
                assert node.level == 0, path
                assert node.module is not None, path
                assert not node.module.startswith("literalizer.languages"), (
                    path
                )
                assert not (
                    node.module == "literalizer"
                    and any(alias.name == "languages" for alias in node.names)
                ), path
            elif isinstance(node, ast.Import):
                assert all(
                    not alias.name.startswith("literalizer.languages")
                    for alias in node.names
                ), path


def test_native_helper_dependencies_preserve_consumers(
    native_filters: dict[str, list[str]],
) -> None:
    """Changing an imported helper also selects its importing jobs."""
    owners: defaultdict[str, set[str]] = defaultdict(set[str])
    for job, patterns in native_filters.items():
        if job != "full":
            for owned_path in patterns[1:]:
                owners[owned_path].add(job)
    for path in (_ROOT / "scripts").glob(pattern="*.py"):
        tree = ast.parse(source=path.read_text())
        for module in _script_imports(tree=tree):
            dependency = module.replace(".", "/") + ".py"
            if dependency in owners:
                importer = path.as_posix().removeprefix(f"{_ROOT.as_posix()}/")
                assert importer in owners, (importer, dependency)
                assert owners[importer] <= owners[dependency], (
                    importer,
                    dependency,
                )


def _script_imports(*, tree: ast.AST) -> set[str]:
    """Read explicit imports of native helper modules."""
    modules: set[str] = set()
    for node in ast.walk(node=tree):
        if isinstance(node, ast.ImportFrom):
            if node.module == "scripts":
                modules.update(f"scripts.{alias.name}" for alias in node.names)
            elif node.module is not None and node.module.startswith(
                "scripts."
            ):
                modules.add(node.module)
        elif isinstance(node, ast.Import):
            modules.update(
                alias.name
                for alias in node.names
                if alias.name.startswith("scripts.")
            )
    return modules


def test_native_code_does_not_import_ignored_tests() -> None:
    """Test-only directories cannot become hidden native inputs."""
    ignored = (
        "tests.benchmarks",
        "tests.errors",
        "tests.metadata",
        "tests.runtime",
        "tests.unit_cases",
    )
    for directory in ("src", "scripts", "tests/integration"):
        for path in (_ROOT / directory).rglob(pattern="*.py"):
            if "cases" in path.parts:
                continue
            for node in ast.walk(node=ast.parse(source=path.read_text())):
                if isinstance(node, ast.ImportFrom):
                    assert node.module is None or not node.module.startswith(
                        ignored
                    ), path
                    assert all(
                        f"{node.module}.{alias.name}" not in ignored
                        for alias in node.names
                    ), path
                elif isinstance(node, ast.Import):
                    assert all(
                        not alias.name.startswith(ignored)
                        for alias in node.names
                    ), path
