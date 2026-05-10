"""Benchmarks for :func:`literalize` covering the main hot paths.

Each case exercises a distinct code path so regressions localize cleanly:

* ``test_yaml_fast_path`` — comment-free YAML parsed by the C-backed
  ``typ='safe', pure=False`` loader and formatted without the
  round-trip comment resolver.
* ``test_yaml_with_comments`` — YAML containing line comments, forcing
  the slower round-trip loader and the comment-resolution phase.
* ``test_json_nested`` — large nested JSON document, exercising the
  formatter recursion and language-spec dispatch without the YAML
  machinery.
* ``test_heterogeneous_widening`` — sibling dicts and lists with
  diverging inferred types, exercising the sequence/dict opener
  widening logic.
"""

import json

from pytest_codspeed import BenchmarkFixture

from literalizer import InputFormat, literalize
from literalizer.languages import Python

PYTHON = Python(
    date_format=Python.date_formats.PYTHON,
    datetime_format=Python.datetime_formats.PYTHON,
    bytes_format=Python.bytes_formats.HEX,
    sequence_format=Python.sequence_formats.TUPLE,
    set_format=Python.set_formats.SET,
    variable_type_hints=Python.variable_type_hints_formats.NEVER,
)


def _build_yaml_source(*, n_records: int, with_comments: bool) -> str:
    """Return a YAML document with *n_records* user entries."""
    lines: list[str] = []
    if with_comments:
        lines.append("# generated fixture")
    lines.append("users:")
    for i in range(n_records):
        lines.append(f"  - id: {i}")
        lines.append(f"    name: user_{i}")
        lines.append(f"    score: {i * 1.5}")
        lines.append(f"    active: {'true' if i % 2 == 0 else 'false'}")
        if with_comments:
            lines.append(f"    # record {i}")
    return "\n".join(lines) + "\n"


def _build_json_source(*, depth: int, fanout: int) -> str:
    """Return a JSON document nested to *depth* with ``fanout`` children
    per level.
    """

    def build(*, level: int) -> object:
        """Recursively construct a dict of the requested depth."""
        if level == 0:
            return {"id": level, "name": f"leaf_{level}", "value": 1.25}
        return {f"child_{i}": build(level=level - 1) for i in range(fanout)}

    return json.dumps(obj=build(level=depth))


_YAML_FAST = _build_yaml_source(n_records=100, with_comments=False)
_YAML_WITH_COMMENTS = _build_yaml_source(n_records=100, with_comments=True)
_JSON_NESTED = _build_json_source(depth=4, fanout=4)
_JSON_HETEROGENEOUS = json.dumps(
    obj={
        "rows": [
            {"x": 1, "y": "a", "tags": [1, 2, 3]},
            {"x": 2.5, "y": "b", "tags": ["a", "b"]},
            {"x": True, "y": "c", "tags": []},
        ]
        * 20,
    },
)


def _run(*, source: str, input_format: InputFormat) -> str:
    """Literalize *source* to Python and return the rendered code."""
    return literalize(
        source=source,
        input_format=input_format,
        language=PYTHON,
    ).code


def test_yaml_fast_path(benchmark: BenchmarkFixture) -> None:
    """Comment-free YAML through the C-backed safe loader."""
    benchmark(_run, source=_YAML_FAST, input_format=InputFormat.YAML)


def test_yaml_with_comments(benchmark: BenchmarkFixture) -> None:
    """YAML with comments, forcing the round-trip loader and resolver."""
    benchmark(
        _run,
        source=_YAML_WITH_COMMENTS,
        input_format=InputFormat.YAML,
    )


def test_json_nested(benchmark: BenchmarkFixture) -> None:
    """Deeply nested JSON exercising formatter recursion."""
    benchmark(_run, source=_JSON_NESTED, input_format=InputFormat.JSON)


def test_heterogeneous_widening(benchmark: BenchmarkFixture) -> None:
    """Sibling collections with diverging inferred types."""
    benchmark(
        _run,
        source=_JSON_HETEROGENEOUS,
        input_format=InputFormat.JSON,
    )
