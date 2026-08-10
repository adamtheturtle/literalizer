"""Perl float numeric-identity regression tests."""

import json
import shutil
import subprocess

from literalizer import InputFormat, literalize
from literalizer.languages import Perl


def test_perl_float_literals_force_numeric_identity() -> None:
    """Large scientific literals participate in numeric arithmetic."""
    result = literalize(
        source="[0.1, 1e16, 1e-5, 123456789012345678.0]",
        input_format=InputFormat.JSON,
        language=Perl(),
    )

    assert 'Math::BigFloat->new("1.0e+16")' in result.code
    assert 'Math::BigFloat->new("1.2345678901234568e+17")' in result.code
    assert "use Math::BigFloat;" in result.preamble


def test_json_pp_keeps_large_float_values_numeric() -> None:
    """JSON::PP emits the reported values as numbers without rounding."""
    perl = shutil.which(cmd="perl")
    assert perl is not None, "Perl is required for this test"
    result = literalize(
        source="[0.1, 1e16, 1e-5, 123456789012345678.0]",
        input_format=InputFormat.JSON,
        language=Perl(),
    )
    preamble = "\n".join(result.preamble)
    program = (
        f"use JSON::PP; {preamble}\nmy $value = "
        f"{result.code}; print JSON::PP->new->allow_bignum->encode($value);"
    )
    completed = subprocess.run(
        args=[perl, "-e", program],
        check=True,
        capture_output=True,
        text=True,
    )

    assert json.loads(s=completed.stdout) == [
        0.1,
        1e16,
        1e-5,
        123456789012345678.0,
    ]
