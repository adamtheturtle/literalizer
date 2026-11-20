"""Corruption controls for native assertions in compiling golden files."""

import dataclasses
import re
import subprocess
import sys
from pathlib import Path

import pytest

from literalizer.languages import Python

from .language_specs import make_golden_path

_MARKER = "# Independent native value checks."
_CASES = Path(__file__).parent / "cases"


@dataclasses.dataclass(frozen=True, kw_only=True)
class Corruption:
    """A changed native literal, independent of the authored expected
    input.
    """

    case: str
    stem_suffix: str
    replacement: tuple[str, str]


_CORRUPTIONS = (
    Corruption(
        case="list_beyond_i64",
        stem_suffix="",
        replacement=("9223372036854775808", "9223372036854775809"),
    ),
    Corruption(
        case="list_beyond_i64",
        stem_suffix="",
        replacement=("9223372036854775808", "9223372036854775808.0"),
    ),
    Corruption(
        case="bool_list",
        stem_suffix="",
        replacement=("True", "1"),
    ),
    Corruption(
        case="float_negative_zero",
        stem_suffix="",
        replacement=("-0.0", "0.0"),
    ),
    Corruption(
        case="scientific_float_precision",
        stem_suffix="_float_format_scientific_precision",
        replacement=("1.2345678901234567", "1.2345678901234565"),
    ),
    Corruption(
        case="float_special_values",
        stem_suffix="",
        replacement=('float("nan")', 'float("inf")'),
    ),
    Corruption(
        case="binary_octets",
        stem_suffix="",
        replacement=("00010203", "01010203"),
    ),
    Corruption(
        case="int_key_dict",
        stem_suffix="",
        replacement=('1: "one"', '"1": "one"'),
    ),
    Corruption(
        case="date_list",
        stem_suffix="",
        replacement=("day=20", "day=21"),
    ),
    Corruption(
        case="scalar_datetime_non_utc",
        stem_suffix="",
        replacement=("hour=18", "hour=17"),
    ),
    Corruption(
        case="scalar_datetime_non_utc",
        stem_suffix="",
        replacement=("minutes=30", "minutes=0"),
    ),
    Corruption(
        case="list_beyond_i64",
        stem_suffix="",
        replacement=(
            "(\n    9223372036854775807,\n    9223372036854775808,\n)",
            "{9223372036854775807: None, 9223372036854775808: None}",
        ),
    ),
    Corruption(
        case="binary_nonempty_octets",
        stem_suffix="_bytes_format_python",
        replacement=(r"\x00", r"\x01"),
    ),
    Corruption(
        case="binary_nonempty_octets",
        stem_suffix="_bytes_format_python",
        replacement=("b'", "'"),
    ),
)


@pytest.mark.parametrize(
    argnames="corruption",
    argvalues=_CORRUPTIONS,
)
def test_native_value_corruptions(
    *,
    corruption: Corruption,
    tmp_path: Path,
) -> None:
    """Corrupt generated values while retaining the original native
    assertions.
    """
    path = make_golden_path(
        parent=_CASES / corruption.case,
        name=Python.__name__ + corruption.stem_suffix,
        lang_cls=Python,
        version=next(iter(Python.VersionFormats)),
    )
    declaration, consumer = path.read_text(encoding="utf-8").split(
        sep=_MARKER, maxsplit=1
    )
    old, new = corruption.replacement
    assert old in declaration
    mutated_declaration = declaration.replace(old, new)
    program = mutated_declaration + _MARKER + consumer
    target = tmp_path / path.name
    _ = target.write_text(data=program, encoding="utf-8")
    result = subprocess.run(  # noqa: S603 - execute an authored native golden consumer
        args=[sys.executable, "-I", str(object=target)],
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )
    assert result.returncode != 0, (
        f"{path}: native consumer missed {old!r} -> {new!r}"
    )

    # A parse error or a failure while constructing the value cannot
    # demonstrate that the consumer caught the corruption.
    error = re.search(
        pattern=r"^AssertionError(?::|$)",
        string=result.stderr,
        flags=re.MULTILINE,
    )
    assert error is not None, result.stderr
    frames = re.findall(
        pattern=r'^\s*File ".*", line (\d+), in ',
        string=result.stderr,
        flags=re.MULTILINE,
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
