"""Typed observations and corruption controls for native golden files."""

import dataclasses
import os
import re
import sys
from pathlib import Path

import pytest
from pydantic import JsonValue

from literalizer.languages import Python, Ruby
from scripts.native_golden_observations import (
    CONSUMER_MARKER,
    check_golden_observation,
    expected_observation,
    run_golden_program,
)

from .case_manifests import load_case_manifest
from .language_specs import make_golden_path

_CASES = Path(__file__).parent / "cases"
_BACKENDS = {
    "python": (
        Python,
        (sys.executable, "-I"),
        r'^\s*File ".*", line (\d+), in ',
        r"^AssertionError(?::|$)",
    ),
    "ruby": (
        Ruby,
        ("ruby",),
        r"^.*?:(\d+):in .* \(RuntimeError\)$",
        r" \(RuntimeError\)$",
    ),
}
_RUBY_OPT_IN = pytest.mark.skipif(
    condition=os.environ.get(key="LITERALIZER_TEST_RUBY") != "1",
    reason="Set LITERALIZER_TEST_RUBY=1 with Ruby 3+ on PATH",
)


def _expected(*, fixture: Path) -> JsonValue:
    """Read the original input with its authored native substitutions."""
    manifest = load_case_manifest(case_dir=fixture.parent)
    return expected_observation(
        fixture=fixture,
        input_path=manifest.input.path,
        substitutions=manifest.base_context.resolved_record_null_substitutions(),
    )


def _observed_fixtures() -> list[pytest.ParameterSet]:
    """Select the capability groups with authored native consumers."""
    params: list[pytest.ParameterSet] = []
    for manifest in sorted(_CASES.glob(pattern="*/case.toml")):
        if CONSUMER_MARKER not in manifest.read_text(encoding="utf-8"):
            continue
        for fixture in sorted(manifest.parent.iterdir()):
            if fixture.suffix not in {".py", ".rb"}:
                continue
            if CONSUMER_MARKER not in fixture.read_text(encoding="utf-8"):
                continue
            backend = "python" if fixture.suffix == ".py" else "ruby"
            params.append(
                pytest.param(
                    backend,
                    fixture,
                    marks=() if backend == "python" else _RUBY_OPT_IN,
                    id=f"{fixture.parent.name}/{fixture.name}",
                )
            )
    return params


@pytest.mark.parametrize(
    argnames=("backend_name", "fixture"),
    argvalues=_observed_fixtures(),
)
def test_native_golden_observation(
    *, backend_name: str, fixture: Path, tmp_path: Path
) -> None:
    """Compare native values with the authored input and selected contract."""
    _, command, _, _ = _BACKENDS[backend_name]
    declaration, _ = fixture.read_text(encoding="utf-8").split(
        sep=CONSUMER_MARKER, maxsplit=1
    )
    check_golden_observation(
        fixture=fixture,
        declaration=declaration,
        command=command,
        expected=_expected(fixture=fixture),
        scratch=tmp_path,
    )


@dataclasses.dataclass(frozen=True, kw_only=True)
class Corruption:
    """A changed native literal, independent of the authored expected
    input.
    """

    case: str
    stem_suffix: str
    python: tuple[str, str]
    ruby: tuple[str, str]


_CORRUPTIONS = (
    Corruption(
        case="list_beyond_i64",
        stem_suffix="",
        python=("9223372036854775808", "9223372036854775809"),
        ruby=("9223372036854775808", "9223372036854775809"),
    ),
    Corruption(
        case="list_beyond_i64",
        stem_suffix="",
        python=("9223372036854775808", "9223372036854775808.0"),
        ruby=("9223372036854775808", "9223372036854775808.0"),
    ),
    Corruption(
        case="bool_list",
        stem_suffix="",
        python=("True", "1"),
        ruby=("true", "1"),
    ),
    Corruption(
        case="float_negative_zero",
        stem_suffix="",
        python=("-0.0", "0.0"),
        ruby=("-0.0", "0.0"),
    ),
    Corruption(
        case="scientific_float_precision",
        stem_suffix="_float_format_scientific_precision",
        python=("1.2345678901234567", "1.2345678901234565"),
        ruby=("1.2345678901234567", "1.2345678901234565"),
    ),
    Corruption(
        case="float_special_values",
        stem_suffix="",
        python=('float("nan")', 'float("inf")'),
        ruby=("Float::NAN", "Float::INFINITY"),
    ),
    Corruption(
        case="binary_octets",
        stem_suffix="",
        python=("00010203", "01010203"),
        ruby=("00010203", "01010203"),
    ),
    Corruption(
        case="int_key_dict",
        stem_suffix="",
        python=('1: "one"', '"1": "one"'),
        ruby=('1 => "one"', '"1" => "one"'),
    ),
    Corruption(
        case="date_list",
        stem_suffix="",
        python=("day=20", "day=21"),
        ruby=("2, 20,", "2, 21,"),
    ),
    Corruption(
        case="scalar_datetime_non_utc",
        stem_suffix="",
        python=("hour=18", "hour=17"),
        ruby=("15, 18,", "15, 17,"),
    ),
    Corruption(
        case="scalar_datetime_non_utc",
        stem_suffix="",
        python=("minutes=30", "minutes=0"),
        ruby=("+05:30", "+05:00"),
    ),
    Corruption(
        case="scalar_datetime_non_utc",
        stem_suffix="",
        python=(
            "hour=18, minute=0, second=0, tzinfo=datetime.timezone"
            "(offset=datetime.timedelta(hours=5, minutes=30))",
            "hour=17, minute=30, second=0, tzinfo=datetime.timezone"
            "(offset=datetime.timedelta(hours=5))",
        ),
        ruby=('18, 0, 0, "+05:30"', '17, 30, 0, "+05:00"'),
    ),
)


@pytest.mark.parametrize(
    argnames=("backend_name", "corruption"),
    argvalues=[("python", corruption) for corruption in _CORRUPTIONS]
    + [
        pytest.param("ruby", corruption, marks=_RUBY_OPT_IN)
        for corruption in _CORRUPTIONS
    ]
    + [
        (
            "python",
            Corruption(
                case="list_beyond_i64",
                stem_suffix="",
                python=(
                    "(\n    9223372036854775807,\n    9223372036854775808,\n)",
                    "{9223372036854775807: None, 9223372036854775808: None}",
                ),
                ruby=("", ""),
            ),
        ),
        (
            "python",
            Corruption(
                case="binary_nonempty_octets",
                stem_suffix="_bytes_format_python",
                python=(r"\x00", r"\x01"),
                ruby=("", ""),
            ),
        ),
        (
            "python",
            Corruption(
                case="binary_nonempty_octets",
                stem_suffix="_bytes_format_python",
                python=("b'", "'"),
                ruby=("", ""),
            ),
        ),
    ],
)
def test_native_value_corruptions(
    *,
    backend_name: str,
    corruption: Corruption,
    tmp_path: Path,
) -> None:
    """Corrupt generated values while retaining the original native
    assertions.
    """
    lang_cls, command, frame_pattern, error_pattern = _BACKENDS[backend_name]
    path = make_golden_path(
        parent=_CASES / corruption.case,
        name=lang_cls.__name__ + corruption.stem_suffix,
        lang_cls=lang_cls,
        version=next(iter(lang_cls.VersionFormats)),
    )
    declaration, consumer = path.read_text(encoding="utf-8").split(
        sep=CONSUMER_MARKER, maxsplit=1
    )
    old, new = (
        corruption.python if backend_name == "python" else corruption.ruby
    )
    assert old in declaration
    mutated_declaration = declaration.replace(old, new)
    program = mutated_declaration + CONSUMER_MARKER + consumer
    result = run_golden_program(
        fixture=path, command=command, program=program, scratch=tmp_path
    )
    assert result.returncode != 0, (
        f"{path}: native consumer missed {old!r} -> {new!r}"
    )

    # A parse error or a failure while constructing the value cannot
    # demonstrate that the consumer caught the corruption.
    error = re.search(
        pattern=error_pattern, string=result.stderr, flags=re.MULTILINE
    )
    assert error is not None, result.stderr
    frames = re.findall(
        pattern=frame_pattern, string=result.stderr, flags=re.MULTILINE
    )
    assert len(frames) > 0, result.stderr
    marker_line = mutated_declaration.count("\n") + 1
    failure_line = int(frames[-1])
    assert failure_line > marker_line, result.stderr
    assert (
        program.splitlines()[failure_line - 1]
        .lstrip()
        .startswith(("assert ", "raise "))
    ), result.stderr

    with pytest.raises(
        expected_exception=AssertionError, match="native observation mismatch"
    ):
        check_golden_observation(
            fixture=path,
            declaration=mutated_declaration,
            command=command,
            expected=_expected(fixture=path),
            scratch=tmp_path,
        )
