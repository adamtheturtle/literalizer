r"""``isinstance()`` against a ``@runtime_checkable`` Protocol is fast
when every member resolves to a non-``None`` value, and slow (O(N) in
member count) when any member is ``None``.

Reported upstream as
https://github.com/python/cpython/issues/156413.

This is plain ``isinstance`` behavior — no beartype involved.
``beartype`` amplifies the impact because every
``@beartype``-decorated function parameter typed as a
``runtime_checkable`` Protocol triggers an ``isinstance`` check on
every call.

Usage:

    hyperfine --warmup 1 \
      'python repro.py none-5' \
      'python repro.py none-110' \
      'python repro.py true-5' \
      'python repro.py true-110'
"""

import sys
from typing import Protocol, runtime_checkable


def make_protocol(n_attrs: int) -> type:
    """Build a ``@runtime_checkable`` Protocol with *n_attrs* bool
    properties.
    """

    def protocol_member(_: object) -> bool:
        """Stand in for a generated Protocol property."""
        raise NotImplementedError

    namespace: dict[str, object] = {
        f"p{i}": property(fget=protocol_member) for i in range(n_attrs)
    }
    return runtime_checkable(cls=type("P", (Protocol,), namespace))


def make_impl(n_attrs: int, last_value: object) -> object:
    """Build an instance with attributes ``p0..p_{n-2}`` set to ``True``
    and ``p_last`` set to *last_value* (``None`` or ``True``).
    """
    attrs: dict[str, object] = {f"p{i}": True for i in range(n_attrs - 1)}
    attrs[f"p{n_attrs - 1}"] = last_value
    return type("Impl", (), attrs)()


ITERS = 200_000


def main() -> None:
    """Run ``ITERS`` ``isinstance`` checks for one (mode, size) pair."""
    mode = sys.argv[1]
    last_label, n_label = mode.split(sep="-")
    n_attrs = int(n_label)
    last_value: object
    last_value = True
    if last_label == "none":
        last_value = None

    proto = make_protocol(n_attrs=n_attrs)
    instance = make_impl(n_attrs=n_attrs, last_value=last_value)

    isinstance(instance, proto)
    for _ in range(ITERS):
        isinstance(instance, proto)


if __name__ == "__main__":
    main()
