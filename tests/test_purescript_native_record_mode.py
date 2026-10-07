"""Public API coverage for opt-in PureScript records."""

from textwrap import dedent

import pytest

from literalizer import InputFormat, literalize, literalize_call
from literalizer.exceptions import (
    HeterogeneousScalarCollectionError,
    UnrepresentableInputError,
    UnrepresentableIntegerError,
)
from literalizer.languages import PureScript


@pytest.mark.parametrize(
    argnames=("source", "input_format", "message"),
    argvalues=[
        ('{"not-a-field": 1}', InputFormat.JSON, "field"),
        ('{"case": 1}', InputFormat.JSON, "field"),
        ('{"Bad": 1}', InputFormat.JSON, "field"),
        ("1: one\n", InputFormat.YAML, "field"),
        ("{}", InputFormat.JSON, "empty records"),
        ('{"x": null}', InputFormat.JSON, "NoneType"),
        ('[{"x": 1}, {"x": "one"}]', InputFormat.JSON, "uniform"),
        ('[{"x": 1}, {"y": 1}]', InputFormat.JSON, "uniform"),
        ("[1, 2147483648]", InputFormat.JSON, "integer widths"),
        ("--- !!omap\n- a: 1\n", InputFormat.YAML, "ordered maps"),
        ("--- !!set\na:\n", InputFormat.YAML, "set"),
    ],
)
def test_record_mode_rejects_unsupported_input(
    source: str, input_format: InputFormat, message: str
) -> None:
    """Unsupported shapes fail before producing invalid code."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError, match=message
    ):
        _ = literalize(
            source=source,
            input_format=input_format,
            language=PureScript(dict_format=PureScript.dict_formats.RECORD),
        )


def test_record_mode_conflicts_with_argonaut() -> None:
    """Native records and dynamic Argonaut values cannot be combined."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError, match="json_type"
    ):
        _ = literalize(
            source='{"x": 1}',
            input_format=InputFormat.JSON,
            language=PureScript(
                dict_format=PureScript.dict_formats.RECORD,
                json_type=PureScript.json_types.ARGONAUT_JSON,
            ),
        )


def test_record_mode_rejects_mixed_scalar_array() -> None:
    """A native array cannot infer both Int and String elements."""
    with pytest.raises(expected_exception=HeterogeneousScalarCollectionError):
        _ = literalize(
            source='[1, "hello"]',
            input_format=InputFormat.JSON,
            language=PureScript(dict_format=PureScript.dict_formats.RECORD),
        )


def test_record_mode_rejects_integer_beyond_number_precision() -> None:
    """Avoid silently rounding beyond the safe integer range."""
    with pytest.raises(expected_exception=UnrepresentableIntegerError):
        _ = literalize(
            source='{"value": 9007199254740993}',
            input_format=InputFormat.JSON,
            language=PureScript(dict_format=PureScript.dict_formats.RECORD),
        )


def test_record_mode_call_argument() -> None:
    """Calls receive a native record rather than a ``Val`` constructor."""
    # The wrapped call still declares its stub as Val -> Unit, although
    # native-record mode emits no Val type, so it has no compiling golden.
    result = literalize_call(
        source='[[{"x": 1}]]',
        input_format=InputFormat.JSON,
        language=PureScript(dict_format=PureScript.dict_formats.RECORD),
        target_function="consume",
        parameter_names=("item",),
        wrap_in_file=True,
    )
    assert result.code == dedent(
        text="""\
        module Check where


        import Prelude
        consume :: Val -> Unit
        consume _ = unit


        main :: Unit
        main =
            let
                _ = consume ({ x: 1 })
            in
            unit"""
    )
