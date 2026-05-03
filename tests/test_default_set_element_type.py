"""Tests for default set element type support."""

import pytest

from literalizer.exceptions import DefaultSetElementTypeNotSupportedError
from literalizer.languages import Scala


def test_unsupported_default_set_element_type_raises_typed_error() -> None:
    """Unsupported languages reject ``default_set_element_type`` by
    name.
    """
    with pytest.raises(
        expected_exception=DefaultSetElementTypeNotSupportedError,
    ) as exc_info:
        Scala(default_set_element_type="String")

    assert exc_info.value.language_name == "Scala"
