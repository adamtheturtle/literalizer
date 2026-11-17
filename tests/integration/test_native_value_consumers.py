"""Corruption controls for native assertions in compiling golden files."""

import dataclasses
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from literalizer.languages import Python, Ruby

from .language_specs import make_golden_path

_MARKER = "# Independent native value checks."
_CASES = Path(__file__).parent / "cases"
_MINIMUM_RUBY_MAJOR = 3


@pytest.fixture(scope="session", name="ruby_available")
def fixture_ruby_available() -> bool:
    """Detect a runtime supported by the Ruby backend."""
    ruby = shutil.which(cmd="ruby")
    if ruby is None:
        return False
    result = subprocess.run(  # noqa: S603 - inspect the selected native interpreter
        args=[ruby, "-e", "puts RUBY_VERSION.split('.').first.to_i"],
        capture_output=True,
        text=True,
        check=True,
        timeout=30,
    )
    return int(result.stdout) >= _MINIMUM_RUBY_MAJOR


def _execute(
    *, path: Path, ruby_available: bool
) -> subprocess.CompletedProcess[str]:
    """Use the same self-contained programs executed by the native
    jobs.
    """
    if path.suffix == ".py":
        args = [sys.executable, "-I", str(object=path)]
    else:
        if not ruby_available:
            pytest.skip(reason="Ruby 3+ is unavailable")
        ruby = shutil.which(cmd="ruby")
        assert ruby is not None
        args = [ruby, str(object=path)]
    return subprocess.run(  # noqa: S603 - execute an authored native golden consumer
        args=args,
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
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
)


@pytest.mark.parametrize(
    argnames=("backend_name", "corruption"),
    argvalues=[
        (backend_name, corruption)
        for backend_name in ("python", "ruby")
        for corruption in _CORRUPTIONS
    ]
    + [
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
    ruby_available: bool,
) -> None:
    """Corrupt generated values while retaining the original native
    assertions.
    """
    lang_cls = {"python": Python, "ruby": Ruby}[backend_name]
    path = make_golden_path(
        parent=_CASES / corruption.case,
        name=lang_cls.__name__ + corruption.stem_suffix,
        lang_cls=lang_cls,
        version=next(iter(lang_cls.VersionFormats)),
    )
    declaration, consumer = path.read_text(encoding="utf-8").split(
        sep=_MARKER, maxsplit=1
    )
    old, new = (
        corruption.python if backend_name == "python" else corruption.ruby
    )
    assert old in declaration
    target = tmp_path / corruption.case / path.name
    target.parent.mkdir()
    _ = target.write_text(
        data=declaration.replace(old, new) + _MARKER + consumer,
        encoding="utf-8",
    )
    result = _execute(path=target, ruby_available=ruby_available)
    assert result.returncode != 0, (
        f"{path}: native consumer missed {old!r} -> {new!r}"
    )
    assert corruption.case in result.stderr
