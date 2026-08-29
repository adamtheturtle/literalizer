"""The module-name boundary that is still valid.

The rejection is declared in ``tests/errors/rejections`` and run by
``test_rejections.py``.  What is left here is the acceptance side, which
no rejection manifest expresses.
"""

from literalizer.languages import Erlang


def test_erlang_accepts_module_name_at_atom_limit() -> None:
    """The 255-character atom boundary remains valid."""
    Erlang(module_name="a" * 255)
