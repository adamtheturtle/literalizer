"""Build invocations of the shared GNU timeout command wrapper."""

from collections.abc import Sequence
from pathlib import Path

_WRAPPER = Path(__file__).resolve().with_name(name="run-bounded.sh")


def bounded_command(
    *, args: Sequence[str | Path], fixture: str, timeout_seconds: float
) -> list[str]:
    """Give a compiler or executable its own deadline and fixture label.

    The absolute wrapper path also works when subprocesses run in temporary
    directories. The wrapper owns timeout discovery, process-group killing,
    status preservation, and stderr diagnostics; stdout remains unchanged.
    """
    return [
        str(object=_WRAPPER),
        fixture,
        f"{timeout_seconds:g}s",
        "KILL",
        *(str(object=arg) for arg in args),
    ]
