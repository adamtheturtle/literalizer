"""Analyze Dart golden files and force their declared lazy bindings."""

import shutil
import subprocess
import sys
import tempfile
from collections.abc import Sequence
from pathlib import Path

from literalizer import VariableForm
from literalizer.languages import Dart
from tests.integration.call_cases import discover_call_cases
from tests.integration.call_variant_cases import build_call_variant_cases
from tests.integration.golden_scenarios import golden_groups
from tests.integration.language_specs import make_golden_path
from tests.integration.literalize_ref_cases import (
    discover_literalize_default_ref_cases,
    discover_literalize_ref_cases,
)

_CASES_DIR = Path(__file__).parent.parent / "tests" / "integration" / "cases"


def _binding_name(*, variable_form: VariableForm | None) -> str:
    """Use the declared name or Dart's nameless-wrapper sentinel."""
    return "my_data" if variable_form is None else variable_form.name


def _literalize_bindings() -> dict[Path, str]:
    """Read regular rendering bindings from the golden registry."""
    bindings: dict[Path, str] = {}
    for group in golden_groups():
        for rendering in group.renderings:
            if rendering.lang_cls is not Dart:
                continue
            for version in rendering.versions:
                spec = rendering.spec_for(version=version)
                if spec.language_version is not version:
                    continue
                golden = make_golden_path(
                    parent=rendering.golden_parent,
                    name=rendering.golden_name,
                    extension=spec.extension,
                    lang_cls=Dart,
                    version=version,
                )
                bindings[golden.resolve()] = _binding_name(
                    variable_form=rendering.render.variable_form
                )
    return bindings


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
                name="Dart_call",
                extension=Dart.extension,
                lang_cls=Dart,
                version=version,
            )
            bindings[golden.resolve()] = _binding_name(
                variable_form=call_case.config.variable_form
            )
    for variant_case in build_call_variant_cases():
        if variant_case.variant.lang_cls is not Dart:
            continue
        golden = make_golden_path(
            parent=_CASES_DIR / variant_case.config.case_dir_name,
            name=f"{variant_case.variant.name}_call",
            extension=Dart.extension,
            lang_cls=Dart,
            version=variant_case.variant.spec.language_version,
        )
        bindings[golden.resolve()] = _binding_name(
            variable_form=variant_case.config.variable_form
        )
    return bindings


def _ref_bindings() -> dict[Path, str]:
    """Read declared roots for explicit and default references."""
    bindings: dict[Path, str] = {}
    for cases, name in (
        (discover_literalize_ref_cases(), "Dart_ref"),
        (discover_literalize_default_ref_cases(), "Dart_ref_default"),
    ):
        for ref_case in cases:
            if ref_case.lang_cls is not Dart:
                continue
            for version in Dart.VersionFormats:
                golden = make_golden_path(
                    parent=_CASES_DIR / ref_case.config.case_dir_name,
                    name=name,
                    extension=Dart.extension,
                    lang_cls=Dart,
                    version=version,
                )
                bindings[golden.resolve()] = (
                    ref_case.config.resolved_variable_form().name
                )
    return bindings


def dart_fixture_bindings() -> dict[Path, str]:
    """Read bindings from the same registries that own golden files."""
    return _literalize_bindings() | _call_bindings() | _ref_bindings()


def _fresh_getter_name(*, source: str) -> str:
    """Choose an accessor name absent from the complete fixture text."""
    name = "literalizerFixtureRoot"
    suffix = 0
    while name in source:
        suffix += 1
        name = f"literalizerFixtureRoot{suffix}"
    return name


def write_dart_driver(*, fixtures: Sequence[Path], target: Path) -> None:
    """Copy owned fixtures and reference their actual top-level roots."""
    bindings = dart_fixture_bindings()
    imports: list[str] = []
    roots: list[str] = []
    for index, fixture in enumerate(iterable=fixtures):
        try:
            binding = bindings[fixture.resolve()]
        except KeyError as exc:
            msg = f"Dart fixture has no golden metadata: {fixture}"
            raise ValueError(msg) from exc
        copied_name = f"fixture_{index}.dart"
        source = fixture.read_bytes()
        getter = _fresh_getter_name(source=source.decode(encoding="utf-8"))
        accessor = f"\nget {getter} => {binding};\n"
        _ = (target / copied_name).write_bytes(
            data=source + accessor.encode(encoding="utf-8")
        )
        imports.append(f'import "{copied_name}" as f{index};')
        roots.append(f"    f{index}.{getter},")
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
                "  final sink = <Object?>[",
                *roots,
                "  ];",
                "  if (sink.isEmpty) throw StateError('unreachable');",
                "}",
                "",
            ]
        ),
        encoding="utf-8",
    )


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
