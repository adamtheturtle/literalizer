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

One key is excluded from the comparison because the Perl JSON encoder
emits floats with only 15 significant digits.  The shared input's
``float_large_exponent`` value is the IEEE 754 ``DBL_MAX``; rounded to
15 digits it becomes ``1.79769313486232e+308``, which on parse rounds
*up* past ``DBL_MAX`` and Python decodes as ``inf``:

* ``float_large_exponent`` -- ``1.7976931348623157e308`` -> ``inf``
  after encode/decode.

``double_array`` (``[1.0, 2.5]`` -> ``[1, 2.5]``) and ``negative_zero``
(``-0.0`` -> ``0``) survive the comparison because Python treats
``1.0 == 1`` and ``-0.0 == 0`` as equal, so they do not need to be
excluded even though Perl scalars discard the distinction.

This lives here, driven by the ``Perl roundtrip`` step of the
``lint-perl`` job in ``.github/workflows/lint.yml``, because that job is
where the pinned Perl toolchain is installed.  It shares the same input
and comparison logic as the other per-language round-trip helpers.
"""

import shutil

import roundtrip_common

from literalizer.languages import Perl

_VAR_NAME = "myData"
_LABEL = "Perl"
_EXCLUDED_KEYS = ("float_large_exponent",)


def _build_program(json_text: str) -> str:
    """Return a runnable Perl program literalized from *json_text*."""
    language = Perl(
        bool_format=Perl.bool_formats.JSON_PP_REF,
        integer_width_strategy=Perl.integer_width_strategies.MATH_BIG_INT,
    )
    result = roundtrip_common.literalize_new_variable(
        language=language,
        json_text=json_text,
        var_name=_VAR_NAME,
        pre_indent_level=0,
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


def main() -> None:
    """Round-trip the shared document through the Perl backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    perl = shutil.which(cmd="perl") or "perl"
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="main.pl",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[perl, "main.pl"],
                failure_label="perl runtime error",
            ),
        ],
        excluded_keys=_EXCLUDED_KEYS,
    )


if __name__ == "__main__":
    main()
