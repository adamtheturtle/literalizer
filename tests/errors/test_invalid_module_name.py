"""Module-name validation errors."""

import pytest

from literalizer.exceptions import InvalidModuleNameError
from literalizer.languages import Java


@pytest.mark.parametrize(argnames="module_name", argvalues=["int", "_"])
def test_java_rejects_reserved_module_name(module_name: str) -> None:
    """Java wrapper classes cannot use reserved identifiers."""
    with pytest.raises(expected_exception=InvalidModuleNameError):
        Java(module_name=module_name)
