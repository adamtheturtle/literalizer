"""Compile public-default modules without changing their generated
names.
"""

import shutil
import subprocess
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parents[2]
_FIXTURES = _ROOT / "tests/integration/default_module_names"


@pytest.mark.parametrize(
    argnames="version", argvalues=["cpp14", "cpp17", "cpp20"]
)
@pytest.mark.parametrize(
    argnames="control",
    argvalues=["correct", "wrong_entrypoint", "wrong_result"],
)
def test_default_cpp_module_execution(
    tmp_path: Path,
    version: str,
    control: str,
) -> None:
    """The driver invokes Module and propagates its actual return
    value.
    """
    bash = shutil.which(cmd="bash")
    if (
        bash is None
        or shutil.which(cmd="clang++") is None
        or (
            shutil.which(cmd="timeout") is None
            and shutil.which(cmd="gtimeout") is None
        )
    ):
        pytest.skip(reason="Bash, clang++ and GNU timeout are required")
    directory = tmp_path / "default_module_names"
    directory.mkdir()
    name = f"Cpp_default_module_name@{version}.cpp"
    source = (_FIXTURES / name).read_text(encoding="utf-8")
    if control == "wrong_entrypoint":
        source = source.replace("Module()", "WrongModule()")
    elif control == "wrong_result":
        source = source.replace("return 0;", "return 42;")
    fixture = directory / name
    _ = fixture.write_text(data=source, encoding="utf-8")
    result = subprocess.run(  # noqa: S603 - installed tool and authored controls
        args=[
            bash,
            str(object=_ROOT / "scripts/lint-cpp-fixture.sh"),
            "run",
            str(object=fixture),
        ],
        cwd=_ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=120,
    )
    assert (result.returncode == 0) is (control == "correct"), result.stderr
    assert fixture.read_text(encoding="utf-8") == source
