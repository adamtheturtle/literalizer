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
* ``test_json_large_flat_records`` — large flat JSON record array,
  exercising repeated dict/list/scalar rendering and large output
  generation.
* ``test_heterogeneous_widening`` — sibling dicts and lists with
  diverging inferred types, exercising the sequence/dict opener
  widening logic.
* ``test_json_large_flat_records_json_native`` — the same flat record
  array rendered by every language that opts into the shared
  JSON-native whole-document fast path, one benchmark per language.
"""

import json

import pytest
from pytest_codspeed import BenchmarkFixture

from literalizer import InputFormat, Language, literalize
from literalizer.languages import (
    C,
    Cpp,
    Crystal,
    Elm,
    Erlang,
    Gleam,
    Haskell,
    Kotlin,
    OCaml,
    Odin,
    PureScript,
    Python,
    Rust,
    Scala,
    Zig,
)

PYTHON = Python(
    date_format=Python.date_formats.PYTHON,
    datetime_format=Python.datetime_formats.PYTHON,
    bytes_format=Python.bytes_formats.HEX,
    sequence_format=Python.sequence_formats.TUPLE,
    set_format=Python.set_formats.SET,
    variable_type_hints=Python.variable_type_hints_formats.NEVER,
)
RUST_JSON_VALUE = Rust(json_type=Rust.json_types.SERDE_JSON_VALUE)

# Every language registered on the shared JSON-native fast path, each
# with the ``json_type`` mode that qualifies for it.  Keep in sync with
# the ``register_json_native_document_fast`` calls in
# :mod:`literalizer.languages`.
JSON_NATIVE_LANGUAGES: dict[str, Language] = {
    "C": C(json_type=C.json_types.CJSON),
    "Cpp": Cpp(json_type=Cpp.json_types.NLOHMANN_JSON),
    "Crystal": Crystal(json_type=Crystal.json_types.JSON_ANY),
    "Elm": Elm(json_type=Elm.json_types.JSON_ENCODE_VALUE),
    "Erlang": Erlang(json_type=Erlang.json_types.OTP_JSON),
    "Gleam": Gleam(json_type=Gleam.json_types.GLEAM_JSON_JSON),
    "Haskell": Haskell(json_type=Haskell.json_types.AESON_VALUE),
    "Kotlin": Kotlin(json_type=Kotlin.json_types.KOTLINX_JSON_ELEMENT),
    "OCaml": OCaml(json_type=OCaml.json_types.YOJSON_SAFE_T),
    "Odin": Odin(json_type=Odin.json_types.JSON_VALUE),
    "PureScript": PureScript(json_type=PureScript.json_types.ARGONAUT_JSON),
    "Rust": RUST_JSON_VALUE,
    "Scala": Scala(json_type=Scala.json_types.CIRCE),
    "Zig": Zig(json_type=Zig.json_types.STD_JSON_VALUE),
}


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


def _build_json_flat_records_source(*, n_records: int) -> str:
    """Return a large flat JSON array of repeated record-shaped dicts."""
    return json.dumps(
        obj=[
            {
                "id": i,
                "name": f"user_{i}",
                "active": i % 2 == 0,
                "score": i * 1.25,
                "tags": [f"tag_{i % 10}", f"group_{i % 25}"],
                "metrics": {
                    "views": i * 3,
                    "clicks": i % 17,
                    "ratio": (i % 100) / 100,
                },
            }
            for i in range(n_records)
        ],
    )


_YAML_FAST = _build_yaml_source(n_records=100, with_comments=False)
_YAML_WITH_COMMENTS = _build_yaml_source(n_records=100, with_comments=True)
_JSON_NESTED = _build_json_source(depth=4, fanout=4)
_JSON_LARGE_FLAT_RECORDS = _build_json_flat_records_source(n_records=1_000)
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


def _run_json_native(*, source: str, language: Language) -> str:
    """Literalize JSON to *language*'s dynamic JSON node type."""
    return literalize(
        source=source,
        input_format=InputFormat.JSON,
        language=language,
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


def test_json_large_flat_records(benchmark: BenchmarkFixture) -> None:
    """Flat JSON record array exercising high-volume rendering."""
    benchmark(
        _run,
        source=_JSON_LARGE_FLAT_RECORDS,
        input_format=InputFormat.JSON,
    )


@pytest.mark.parametrize(
    argnames="language",
    argvalues=JSON_NATIVE_LANGUAGES.values(),
    ids=JSON_NATIVE_LANGUAGES.keys(),
)
def test_json_large_flat_records_json_native(
    benchmark: BenchmarkFixture,
    language: Language,
) -> None:
    """Large JSON record array through the JSON-native fast path."""
    benchmark(
        _run_json_native,
        source=_JSON_LARGE_FLAT_RECORDS,
        language=language,
    )


def test_heterogeneous_widening(benchmark: BenchmarkFixture) -> None:
    """Sibling collections with diverging inferred types."""
    benchmark(
        _run,
        source=_JSON_HETEROGENEOUS,
        input_format=InputFormat.JSON,
    )
