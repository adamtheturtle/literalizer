r"""Perl JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to a Perl
``my $myData = ...;`` declaration, wrap it in a tiny script that prints
``JSON::PP->new->utf8->allow_bignum->encode($myData)``, run it with
Perl, and hand the emitted JSON to :func:`roundtrip_common.verify`.

Two non-default Perl options are used so the round-trip is faithful for
the values Perl *can* represent:

* ``bool_format=JSON_PP_REF`` renders booleans as ``\1`` / ``\0``,
  which ``JSON::PP`` encodes as JSON ``true`` / ``false``.  The default
  ``INTEGER`` form would collapse booleans to the integers ``1`` / ``0``
  (see issue #2586).
* ``integer_width_strategy=MATH_BIG_INT`` renders integers wider than a
  native scalar via ``Math::BigInt->new("...")``, which the ``JSON::PP``
  ``allow_bignum`` mode then serializes back as a plain JSON integer.
  The default ``BARE`` form would silently demote the 26-digit
  ``biginteger`` field to an NV (see issue #2588).

Large finite floats use core ``Math::BigFloat`` values so JSON::PP's
``allow_bignum`` mode preserves all significant digits on every platform.
``float_large_exponent`` remains excluded because JSON::PP expands that
integral-valued maximum double to a decimal integer whose exact mathematical
value differs from the original binary64 value.

``double_array`` (``[1.0, 2.5]`` -> ``[1, 2.5]``) and ``negative_zero``
(``-0.0`` -> ``0``) survive the comparison because Python treats
``1.0 == 1`` and ``-0.0 == 0`` as equal, so they do not need to be
excluded even though Perl scalars discard the distinction.

This lives here, driven by the ``Perl roundtrip`` step of the
``lint-perl`` job in ``.github/workflows/lint.yml``, because that job is
where the pinned Perl toolchain is installed.  It shares the same input
and comparison logic as the other per-language round-trip helpers.
"""

import dataclasses
import json
import shutil

import click

from literalizer import CollectionLayout, InputFormat, NewVariable, literalize
from literalizer.languages import Perl
from scripts import roundtrip_common

_VAR_NAME = "myData"
_LABEL = "Perl"
_EXCLUDED_KEYS = ("float_large_exponent",)


def _build_program(
    *, json_text: str, language: Perl, layout: CollectionLayout
) -> str:
    """Render a Perl program with the selected options."""
    result = literalize(
        source=json_text,
        input_format=InputFormat.JSON,
        language=language,
        variable_form=NewVariable(name=_VAR_NAME, modifiers=frozenset()),
        collection_layout=layout,
    )
    preamble = "\n".join((*result.preamble, *result.body_preamble))
    return (
        "use strict;\n"
        "use warnings;\n"
        "use JSON::PP;\n"
        f"{preamble}\n"
        f"{result.code}\n"
        "my $json = JSON::PP->new->utf8->allow_bignum->canonical;\n"
        "binmode STDOUT;\n"
        f"print $json->encode(${_VAR_NAME});\n"
    )


def _check_program(
    *,
    perl: str,
    label: str,
    json_text: str,
    language: Perl,
    layout: CollectionLayout,
    excluded_keys: tuple[str, ...],
) -> None:
    """Run one document through Perl's native JSON serializer."""
    roundtrip_common.execute(
        label=label,
        source_filename="main.pl",
        program=_build_program(
            json_text=json_text, language=language, layout=layout
        ),
        steps=[
            roundtrip_common.Step(
                args=[perl, "main.pl"],
                failure_label="perl runtime error",
            ),
        ],
        excluded_keys=excluded_keys,
        expected_json=json_text,
        extra_files=None,
    )


def _check_option_pairs(*, perl: str, language: Perl) -> None:
    """Exercise every pair across string, integer and layout options."""
    json_text = json.dumps(
        obj={
            "text": 'café 日本語, "quotes", \\ and $value',
            "values": [-16384, True, 99999999999999999999999999, []],
        },
        ensure_ascii=False,
    )
    for string_format, integer_format, layout in (
        (
            Perl.string_formats.DOUBLE,
            Perl.integer_formats.HEX,
            CollectionLayout.COMPACT,
        ),
        (
            Perl.string_formats.DOUBLE,
            Perl.integer_formats.OCTAL,
            CollectionLayout.MULTILINE,
        ),
        (
            Perl.string_formats.DOUBLE_UTF8,
            Perl.integer_formats.HEX,
            CollectionLayout.MULTILINE,
        ),
        (
            Perl.string_formats.DOUBLE_UTF8,
            Perl.integer_formats.OCTAL,
            CollectionLayout.COMPACT,
        ),
    ):
        _check_program(
            perl=perl,
            label=(
                f"{_LABEL} {string_format.name}/{integer_format.name}/"
                f"{layout.name}"
            ),
            json_text=json_text,
            language=dataclasses.replace(
                language,
                string_format=string_format,
                integer_format=integer_format,
            ),
            layout=layout,
            excluded_keys=(),
        )


@click.command()
def main() -> None:
    """Round-trip the shared document and the bounded option pairs."""
    json_text = roundtrip_common.input_for_capabilities(
        capabilities=Perl.variant_metadata.round_trip_capabilities,
    )
    language = Perl(
        bool_format=Perl.bool_formats.JSON_PP_REF,
        integer_width_strategy=Perl.integer_width_strategies.MATH_BIG_INT,
    )
    perl = shutil.which(cmd="perl")
    if perl is None or perl == "":
        perl = "perl"
    _check_program(
        perl=perl,
        label=_LABEL,
        json_text=json_text,
        language=language,
        layout=CollectionLayout.COMPACT,
        excluded_keys=_EXCLUDED_KEYS,
    )
    _check_option_pairs(perl=perl, language=language)


if __name__ == "__main__":
    main()
