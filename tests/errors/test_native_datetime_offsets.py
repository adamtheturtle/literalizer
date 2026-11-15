"""Reject native document timestamps outside their offset grammar."""

import datetime as dt

import pytest

import literalizer
from literalizer.exceptions import UnrepresentableInputError
from literalizer.languages import Toml, Yaml


@pytest.mark.parametrize(argnames="language", argvalues=[Toml(), Yaml()])
@pytest.mark.parametrize(
    argnames="offset_microseconds",
    argvalues=[1_000_000, -1_000_000, 1, -1, 19_815_000_001, -19_815_000_001],
)
def test_native_document_subminute_offset(
    language: literalizer.Language, offset_microseconds: int
) -> None:
    """Reject seconds and microseconds outside the timestamp grammar."""
    stamp = dt.datetime(
        year=2001,
        month=2,
        day=3,
        hour=4,
        minute=5,
        second=6,
        tzinfo=dt.timezone(
            offset=dt.timedelta(microseconds=offset_microseconds)
        ),
    )
    variable = (
        literalizer.NewVariable(name="my_data", modifiers=frozenset())
        if language.supports_variable_names
        else None
    )
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="sub-minute UTC offset",
    ):
        _ = literalizer.literalize(
            source='{"stamp": null}',
            input_format=literalizer.InputFormat.JSON,
            language=language,
            variable_form=variable,
            record_null_substitutions={"stamp": stamp},
            wrap_in_file=True,
        )
