"""Raw lone UTF-16 surrogates are rejected before rendering.

These sources are not valid UTF-8 and cannot be written into TOML.
Serializable escaped-surrogate cases live in the JSON and YAML
unpaired-surrogate rejection manifests, beside the JSONC cases.
"""

from collections.abc import Callable

import pytest

from literalizer import InputFormat, literalize
from literalizer.exceptions import (
    JSON5ParseError,
    ParseError,
    TOMLParseError,
    YAMLParseError,
)
from literalizer.languages import Python

type ParseErrorType = type[ParseError]

PYTHON = Python(
    date_format=Python.date_formats.PYTHON,
    datetime_format=Python.datetime_formats.PYTHON,
    bytes_format=Python.bytes_formats.HEX,
    sequence_format=Python.sequence_formats.TUPLE,
    set_format=Python.set_formats.SET,
    variable_type_hints=Python.variable_type_hints_formats.NEVER,
)


def _json5_value(*, surrogate: str) -> str:
    """Return JSON5 containing a raw surrogate value."""
    return f'{{outer: [{{value: "{surrogate}"}}]}}'


def _json5_key(*, surrogate: str) -> str:
    """Return JSON5 containing a raw surrogate mapping key."""
    return f'{{outer: [{{"{surrogate}": "value"}}]}}'


def _yaml_value(*, surrogate: str) -> str:
    """Return YAML containing a raw surrogate value."""
    return f'outer:\n  - value: "{surrogate}"\n'


def _yaml_key(*, surrogate: str) -> str:
    """Return YAML containing a raw surrogate mapping key."""
    return f'outer:\n  - "{surrogate}": value\n'


def _toml_value(*, surrogate: str) -> str:
    """Return TOML containing a raw surrogate value."""
    return f'outer = [{{ value = "{surrogate}" }}]'


def _toml_key(*, surrogate: str) -> str:
    """Return TOML containing a raw surrogate mapping key."""
    return f'outer = [{{ "{surrogate}" = "value" }}]'


@pytest.mark.parametrize(
    argnames=("input_format", "error_type", "source_factory"),
    argvalues=[
        (InputFormat.JSON5, JSON5ParseError, _json5_value),
        (InputFormat.JSON5, JSON5ParseError, _json5_key),
        (InputFormat.YAML, YAMLParseError, _yaml_value),
        (InputFormat.YAML, YAMLParseError, _yaml_key),
        (InputFormat.TOML, TOMLParseError, _toml_value),
        (InputFormat.TOML, TOMLParseError, _toml_key),
    ],
)
@pytest.mark.parametrize(
    argnames="surrogate_code_point",
    argvalues=[0xD800, 0xDC00],
)
def test_unpaired_surrogates_raise_parse_error(
    *,
    input_format: InputFormat,
    error_type: ParseErrorType,
    source_factory: Callable[..., str],
    surrogate_code_point: int,
) -> None:
    """Every parser rejects lone high and low surrogates recursively."""
    surrogate = chr(surrogate_code_point)
    with pytest.raises(
        expected_exception=error_type,
        match=rf"unpaired UTF-16 surrogate U\+{surrogate_code_point:04X}",
    ):
        _ = literalize(
            source=source_factory(surrogate=surrogate),
            input_format=input_format,
            language=PYTHON,
        )


def test_unpaired_surrogate_in_toml_comment_raises_parse_error() -> None:
    """Preserved source comments cannot put a surrogate in output code."""
    with pytest.raises(
        expected_exception=TOMLParseError,
        match=r"unpaired UTF-16 surrogate U\+D800",
    ):
        _ = literalize(
            source=f'value = "safe" # {chr(0xD800)}',
            input_format=InputFormat.TOML,
            language=PYTHON,
        )
