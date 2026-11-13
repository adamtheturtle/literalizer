"""Analyze Dart golden files and force their declared lazy bindings."""

import shutil
import subprocess
import sys
import tempfile
from collections.abc import Sequence
from pathlib import Path

from beartype import beartype

from literalizer import VariableForm
from literalizer.languages import Dart
from tests.integration.call_collection import (
    discover_call_cases,
)
from tests.integration.call_variant_cases import build_call_variant_cases
from tests.integration.case_manifests import RefCaseSpec
from tests.integration.constructor_cases import (
    constructor_binding_cases,
)
from tests.integration.golden_scenarios import golden_groups
from tests.integration.language_specs import make_golden_path
from tests.integration.reference_cases import reference_golden_cases

_CASES_DIR = Path(__file__).parent.parent / "tests" / "integration" / "cases"


@beartype
def _binding_name(*, variable_form: VariableForm | None) -> str:
    """Use the declared name or Dart's nameless-wrapper sentinel."""
    return "my_data" if variable_form is None else variable_form.name


@beartype
def _literalize_bindings() -> dict[Path, str | None]:
    """Read roots, using None for native programs with a main function."""
    return {
        rendering.golden_path(version=spec.language_version).resolve(): (
            None
            if rendering.consumer_template is not None
            else _binding_name(variable_form=rendering.render.variable_form)
        )
        for group in golden_groups()
        for rendering in group.renderings
        if rendering.lang_cls is Dart
        for spec in rendering.specs
    }


@beartype
def _call_bindings() -> dict[Path, str]:
    """Read call roots, including the nameless-wrapper sentinel."""
    bindings: dict[Path, str] = {}
    for call_case in discover_call_cases():
        if (
            call_case.lang_cls is not Dart
            or call_case.expected_exception is not None
        ):
            continue
        for version in Dart.VersionFormats:
            golden = make_golden_path(
                parent=_CASES_DIR / call_case.config.case_dir_name,
                name=call_case.config.golden_name(name="Dart_call"),
                lang_cls=Dart,
                version=version,
            )
            bindings[golden.resolve()] = _binding_name(
                variable_form=call_case.config.variable_form
            )
    for variant_case in build_call_variant_cases(cases_dir=_CASES_DIR):
        if variant_case.variant.lang_cls is not Dart:
            continue
        golden = make_golden_path(
            parent=_CASES_DIR / variant_case.config.case_dir_name,
            name=variant_case.config.golden_name(
                name=f"{variant_case.variant.name}_call"
            ),
            lang_cls=Dart,
            version=variant_case.variant.spec.language_version,
        )
        bindings[golden.resolve()] = _binding_name(
            variable_form=variant_case.config.variable_form
        )
    return bindings


@beartype
def _ref_binding_name(*, config: RefCaseSpec) -> str | None:
    """Run composed reference programs, otherwise read their root
    binding.
    """
    if config.consumer is not None or len(config.external_declarations) > 0:
        return None
    return _binding_name(variable_form=config.resolved_variable_form())


@beartype
def _ref_bindings() -> dict[Path, str | None]:
    """Read roots or native entry points from the reference renderings."""
    return {
        rendering.golden_path(
            cases_dir=_CASES_DIR
        ).resolve(): _ref_binding_name(config=rendering.config)
        for case in reference_golden_cases()
        if case.lang_cls is Dart
        for rendering in case.renderings
    }


@beartype
def _constructor_bindings() -> dict[Path, str]:
    """Read constructor roots from their owning manifest metadata."""
    bindings: dict[Path, str] = {}
    for case in constructor_binding_cases(cases_dir=_CASES_DIR):
        if case.lang_cls is not Dart:
            continue
        config = case.manifest.constructor
        if config is None:
            msg = f"Missing constructor metadata for {case.name}."
            raise ValueError(msg)
        for rendering in case.renderings:
            bindings[rendering.golden_path.resolve()] = config.variable_name
    return bindings


@beartype
def dart_fixture_bindings() -> dict[Path, str | None]:
    """Read bindings from the same registries that own golden files."""
    return (
        _literalize_bindings()
        | _call_bindings()
        | _ref_bindings()
        | _constructor_bindings()
    )


@beartype
def _fresh_getter_name(*, source: str) -> str:
    """Choose an accessor name absent from the complete fixture text."""
    name = "fixtureRoot"
    suffix = 0
    while name in source:
        suffix += 1
        name = f"fixtureRoot{suffix}"
    return name


@beartype
def write_dart_driver(*, fixtures: Sequence[Path], target: Path) -> None:
    """Copy fixtures and invoke native programs or read top-level
    roots.
    """
    bindings = dart_fixture_bindings()
    imports: list[str] = []
    roots: list[str] = []
    entrypoints: list[str] = []
    for index, fixture in enumerate(iterable=fixtures):
        try:
            binding = bindings[fixture.resolve()]
        except KeyError as exc:
            msg = f"Dart fixture has no golden metadata: {fixture}"
            raise ValueError(msg) from exc
        copied_name = f"fixture_{index}.dart"
        source = fixture.read_bytes()
        accessor = ""
        if binding is None:
            entrypoints.append(f"  f{index}.main();")
        else:
            getter = _fresh_getter_name(source=source.decode(encoding="utf-8"))
            accessor = f"\nget {getter} => {binding};\n"
            roots.append(f"    f{index}.{getter},")
        _ = (target / copied_name).write_bytes(
            data=source + accessor.encode(encoding="utf-8")
        )
        imports.append(f'import "{copied_name}" as f{index};')
        _ = sys.stdout.write(f"{copied_name} <- {fixture}\n")
    _ = sys.stdout.flush()
    # The lower version bound selects the declared Dart language grammar.
    _ = (target / "pubspec.yaml").write_text(
        data="name: check\nenvironment:\n  sdk: ^3.0.0\n",
        encoding="utf-8",
    )
    _ = (target / "main.dart").write_text(
        data="\n".join(
            [
                *imports,
                "void main() {",
                *entrypoints,
                "  final sink = <Object?>[",
                *roots,
                "  ];",
                (
                    "  if (sink.length != "
                    f"{len(roots)}) throw StateError('unreachable');"
                ),
                "}",
                "",
            ]
        ),
        encoding="utf-8",
    )


@beartype
def main() -> None:
    """Consume null-separated paths, then analyze and run the driver."""
    fixtures = [
        Path(filename.decode(encoding="utf-8"))
        for filename in sys.stdin.buffer.read().split(sep=b"\0")
        if len(filename) > 0
    ]
    if len(fixtures) == 0:
        msg = "No Dart fixture paths were provided."
        raise ValueError(msg)
    dart = shutil.which(cmd="dart")
    if dart is None:
        msg = "Dart executable was not found."
        raise RuntimeError(msg)
    with tempfile.TemporaryDirectory(suffix="-literalizer-dart") as directory:
        target = Path(directory)
        write_dart_driver(fixtures=fixtures, target=target)
        _ = subprocess.run(
            args=[dart, "analyze", "--fatal-infos", str(object=target)],
            check=True,
        )
        _ = subprocess.run(
            args=[dart, "run", "main.dart"], cwd=target, check=True
        )


if __name__ == "__main__":
    main()
