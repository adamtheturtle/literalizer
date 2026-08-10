"""Perl float numeric-identity regression tests."""

import json
import shutil
import subprocess

import pytest

from literalizer import InputFormat, literalize
from literalizer.languages import Perl


def test_perl_float_literals_force_numeric_identity() -> None:
    """Large scientific literals participate in numeric arithmetic."""
    result = literalize(
        source="[0.1, 1e16, 1e-5, 123456789012345678.0]",
        input_format=InputFormat.JSON,
        language=Perl(),
    )

    assert "(0.0 + 1.0e+16)" in result.code
    assert "(0.0 + 1.2345678901234568e+17)" in result.code


def test_json_pp_keeps_large_float_values_numeric() -> None:
    """JSON::PP emits the reported values as numbers without rounding."""
    perl = shutil.which(cmd="perl")
    if perl is None:
        pytest.skip(reason="Perl is not installed")
    result = literalize(
        source="[0.1, 1e16, 1e-5, 123456789012345678.0]",
        input_format=InputFormat.JSON,
        language=Perl(),
    )
    program = (
        "use JSON::PP; my $value = "
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
