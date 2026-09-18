"""Input boundaries for the opt-in native Roc record format."""

import pytest

from literalizer import InputFormat, literalize
from literalizer.exceptions import UnrepresentableInputError
from literalizer.languages import Roc


@pytest.mark.parametrize(
    argnames="source",
    argvalues=[
        '{"not-a-field": 1}',
        '{"if": 1}',
        '{"outer": {"Bad": 1}}',
    ],
)
def test_record_mode_rejects_non_field_keys(source: str) -> None:
    """Never emit a syntactically invalid Roc record field."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError, match="field"
    ):
        _ = literalize(
            source=source,
            input_format=InputFormat.JSON,
            language=Roc(dict_format=Roc.dict_formats.RECORD),
        )


def test_default_mode_preserves_arbitrary_string_keys() -> None:
    """Native records do not narrow the pre-existing tagged mode."""
    result = literalize(
        source='{"not-a-field": 1}',
        input_format=InputFormat.JSON,
        language=Roc(),
    )
    assert '("not-a-field", RInt 1i128)' in result.code


def test_record_mode_rejects_conflicting_list_field_types() -> None:
    """A Roc list cannot mix records with conflicting field types."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="uniform record list types",
    ):
        _ = literalize(
            source='[{"x": 1}, {"x": "a"}]',
            input_format=InputFormat.JSON,
            language=Roc(dict_format=Roc.dict_formats.RECORD),
        )
