"""Compile binary property programs and golden files in native Erlang.

This replaces the regex extraction in test_binary_roundtrip.py. The Erlang
CI job supplies the native runtime, so ordinary Python CI does not need it.
"""

import base64
import shutil
import subprocess
import tempfile
from pathlib import Path

from hypothesis import example, given, settings
from hypothesis import strategies as st

from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import Erlang

_DRIVER = """\
#!/usr/bin/env escript
main([Path, Shape | Encoded]) ->
    Values = [base64:decode(Value) || Value <- Encoded],
    Expected = case Shape of
        "scalar" -> [Value] = Values, Value;
        "sequence" -> Values
    end,
    Options = [binary, warnings_as_errors, report_errors, report_warnings],
    {ok, Module, Beam} = compile:file(Path, Options),
    {module, Module} = code:load_binary(Module, Path, Beam),
    Expected = Module:x().
"""


def _run_program(
    *, program: str, values: tuple[bytes, ...], shape: str
) -> None:
    """Compile the actual module with fatal warnings and check x/0's value."""
    escript = shutil.which(cmd="escript") or "escript"
    with tempfile.TemporaryDirectory() as temporary:
        directory = Path(temporary)
        source = directory / "module.erl"
        driver = directory / "check.escript"
        _ = source.write_text(data=program, encoding="utf-8")
        _ = driver.write_text(data=_DRIVER, encoding="utf-8")
        subprocess.run(
            args=[
                escript,
                str(object=driver),
                str(object=source),
                shape,
                *(
                    base64.b64encode(s=value).decode(encoding="ascii")
                    for value in values
                ),
            ],
            check=True,
            capture_output=True,
            text=True,
            timeout=30,
        )


@settings(deadline=None)
@example(data=b"")
@example(data=bytes(range(256)))
@given(data=st.binary())
def check_binary_document(data: bytes) -> None:
    """Retain every generated source and API option from the regex
    test.
    """
    encoded = base64.b64encode(s=data).decode(encoding="ascii")
    result = literalize(
        source=f'!!binary "{encoded}"\n',
        input_format=InputFormat.YAML,
        language=Erlang(),
        variable_form=NewVariable(name="my_data", modifiers=frozenset()),
        wrap_in_file=True,
    )
    if result.source_data != data:
        msg = "binary source data changed"
        raise AssertionError(msg)
    _run_program(program=result.code, values=(data,), shape="scalar")


def main() -> None:
    """Check the canonical golden and all generated binary documents."""
    golden = (
        Path(__file__).resolve().parents[1]
        / "tests/integration/cases/binary_octets/Erlang@otp_25.erl"
    )
    _run_program(
        program=golden.read_text(encoding="utf-8"),
        values=(b"", bytes(range(256)), bytes(reversed(range(256)))),
        shape="sequence",
    )
    # Hypothesis supplies data to the generated zero-argument check.
    check_binary_document()  # pylint: disable=no-value-for-parameter


if __name__ == "__main__":
    main()
