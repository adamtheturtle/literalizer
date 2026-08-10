"""Perl special-float syntax regression tests."""

import shutil
import subprocess

import pytest

from literalizer import InputFormat, literalize
from literalizer.languages import Perl


def test_perl_special_floats_are_strict_safe() -> None:
    """Infinity and NaN output compiles under modern Perl strict mode."""
    result = literalize(
        source="[.inf, -.inf, .nan]",
        input_format=InputFormat.YAML,
        language=Perl(),
    )
    assert "9**9**9" in result.code
    assert "Inf" not in result.code

    perl = shutil.which(cmd="perl")
    if perl is None:
        pytest.skip(reason="Perl is not installed")  # pragma: no cover
    program = f"use strict; use warnings; my $value = {result.code};"
    completed = subprocess.run(
        args=[perl, "-e", program],
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr
