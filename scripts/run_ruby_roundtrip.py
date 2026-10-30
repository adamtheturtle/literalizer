"""Ruby JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to a Ruby
``myData = ...`` assignment, wrap it in a tiny script that prints
``JSON.generate(myData)``, run it with Ruby, and hand the emitted JSON
to :func:`roundtrip_common.verify`.

This lives here, driven by the ``Ruby roundtrip`` step of the
``lint-fast`` job in ``.github/workflows/lint.yml``, because that job is
where the Ruby toolchain is installed.  It shares the same input and
comparison logic as the other per-language round-trip helpers.
"""

import datetime as dt
import json
import shutil
from fractions import Fraction

from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import Ruby
from scripts import roundtrip_common

_VAR_NAME = "myData"
_LABEL = "Ruby"


def _build_program(json_text: str) -> str:
    """Return a runnable Ruby program literalized from *json_text*."""
    result = roundtrip_common.literalize_new_variable(
        language=Ruby(),
        json_text=json_text,
        var_name=_VAR_NAME,
        pre_indent_level=0,
    )
    preamble = "\n".join((*result.preamble, *result.body_preamble))
    return (
        "# frozen_string_literal: true\n"
        "\n"
        "require 'json'\n"
        f"{preamble}\n"
        f"{result.code}\n"
        f'negative_zero = {_VAR_NAME}.fetch("negative_zero")\n'
        "unless negative_zero.is_a?(Float) && negative_zero.zero? &&\n"
        "       (1.0 / negative_zero).negative?\n"
        '  raise "negative_zero lost its sign"\n'
        "end\n"
        f"STDOUT.write(JSON.generate({_VAR_NAME}))\n"
    )


def _check_date_calendars(*, ruby: str) -> None:
    """Verify native dates and arithmetic across the Gregorian reform."""
    dates = ("1500-03-01", "1582-10-10", "1582-10-15", "2024-01-15")
    source = "\n".join(f"- {date}" for date in dates)
    for date_format, previous_day in (
        (Ruby.date_formats.RUBY, "1582-10-14"),
        (Ruby.date_formats.RUBY_SHORT, "1582-10-04"),
    ):
        result = literalize(
            source=source,
            input_format=InputFormat.YAML,
            language=Ruby(date_format=date_format),
            variable_form=NewVariable(name=_VAR_NAME, modifiers=frozenset()),
        )
        preamble = "\n".join((*result.preamble, *result.body_preamble))
        program = (
            "# frozen_string_literal: true\n"
            "require 'json'\n"
            f"{preamble}\n{result.code}\n"
            "raise 'date arithmetic changed' unless "
            f"({_VAR_NAME}[2] - 1).iso8601 == '{previous_day}'\n"
            f'STDOUT.write(JSON.generate("dates" => '
            f"{_VAR_NAME}.map(&:iso8601)))\n"
        )
        roundtrip_common.execute(
            label=f"Ruby {date_format.name} calendar",
            source_filename="dates.rb",
            program=program,
            steps=[
                roundtrip_common.Step(
                    args=[ruby, "dates.rb"],
                    failure_label="Ruby date calendar mismatch",
                ),
            ],
            excluded_keys=(),
            expected_json=json.dumps(obj={"dates": dates}),
            extra_files=None,
        )


def _check_datetime_offsets(*, ruby: str) -> None:
    """Native formatter inputs retain exact instants and UTC offsets.

    YAML/TOML timestamps cannot carry these subminute offsets, and Ruby's
    reference framework deliberately rejects native bound references.
    """
    offsets = (
        0,
        19_800_000_000,
        -19_800_000_000,
        1_000_000,
        -1_000_000,
        1,
        -1,
        19_815_000_001,
        -19_815_000_001,
    )
    expressions: list[str] = []
    expected: list[list[int]] = []
    epoch = dt.datetime(year=1970, month=1, day=1, tzinfo=dt.UTC)
    for microseconds in offsets:
        stamp = dt.datetime(
            year=2001,
            month=2,
            day=3,
            hour=4,
            minute=5,
            second=6,
            microsecond=123456,
            tzinfo=dt.timezone(offset=dt.timedelta(microseconds=microseconds)),
        )
        expressions.append(Ruby().format_datetime(stamp))
        instant = Fraction(
            numerator=(stamp - epoch) // dt.timedelta(microseconds=1),
            denominator=1_000_000,
        )
        offset = Fraction(numerator=microseconds, denominator=1_000_000)
        expected.append(
            [
                instant.numerator,
                instant.denominator,
                offset.numerator,
                offset.denominator,
            ]
        )
    program = (
        "require 'json'\n"
        f"values = [{', '.join(expressions)}]\n"
        "actual = values.map { |t| [t.to_r.numerator, t.to_r.denominator, "
        "t.utc_offset.numerator, t.utc_offset.denominator] }\n"
        "STDOUT.write(JSON.generate({values: actual}))\n"
    )
    roundtrip_common.execute(
        label="Ruby native datetime offsets",
        source_filename="offsets.rb",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[ruby, "offsets.rb"],
                failure_label="Ruby datetime offset mismatch",
            )
        ],
        excluded_keys=(),
        expected_json=json.dumps(obj={"values": expected}),
        extra_files=None,
    )


def main() -> None:
    """Round-trip the shared document through the Ruby backend."""
    json_text = roundtrip_common.input_for_capabilities(
        capabilities=Ruby.variant_metadata.round_trip_capabilities,
    )
    program = _build_program(json_text=json_text)
    ruby = shutil.which(cmd="ruby")
    if ruby is None or ruby == "":
        ruby = "ruby"
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="main.rb",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[ruby, "main.rb"],
                failure_label="ruby runtime error",
            ),
        ],
        excluded_keys=(),
        expected_json=json_text,
        extra_files=None,
    )
    _check_date_calendars(ruby=ruby)
    _check_datetime_offsets(ruby=ruby)


if __name__ == "__main__":
    main()
