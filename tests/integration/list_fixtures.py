"""Print null-byte-terminated paths selected from the golden inventory."""

import functools
import sys
from pathlib import Path

import click

from .golden_artifacts import GoldenArtifact
from .golden_inventory import authored_paths, golden_artifacts

CASES_DIR: Path = Path("tests/integration/cases")


@functools.cache
def _artifacts_by_extension() -> dict[str, set[GoldenArtifact]]:
    """Index resolved artifacts once for callers selecting several
    versions.
    """
    by_extension: dict[str, set[GoldenArtifact]] = {}
    for artifact in golden_artifacts(cases_dir=CASES_DIR):
        by_extension.setdefault(artifact.language.extension, set()).add(
            artifact
        )
    return by_extension


def fixture_paths(
    *,
    extension: str | None,
    version: str | None = None,  # noqa: NOD001 - version pins are opt-in
    include_default_module_names: bool = False,  # noqa: NOD001 - job coverage
    language: str | None = None,  # noqa: NOD001 - disambiguate shared extensions
    include_authored: bool = False,  # noqa: NOD001 - parser coverage only
    case_name: str | None = None,  # noqa: NOD001 - optionally scope ownership
) -> tuple[Path, ...]:
    """Select existing golden files, optionally including authored inputs.

    Some renderings skip at runtime, so the ownership inventory can
    include paths that have no checked-in golden.
    """
    by_extension = _artifacts_by_extension()
    artifacts = (
        (artifact for group in by_extension.values() for artifact in group)
        if extension is None
        else iter(by_extension.get(extension, ()))
    )
    paths = {
        artifact.path
        for artifact in artifacts
        if (version is None or artifact.version.name.lower() == version)
        and (language is None or artifact.language.__name__ == language)
        and (case_name is None or artifact.case_name == case_name)
        and (
            case_name is not None
            or include_default_module_names
            or CASES_DIR in artifact.path.parents
        )
    }
    if include_authored:
        authored = authored_paths(cases_dir=CASES_DIR, case_name=case_name)
        paths.update(
            path
            for path in authored
            if path.suffix == extension
            or (extension is None and case_name is not None)
        )
    return tuple(sorted(path for path in paths if path.is_file()))


@click.command()
@click.argument("extension", required=False)
@click.argument("version", required=False)
@click.option("--include-default-module-names", is_flag=True)
@click.option("--language")
@click.option("--include-authored", is_flag=True)
@click.option(
    "--case",
    "case_name",
    help="Select by case name, including its default-module fixtures.",
)
def main(
    extension: str | None,
    version: str | None,
    *,
    include_default_module_names: bool,
    language: str | None,
    include_authored: bool,
    case_name: str | None,
) -> None:
    """Emit fixture paths by extension, language, version or case."""
    if extension is None and language is None and case_name is None:
        msg = "Provide an extension, --language or --case."
        raise click.UsageError(message=msg)
    paths = fixture_paths(
        extension=extension,
        version=version,
        include_default_module_names=include_default_module_names,
        language=language,
        include_authored=include_authored,
        case_name=case_name,
    )
    output = b"".join(f"{path}".encode() + b"\0" for path in paths)
    _ = sys.stdout.buffer.write(output)


if __name__ == "__main__":
    main()
