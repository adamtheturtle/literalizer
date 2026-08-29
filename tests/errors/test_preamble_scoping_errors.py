"""Negative-path checks for wrap-mode preamble scoping.

These call an internal helper with a malformed spec to reach its
guard, which no public entry point can be made to do, so a rejection
manifest cannot declare them.
"""

import importlib
import inspect

import pytest


def test_scope_preamble_for_wrap_requires_language_metaclass() -> None:
    """Malformed internal language specs fail immediately."""
    module = importlib.import_module(name="literalizer._literalize")
    function_name = "_scope_preamble_for_wrap"
    scope_preamble_for_wrap = inspect.unwrap(func=vars(module)[function_name])

    with pytest.raises(
        expected_exception=TypeError,
        match="requires a LanguageCls language",
    ):
        scope_preamble_for_wrap(
            language=object(),
            preamble=(),
            data_dependent_entries=(),
        )
