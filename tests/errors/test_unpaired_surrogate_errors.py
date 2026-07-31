"""Unpaired UTF-16 surrogate input is rejected before rendering."""

import importlib
from collections.abc import Callable

import pytest
from ruamel.yaml.comments import CommentedOrderedMap, CommentedSet

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
type DataFactory = Callable[..., object]

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


def _toml_value(*, surrogate: str) -> str:
    """Return TOML containing a raw surrogate value."""
    return f'outer = [{{ value = "{surrogate}" }}]'


def _toml_key(*, surrogate: str) -> str:
    """Return TOML containing a raw surrogate mapping key."""
    return f'outer = [{{ "{surrogate}" = "value" }}]'


def _nested_set(*, surrogate: str) -> object:
    """Return a nested parsed YAML tree containing a surrogate set
    item.
    """
    commented_set = CommentedSet(values=[surrogate])
    return {"outer": [{"inner": commented_set}]}


def _nested_ordered_map(*, surrogate: str) -> object:
    """Return a nested parsed YAML tree containing a surrogate omap
    value.
    """
    ordered_map = CommentedOrderedMap()
    ordered_map["key"] = surrogate
    return {"outer": [{"inner": ordered_map}]}


class _StubYaml:
    """Return a prepared parsed YAML tree."""

    def __init__(self, *, data: object) -> None:
        """Store the value returned by :meth:`load`."""
        self._data = data

    def load(self, *, stream: str) -> object:
        """Return the prepared tree."""
        del stream
        return self._data


@pytest.mark.parametrize(
    argnames=("input_format", "error_type", "source_factory"),
    argvalues=[
        (InputFormat.JSON, JSONParseError, _json_value),
        (InputFormat.JSON, JSONParseError, _json_key),
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
        literalize(
            source=source_factory(surrogate=surrogate),
            input_format=input_format,
            language=PYTHON,
        )


@pytest.mark.parametrize(
    argnames="data_factory",
    argvalues=[_nested_set, _nested_ordered_map],
)
def test_unpaired_surrogate_in_yaml_container_raises_parse_error(
    *,
    monkeypatch: pytest.MonkeyPatch,
    data_factory: DataFactory,
) -> None:
    """Nested YAML sets and ordered maps are validated recursively."""
    surrogate = chr(0xD800)
    stub_yaml = _StubYaml(data=data_factory(surrogate=surrogate))

    def get_stub_yaml() -> _StubYaml:
        """Return the test parser."""
        return stub_yaml

    parsing = importlib.import_module(name="literalizer._parsing")
    monkeypatch.setattr(
        target=parsing,
        name="get_yaml",
        value=get_stub_yaml,
    )

    with pytest.raises(
        expected_exception=YAMLParseError,
        match=r"unpaired UTF-16 surrogate U\+D800",
    ):
        literalize(
            source="!!stub",
            input_format=InputFormat.YAML,
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
