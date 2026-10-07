"""Public call rendering for opt-in PureScript records."""

from textwrap import dedent

from literalizer import InputFormat, literalize_call
from literalizer.languages import PureScript


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
