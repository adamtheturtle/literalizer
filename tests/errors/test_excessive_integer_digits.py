"""Rejection tests for integers too wide for the interpreter to write out.

CPython caps ``int``-to-``str`` conversion at
``sys.get_int_max_str_digits()`` decimal digits.  The limit is lowered
here rather than written into a fixture so the inputs stay small and the
tests do not depend on the interpreter's default, which is a tuning knob
rather than a promise.
"""

import sys
from collections.abc import Iterator

import pytest

from literalizer import InputFormat, NewVariable, literalize
from literalizer.exceptions import (
    ExcessiveIntegerDigitsError,
    LiteralizerError,
)
from literalizer.languages import Python

_LOWERED_LIMIT = 640
"""A digit limit far below the interpreter's default.

``sys.set_int_max_str_digits`` refuses anything under 640, so this is
the smallest value that keeps the test inputs short.
"""

_OVER_LIMIT_DIGITS = "1" + "0" * _LOWERED_LIMIT
"""A decimal token one digit wider than the lowered limit allows."""


@pytest.fixture(name="lowered_digit_limit")
def fixture_lowered_digit_limit() -> Iterator[None]:
    """Lower the interpreter's integer conversion limit for one test."""
    original = sys.get_int_max_str_digits()
    sys.set_int_max_str_digits(maxdigits=_LOWERED_LIMIT)
    try:
        yield
    finally:
        sys.set_int_max_str_digits(maxdigits=original)


@pytest.mark.usefixtures("lowered_digit_limit")
@pytest.mark.parametrize(
    argnames=("source", "input_format"),
    argvalues=[
        pytest.param(
            f'{{"a": {_OVER_LIMIT_DIGITS}}}',
            InputFormat.JSON,
            id="json-decimal",
        ),
        pytest.param(
            f'{{"a": {_OVER_LIMIT_DIGITS}}}',
            InputFormat.JSON5,
            id="json5-decimal",
        ),
        pytest.param(
            f"a: {_OVER_LIMIT_DIGITS}",
            InputFormat.YAML,
            id="yaml-decimal",
        ),
        pytest.param(
            '{"a": 0x' + "f" * _LOWERED_LIMIT + "}",
            InputFormat.JSON5,
            id="json5-hexadecimal",
        ),
        pytest.param(
            "a = 0x" + "f" * _LOWERED_LIMIT,
            InputFormat.TOML,
            id="toml-hexadecimal",
        ),
    ],
)
def test_parsed_integer_beyond_digit_limit(
    source: str,
    input_format: InputFormat,
) -> None:
    """An integer the interpreter will not write out is rejected."""
    with pytest.raises(
        expected_exception=ExcessiveIntegerDigitsError,
        match="more decimal digits",
    ):
        literalize(
            source=source,
            input_format=input_format,
            language=Python(),
            variable_form=NewVariable(name="v", modifiers=frozenset()),
        )


@pytest.mark.usefixtures("lowered_digit_limit")
def test_toml_decimal_beyond_digit_limit() -> None:
    """A TOML decimal integer too wide to write out is rejected.

    Which rejection arrives depends on the tomlkit release: some read
    the token as a float, which reaches the numeric-token check and
    gives :class:`ExcessiveIntegerDigitsError`, while others refuse it
    as an invalid number.  Both are typed, which is what the contract
    promises; the bare ``ValueError`` is what must not escape.
    """
    with pytest.raises(expected_exception=LiteralizerError):
        literalize(
            source=f"a = {_OVER_LIMIT_DIGITS}",
            input_format=InputFormat.TOML,
            language=Python(),
            variable_form=NewVariable(name="v", modifiers=frozenset()),
        )


@pytest.mark.usefixtures("lowered_digit_limit")
def test_substituted_integer_beyond_digit_limit() -> None:
    """An integer supplied through the API is rejected the same way.

    Nothing is parsed here, so the rejection has to come from the
    renderer rather than from an input hook.
    """
    with pytest.raises(
        expected_exception=ExcessiveIntegerDigitsError,
        match="more decimal digits",
    ):
        literalize(
            source='{"a": null}',
            input_format=InputFormat.JSON,
            language=Python(),
            variable_form=NewVariable(name="v", modifiers=frozenset()),
            record_null_substitutions={"a": 10**_LOWERED_LIMIT},
        )


@pytest.mark.usefixtures("lowered_digit_limit")
def test_integer_at_digit_limit_is_accepted() -> None:
    """The widest integer the interpreter writes out still renders."""
    at_limit = "9" * _LOWERED_LIMIT
    result = literalize(
        source=f'{{"a": {at_limit}}}',
        input_format=InputFormat.JSON,
        language=Python(),
        variable_form=NewVariable(name="v", modifiers=frozenset()),
    )
    assert result.code == f'v = {{\n    "a": {at_limit},\n}}'


def test_disabled_digit_limit_renders_any_width() -> None:
    """No integer is rejected while the interpreter's limit is off."""
    original = sys.get_int_max_str_digits()
    sys.set_int_max_str_digits(maxdigits=0)
    try:
        result = literalize(
            source='{"a": null}',
            input_format=InputFormat.JSON,
            language=Python(),
            variable_form=NewVariable(name="v", modifiers=frozenset()),
            record_null_substitutions={"a": 10**_LOWERED_LIMIT},
        )
    finally:
        sys.set_int_max_str_digits(maxdigits=original)
    assert result.code == f'v = {{\n    "a": {10**_LOWERED_LIMIT},\n}}'
