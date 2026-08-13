"""Tcl call comments remain comments at trailing command position."""

import subprocess
from shutil import which

from literalizer import InputFormat, literalize_call
from literalizer.languages import Tcl


def test_tcl_trailing_call_comment_is_not_an_argument() -> None:
    """A strict one-argument proc accepts a commented generated call."""
    rendered = literalize_call(
        source='[["a"]]',
        input_format=InputFormat.JSON,
        language=Tcl(),
        target_function="process",
        parameter_names=["x"],
        comment_source=["first case"],
    )
    script = f"proc process {{x}} {{return $x}}\n{rendered.code}\n"

    tclsh = which(cmd="tclsh")
    assert tclsh is not None
    completed = subprocess.run(
        args=[tclsh],
        input=script,
        text=True,
        capture_output=True,
        check=False,
    )

    assert rendered.code == 'process "a"  ;# first case'
    assert completed.returncode == 0, completed.stderr
