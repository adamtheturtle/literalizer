"""Error contracts for internal call checks."""

import inspect

import pytest

from literalizer._language import validate_call_parameter_names


def test_call_parameter_validation_requires_language_metaclass() -> None:
    """Malformed internal language objects fail immediately."""
    validator = inspect.unwrap(func=validate_call_parameter_names)
    with pytest.raises(
        expected_exception=TypeError,
        match="requires a LanguageCls language",
    ):
        validator(language=object(), names=(), reject_reserved=True)
