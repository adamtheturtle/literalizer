"""Target-induced scalar collection collision errors."""

import pytest

from literalizer import InputFormat, literalize
from literalizer._language import Language
from literalizer.exceptions import TargetScalarCollisionError
from literalizer.languages import JavaScript, Swift


@pytest.mark.parametrize(
    argnames=("source", "language"),
    argvalues=[
        (
            "!!set\n? !!binary /w==\n? ff\n",
            JavaScript(bytes_format=JavaScript.bytes_formats.HEX),
        ),
        (
            '!!set\n? 2024-01-01\n? "2024-01-01"\n',
            JavaScript(date_format=JavaScript.date_formats.ISO),
        ),
        (
            "!!set\n? 1970-01-01T00:00:01Z\n? 1\n",
            JavaScript(datetime_format=JavaScript.datetime_formats.EPOCH),
        ),
        (
            '2024-01-01: temporal\n"2024-01-01": string\n',
            JavaScript(date_format=JavaScript.date_formats.ISO),
        ),
        (
            "1970-01-01T00:00:01Z: temporal\n1: integer\n",
            JavaScript(datetime_format=JavaScript.datetime_formats.EPOCH),
        ),
        (
            "2024-01-01: date\n2024-01-01T00:00:00Z: datetime\n",
            Swift(),
        ),
    ],
)
def test_target_scalar_collision_raises(
    source: str,
    language: Language,
) -> None:
    """Distinct source scalars must remain distinct collection values."""
    with pytest.raises(
        expected_exception=TargetScalarCollisionError,
        match="renders distinct collection scalars",
    ):
        literalize(
            source=source,
            input_format=InputFormat.YAML,
            language=language,
        )
