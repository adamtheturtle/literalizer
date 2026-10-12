"""Build invocations of the shared GNU timeout command wrapper."""

from collections.abc import Sequence
from pathlib import Path

from beartype import beartype

_WRAPPER = Path(__file__).resolve().with_name(name="run-bounded.sh")


@beartype
def bounded_command(
    *, args: Sequence[str | Path], fixture: str, timeout_seconds: float
) -> list[str]:
    """Give a compiler or executable its own deadline and fixture label.

    The absolute wrapper path also works when subprocesses run in temporary
    directories. GNU timeout owns deadlines and process termination; the
    wrapper only discovers it and adds diagnostics. Standard output remains
    unchanged.
    """
    return [
        str(object=_WRAPPER),
        fixture,
        "--signal=KILL",
        f"{timeout_seconds:g}s",
        *(str(object=arg) for arg in args),
    ]
