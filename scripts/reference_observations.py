"""Compare native reference observations with authored fixture values."""

import json
import subprocess
from pathlib import Path

import click

from scripts.bounded_command import bounded_command, run_bounded_command
from tests.integration.case_manifests import (
    ExternalRefContext,
    RefValueCheckSpec,
    load_case_manifest,
)


def _expected_observations(*, fixture: Path) -> tuple[str, ...] | None:
    """Read the initial and final expectations in execution order."""
    stem, _, _ = fixture.stem.partition("@")
    if not stem.endswith("_ref_default"):
        return None
    case = load_case_manifest(case_dir=fixture.parent)
    if case.ref is None or not isinstance(
        case.ref.context, ExternalRefContext
    ):
        return None
    context = case.ref.context
    if not isinstance(context.consumer, RefValueCheckSpec):
        return None
    initial = context.declarations.get("my_data")
    if initial is None:
        return (context.consumer.expected_source,)
    return (initial, context.consumer.expected_source)


def _canonical_json(*, source: str) -> str:
    """Compare JSON structure while keeping booleans distinct from numbers."""
    return json.dumps(obj=json.loads(s=source), sort_keys=True)


def run_reference_fixture(
    *, fixture: Path, executable: Path, timeout_seconds: float
) -> None:
    """Run a native fixture and compare its JSON lines when requested."""
    expected = _expected_observations(fixture=fixture)
    label = f"Reference execution: {fixture}"
    if expected is None:
        run_bounded_command(
            args=[executable],
            fixture=label,
            timeout_seconds=timeout_seconds,
            cwd=None,
        )
        return
    run = subprocess.run(
        args=bounded_command(
            args=[executable], fixture=label, timeout_seconds=timeout_seconds
        ),
        check=False,
        capture_output=True,
        encoding="utf-8",
    )
    if run.returncode != 0:
        msg = f"{label} exited {run.returncode}\n{run.stdout}{run.stderr}"
        raise click.ClickException(message=msg)
    try:
        actual = tuple(
            _canonical_json(source=line) for line in run.stdout.splitlines()
        )
        wanted = tuple(_canonical_json(source=line) for line in expected)
    except ValueError as exc:
        msg = f"{label}: invalid observation JSON ({exc})\n{run.stdout!r}"
        raise click.ClickException(message=msg) from exc
    if actual != wanted:
        msg = (
            f"{label}: observation mismatch\n"
            f"  expected: {wanted!r}\n"
            f"  got:      {actual!r}"
        )
        raise click.ClickException(message=msg)


@click.command()
@click.argument("fixture", type=click.Path(path_type=Path, exists=True))
@click.argument("executable", type=click.Path(path_type=Path, exists=True))
def main(*, fixture: Path, executable: Path) -> None:
    """Run the compiled fixture and check its reference observations."""
    run_reference_fixture(
        fixture=fixture, executable=executable, timeout_seconds=60.0
    )


if __name__ == "__main__":
    main()
