"""Check repository-specific native CI filters against their consumers."""

import re
from pathlib import Path

from pydantic import TypeAdapter
from ruamel.yaml import YAML

from tests.yaml_support import as_yaml_parser


def test_selection_covers_workflow_commands() -> None:
    """Every native job and consumed extension has a matching filter."""
    root = Path(__file__).resolve().parents[2]
    parser = as_yaml_parser(parser=YAML())
    filters = TypeAdapter(type=dict[str, list[str]]).validate_python(
        parser.load(stream=root / ".github/native-filters.yml"),
    )
    # Retain shell fixture commands when inspecting top-level job blocks.
    jobs = dict(
        re.findall(
            pattern=r"^  ([\w-]+):\n(.*?)(?=^  [\w-]+:|\Z)",
            string=(root / ".github/workflows/lint.yml").read_text(
                encoding="utf-8",
            ),
            flags=re.MULTILINE | re.DOTALL,
        )
    )
    native_jobs = {
        job
        for job in jobs
        if job.startswith("lint-") or job == "build-cpp-toolchain"
    }
    assert native_jobs == filters.keys() - {"full"}
    known_extensions: set[str] = set()
    for job_id in native_jobs:
        (pattern,) = filters[job_id]
        assert pattern.startswith("tests/integration/cases/*/*@*.")
        extensions = {
            f".{suffix}"
            for suffix in pattern.rsplit(sep=".", maxsplit=1)[1]
            .strip("{}")
            .split(sep=",")
        }
        known_extensions.update(extensions)
        job = jobs[job_id]
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
    # An extension added to any job must also be safe to filter globally.
    (goldens,) = [
        pattern
        for pattern in filters["full"]
        if pattern.startswith("!tests/integration/cases/")
    ]
    assert goldens == (
        "!tests/integration/cases/*/*@*.{"
        + ",".join(sorted(extension[1:] for extension in known_extensions))
        + "}"
    )
    assert "      - native-changes\n" in jobs["completion-lint"]
