"""Missing native constructor syntax is an error."""

import pytest

from tests.integration.case_manifests import (
    CaseManifestError,
    ConstructorCaseSpec,
)
from tests.integration.constructor_templates import constructor_target_template


def test_missing_target_template_is_an_error() -> None:
    """A selected backend needs an entry in the native template table."""
    config = ConstructorCaseSpec(target_templates={"Ada": "{target}"})
    with pytest.raises(
        expected_exception=CaseManifestError,
        match="no constructor target template for 'Nix'",
    ):
        _ = constructor_target_template(config=config, language_name="Nix")
