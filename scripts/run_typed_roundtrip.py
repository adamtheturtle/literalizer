"""Execute capability-selected golden values through a typed oracle."""

import base64
import dataclasses
import datetime as dt
import json
import os.path
import shutil
import sys
import tomllib
from pathlib import Path
from typing import Literal

import click
from pydantic import BaseModel, Field, JsonValue, TypeAdapter
from ruamel.yaml import YAML

from scripts.bounded_command import bounded_command
from scripts.native_observation import (
    is_native_mapping,
    is_native_sequence,
    observe,
    verify_observation,
)
from scripts.roundtrip_common import (
    Step,
    json_object_from_text,
    run_program,
)
from tests.native_value_sources import RefValueSource
from tests.yaml_support import as_yaml_parser

_ROOT = Path(__file__).resolve().parent.parent
_CASES = _ROOT / "tests/integration/cases"
type Capability = Literal[
    "values", "native-bytes", "records", "iso-datetime", "fractional-offsets"
]


# Defaults describe omitted keys in the authored corpus contract.
class CaseGroup(BaseModel, extra="forbid", frozen=True):  # noqa: NOD001
    """One capability's inputs, fixtures and representation contract."""

    capability: Capability
    cases: tuple[str, ...]
    stems: tuple[str, ...]
    bytes_format: Literal["native", "hex", "base64"] = "hex"
    datetime_format: Literal["native", "epoch", "iso"] = "native"


class Corpus(BaseModel, extra="forbid", frozen=True):
    """The small fixed deterministic corpus declaration."""

    groups: tuple[CaseGroup, ...] = Field(min_length=1)


@dataclasses.dataclass(frozen=True, kw_only=True)
class Backend:
    """Inspector capabilities and public representation conventions."""

    name: str
    extension: str
    capabilities: frozenset[Capability]
    naive_is_utc: bool


BACKENDS = {
    "python": Backend(
        name="Python",
        extension="py",
        capabilities=frozenset({"values", "native-bytes", "records"}),
        naive_is_utc=False,
    ),
    "ruby": Backend(
        name="Ruby",
        extension="rb",
        capabilities=frozenset(
            {"values", "iso-datetime", "fractional-offsets"}
        ),
        naive_is_utc=True,
    ),
}


# Each explicit public conversion returns its selected representation.
def _project(  # noqa: PLR0911
    *, value: object, group: CaseGroup, backend: Backend
) -> object:
    """Apply only the selected documented representation conversions."""
    if isinstance(value, bytes):
        if group.bytes_format == "hex":
            return value.hex()
        if group.bytes_format == "base64":
            return base64.b64encode(s=value).decode(encoding="ascii")
        return value
    if isinstance(value, dt.datetime):
        if group.datetime_format == "iso":
            return value.isoformat()
        if group.datetime_format == "epoch":
            aware = (
                value
                if value.tzinfo is not None
                else value.replace(tzinfo=dt.UTC)
            )
            epoch = dt.datetime(year=1970, month=1, day=1, tzinfo=dt.UTC)
            microseconds = (aware - epoch) // dt.timedelta(microseconds=1)
            return (
                microseconds // 1_000_000
                if microseconds % 1_000_000 == 0
                else microseconds / 1_000_000
            )
        if backend.naive_is_utc and value.tzinfo is None:
            return value.replace(tzinfo=dt.UTC)
        return value
    if is_native_mapping(value):
        return {
            _project(value=key, group=group, backend=backend): _project(
                value=item, group=group, backend=backend
            )
            for key, item in value.items()
        }
    if is_native_sequence(value):
        return [
            _project(value=item, group=group, backend=backend)
            for item in value
        ]
    return value


def _input(*, case_dir: Path) -> object:
    """Decode authored input independently of Literalizer's
    parser/renderer.
    """
    inputs = [
        path
        for path in case_dir.glob(pattern="input.*")
        if path.suffix in {".json", ".yaml", ".toml"}
    ]
    if len(inputs) != 1:
        msg = f"{case_dir.name}: expected one JSON/YAML/TOML input"
        raise ValueError(msg)
    path = inputs[0]
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".json":
        value: object = json.loads(s=text)
    elif path.suffix == ".toml":
        value = tomllib.loads(text)
    else:
        value = as_yaml_parser(parser=YAML(typ="safe")).load(stream=text)
    # Native datetime offsets are authored in TOML, not rendered expectations.
    manifest = tomllib.loads(
        (case_dir / "case.toml").read_text(encoding="utf-8")
    )
    substitutions = TypeAdapter[dict[str, RefValueSource]](
        type=dict[str, RefValueSource]
    ).validate_python(
        manifest.get("base_context", {}).get("record_null_value_sources", {})
    )
    if len(substitutions) > 0:
        if not is_native_mapping(value):
            msg = f"{case_dir.name}: substitutions require a mapping input"
            raise ValueError(msg)
        mapping = dict(value)
        for key, source in substitutions.items():
            if key not in mapping or mapping[key] is not None:
                msg = (
                    f"{case_dir.name}: substitution {key!r} must replace null"
                )
                raise ValueError(msg)
            mapping[key] = source.to_value()
        return mapping
    return value


def selected_cases(*, backend: Backend) -> dict[Path, JsonValue]:
    """Discover supported versions; missing fixtures fail closed."""
    corpus = Corpus.model_validate(
        obj=tomllib.loads(
            Path(__file__)
            .with_name(name="typed_roundtrip_cases.toml")
            .read_text(encoding="utf-8")
        )
    )
    selected: dict[Path, JsonValue] = {}
    for group in corpus.groups:
        if group.capability not in backend.capabilities:
            continue
        for name in group.cases:
            case_dir = _CASES / name
            want = observe(
                value=_project(
                    value=_input(case_dir=case_dir),
                    group=group,
                    backend=backend,
                )
            )
            for stem in group.stems:
                pattern = (
                    f"{stem.format(backend=backend.name)}"
                    f"@*.{backend.extension}"
                )
                paths = sorted(case_dir.glob(pattern=pattern))
                if len(paths) == 0:
                    msg = f"{backend.name}/{name}: no fixtures match {pattern}"
                    raise ValueError(msg)
                for path in paths:
                    if path in selected:
                        msg = f"duplicate typed case: {path}"
                        raise ValueError(msg)
                    selected[path] = want
    return selected


def _label(*, path: Path, root: Path) -> str:
    """Use stable relative fixture labels on each supported
    Python/platform.
    """
    return Path(os.path.relpath(path=path, start=root)).as_posix()


def build_program(
    *, backend: Backend, fixtures: tuple[Path, ...], cases_dir: Path
) -> str:
    """Append independent inspection to the actual golden files."""
    if backend.name == "Python":
        return (
            "import json, runpy, sys\n"
            f"sys.path.insert(0, {str(object=_ROOT)!r})\n"
            "from scripts.native_observation import observe\n"
            "actual = {}\n"
            "def inspect_fixture(path, label):\n"
            "    try:\n"
            "        return observe(value=runpy.run_path(path)['my_data'])\n"
            "    except Exception as exc:\n"
            "        raise RuntimeError(label) from exc\n"
            + "".join(
                f"label = {_label(path=path, root=cases_dir)!r}\n"
                "actual[label] = inspect_fixture("
                f"{str(object=path)!r}, label)\n"
                for path in fixtures
            )
            + "print(json.dumps(actual, allow_nan=False))\n"
        )
    inspector = (
        Path(__file__)
        .with_name(name="native_observer.rb")
        .read_text(encoding="utf-8")
    )
    return (
        inspector
        + "\nactual = {}\n"
        + "".join(
            "label = "
            f"{json.dumps(obj=_label(path=path, root=cases_dir))}\n"
            "actual[label] = -> {\nbegin\n"
            f"{path.read_text(encoding='utf-8')}\n"
            "observe_native(my_data)\nrescue StandardError => e\n"
            'warn "#{label}: #{e}"\nraise\nend\n}.call\n'
            for path in fixtures
        )
        + "STDOUT.write(JSON.generate(actual))\n"
    )


@dataclasses.dataclass(frozen=True, kw_only=True)
class CoverageReport:
    """Observed fixtures and this runner's explicit coverage gap."""

    observed: list[str]
    snapshot_compile_only: list[str]


def check_backend(*, backend: Backend) -> CoverageReport:
    """Run bounded native execution and report the remaining coverage
    gap.
    """
    selected = selected_cases(backend=backend)
    executable = (
        sys.executable
        if backend.name == "Python"
        else shutil.which(cmd="ruby")
    )
    if executable is None or executable == "":
        msg = f"{backend.name}: required runtime is unavailable"
        raise ValueError(msg)
    filename = f"typed.{backend.extension}"
    output = run_program(
        label=f"{backend.name} typed goldens",
        source_filename=filename,
        program=build_program(
            backend=backend, fixtures=tuple(selected), cases_dir=_CASES
        ),
        steps=[
            Step(
                args=bounded_command(
                    args=[executable, filename],
                    fixture=f"{backend.name} typed goldens",
                    timeout_seconds=60,
                ),
                failure_label="native inspector failed",
            )
        ],
        extra_files=None,
    )
    actual = json_object_from_text(text=output)
    labels = {_label(path=path, root=_CASES) for path in selected}
    if actual.keys() != labels:
        msg = (
            f"{backend.name}: missing/unexpected case observations: "
            f"{labels ^ actual.keys()}"
        )
        raise ValueError(msg)
    for path, expected in selected.items():
        label = _label(path=path, root=_CASES)
        verify_observation(
            label=label, actual=actual[label], expected=expected
        )
    remaining = sorted(
        _label(path=path, root=_CASES)
        for path in _CASES.glob(
            pattern=f"*/{backend.name}*.{backend.extension}"
        )
        if path not in selected
    )
    return CoverageReport(
        observed=sorted(labels), snapshot_compile_only=remaining
    )


@click.command()
@click.option(
    "--backend",
    "backend_name",
    type=click.Choice(choices=tuple(BACKENDS)),
    required=True,
)
@click.option("--report", type=click.Path(path_type=Path), default=None)
def main(*, backend_name: str, report: Path | None) -> None:
    """Verify typed groups and optionally write all coverage labels."""
    try:
        result = check_backend(backend=BACKENDS[backend_name])
    except ValueError as exc:
        raise click.ClickException(message=str(object=exc)) from exc
    if report is not None:
        _ = report.write_text(
            data=json.dumps(obj=dataclasses.asdict(obj=result), indent=2)
            + "\n",
            encoding="utf-8",
        )
    click.echo(
        message=(
            f"{backend_name}: {len(result.observed)} typed observations OK;"
            " "
            f"{len(result.snapshot_compile_only)} fixtures receive only "
            "snapshot/compile checks from this runner "
            "(use --report for labels)"
        )
    )


if __name__ == "__main__":
    main()
