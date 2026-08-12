"""Negative-path checks for nested collection rendering context."""

import importlib
import inspect
from types import SimpleNamespace

import pytest


def test_nested_collection_context_requires_language_metaclass() -> None:
    """Malformed internal render contexts fail immediately."""
    module = importlib.import_module(name="literalizer._literalize")
    function_name = "_nested_collection_context"
    nested_collection_context = inspect.unwrap(
        func=vars(module)[function_name]
    )

    with pytest.raises(
        expected_exception=TypeError,
        match="requires a LanguageCls language",
    ):
        nested_collection_context(value=[], ctx=SimpleNamespace(spec=object()))
