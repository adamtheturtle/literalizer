"""Keep CI filtering conservative as test support evolves."""

import ast
import os
from pathlib import Path

import pytest
from pydantic import TypeAdapter
from ruamel.yaml import YAML

from tests.yaml_support import as_yaml_parser


@pytest.mark.parametrize(argnames="job", argvalues=["tests", "benchmarks"])
def test_ci_inputs_are_not_ignored(job: str) -> None:
    """Imported support cannot be hidden by a CI job's exclusions."""
    root = Path(__file__).resolve().parents[2]
    parser = as_yaml_parser(parser=YAML())
    filters = TypeAdapter(type=dict[str, list[str]]).validate_python(
        parser.load(stream=root / ".github/ci-filters.yml"),
    )
    ignored_directories = {
        pattern[1:-3]
        for pattern in filters[job]
        if pattern.startswith("!") and pattern.endswith("/**")
    }
    ignored_modules = tuple(
        directory.replace("/", ".") for directory in ignored_directories
    )
    for directory in ("src", "scripts", "tests"):
        for parent, directories, filenames in os.walk(top=root / directory):
            directories[:] = [
                name
                for name in directories
                if name not in {"cases", "default_module_names", "__pycache__"}
                and (Path(parent) / name)
                .as_posix()
                .removeprefix(f"{root.as_posix()}/")
                not in ignored_directories
            ]
            for name in filenames:
                if name.endswith(".py"):
                    path = Path(parent) / name
                    _check_imports(
                        tree=ast.parse(source=path.read_text()),
                        path=path,
                        ignored=ignored_modules,
                    )


def _check_imports(
    *, tree: ast.AST, path: Path, ignored: tuple[str, ...]
) -> None:
    """Reject explicit imports of excluded inputs."""
    for node in ast.walk(node=tree):
        if isinstance(node, ast.ImportFrom):
            assert node.module is None or not node.module.startswith(
                ignored
            ), path
            if node.module == "tests":
                assert all(
                    f"tests.{alias.name}" not in ignored
                    for alias in node.names
                ), path
        elif isinstance(node, ast.Import):
            assert all(
                not alias.name.startswith(ignored) for alias in node.names
            ), path
