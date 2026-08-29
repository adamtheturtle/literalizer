"""Unpaired UTF-16 surrogate input is rejected before rendering.

Half of these sources carry a raw lone surrogate, which is not valid
UTF-8 and so cannot be written into a manifest's TOML at all.  The
escaped half is generated from the same factories, so it stays beside
the raw half rather than being split across two places.
"""

from collections.abc import Callable

import pytest

from literalizer import InputFormat, Language, NewVariable, literalize
from literalizer.exceptions import (
    JSON5ParseError,
    JSONParseError,
    ParseError,
    TOMLParseError,
    YAMLParseError,
)
from literalizer.languages import Ada, Cobol, Python

type ParseErrorType = type[ParseError]

PYTHON = Python(
    date_format=Python.date_formats.PYTHON,
    datetime_format=Python.datetime_formats.PYTHON,
    bytes_format=Python.bytes_formats.HEX,
    sequence_format=Python.sequence_formats.TUPLE,
    set_format=Python.set_formats.SET,
    variable_type_hints=Python.variable_type_hints_formats.NEVER,
)


def _json_value(*, surrogate: str) -> str:
    """Return JSON with *surrogate* represented by a Unicode escape."""
    return f'{{"outer": [{{"value": "\\u{ord(surrogate):04x}"}}]}}'


def _json_key(*, surrogate: str) -> str:
    """Return JSON with *surrogate* in a nested mapping key."""
    return f'{{"outer": [{{"\\u{ord(surrogate):04x}": "value"}}]}}'


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


def _yaml_set(*, surrogate: str) -> str:
    """Return YAML with a surrogate escape in a nested set item."""
    return f'outer:\n  - inner: !!set\n      ? "\\u{ord(surrogate):04x}"\n'


def _yaml_ordered_map(*, surrogate: str) -> str:
    """Return YAML with a surrogate escape in an ordered-map value."""
    return (
        f'outer:\n  - inner: !!omap\n      - key: "\\u{ord(surrogate):04x}"\n'
    )


def _toml_value(*, surrogate: str) -> str:
    """Return TOML containing a raw surrogate value."""
    return f'outer = [{{ value = "{surrogate}" }}]'


def _toml_key(*, surrogate: str) -> str:
    """Return TOML containing a raw surrogate mapping key."""
    return f'outer = [{{ "{surrogate}" = "value" }}]'


@pytest.mark.parametrize(
    argnames=("input_format", "error_type", "source_factory"),
    argvalues=[
        (InputFormat.JSON, JSONParseError, _json_value),
        (InputFormat.JSON, JSONParseError, _json_key),
        (InputFormat.JSON5, JSON5ParseError, _json5_value),
        (InputFormat.JSON5, JSON5ParseError, _json5_key),
        (InputFormat.YAML, YAMLParseError, _yaml_value),
        (InputFormat.YAML, YAMLParseError, _yaml_key),
        (InputFormat.YAML, YAMLParseError, _yaml_set),
        (InputFormat.YAML, YAMLParseError, _yaml_ordered_map),
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
        literalize(
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
        literalize(
            source=f'value = "safe" # {chr(0xD800)}',
            input_format=InputFormat.TOML,
            language=PYTHON,
        )


@pytest.mark.parametrize(argnames="language", argvalues=[Ada(), Cobol()])
def test_reported_backends_do_not_leak_unicode_encode_error(
    language: Language,
) -> None:
    """The original Ada and COBOL failures now stop at parsing."""
    with pytest.raises(expected_exception=JSONParseError):
        literalize(
            source='{"x": "\\ud800"}',
            input_format=InputFormat.JSON,
            language=language,
            variable_form=NewVariable(
                name="my_data",
                modifiers=frozenset(),
            ),
            wrap_in_file=True,
        )
